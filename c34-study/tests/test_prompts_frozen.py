#!/usr/bin/env python3
"""C34 M2 tests — the treatment prompts are frozen, byte for byte.

The prompts ARE the treatment (registration correction v2 C-1, "THE M2
BLOCKER"). This suite does not compare the harness against a copy of the
strings kept in the test file — it compares it against the strings pinned in
the correction DOCUMENT itself, so drift in either the harness or the
registration is caught. The mutation tests prove a one-character change
fails.
"""
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
sys.path.insert(0, STUDY)
REPO = os.path.dirname(os.path.dirname(STUDY))
CORRECTION = os.path.join(
    REPO, "instruments", "2026-08-13-c34-registration-correction-v2.md")

import _env                        # noqa: E402
import generate_questions as G      # noqa: E402
import run_policies as P            # noqa: E402


def pinned_prompts():
    """Execute the fenced code blocks of correction v2 C-1 and return the
    prompt strings exactly as the registration pins them."""
    with open(CORRECTION) as fh:
        doc = fh.read()
    ns = {}
    for block in re.findall(r"\n```\n(.*?)\n```\n", doc, re.S):
        if "_PROMPT" in block or "COMMON" in block:
            exec(compile(block, CORRECTION, "exec"), ns)
    ns.pop("__builtins__", None)
    return ns


class TestPromptsByteVerbatim(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # the correction document and C29's harness are repository files
        _env.require_repo_file(
            "instruments/2026-08-13-c34-registration-correction-v2.md")
        cls.pinned = pinned_prompts()

    def test_all_five_prompts_are_pinned_in_the_correction(self):
        self.assertEqual(
            sorted(self.pinned),
            ["B_PROMPT", "COMMON", "C_PROMPT", "D_PROMPT", "Q_PROMPT",
             "S_PROMPT"])

    def test_generation_prompts_byte_identical(self):
        self.assertEqual(G.Q_PROMPT, self.pinned["Q_PROMPT"])
        self.assertEqual(G.S_PROMPT, self.pinned["S_PROMPT"])

    def test_policy_prompts_byte_identical(self):
        self.assertEqual(P.COMMON, self.pinned["COMMON"])
        self.assertEqual(P.B_PROMPT, self.pinned["B_PROMPT"])
        self.assertEqual(P.C_PROMPT, self.pinned["C_PROMPT"])
        self.assertEqual(P.D_PROMPT, self.pinned["D_PROMPT"])

    def test_dead_run_one_character_drift_fails(self):
        """The comparison must be a byte comparison, not a fuzzy one."""
        for name, live in (("Q_PROMPT", G.Q_PROMPT), ("S_PROMPT", G.S_PROMPT),
                           ("COMMON", P.COMMON), ("B_PROMPT", P.B_PROMPT),
                           ("C_PROMPT", P.C_PROMPT), ("D_PROMPT", P.D_PROMPT)):
            for drifted in (live[:-1], live + " ", live.replace(" ", "  ", 1),
                            live.replace("\n", " ", 1)):
                self.assertNotEqual(drifted, self.pinned[name],
                                    f"{name} drift undetected")

    def test_dead_run_em_dash_in_COMMON_is_not_a_hyphen(self):
        """COMMON's em dash is a real byte difference the answerer sees."""
        self.assertIn("—", P.COMMON)
        self.assertNotEqual(P.COMMON.replace("—", "-"),
                            self.pinned["COMMON"])

    def test_prompts_carry_the_verbatim_c29_source_they_claim(self):
        """The correction says these are byte-verbatim from C29's committed
        harness at cb73654. Check that claim against C29 directly, so the
        chain harness -> correction -> parent is closed."""
        c29 = os.path.join(REPO, "analyses", "c29-curation-vs-search-"
                           "sufficiency")
        ns = {}
        for fname in ("generate_questions.py", "run_policies.py"):
            with open(os.path.join(c29, fname)) as fh:
                src = fh.read()
            for m in re.finditer(
                    r"^((?:Q|S|B|C|D)_PROMPT|COMMON) = (\"\"\".*?\"\"\"|\(.*?\))"
                    r"$", src, re.S | re.M):
                exec(compile(m.group(0), fname, "exec"), ns)
        for name in ("Q_PROMPT", "S_PROMPT", "COMMON", "B_PROMPT", "C_PROMPT",
                     "D_PROMPT"):
            self.assertEqual(ns[name], self.pinned[name],
                             f"{name} is not byte-verbatim from C29")


class TestDeviationD1NoArmA(unittest.TestCase):
    """D-1: the flat-load arm is dropped. Not disabled — absent."""

    def test_no_A_PROMPT_anywhere_in_the_harness(self):
        self.assertFalse(hasattr(P, "A_PROMPT"))
        for name in sorted(os.listdir(STUDY)):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(STUDY, name)) as fh:
                src = fh.read()
            self.assertIsNone(re.search(r"^\s*A_PROMPT\s*=", src, re.M), name)
            self.assertNotIn("A_PROMPT.format", src, name)

    def test_policies_are_exactly_B_C_D(self):
        self.assertEqual(P.POLICIES, ("B", "C", "D"))
        self.assertEqual(P.AGENTIC, ("B", "C"))

    def test_no_flat_corpus_dump(self):
        with open(os.path.join(STUDY, "run_policies.py")) as fh:
            src = fh.read()
        self.assertNotIn("flat_dump", src)
        self.assertNotIn("FLAT_BUDGET_CHARS", src)

    def test_unregistered_policy_is_refused(self):
        with self.assertRaises(ValueError):
            P.build_prompt({"question": "q", "rp": "x.md"}, "A", "")


class TestGenerationInputRule(unittest.TestCase):
    """Correction v2 C-4: body[:8000] after frontmatter strip, verbatim from
    C29 for comparability with the parent."""

    def test_generation_input_chars_is_8000(self):
        self.assertEqual(G.GEN_INPUT_CHARS, 8000)

    def test_frontmatter_is_stripped_before_generation(self):
        import harness_lib as H
        text = "---\nsummary: a summary the generator must never see\n---\n\nbody line\n"
        fm, body = H.strip_frontmatter(text)
        self.assertIn("summary:", fm)
        self.assertNotIn("summary:", body)

    def test_salts_are_the_registered_ones(self):
        self.assertEqual(G.CONFIRMATORY_SALT, "c34-confirmatory-v1:")
        self.assertEqual(G.SMOKE_SALT, "c34-smoke-v1:")
        self.assertEqual((G.N_CONFIRMATORY, G.N_SMOKE), (120, 10))


if __name__ == "__main__":
    unittest.main(verbosity=2)
