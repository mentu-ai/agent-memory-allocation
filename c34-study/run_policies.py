#!/usr/bin/env python3
"""C34 — policy runner and campaign entrypoint (M5/M6; only after the
question-freeze commit).

Three arms, symmetrically instrumented (registration §3). Arm A is NOT
implemented: deviation D-1 drops the flat-load arm, so there is no A_PROMPT
and no corpus dump in this harness at all.

Ordering, enforced mechanically rather than by convention:
  * the two-call reality probe runs FIRST (correction v2 C-5) — the call
    ledger refuses to reserve any other bucket until it has completed;
  * then the excluded smoke set (10 questions x 3 policies), audited;
  * then the confirmatory pass (120 x 3).

Per-record discipline:
  * one JSON record per (question, policy); idempotent and resumable — an
    existing SCORED record is never overwritten, so no scored answer can be
    re-rolled (registration §4);
  * every attempt, including errors, is appended to runs/attempts/ so
    "no scored answer was re-rolled" is checkable by record identity rather
    than by assertion (C29 deleted its error records);
  * retries only for the registered infrastructure classes, only against the
    non-transferable retry reserve, each recorded with its class;
  * a hydration record is written for B and C alike (deviation D-6);
  * smoke records carry `barred_from_adjudication: true` in the record itself.

Usage:
  python3 run_policies.py --stage probe
  python3 run_policies.py --stage smoke
  python3 run_policies.py --stage confirmatory [--retry]
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import harness_lib as H
from build_index import index_text

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-08-13"
POLICIES = ("B", "C", "D")
AGENTIC = ("B", "C")
TIMEOUT_AGENTIC = 900     # C29's committed 420 -> 900 s amendment
TIMEOUT_SINGLE = 420
D_DOC_CHARS = 60_000      # carried verbatim from C29 run_policies

# ---------------------------------------------------------------------------
# Frozen treatment prompts — BYTE-VERBATIM from C29's run_policies.py lines
# 22-56 at cb73654, pinned by registration correction v2 C-1. A_PROMPT is not
# carried (deviation D-1). `test_prompts_frozen.py` byte-compares these
# against the strings pinned in the correction document itself; a
# one-character change fails the test.
# ---------------------------------------------------------------------------
COMMON = ("\nReply with your final line exactly as 'ANSWER: <the answer>' — "
          "the answer should be the exact wording from the document.")

B_PROMPT = """Answer the question using the markdown corpus in the current
directory. Use Grep/Glob to find relevant files and Read to inspect them.
Be efficient.{common}

QUESTION: {q}"""

C_PROMPT = """Answer the question about the markdown corpus in the current
directory. Below is an INDEX of every file (path — one-line digest).
Protocol: consult the index first; if it already answers the question, answer
directly. Otherwise Read the FEWEST files needed (paths are relative to the
current directory). Do not read more than necessary.{common}

INDEX:
{index}

QUESTION: {q}"""

D_PROMPT = """Answer the question from the single document below.
Do not use any tools.

DOCUMENT ({rp}):
{doc}

