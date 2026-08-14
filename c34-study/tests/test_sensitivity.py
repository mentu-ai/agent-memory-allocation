#!/usr/bin/env python3
"""C34 tests — correction v4's annotations and the non-adjudicating
sensitivity rows, with their dead runs.

Offline. One class reads the REAL committed question set, index and snapshot,
which is what makes correction v4's enumeration a commitment rather than a
comment.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
sys.path.insert(0, STUDY)
sys.path.insert(0, HERE)

import adjudicate as A         # noqa: E402
import fixtures as F           # noqa: E402
import harness_lib as H        # noqa: E402
from test_adjudicate import NO_FLAGS, SMOKE_PLAN, N_CONF, N_SMOKE  # noqa: E402


def q(qid, rp, answer):
    return {"id": qid, "rp": rp, "answer": answer, "qtype": "lookup",
            "set": "confirmatory"}


class TestAnnotationConditions(unittest.TestCase):
    """Each condition of v4 H1-H3, on constructed inputs."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.snap = os.path.join(self.tmp, "corpus-snapshot")
        os.makedirs(os.path.join(self.snap, "docs"))

    def write(self, rp, body):
        path = os.path.join(self.snap, rp)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(body)

    def test_F3_length_floor(self):
        self.write("docs/a.md", "# t\n\nthe value is 0 here\n")
        ann = A.compute_annotations([q("q001", "docs/a.md", "0")], self.snap,
                                    {}, ["docs/a.md"])
        self.assertEqual(ann["scoring_degenerate"]["q001"],
                         ["F3_length_floor"])

    def test_F2_cross_answer_collision_including_equality(self):
        self.write("docs/a.md", "# t\n\nalpha beta gamma delta\n")
        self.write("docs/b.md", "# t\n\nalpha beta gamma delta epsilon\n")
        qs = [q("q001", "docs/a.md", "alpha beta"),
              q("q002", "docs/b.md", "alpha beta gamma")]
        ann = A.compute_annotations(qs, self.snap, {}, ["docs/a.md", "docs/b.md"])
        self.assertEqual(ann["scoring_degenerate"]["q001"],
                         ["F2_cross_answer_collision"])
        self.assertNotIn("q002", ann["scoring_degenerate"])
        # equality collides in both directions
        qs2 = [q("q001", "docs/a.md", "alpha beta"),
               q("q002", "docs/b.md", "alpha beta")]
        ann2 = A.compute_annotations(qs2, self.snap, {}, ["docs/a.md", "docs/b.md"])
        self.assertEqual(sorted(ann2["scoring_degenerate"]), ["q001", "q002"])

    def test_F1_corpus_ubiquity_threshold(self):
        for i in range(A.F1_UBIQUITY_MIN):
            self.write(f"docs/f{i:03d}.md", "# t\n\nthe ubiquitous phrase\n")
        paths = [f"docs/f{i:03d}.md" for i in range(A.F1_UBIQUITY_MIN)]
        qs = [q("q001", "docs/f000.md", "the ubiquitous phrase")]
        ann = A.compute_annotations(qs, self.snap, {}, paths)
        self.assertIn("F1_corpus_ubiquity", ann["scoring_degenerate"]["q001"])
        # one file short of the threshold does not trip it
        ann = A.compute_annotations(qs, self.snap, {}, paths[:-1])
        self.assertNotIn("q001", ann["scoring_degenerate"])

    def test_F1_denominator_is_the_corpus_not_the_question_set(self):
        """The confirmatory set covers 120 of the 141 files, so deriving the
        denominator from the questions would measure the wrong population."""
        for i in range(A.F1_UBIQUITY_MIN):
            self.write(f"docs/f{i:03d}.md", "# t\n\nthe ubiquitous phrase\n")
        qs = [q("q001", "docs/f000.md", "the ubiquitous phrase")]
        corpus = [f"docs/f{i:03d}.md" for i in range(A.F1_UBIQUITY_MIN)]
        self.assertIn("q001",
                      A.compute_annotations(qs, self.snap, {}, corpus)
                      ["scoring_degenerate"])
        # the same question judged against only its own file: not ubiquitous
        self.assertNotIn("q001",
                         A.compute_annotations(qs, self.snap, {}, ["docs/f000.md"])
                         ["scoring_degenerate"])

    def test_index_leak(self):
        self.write("docs/a.md", "# t\n\nthe purge deleted 233,918 rows\n")
        qs = [q("q001", "docs/a.md", "233,918")]
        clean = A.compute_annotations(
            qs, self.snap, {"docs/a.md": {"digest": "a regime note"}},
            ["docs/a.md"])
        self.assertEqual(clean["index_leak"], {})
        leaked = A.compute_annotations(
            qs, self.snap,
            {"docs/a.md": {"digest": "regime note: purge of 233,918 rows"}},
            ["docs/a.md"])
        self.assertEqual(leaked["index_leak"]["q001"],
                         ["own_digest_contains_gold"])

    def test_outside_generation_slice(self):
        body = "# t\n\n" + ("filler line\n" * 1200) + "the late marker\n"
        self.write("docs/a.md", body)
        ann = A.compute_annotations([q("q001", "docs/a.md",
                                       "the late marker")], self.snap, {},
                                    ["docs/a.md"])
        self.assertEqual(ann["outside_generation_slice"]["q001"],
                         ["gold_beyond_generation_slice"])
        ann2 = A.compute_annotations([q("q001", "docs/a.md", "filler line")],
                                     self.snap, {}, ["docs/a.md"])
        self.assertEqual(ann2["outside_generation_slice"], {})

    def test_annotations_are_independent_of_each_other(self):
        """A question can carry more than one, and each is reported."""
        self.write("docs/a.md", "# t\n\nvalue 0 appears\n")
        ann = A.compute_annotations([q("q001", "docs/a.md", "0")], self.snap,
                                    {"docs/a.md": {"digest": "0 rows"}},
                                    ["docs/a.md"])
        self.assertIn("q001", ann["scoring_degenerate"])
        self.assertIn("q001", ann["index_leak"])


