#!/usr/bin/env python3
"""C34 harness — shared library. Committed at M2, before the corpus snapshot,
before any question, and before any provider call.

Carries C29's mechanics verbatim except where the registered deviations say
otherwise (`corpus/conjectures/c34-public-curation-vs-search-replication.md`
§Registered deviations, plus corrections v2 and v3):

  D-1  arm A is not implemented at all (no A_PROMPT, no flat dump).
  D-6  the hydration record is computed for B and C by ONE code path
       (`hydration_record`), never arm-conditionally.
  D-8  README.md is exempt from rule R (see corpus_rule.py).

New relative to C29, and why:
  * ordered Grep/Glob invocations WITH their patterns are recorded, not just a
    count (registration §3 "per-question hydration record");
  * the provider-resolved model identity is extracted from all three sites the
    C31 adapter enumerated (system/init, assistant message, result modelUsage)
    and recorded per run; a mismatch is an instrument-insufficient cause, so it
    must be observable rather than asserted;
  * every provider call is reserved against a durable, non-transferable
    sub-ceiling ledger BEFORE dispatch;
  * error attempts are preserved rather than deleted (C29 deleted them), so
    "no scored answer was ever re-rolled" is checkable by record identity.

Nothing in this module reads any Mentu substrate: the study reads repository
files and calls a model (registration §Release binding).
"""
import hashlib
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SANDBOX = os.path.join("/private/tmp/claude-501", "c34-sandbox")
MANIFEST = os.path.join(HERE, "corpus-manifest.json")
SNAPSHOT_DIR = os.path.join(HERE, "corpus-snapshot")
RUNS = os.path.join(HERE, "runs")
ATTEMPTS = os.path.join(RUNS, "attempts")
LEDGER_PATH = os.path.join(HERE, "call-ledger.jsonl")

# --- pinned identities (registration §4; unchanged from C29 D3) -------------
ANSWERER = "claude-haiku-4-5-20251001"
GENERATOR = "claude-sonnet-5"

NO_TOOLS = ["--disallowedTools", "Bash", "Read", "Grep", "Glob", "Write",
            "Edit", "WebFetch", "WebSearch", "Task", "Agent", "Skill",
            "NotebookEdit", "TodoWrite"]

# Verified precondition (correction v3 G5): the corpus is pinned to the
# cb73654 tree, so the <135 and >170 branches are dead and this single
# assertion replaces both. Duplicated from corpus_rule.py deliberately — the
# sandbox must fail closed even if enumeration is not re-run.
EXPECTED_CORPUS_FILES = 141

# --- registered call budget (registration §4) -------------------------------
GLOBAL_CEILING = 950
SUB_CEILINGS = {
    "reality_probe": 2,     # 1 generator + 1 answerer; runs FIRST (v2 C-5)
    "generation": 170,      # 1 per eligible file, cap
    "regeneration": 45,     # dropped-file regeneration pass, cap
    "digest": 170,          # 1 per file lacking an extractable digest, cap
    "smoke": 30,            # 10 excluded questions x 3 policies
    "confirmatory": 360,    # 120 questions x 3 policies
    "retry": 150,           # registered error classes only, non-transferable
}

# --- registered retry classes (registration §4, "tightened") ----------------
RETRYABLE = ("provider_session_limit", "transport_failure_before_content",
             "subprocess_timeout")
SESSION_LIMIT_MARKERS = ("session limit", "usage limit", "rate limit",
                         "overloaded")


class CeilingExhausted(RuntimeError):
    """A registered sub-ceiling or the global ceiling is spent. Never raised
    into a threshold relaxation: the caller seals instrument-insufficient with
    reason `registered_budget_exhausted`."""


class ProbeNotRun(RuntimeError):
    """The two-call reality probe has not completed. Correction v2 C-5 orders
    it BEFORE every other provider call — availability is bought before the
    generation budget is spent, not assumed (Phase-H rule 3)."""


class LedgerIntegrityError(RuntimeError):
    """The durable call ledger does not verify. Raised on load, never
    swallowed: a ledger that has lost or gained lines under-counts, and the
    failure direction of an under-count is overspending a ceiling that is
    never allowed to be raised."""


GENESIS_SEAL = "0" * 64


