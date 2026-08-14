#!/usr/bin/env python3
"""C34 — the whole offline M2 test suite in one command, plus the leak gate.

No provider, no network, no Mentu path. Every gate in this study ships its
dead run here, in the same commit as the gate (Phase-H rule 1).

## The leak gate

A test that writes a live-run artifact into the study directory has escaped
its fixture. This happened once during M2: two `STOP-*.json` markers written
by tests landed here, and a stray STOP marker would have sealed the real
adjudication `instrument-insufficient`.

The gate fires on two distinct conditions, because the incident state is the
second one and a before/after diff alone would hide it:

  * `created_by_suite` — the artifact was not present before the suite ran.
    Always a leak, even if a committed artifact of the same name exists: the
    suite mutating a milestone output is worse, not better.
  * `present_but_uncommitted` — the artifact is here now and git does not
    track it. This is the discriminator that separates a registered milestone
    output from residue. `corpus-snapshot/` after M3 is committed and passes;
    a STOP marker a test dropped is untracked and fails, whether it appeared
    during this run or was already lying here from a previous one.

Consequence for milestone work: produce the artifact, COMMIT it, then re-run
the suite. A green suite over uncommitted live-run state is exactly the
reading this gate refuses to give.

Usage: python3 run_tests.py
"""
import glob
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SUITES = ("test_corpus_rule", "test_prompts_frozen", "test_harness_lib",
          "test_generation", "test_adjudicate", "test_audit_smoke",
          "test_run_policies", "test_leak_gate", "test_sensitivity")

# Every artifact a live run produces. Names and globs, relative to the study
# directory. Registered milestone outputs are in here deliberately — the gate
# distinguishes them by whether git tracks them, not by their name.
LIVE_PATTERNS = (
    "runs", "gen-cache", "corpus-snapshot",
    "call-ledger.jsonl", "call-ledger.jsonl.head.json",
    "reality-probe.json", "corpus-manifest.json",
    "rule-R-evaluation-log.json",
    "questions-*.json", "index-*.json", "selection-*.json",
    "effect-table-*.json", "smoke-audit-*.json", "STOP-*.json",
)


def live_artifacts(here):
    """Basenames of every live-run artifact currently present."""
    found = set()
    for pattern in LIVE_PATTERNS:
        for path in glob.glob(os.path.join(here, pattern)):
            found.add(os.path.basename(path))
    return sorted(found)


EXPECTED_MANIFEST = "expected-artifacts.json"


def in_git_work_tree(here):
    try:
        out = subprocess.run(
            ["git", "-C", here, "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True).stdout.strip()
    except OSError:
        return False
    return out == "true"


def expected_artifacts(here):
    """The committed list of artifacts this study legitimately ships.

    Finding G-M3-1: the gate's discriminator is git-tracked status, and the
    public bundle ships WITHOUT a git work tree. Outside one, `git ls-files`
    returns nothing, every artifact reads as uncommitted, and a reader running
    the suite would see the gate fail on a perfectly good bundle. This
    manifest is the fallback: in-repo, git remains authoritative; outside a
    repo, an artifact is accounted for iff it is named here.
    """
    path = os.path.join(here, EXPECTED_MANIFEST)
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return set(json.load(fh).get("artifacts", []))


def is_tracked(here, name):
    """True iff the artifact is accounted for: git-tracked inside a work
    tree, or named in the expected-artifact manifest outside one."""
    if in_git_work_tree(here):
        try:
            out = subprocess.run(["git", "-C", here, "ls-files", "--", name],
                                 capture_output=True, text=True).stdout
        except OSError:
            return False
        return bool(out.strip())
    expected = expected_artifacts(here)
    if expected is None:
        return False          # no git, no manifest: fail closed, as before
    return name in expected


def leak_findings(here, before):
    """The gate. Returns [(condition, [names])]; empty means clean."""
    now = live_artifacts(here)
    created = [n for n in now if n not in before]
    uncommitted = [n for n in now if not is_tracked(here, n)]
    findings = []
    if created:
        findings.append(("created_by_suite", created))
    if uncommitted:
        findings.append(("present_but_uncommitted", uncommitted))
    return findings


def exit_code(tests_passed, findings):
    """A leak fails the run even when every test passed."""
    return 0 if (tests_passed and not findings) else 1


def main():
    sys.path.insert(0, HERE)
    sys.path.insert(0, os.path.join(HERE, "tests"))
    before = live_artifacts(HERE)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite(loader.loadTestsFromName(m) for m in SUITES)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    findings = leak_findings(HERE, before)
    print(f"\nsuites={len(SUITES)} tests={result.testsRun} "
          f"failures={len(result.failures)} errors={len(result.errors)}")
    if findings:
        for condition, names in findings:
            print(f"LEAK GATE FAILED [{condition}]: {names}")
        print("A live-run artifact is unaccounted for. Commit it if it is a "
              "registered milestone output; delete it if a test wrote it.")
    else:
        print("leak gate: clean — every live-run artifact present is "
              "committed, and the suite created none")
    return exit_code(result.wasSuccessful(), findings)


if __name__ == "__main__":
    sys.exit(main())
