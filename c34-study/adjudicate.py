#!/usr/bin/env python3
"""C34 — deterministic adjudicator over recorded runs (frozen criteria).

Runs are stochastic evidence; this computation is reproducible byte-for-byte
from runs/ + the frozen question set + the committed snapshot. Interpretation
never changes a verdict.

FROZEN PREDICTIONS (registration §Predictions):
  P1  acc(B) >= acc(C) - 3pp                        [verbatim from C29]
  P2  total tokens(B) <= 2x unamortized total(C)    [verbatim from C29]
  P3' wrong-stop rate(C) >= wrong-stop rate(B), both under the identical rule
      "incorrect AND the gold file was never read" (deviation D-2). The
      operator is `>=`: an exact tie PASSES (correction v2 C-8, v3 G2).
  P4  marginal(B) >= 3x marginal(D) AND marginal(C) >= 3x marginal(D)
      (deviation D-3: the measure is frozen WITH the threshold, and marginal
      is the harder reading — C29's own B would have failed it at 2.85x).
      Totals are reported alongside, non-adjudicating.
  P5  (a) localization rate(B) > localization rate(C), AND
      (b) among non-hydrated answers pooled across B and C, >=80% incorrect.
      (b) adjudicates only if the pooled non-hydrated denominator is >= 20;
      below that it is `not_exercised`, is reported with its denominator, and
      P5 adjudicates on (a) alone (deviation D-9 / correction v2 C-6).

VERDICT PRECEDENCE (deviation D-4 — total, first matching clause wins):
  1 void                    question-set contamination; no partial salvage
  2 instrument-insufficient floors, hashes, hydration, model identity, budget
  3 refuted                 acc(C)-acc(B) > 3pp AND amortized total(C)
                            <= 0.5x total(B)                [verbatim from C29]
  4 supported               P1 & P2 & P3' & P4 & P5, floors met
  5 revised                 everything else, machine reason enumerating each
                            failed prediction

The registered instrument-insufficient cause "rule R yields fewer than 135
files at S" is NOT implemented as a live branch: correction v3 G5 records it
as a dead branch and replaces it with the corpus precondition (exactly 141
accepted files), which this adjudicator checks and which fails closed under
the reason `corpus_precondition_failed`.

Verdict legibility (correction v2 C-12): the P1 / P3' / P5 outcomes are
emitted at TOP LEVEL beside the verdict word, so the curation-vs-search answer
stays readable next to a P4-marginal headroom verdict that is orthogonal to it.

Usage: python3 adjudicate.py [--runs DIR] [--out PATH]
"""
import argparse
import glob
import json
import math
import os
import sys

import harness_lib as H

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-08-13"
POLICIES = ("B", "C", "D")
AGENTIC = ("B", "C")

# frozen thresholds
P1_MARGIN = 0.03
P2_FACTOR = 2.0
P4_FACTOR = 3.0
P5B_MIN_INCORRECT = 0.80
P5B_MIN_DENOM = 20          # deviation D-9 (correction v2 C-6)
REFUTED_COST_FACTOR = 0.5
PROFLIGATE_FACTOR = 5.0
SCORED_FLOOR = 100

# order in which instrument-insufficient causes are named (frozen)
II_ORDER = ("question_yield_shortfall", "corpus_precondition_failed",
            "corpus_manifest_missing", "corpus_snapshot_hash_mismatch",
            "scored_question_floor", "missing_hydration_record",
            "model_identity_drift", "registered_budget_exhausted",
            "pinned_answerer_unavailable")


# ---------------------------------------------------------------------------
# denominator discipline (Phase-H rule 4): every zero carries its denominator
# and its exercised-status
# ---------------------------------------------------------------------------
def rate(num, den, nd=4):
    if den == 0:
        return {"value": None, "numerator": num, "denominator": den,
                "status": "not_exercised"}
    return {"value": round(num / den, nd), "numerator": num,
            "denominator": den,
            "status": "zero_events" if num == 0 else "observed"}


def val(r):
    return None if r is None else r["value"]


