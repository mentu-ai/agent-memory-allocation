#!/usr/bin/env python3
"""C34 — question-set generation (M4; runs AFTER the corpus-snapshot commit,
BEFORE any policy run; the outputs are then frozen by commit with sha256).

Contract, carried from C29 D4 and registration §2:
  * ONE factual question per eligible corpus file, answer an exact contiguous
    string from the body, 3-15 words, generator-labeled lookup|synthesis;
  * the generator receives FRONTMATTER-STRIPPED BODIES ONLY, by the committed
    mechanical strip, so "generation did not use the summary layers" is
    provable by construction rather than asserted;
  * generation input is `body[:8000]` — carried verbatim from C29 for
    comparability with the parent (correction v2 C-4). Disclosed consequence
    on this corpus (correction v3 G1): 50 of 141 files exceed 8,000 bytes;
    292,894 of 1,162,998 corpus bytes (25.2%) are unreachable to the
    generator, concentrating gold answers toward document heads;
  * mechanical validation = normalized exact-substring containment in the
    body; non-occurring candidates are dropped and counted;
  * ONE regeneration pass, in ASCENDING QUESTION ID until the 45-call
    sub-ceiling binds; files still unregenerated when it binds are recorded as
    dropped (correction v2 C-7);
  * question ids are assigned per SOURCE FILE in ascending path order before
    any validation, so "ascending question id" is well defined for the
    regeneration order and dropped files leave visible gaps.

Digests are NOT authored here: digest authoring is a separate committed pass
(`build_index.py`), per the registration's exposure rule 2.

Usage: python3 generate_questions.py            # full pass
       python3 generate_questions.py --select-only   # re-run frozen selection
"""
import argparse
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import harness_lib as H

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "gen-cache")
DATE = "2026-08-13"
Q_OUT = os.path.join(HERE, f"questions-{DATE}.json")
SELECT_OUT = os.path.join(HERE, f"selection-{DATE}.json")

# --- frozen salts (registration §2; fixed before any question existed) ------
CONFIRMATORY_SALT = "c34-confirmatory-v1:"
SMOKE_SALT = "c34-smoke-v1:"
N_CONFIRMATORY = 120
N_SMOKE = 10

# ---------------------------------------------------------------------------
# Frozen treatment prompt — BYTE-VERBATIM from C29's generate_questions.py
# lines 40-55 at cb73654, pinned by registration correction v2 C-1.
# Any deviation discovered here is a registration matter, not an
# implementation choice. `test_prompts_frozen.py` byte-compares these against
# the strings pinned in the correction document itself.
# ---------------------------------------------------------------------------
Q_PROMPT = """From the document body below, write ONE factual question that
can be answered ONLY from this text. The answer MUST be an exact contiguous
string copied from the text, 3-15 words. Classify the question as "lookup"
(single fact) or "synthesis" (relates two parts of the text).
Reply with ONLY a JSON object: {{"question": "...", "answer": "...",
"qtype": "lookup|synthesis"}}

DOCUMENT BODY ({rp}):
{body}"""

S_PROMPT = """Write a one-line summary (max 140 characters) of what this
document is and contains, useful for deciding whether to open it.
Reply with ONLY the summary line.

DOCUMENT BODY ({rp}):
{body}"""

GEN_INPUT_CHARS = 8000          # correction v2 C-4, verbatim from C29
RETRY_NOTE = ("\n\nIMPORTANT: your previous answer was not an exact "
              "substring. The answer must be copied verbatim.")


def cache_path(key):
    os.makedirs(CACHE, exist_ok=True)
    return os.path.join(
        CACHE, hashlib.sha256(key.encode()).hexdigest()[:24] + ".json")


def cached_keys():
    """{bucket: [call key]} for every cached generator output — the durable
    artifacts the ledger's cross-run discovery reconciles against."""
    out = {}
    if not os.path.isdir(CACHE):
        return out
    for name in sorted(os.listdir(CACHE)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(CACHE, name)) as fh:
            d = json.load(fh)
        out.setdefault(d["bucket"], []).append(d["key"])
    return out


