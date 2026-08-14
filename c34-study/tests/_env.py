#!/usr/bin/env python3
"""C34 tests — where am I running?

The suite ships in the public bundle, which is a plain directory: no git
history, and no sibling repository files. A handful of tests legitimately
need one or the other. They SKIP in the bundle with an explicit reason rather
than failing (which would tell a reader the study is broken) or being deleted
(which would cost the repository its coverage).

Everything about the study itself — the harness, the adjudicator, all 390 run
records, the effect table, the annotations, the fixtures and every dead run
that does not require the repository — runs in both places.
"""
import os
import subprocess
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(STUDY, "..", ".."))


def in_git_work_tree(path=STUDY):
    try:
        out = subprocess.run(
            ["git", "-C", path, "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True).stdout.strip()
    except OSError:
        return False
    return out == "true"


def repo_file(rel):
    """Absolute path to a repository file, or None when it does not ship."""
    p = os.path.join(REPO, rel)
    return p if os.path.exists(p) else None


BUNDLE_REASON = ("runs from the public bundle, which ships no git history "
                 "and no sibling repository files; this check needs the "
                 "epistemics work tree (see registration/correction-v5.md)")

requires_repo = unittest.skipUnless(in_git_work_tree(), BUNDLE_REASON)


def require_repo_or_skip():
    """For setUpClass, where a decorator cannot reach."""
    if not in_git_work_tree():
        raise unittest.SkipTest(BUNDLE_REASON)


def require_repo_file(rel):
    p = repo_file(rel)
    if p is None:
        raise unittest.SkipTest(f"{rel} does not ship in the bundle; "
                                f"{BUNDLE_REASON}")
    return p