def fisher_exact_two_sided(a, b, c, d):
    """2x2 [[a,b],[c,d]]; two-sided p by summing every table whose
    probability does not exceed the observed one. Stdlib only."""
    n = a + b + c + d
    if n == 0:
        return None
    r1, r2, c1 = a + b, c + d, a + c

    def prob(x):
        return (math.comb(r1, x) * math.comb(r2, c1 - x)) / math.comb(n, c1)

    p0 = prob(a)
    lo, hi = max(0, c1 - r2), min(r1, c1)
    tot = sum(prob(x) for x in range(lo, hi + 1)
              if prob(x) <= p0 * (1 + 1e-9))
    return round(min(1.0, tot), 6)


# ---------------------------------------------------------------------------
# gates
# ---------------------------------------------------------------------------
def verify_snapshot(manifest_path, snapshot_dir, expect_files):
    """Returns (causes, detail). Fails closed."""
    causes, detail = [], {}
    if not os.path.exists(manifest_path):
        return ["corpus_manifest_missing"], {"manifest": manifest_path}
    with open(manifest_path) as fh:
        man = json.load(fh)
    entries = man.get("entries", [])
    detail["manifest_files"] = len(entries)
    if expect_files is not None and len(entries) != expect_files:
        causes.append("corpus_precondition_failed")
        detail["expected_files"] = expect_files
    bad = []
    for e in sorted(entries, key=lambda x: x["path"]):
        p = os.path.join(snapshot_dir, e["path"])
        try:
            with open(p, "rb") as fh:
                raw = fh.read()
        except OSError:
            bad.append(e["path"])
            continue
        if H.sha256_bytes(raw) != e["sha256"] or len(raw) != e["size"]:
            bad.append(e["path"])
    if bad:
        causes.append("corpus_snapshot_hash_mismatch")
        detail["mismatched"] = sorted(bad)[:20]
        detail["mismatched_n"] = len(bad)
    return causes, detail


def contamination_findings(questions, snapshot_dir, freeze_ts, records):
    """Clause 1. Two mechanical checks:
    (a) every question's recorded generation-input sha256 must reproduce from
        an independently stripped body slice of the snapshot — if it does not,
        the generator did not see what the freeze claims it saw;
    (b) no policy-run record may predate the question-freeze commit."""
    out = []
    try:
        from generate_questions import gen_input
    except Exception:                                  # pragma: no cover
        gen_input = None
    if gen_input is not None:
        for q in questions:
            want = q.get("generation_input_sha256")
            if not want:
                out.append({"check": "generation_provenance_missing",
                            "qid": q["id"]})
                continue
            try:
                _body, _sent, got = gen_input(q["rp"], snapshot_dir)
            except OSError:
                out.append({"check": "generation_source_missing",
                            "qid": q["id"]})
                continue
            if got != want:
                out.append({"check": "generation_input_hash_mismatch",
                            "qid": q["id"]})
    if freeze_ts is not None:
        for r in records:
            started = r.get("started_at")
            if started is not None and started < freeze_ts:
                out.append({"check": "run_predates_question_freeze",
                            "qid": r.get("qid"), "policy": r.get("policy")})
    return out


