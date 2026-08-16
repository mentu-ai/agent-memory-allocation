"""c36 mechanical adjudication — frozen thresholds, verdict from records only.

Thresholds are transcribed from corpus/conjectures/c36-fused-locator-localization.md
(frozen 2026-08-16, commit 8604a09) and may not be edited here or there.
Interpretation never changes the verdict.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs-c36")

P1_MIN_PP = 5.0          # L2 - L0 localization, confirmatory set
P3_MIN_PP = 8.0          # Spanish-gold subset, L2 - L0
P3_MIN_N = 25            # subset power guard
P4_BUILD_MS = 15_000     # median of 5 cold builds
P4_QUERY_MS = 500        # median added per-query, L2 vs L0


def rates(records, key="located"):
    n = len(records)
    return (100.0 * sum(1 for r in records if r[key]) / n, n) if n else (None, 0)


def main():
    loc = [json.loads(line) for line in open(os.path.join(RUNS, "localization.jsonl"))]
    confirmatory = [r for r in loc if r["set"] == "confirmatory"]
    by_arm = {arm: [r for r in confirmatory if r["arm"] == arm] for arm in ("L0", "L1", "L2", "L4")}
    l0, n0 = rates(by_arm["L0"]); l1, _ = rates(by_arm["L1"])
    l2, n2 = rates(by_arm["L2"]); l4, _ = rates(by_arm["L4"])
    assert n0 == n2 and n0 > 0, "arms must cover identical confirmatory denominators"

    metrics = json.load(open(os.path.join(HERE, "metrics-c36.json")))

    subset_path = os.path.join(HERE, "spanish-gold-c36.json")
    spanish = set(json.load(open(subset_path))) if os.path.exists(subset_path) else set()
    es = {arm: [r for r in by_arm[arm] if r["rp"] in spanish] for arm in ("L0", "L2")}
    es_l0, es_n = rates(es["L0"]); es_l2, _ = rates(es["L2"])

    p5 = {}
    for arm in ("L0", "L2"):
        path = os.path.join(RUNS, f"p5-{arm}.jsonl")
        if os.path.exists(path):
            records = [json.loads(line) for line in open(path)]
            if records:
                # The boundary rule adjudicates; the C34 rule ships descriptively.
                p5[arm] = 100.0 * sum(1 for r in records if r["score"]["boundary"]) / len(records)

    p1_delta = l2 - l0
    p1 = p1_delta >= P1_MIN_PP
    p2 = l2 >= l1
    p3_powered = es_n >= P3_MIN_N
    p3 = (es_l2 - es_l0 >= P3_MIN_PP) if p3_powered else None
    p4 = (metrics["cold_build_ms_median"] <= P4_BUILD_MS
          and metrics["added_ms_L2_vs_L0_median"] <= P4_QUERY_MS)
    p5_pass = (p5.get("L2", 0) - p5.get("L0", 0) >= 0.0) if len(p5) == 2 else None

    if p1_delta <= 0.0:
        verdict = "refuted"
    elif p1 and p2 and p4 and (p3 is not False) and (p5_pass is not False):
        verdict = "supported"
    else:
        verdict = "revised"

    result = {
        "localization_pct": {"L0": l0, "L1": l1, "L2": l2, "L4": l4, "n": n0},
        "P1": {"delta_pp": round(p1_delta, 1), "threshold": P1_MIN_PP, "pass": p1},
        "P2": {"L2": l2, "L1": l1, "pass": p2},
        "P3": {"n": es_n, "powered": p3_powered,
               "delta_pp": round(es_l2 - es_l0, 1) if p3_powered else None, "pass": p3},
        "P4": {"build_ms": metrics["cold_build_ms_median"],
               "added_query_ms": metrics["added_ms_L2_vs_L0_median"], "pass": p4},
        "P5": {"accuracy_pct": p5, "pass": p5_pass},
        "verdict": verdict,
    }
    print(json.dumps(result, indent=1, sort_keys=True))
    with open(os.path.join(HERE, "adjudication-c36.json"), "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