def _seal(prev_seal, entry):
    """Running digest over the chain. Detects truncation, accidental
    corruption and any edit that does not re-seal the whole chain forward.
    It is not a defense against a determined forger with write access — no
    unauthenticated hash chain is, C33's `record_sha256` included."""
    payload = json.dumps({k: v for k, v in entry.items() if k != "seal"},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((prev_seal + payload).encode()).hexdigest()


# ---------------------------------------------------------------------------
# Durable call ledger
# ---------------------------------------------------------------------------
class CallLedger:
    """Append-only provider-call ledger, checked and durably recorded BEFORE
    every call (registration §4). Sub-ceilings are non-transferable: unused
    budget in one bucket never funds another.

    Reservation-before-dispatch means a crash between the two counts a call
    that never reached the provider. That is the safe direction against a
    registered ceiling and is deliberate.

    Cross-run discovery (the C33 pattern): a ledger file that lost entries
    would under-count and silently overspend the ceiling, so `discover()`
    reconciles durable artifacts against the ledger by call key before any new
    reservation. Keys that exist as artifacts but not in the ledger are
    appended as `discovered` entries. The count only ever moves up.

    Integrity and recovery are deliberately separated, because they pull in
    opposite directions and integrity wins:

      * a ledger that is INCONSISTENT with itself or with its head record —
        truncated, edited, a gap in `seq`, a hand-appended entry — raises on
        load. Nothing proceeds on a doubtful count;
      * a ledger that is wholly ABSENT (both the journal and its head record)
        is a loss, not a corruption. It starts from genesis and `discover()`
        rebuilds it from the artifacts the calls produced.

    So deleting the journal while leaving the head record is refused rather
    than silently recovered: that state is indistinguishable from truncation,
    and resolving it is an operator decision, not a harness default.
    """

    def __init__(self, path=LEDGER_PATH):
        import threading
        self.path = path
        self.head_path = path + ".head.json"
        self.lock = threading.Lock()
        self.entries = []
        self.head_seal = GENESIS_SEAL
        if os.path.exists(path):
            self._load()

    def _load(self):
        """Verify the whole chain before any reservation is made. Every
        inconsistency raises; nothing proceeds on a doubtful count."""
        with open(self.path) as fh:
            lines = [ln for ln in fh.read().splitlines() if ln.strip()]
        prev = GENESIS_SEAL
        for i, line in enumerate(lines):
            try:
                e = json.loads(line)
            except ValueError as exc:
                raise LedgerIntegrityError(
                    f"call ledger line {i} does not parse (truncated write?): "
                    f"{exc}") from exc
            if e.get("seq") != i:
                raise LedgerIntegrityError(
                    f"call ledger seq gap at line {i}: entry claims "
                    f"seq={e.get('seq')}")
            want = _seal(prev, e)
            if e.get("seal") != want:
                raise LedgerIntegrityError(
                    f"call ledger seal mismatch at line {i}: the entry was "
                    "edited, or the chain was rewritten")
            prev = e["seal"]
            self.entries.append(e)
        if os.path.exists(self.head_path):
            with open(self.head_path) as fh:
                head = json.load(fh)
            if head.get("entries") != len(self.entries) or \
                    head.get("head_seal") != prev:
                raise LedgerIntegrityError(
                    f"call ledger head mismatch: head records "
                    f"{head.get('entries')} entries, file holds "
                    f"{len(self.entries)} (truncated?)")
        self.head_seal = prev

    # -- accounting --------------------------------------------------------
    def counts(self):
        c = {b: 0 for b in SUB_CEILINGS}
        for e in self.entries:
            c[e["bucket"]] = c.get(e["bucket"], 0) + 1
        return c

    def total(self):
        return len(self.entries)

    def keys(self):
        return {e["key"] for e in self.entries}

    def remaining(self, bucket):
        return SUB_CEILINGS[bucket] - self.counts().get(bucket, 0)

    # -- durable append ----------------------------------------------------
    def _append(self, entry):
        entry["seal"] = _seal(self.head_seal, entry)
        self.entries.append(entry)
        with open(self.path, "a") as fh:
            fh.write(json.dumps(entry, sort_keys=True) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        self.head_seal = entry["seal"]
        with open(self.head_path, "w") as fh:
            json.dump({"entries": len(self.entries),
                       "head_seal": self.head_seal}, fh, sort_keys=True)
            fh.flush()
            os.fsync(fh.fileno())
        return entry

    def probe_complete(self):
        return self.counts().get("reality_probe", 0) >= \
            SUB_CEILINGS["reality_probe"]

    def discover(self, artifact_keys):
        """artifact_keys: {bucket: iterable of call keys already spent}.
        Appends `discovered` entries for keys absent from the ledger."""
        known = self.keys()
        found = []
        for bucket, ks in sorted(artifact_keys.items()):
            for k in sorted(set(ks)):
                if k not in known:
                    found.append(self._append(
                        {"seq": len(self.entries), "bucket": bucket, "key": k,
                         "ts": None, "origin": "discovered"}))
                    known.add(k)
        return found

    def reserve(self, bucket, key, model):
        """Record a call BEFORE dispatching it. Raises CeilingExhausted or
        ProbeNotRun; never returns a reservation the ceilings do not allow."""
        if bucket not in SUB_CEILINGS:
            raise ValueError(f"unregistered budget bucket: {bucket}")
        with self.lock:
            if bucket != "reality_probe" and not self.probe_complete():
                raise ProbeNotRun(
                    "reality probe incomplete "
                    f"({self.counts().get('reality_probe', 0)}/"
                    f"{SUB_CEILINGS['reality_probe']}); correction v2 C-5 "
                    f"orders it before any {bucket} call")
            c = self.counts()
            if c.get(bucket, 0) >= SUB_CEILINGS[bucket]:
                raise CeilingExhausted(
                    f"sub-ceiling exhausted: {bucket} "
                    f"{c[bucket]}/{SUB_CEILINGS[bucket]}")
            if self.total() >= GLOBAL_CEILING:
                raise CeilingExhausted(
                    f"global ceiling exhausted: "
                    f"{self.total()}/{GLOBAL_CEILING}")
            return self._append(
                {"seq": len(self.entries), "bucket": bucket, "key": key,
                 "model": model, "ts": round(time.time(), 3),
                 "origin": "reserved"})


def write_stop(reason, detail, here):
    """Seal an instrument-insufficient stop. The adjudicator reads these.

    `here` is REQUIRED and has no default. During M2 a default of this
    module's own directory let test-written STOP markers land in the real
    study directory, where one would have sealed the real adjudication
    `instrument-insufficient`. The fix is the removal of the default, not a
    correction of the call sites that used it."""
    path = os.path.join(here, f"STOP-{reason}.json")
    with open(path, "w") as fh:
        json.dump({"reason": reason, "detail": detail,
                   "ts": round(time.time(), 3)}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return path


def stop_markers(here=HERE):
    out = []
    if not os.path.isdir(here):
        return out
    for name in sorted(os.listdir(here)):
        if name.startswith("STOP-") and name.endswith(".json"):
            with open(os.path.join(here, name)) as fh:
                out.append(json.load(fh))
    return out


# ---------------------------------------------------------------------------
# Text mechanics (carried verbatim from C29 harness_lib)
# ---------------------------------------------------------------------------
def strip_frontmatter(text):
    """Return (frontmatter_block or '', body). Mechanical, provable."""
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines(keepends=True)
    for i, l in enumerate(lines[1:], 1):
        if l.strip() == "---":
            return "".join(lines[:i + 1]), "".join(lines[i + 1:])
    return "", text


def digest_from_frontmatter(fm):
    """Mechanical digest: summary|description|title field, first found."""
    for key in ("summary", "description", "title"):
        m = re.search(rf"^{key}:\s*(.+?)$", fm, re.M)
        if m:
            v = m.group(1).strip().strip("\"'")
            if v and v != ">-" and not v.startswith(("|", ">")):
                return v[:200]
    return None


def normalize(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def answer_line(text):
    for line in reversed((text or "").splitlines()):
        if line.strip().upper().startswith("ANSWER:"):
            return line.split(":", 1)[1].strip()
    return (text or "").strip()[-500:]


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# Sandbox: assembled from the committed snapshot, hash-verified per file
# ---------------------------------------------------------------------------
def load_manifest(path=MANIFEST):
    with open(path) as fh:
        return json.load(fh)


def build_sandbox(manifest_path=MANIFEST, snapshot_dir=SNAPSHOT_DIR,
                  sandbox=SANDBOX, expect_files=EXPECTED_CORPUS_FILES):
    """Assemble the run sandbox from the committed snapshot with per-file
    sha256 verification. Never reads the live working tree (registration §1).
    Returns {relpath: {"path", "size", "sha256"}}."""
    import shutil
    man = load_manifest(manifest_path)
    entries = man["entries"]
    if expect_files is not None and len(entries) != expect_files:
        raise SystemExit(
            f"CORPUS PRECONDITION FAILED at sandbox assembly: manifest has "
            f"{len(entries)} files, registered precondition is {expect_files} "
            "(correction v3 G5). Stopping before any provider call.")
    if os.path.isdir(sandbox):
        shutil.rmtree(sandbox)
    mapping = {}
    for e in sorted(entries, key=lambda x: x["path"]):
        src = os.path.join(snapshot_dir, e["path"])
        with open(src, "rb") as fh:
            raw = fh.read()
        got = sha256_bytes(raw)
        if got != e["sha256"] or len(raw) != e["size"]:
            raise SystemExit(
                "SNAPSHOT HASH MISMATCH, corpus not frozen: "
                f"{e['path']} (manifest {e['sha256'][:12]}, "
                f"snapshot {got[:12]})")
        dest = os.path.join(sandbox, e["path"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(raw)
        mapping[e["path"]] = dict(e)
    return mapping


def read_snapshot(rp, snapshot_dir=SNAPSHOT_DIR):
    with open(os.path.join(snapshot_dir, rp), "rb") as fh:
        return fh.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Hydration record — ONE code path for B and C (deviation D-6)
# ---------------------------------------------------------------------------
def located_in(reads, gold_rp):
    """C29's committed hydration rule, unchanged: any recorded read path ends
    with, or contains, the question's gold relative path."""
    return any(rd.endswith(gold_rp) or gold_rp in rd for rd in reads)


def hydration_record(reads, searches, gold_rp):
    """The frozen per-question hydration record (registration §3). Computed
    identically for B and C — C29 computed it only under `if p == "C"`, which
    is the defect deviation D-6 repairs."""
    reads = list(reads)
    first = reads[0] if reads else None
    return {
        "reads": reads,
        "searches": list(searches),
        "read_count": len(reads),
        "first_read_path": first,
        "located": located_in(reads, gold_rp),
        "first_read_is_gold": bool(
            first is not None and located_in([first], gold_rp)),
        "zero_read": len(reads) == 0,
    }


HYDRATION_FIELDS = ("reads", "searches", "read_count", "first_read_path",
                    "located", "first_read_is_gold", "zero_read")


def hydration_complete(rec):
    """A scored B or C run missing any hydration field is a floor failure, not
    a footnote (deviation D-6)."""
    h = rec.get("hydration")
    if not isinstance(h, dict):
        return False
    return all(k in h for k in HYDRATION_FIELDS)


# ---------------------------------------------------------------------------
# Provider-resolved model identity
# ---------------------------------------------------------------------------
def model_identities(events):
    """Every model identity the provider reported, from the three sites the
    C31 adapter enumerated. Returns a sorted list; the smoke audit and the
    adjudicator require it to equal [pinned]."""
    ids = set()
    for ev in events:
        if not isinstance(ev, dict):
            continue
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            if isinstance(ev.get("model"), str):
                ids.add(ev["model"])
        if ev.get("type") == "assistant":
            msg = ev.get("message")
            if isinstance(msg, dict) and isinstance(msg.get("model"), str):
                ids.add(msg["model"])
        if ev.get("type") == "result" or "usage" in ev:
            mu = ev.get("modelUsage", ev.get("model_usage"))
            if isinstance(mu, dict):
                ids.update(k for k in mu if isinstance(k, str))
            if isinstance(ev.get("model"), str):
                ids.add(ev["model"])
    return sorted(ids)


def classify_error(rec, stderr=""):
    """Registered infrastructure classes only; everything else is
    non-retryable (registration §4: a scored answer is never re-rolled)."""
    if rec.get("error") == "timeout":
        return "subprocess_timeout"
    blob = " ".join([str(rec.get("result_text") or ""), str(stderr or "")])
    low = blob.lower()
    if any(m in low for m in SESSION_LIMIT_MARKERS):
        return "provider_session_limit"
    if rec.get("error") == "unparseable" and not rec.get("saw_assistant"):
        return "transport_failure_before_content"
    if rec.get("is_error"):
        return "provider_error_unclassified"
    return None


# ---------------------------------------------------------------------------
# The one pinned provider entry point
# ---------------------------------------------------------------------------
def parse_events(raw):
    """stream-json -> [event]. Non-JSON lines are ignored, as C29 did."""
    events = []
    for line in (raw or "").splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    return events


def record_from_events(events, model):
    """Token components, tool events and resolved identity from a stream."""
    reads, searches, saw_assistant = [], [], False
    result_ev = None
    for ev in events:
        if ev.get("type") == "assistant":
            saw_assistant = True
            for b in ((ev.get("message") or {}).get("content") or []):
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    inp = b.get("input") or {}
                    if b.get("name") == "Read":
                        reads.append(inp.get("file_path", ""))
                    elif b.get("name") in ("Grep", "Glob"):
                        searches.append({
                            "tool": b.get("name"),
                            "pattern": inp.get("pattern") or inp.get("glob")
                            or inp.get("query") or "",
                            "path": inp.get("path") or ""})
        elif ev.get("type") == "result":
            result_ev = ev
    d = result_ev or {}
    return _usage_record(d, model, events, reads, searches, saw_assistant)


def _usage_record(d, model, events, reads, searches, saw_assistant):
    usage = d.get("usage") or {}
    uncached = usage.get("input_tokens", 0)
    cc = usage.get("cache_creation_input_tokens", 0)
    cr = usage.get("cache_read_input_tokens", 0)
    out = usage.get("output_tokens", 0)
    return {
        "result_text": d.get("result", ""),
        "answer": answer_line(d.get("result", "")),
        # components kept separate: nested-CLI system-prompt overhead lives
        # mostly in cache_read, and P4 adjudicates on marginal tokens (D-3)
        "input_uncached": uncached,
        "cache_creation_tokens": cc,
        "cache_read_tokens": cr,
        "input_tokens": uncached + cc + cr,      # frozen "total input" reading
        "output_tokens": out,
        "tokens_total": uncached + cc + cr + out,
        "tokens_marginal": uncached + cc + out,
        "cost_usd": d.get("total_cost_usd"),
        "num_turns": d.get("num_turns"),
        "reads": reads, "searches": searches,
        "saw_assistant": saw_assistant,
        "model_requested": model,
        "model_identities": model_identities(events),
        "is_error": d.get("is_error", False),
    }


def run_claude(prompt, model, allowed_tools=None, cwd=None, stream=False,
               timeout=420, ledger=None, bucket=None, key=None):
    """One pinned headless call; returns a raw record (never raises except on
    an exhausted registered ceiling).

    The ledger reservation happens BEFORE dispatch (registration §4). Callers
    that pass no ledger are offline callers (tests); a live pass always passes
    one, and `run_policies`/`generate_questions` require it.
    """
    if ledger is not None:
        ledger.reserve(bucket, key, model)
    cmd = ["claude", "-p", "--model", model, "--no-session-persistence",
           "--output-format", "stream-json" if stream else "json"]
    if stream:
        cmd.append("--verbose")
    if allowed_tools:
        cmd += ["--allowedTools"] + allowed_tools
    else:
        cmd += NO_TOOLS
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, input=prompt, capture_output=True,
                              text=True, cwd=cwd or HERE, timeout=timeout)
        raw, stderr = proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        rec = {"error": "timeout", "duration_s": round(time.time() - t0, 1),
               "started_at": round(t0, 3), "model_requested": model}
        rec["error_class"] = classify_error(rec)
        return rec
    if stream:
        events = parse_events(raw)
        rec = record_from_events(events, model)
    else:
        try:
            d = json.loads(raw)
        except ValueError:
            rec = {"error": "unparseable", "stderr": stderr[-500:],
                   "duration_s": round(time.time() - t0, 1),
                   "started_at": round(t0, 3),
                   "model_requested": model, "saw_assistant": False}
            rec["error_class"] = classify_error(rec, stderr)
            return rec
        rec = _usage_record(d, model, [d], [], [], True)
    rec["started_at"] = round(t0, 3)
    rec["duration_s"] = round(time.time() - t0, 1)
    rec["error_class"] = classify_error(rec, stderr)
    return rec