QUESTION: {q}{common}"""

PROBE_PROMPT = "Reply with the single word OK and nothing else."


def build_prompt(q, policy, index_block, snapshot_dir=H.SNAPSHOT_DIR):
    if policy == "B":
        return B_PROMPT.format(common=COMMON, q=q["question"])
    if policy == "C":
        return C_PROMPT.format(common=COMMON, q=q["question"],
                               index=index_block)
    if policy == "D":
        doc = H.read_snapshot(q["rp"], snapshot_dir)
        return D_PROMPT.format(common=COMMON, q=q["question"], rp=q["rp"],
                               doc=doc[:D_DOC_CHARS])
    raise ValueError(f"unregistered policy: {policy}")


def is_scored(rec):
    """A record is scored iff it carries no error. Scored records are frozen:
    the runner never rewrites one."""
    return not (rec.get("error") or rec.get("is_error"))


class ScoredRecordExists(RuntimeError):
    """An attempt was made to overwrite a scored run record. Registration §4:
    a scored answer is never re-rolled. The guarantee lives at the WRITE SITE
    rather than in the job planner, so it holds by construction for every
    caller rather than by the shape of the call graph."""


class Campaign:
    """The paths one campaign runs against. Kept explicit so the runner is
    exercisable offline against a fixture study directory."""

    def __init__(self, study=HERE, date=DATE):
        self.study = study
        self.runs = os.path.join(study, "runs")
        self.attempts = os.path.join(self.runs, "attempts")
        self.q_file = os.path.join(study, f"questions-{date}.json")
        self.i_file = os.path.join(study, f"index-{date}.json")
        self.manifest = os.path.join(study, "corpus-manifest.json")
        self.snapshot = os.path.join(study, "corpus-snapshot")
        self.sandbox = H.SANDBOX
        self.ledger_path = os.path.join(study, "call-ledger.jsonl")
        self.probe_out = os.path.join(study, "reality-probe.json")
        self.expect_files = H.EXPECTED_CORPUS_FILES

    # -- durable record paths ---------------------------------------------
    def record_path(self, qid, policy):
        return os.path.join(self.runs, f"{qid}_{policy}.json")

    def attempts_path(self, qid, policy):
        return os.path.join(self.attempts, f"{qid}_{policy}.jsonl")

    def existing(self, qid, policy):
        p = self.record_path(qid, policy)
        if not os.path.exists(p):
            return None
        with open(p) as fh:
            return json.load(fh)

    def attempt_count(self, qid, policy):
        p = self.attempts_path(qid, policy)
        if not os.path.exists(p):
            return 0
        with open(p) as fh:
            return sum(1 for line in fh if line.strip())

    def write_record(self, qid, policy, rec):
        """The single write site for run records. Refuses to overwrite a
        scored record, whoever the caller is (registration §4)."""
        prev = self.existing(qid, policy)
        if prev is not None and is_scored(prev):
            raise ScoredRecordExists(
                f"{qid}_{policy} already holds a scored record; a scored "
                "answer is never re-rolled (registration §4)")
        os.makedirs(self.runs, exist_ok=True)
        with open(self.record_path(qid, policy), "w") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)

    def append_attempt(self, qid, policy, rec):
        os.makedirs(self.attempts, exist_ok=True)
        with open(self.attempts_path(qid, policy), "a") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")

    def ledger(self):
        led = H.CallLedger(self.ledger_path)
        led.discover({**self.probe_keys(), **self.discoverable_keys()})
        return led

    def discoverable_keys(self):
        """Cross-run discovery: call keys provable from durable run artifacts.
        Every attempt line carries its bucket and its key, so a lost ledger is
        rebuilt from the records the calls produced rather than trusted."""
        out = {}
        if not os.path.isdir(self.attempts):
            return out
        for name in sorted(os.listdir(self.attempts)):
            if not name.endswith(".jsonl"):
                continue
            with open(os.path.join(self.attempts, name)) as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    r = json.loads(line)
                    b, k = r.get("budget_bucket"), r.get("call_key")
                    if b and k:
                        out.setdefault(b, []).append(k)
        return out

    def probe_keys(self):
        """The probe writes no run record, so its two calls are discovered
        from the probe artifact instead."""
        if not os.path.exists(self.probe_out):
            return {}
        with open(self.probe_out) as fh:
            d = json.load(fh)
        keys = [v["call_key"] for k, v in sorted(d.items())
                if isinstance(v, dict) and v.get("call_key")]
        return {"reality_probe": keys} if keys else {}

    # -- stages ------------------------------------------------------------
    def reality_probe(self):
        """Two budgeted calls: model availability + schema acceptance,
        generator and answerer (registration §4; ordered first by C-5)."""
        led = self.ledger()
        out = {}
        for role, model in (("generator", H.GENERATOR),
                            ("answerer", H.ANSWERER)):
            key = f"probe:{role}"
            rec = H.run_claude(PROBE_PROMPT, model, ledger=led,
                               bucket="reality_probe", key=key,
                               timeout=TIMEOUT_SINGLE)
            out[role] = {
                "call_key": key,
                "model_requested": model,
                "model_identities": rec.get("model_identities", []),
                "identity_matches_pin":
                    rec.get("model_identities") == [model],
                "input_tokens_nonzero": bool(rec.get("input_tokens", 0)),
                "is_error": bool(rec.get("error") or rec.get("is_error")),
                "error_class": rec.get("error_class"),
                "answer": (rec.get("answer") or "")[:200],
            }
        ok = all(v["identity_matches_pin"] and v["input_tokens_nonzero"]
                 and not v["is_error"] for v in out.values())
        out["probe_passed"] = ok
        with open(self.probe_out, "w") as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
            fh.write("\n")
        if not ok:
            H.write_stop("pinned_answerer_unavailable", out,
                         here=self.study)
        return out

    def run_one(self, q, policy, index_block, led, bucket, which_set, key):
        prompt = build_prompt(q, policy, index_block, self.snapshot)
        kw = dict(ledger=led, bucket=bucket, key=key)
        if policy == "B":
            rec = H.run_claude(prompt, H.ANSWERER,
                               allowed_tools=["Grep", "Glob", "Read"],
                               cwd=self.sandbox, stream=True,
                               timeout=TIMEOUT_AGENTIC, **kw)
        elif policy == "C":
            rec = H.run_claude(prompt, H.ANSWERER, allowed_tools=["Read"],
                               cwd=self.sandbox, stream=True,
                               timeout=TIMEOUT_AGENTIC, **kw)
        else:
            rec = H.run_claude(prompt, H.ANSWERER, timeout=TIMEOUT_SINGLE,
                               **kw)
        rec.update({"qid": q["id"], "policy": policy, "gold_rp": q["rp"],
                    "qtype": q.get("qtype"), "set": which_set,
                    "barred_from_adjudication": which_set == "smoke",
                    "budget_bucket": bucket, "call_key": key,
                    "ledger_position": led.total()})
        # deviation D-6: ONE code path, both agentic arms, never `if p == "C"`
        if policy in AGENTIC:
            rec["hydration"] = H.hydration_record(
                rec.get("reads", []), rec.get("searches", []), q["rp"])
        rec.pop("result_text", None)         # keep records compact; answer kept
        return rec

    def plan(self, questions, bucket, retry):
        """(question, policy, budget bucket) for every call still owed. A
        scored record is never re-run: no re-rolling (registration §4)."""
        jobs = []
        for q in questions:
            for p in POLICIES:
                prev = self.existing(q["id"], p)
                if prev is None:
                    jobs.append((q, p, bucket))
                elif not is_scored(prev):
                    if retry and prev.get("error_class") in H.RETRYABLE:
                        jobs.append((q, p, "retry"))
        return jobs

    def run_stage(self, which_set, retry=False, workers=3):
        with open(self.q_file) as fh:
            qdata = json.load(fh)
        with open(self.i_file) as fh:
            index_block = index_text(json.load(fh)["index"])
        questions = [q for q in qdata["questions"] if q["set"] == which_set]
        bucket = "smoke" if which_set == "smoke" else "confirmatory"

        os.makedirs(self.runs, exist_ok=True)
        os.makedirs(self.attempts, exist_ok=True)
        H.build_sandbox(self.manifest, self.snapshot, self.sandbox,
                        expect_files=self.expect_files)
        led = self.ledger()
        if not led.probe_complete():
            raise SystemExit("reality probe not complete — run `--stage "
                             "probe` first (correction v2 C-5).")
        jobs = self.plan(questions, bucket, retry)

        def run(job):
            q, p, b = job
            prev = self.existing(q["id"], p)
            key = f"{b}:{q['id']}:{p}#{self.attempt_count(q['id'], p)}"
            try:
                rec = self.run_one(q, p, index_block, led, b, which_set, key)
            except H.CeilingExhausted as exc:
                H.write_stop("registered_budget_exhausted",
                             {"stage": which_set, "qid": q["id"],
                              "policy": p, "detail": str(exc)},
                             here=self.study)
                raise
            rec["retry_of_class"] = ((prev or {}).get("error_class")
                                     if b == "retry" else None)
            self.append_attempt(q["id"], p, rec)
            self.write_record(q["id"], p, rec)
            return rec

        print(f"stage={which_set} jobs={len(jobs)}", flush=True)
        done = 0
        with ThreadPoolExecutor(workers) as ex:
            for _ in ex.map(run, jobs):
                done += 1
                if done % 20 == 0:
                    print(f"done {done}/{len(jobs)}", flush=True)
        print(f"complete: {done} records; ledger {led.total()}/"
              f"{H.GLOBAL_CEILING}")
        return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True,
                    choices=("probe", "smoke", "confirmatory"))
    ap.add_argument("--retry", action="store_true",
                    help="retry records whose error class is registered")
    args = ap.parse_args()
    camp = Campaign()
    if args.stage == "probe":
        out = camp.reality_probe()
        print(json.dumps(out, indent=1, sort_keys=True))
        return 0 if out["probe_passed"] else 1
    camp.run_stage(args.stage, retry=args.retry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