def cached(bucket, key, fn):
    """Resumability: a cached model output is not a new provider call, so it
    is not charged again to the registered ceiling."""
    path = cache_path(key)
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)["value"]
    val = fn()
    with open(path, "w") as fh:
        json.dump({"bucket": bucket, "key": key, "value": val}, fh)
    print(f"[gen] {bucket} {key}", flush=True)
    return val


def gen_input(rp, snapshot_dir=H.SNAPSHOT_DIR):
    """The exact bytes the generator sees, and their provenance hash."""
    text = H.read_snapshot(rp, snapshot_dir)
    _fm, body = H.strip_frontmatter(text)
    body = body.strip()
    sent = body[:GEN_INPUT_CHARS]
    return body, sent, hashlib.sha256(sent.encode("utf-8")).hexdigest()


def validate(candidate, body):
    """Mechanical validation, carried from C29: normalized containment of the
    proposed answer in the source body."""
    ans = candidate.get("answer", "")
    if not ans:
        return "empty_answer"
    if H.normalize(ans) not in H.normalize(body):
        return "answer_not_in_body"
    return None


def gen_one(qid, rp, ledger, bucket, retry_note=""):
    body, sent, gen_sha = gen_input(rp)
    if len(body.splitlines()) < 8:
        return {"id": qid, "rp": rp, "skip": "too_short"}
    prompt = Q_PROMPT.format(rp=rp, body=sent) + retry_note
    rec = H.run_claude(prompt, H.GENERATOR, ledger=ledger, bucket=bucket,
                       key=f"{bucket}:{rp}")
    base = {"id": qid, "rp": rp, "generation_input_sha256": gen_sha,
            "generation_input_chars": len(sent),
            "gen_tokens": rec.get("tokens_total", 0),
            "generator": H.GENERATOR}
    txt = rec.get("result_text", "")
    try:
        q = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])
    except (ValueError, KeyError):
        return {**base, "fail": "unparseable"}
    bad = validate(q, body)
    if bad:
        return {**base, "fail": bad, "candidate": q}
    return {**base, "question": q["question"], "answer": q["answer"],
            "qtype": q.get("qtype", "lookup")}


def regeneration_plan(results, remaining):
    """Correction v2 C-7: regeneration proceeds in ASCENDING QUESTION ID
    until the 45-call sub-ceiling binds; files still unregenerated when it
    binds are recorded as dropped, and the shortfall rule applies to the
    validated count. Returns (to_regenerate, unregenerated)."""
    failed = sorted(r["id"] for r in results if r.get("fail"))
    cap = max(0, remaining)
    return failed[:cap], failed[cap:]


def salted_order(ids, salt):
    """sha256(salt + question id), ascending — the frozen selection rule."""
    return sorted(ids, key=lambda i: hashlib.sha256(
        (salt + i).encode()).hexdigest())


