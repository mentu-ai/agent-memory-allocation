#!/usr/bin/env python3
"""C34 M2 tests — the frozen adjudicator: every verdict branch, every named
machine reason, every dead run, and byte-identity across replays.

Offline only. Fixtures are synthetic run records; no provider is contacted.
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

import adjudicate as A         # noqa: E402
import fixtures as F           # noqa: E402
import harness_lib as H        # noqa: E402

N_CONF, N_SMOKE = 110, 10
# The synthetic fixture corpus carries no degenerate, leaked or
# out-of-slice gold, so the correct expectation for a fixture is "all empty".
# Passing it keeps the v4 flag gate LIVE in every adjudicator test rather than
# switching it off, so a fixture that acquires such a gold fails loudly.
NO_FLAGS = {"scoring_degenerate": (), "index_leak": (),
            "outside_generation_slice": ()}

SMOKE_PLAN = {"B": dict(n_located=8, n_correct=7, tot=1000, marg=100),
              "C": dict(n_located=5, n_correct=4, tot=900, marg=90),
              "D": dict(n_correct=9, tot=500, marg=50)}


class Case(unittest.TestCase):
    """Builds a whole synthetic study and adjudicates it."""

    def build(self, plan, n_conf=N_CONF, n_smoke=N_SMOKE, mutate=None,
              validated=None, break_provenance=(), authoring_tokens=50_000,
              expect_files=None, smoke=True, stops=(), edit=None,
              drop_manifest=False, expected_flags=NO_FLAGS):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        man, snap, entries = F.make_corpus(tmp, n_conf + n_smoke,
                                           mutate=mutate)
        q, questions = F.make_questions(tmp, n_conf, n_smoke, snap,
                                        validated=validated,
                                        break_provenance=break_provenance)
        idx = F.make_index(tmp, questions, authoring_tokens=authoring_tokens)
        runs = F.make_runs(tmp, questions, plan)
        if smoke:
            F.make_runs(tmp, questions, SMOKE_PLAN, which_set="smoke")
        for reason in stops:
            with open(os.path.join(tmp, f"STOP-{reason}.json"), "w") as fh:
                json.dump({"reason": reason, "detail": {}}, fh)
        if edit:
            edit(runs)
        if drop_manifest:
            os.remove(man)
        self.tmp, self.runs, self.q, self.idx = tmp, runs, q, idx
        self.man, self.snap = man, snap
        return A.adjudicate(runs, q, idx, man, snap, tmp,
                            expect_files=(len(entries)
                                          if expect_files is None
                                          else expect_files),
                            expected_flags=expected_flags)


def edit_record(path):
    def apply(fn):
        def _inner(runs):
            full = os.path.join(runs, path)
            with open(full) as fh:
                rec = json.load(fh)
            fn(rec)
            with open(full, "w") as fh:
                json.dump(rec, fh, indent=1, sort_keys=True)
        return _inner
    return apply


# ---------------------------------------------------------------------------
class TestSupported(Case):

    def setUp(self):
        self.effect = self.build(F.plan_supported())

    def test_verdict_is_supported(self):
        self.assertEqual(self.effect["verdict"], "supported")
        self.assertEqual(self.effect["verdict_reason"],
                         "P1_P2_P3prime_P4_P5_all_pass")
        self.assertEqual(self.effect["failed_predictions"], [])

    def test_all_five_predictions_pass(self):
        self.assertEqual(set(self.effect["predictions"].values()), {True})

    def test_smoke_records_are_barred_from_every_denominator(self):
        self.assertEqual(self.effect["records_barred"], N_SMOKE * 3)
        for p in ("B", "C", "D"):
            self.assertEqual(self.effect["per_policy"][p]["scored"], N_CONF)

    def test_verdict_legibility_headline_is_top_level(self):
        """Correction v2 C-12: P1 / P3' / P5 sit beside the verdict word."""
        h = self.effect["headline"]
        self.assertEqual(sorted(h), ["P1_accuracy_parity",
                                     "P3prime_wrong_stop_tax",
                                     "P5_localization_advantage"])
        self.assertIn("acc_B", h["P1_accuracy_parity"])
        self.assertIn("wrong_stop_rate_C", h["P3prime_wrong_stop_tax"])
        self.assertIn("localization_rate_B", h["P5_localization_advantage"])

    def test_non_adjudicating_comparability_block_is_complete(self):
        na = self.effect["non_adjudicating"]
        for key in ("c29_asymmetric_P3", "P2_on_marginal_not_adjudicated",
                    "P4_on_totals_not_adjudicated", "qtype",
                    "first_read_precision", "stop_decomposition",
                    "error_rates", "accuracy_B_vs_C_fisher_exact_p",
                    "c_authoring_cost"):
            self.assertIn(key, na)

    def test_p4_adjudicates_on_marginal_and_reports_totals_alongside(self):
        """Deviation D-3: the measure is frozen with the threshold."""
        na = self.effect["non_adjudicating"]
        self.assertIn("ratio_B_over_D", na["P4_adjudicated_ratios_marginal"])
        self.assertIn("ratio_B_over_D", na["P4_on_totals_not_adjudicated"])
        self.assertFalse(na["P4_on_totals_not_adjudicated"].get(
            "adjudicating", False))

    def test_mis_routed_and_true_stop_decompose_the_wrong_stops(self):
        for p in ("B", "C"):
            s = self.effect["per_policy"][p]
            self.assertEqual(
                s["mis_routed_rate"]["numerator"]
                + s["true_stop_rate"]["numerator"],
                s["wrong_stop_rate"]["numerator"])

    def test_every_rate_carries_denominator_and_status(self):
        """Phase-H rule 4."""
        def walk(node):
            if isinstance(node, dict):
                if set(node) >= {"value", "numerator", "denominator",
                                 "status"}:
                    self.assertIn(node["status"],
                                  ("observed", "zero_events",
                                   "not_exercised"))
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(self.effect)

    def test_two_runs_are_byte_identical(self):
        again = A.adjudicate(self.runs, self.q, self.idx, self.man, self.snap,
                             self.tmp, expect_files=N_CONF + N_SMOKE,
                             expected_flags=NO_FLAGS)
        self.assertEqual(json.dumps(self.effect, indent=1, sort_keys=True),
                         json.dumps(again, indent=1, sort_keys=True))

    def test_effect_table_carries_no_wall_clock(self):
        blob = json.dumps(self.effect)
        for token in ("started_at", "duration_s", "\"ts\""):
            self.assertNotIn(token, blob)


