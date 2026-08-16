---
id: c36-harness-freeze
conjecture: corpus/conjectures/c36-fused-locator-localization.md
registration: instruments/2026-08-16-c36-locator-bakeoff-registration.md
date: 2026-08-16
status: frozen-before-generation
---

# C36 harness freeze

Registration §6 checklist, item 1. This directory is committed and
hash-pinned **before any question is generated and before any arm runs**.
After this commit, changes here are dated correction documents, not edits.

## 1. Pins

| What | Pin |
|---|---|
| Corpus | C34 snapshot, 141 files, manifest sha256 `61b8d90b…f2a9b`, snapshot commit `cb736542…` — every file hash re-verified at every sandbox setup; mismatch aborts |
| mentu-navigator | commit `e405604476198aa760a9d36fcbae4b8f91116f30`; asserted before Phase A; drift aborts |
| Imported C34 instrument | `harness_lib.py` `d0fc51e2…9a50`, `generate_questions.py` `70c76660…1bc186` — byte-verified on every import |
| Generator model | `H.GENERATOR` = `claude-sonnet-5` (C34's, unchanged) |
| Answerer model | `H.ANSWERER` = `claude-haiku-4-5-20251001` (C34's, unchanged) |
| Generation prompt | C34 `Q_PROMPT` + `GEN_INPUT_CHARS` (8,000) + `RETRY_NOTE`, imported byte-verified |
| Salts | `c36-confirmatory-v1:` / `c36-smoke-v1:` (frozen here; no question exists) |
| Contract | k = 8 across all arms; D4 pins as shipped at the navigator commit |
| Scoring | boundary rule adjudicates; C34 rule descriptive (`scoring.py`) |

## 2. Sandbox discipline

Arms read a copy of the snapshot at `/private/tmp/claude-501/c36-sandbox/corpus`,
hash-verified against the manifest on every setup. Rationale: (a) the
navigator resolves a repository to its git toplevel, so running against the
in-repo snapshot would index all of epistemics; (b) `MENTU_NAV_HOME` points
into the sandbox, so bake-off telemetry never touches the production PD-1
sink; (c) the epistemics repo is never written by any run (asserted by
test_read_only_after_arms).

## 3. Run order (binding)

1. `python3 tests/test_c36.py` — 18 freeze tests green (includes live L0/L1/L2 smoke).
2. `python3 generate_questions_c36.py` — generation with gates; emits
   `questions-c36.json` (hash-pinned in the generation commit),
   `generation-log-c36.json` (per-gate rejection counts, exclusions,
   attempts), `spanish-gold-c36.json` (P3 subset, `lang: es` tag only).
3. `python3 run_arms.py a` — Phase A: localization for L0/L1/L2/L4 over all
   questions, one-shot (refuses to rerun over existing records); emits
   `metrics-c36.json` (P4 inputs: 5 cold builds, per-query medians).
4. `python3 run_arms.py b` — Phase B: P5 answerer runs, arms L0 and L2,
   confirmatory set only, resumable by record id.
5. `python3 adjudicate_c36.py` — mechanical verdict per the frozen
   thresholds; emits `adjudication-c36.json`. Interpretation never changes it.
6. Results document written from `adjudication-c36.json`; corpus move per
   the constitution.

## 4. The P5 policy, pinned (hydrate-all)

One locate per question per arm; the answerer receives the question plus
the full bodies of the arm's top-8 documents in rank order (each truncated
at 6,000 chars with a visible marker), answers in the C34 `ANSWER:`
convention. One model call per question per arm; no agentic read loop.

**Recorded deviation from C34's policy shape:** C34's search arm was an
iterative agentic grep loop. c36's P5 is a bounded hydrate-all policy.
Reason: c36 adjudicates arm-vs-arm *within itself*, and the bounded policy
makes the locator the only varying input — read-choice variance is removed
by construction. Consequence: c36's absolute accuracy numbers are not
comparable to C34's; only the L2−L0 delta is interpreted, which is all P5
stakes.

## 5. Machine record

Written into `metrics-c36.json` context at Phase A run time (hardware,
OS, node/python versions). The P4 build bound applies as measured on that
machine, which is recorded, not assumed.

## 6. Deviations at freeze time

None. The leak gate (G3) is recorded not-applicable in the generation log
(no arm in this study consumes digests); underpowered P3 adjudicates
nothing per the conjecture's n ≥ 25 guard.