def select(validated_ids):
    """The frozen shortfall rule (registration §2). Returns
    (confirmatory, smoke, branch) or raises on the stop branch."""
    n = len(validated_ids)
    if n >= 130:
        n_conf, branch = N_CONFIRMATORY, "full"
    elif n >= 115:
        n_conf, branch = n - N_SMOKE, "shortfall"
    else:
        raise SystemExit(
            f"question_yield_shortfall: {n} validated < 115. Sealing "
            "instrument-insufficient before any policy run (registration §2).")
    conf = salted_order(validated_ids, CONFIRMATORY_SALT)[:n_conf]
    rest = [i for i in validated_ids if i not in set(conf)]
    smoke = salted_order(rest, SMOKE_SALT)[:N_SMOKE]
    return sorted(conf), sorted(smoke), branch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--select-only", action="store_true")
    args = ap.parse_args()

    man = H.load_manifest()
    paths = sorted(e["path"] for e in man["entries"])
    if len(paths) != H.EXPECTED_CORPUS_FILES:
        raise SystemExit(
            f"CORPUS PRECONDITION FAILED: {len(paths)} snapshot files, "
            f"expected {H.EXPECTED_CORPUS_FILES} (correction v3 G5).")
    ids = {rp: f"q{i:03d}" for i, rp in enumerate(paths, 1)}

    ledger = H.CallLedger()
    ledger.discover(cached_keys())        # cross-run discovery before spending

    if not args.select_only:
        with ThreadPoolExecutor(8) as ex:
            results = list(ex.map(
                lambda rp: cached("generation", f"generation:{rp}",
                                  lambda rp=rp: gen_one(ids[rp], rp, ledger,
                                                        "generation")),
                paths))
        # --- one regeneration pass, ascending question id (C-7) -----------
        by_id = {r["id"]: r for r in results}
        to_regen, unregenerated = regeneration_plan(
            results, ledger.remaining("regeneration"))
        regenerated = {}
        for qid in to_regen:                     # ascending question id
            rp = by_id[qid]["rp"]
            regenerated[qid] = cached(
                "regeneration", f"regeneration:{rp}",
                lambda rp=rp, qid=qid: gen_one(qid, rp, ledger,
                                               "regeneration",
                                               retry_note=RETRY_NOTE))
        results = [regenerated.get(r["id"], r)
                   if r.get("fail") and r["id"] in regenerated else r
                   for r in results]
    else:
        results = []
        for rp in paths:
            for bucket in ("regeneration", "generation"):
                p = cache_path(f"{bucket}:{rp}")
                if os.path.exists(p):
                    with open(p) as fh:
                        v = json.load(fh)["value"]
                    if v.get("question") or bucket == "generation":
                        results.append(v)
                        break
        unregenerated = []

    validated = [r for r in results if r.get("question")]
    dropped = sorted(r["id"] for r in results if r.get("fail"))
    skipped = sorted(r["id"] for r in results if r.get("skip"))
    conf, smoke, branch = select(sorted(r["id"] for r in validated))

    by_id = {r["id"]: r for r in validated}
    questions = [{"id": qid, "rp": by_id[qid]["rp"],
                  "question": by_id[qid]["question"],
                  "answer": by_id[qid]["answer"],
                  "qtype": by_id[qid]["qtype"],
                  "set": ("confirmatory" if qid in set(conf)
                          else "smoke" if qid in set(smoke) else "unused"),
                  "generation_input_sha256":
                      by_id[qid]["generation_input_sha256"]}
                 for qid in sorted(by_id)]

    with open(Q_OUT, "w") as fh:
        json.dump({"generator": H.GENERATOR, "answerer": H.ANSWERER,
                   "snapshot_commit": man["snapshot_commit"],
                   "corpus_files": len(paths),
                   "validated": len(validated), "n_confirmatory": len(conf),
                   "n_smoke": len(smoke), "shortfall_branch": branch,
                   "dropped_after_regeneration": dropped,
                   "unregenerated_at_subceiling": sorted(unregenerated),
                   "skipped_short": skipped,
                   "generation_input_chars": GEN_INPUT_CHARS,
                   "questions": questions}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(SELECT_OUT, "w") as fh:
        json.dump({"confirmatory_salt": CONFIRMATORY_SALT,
                   "smoke_salt": SMOKE_SALT, "branch": branch,
                   "confirmatory": conf, "smoke": smoke}, fh, indent=1,
                  sort_keys=True)
        fh.write("\n")
    for p in (Q_OUT, SELECT_OUT):
        with open(p, "rb") as fh:
            print(os.path.basename(p),
                  hashlib.sha256(fh.read()).hexdigest()[:16], flush=True)
    print(f"validated={len(validated)} confirmatory={len(conf)} "
          f"smoke={len(smoke)} dropped={len(dropped)} branch={branch}")


if __name__ == "__main__":
    sys.exit(main())
