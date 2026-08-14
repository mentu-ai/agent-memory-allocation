#!/usr/bin/env python3
"""C34 M2 tests — the leak gate and its constructed leaks (finding G-M2-2).

The gate exists because of a real incident: two STOP markers written by tests
landed in the real study directory, where one would have sealed the real
adjudication `instrument-insufficient`. These tests construct that state and
prove the gate fails on it — including the case the first version of the gate
would have hidden, where the residue was already present before the suite ran.

Offline. The only subprocess used is `git`, on temporary repositories.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
sys.path.insert(0, STUDY)
sys.path.insert(0, HERE)

import _env                   # noqa: E402
import harness_lib as H        # noqa: E402
import run_tests as RT         # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args],
                          capture_output=True, text=True, check=True)


class TestGateOnConstructedLeaks(unittest.TestCase):
    """A temporary git repository standing in for the study directory."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        git(self.tmp, "init", "-q")
        git(self.tmp, "config", "user.email", "t@example.invalid")
        git(self.tmp, "config", "user.name", "t")
        with open(os.path.join(self.tmp, "harness.py"), "w") as fh:
            fh.write("# placeholder\n")
        git(self.tmp, "add", "harness.py")
        git(self.tmp, "commit", "-q", "-m", "init")

    def drop(self, name, body="{}"):
        path = os.path.join(self.tmp, name)
        with open(path, "w") as fh:
            fh.write(body)
        return path

    def commit(self, name):
        git(self.tmp, "add", name)
        git(self.tmp, "commit", "-q", "-m", f"add {name}")

    # -- the clean case ---------------------------------------------------
    def test_a_clean_directory_produces_no_findings(self):
        before = RT.live_artifacts(self.tmp)
        self.assertEqual(before, [])
        self.assertEqual(RT.leak_findings(self.tmp, before), [])

    # -- dead run 1: the suite creates a leak -----------------------------
    def test_dead_run_a_leak_created_during_the_suite_fails(self):
        before = RT.live_artifacts(self.tmp)
        self.drop("STOP-registered_budget_exhausted.json")
        findings = RT.leak_findings(self.tmp, before)
        conditions = [c for c, _ in findings]
        self.assertIn("created_by_suite", conditions)
        self.assertIn("STOP-registered_budget_exhausted.json",
                      dict(findings)["created_by_suite"])

    # -- dead run 2: THE INCIDENT STATE, residue already present ----------
    def test_dead_run_pre_existing_residue_fails_rather_than_hiding(self):
        """The exact M2 incident: a STOP marker already sitting in the study
        directory before the suite runs. A before/after diff alone would put
        it in `before` and report the run clean."""
        self.drop("STOP-pinned_answerer_unavailable.json")
        before = RT.live_artifacts(self.tmp)
        self.assertIn("STOP-pinned_answerer_unavailable.json", before)
        findings = RT.leak_findings(self.tmp, before)
        conditions = [c for c, _ in findings]
        self.assertNotIn("created_by_suite", conditions)   # it is not new
        self.assertIn("present_but_uncommitted", conditions)
        self.assertNotEqual(findings, [])

    # -- the discriminator: a committed milestone output is not a leak ----
    def test_a_committed_milestone_output_passes(self):
        self.drop("corpus-manifest.json", json.dumps({"entries": []}))
        self.commit("corpus-manifest.json")
        before = RT.live_artifacts(self.tmp)
        self.assertEqual(before, ["corpus-manifest.json"])
        self.assertEqual(RT.leak_findings(self.tmp, before), [])

    def test_a_committed_artifact_still_fails_if_the_suite_rewrites_it(self):
        self.drop("questions-2026-08-13.json")
        self.commit("questions-2026-08-13.json")
        before = [n for n in RT.live_artifacts(self.tmp)
                  if n != "questions-2026-08-13.json"]      # as if unseen
        conditions = [c for c, _ in RT.leak_findings(self.tmp, before)]
        self.assertIn("created_by_suite", conditions)

    def test_a_committed_snapshot_directory_passes(self):
        os.makedirs(os.path.join(self.tmp, "corpus-snapshot", "docs"))
        self.drop(os.path.join("corpus-snapshot", "docs", "a.md"), "# a\n")
        self.commit("corpus-snapshot")
        before = RT.live_artifacts(self.tmp)
        self.assertEqual(before, ["corpus-snapshot"])
        self.assertEqual(RT.leak_findings(self.tmp, before), [])

    def test_an_uncommitted_snapshot_directory_fails(self):
        os.makedirs(os.path.join(self.tmp, "corpus-snapshot", "docs"))
        self.drop(os.path.join("corpus-snapshot", "docs", "a.md"), "# a\n")
        before = RT.live_artifacts(self.tmp)
        conditions = [c for c, _ in RT.leak_findings(self.tmp, before)]
        self.assertIn("present_but_uncommitted", conditions)

    # -- every registered live artifact is watched ------------------------
    def test_the_watch_list_covers_every_live_artifact_the_study_writes(self):
        for name in ("runs", "gen-cache", "corpus-snapshot",
                     "call-ledger.jsonl", "call-ledger.jsonl.head.json",
                     "reality-probe.json", "corpus-manifest.json",
                     "rule-R-evaluation-log.json",
                     "questions-2026-08-13.json", "index-2026-08-13.json",
                     "selection-2026-08-13.json",
                     "effect-table-2026-08-13.json",
                     "smoke-audit-2026-08-13.json",
                     "STOP-registered_budget_exhausted.json"):
            with self.subTest(name=name):
                sub = tempfile.mkdtemp()
                self.addCleanup(shutil.rmtree, sub, True)
                with open(os.path.join(sub, name), "w") as fh:
                    fh.write("x")
                self.assertIn(name, RT.live_artifacts(sub))

    def test_a_leak_fails_the_run_even_when_every_test_passed(self):
        self.assertEqual(RT.exit_code(True, []), 0)
        self.assertEqual(
            RT.exit_code(True, [("present_but_uncommitted", ["STOP-x.json"])]),
            1)
        self.assertEqual(RT.exit_code(False, []), 1)