class TestDeadRunFlagEnumerationMismatch(unittest.TestCase):
    """Dead run 1: the enumeration is a commitment. A drift must raise a
    NAMED exception, and the test asserts the type — not merely that
    something went wrong."""

    def build(self, expected_flags):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        man, snap, entries = F.make_corpus(tmp, N_CONF + N_SMOKE)
        qf, questions = F.make_questions(tmp, N_CONF, N_SMOKE, snap)
        idx = F.make_index(tmp, questions)
        runs = F.make_runs(tmp, questions, F.plan_supported())
        return A.adjudicate(runs, qf, idx, man, snap, tmp,
                            expect_files=len(entries),
                            expected_flags=expected_flags)

    def test_named_exception_type(self):
        with self.assertRaises(A.FlagEnumerationMismatch):
            self.build({"scoring_degenerate": ("q001",), "index_leak": (),
                        "outside_generation_slice": ()})

    def test_it_is_not_merely_some_runtime_error(self):
        try:
            self.build({"scoring_degenerate": ("q001",), "index_leak": (),
                        "outside_generation_slice": ()})
        except A.FlagEnumerationMismatch as exc:
            self.assertIn("scoring_degenerate", str(exc))
            self.assertIn("enumerated-only", str(exc))
        else:
            self.fail("no mismatch raised")

    def test_it_raises_in_both_directions(self):
        """Computed-only drift must raise too, not just enumerated-only."""
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        _man, snap, _e = F.make_corpus(tmp, 3)
        qs = [q("q001", "docs/doc001.md", "0")]        # trips F3
        ann = A.compute_annotations(qs, snap, {}, ["docs/doc001.md"])
        with self.assertRaises(A.FlagEnumerationMismatch) as cm:
            A.verify_flag_enumerations(ann, {"scoring_degenerate": (),
                                             "index_leak": (),
                                             "outside_generation_slice": ()})
        self.assertIn("computed-only", str(cm.exception))

    def test_a_correct_enumeration_does_not_raise(self):
        e = self.build(NO_FLAGS)
        self.assertEqual(e["verdict"], "supported")


