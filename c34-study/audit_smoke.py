#!/usr/bin/env python3
"""C34 — the excluded-smoke gate (M5).

The 10 smoke questions run all three policies (30 calls) and are audited
BEFORE any confirmatory call. Smoke questions are permanently barred from
adjudication, from every denominator and from the effect table.

The audit verifies, mechanically (registration §4):
  1. nonzero input tokens on every call — no request rejected at the API
     boundary (the C33 hollow-pilot failure mode);
  2. the resolved model identity equals the pinned identity on every call;
  3. a hydration record is present for every B and C run (deviation D-6);
  4. the corpus sandbox hash-verifies against the committed snapshot;
  5. the adjudicator runs end to end on the smoke records.

One check beyond the registered list, added under Phase-H rule 1 and shipping
with its own dead run: `provider_output_not_degenerate` — a run set whose
answers are all empty, or all byte-identical, is not evidence even when every
token count is healthy. Adding an audit check can only make the gate stricter;
it relaxes no threshold and touches no verdict criterion.

Deterministic: two independent replays produce byte-identical artifacts
(no timestamps, sorted keys).

Usage: python3 audit_smoke.py [--runs DIR] [--out PATH]
"""
import argparse
import glob
import json
import os
import sys

import adjudicate as A
import harness_lib as H

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-08-13"


def load_smoke_records(runs_dir, smoke_ids):
    out = []
    for path in sorted(glob.glob(os.path.join(runs_dir, "q*_*.json"))):
        with open(path) as fh:
            r = json.load(fh)
        if r["qid"] in smoke_ids:
            out.append(r)
    return out


def audit(runs_dir, questions_path, index_path, manifest_path, snapshot_dir,
          study_dir, expect_files=None):
    with open(questions_path) as fh:
        qdata = json.load(fh)
    smoke_ids = {q["id"] for q in qdata["questions"]
                 if q.get("set") == "smoke"}
    records = load_smoke_records(runs_dir, smoke_ids)

    findings = []

    # 1. nonzero input tokens on every call
    hollow = sorted(f"{r['qid']}_{r['policy']}" for r in records
                    if not r.get("input_tokens"))
    if hollow:
        findings.append({"check": "nonzero_input_tokens", "failed": hollow})

    # 2. resolved model identity equals the pin
    drift = sorted(f"{r['qid']}_{r['policy']}" for r in records
                   if r.get("model_identities") != [H.ANSWERER])
    if drift:
        findings.append({"check": "resolved_model_identity", "failed": drift})

    # 3. hydration record on every B and C run
    missing = sorted(f"{r['qid']}_{r['policy']}" for r in records
                     if r.get("policy") in ("B", "C")
                     and not H.hydration_complete(r))
    if missing:
        findings.append({"check": "hydration_record_present",
                         "failed": missing})

    # 4. sandbox hash-verifies against the snapshot
    snap_causes, snap_detail = A.verify_snapshot(manifest_path, snapshot_dir,
                                                 expect_files)
    if snap_causes:
        findings.append({"check": "corpus_snapshot_verified",
                         "failed": snap_causes, "detail": snap_detail})

    # 5. records are marked barred, in the records themselves
    unmarked = sorted(f"{r['qid']}_{r['policy']}" for r in records
                      if not r.get("barred_from_adjudication"))
    if unmarked:
        findings.append({"check": "smoke_records_marked_barred",
                         "failed": unmarked})

    # 6. provider output is not degenerate (Phase-H rule 1 addition)
    answers = [(r.get("answer") or "").strip() for r in records
               if not (r.get("error") or r.get("is_error"))]
    degenerate = bool(answers) and (
        all(not a for a in answers) or len(set(answers)) == 1)
    if degenerate or not answers:
        findings.append({"check": "provider_output_not_degenerate",
                         "failed": ["all answers empty or identical"
                                    if answers else "no scored smoke record"],
                         "distinct_answers": len(set(answers))})

    # 7. the adjudicator runs end to end on the smoke records
    adjudicator_ran, adjudicator_error = False, None
    smoke_effect = None
    try:
        smoke_effect = A.adjudicate(runs_dir, questions_path, index_path,
                                    manifest_path, snapshot_dir, study_dir,
                                    expect_files=expect_files,
                                    include_set="smoke",
                                    check_flags=False)
        adjudicator_ran = True
    except Exception as exc:                              # gate, not a crash
        adjudicator_error = f"{type(exc).__name__}: {exc}"
        findings.append({"check": "adjudicator_end_to_end",
                         "failed": [adjudicator_error]})

    report = {
        "gate": "excluded_smoke_audit",
        "passed": not findings,
        "findings": findings,
        "smoke_questions": sorted(smoke_ids),
        "smoke_records": len(records),
        "expected_records": len(smoke_ids) * 3,
        "adjudicator_ran_end_to_end": adjudicator_ran,
        "adjudicator_error": adjudicator_error,
        "adjudicator_smoke_verdict": (smoke_effect or {}).get("verdict"),
        "adjudicator_smoke_verdict_bearing": False,
        "note": "smoke records are permanently barred from adjudication, "
                "from every denominator and from the effect table; the "
                "verdict above is an end-to-end liveness check only",
    }
    return report


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
        HERE, f"smoke-audit-{DATE}.json"))
    args = ap.parse_args()
    report = audit(args.runs, args.questions, args.index, args.manifest,
                   args.snapshot, args.study_dir,
                   expect_files=H.EXPECTED_CORPUS_FILES)
    blob = json.dumps(report, indent=1, sort_keys=True) + "\n"
    with open(args.out, "w") as fh:
        fh.write(blob)
    print(blob, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
