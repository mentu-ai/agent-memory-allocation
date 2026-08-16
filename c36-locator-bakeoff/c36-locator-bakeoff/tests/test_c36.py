"""c36 freeze tests — everything verifiable without a provider call.

Run: cd analyses/c36-locator-bakeoff && python3 -m pytest tests/ -q
 (or python3 tests/test_c36.py)
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

import c36lib                                   # noqa: E402
from scoring import contains_boundary, contains_c34, score   # noqa: E402
from generate_questions_c36 import gate_check, salted_order, word_count  # noqa: E402


class TestFreeze(unittest.TestCase):
    def test_c34_pins_hold(self):
        c36lib.verify_c34_pins()  # raises on drift

    def test_navigator_commit_pinned(self):
        c36lib.assert_navigator_commit()  # raises on drift

    def test_sandbox_setup_verifies_every_hash(self):
        corpus_dir = c36lib.setup_sandbox(fresh=False)
        self.assertTrue(os.path.isdir(corpus_dir))
        manifest = c36lib.load_manifest()
        self.assertEqual(manifest["files"], 141)


class TestScoring(unittest.TestCase):
    def test_q073_class_closed_by_boundary_rule(self):
        # C34 defect N5: gold hash inside a longer hash scored correct.
        self.assertTrue(contains_c34("commit 0b320d9d3d66 fixed it", "0b320d9d"))
        self.assertFalse(contains_boundary("commit 0b320d9d3d66 fixed it", "0b320d9d"))

    def test_boundary_rule_accepts_true_containment(self):
        self.assertTrue(contains_boundary("It ends with the Codex trailer.", "the Codex trailer"))
        self.assertTrue(contains_boundary("La respuesta: el registro semanal.", "el registro semanal"))

    def test_normalization_matches_c34_semantics(self):
        self.assertTrue(contains_c34("THE  CODEX\ntrailer", "the codex trailer"))
        self.assertTrue(contains_boundary("THE  CODEX\ntrailer", "the codex trailer"))

    def test_score_reports_both_rules(self):
        self.assertEqual(score("x 0b320d9d3d66", "0b320d9d"), {"boundary": False, "c34": True})


class TestGates(unittest.TestCase):
    BODY = "The retention window folds segments older than one quarter into the archive."

    def _cand(self, q, a):
        return {"question": q, "answer": a, "qtype": "lookup"}

    def test_accepts_compliant_candidate(self):
        ok, failed = gate_check(
            self._cand("What happens to old segments?", "folds segments older than one quarter"),
            self.BODY, {"doc.md": self.BODY.lower()})
        self.assertTrue(ok, failed)

    def test_length_gate_is_counted_not_instructed(self):
        ok, failed = gate_check(self._cand("How many?", "one quarter"), self.BODY, {})
        self.assertIn("length", failed)          # 2 words < 3
        long_gold = " ".join(["word"] * 16)
        ok, failed = gate_check(self._cand("?", long_gold), long_gold, {})
        self.assertIn("length", failed)          # 16 words > 15

    def test_verbatim_gate(self):
        ok, failed = gate_check(self._cand("?", "not in the body at all"), self.BODY, {})
        self.assertIn("verbatim", failed)

    def test_failable_in_question_gate(self):
        ok, failed = gate_check(
            self._cand("Does it fold segments older than one quarter?",
                       "fold segments older than one quarter"),
            "It will fold segments older than one quarter into the archive.", {})
        self.assertIn("failable-in-question", failed)

    def test_failable_multidoc_gate(self):
        gold = "folds segments older than one quarter"
        bodies = {f"d{i}.md": f"text {gold.lower()} text" for i in range(3)}
        ok, failed = gate_check(self._cand("?", gold), self.BODY, bodies)
        self.assertIn("failable-multidoc", failed)

    def test_non_degenerate_gate(self):
        ok, failed = gate_check(self._cand("?", "19 44 07"), "x 19 44 07 y", {})
        self.assertIn("non-degenerate", failed)  # C34 defect: unfailable numerics

    def test_word_count(self):
        self.assertEqual(word_count("the Codex trailer"), 3)


class TestSplit(unittest.TestCase):
    def test_salted_order_deterministic(self):
        ids = [f"q{i:03d}" for i in range(1, 142)]
        a = salted_order(ids, "c36-confirmatory-v1:")
        b = salted_order(list(reversed(ids)), "c36-confirmatory-v1:")
        self.assertEqual(a, b)
        self.assertNotEqual(a, salted_order(ids, "c34-confirmatory-v1:"))


class TestArms(unittest.TestCase):
    def test_fts5_adapter_contract(self):
        from fts5_adapter import locate_fts5
        corpus_dir = c36lib.setup_sandbox(fresh=False)
        envelope = locate_fts5(corpus_dir, "observatory beat packet", k=8)
        self.assertLessEqual(len(envelope["hits"]), 8)
        self.assertEqual(envelope["strategy"], "sqlite-fts5-porter-unicode61")
        for hit in envelope["hits"]:
            self.assertTrue(hit["path"].endswith(".md"))

    def test_navigator_arms_smoke(self):
        corpus_dir = c36lib.setup_sandbox(fresh=False)
        for arm in ("L0", "L1", "L2"):
            envelope = c36lib.locate(corpus_dir, "observatory beat packet", arm)
            self.assertLessEqual(len(envelope["hits"]), c36lib.K, arm)
            self.assertEqual(envelope["request"]["k"], c36lib.K, arm)

    def test_read_only_after_arms(self):
        import subprocess
        out = subprocess.run(["git", "-C", c36lib.EPISTEMICS, "status", "--porcelain",
                              "analyses/c34-public-curation-vs-search-replication/corpus-snapshot"],
                             capture_output=True, text=True)
        self.assertEqual(out.stdout.strip(), "", "the frozen snapshot must never change")


if __name__ == "__main__":
    unittest.main(verbosity=1)