class TestDeadRunDisagreeingSensitivityRow(unittest.TestCase):
    """Dead run 2: a sensitivity row that disagrees with the primary result
    must be REPORTED as a finding and must change no verdict."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        man, snap, entries = F.make_corpus(self.tmp, N_CONF + N_SMOKE)
        qf, questions = F.make_questions(self.tmp, N_CONF, N_SMOKE, snap)
        idx = F.make_index(self.tmp, questions)
        runs = F.make_runs(self.tmp, questions, {
            "B": dict(n_located=94, n_correct=55,
                      n_correct_among_nonlocated=2, tot=130_000, marg=22_000),
            "C": dict(n_located=58, n_correct=60,
                      n_correct_among_nonlocated=6, tot=90_000, marg=15_000),
            "D": dict(n_correct=104, tot=25_000, marg=3_000)})
        F.make_runs(self.tmp, questions, SMOKE_PLAN, which_set="smoke")
        # Make two golds degenerate (2 chars -> F3, and identical -> F2) and
        # let ONLY B get them right, so removing them moves B's accuracy and
        # not C's. The gold is "fi" — from "filler", present in every fixture
        # body — which trips F1+F2+F3 exactly as the real q014/q023/q037 do,
        # and nothing else. Two likelier choices were rejected because the
        # gate correctly fires on them. They are true positives, not false
        # ones, but each adds a second annotation and would confound the
        # single effect this dead run exists to show:
        #   "0"  also trips index_leak — the fixture's own digests embed the
        #        file number ("digest for docs/doc001.md");
        #   "zz" also trips outside_generation_slice — it appears in no
        #        fixture body, so it cannot be inside the generator's
        #        8,000-character slice.
        with open(qf) as fh:
            qd = json.load(fh)
        for entry in qd["questions"]:
            if entry["id"] in ("q001", "q002"):
                entry["answer"] = "fi"
        with open(qf, "w") as fh:
            json.dump(qd, fh, indent=1, sort_keys=True)
        for qid in ("q001", "q002"):
            for policy, ans in (("B", "fi"), ("C", "qqq"), ("D", "fi")):
                p = os.path.join(runs, f"{qid}_{policy}.json")
                with open(p) as fh:
                    rec = json.load(fh)
                rec["answer"] = ans
                with open(p, "w") as fh:
                    json.dump(rec, fh, indent=1, sort_keys=True)
        self.effect = A.adjudicate(
            runs, qf, idx, man, snap, self.tmp, expect_files=len(entries),
            expected_flags={"scoring_degenerate": ("q001", "q002"),
                            "index_leak": (), "outside_generation_slice": ()})

    def row(self, label):
        return next(r for r in self.effect["non_adjudicating"]
                    ["sensitivity_rows"] if r["label"] == label)

    def test_the_degenerate_pair_is_annotated(self):
        ann = self.effect["non_adjudicating"]["question_set_annotations"]
        self.assertEqual(ann["scoring_degenerate"]["qids"], ["q001", "q002"])
        self.assertEqual(ann["scoring_degenerate"]["n"], 2)

    def test_the_row_disagrees_and_says_so(self):
        r = self.row("excluding_scoring_degenerate")
        self.assertTrue(r["disagrees_with_primary"])
        self.assertTrue(r["predictions_flipped"])
        self.assertEqual(r["denominator"], N_CONF - 2)
        self.assertEqual(r["excluded_qids"], ["q001", "q002"])

    def test_the_disagreement_changes_no_verdict(self):
        r = self.row("excluding_scoring_degenerate")
        self.assertIn("P1", r["predictions_flipped"])
        self.assertTrue(r["predictions_primary"]["P1"])
        self.assertFalse(r["predictions"]["P1"])
        # the verdict is the PRIMARY computation, untouched by the row
        self.assertTrue(self.effect["predictions"]["P1_accuracy_parity"])
        self.assertNotIn("P1", self.effect["failed_predictions"])
        self.assertTrue(self.effect["headline"]["P1_accuracy_parity"]["pass"])

    def test_the_row_is_labelled_non_adjudicating(self):
        for r in self.effect["non_adjudicating"]["sensitivity_rows"]:
            self.assertFalse(r["adjudicating"])
            self.assertIn("never a tiebreak", r["note"])

    def test_both_rows_are_present_with_denominators_and_deltas(self):
        labels = [r["label"] for r in
                  self.effect["non_adjudicating"]["sensitivity_rows"]]
        self.assertEqual(labels, ["excluding_scoring_degenerate",
                                  "excluding_index_leak"])
        for r in self.effect["non_adjudicating"]["sensitivity_rows"]:
            self.assertIn("denominator", r)
            self.assertIn("accuracy_delta_vs_primary", r)
            self.assertIn("scored_per_policy", r)

    def test_index_leak_row_excludes_nothing_here_and_agrees(self):
        r = self.row("excluding_index_leak")
        self.assertEqual(r["excluded_qids"], [])
        self.assertEqual(r["denominator"], N_CONF)
        self.assertFalse(r["disagrees_with_primary"])

    def test_outside_generation_slice_excludes_nothing(self):
        """v4 H3: it is a provenance annotation, never a sensitivity row."""
        labels = [r["label"] for r in
                  self.effect["non_adjudicating"]["sensitivity_rows"]]
        self.assertNotIn("excluding_outside_generation_slice", labels)

    def test_still_byte_deterministic_with_sensitivity_rows(self):
        blob = json.dumps(self.effect, indent=1, sort_keys=True)
        again = A.adjudicate(
            os.path.join(self.tmp, "runs"),
            os.path.join(self.tmp, "questions-2026-08-13.json"),
            os.path.join(self.tmp, "index-2026-08-13.json"),
            os.path.join(self.tmp, "corpus-manifest.json"),
            os.path.join(self.tmp, "corpus-snapshot"), self.tmp,
            expect_files=N_CONF + N_SMOKE,
            expected_flags={"scoring_degenerate": ("q001", "q002"),
                            "index_leak": (), "outside_generation_slice": ()})
        self.assertEqual(blob, json.dumps(again, indent=1, sort_keys=True))


class TestAgainstTheRealCommittedArtifacts(unittest.TestCase):
    """Dead run 3, and the one that makes v4's enumeration binding: the
    annotation sets recomputed from the COMMITTED question set, index and
    snapshot must equal what correction v4 enumerates."""

    @classmethod
    def setUpClass(cls):
        qp = os.path.join(STUDY, "questions-2026-08-13.json")
        ip = os.path.join(STUDY, "index-2026-08-13.json")
        if not (os.path.exists(qp) and os.path.exists(ip)):
            raise unittest.SkipTest("pre-M4: no frozen question set yet")
        with open(qp) as fh:
            cls.conf = [q for q in json.load(fh)["questions"]
                        if q["set"] == "confirmatory"]
        with open(ip) as fh:
            cls.index = json.load(fh)["index"]
        with open(os.path.join(STUDY, "corpus-manifest.json")) as fh:
            paths = sorted(e["path"] for e in json.load(fh)["entries"])
        cls.ann = A.compute_annotations(
            cls.conf, os.path.join(STUDY, "corpus-snapshot"), cls.index, paths)

    def test_scoring_degenerate_matches_correction_v4(self):
        self.assertEqual(sorted(self.ann["scoring_degenerate"]),
                         sorted(A.FLAGS_SCORING_DEGENERATE))

    def test_index_leak_matches_correction_v4(self):
        self.assertEqual(sorted(self.ann["index_leak"]),
                         sorted(A.FLAGS_INDEX_LEAK))

    def test_outside_generation_slice_matches_correction_v4(self):
        self.assertEqual(sorted(self.ann["outside_generation_slice"]),
                         sorted(A.FLAGS_OUTSIDE_GENERATION_SLICE))

    def test_the_default_verification_passes_on_the_real_artifacts(self):
        A.verify_flag_enumerations(self.ann)      # must not raise

    def test_the_three_starkest_trip_all_three_conditions(self):
        for qid in ("q014", "q023", "q037"):
            self.assertEqual(
                self.ann["scoring_degenerate"][qid],
                ["F1_corpus_ubiquity", "F2_cross_answer_collision",
                 "F3_length_floor"], qid)

    def test_the_remainder_trip_collision_only(self):
        for qid in ("q058", "q076", "q077", "q129", "q138"):
            self.assertEqual(self.ann["scoring_degenerate"][qid],
                             ["F2_cross_answer_collision"], qid)

    def test_sensitivity_denominators_are_the_registered_112_and_117(self):
        self.assertEqual(120 - len(self.ann["scoring_degenerate"]), 112)
        self.assertEqual(120 - len(self.ann["index_leak"]), 117)
        self.assertGreaterEqual(112, A.SCORED_FLOOR)
        self.assertGreaterEqual(117, A.SCORED_FLOOR)

    def test_only_q014_carries_two_annotations(self):
        both = set(self.ann["scoring_degenerate"]) & set(self.ann["index_leak"])
        self.assertEqual(both, {"q014"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
