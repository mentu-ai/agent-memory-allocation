#!/usr/bin/env python3
"""C34 — offline fixture factory for the M2 test suite.

Builds a complete synthetic study directory (corpus snapshot, manifest,
frozen question set, index, run records) so every gate and every verdict
branch is reachable without a provider, a network call, or any Mentu path.

Nothing here ever calls `claude`, opens a socket, or reads a Mentu substrate.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import harness_lib as H          # noqa: E402

BODY_LINES = 12


def doc_text(i):
    lines = [f"# Synthetic document {i:03d}", "",
             f"The registered marker for document {i:03d} is "
             f"alpha-{i:03d}-omega.", ""]
    lines += [f"Filler line {j} for document {i:03d}." for j in range(BODY_LINES)]
    return ("---\n"
            f"summary: synthetic corpus document {i:03d}\n"
            "---\n\n" + "\n".join(lines) + "\n")


def gold_answer(i):
    return f"alpha-{i:03d}-omega"


def make_corpus(root, n_files, mutate=None, extra_files=()):
    """Write the snapshot + manifest. `mutate` renames a file's bytes AFTER
    hashing, producing the snapshot-mismatch dead run. `extra_files` is
    [(relpath, text)] for smuggling audit-flagged content in."""
    snap = os.path.join(root, "corpus-snapshot")
    entries = []
    for i in range(1, n_files + 1):
        rp = f"docs/doc{i:03d}.md"
        raw = doc_text(i).encode()
        dest = os.path.join(snap, rp)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(raw)
        entries.append({"path": rp, "size": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()})
    for rp, text in extra_files:
        raw = text.encode()
        dest = os.path.join(snap, rp)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(raw)
        entries.append({"path": rp, "size": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()})
    man = os.path.join(root, "corpus-manifest.json")
    with open(man, "w") as fh:
        json.dump({"snapshot_commit": "0" * 40, "files": len(entries),
                   "bytes": sum(e["size"] for e in entries),
                   "entries": entries}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    if mutate:
        with open(os.path.join(snap, mutate), "ab") as fh:
            fh.write(b"\nmutated after snapshot\n")
    return man, snap, entries


def make_questions(root, n_conf, n_smoke, snapshot_dir, validated=None,
                   break_provenance=(), date="2026-08-13"):
    """Frozen question set with real generation-input provenance hashes."""
    from generate_questions import gen_input
    questions = []
    for i in range(1, n_conf + n_smoke + 1):
        rp = f"docs/doc{i:03d}.md"
        _body, _sent, sha = gen_input(rp, snapshot_dir)
        if f"q{i:03d}" in set(break_provenance):
            sha = "0" * 64
        questions.append({
            "id": f"q{i:03d}", "rp": rp,
            "question": f"What is the registered marker for document {i:03d}?",
            "answer": gold_answer(i),
            "qtype": "lookup" if i % 4 else "synthesis",
            "set": "confirmatory" if i <= n_conf else "smoke",
            "generation_input_sha256": sha})
    path = os.path.join(root, f"questions-{date}.json")
    with open(path, "w") as fh:
        json.dump({"generator": H.GENERATOR, "answerer": H.ANSWERER,
                   "snapshot_commit": "0" * 40,
                   "validated": (len(questions) if validated is None
                                 else validated),
                   "n_confirmatory": n_conf, "n_smoke": n_smoke,
                   "shortfall_branch": "full",
                   "questions": questions}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return path, questions


def make_index(root, questions, authoring_tokens=50_000, date="2026-08-13"):
    index = {q["rp"]: {"digest": f"digest for {q['rp']}",
                       "source": "frontmatter"} for q in questions}
    path = os.path.join(root, f"index-{date}.json")
    with open(path, "w") as fh:
        json.dump({"generator": H.GENERATOR, "files": len(index),
                   "authoring_tokens_total": authoring_tokens,
                   "index": index}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return path


def run_record(q, policy, correct, reads=(), searches=(), tot=0, marg=0,
               which_set="confirmatory", error=None,
               identities=None, hydration=True, input_tokens=None,
               answer=None):
    if answer is None:
        answer = q["answer"] if correct else "something else entirely"
    rec = {
        "qid": q["id"], "policy": policy, "gold_rp": q["rp"],
        "qtype": q["qtype"], "set": which_set,
        "barred_from_adjudication": which_set == "smoke",
        "answer": answer,
        "input_uncached": 0, "cache_creation_tokens": 0,
        "cache_read_tokens": 0,
        "input_tokens": tot if input_tokens is None else input_tokens,
        "output_tokens": 0,
        "tokens_total": tot, "tokens_marginal": marg,
        "model_identities": ([H.ANSWERER] if identities is None
                             else identities),
        "model_requested": H.ANSWERER,
        "is_error": bool(error), "error_class": error,
        "started_at": 1_800_000_000.0,
        "reads": list(reads), "searches": list(searches),
        "budget_bucket": "confirmatory", "call_key": f"x:{q['id']}:{policy}",
    }
    if error:
        rec["error"] = error
    if policy in ("B", "C") and hydration:
        rec["hydration"] = H.hydration_record(reads, searches, q["rp"])
    return rec


def make_runs(root, questions, plan, which_set="confirmatory"):
    """plan: {policy: dict(n_correct, n_located, n_correct_among_nonlocated,
    tot, marg, errors, zero_read_share, **record kwargs)}.

    Located questions come first in ascending qid, so every scenario is a
    deterministic function of the counts.
    """
    runs = os.path.join(root, "runs")
    os.makedirs(runs, exist_ok=True)
    qs = [q for q in questions if q["set"] == which_set]
    for policy, spec in sorted(plan.items()):
        n = len(qs)
        n_loc = spec.get("n_located", n if policy in ("B", "C") else 0)
        n_err = spec.get("errors", 0)
        c_nl = spec.get("n_correct_among_nonlocated", 0)
        n_correct = spec.get("n_correct", n)
        zero_share = spec.get("zero_read_share", 0.5)
        kwargs = {k: v for k, v in spec.items()
                  if k not in ("n_correct", "n_located", "errors",
                               "n_correct_among_nonlocated", "tot", "marg",
                               "zero_read_share")}
        located_correct = n_correct - c_nl
        nl_seen = 0
        for idx, q in enumerate(qs):
            err = spec.get("error_class", "subprocess_timeout") \
                if idx < n_err else None
            located = policy in ("B", "C") and idx < n_loc
            if policy == "D":
                correct = idx < n_correct
                reads, searches = [], []
            elif located:
                correct = idx < located_correct
                reads = [f"/sandbox/{q['rp']}"]
                searches = [{"tool": "Grep", "pattern": "marker", "path": ""}]
            else:
                correct = nl_seen < c_nl
                nl_seen += 1
                zero = (nl_seen % 2 == 0) if zero_share else False
                reads = [] if zero else ["/sandbox/docs/doc999.md"]
                searches = [] if zero else [
                    {"tool": "Glob", "pattern": "**/*.md", "path": ""}]
            rec = run_record(q, policy, correct, reads, searches,
                             tot=spec.get("tot", 0), marg=spec.get("marg", 0),
                             which_set=which_set, error=err, **kwargs)
            with open(os.path.join(runs, f"{q['id']}_{policy}.json"),
                      "w") as fh:
                json.dump(rec, fh, indent=1, sort_keys=True)
    return runs


# --- the reference plans ---------------------------------------------------
def plan_supported(n=110):
    """B beats C on accuracy and localization, C carries the wrong-stop tax,
    both clear 3x oracle on marginal tokens, pooled non-hydrated is 88%
    incorrect over a denominator of 68."""
    return {
        "B": dict(n_located=94, n_correct=79, n_correct_among_nonlocated=2,
                  tot=130_000, marg=22_000),
        "C": dict(n_located=58, n_correct=52, n_correct_among_nonlocated=6,
                  tot=90_000, marg=15_000),
        "D": dict(n_correct=104, tot=25_000, marg=3_000),
    }