class TestGateOutsideAGitWorkTree(unittest.TestCase):
    """Finding G-M3-1: the public bundle ships without a git work tree. The
    gate's discriminator is git-tracked status, so outside a repo every
    artifact would read as uncommitted and a reader's `run_tests.py` would
    fail on a perfectly good bundle. The expected-artifact manifest is the
    fallback."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()          # NOT a git repository
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def drop(self, name, body="{}"):
        with open(os.path.join(self.tmp, name), "w") as fh:
            fh.write(body)

    def manifest(self, names):
        self.drop("expected-artifacts.json",
                  json.dumps({"artifacts": list(names)}))

    @_env.requires_repo
    def test_the_temp_dir_is_not_a_git_work_tree(self):
        self.assertFalse(RT.in_git_work_tree(self.tmp))
        self.assertTrue(RT.in_git_work_tree(STUDY))

    def test_dead_run_no_git_and_no_manifest_fails_closed(self):
        """Without either authority the gate must NOT wave artifacts through."""
        self.drop("corpus-manifest.json")
        self.assertIsNone(RT.expected_artifacts(self.tmp))
        conditions = [c for c, _ in RT.leak_findings(self.tmp, ["corpus-manifest.json"])]
        self.assertIn("present_but_uncommitted", conditions)

    def test_a_bundle_with_its_manifest_passes(self):
        for name in ("corpus-manifest.json", "questions-2026-08-13.json",
                     "effect-table-2026-08-14.json"):
            self.drop(name)
        os.makedirs(os.path.join(self.tmp, "corpus-snapshot"))
        self.drop(os.path.join("corpus-snapshot", "a.md"), "# a\n")
        names = RT.live_artifacts(self.tmp)
        self.manifest(names)
        self.assertEqual(RT.leak_findings(self.tmp, names), [])

    def test_an_artifact_absent_from_the_manifest_still_fails(self):
        """The fallback accounts for artifacts; it does not excuse them."""
        self.drop("corpus-manifest.json")
        self.drop("STOP-registered_budget_exhausted.json")
        self.manifest(["corpus-manifest.json"])       # STOP not named
        findings = dict(RT.leak_findings(self.tmp, RT.live_artifacts(self.tmp)))
        self.assertIn("present_but_uncommitted", findings)
        self.assertEqual(findings["present_but_uncommitted"],
                         ["STOP-registered_budget_exhausted.json"])

    def test_created_by_suite_still_fires_outside_a_repo(self):
        self.drop("corpus-manifest.json")
        self.manifest(["corpus-manifest.json", "STOP-x.json"])
        before = RT.live_artifacts(self.tmp)
        self.drop("STOP-x.json")                      # appears mid-suite
        conditions = [c for c, _ in RT.leak_findings(self.tmp, before)]
        self.assertIn("created_by_suite", conditions)
        self.assertNotIn("present_but_uncommitted", conditions)

    @_env.requires_repo
    def test_the_shipped_manifest_matches_what_git_tracks(self):
        """In-repo and out-of-repo must give the SAME answer, or the fallback
        would quietly ship a different rule than the one under test."""
        expected = RT.expected_artifacts(STUDY)
        self.assertIsNotNone(expected, "expected-artifacts.json must ship")
        present = set(RT.live_artifacts(STUDY))
        self.assertEqual(present, expected & present)
        for name in sorted(present):
            tracked = bool(subprocess.run(
                ["git", "-C", STUDY, "ls-files", "--", name],
                capture_output=True, text=True).stdout.strip())
            self.assertEqual(tracked, name in expected, name)


class TestGateOnTheRealStudyDirectory(unittest.TestCase):
    """The dead run that matters: construct the leak in the actual study
    directory the actual gate guards, and prove it fires."""

    def test_dead_run_a_stop_marker_here_fails_the_real_gate(self):
        name = "STOP-c34_leak_gate_dead_run.json"
        path = os.path.join(STUDY, name)
        self.assertFalse(os.path.exists(path), "dead-run residue from a "
                         "previous run — the gate should have caught it")
        before = RT.live_artifacts(STUDY)
        self.addCleanup(lambda: os.path.exists(path) and os.remove(path))
        with open(path, "w") as fh:
            json.dump({"reason": "dead_run"}, fh)
        findings = RT.leak_findings(STUDY, before)
        conditions = [c for c, _ in findings]
        self.assertIn("created_by_suite", conditions)
        self.assertIn("present_but_uncommitted", conditions)
        os.remove(path)
        self.assertEqual(RT.leak_findings(STUDY, before), [])


class TestWriteStopHasNoDefaultDirectory(unittest.TestCase):
    """Finding G-M2-2(c): the incident's cause was the default, not the call
    sites. The default is gone."""

    def test_here_is_a_required_argument(self):
        with self.assertRaises(TypeError):
            H.write_stop("registered_budget_exhausted", {})

    def test_write_stop_writes_where_it_is_told(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        path = H.write_stop("pinned_answerer_unavailable", {"x": 1}, tmp)
        self.assertEqual(os.path.dirname(path), tmp)
        self.assertEqual([m["reason"] for m in H.stop_markers(tmp)],
                         ["pinned_answerer_unavailable"])

    def test_the_module_directory_holds_no_stop_marker(self):
        self.assertEqual(H.stop_markers(STUDY), [])

    def test_no_caller_relies_on_a_default(self):
        import ast
        for name in sorted(os.listdir(STUDY)):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(STUDY, name)) as fh:
                tree = ast.parse(fh.read())
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                fn = node.func
                target = getattr(fn, "attr", getattr(fn, "id", None))
                if target == "write_stop":
                    self.assertTrue(
                        len(node.args) >= 3
                        or any(k.arg == "here" for k in node.keywords),
                        f"{name} calls write_stop without an explicit "
                        "directory")


class TestCorpusRuleWritesNothingWhenAskedNothing(unittest.TestCase):
    """Finding G-M2-3: a bare invocation must leave the directory untouched,
    so a verification pass can re-enumerate freely."""

    @_env.requires_repo
    def test_bare_invocation_leaves_the_directory_byte_unchanged(self):
        """Before M3 the evaluation log does not exist and must not appear;
        after M3 it exists as a committed artifact and must not be touched.
        Both are the same property: a bare invocation writes nothing."""
        import corpus_rule as R
        before = RT.live_artifacts(STUDY)
        existed = os.path.exists(R.EVAL_LOG)
        prior = open(R.EVAL_LOG, "rb").read() if existed else None
        proc = subprocess.run(
            [sys.executable, os.path.join(STUDY, "corpus_rule.py")],
            capture_output=True, text=True, cwd=STUDY)
        self.assertEqual(proc.returncode, 0, proc.stderr[-500:])
        self.assertIn('"accepted_files": 141', proc.stdout)
        self.assertNotIn("evaluation log ->", proc.stdout)
        self.assertNotIn("snapshot:", proc.stdout)
        if existed:
            self.assertEqual(open(R.EVAL_LOG, "rb").read(), prior)
        else:
            self.assertFalse(os.path.exists(R.EVAL_LOG))
        self.assertEqual(RT.leak_findings(STUDY, before), [])

    @_env.requires_repo
    def test_the_committed_snapshot_is_not_disturbed_by_a_bare_invocation(self):
        """The M3 artifacts are committed; re-enumerating must not rewrite
        them, so a verifier can run rule R as often as they like."""
        man = os.path.join(STUDY, "corpus-manifest.json")
        if not os.path.exists(man):
            self.skipTest("pre-M3: no snapshot committed yet")
        prior = open(man, "rb").read()
        subprocess.run([sys.executable,
                        os.path.join(STUDY, "corpus_rule.py")],
                       capture_output=True, text=True, cwd=STUDY, check=True)
        self.assertEqual(open(man, "rb").read(), prior)
        dirty = subprocess.run(
            ["git", "-C", STUDY, "status", "--porcelain", "--",
             "corpus-snapshot", "corpus-manifest.json",
             "rule-R-evaluation-log.json"],
            capture_output=True, text=True).stdout.strip()
        self.assertEqual(dirty, "",
                         f"re-enumeration dirtied the M3 artifacts: {dirty}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
