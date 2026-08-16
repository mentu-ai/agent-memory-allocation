"""c36 question generation — the regeneration protocol, gates enforced.

Binds instruments/2026-08-16-locator-bakeoff-question-regeneration-intent.md
(G1-G6) under the c36 registration. The generator MODEL and PROMPT are the
byte-verified C34 ones (Q_PROMPT, GEN_INPUT_CHARS, RETRY_NOTE imported from
the pinned module); what is NEW is that every constraint is now a mechanical
acceptance gate with reject-and-regenerate (max 3 attempts/document) and a
per-gate rejection log — the C34 defect was constraints that existed only as
instructions (30.0% violation measured).

Salts (frozen here, before any question exists):
  confirmatory: "c36-confirmatory-v1:"   smoke: "c36-smoke-v1:"
Split: sha256(salt + qid) ascending, first 120 confirmatory / 10 smoke —
the C34 mechanism with new salts.

Usage:  python3 generate_questions_c36.py            # generate + validate + freeze
        python3 generate_questions_c36.py --dry-run  # gates over cached candidates only
"""
import hashlib
import json
import os
import re
import sys

import c36lib
from scoring import contains_boundary, normalize

CONFIRMATORY_SALT = "c36-confirmatory-v1:"
SMOKE_SALT = "c36-smoke-v1:"
N_CONFIRMATORY = 120
N_SMOKE = 10
MAX_ATTEMPTS = 3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_QUESTIONS = os.path.join(HERE, "questions-c36.json")
OUT_LOG = os.path.join(HERE, "generation-log-c36.json")
GEN_CACHE = os.path.join(HERE, "gen-cache")

_ALPHA = re.compile(r"[^\W\d_]{3,}", re.UNICODE)
_FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


def word_count(gold):
    """G3 `length`: whitespace token count of the raw gold — counted, not instructed."""
    return len(gold.split())


def gate_check(candidate, body, corpus_bodies):
    """All G3 gates for one candidate. Returns (ok, [failed gate names])."""
    q, gold = candidate.get("question", ""), candidate.get("answer", "")
    failed = []
    if not gold or gold not in body:
        failed.append("verbatim")
    if not (3 <= word_count(gold) <= 15):
        failed.append("length")
    # failable: locating wrongly must be able to fail —
    #   (a) the gold may not be recoverable from the question itself,
    #   (b) the gold may occur in at most 2 corpus documents.
    if gold and contains_boundary(q, gold):
        failed.append("failable-in-question")
    if gold and sum(1 for b in corpus_bodies.values() if normalize(gold) in b) > 2:
        failed.append("failable-multidoc")
    if not _ALPHA.search(gold or ""):
        failed.append("non-degenerate")
    # leak gate: no arm in this study uses digests; recorded not-applicable
    # in the log rather than silently skipped (G3 table, `leak`).
    return (len(failed) == 0, failed)


def salted_order(ids, salt):
    return sorted(ids, key=lambda i: hashlib.sha256((salt + i).encode()).hexdigest())


def generate():
    H, G = c36lib.load_c34()
    corpus_dir = c36lib.setup_sandbox(fresh=False)
    manifest = c36lib.load_manifest()
    os.makedirs(GEN_CACHE, exist_ok=True)

    bodies, normalized_bodies = {}, {}
    for entry in manifest["entries"]:
        with open(os.path.join(corpus_dir, entry["path"]), encoding="utf-8", errors="replace") as f:
            raw = f.read()
        bodies[entry["path"]] = _FRONTMATTER.sub("", raw)
        normalized_bodies[entry["path"]] = normalize(bodies[entry["path"]])

    questions, log = [], {"gates": {}, "excluded": [], "attempts": {}, "leak_gate": "not-applicable (no digest arm)"}
    for index, entry in enumerate(sorted(bodies), 1):
        body = bodies[entry][:G.GEN_INPUT_CHARS]
        accepted = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            cache_key = hashlib.sha256(f"{entry}:{attempt}:{body}".encode()).hexdigest()
            cache_path = os.path.join(GEN_CACHE, cache_key + ".json")
            if os.path.exists(cache_path):
                with open(cache_path) as f:
                    candidate = json.load(f)
            else:
                prompt = G.Q_PROMPT.format(rp=entry, body=body)
                if attempt > 1:
                    prompt += G.RETRY_NOTE
                rec = H.run_claude(prompt, H.GENERATOR)
                if rec.get("error"):
                    # Provider failure is NOT a gate rejection and is never
                    # cached: the attempt slot stays retryable on rerun.
                    log["provider_errors"] = log.get("provider_errors", 0) + 1
                    print(f"  provider error on {entry} attempt {attempt}: {rec['error']} — retryable")
                    continue
                text = rec.get("result_text", "")
                match = re.search(r"\{.*\}", text, re.DOTALL)
                try:
                    candidate = json.loads(match.group(0)) if match else {}
                except ValueError:
                    candidate = {}
                with open(cache_path, "w") as f:
                    json.dump(candidate, f)
            ok, failed = gate_check(candidate, body, normalized_bodies)
            for gate in failed:
                log["gates"][gate] = log["gates"].get(gate, 0) + 1
            log["attempts"][entry] = attempt
            if ok:
                accepted = candidate
                break
        if accepted is None:
            log["excluded"].append(entry)   # counted, never silently skipped
            continue
        questions.append({
            "id": f"q{index:03d}",
            "rp": entry,
            "question": accepted["question"],
            "answer": accepted["answer"],
            "qtype": accepted.get("qtype", "lookup"),
            "generation_input_sha256": hashlib.sha256(body.encode()).hexdigest(),
        })

    ordered = salted_order([q["id"] for q in questions], CONFIRMATORY_SALT)
    confirmatory = set(ordered[:N_CONFIRMATORY])
    remaining = [i for i in ordered[N_CONFIRMATORY:]]
    smoke = set(salted_order(remaining, SMOKE_SALT)[:N_SMOKE])
    for q in questions:
        q["set"] = "confirmatory" if q["id"] in confirmatory else "smoke" if q["id"] in smoke else "reserve"

    with open(OUT_QUESTIONS, "w") as f:
        json.dump(questions, f, indent=1, sort_keys=True)
    # P3 subset, fixed at generation time: gold documents whose frontmatter
    # carries `lang: es`. Tag-only (no detector), so membership is mechanical.
    spanish = sorted({
        e["path"] for e in manifest["entries"]
        if re.search(r"^lang:\s*[\"']?es[\"']?\s*$",
                     open(os.path.join(corpus_dir, e["path"]), encoding="utf-8",
                          errors="replace").read(2048), re.MULTILINE)
    })
    with open(os.path.join(HERE, "spanish-gold-c36.json"), "w") as f:
        json.dump(spanish, f, indent=1)
    log["accepted"] = len(questions)
    log["confirmatory"] = len(confirmatory)
    log["smoke"] = len(smoke)
    with open(OUT_LOG, "w") as f:
        json.dump(log, f, indent=1, sort_keys=True)
    print(f"accepted {len(questions)} / {len(bodies)} documents; "
          f"gate rejections: {log['gates']}; excluded: {len(log['excluded'])}")
    print(f"frozen at: {OUT_QUESTIONS} sha256 {c36lib.sha256_file(OUT_QUESTIONS)}")


if __name__ == "__main__":
    generate()