# ---------------------------------------------------------------------------
class TestRefuted(Case):

    def test_curation_dominates_triggers_refuted(self):
        e = self.build({
            "B": dict(n_located=94, n_correct=50, n_correct_among_nonlocated=2,
                      tot=200_000, marg=22_000),
            "C": dict(n_located=58, n_correct=80, n_correct_among_nonlocated=6,
                      tot=40_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        self.assertEqual(e["verdict"], "refuted")
        self.assertEqual(e["verdict_reason"], "curation_dominates")
        self.assertTrue(e["refutation_check"])


class TestRevisedNamedReasons(Case):
    """Each named single-failure reason from the registered verdict map."""

    def test_P1_accuracy_reversal_without_cost_dominance(self):
        e = self.build({
            "B": dict(n_located=94, n_correct=50, n_correct_among_nonlocated=2,
                      tot=100_000, marg=22_000),
            "C": dict(n_located=58, n_correct=80, n_correct_among_nonlocated=6,
                      tot=90_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        self.assertEqual(e["verdict"], "revised")
        self.assertEqual(e["verdict_reason"],
                         "accuracy_reversal_without_cost_dominance")
        self.assertEqual(e["failed_predictions"], ["P1"])
        self.assertFalse(e["refutation_check"])

    def test_P2_search_accurate_but_token_profligate(self):
        plan = F.plan_supported()
        plan["B"]["tot"] = 300_000
        e = self.build(plan)
        self.assertEqual(e["verdict"], "revised")
        self.assertEqual(e["verdict_reason"],
                         "search_accurate_but_token_profligate")
        self.assertEqual(e["failed_predictions"], ["P2"])

    def test_P3prime_no_wrong_stop_tax_at_power(self):
        e = self.build({
            "B": dict(n_located=60, n_correct=55,
                      n_correct_among_nonlocated=0,
                      tot=130_000, marg=22_000),
            "C": dict(n_located=58, n_correct=50,
                      n_correct_among_nonlocated=20,
                      tot=90_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        self.assertEqual(e["verdict"], "revised")
        self.assertEqual(e["verdict_reason"], "no_wrong_stop_tax_at_power")
        self.assertEqual(e["failed_predictions"], ["P3prime"])

    def test_P4_headroom_not_established_on_marginal_tokens(self):
        plan = F.plan_supported()
        plan["D"]["marg"] = 10_000
        e = self.build(plan)
        self.assertEqual(e["verdict"], "revised")
        self.assertEqual(e["verdict_reason"],
                         "headroom_not_established_on_marginal_tokens")
        self.assertEqual(e["failed_predictions"], ["P4"])
        # C29's own B sat at 2.85x on this measure: the foreseeable outcome,
        # and C-12 requires the curation answer to stay legible beside it
        self.assertTrue(e["headline"]["P1_accuracy_parity"]["pass"])
        self.assertTrue(e["headline"]["P3prime_wrong_stop_tax"]["pass"])
        self.assertTrue(e["headline"]["P5_localization_advantage"]["pass"])

    def test_P5_localization_advantage_not_reproduced(self):
        e = self.build({
            "B": dict(n_located=58, n_correct=79,
                      n_correct_among_nonlocated=52,
                      tot=130_000, marg=22_000),
            "C": dict(n_located=94, n_correct=78,
                      n_correct_among_nonlocated=0,
                      tot=90_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        self.assertEqual(e["verdict"], "revised")
        self.assertEqual(e["verdict_reason"],
                         "localization_advantage_not_reproduced")
        self.assertEqual(e["failed_predictions"], ["P5"])

    def test_multiple_failures_enumerate_each_one(self):
        plan = F.plan_supported()
        plan["B"]["tot"] = 300_000        # P2
        plan["D"]["marg"] = 10_000        # P4
        e = self.build(plan)
        self.assertEqual(e["verdict"], "revised")
        self.assertEqual(e["verdict_reason"],
                         "multiple_predictions_failed:P2+P4")
        self.assertEqual(e["failed_predictions"], ["P2", "P4"])


# ---------------------------------------------------------------------------
class TestP3PrimeTiesAndSymmetry(Case):

    def test_exact_tie_passes_P3prime(self):
        """Correction v2 C-8 / v3 G2: the operator is `>=`, so a tie PASSES,
        and `no_wrong_stop_tax_at_power` is reachable only on a strict
        reversal."""
        e = self.build({
            "B": dict(n_located=90, n_correct=79,
                      n_correct_among_nonlocated=0,
                      tot=130_000, marg=22_000),
            "C": dict(n_located=90, n_correct=52,
                      n_correct_among_nonlocated=0,
                      tot=90_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        h = e["headline"]["P3prime_wrong_stop_tax"]
        self.assertEqual(h["wrong_stop_rate_B"], h["wrong_stop_rate_C"])
        self.assertTrue(h["pass"])
        self.assertEqual(h["operator"], ">= (ties pass)")
        self.assertNotIn("P3prime", e["failed_predictions"])

    def test_wrong_stop_is_computed_for_B_by_the_same_rule(self):
        """Deviation D-2: C29 computed wrong-stop under `if p == "C"`, which
        made B's rate read as structurally zero. Here B has a rate."""
        e = self.build(F.plan_supported())
        b = e["per_policy"]["B"]["wrong_stop_rate"]
        self.assertGreater(b["value"], 0)
        self.assertEqual(b["denominator"], N_CONF)

    def test_c29_asymmetric_P3_is_reported_but_does_not_adjudicate(self):
        e = self.build(F.plan_supported())
        na = e["non_adjudicating"]["c29_asymmetric_P3"]
        self.assertIn("would_pass", na)
        self.assertNotEqual(na["c_wrong_stop_rate"],
                            na["b_wrong_answer_rate"])
        self.assertNotIn("asymmetric", e["verdict_reason"])


class TestP5bDenominatorFloor(Case):

    def test_below_20_pooled_the_conjunct_is_not_exercised(self):
        """Deviation D-9 (correction v2 C-6): below a pooled denominator of
        20, P5(b) is `not_exercised`, is reported with its denominator, and
        P5 adjudicates on P5(a) alone."""
        e = self.build({
            "B": dict(n_located=105, n_correct=100,
                      n_correct_among_nonlocated=5,
                      tot=130_000, marg=22_000),
            "C": dict(n_located=100, n_correct=95,
                      n_correct_among_nonlocated=10,
                      tot=90_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        p5 = e["headline"]["P5_localization_advantage"]
        self.assertEqual(p5["P5b_status"], "not_exercised")
        self.assertIsNone(p5["P5b_pass"])
        self.assertEqual(p5["P5b_pooled_non_hydrated"]["denominator"], 15)
        self.assertEqual(p5["P5b_min_denominator"], 20)
        self.assertTrue(p5["P5a_pass"])
        self.assertTrue(p5["pass"])          # rests on P5(a) alone
        self.assertEqual(e["verdict"], "supported")

    def test_at_or_above_20_the_conjunct_adjudicates(self):
        e = self.build(F.plan_supported())
        p5 = e["headline"]["P5_localization_advantage"]
        self.assertEqual(p5["P5b_status"], "adjudicating")
        self.assertGreaterEqual(p5["P5b_pooled_non_hydrated"]["denominator"],
                                20)
        self.assertTrue(p5["P5b_pass"])

    def test_exercised_but_failing_P5b_fails_P5(self):
        e = self.build({
            "B": dict(n_located=94, n_correct=79,
                      n_correct_among_nonlocated=16,
                      tot=130_000, marg=22_000),
            "C": dict(n_located=58, n_correct=52,
                      n_correct_among_nonlocated=52,
                      tot=90_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        p5 = e["headline"]["P5_localization_advantage"]
        self.assertTrue(p5["P5a_pass"])
        self.assertFalse(p5["P5b_pass"])
        self.assertFalse(p5["pass"])
        self.assertEqual(e["verdict_reason"],
                         "localization_advantage_not_reproduced")


# ---------------------------------------------------------------------------
class TestInstrumentInsufficientCauses(Case):

    def test_scored_question_floor(self):
        e = self.build(F.plan_supported(), n_conf=50, validated=130)
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "scored_question_floor")
        self.assertFalse(e["floors"]["scored_ge_100_each_BCD"])

    def test_dead_run_degenerate_all_invalid_run(self):
        """A run set in which every call errored must not adjudicate — and
        every zero must carry its denominator and `not_exercised` status
        rather than reading as a measured zero (Phase-H rule 4)."""
        plan = {p: dict(F.plan_supported()[p], errors=N_CONF)
                for p in ("B", "C", "D")}
        e = self.build(plan)
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "scored_question_floor")
        for p in ("B", "C", "D"):
            s = e["per_policy"][p]
            self.assertEqual(s["scored"], 0)
            self.assertEqual(s["errors"], N_CONF)
            self.assertEqual(s["accuracy"]["status"], "not_exercised")
            self.assertIsNone(s["accuracy"]["value"])

    def test_dead_run_missing_hydration_on_a_scored_B_run(self):
        """The instrument note's dead run: it must produce
        instrument-insufficient, not a silent zero."""
        e = self.build(F.plan_supported(),
                       edit=edit_record("q001_B.json")(
                           lambda r: r.pop("hydration")))
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "missing_hydration_record")
        self.assertEqual(
            e["instrument_insufficient_detail"]["missing_hydration_qids"],
            ["q001"])
        self.assertFalse(e["floors"]["hydration_records_complete"])

    def test_dead_run_model_identity_drift(self):
        e = self.build(F.plan_supported(),
                       edit=edit_record("q002_C.json")(
                           lambda r: r.update(
                               {"model_identities": ["claude-sonnet-5"]})))
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "model_identity_drift")
        self.assertFalse(
            e["floors"]["one_resolved_identity_per_pinned_model"])

    def test_dead_run_snapshot_hash_mismatch(self):
        e = self.build(F.plan_supported(), mutate="docs/doc004.md")
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "corpus_snapshot_hash_mismatch")
        self.assertEqual(
            e["instrument_insufficient_detail"]["mismatched"],
            ["docs/doc004.md"])

    def test_dead_run_corpus_precondition_failed(self):
        e = self.build(F.plan_supported(), expect_files=141)
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "corpus_precondition_failed")

    def test_dead_run_manifest_missing(self):
        e = self.build(F.plan_supported(), drop_manifest=True)
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "corpus_manifest_missing")

    def test_registered_budget_exhausted_stop_marker(self):
        e = self.build(F.plan_supported(),
                       stops=("registered_budget_exhausted",))
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "registered_budget_exhausted")

    def test_pinned_answerer_unavailable_stop_marker(self):
        e = self.build(F.plan_supported(),
                       stops=("pinned_answerer_unavailable",))
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "pinned_answerer_unavailable")

    def test_question_yield_shortfall(self):
        e = self.build(F.plan_supported(), validated=100)
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertEqual(e["verdict_reason"], "question_yield_shortfall")

    def test_causes_are_named_in_the_frozen_order(self):
        e = self.build(F.plan_supported(), n_conf=50, validated=100)
        self.assertEqual(e["instrument_insufficient_causes"],
                         ["question_yield_shortfall", "scored_question_floor"])
        self.assertEqual(e["verdict_reason"], "question_yield_shortfall")

    def test_registered_135_floor_branch_is_not_implemented(self):
        """Correction v3 G5: the <135 and >170 branches are dead. The
        precondition assertion replaces both, and no live code path may
        implement them."""
        with open(os.path.join(os.path.dirname(HERE), "adjudicate.py")) as fh:
            src = fh.read()
        self.assertNotIn("135", src.split('"""', 2)[2])
        self.assertNotIn("170", src.split('"""', 2)[2])
        self.assertIn("corpus_precondition_failed", A.II_ORDER)


# ---------------------------------------------------------------------------
class TestVoidAndPrecedence(Case):

    def test_generation_provenance_mismatch_voids_the_run_set(self):
        e = self.build(F.plan_supported(), break_provenance=("q003",))
        self.assertEqual(e["verdict"], "void")
        self.assertEqual(e["verdict_reason"], "question_set_contamination")
        self.assertEqual(
            [f["check"] for f in e["contamination_findings"]],
            ["generation_input_hash_mismatch"])

    def test_a_run_predating_the_question_freeze_is_contamination(self):
        """C29's frozen contamination rule, carried verbatim: no partial
        salvage."""
        found = A.contamination_findings(
            [], "/nonexistent", freeze_ts=1_800_000_100,
            records=[{"qid": "q001", "policy": "B",
                      "started_at": 1_800_000_000.0},
                     {"qid": "q002", "policy": "C",
                      "started_at": 1_800_000_200.0}])
        self.assertEqual([f["check"] for f in found],
                         ["run_predates_question_freeze"])
        self.assertEqual(found[0]["qid"], "q001")

    def test_void_precedes_instrument_insufficient(self):
        e = self.build(F.plan_supported(), n_conf=50,
                       break_provenance=("q003",))
        self.assertEqual(e["verdict"], "void")
        self.assertTrue(e["instrument_insufficient_causes"])   # both present

    def test_instrument_insufficient_precedes_refuted(self):
        e = self.build({
            "B": dict(n_located=94, n_correct=50, tot=200_000, marg=22_000),
            "C": dict(n_located=58, n_correct=80, tot=40_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)},
            edit=edit_record("q001_B.json")(lambda r: r.pop("hydration")))
        self.assertEqual(e["verdict"], "instrument-insufficient")
        self.assertTrue(e["refutation_check"])   # would have refuted


# ---------------------------------------------------------------------------
class TestLocalizationAndWrongStopDoNotCollapse(Case):
    """The instrument note's adjudicator dead run: every C answer correct
    while no gold file was read must yield localization 0 AND wrong-stop 0,
    with neither mistaken for the other."""

    def test_all_correct_never_located(self):
        e = self.build({
            "B": dict(n_located=94, n_correct=79,
                      n_correct_among_nonlocated=2,
                      tot=130_000, marg=22_000),
            "C": dict(n_located=0, n_correct=N_CONF,
                      n_correct_among_nonlocated=N_CONF,
                      tot=90_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        c = e["per_policy"]["C"]
        self.assertEqual(c["localization_rate"]["value"], 0.0)
        self.assertEqual(c["localization_rate"]["status"], "zero_events")
        self.assertEqual(c["wrong_stop_rate"]["value"], 0.0)
        self.assertEqual(c["wrong_stop_rate"]["status"], "zero_events")
        self.assertEqual(c["non_hydrated_rate"]["value"], 1.0)
        self.assertEqual(c["accuracy"]["value"], 1.0)
        self.assertEqual(c["mis_routed_rate"]["value"], 0.0)
        self.assertEqual(c["true_stop_rate"]["value"], 0.0)
        # the two zeros are distinct measurements, not one collapsed into
        # the other: localization is a hydration fact, wrong-stop is a joint
        # fact about hydration AND correctness
        self.assertNotEqual(c["localization_rate"]["denominator"], 0)
        self.assertNotEqual(c["non_hydrated_rate"]["numerator"],
                            c["wrong_stop_rate"]["numerator"])


class TestSmokeSetIsNeverAdjudicated(Case):

    def test_smoke_ids_are_absent_from_confirmatory_denominators(self):
        e = self.build(F.plan_supported())
        self.assertEqual(e["questions_confirmatory"], N_CONF)
        self.assertEqual(e["records_adjudicated"], N_CONF * 3)
        self.assertTrue(e["verdict_bearing"])
        self.assertEqual(e["adjudicated_set"], "confirmatory")

    def test_smoke_mode_is_marked_non_verdict_bearing(self):
        self.build(F.plan_supported())
        e = A.adjudicate(self.runs, self.q, self.idx, self.man, self.snap,
                         self.tmp, expect_files=N_CONF + N_SMOKE,
                         include_set="smoke", expected_flags=NO_FLAGS)
        self.assertFalse(e["verdict_bearing"])
        self.assertEqual(e["adjudicated_set"], "smoke")
        self.assertEqual(e["records_adjudicated"], N_SMOKE * 3)


class TestFisherExact(unittest.TestCase):

    def test_matches_known_values(self):
        # Fisher's classic tea-tasting table
        self.assertAlmostEqual(A.fisher_exact_two_sided(3, 1, 1, 3),
                               0.485714, places=5)
        self.assertAlmostEqual(A.fisher_exact_two_sided(4, 0, 0, 4),
                               0.028571, places=5)
        self.assertEqual(A.fisher_exact_two_sided(0, 0, 0, 0), None)

    def test_independent_table_is_near_one(self):
        self.assertGreater(A.fisher_exact_two_sided(50, 50, 50, 50), 0.9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
