#!/usr/bin/env python3
"""C34 M2 tests — harness mechanics and their dead runs.

Offline only. `run_claude` is never invoked: no provider, no network, no
subprocess to `claude`, no Mentu path.
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


class TestHydrationOneCodePath(unittest.TestCase):
    """Deviation D-6: the record is computed by ONE function for both agentic
    arms. C29 computed it under `if p == "C"`, and the manuscript read
    mis-routing as stopping at two claim sites as a result."""

    GOLD = "docs/doc007.md"

    def test_identical_inputs_give_identical_records_across_arms(self):
        reads = ["/sandbox/docs/doc007.md"]
        searches = [{"tool": "Grep", "pattern": "x", "path": ""}]
        b = H.hydration_record(reads, searches, self.GOLD)
        c = H.hydration_record(reads, searches, self.GOLD)
        self.assertEqual(b, c)      # no arm argument exists to differ on
        self.assertNotIn("policy", H.hydration_record.__code__.co_varnames)

    def test_located_first_read_gold_and_zero_read(self):
        h = H.hydration_record(["/s/docs/doc007.md"], [], self.GOLD)
        self.assertTrue(h["located"] and h["first_read_is_gold"])
        self.assertFalse(h["zero_read"])
        self.assertEqual(h["read_count"], 1)

    def test_mis_routed_is_distinguishable_from_true_stop(self):
        mis = H.hydration_record(["/s/docs/doc999.md"], [], self.GOLD)
        stop = H.hydration_record([], [], self.GOLD)
        self.assertFalse(mis["located"])
        self.assertEqual(mis["read_count"], 1)
        self.assertFalse(mis["zero_read"])
        self.assertFalse(stop["located"])
        self.assertTrue(stop["zero_read"])

    def test_first_read_is_gold_false_when_gold_read_second(self):
        h = H.hydration_record(["/s/docs/doc999.md", "/s/docs/doc007.md"],
                               [], self.GOLD)
        self.assertTrue(h["located"])
        self.assertFalse(h["first_read_is_gold"])

    def test_searches_carry_their_patterns(self):
        h = H.hydration_record(
            [], [{"tool": "Grep", "pattern": "alpha-007", "path": ""}],
            self.GOLD)
        self.assertEqual(h["searches"][0]["pattern"], "alpha-007")

    def test_dead_run_missing_hydration_is_detected(self):
        self.assertFalse(H.hydration_complete({"policy": "B"}))
        self.assertFalse(H.hydration_complete({"hydration": {"reads": []}}))
        self.assertTrue(H.hydration_complete(
            {"hydration": H.hydration_record([], [], self.GOLD)}))


class TestCallLedger(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "call-ledger.jsonl")
        self.led = H.CallLedger(self.path)
        self.led.reserve("reality_probe", "probe:generator", H.GENERATOR)
        self.led.reserve("reality_probe", "probe:answerer", H.ANSWERER)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_registered_budget_matches_the_registration_table(self):
        self.assertEqual(H.SUB_CEILINGS,
                         {"reality_probe": 2, "generation": 170,
                          "regeneration": 45, "digest": 170, "smoke": 30,
                          "confirmatory": 360, "retry": 150})
        self.assertEqual(sum(H.SUB_CEILINGS.values()), 927)
        self.assertEqual(H.GLOBAL_CEILING, 950)

    def test_probe_first_ordering_is_enforced(self):
        """Correction v2 C-5: availability is bought before the generation
        budget is spent, not assumed."""
        fresh = H.CallLedger(os.path.join(self.tmp, "fresh.jsonl"))
        with self.assertRaises(H.ProbeNotRun):
            fresh.reserve("generation", "generation:docs/a.md", H.GENERATOR)
        fresh.reserve("reality_probe", "p1", H.GENERATOR)
        with self.assertRaises(H.ProbeNotRun):
            fresh.reserve("generation", "generation:docs/a.md", H.GENERATOR)
        fresh.reserve("reality_probe", "p2", H.ANSWERER)
        fresh.reserve("generation", "generation:docs/a.md", H.GENERATOR)

    def test_reservation_is_durable_before_dispatch(self):
        self.led.reserve("generation", "generation:docs/a.md", H.GENERATOR)
        reread = H.CallLedger(self.path)
        self.assertEqual(reread.total(), 3)
        self.assertIn("generation:docs/a.md", reread.keys())

    def test_dead_run_sub_ceiling_exhaustion_stops_the_pass(self):
        for i in range(H.SUB_CEILINGS["regeneration"]):
            self.led.reserve("regeneration", f"regeneration:{i}", H.GENERATOR)
        self.assertEqual(self.led.remaining("regeneration"), 0)
        with self.assertRaises(H.CeilingExhausted):
            self.led.reserve("regeneration", "regeneration:overflow",
                             H.GENERATOR)
        # non-transferable: an untouched bucket does not fund the spent one
        self.assertEqual(self.led.remaining("digest"), 170)
        self.led.reserve("digest", "digest:docs/a.md", H.GENERATOR)

    def test_dead_run_global_ceiling_is_not_raised_by_spare_buckets(self):
        led = H.CallLedger(os.path.join(self.tmp, "g.jsonl"))
        led.reserve("reality_probe", "p1", H.GENERATOR)
        led.reserve("reality_probe", "p2", H.ANSWERER)
        for b, n in (("confirmatory", 360), ("retry", 150),
                     ("generation", 170), ("digest", 170), ("smoke", 30),
                     ("regeneration", 45)):
            for i in range(n):
                led.reserve(b, f"{b}:{i}", H.ANSWERER)
        self.assertEqual(led.total(), 927)
        for b in H.SUB_CEILINGS:
            with self.assertRaises(H.CeilingExhausted):
                led.reserve(b, f"{b}:overflow", H.ANSWERER)

    def test_cross_run_discovery_rebuilds_a_lost_ledger(self):
        """A WHOLLY ABSENT ledger is a loss, not a corruption: it starts from
        genesis and discovery reconciles it against the artifacts the calls
        produced. The count only ever moves up. (A ledger that is merely
        inconsistent raises instead — see TestLedgerIntegrity.)"""
        for i in range(5):
            self.led.reserve("generation", f"generation:docs/{i}.md",
                             H.GENERATOR)
        os.remove(self.path)                  # journal and head both gone
        os.remove(self.path + ".head.json")
        lost = H.CallLedger(self.path)
        self.assertEqual(lost.total(), 0)
        lost.discover({"generation": [f"generation:docs/{i}.md"
                                      for i in range(5)],
                       "reality_probe": ["probe:generator", "probe:answerer"]})
        self.assertEqual(lost.counts()["generation"], 5)
        self.assertTrue(lost.probe_complete())
        lost.discover({"generation": ["generation:docs/0.md"]})   # idempotent
        self.assertEqual(lost.counts()["generation"], 5)

    def test_unregistered_bucket_is_refused(self):
        with self.assertRaises(ValueError):
            self.led.reserve("extra_budget", "x", H.ANSWERER)


class TestLedgerIntegrity(unittest.TestCase):
    """Finding G-M2-1: the ledger is verified on load, and every
    inconsistency raises rather than proceeding. The failure direction of a
    silently short ledger is overspending a ceiling that is never allowed to
    be raised."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.path = os.path.join(self.tmp, "call-ledger.jsonl")
        led = H.CallLedger(self.path)
        led.reserve("reality_probe", "probe:generator", H.GENERATOR)
        led.reserve("reality_probe", "probe:answerer", H.ANSWERER)
        for i in range(4):
            led.reserve("generation", f"generation:docs/{i}.md", H.GENERATOR)

    def lines(self):
        with open(self.path) as fh:
            return [ln for ln in fh.read().splitlines() if ln.strip()]

    def rewrite(self, lines):
        with open(self.path, "w") as fh:
            fh.write("\n".join(lines) + "\n")

    def test_a_sound_ledger_loads_and_counts(self):
        led = H.CallLedger(self.path)
        self.assertEqual(led.total(), 6)
        self.assertEqual(led.counts()["generation"], 4)
        self.assertTrue(led.probe_complete())

    def test_every_entry_carries_a_chained_seal(self):
        prev = H.GENESIS_SEAL
        for line in self.lines():
            e = json.loads(line)
            self.assertEqual(e["seal"], H._seal(prev, e))
            prev = e["seal"]

    def test_dead_run_truncated_ledger_raises(self):
        """A dropped line leaves a chain that still verifies; the head record
        is what catches it."""
        self.rewrite(self.lines()[:-1])
        with self.assertRaises(H.LedgerIntegrityError) as cm:
            H.CallLedger(self.path)
        self.assertIn("head mismatch", str(cm.exception))

    def test_dead_run_partial_final_write_raises(self):
        lines = self.lines()
        lines[-1] = lines[-1][:len(lines[-1]) // 2]
        self.rewrite(lines)
        with self.assertRaises(H.LedgerIntegrityError) as cm:
            H.CallLedger(self.path)
        self.assertIn("does not parse", str(cm.exception))

    def test_dead_run_edited_line_raises(self):
        lines = self.lines()
        e = json.loads(lines[2])
        e["bucket"] = "digest"                 # move a call to another budget
        lines[2] = json.dumps(e, sort_keys=True)
        self.rewrite(lines)
        with self.assertRaises(H.LedgerIntegrityError) as cm:
            H.CallLedger(self.path)
        self.assertIn("seal mismatch", str(cm.exception))

    def test_dead_run_seq_gap_raises(self):
        lines = self.lines()
        del lines[2]
        self.rewrite(lines)
        with self.assertRaises(H.LedgerIntegrityError) as cm:
            H.CallLedger(self.path)
        self.assertIn("seq gap", str(cm.exception))

    def test_dead_run_a_forged_appended_entry_raises(self):
        """An extra reservation appended by hand, without re-sealing."""
        lines = self.lines()
        lines.append(json.dumps({"seq": 6, "bucket": "generation",
                                 "key": "forged", "seal": "0" * 64},
                                sort_keys=True))
        self.rewrite(lines)
        with self.assertRaises(H.LedgerIntegrityError):
            H.CallLedger(self.path)

    def test_integrity_failure_blocks_counting_entirely(self):
        """Nothing proceeds on a doubtful count: the object does not
        construct, so no caller can read a partial total from it."""
        self.rewrite(self.lines()[:-1])
        with self.assertRaises(H.LedgerIntegrityError):
            H.CallLedger(self.path).total()

    def test_dead_run_journal_deleted_but_head_kept_raises(self):
        """Indistinguishable from truncation, so it is refused rather than
        silently recovered. Resolving it is an operator decision."""
        os.remove(self.path)
        open(self.path, "w").close()
        with self.assertRaises(H.LedgerIntegrityError):
            H.CallLedger(self.path)

    def test_a_wholly_absent_ledger_is_a_loss_not_a_corruption(self):
        os.remove(self.path)
        os.remove(self.path + ".head.json")
        self.assertEqual(H.CallLedger(self.path).total(), 0)

    def test_discovery_maintains_the_chain(self):
        led = H.CallLedger(self.path)
        led.discover({"digest": ["digest:docs/a.md"]})
        reread = H.CallLedger(self.path)       # must verify
        self.assertEqual(reread.total(), 7)
        self.assertEqual(reread.counts()["digest"], 1)


class TestSandboxAssembly(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.sandbox = os.path.join(self.tmp, "sandbox")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_sandbox_assembles_from_the_snapshot(self):
        man, snap, entries = F.make_corpus(self.tmp, 5)
        mapping = H.build_sandbox(man, snap, self.sandbox,
                                  expect_files=len(entries))
        self.assertEqual(len(mapping), 5)
        for e in entries:
            with open(os.path.join(self.sandbox, e["path"]), "rb") as fh:
                self.assertEqual(H.sha256_bytes(fh.read()), e["sha256"])

    def test_dead_run_file_mutated_after_snapshot_fails_verification(self):
        man, snap, entries = F.make_corpus(self.tmp, 5,
                                           mutate="docs/doc003.md")
        with self.assertRaises(SystemExit) as cm:
            H.build_sandbox(man, snap, self.sandbox,
                            expect_files=len(entries))
        self.assertIn("SNAPSHOT HASH MISMATCH", str(cm.exception))

    def test_dead_run_corpus_precondition_fails_closed(self):
        """Correction v3 G5: one precondition assertion in place of the dead
        <135 and >170 branches."""
        man, snap, entries = F.make_corpus(self.tmp, 5)
        with self.assertRaises(SystemExit) as cm:
            H.build_sandbox(man, snap, self.sandbox, expect_files=141)
        self.assertIn("CORPUS PRECONDITION FAILED", str(cm.exception))

    def test_expected_corpus_files_is_the_registered_141(self):
        self.assertEqual(H.EXPECTED_CORPUS_FILES, 141)


class TestModelIdentityAndErrors(unittest.TestCase):

    def test_identity_read_from_all_three_provider_sites(self):
        pin = H.ANSWERER
        for events in (
                [{"type": "system", "subtype": "init", "model": pin}],
                [{"type": "assistant", "message": {"model": pin}}],
                [{"type": "result", "modelUsage": {pin: {}}}],
                [{"type": "result", "model_usage": {pin: {}}}]):
            self.assertEqual(H.model_identities(events), [pin])

    def test_dead_run_identity_drift_is_visible(self):
        events = [{"type": "system", "subtype": "init", "model": H.ANSWERER},
                  {"type": "assistant",
                   "message": {"model": "claude-sonnet-5"}}]
        self.assertEqual(H.model_identities(events),
                         sorted([H.ANSWERER, "claude-sonnet-5"]))
        self.assertNotEqual(H.model_identities(events), [H.ANSWERER])

    def test_hollow_run_reports_zero_tokens_and_no_identity(self):
        rec = H.record_from_events(
            [{"type": "result", "is_error": True, "usage": {},
              "result": ""}], H.ANSWERER)
        self.assertEqual(rec["input_tokens"], 0)
        self.assertEqual(rec["tokens_total"], 0)
        self.assertEqual(rec["model_identities"], [])
        self.assertTrue(rec["is_error"])

    def test_token_components_and_derived_measures(self):
        rec = H.record_from_events([{"type": "result", "usage": {
            "input_tokens": 10, "cache_creation_input_tokens": 100,
            "cache_read_input_tokens": 1000, "output_tokens": 5},
            "result": "ANSWER: x"}], H.ANSWERER)
        self.assertEqual(rec["tokens_total"], 1115)
        self.assertEqual(rec["tokens_marginal"], 115)     # excludes cache read
        self.assertEqual(rec["answer"], "x")

    def test_registered_retry_classes_only(self):
        self.assertEqual(H.RETRYABLE,
                         ("provider_session_limit",
                          "transport_failure_before_content",
                          "subprocess_timeout"))
        self.assertEqual(H.classify_error({"error": "timeout"}),
                         "subprocess_timeout")
        self.assertEqual(
            H.classify_error({"is_error": True,
                              "result_text": "You've hit your session limit"}),
            "provider_session_limit")
        self.assertEqual(
            H.classify_error({"error": "unparseable", "saw_assistant": False}),
            "transport_failure_before_content")
        self.assertIsNone(H.classify_error({"is_error": False}))

    def test_a_substantive_provider_error_is_not_retryable(self):
        cls = H.classify_error({"is_error": True, "result_text": "nonsense"})
        self.assertEqual(cls, "provider_error_unclassified")
        self.assertNotIn(cls, H.RETRYABLE)

    def test_tool_events_captured_in_order_with_patterns(self):
        events = [
            {"type": "assistant", "message": {"model": H.ANSWERER, "content": [
                {"type": "tool_use", "name": "Grep",
                 "input": {"pattern": "alpha", "path": "docs"}},
                {"type": "tool_use", "name": "Read",
                 "input": {"file_path": "/s/docs/doc001.md"}}]}},
            {"type": "assistant", "message": {"model": H.ANSWERER, "content": [
                {"type": "tool_use", "name": "Glob",
                 "input": {"pattern": "**/*.md"}},
                {"type": "tool_use", "name": "Read",
                 "input": {"file_path": "/s/docs/doc002.md"}}]}},
            {"type": "result", "usage": {}, "result": "ANSWER: y"}]
        rec = H.record_from_events(events, H.ANSWERER)
        self.assertEqual(rec["reads"],
                         ["/s/docs/doc001.md", "/s/docs/doc002.md"])
        self.assertEqual([s["tool"] for s in rec["searches"]],
                         ["Grep", "Glob"])
        self.assertEqual([s["pattern"] for s in rec["searches"]],
                         ["alpha", "**/*.md"])


class TestNoNetworkOrMentuPaths(unittest.TestCase):
    """The study reads repository files and calls a model. It reads no Mentu
    substrate, so the observer-effect rule is satisfied trivially — and this
    test is what makes that mechanical rather than asserted."""

    FORBIDDEN_IMPORTS = {"socket", "ssl", "http", "urllib", "requests",
                         "sqlite3", "ftplib", "telnetlib", "smtplib"}
    # substrings forbidden in STRING LITERALS — prose in docstrings may name
    # Mentu, but no executable path may address it
    FORBIDDEN_LITERALS = (".mentu", "mcp__", "http://", "https://", "sqlite",
                          "REDACTED-CLIENT-IDENTIFIER-workspace")

    def _modules(self):
        study = os.path.dirname(HERE)
        for name in sorted(os.listdir(study)):
            if name.endswith(".py"):
                with open(os.path.join(study, name)) as fh:
                    yield name, fh.read()

    def test_no_module_imports_a_network_or_database_surface(self):
        import ast
        for name, src in self._modules():
            for node in ast.walk(ast.parse(src)):
                mods = []
                if isinstance(node, ast.Import):
                    mods = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    mods = [node.module]
                for m in mods:
                    self.assertNotIn(m.split(".")[0], self.FORBIDDEN_IMPORTS,
                                     f"{name} imports {m}")

    def test_no_string_literal_addresses_mentu_or_a_network_endpoint(self):
        import ast
        for name, src in self._modules():
            for node in ast.walk(ast.parse(src)):
                if isinstance(node, ast.Constant) and isinstance(node.value,
                                                                 str):
                    if len(node.value) > 400:      # module/function docstrings
                        continue
                    low = node.value.lower()
                    for token in self.FORBIDDEN_LITERALS:
                        self.assertNotIn(token, low,
                                         f"{name} literal names {token!r}")

    def test_the_only_provider_entry_point_is_run_claude(self):
        """No module but `harness_lib` may dispatch the provider. The other
        subprocess use in the study is git plumbing over the pinned tree."""
        for name, src in self._modules():
            if name == "harness_lib.py":
                continue
            self.assertNotIn('"claude"', src, name)
            for call in src.split("subprocess.run(")[1:]:
                self.assertTrue(call.lstrip().startswith('["git"'),
                                f"{name} runs a non-git subprocess")

    def test_harness_dispatches_claude_with_no_session_persistence(self):
        with open(os.path.join(os.path.dirname(HERE),
                               "harness_lib.py")) as fh:
            src = fh.read()
        self.assertIn('"--no-session-persistence"', src)
        self.assertEqual(src.count("subprocess.run("), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
