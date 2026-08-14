#!/usr/bin/env python3
"""C34 M2 tests — rule R, its ledger, and its dead runs.

Offline: git plumbing over the pinned tree only. No provider, no network, no
Mentu CLI/MCP path.
"""
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import _env                      # noqa: E402
import corpus_rule as R          # noqa: E402

REPO = R.REPO
AUDIT_SRC = os.path.join(REPO, "paper", "agent-memory-allocation",
                         "sensitivity_audit.py")


class TestRuleRAtPinnedTree(unittest.TestCase):
    """The registered enumeration, recomputed rather than trusted."""

    @classmethod
    def setUpClass(cls):
        # rule R enumerates the git TREE at cb73654; the bundle ships none
        _env.require_repo_or_skip()
        cls.accepted, cls.ledger, cls.summary = R.enumerate_corpus()

    def test_precondition_141_files_1162998_bytes(self):
        # correction v2's post-exemption arithmetic; correction v3 G5 makes
        # this the verified precondition that replaces the dead <135 / >170
        # branches.
        self.assertEqual(self.summary["accepted_files"], 141)
        self.assertEqual(self.summary["accepted_bytes"], 1_162_998)
        R.assert_precondition(self.summary)          # must not raise

    def test_rejection_ledger_matches_registration(self):
        self.assertEqual(self.summary["rejected_by_clause"],
                         {"size": 3, "audit": 5, "selfref": 4,
                          "exemption": 1})

    def test_readme_is_the_named_exemption(self):
        ex = [e for e in self.ledger if e["rejected_by"] == "exemption"]
        self.assertEqual([e["path"] for e in ex], ["README.md"])
        # D-8 narrows the corpus by name, not by a content clause: README.md
        # matches no other rejecting clause, which is why `exemption` is
        # ordered last and the registered 3/5/4 arithmetic is unchanged.
        self.assertEqual(ex[0]["matching_clauses"], ["exemption"])

    def test_no_accepted_path_names_c29_or_c34(self):
        for a in self.accepted:
            self.assertNotIn("c29", a["path"].lower(), a["path"])
            self.assertNotIn("c34", a["path"].lower(), a["path"])

    def test_no_accepted_path_under_paper_or_analyses(self):
        for a in self.accepted:
            self.assertFalse(a["path"].startswith(("paper/", "analyses/")),
                             a["path"])

    def test_every_accepted_file_passes_the_audit_with_zero_flags(self):
        for a in self.accepted:
            raw = R.read_blobs([_blob_sha(a["path"])])[_blob_sha(a["path"])]
            self.assertFalse(R.audit(raw)["flag"], a["path"])

    def test_every_accepted_file_is_at_least_2000_bytes(self):
        self.assertTrue(all(a["size"] >= 2000 for a in self.accepted))

    def test_ledger_annotates_all_matching_clauses(self):
        """Correction v2 C-9: order-annotated, not order-dependent — the
        `rejected_by` bucket is the first match in the frozen order, and
        every match is listed."""
        for e in self.ledger:
            if e["rejected_by"] is None:
                self.assertEqual(e["matching_clauses"], [])
            else:
                self.assertIn(e["rejected_by"], e["matching_clauses"])
                first = next(c for c in R.CLAUSE_ORDER
                             if c in e["matching_clauses"])
                self.assertEqual(e["rejected_by"], first)

    def test_enumeration_is_deterministic(self):
        a2, l2, s2 = R.enumerate_corpus()
        self.assertEqual(s2, self.summary)
        self.assertEqual([e["path"] for e in l2],
                         [e["path"] for e in self.ledger])


def _blob_sha(path):
    for p, sha, _n in R.tree_entries():
        if p == path:
            return sha
    raise KeyError(path)


