#!/usr/bin/env python3
"""C34 M2 tests — the campaign runner: ordering, no-re-roll, retries, budget.

`H.run_claude` is replaced by an offline stub for these tests. No provider is
contacted, no subprocess is spawned, and the stub is installed on the harness
module so the runner's real ledger, retry and record logic is what executes.
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

import fixtures as F           # noqa: E402
import harness_lib as H        # noqa: E402
import run_policies as P       # noqa: E402

N_CONF, N_SMOKE = 12, 4


class StubProvider:
    """Offline stand-in for `claude -p`. Records every dispatch so ordering
    and budget behavior are observable."""

    def __init__(self, outcome=None):
        self.calls = []
        self.outcome = outcome or (lambda n, model, kw: {})

    def __call__(self, prompt, model, allowed_tools=None, cwd=None,
                 stream=False, timeout=420, ledger=None, bucket=None,
                 key=None):
        if ledger is not None:
            ledger.reserve(bucket, key, model)
        self.calls.append({"bucket": bucket, "key": key, "model": model,
                           "tools": allowed_tools, "prompt": prompt})
        base = {"answer": "alpha-001-omega", "input_tokens": 1000,
                "input_uncached": 10, "cache_creation_tokens": 90,
                "cache_read_tokens": 900, "output_tokens": 20,
                "tokens_total": 1020, "tokens_marginal": 120,
                "model_requested": model, "model_identities": [model],
                "is_error": False, "error_class": None,
                "started_at": 1_800_000_500.0, "duration_s": 1.0,
                "reads": [], "searches": [], "saw_assistant": True}
        base.update(self.outcome(len(self.calls), model, key))
        return base


class RunnerCase(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        man, snap, entries = F.make_corpus(self.tmp, N_CONF + N_SMOKE)
        self.q, self.questions = F.make_questions(self.tmp, N_CONF, N_SMOKE,
                                                  snap)
        F.make_index(self.tmp, self.questions)
        self.camp = P.Campaign(self.tmp)
        self.camp.expect_files = len(entries)
        self.camp.sandbox = os.path.join(self.tmp, "sandbox")
        self.real = H.run_claude
        self.addCleanup(setattr, H, "run_claude", self.real)

    def install(self, stub):
        self.stub = stub
        H.run_claude = stub

    def probe(self):
        self.camp.reality_probe()


class TestOrdering(RunnerCase):

    def test_reality_probe_runs_before_any_other_call(self):
        """Correction v2 C-5, enforced by the ledger rather than by
        convention: a stage refuses to start without it."""
        self.install(StubProvider())
        with self.assertRaises(SystemExit) as cm:
            self.camp.run_stage("smoke")
        self.assertIn("reality probe not complete", str(cm.exception))
        self.assertEqual(self.stub.calls, [])

    def test_probe_spends_exactly_two_calls_one_per_role(self):
        self.install(StubProvider())
        out = self.camp.reality_probe()
        self.assertTrue(out["probe_passed"])
        self.assertEqual([c["model"] for c in self.stub.calls],
                         [H.GENERATOR, H.ANSWERER])
        self.assertEqual(H.CallLedger(self.camp.ledger_path).total(), 2)

    def test_a_failed_probe_seals_pinned_answerer_unavailable(self):
        self.install(StubProvider(
            lambda n, model, key: {"model_identities": ["some-other-model"]}))
        out = self.camp.reality_probe()
        self.assertFalse(out["probe_passed"])
        self.assertEqual([m["reason"] for m in H.stop_markers(self.tmp)],
                         ["pinned_answerer_unavailable"])

    def test_smoke_precedes_confirmatory_in_the_budget_ledger(self):
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("smoke")
        self.camp.run_stage("confirmatory")
        buckets = [c["bucket"] for c in self.stub.calls]
        self.assertEqual(buckets[:2], ["reality_probe"] * 2)
        self.assertEqual(set(buckets[2:2 + N_SMOKE * 3]), {"smoke"})
        self.assertEqual(set(buckets[2 + N_SMOKE * 3:]), {"confirmatory"})


class TestRecordDiscipline(RunnerCase):

    def test_three_arms_run_and_only_the_agentic_ones_get_tools(self):
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        tools = {}
        for c in self.stub.calls[2:]:
            tools[c["key"].split(":")[2].split("#")[0]] = c["tools"]
        self.assertEqual(tools["B"], ["Grep", "Glob", "Read"])
        self.assertEqual(tools["C"], ["Read"])
        self.assertIsNone(tools["D"])

    def test_hydration_is_written_for_both_agentic_arms(self):
        """Deviation D-6."""
        self.install(StubProvider(
            lambda n, model, key: {"reads": ["/s/docs/doc001.md"],
                                   "searches": [{"tool": "Grep",
                                                 "pattern": "a",
                                                 "path": ""}]}))
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        for policy in ("B", "C"):
            rec = self.camp.existing("q001", policy)
            self.assertTrue(H.hydration_complete(rec), policy)
            self.assertTrue(rec["hydration"]["located"])
        self.assertNotIn("hydration", self.camp.existing("q001", "D"))

    def test_smoke_records_are_marked_barred_in_the_record(self):
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("smoke", workers=1)
        rec = self.camp.existing("q013", "B")
        self.assertEqual(rec["set"], "smoke")
        self.assertTrue(rec["barred_from_adjudication"])

    def test_D_receives_the_gold_document_and_no_tools(self):
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        d = next(c for c in self.stub.calls if c["key"].endswith(":D#0"))
        self.assertIn("alpha-", d["prompt"])
        self.assertIn("Do not use any tools.", d["prompt"])
        self.assertIsNone(d["tools"])

    def test_C_receives_the_index_and_B_does_not(self):
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        b = next(c for c in self.stub.calls if c["key"].endswith(":B#0"))
        c = next(x for x in self.stub.calls if x["key"].endswith(":C#0"))
        self.assertNotIn("INDEX:", b["prompt"])
        self.assertIn("INDEX:", c["prompt"])
        self.assertIn("docs/doc001.md — ", c["prompt"])


class TestNoReRoll(RunnerCase):

    def test_a_scored_record_is_never_re_run(self):
        """Registration §4: a scored answer is never re-rolled. Checkable by
        record identity, not by assertion — the attempts log holds every
        attempt ever made."""
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        first = len(self.stub.calls)
        self.camp.run_stage("confirmatory", workers=1)          # resume
        self.assertEqual(len(self.stub.calls), first)
        self.camp.run_stage("confirmatory", retry=True, workers=1)
        self.assertEqual(len(self.stub.calls), first)
        for name in sorted(os.listdir(self.camp.attempts)):
            with open(os.path.join(self.camp.attempts, name)) as fh:
                lines = [json.loads(x) for x in fh if x.strip()]
            self.assertEqual(sum(1 for r in lines if P.is_scored(r)), 1, name)

    def test_the_write_site_refuses_to_overwrite_a_scored_record(self):
        """Finding G-M2-6: the guarantee lives at the write site, so it holds
        for every caller by construction rather than by the shape of the call
        graph. Called directly here, bypassing the job planner entirely."""
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        scored = self.camp.existing("q001", "B")
        self.assertTrue(P.is_scored(scored))
        with self.assertRaises(P.ScoredRecordExists):
            self.camp.write_record("q001", "B", dict(scored, answer="forged"))
        self.assertEqual(self.camp.existing("q001", "B")["answer"],
                         scored["answer"])

    def test_the_write_site_allows_replacing_an_error_record(self):
        rec = {"qid": "q001", "policy": "B", "is_error": True,
               "error": "timeout", "error_class": "subprocess_timeout"}
        self.camp.write_record("q001", "B", rec)
        self.camp.write_record("q001", "B", dict(rec, answer="recovered",
                                                 is_error=False, error=None))
        self.assertEqual(self.camp.existing("q001", "B")["answer"],
                         "recovered")
        with self.assertRaises(P.ScoredRecordExists):
            self.camp.write_record("q001", "B", rec)

    def test_only_registered_error_classes_are_retried(self):
        def outcome(n, model, key):
            if key and key.startswith("confirmatory:q001:B"):
                return {"is_error": True, "error": "provider_error",
                        "error_class": "provider_error_unclassified"}
            if key and key.startswith("confirmatory:q002:B"):
                return {"is_error": True, "error": "timeout",
                        "error_class": "subprocess_timeout"}
            return {}
        self.install(StubProvider(outcome))
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        before = len(self.stub.calls)
        self.camp.run_stage("confirmatory", retry=True, workers=1)
        retried = [c["key"] for c in self.stub.calls[before:]]
        self.assertEqual(retried, ["retry:q002:B#1"])
        self.assertEqual(
            self.camp.existing("q002", "B")["retry_of_class"],
            "subprocess_timeout")

    def test_a_retry_is_charged_to_the_reserve_not_the_original_bucket(self):
        def outcome(n, model, key):
            return ({"is_error": True, "error": "timeout",
                     "error_class": "subprocess_timeout"}
                    if key and key.startswith("confirmatory:q003:C")
                    else {})
        self.install(StubProvider(outcome))
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        self.camp.run_stage("confirmatory", retry=True, workers=1)
        counts = H.CallLedger(self.camp.ledger_path).counts()
        self.assertEqual(counts["confirmatory"], N_CONF * 3)
        self.assertEqual(counts["retry"], 1)

    def test_every_attempt_is_preserved_including_errors(self):
        def outcome(n, model, key):
            return ({"is_error": True, "error": "timeout",
                     "error_class": "subprocess_timeout"}
                    if key and key.startswith("confirmatory:q004:B")
                    else {})
        self.install(StubProvider(outcome))
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        self.camp.run_stage("confirmatory", retry=True, workers=1)
        with open(self.camp.attempts_path("q004", "B")) as fh:
            lines = [json.loads(x) for x in fh if x.strip()]
        self.assertEqual(len(lines), 2)
        self.assertEqual([r["budget_bucket"] for r in lines],
                         ["confirmatory", "retry"])


class TestBudgetEnforcement(RunnerCase):

    def test_dead_run_sub_ceiling_exhaustion_seals_the_stop_marker(self):
        self.install(StubProvider())
        self.probe()
        led = H.CallLedger(self.camp.ledger_path)
        for i in range(H.SUB_CEILINGS["confirmatory"]):
            led.reserve("confirmatory", f"filler:{i}", H.ANSWERER)
        with self.assertRaises(H.CeilingExhausted):
            self.camp.run_stage("confirmatory", workers=1)
        self.assertIn("registered_budget_exhausted",
                      [m["reason"] for m in H.stop_markers(self.tmp)])

    def test_cross_run_discovery_prevents_double_spending_a_lost_ledger(self):
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        spent = H.CallLedger(self.camp.ledger_path).total()
        os.remove(self.camp.ledger_path)                 # lose the ledger
        os.remove(self.camp.ledger_path + ".head.json")  # journal AND head
        rebuilt = self.camp.ledger()
        self.assertEqual(rebuilt.total(), spent)
        self.assertEqual(rebuilt.counts()["confirmatory"], N_CONF * 3)
        self.assertTrue(rebuilt.probe_complete())

    def test_the_sandbox_is_assembled_from_the_snapshot_each_run(self):
        self.install(StubProvider())
        self.probe()
        self.camp.run_stage("confirmatory", workers=1)
        self.assertTrue(os.path.isdir(self.camp.sandbox))
        with open(os.path.join(self.camp.sandbox, "docs", "doc001.md")) as fh:
            self.assertIn("alpha-001-omega", fh.read())

    def test_a_mutated_snapshot_stops_the_stage_before_any_call(self):
        self.install(StubProvider())
        self.probe()
        with open(os.path.join(self.camp.snapshot, "docs", "doc002.md"),
                  "ab") as fh:
            fh.write(b"\ntampered\n")
        before = len(self.stub.calls)
        with self.assertRaises(SystemExit) as cm:
            self.camp.run_stage("confirmatory", workers=1)
        self.assertIn("SNAPSHOT HASH MISMATCH", str(cm.exception))
        self.assertEqual(len(self.stub.calls), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