def freeze_commit_ts(path, repo=None):
    """Author timestamp of the commit that froze the question set. Returns
    None when the file is not committed (pre-M4, and in offline fixtures)."""
    import subprocess
    repo = repo or os.path.dirname(os.path.abspath(path))
    try:
        out = subprocess.run(
            ["git", "-C", repo, "log", "--diff-filter=A", "--format=%at",
             "--", os.path.basename(path)],
            capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        return None
    return int(out[-1]) if out else None


# ---------------------------------------------------------------------------
# per-policy statistics — ONE code path for B and C (deviation D-6)
# ---------------------------------------------------------------------------
def policy_stats(records, gold, authoring_tokens):
    per = {}
    for p in POLICIES:
        rs = sorted((r for r in records if r.get("policy") == p),
                    key=lambda r: r["qid"])
        scored, errors = [], []
        for r in rs:
            (errors if (r.get("error") or r.get("is_error")) else
             scored).append(r)
        n = len(scored)
        correct = tok = marg = 0
        located = first_gold = non_hydrated = 0
        wrong_stop = mis_routed = true_stop = 0
        missing_hydration, identity_drift = [], []
        non_hydrated_records = []
        for r in scored:
            g = gold[r["qid"]]
            ok = H.normalize(g["answer"]) in H.normalize(r.get("answer", ""))
            correct += ok
            tok += r.get("tokens_total", 0)
            marg += r.get("tokens_marginal", 0)
            if r.get("model_identities") != [H.ANSWERER]:
                identity_drift.append(r["qid"])
            if p in AGENTIC:
                if not H.hydration_complete(r):
                    missing_hydration.append(r["qid"])
                    continue
                h = r["hydration"]
                located += h["located"]
                first_gold += h["first_read_is_gold"]
                if not h["located"]:
                    non_hydrated += 1
                    non_hydrated_records.append((p, r["qid"], ok))
                    if not ok:
                        wrong_stop += 1
                        if h["read_count"] >= 1:
                            mis_routed += 1
                        if h["zero_read"]:
                            true_stop += 1
        st = {
            "scored": n, "errors": len(errors),
            "error_qids": sorted(r["qid"] for r in errors),
            "error_classes": sorted({r.get("error_class") or "unclassified"
                                     for r in errors}),
            "accuracy": rate(correct, n),
            "error_rate": rate(n - correct, n),
            "tokens_total": tok, "tokens_marginal": marg,
            "tokens_total_per_q": round(tok / n, 1) if n else None,
            "tokens_marginal_per_q": round(marg / n, 1) if n else None,
            "model_identity_drift_qids": sorted(identity_drift),
        }
        if p in AGENTIC:
            st.update({
                "localization_rate": rate(located, n),
                "first_read_precision": rate(first_gold, n),
                "non_hydrated_rate": rate(non_hydrated, n),
                "wrong_stop_rate": rate(wrong_stop, n),
                "mis_routed_rate": rate(mis_routed, n),
                "true_stop_rate": rate(true_stop, n),
                "missing_hydration_qids": sorted(missing_hydration),
                "non_hydrated_pool": non_hydrated_records,
            })
        if p == "C":
            st["authoring_tokens"] = authoring_tokens
            st["tokens_total_amortized"] = tok + authoring_tokens
            st["tokens_total_unamortized"] = tok
            st["authoring_tokens_per_q"] = (round(authoring_tokens / n, 1)
                                            if n else None)
        per[p] = st
    return per


def predictions_from(per):
    """The frozen predictions over one per-policy table. Extracted so the
    primary computation and each non-adjudicating sensitivity row run through
    IDENTICAL code (correction v4 H4) — a sensitivity row that differed by so
    much as a rounding path would not be evidence about the primary result."""
    accB, accC = val(per["B"]["accuracy"]), val(per["C"]["accuracy"])
    totB, totC, totD = (per[p]["tokens_total"] for p in POLICIES)
    marB, marC, marD = (per[p]["tokens_marginal"] for p in POLICIES)
    totCam = per["C"].get("tokens_total_amortized", totC)
    wsB, wsC = (val(per[p]["wrong_stop_rate"]) for p in AGENTIC)
    locB, locC = (val(per[p]["localization_rate"]) for p in AGENTIC)

    pool = per["B"].get("non_hydrated_pool", []) + \
        per["C"].get("non_hydrated_pool", [])
    pool_den = len(pool)
    pool_incorrect = sum(1 for (_p, _q, ok) in pool if not ok)
    p5b_rate = rate(pool_incorrect, pool_den)
    p5b_exercised = pool_den >= P5B_MIN_DENOM
    p5b = (pool_incorrect / pool_den >= P5B_MIN_INCORRECT) \
        if p5b_exercised else None

    p1 = accB is not None and accC is not None and accB >= accC - P1_MARGIN
    p2 = bool(totC) and totB <= P2_FACTOR * totC
    p3p = wsB is not None and wsC is not None and wsC >= wsB   # ties PASS
    p4 = bool(marD) and marB >= P4_FACTOR * marD and marC >= P4_FACTOR * marD
    p5a = locB is not None and locC is not None and locB > locC
    p5 = bool(p5a) and (p5b is not False)
    out = {"accB": accB, "accC": accC, "totB": totB, "totC": totC,
           "totD": totD, "marB": marB, "marC": marC, "marD": marD,
           "totCam": totCam, "wsB": wsB, "wsC": wsC, "locB": locB,
           "locC": locC, "p5b_rate": p5b_rate,
           "p5b_exercised": p5b_exercised, "p5b": p5b,
           "P1": p1, "P2": p2, "P3prime": p3p, "P4": p4, "P5a": p5a, "P5": p5,
           "refuted": (accB is not None and accC is not None
                       and (accC - accB) > P1_MARGIN
                       and totCam <= REFUTED_COST_FACTOR * totB),
           "profligate": bool(totC) and totB > PROFLIGATE_FACTOR * totC,
           "scored": {p: per[p]["scored"] for p in POLICIES}}
    out["failed"] = [k for k in ("P1", "P2", "P3prime", "P4", "P5")
                     if not out[k]]
    return out


# ---------------------------------------------------------------------------
# Question-set annotations (correction v4; non-adjudicating)
# ---------------------------------------------------------------------------
class FlagEnumerationMismatch(RuntimeError):
    """The annotation sets computed from the committed artifacts differ from
    the sets enumerated in correction v4. Raised, never reported: the
    enumeration is a commitment, and a commitment that can silently drift is a
    comment. Named so its dead run can assert the type rather than merely that
    something went wrong."""


# Frozen enumerations from correction v4 H1-H3, computed there from the
# committed question set and re-derived here at adjudication time.
FLAGS_SCORING_DEGENERATE = ("q014", "q023", "q037", "q058", "q076", "q077",
                            "q129", "q138")
FLAGS_INDEX_LEAK = ("q014", "q101", "q127")
FLAGS_OUTSIDE_GENERATION_SLICE = ("q131",)
F1_UBIQUITY_MIN = 71        # a majority of the 141 snapshot files
F3_MAX_NORMALIZED_LEN = 2
GEN_INPUT_CHARS = 8000      # correction v2 C-4


def compute_annotations(questions, snapshot_dir, index, corpus_paths):
    """Correction v4 H1-H3, mechanical over the committed artifacts. Returns
    {annotation: {qid: [conditions]}}. No judgment, no stored verdict.

    `corpus_paths` is the FULL corpus (all 141 snapshot files, from the
    manifest) and is REQUIRED. F1's denominator is the corpus, not the set of
    files the questions happen to reference: the confirmatory set covers 120
    of the 141 files, so deriving it from the questions measures ubiquity
    against the wrong population.

    It carries no default because it once did (finding S-1). The implicit
    fallback was the bug — it produced identical flag sets on this corpus, so
    every enumeration check passed while the denominator was wrong. A caller
    that cannot name its corpus must say so explicitly by passing the question
    paths, not inherit that choice silently.
    """
    bodies = {}
    for rp in set(corpus_paths) | {q["rp"] for q in questions}:
        try:
            raw = H.read_snapshot(rp, snapshot_dir)
        except OSError:
            raw = ""
        bodies[rp] = H.strip_frontmatter(raw)[1]
    norm_bodies = {rp: H.normalize(bodies[rp]) for rp in corpus_paths}

    degenerate, leak, outside = {}, {}, {}
    for q in questions:
        g = H.normalize(q["answer"])
        conds = []
        if sum(1 for b in norm_bodies.values() if g and g in b) >= \
                F1_UBIQUITY_MIN:
            conds.append("F1_corpus_ubiquity")
        if any(other["id"] != q["id"] and g in H.normalize(other["answer"])
               for other in questions):
            conds.append("F2_cross_answer_collision")
        if len(g) <= F3_MAX_NORMALIZED_LEN:
            conds.append("F3_length_floor")
        if conds:
            degenerate[q["id"]] = conds
        digest = (index.get(q["rp"]) or {}).get("digest", "")
        if g and g in H.normalize(digest):
            leak[q["id"]] = ["own_digest_contains_gold"]
        slice_ = H.normalize(bodies[q["rp"]].strip()[:GEN_INPUT_CHARS])
        if g and g not in slice_:
            outside[q["id"]] = ["gold_beyond_generation_slice"]
    return {"scoring_degenerate": degenerate, "index_leak": leak,
            "outside_generation_slice": outside}


def verify_flag_enumerations(annotations, expected=None):
    """Compare the computed sets against correction v4's enumerations. Raises
    FlagEnumerationMismatch on any difference, in either direction."""
    if expected is None:
        expected = {"scoring_degenerate": FLAGS_SCORING_DEGENERATE,
                    "index_leak": FLAGS_INDEX_LEAK,
                    "outside_generation_slice":
                        FLAGS_OUTSIDE_GENERATION_SLICE}
    for name, want in sorted(expected.items()):
        got = set(annotations.get(name, {}))
        if got != set(want):
            raise FlagEnumerationMismatch(
                f"{name}: computed {sorted(got)} but correction v4 enumerates "
                f"{sorted(want)} (computed-only {sorted(got - set(want))}, "
                f"enumerated-only {sorted(set(want) - got)})")


def qtype_block(records, gold):
    out = {"split": {t: sum(1 for q in gold.values() if q.get("qtype") == t)
                     for t in ("lookup", "synthesis")}, "accuracy": {}}
    for p in POLICIES:
        out["accuracy"][p] = {}
        for t in ("lookup", "synthesis"):
            rs = [r for r in records
                  if r.get("policy") == p
                  and not (r.get("error") or r.get("is_error"))
                  and gold[r["qid"]].get("qtype") == t]
            ok = sum(1 for r in rs
                     if H.normalize(gold[r["qid"]]["answer"])
                     in H.normalize(r.get("answer", "")))
            out["accuracy"][p][t] = rate(ok, len(rs), 3)
    return out


# ---------------------------------------------------------------------------
# the adjudication
# ---------------------------------------------------------------------------
def sensitivity_row(records, gold, authoring_tokens, excluded, primary,
                    label):
    """One non-adjudicating row: the IDENTICAL computation over the questions
    that carry no excluded annotation (correction v4 H4).

    It carries no verdict, moves no threshold, and is never a tiebreak. If it
    disagrees with the primary result, THAT DISAGREEMENT IS THE FINDING and is
    reported as such — the verdict remains the primary computation on all 120.
    """
    keep = {q: g for q, g in gold.items() if q not in excluded}
    subset = [r for r in records if r["qid"] in keep]
    per = policy_stats(subset, keep, authoring_tokens)
    got = predictions_from(per)
    keys = ("P1", "P2", "P3prime", "P4", "P5")
    flipped = [k for k in keys if got[k] != primary[k]]
    return {
        "label": label,
        "adjudicating": False,
        "excluded_qids": sorted(excluded),
        "excluded_n": len(excluded),
        "denominator": len(keep),
        "scored_per_policy": got["scored"],
        "predictions": {k: got[k] for k in keys},
        "predictions_primary": {k: primary[k] for k in keys},
        "predictions_flipped": flipped,
        "disagrees_with_primary": bool(flipped),
        "accuracy": {"B": got["accB"], "C": got["accC"]},
        "accuracy_delta_vs_primary": {
            arm: (None if (got[k] is None or primary[k] is None)
                  else round(got[k] - primary[k], 4))
            for arm, k in (("B", "accB"), ("C", "accC"))},
        "wrong_stop_rate": {"B": got["wsB"], "C": got["wsC"]},
        "localization_rate": {"B": got["locB"], "C": got["locC"]},
        "p5b_pooled_non_hydrated": got["p5b_rate"],
        "p5b_status": ("adjudicating_in_primary_only"
                       if got["p5b_exercised"] else "not_exercised"),
        "note": "non-adjudicating; the verdict is the primary computation on "
                "the full confirmatory set. A disagreement here is a reported "
                "finding, never a tiebreak and never a threshold change.",
    }


def adjudicate(runs_dir, questions_path, index_path, manifest_path,
               snapshot_dir, study_dir, expect_files=None,
               include_set="confirmatory", expected_flags=None,
               check_flags=True):
    """`include_set` is "confirmatory" for the verdict-bearing path. The smoke
    audit calls it with "smoke" purely to prove the adjudicator runs end to
    end on the smoke records (registration §4); that output is labeled
    non-verdict-bearing and the 10 smoke questions remain permanently barred
    from the confirmatory denominators, tables and verdict."""
    with open(questions_path) as fh:
        qdata = json.load(fh)
    confirmatory = [q for q in qdata["questions"]
                    if q.get("set") == include_set]
    gold = {q["id"]: q for q in confirmatory}
    with open(index_path) as fh:
        idata = json.load(fh)
    authoring_tokens = idata.get("authoring_tokens_total", 0)
    index = idata.get("index", {})

    records, barred = [], 0
    for path in sorted(glob.glob(os.path.join(runs_dir, "q*_*.json"))):
        with open(path) as fh:
            r = json.load(fh)
        if r["qid"] not in gold:
            barred += 1
            continue
        if include_set == "confirmatory" and (
                r.get("barred_from_adjudication") or r.get("set") == "smoke"):
            barred += 1
            continue
        records.append(r)

    per = policy_stats(records, gold, authoring_tokens)
    primary = predictions_from(per)

    # correction v4 H1-H3: annotations computed from the committed artifacts,
    # then checked against the frozen enumerations. The check raises.
    # S-1: the corpus is named explicitly at the call site. When the manifest
    # is absent (a dead-run fixture), the fallback is stated here rather than
    # hidden in the callee's default.
    if os.path.exists(manifest_path):
        with open(manifest_path) as fh:
            corpus_paths = sorted(e["path"] for e in
                                  json.load(fh).get("entries", []))
    else:
        corpus_paths = sorted({q["rp"] for q in confirmatory})
    annotations = compute_annotations(confirmatory, snapshot_dir, index,
                                      corpus_paths)
    if check_flags:
        verify_flag_enumerations(annotations, expected_flags)
    sensitivity = [
        sensitivity_row(records, gold, authoring_tokens,
                        set(annotations["scoring_degenerate"]), primary,
                        "excluding_scoring_degenerate"),
        sensitivity_row(records, gold, authoring_tokens,
                        set(annotations["index_leak"]), primary,
                        "excluding_index_leak"),
    ]

    # ---- clause 1: void -------------------------------------------------
    freeze_ts = freeze_commit_ts(questions_path)
    contam = contamination_findings(confirmatory, snapshot_dir, freeze_ts,
                                    records)

    # ---- clause 2: instrument-insufficient ------------------------------
    causes, detail = verify_snapshot(manifest_path, snapshot_dir,
                                     expect_files)
    if qdata.get("shortfall_branch") == "stop" or \
            qdata.get("validated", 10 ** 9) < 115:
        causes.append("question_yield_shortfall")
    if min(per[p]["scored"] for p in POLICIES) < SCORED_FLOOR:
        causes.append("scored_question_floor")
        detail["scored"] = {p: per[p]["scored"] for p in POLICIES}
    missing_h = sorted(q for p in AGENTIC
                       for q in per[p].get("missing_hydration_qids", []))
    if missing_h:
        causes.append("missing_hydration_record")
        detail["missing_hydration_qids"] = missing_h
    drift = sorted(q for p in POLICIES
                   for q in per[p]["model_identity_drift_qids"])
    if drift:
        causes.append("model_identity_drift")
        detail["model_identity_drift_qids"] = drift
    for m in H.stop_markers(study_dir):
        if m["reason"] in II_ORDER:
            causes.append(m["reason"])
    causes = [c for c in II_ORDER if c in set(causes)]

    # ---- the frozen predictions -----------------------------------------
    accB, accC = primary["accB"], primary["accC"]
    totB, totC, totD = primary["totB"], primary["totC"], primary["totD"]
    marB, marC, marD = primary["marB"], primary["marC"], primary["marD"]
    totCam = primary["totCam"]
    wsB, wsC = primary["wsB"], primary["wsC"]
    locB, locC = primary["locB"], primary["locC"]
    p5b_rate, p5b_exercised, p5b = (primary["p5b_rate"],
                                    primary["p5b_exercised"], primary["p5b"])
    p1, p2, p3p, p4 = (primary["P1"], primary["P2"], primary["P3prime"],
                       primary["P4"])
    p5a, p5 = primary["P5a"], primary["P5"]
    refuted, profligate = primary["refuted"], primary["profligate"]

    preds = {k: primary[k] for k in ("P1", "P2", "P3prime", "P4", "P5")}
    failed = list(primary["failed"])
    named = {"P1": "accuracy_reversal_without_cost_dominance",
             "P2": "search_accurate_but_token_profligate",
             "P3prime": "no_wrong_stop_tax_at_power",
             "P4": "headroom_not_established_on_marginal_tokens",
             "P5": "localization_advantage_not_reproduced"}

    # ---- verdict precedence (first matching clause wins) ----------------
    if contam:
        verdict, reason = "void", "question_set_contamination"
    elif causes:
        verdict, reason = "instrument-insufficient", causes[0]
    elif refuted:
        verdict, reason = "refuted", "curation_dominates"
    elif not failed:
        verdict, reason = "supported", "P1_P2_P3prime_P4_P5_all_pass"
    else:
        verdict = "revised"
        # `profligate` (total(B) > 5x total(C)) cannot occur while P2 passes,
        # since P2 bounds total(B) at 2x total(C). It is therefore always
        # inside the P2 failure and needs no branch of its own; it is
        # computed and reported below as a comparability statistic.
        reason = (named[failed[0]] if len(failed) == 1
                  else "multiple_predictions_failed:" + "+".join(failed))

    effect = {
        # --- verdict legibility (correction v2 C-12): the curation-vs-search
        # answer sits at top level beside the verdict word ------------------
        "verdict": verdict,
        "verdict_reason": reason,
        "headline": {
            "P1_accuracy_parity": {
                "pass": p1, "acc_B": accB, "acc_C": accC,
                "margin_pp": (round((accB - accC) * 100, 2)
                              if None not in (accB, accC) else None)},
            "P3prime_wrong_stop_tax": {
                "pass": p3p, "wrong_stop_rate_B": wsB,
                "wrong_stop_rate_C": wsC, "operator": ">= (ties pass)"},
            "P5_localization_advantage": {
                "pass": p5, "P5a_pass": p5a,
                "localization_rate_B": locB, "localization_rate_C": locC,
                "P5b_pass": p5b,
                "P5b_status": ("adjudicating" if p5b_exercised
                               else "not_exercised"),
                "P5b_pooled_non_hydrated": p5b_rate,
                "P5b_min_denominator": P5B_MIN_DENOM},
        },
        "conjecture": "c34-public-curation-vs-search-replication",
        "adjudicated_set": include_set,
        "verdict_bearing": include_set == "confirmatory",
        "answerer": H.ANSWERER, "generator": H.GENERATOR,
        "snapshot_commit": qdata.get("snapshot_commit"),
        "questions_confirmatory": len(confirmatory),
        "records_adjudicated": len(records),
        "records_barred": barred,
        "predictions": {
            "P1_accuracy_parity": p1,
            "P2_token_order_totals": p2,
            "P3prime_symmetric_wrong_stop": p3p,
            "P4_headroom_marginal_tokens": p4,
            "P5_localization_advantage": p5,
        },
        "failed_predictions": failed,
        "refutation_check": refuted,
        "instrument_insufficient_causes": causes,
        "instrument_insufficient_detail": detail,
        "contamination_findings": contam,
        "floors": {
            "scored_ge_100_each_BCD":
                min(per[p]["scored"] for p in POLICIES) >= SCORED_FLOOR,
            "scored_per_policy": {p: per[p]["scored"] for p in POLICIES},
            "hydration_records_complete": not missing_h,
            "one_resolved_identity_per_pinned_model": not drift,
        },
        "per_policy": {p: {k: v for k, v in per[p].items()
                           if k != "non_hydrated_pool"} for p in POLICIES},
        # --- non-adjudicating comparability block ------------------------
        "non_adjudicating": {
            "c29_asymmetric_P3": {
                "note": "C29's frozen P3 as originally written — C's "
                        "wrong-stop RATE against B's wrong-ANSWER rate, a "
                        "subset against a superset. Retained for "
                        "comparability; deviation D-2 adjudicates on the "
                        "symmetric form instead.",
                "c_wrong_stop_rate": wsC,
                "b_wrong_answer_rate": val(per["B"]["error_rate"]),
                "would_pass": (wsC is not None
                               and val(per["B"]["error_rate"]) is not None
                               and wsC >= val(per["B"]["error_rate"]))},
            "P2_on_marginal_not_adjudicated": {
                "marginal_B": marB, "marginal_C": marC,
                "ratio_B_over_C": (round(marB / marC, 3) if marC else None),
                "would_pass": bool(marC) and marB <= P2_FACTOR * marC},
            "P4_on_totals_not_adjudicated": {
                "total_B": totB, "total_C": totC, "total_D": totD,
                "ratio_B_over_D": (round(totB / totD, 3) if totD else None),
                "ratio_C_over_D": (round(totC / totD, 3) if totD else None),
                "would_pass": bool(totD) and totB >= P4_FACTOR * totD
                and totC >= P4_FACTOR * totD},
            "P4_adjudicated_ratios_marginal": {
                "ratio_B_over_D": (round(marB / marD, 3) if marD else None),
                "ratio_C_over_D": (round(marC / marD, 3) if marD else None)},
            "token_profligate_check_B_gt_5x_C": profligate,
            "qtype": qtype_block(records, gold),
            "first_read_precision": {
                p: per[p]["first_read_precision"] for p in AGENTIC},
            "stop_decomposition": {
                p: {"mis_routed_rate": per[p]["mis_routed_rate"],
                    "true_stop_rate": per[p]["true_stop_rate"],
                    "non_hydrated_rate": per[p]["non_hydrated_rate"]}
                for p in AGENTIC},
            "error_rates": {p: per[p]["error_rate"] for p in POLICIES},
            "accuracy_B_vs_C_fisher_exact_p": fisher_exact_two_sided(
                per["B"]["accuracy"]["numerator"],
                per["B"]["scored"] - per["B"]["accuracy"]["numerator"],
                per["C"]["accuracy"]["numerator"],
                per["C"]["scored"] - per["C"]["accuracy"]["numerator"]),
            # --- correction v4: annotations + sensitivity (NEVER a verdict)
            "question_set_annotations": {
                name: {"qids": sorted(d), "n": len(d), "conditions": d}
                for name, d in sorted(annotations.items())},
            "sensitivity_rows": sensitivity,
            "sensitivity_note":
                "Correction v4 H4. Both rows re-run the identical computation "
                "over a subset and are non-adjudicating. The verdict is the "
                "primary computation on the full confirmatory set; a row that "
                "disagrees is a reported finding, not a tiebreak. "
                "`outside_generation_slice` is a provenance annotation and "
                "excludes nothing (v4 H3).",
            "c_authoring_cost": {
                "authoring_tokens": authoring_tokens,
                "total_unamortized": totC,
                "total_amortized": totCam,
                "per_question": per["C"].get("authoring_tokens_per_q")},
        },
    }
    return effect


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=H.RUNS)
    ap.add_argument("--questions", default=os.path.join(
        HERE, f"questions-{DATE}.json"))
    ap.add_argument("--index", default=os.path.join(HERE, f"index-{DATE}.json"))
    ap.add_argument("--manifest", default=H.MANIFEST)
    ap.add_argument("--snapshot", default=H.SNAPSHOT_DIR)
    ap.add_argument("--study-dir", default=HERE)
    ap.add_argument("--out", default=os.path.join(
        HERE, f"effect-table-{DATE}.json"))
    args = ap.parse_args()
    effect = adjudicate(args.runs, args.questions, args.index, args.manifest,
                        args.snapshot, args.study_dir,
                        expect_files=H.EXPECTED_CORPUS_FILES)
    blob = json.dumps(effect, indent=1, sort_keys=True) + "\n"
    with open(args.out, "w") as fh:
        fh.write(blob)
    print(blob, end="")


if __name__ == "__main__":
    sys.exit(main())