class TestAuditCopiedVerbatim(unittest.TestCase):
    """Rule R clause 5 must be self-contained in the public bundle, and it
    must be the SAME rule the withheld-corpus audit applies."""

    @classmethod
    def setUpClass(cls):
        # sensitivity_audit.py lives under paper/ and does not ship
        with open(_env.require_repo_file(
                "paper/agent-memory-allocation/sensitivity_audit.py")) as fh:
            cls.src = fh.read()

    def test_client_token_set_is_byte_identical(self):
        m = re.search(r"CLIENT_TOKENS = \[(.*?)\]", self.src, re.S)
        tokens = re.findall(r'"([^"]+)"', m.group(1))
        self.assertEqual(tokens, R.CLIENT_TOKENS)

    def test_spanish_regex_is_byte_identical(self):
        m = re.search(r"ES = re\.compile\((.*?), re\.I\)", self.src, re.S)
        literal = "".join(re.findall(r'r"([^"]*)"', m.group(1)))
        self.assertEqual(literal, R.ES.pattern)

    def test_density_threshold_is_20(self):
        self.assertIn("es_hits >= 20", self.src)
        self.assertFalse(R.audit(("está que para " * 6).encode())["flag"])
        self.assertTrue(R.audit(("está que para " * 7).encode())["flag"])


class TestDeadRuns(unittest.TestCase):
    """Phase-H rule 1: every gate ships a constructed total failure it must
    catch, in the same commit."""

    def test_dead_run_corpus_count_mismatch_fails_closed(self):
        """A corpus that is not the registered 141 files stops the study
        before any provider call (correction v3 G5)."""
        for bad in ({"accepted_files": 134, "accepted_bytes": 1_162_998,
                     "snapshot_commit": "0" * 40},
                    {"accepted_files": 171, "accepted_bytes": 1_162_998,
                     "snapshot_commit": "0" * 40},
                    {"accepted_files": 141, "accepted_bytes": 1_162_999,
                     "snapshot_commit": "0" * 40}):
            with self.assertRaises(SystemExit):
                R.assert_precondition(bad)

    def test_dead_run_audit_flagged_file_smuggled_in_is_rejected(self):
        """A file that would leak third-party content must be rejected by
        clause 5 even though it satisfies every other clause."""
        clean = b"# A clean methodology note\n" + b"filler line\n" * 300
        self.assertTrue(R.evaluate("docs/clean.md", len(clean),
                                   clean)["accepted"])
        if not R.CLIENT_TOKENS:
            # Public bundle: the token list is redacted (correction v5), so
            # there is no token to smuggle. Skip rather than pass vacuously —
            # a test that passes because it tested nothing is worse than one
            # that says it could not run. The Spanish-density half below is
            # not redacted and is exercised by its own dead run.
            self.skipTest("CLIENT_TOKENS redacted (correction v5); the token "
                          "half of clause 5 cannot be exercised in the bundle")
        for smuggled in (clean + b"\nThe REDACTED-CLIENT-IDENTIFIER engagement notes.\n",
                         clean + ("\nque para con los las una "
                                  "resultado semana " * 4).encode()):
            e = R.evaluate("docs/smuggled.md", len(smuggled), smuggled)
            self.assertFalse(e["accepted"])
            self.assertEqual(e["rejected_by"], "audit")

    def test_dead_run_self_referential_path_is_rejected(self):
        raw = b"# note\n" + b"filler\n" * 400
        for path in ("docs/about-c29-results.md",
                     "instruments/2026-08-13-c34-note.md"):
            e = R.evaluate(path, len(raw), raw)
            self.assertFalse(e["accepted"])
            self.assertEqual(e["rejected_by"], "selfref")

    def test_dead_run_undersized_file_is_rejected(self):
        raw = b"# tiny\n"
        e = R.evaluate("docs/tiny.md", len(raw), raw)
        self.assertFalse(e["accepted"])
        self.assertEqual(e["rejected_by"], "size")

    def test_clause_2_and_3_exclude_non_candidates(self):
        self.assertFalse(R.is_candidate("paper/agent-memory-allocation/x.md"))
        self.assertFalse(R.is_candidate("analyses/c29-x/DESIGN.md"))
        self.assertFalse(R.is_candidate("docs/notes.txt"))
        self.assertTrue(R.is_candidate("README.md"))
        self.assertTrue(R.is_candidate("essays/2026-01-01-x.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
