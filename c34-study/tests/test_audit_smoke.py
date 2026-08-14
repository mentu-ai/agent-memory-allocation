#!/usr/bin/env python3
"""C34 M2 tests — the excluded-smoke gate and its dead runs.

The C33 lesson this gate exists for: a pilot in which every provider call was
rejected before inference produced a full set of run records, and the auditor
passed it. Offline only.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import audit_smoke as S        # noqa: E402
import fixtures as F           # noqa: E402
import harness_lib as H        # noqa: E402

N_CONF, N_SMOKE = 110, 10
HEALTHY = {"B": dict(n_located=8, n_correct=7, tot=13_000, marg=2_200),
           "C": dict(n_located=5, n_correct=4, tot=9_000, marg=1_500),
           "D": dict(n_correct=9, tot=2_500, marg=300)}


class SmokeCase(unittest.TestCase):

    def build(self, plan=None, mutate=None, edit=None, answers=None):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        man, snap, entries = F.make_corpus(tmp, N_CONF + N_SMOKE,
                                           mutate=mutate)
        q, questions = F.make_questions(tmp, N_CONF, N_SMOKE, snap)
        idx = F.make_index(tmp, questions)
        runs = F.make_runs(tmp, questions, plan or HEALTHY,
                           which_set="smoke")
        F.make_runs(tmp, questions, F.plan_supported())
        if edit:
            edit(runs)
        self.tmp, self.runs, self.q, self.idx = tmp, runs, q, idx
        self.man, self.snap = man, snap
        return S.audit(runs, q, idx, man, snap, tmp,
                       expect_files=len(entries))

    def failed_checks(self, report):
        return sorted(f["check"] for f in report["findings"])


class TestHealthySmokeRun(SmokeCase):

    def test_a_healthy_smoke_run_passes_every_check(self):
        r = self.build()
        self.assertTrue(r["passed"], r["findings"])
        self.assertEqual(r["smoke_records"], N_SMOKE * 3)
        self.assertEqual(r["expected_records"], N_SMOKE * 3)
        self.assertTrue(r["adjudicator_ran_end_to_end"])
        self.assertFalse(r["adjudicator_smoke_verdict_bearing"])

    def test_two_independent_replays_are_byte_identical(self):
        first = self.build()
        second = S.audit(self.runs, self.q, self.idx, self.man, self.snap,
                         self.tmp, expect_files=N_CONF + N_SMOKE)
        self.assertEqual(json.dumps(first, indent=1, sort_keys=True),
                         json.dumps(second, indent=1, sort_keys=True))

    def test_the_smoke_records_declare_themselves_barred(self):
        self.build()
        with open(os.path.join(self.runs, "q111_B.json")) as fh:
            rec = json.load(fh)
        self.assertEqual(rec["set"], "smoke")
        self.assertTrue(rec["barred_from_adjudication"])


class TestDeadRuns(SmokeCase):
    """Phase-H rule 1: constructed total failures the gate must catch."""

    def test_dead_run_hollow_pilot_every_call_rejected_before_inference(self):
        """C33's first pilot: zero input tokens on every call, and its
        auditor passed it. This one must not."""
        plan = {p: dict(HEALTHY[p], input_tokens=0, tot=0, marg=0)
                for p in HEALTHY}
        r = self.build(plan)
        self.assertFalse(r["passed"])
        self.assertIn("nonzero_input_tokens", self.failed_checks(r))

    def test_dead_run_resolved_model_identity_differs_from_the_pin(self):
        plan = {p: dict(HEALTHY[p], identities=["claude-sonnet-5"])
                for p in HEALTHY}
        r = self.build(plan)
        self.assertFalse(r["passed"])
        self.assertIn("resolved_model_identity", self.failed_checks(r))

    def test_dead_run_missing_hydration_record_on_an_agentic_arm(self):
        plan = dict(HEALTHY)
        plan["B"] = dict(HEALTHY["B"], hydration=False)
        r = self.build(plan)
        self.assertFalse(r["passed"])
        self.assertIn("hydration_record_present", self.failed_checks(r))

    def test_dead_run_corpus_mutated_after_snapshot(self):
        r = self.build(mutate="docs/doc002.md")
        self.assertFalse(r["passed"])
        self.assertIn("corpus_snapshot_verified", self.failed_checks(r))

    def test_dead_run_degenerate_provider_output(self):
        """Healthy token counts, healthy identities, and no evidence: every
        answer identical. Added under Phase-H rule 1 alongside its dead run."""
        plan = {p: dict(HEALTHY[p], answer="ANSWER") for p in HEALTHY}
        r = self.build(plan)
        self.assertFalse(r["passed"])
        self.assertIn("provider_output_not_degenerate",
                      self.failed_checks(r))

    def test_dead_run_smoke_record_not_marked_barred(self):
        def unmark(runs):
            path = os.path.join(runs, "q112_C.json")
            with open(path) as fh:
                rec = json.load(fh)
            rec["barred_from_adjudication"] = False
            with open(path, "w") as fh:
                json.dump(rec, fh, indent=1, sort_keys=True)
        r = self.build(edit=unmark)
        self.assertFalse(r["passed"])
        self.assertIn("smoke_records_marked_barred", self.failed_checks(r))

    def test_a_hollow_run_fails_on_more_than_one_check(self):
        """The hollow failure mode is over-determined; the audit should say so
        rather than resting on a single signal."""
        plan = {p: dict(HEALTHY[p], input_tokens=0, tot=0, marg=0,
                        identities=[], answer="") for p in HEALTHY}
        r = self.build(plan)
        checks = self.failed_checks(r)
        self.assertIn("nonzero_input_tokens", checks)
        self.assertIn("resolved_model_identity", checks)
        self.assertIn("provider_output_not_degenerate", checks)


if __name__ == "__main__":
    unittest.main(verbosity=2)
