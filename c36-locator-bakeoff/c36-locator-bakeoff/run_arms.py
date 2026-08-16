"""c36 arm runner — Phase A (localization, no model) + Phase B (P5, answerer).

Phase A: every question x arms L0/L1/L2/L4 -> one locate call each, recorded
with hits, the adjudicating located@8 measure, and wall time. No model call.

Phase B: arms L0 and L2 only (P5 stakes exactly that pair). The policy is
pinned in FREEZE.md §4 (hydrate-all): the answerer receives the question and
the FULL BODIES of the arm's top-8 documents in rank order (each truncated
at HYDRATE_CHARS with a truncation marker), then answers in the C34
"ANSWER:" convention. One model call per question per arm; the locator is
the only input that differs between arms — pure attribution, no agentic
read-choice variance. Both scoring rules recorded; the boundary rule
adjudicates.

Usage:  python3 run_arms.py a            # Phase A (also writes metrics-c36.json)
        python3 run_arms.py b            # Phase B (provider calls; answerer pinned)
"""
import json
import os
import subprocess
import sys
import time

import c36lib
from scoring import score

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs-c36")
QUESTIONS = os.path.join(HERE, "questions-c36.json")
HYDRATE_CHARS = 6000
P5_ARMS = ("L0", "L2")

ANSWER_PROMPT = """Answer the question using ONLY the documents below.
End with one line: ANSWER: <exact answer copied from a document>

QUESTION: {question}

{documents}"""


def load_questions(subset=None):
    with open(QUESTIONS) as f:
        questions = json.load(f)
    if subset:
        questions = [q for q in questions if q["set"] == subset]
    return questions


def append(path, record):
    os.makedirs(RUNS, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def phase_a():
    c36lib.assert_navigator_commit()
    corpus_dir = c36lib.setup_sandbox(fresh=True)
    out = os.path.join(RUNS, "localization.jsonl")
    if os.path.exists(out):
        raise SystemExit(f"{out} exists; Phase A is one-shot. Move it aside deliberately.")
    per_query = {arm: [] for arm in c36lib.ARMS}
    for q in load_questions():
        for arm in c36lib.ARMS:
            t0 = time.perf_counter()
            envelope = c36lib.locate(corpus_dir, q["question"], arm)
            wall_ms = (time.perf_counter() - t0) * 1000
            per_query[arm].append(wall_ms)
            hits = c36lib.hit_paths(envelope)
            append(out, {
                "id": q["id"], "set": q["set"], "arm": arm, "rp": q["rp"],
                "hits": hits[:c36lib.K],
                "located": c36lib.located(envelope, q["rp"]),
                "located_top1": hits[:1] == [q["rp"]],
                "located_top3": q["rp"] in hits[:3],
                "wall_ms": round(wall_ms, 1),
            })
    # P4 inputs: 5 cold index builds (fresh node process each) + per-query medians.
    builds = []
    for _ in range(5):
        t0 = time.perf_counter()
        subprocess.run(
            ["node", "-e",
             "import(process.argv[1]).then(async m => { await m.getIndex(process.argv[2], "
             "(await import(process.argv[3])).walkRepository); })",
             os.path.join(c36lib.NAVIGATOR, "src", "core", "lexical", "index-cache.js"),
             corpus_dir,
             os.path.join(c36lib.NAVIGATOR, "src", "core", "files.js")],
            check=True, capture_output=True, env=c36lib.nav_env())
        builds.append((time.perf_counter() - t0) * 1000)
    import platform
    node = subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip()
    median = lambda xs: sorted(xs)[len(xs) // 2]
    metrics = {
        "machine": {"platform": platform.platform(), "machine": platform.machine(),
                    "python": platform.python_version(), "node": node},
        "cold_build_ms": sorted(round(b, 1) for b in builds),
        "cold_build_ms_median": round(median(builds), 1),
        "per_query_ms_median": {arm: round(median(v), 1) for arm, v in per_query.items()},
        "added_ms_L2_vs_L0_median": round(median(per_query["L2"]) - median(per_query["L0"]), 1),
    }
    with open(os.path.join(HERE, "metrics-c36.json"), "w") as f:
        json.dump(metrics, f, indent=1, sort_keys=True)
    print(json.dumps(metrics, indent=1))


def phase_b():
    H, _ = c36lib.load_c34()
    corpus_dir = c36lib.setup_sandbox(fresh=False)
    for arm in P5_ARMS:
        out = os.path.join(RUNS, f"p5-{arm}.jsonl")
        done = set()
        if os.path.exists(out):
            with open(out) as f:
                done = {json.loads(line)["id"] for line in f if line.strip()}
        for q in load_questions("confirmatory"):
            if q["id"] in done:
                continue
            envelope = c36lib.locate(corpus_dir, q["question"], arm)
            documents = []
            for rank, rp in enumerate(c36lib.hit_paths(envelope)[:c36lib.K], 1):
                with open(os.path.join(corpus_dir, rp), encoding="utf-8", errors="replace") as f:
                    body = f.read()
                marker = "\n[TRUNCATED]" if len(body) > HYDRATE_CHARS else ""
                documents.append(f"--- DOCUMENT {rank}: {rp} ---\n{body[:HYDRATE_CHARS]}{marker}")
            prompt = ANSWER_PROMPT.format(question=q["question"], documents="\n\n".join(documents))
            rec = H.run_claude(prompt, H.ANSWERER)
            if rec.get("error"):
                # Provider failure: not recorded, resumable on rerun (record
                # ids gate re-dispatch), counted on stderr for the operator.
                print(f"  provider error on {q['id']} {arm}: {rec['error']} — retryable")
                continue
            answer = H.answer_line(rec.get("result_text", ""))
            append(out, {
                "id": q["id"], "arm": arm, "rp": q["rp"],
                "hits": c36lib.hit_paths(envelope)[:c36lib.K],
                "located": c36lib.located(envelope, q["rp"]),
                "answer": answer,
                "score": score(answer, q["answer"]),
                "prompt_chars": len(prompt),
                "read_events": len(documents),
            })
            print(q["id"], arm, "located" if c36lib.located(envelope, q["rp"]) else "miss")


if __name__ == "__main__":
    {"a": phase_a, "b": phase_b}[sys.argv[1]]()
