#!/usr/bin/env python3
"""C34 M2 tests — question generation, selection, and the index pass.

Offline: no provider is contacted. The generator-facing functions are tested
on synthetic snapshot bytes.
"""
import hashlib
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import build_index as B        # noqa: E402
import fixtures as F           # noqa: E402
import generate_questions as G  # noqa: E402
import harness_lib as H        # noqa: E402


class TestGenerationExposure(unittest.TestCase):
    """Registration §2 / C29 D3: the generator receives frontmatter-stripped
    bodies only, by the committed mechanical strip, so "generation did not use
    the summary layers" is provable by construction."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        _man, self.snap, _e = F.make_corpus(self.tmp, 3)

    def test_generator_never_sees_the_frontmatter_digest(self):
        body, sent, _sha = G.gen_input("docs/doc001.md", self.snap)
        self.assertNotIn("summary:", body)
        self.assertNotIn("summary:", sent)
        self.assertIn("alpha-001-omega", body)

    def test_generation_input_hash_is_over_the_exact_bytes_sent(self):
        _body, sent, sha = G.gen_input("docs/doc002.md", self.snap)
        self.assertEqual(
            sha, hashlib.sha256(sent.encode("utf-8")).hexdigest())

    def test_input_is_truncated_at_8000_chars(self):
        rp = "docs/big.md"
        dest = os.path.join(self.snap, rp)
        with open(dest, "w") as fh:
            fh.write("---\nsummary: x\n---\n\n" + ("filler line\n" * 2000))
        _body, sent, _sha = G.gen_input(rp, self.snap)
        self.assertEqual(len(sent), G.GEN_INPUT_CHARS)

    def test_validation_drops_answers_absent_from_the_body(self):
        body, _sent, _sha = G.gen_input("docs/doc001.md", self.snap)
        self.assertIsNone(G.validate({"answer": "alpha-001-omega"}, body))
        self.assertEqual(G.validate({"answer": "not in the body"}, body),
                         "answer_not_in_body")
        self.assertEqual(G.validate({"answer": ""}, body), "empty_answer")

    def test_validation_is_whitespace_normalized_containment(self):
        body, _s, _h = G.gen_input("docs/doc001.md", self.snap)
        self.assertIsNone(G.validate({"answer": "ALPHA-001-OMEGA"}, body))
        self.assertIsNone(G.validate(
            {"answer": "registered  marker\nfor document 001"}, body))


class TestSelection(unittest.TestCase):
    """The frozen salts and the frozen shortfall rule (registration §2)."""

    def ids(self, n):
        return [f"q{i:03d}" for i in range(1, n + 1)]

    def test_full_branch_draws_120_and_10(self):
        conf, smoke, branch = G.select(self.ids(141))
        self.assertEqual((len(conf), len(smoke), branch), (120, 10, "full"))
        self.assertFalse(set(conf) & set(smoke))

    def test_shortfall_branch_keeps_10_smoke_and_reports_its_number(self):
        for n in (115, 120, 129):
            conf, smoke, branch = G.select(self.ids(n))
            self.assertEqual(branch, "shortfall")
            self.assertEqual(len(smoke), 10)
            self.assertEqual(len(conf), n - 10)
            self.assertGreaterEqual(len(conf), 105)

    def test_boundary_at_130_takes_the_full_branch(self):
        self.assertEqual(G.select(self.ids(130))[2], "full")
        self.assertEqual(G.select(self.ids(129))[2], "shortfall")

    def test_below_115_stops_before_any_policy_run(self):
        with self.assertRaises(SystemExit) as cm:
            G.select(self.ids(114))
        self.assertIn("question_yield_shortfall", str(cm.exception))

    def test_selection_is_reproducible_from_the_frozen_salts(self):
        a = G.select(self.ids(141))
        b = G.select(self.ids(141))
        self.assertEqual(a, b)
        self.assertEqual(
            G.salted_order(self.ids(20), G.CONFIRMATORY_SALT)[:3],
            sorted(self.ids(20),
                   key=lambda i: hashlib.sha256(
                       (G.CONFIRMATORY_SALT + i).encode()).hexdigest())[:3])

    def test_the_two_salts_select_differently(self):
        ids = self.ids(141)
        self.assertNotEqual(G.salted_order(ids, G.CONFIRMATORY_SALT),
                            G.salted_order(ids, G.SMOKE_SALT))

    def test_selection_never_depends_on_an_outcome(self):
        """Salted selection is a pure function of the question ids."""
        import inspect
        src = inspect.getsource(G.select) + inspect.getsource(G.salted_order)
        for token in ("answer", "accuracy", "correct", "score", "token"):
            self.assertNotIn(token, src)


class TestRegenerationOrder(unittest.TestCase):
    """Correction v2 C-7."""

    def results(self, failed_ids, n=20):
        return [{"id": f"q{i:03d}",
                 **({"fail": "answer_not_in_body"}
                    if f"q{i:03d}" in set(failed_ids)
                    else {"question": "q"})}
                for i in range(1, n + 1)]

    def test_ascending_question_id(self):
        to_regen, left = G.regeneration_plan(
            self.results(["q009", "q002", "q015"]), remaining=45)
        self.assertEqual(to_regen, ["q002", "q009", "q015"])
        self.assertEqual(left, [])

    def test_sub_ceiling_binds_and_the_remainder_is_recorded_as_dropped(self):
        to_regen, left = G.regeneration_plan(
            self.results([f"q{i:03d}" for i in range(1, 11)]), remaining=4)
        self.assertEqual(to_regen, ["q001", "q002", "q003", "q004"])
        self.assertEqual(left, ["q005", "q006", "q007", "q008", "q009",
                                "q010"])

    def test_exhausted_sub_ceiling_regenerates_nothing(self):
        to_regen, left = G.regeneration_plan(self.results(["q003"]),
                                             remaining=0)
        self.assertEqual(to_regen, [])
        self.assertEqual(left, ["q003"])

    def test_regeneration_sub_ceiling_is_45(self):
        self.assertEqual(H.SUB_CEILINGS["regeneration"], 45)


class TestIndexPass(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        _man, self.snap, _e = F.make_corpus(self.tmp, 3)

    def test_mechanical_digest_extraction_from_frontmatter(self):
        fm, _body = H.strip_frontmatter(
            H.read_snapshot("docs/doc001.md", self.snap))
        self.assertEqual(H.digest_from_frontmatter(fm),
                         "synthetic corpus document 001")

    def test_index_line_format_matches_the_frozen_C_prompt_block(self):
        index = {"docs/b.md": {"digest": "second"},
                 "docs/a.md": {"digest": "first"}}
        self.assertEqual(B.index_text(index),
                         "docs/a.md — first\ndocs/b.md — second")

    def test_digest_authoring_uses_6000_chars(self):
        self.assertEqual(B.DIGEST_INPUT_CHARS, 6000)

    def test_digest_authoring_is_a_separate_pass_from_question_generation(self):
        """Registration exposure rule 2: the generator never sees the digest
        index alongside a question it authored for the same file."""
        with open(os.path.join(os.path.dirname(HERE),
                               "generate_questions.py")) as fh:
            gen_src = fh.read()
        self.assertNotIn("S_PROMPT.format", gen_src)
        self.assertNotIn('"digest"', gen_src)
        with open(os.path.join(os.path.dirname(HERE), "build_index.py")) as fh:
            idx_src = fh.read()
        self.assertNotIn("Q_PROMPT", idx_src)


if __name__ == "__main__":
    unittest.main(verbosity=2)
