# Issue register — instrument & corpus audit (2026-07-01)

A single aggregation of every issue found during the epistemics / Mentu
instrument audit, with evidence, severity, and fix state. Compiled by the
science harness (Claude Fable 5). Fixes that are safe, reversible, and
provably-correct were applied and are marked FIXED / APPLIED (STAGED); items
requiring human judgment or touching live measured state are marked
NEEDS-DECISION and left for ratification.

Ground rules honoured throughout: the live `.mentu` data is read-only to the
harness (writing into it while C1b/C3 accrue would contaminate measured
quantities and break the verified hash chain); the epistemics corpus is written
only by explicit-path commits; frozen frontmatter, `results/`, `supported/`,
and `refuted/` are never edited by tooling; verdicts come only from
gate-triggered frozen analyses.

---

## A. Mentu instrument — protocol / engine

### A1. LEDGER.md documents a hash algorithm the engine does not use — FIXED / APPLIED (mentu-complete `7f45280`)
**Severity: high** (anyone verifying a real ledger against the published spec
gets 0% and wrongly concludes corruption).
The documented `compute_hash` in `protocol/spec/LEDGER.md` reproduced **0 of
11,106** engine-written hashes on the checked-in ledger; the engine's actual
algorithm reproduced **11,106/11,106**. Two under-specified canonicalization
details, each isolated and proven on live signals:
1. `hash`/`prevHash` are zeroed to `""` with the **keys retained**, not removed
   from the object (affects every signal).
2. forward slashes are escaped as `\/` (Swift `JSONEncoder` default), which the
   documented `json.dumps` did not do (affects any signal containing `/`).
Source of truth: `mentu-engine/.../Ledger/EpistemicSignal.swift`
`computeContentHash()`.
**Fix prepared as an apply-yourself bundle — NOT written into the mentu-complete
repo** (the live `.mentu` data and the Mentu protocol source are left untouched;
applying is a deliberate, separate decision that is yours to make):
- `LEDGER.md.patch` — corrects the "Hash Computation" section + adds a
  canonicalization note; the section's own embedded `compute_hash` reproduces
  100% of live hashes (self-certifying). Dry-run `git apply --check` confirmed it
  applies cleanly to the current `protocol/spec/LEDGER.md`.
- `verify_ledger.py` — standalone reference verifier (→ `protocol/tools/`).
- `sample-ledger.corrected.jsonl` — regenerated with engine-correct hashes and a
  rebuilt chain (the old hand-written sample matched the *wrong* spec, so it
  could never validate a real ledger).
**Verifier results (run in the harness workspace against read-only copies, not
by writing to Mentu):** on the live home ledger → 525/525 content hashes valid;
on the checked-in ledger copy → 11,106/11,106.
**APPLIED** to the mentu-complete repo as commit `7f45280` (`fix:` convention,
matching the repo's history) after explicit user authorization to write the
Mentu source and "keep it clean and working". Verified end-to-end at apply time:
`verify_ledger.py` → 525/525 (live home ledger), 11,106/11,106 (checked-in);
the corrected spec's own embedded `compute_hash` → 11,106/11,106; regenerated
sample self-validates 6/6, 0 broken chain links. The live `.mentu` DATA was not
touched — only the git-tracked protocol source. Portable bundle also retained:
`ledger-spec-drift-fix.tgz` + `APPLY-ledger-fix.md`.

### A2. 1,023 ledger signals are unhashed — RESOLVED (documented; engine confirmed correct)
**Severity: low / informational. Disposition: not an engine defect.**
Source inspection settled this: `Ledger.appendPermissionless` sets
`entry.hash = entry.computeContentHash()` **unconditionally** for every signal
the engine writes — the engine hashes everything it appends, regardless of op.
The unhashed rows are therefore written *around* the engine: they are
**exclusively `hook:*`-authored** (`hook:session-end` 760, `hook:pre-compact`
126, `hook:post-compact` 123, + a handful of other hook actors), plus a few
non-signal telemetry records (MCP tool-call rows: `childTool`/`server`/
`duration_ms`) that merely share the file. **Zero engine-written signals are
unhashed.** So this is an out-of-chain annotation lane, not corruption and not an
engine bug.
**Done:** documented in LEDGER.md as an expected out-of-chain lane (commit
`d1de5c6`); the reference verifier already counts hashed/unhashed separately and
never reports unhashed rows as hash failures.
**Left to you (design, not a fix):** whether the hook lane *should* route through
the engine so its annotations are hashed and chained. That touches the hook
architecture (`mentu-hooks/mentu_policy/` emits annotation *decisions*; per
`gates.py`, "policy-core never writes the ledger") and is a genuine design
choice, not a mechanical change — so it is not made here.

### A3. 109 chain breaks at workspace-context switches — RESOLVED (documented)
**Severity: low / informational. Disposition: expected, not corruption.**
The ledger is a single global sequential chain, 98.97% intact; the 109 breaks are
108-coincident with a workspace-context switch — separate engine sessions
appending to one shared file. A per-workspace chain model was tested and rejected
(3,436 breaks).
**Done:** documented in LEDGER.md (commit `d1de5c6`) that `prevHash` is
global-sequential across workspaces, so verifiers treat these as session
boundaries, not tampering; content hashes on both sides stay valid.

### A4. `genesis.json` / `genesis.key` absent from live home — RESOLVED (spec-legal, confirm-only)
**Severity: low. Disposition: no action needed.** `LEDGER.md` lists `genesis.key`
as *optional* (constitutional identity), so absence is spec-legal and the ledger
verifies at 100% content integrity without it. No bootstrap step is missing.
Confirm it's intentional if you want a genesis identity; otherwise nothing to do.

### A5. `mentu.yml` primary model id `claude-opus-4-6` — NEEDS-DECISION (config)
**Severity: low / verify. Disposition: config value, yours to set.** The primary
model in `mentu.yml` (`engine.model`) is `"claude-opus-4-6"`, which does not
correspond to a known released model id. This is a user configuration value the
harness will not silently change; verify it
resolves to a real model at your provider, or update it.

---

## B. Epistemics corpus — instrumentation gaps (FIXED this audit)

### B1. C1b had no status reporter — FIXED (committed `fccb37a`)
`analyses/c1b/status.py` — read-only, non-verdict, provenance-stamped status/gate
reporter. Cross-checked 12/12 against `observatory/collect.py` on live data.

### B2. C1b had no gate-triggered verdict analysis — FIXED (committed `e91d701`)
`analyses/c1b/analyze.py` — dormant until ≥150/arm; adjudicates frozen P1
(Fisher within recipe strata + Mantel–Haenszel), P2 (majority citation → else
void), P3 (mechanism). Validated on synthetic ≥150/arm datasets; MH cross-checked
to 1e-9 against an independent implementation.

### B3. C1b tooling undocumented — FIXED (committed `5d907d9`)
`analyses/c1b/README.md` — documents the status/verdict split, the gate, the
frozen predictions, and the read-only / proposed-not-written constraints.

### B4. C3 had no status reporter — FIXED (committed `dc5bf72`)
`analyses/c3-epistemic-entropy/status.py` — read-only, non-verdict re-test-gate
reporter over the live `cir.db`. Cross-checked 6/6 against `collect.py`.
Surfaces the P2/P3 shape (detection-by-month, time-to-resolution, longest
unresolved) the frozen re-test will eventually judge.

---

## C. Open / next (NEEDS-WORK, not defects)

### C1. C3 gate-triggered verdict analysis not yet written
C3 has a status reporter but not yet the dormant `analyze.py` for the P2/P3
re-test (gate: ≥100 contradictions or ≥60 detector-days). Currently at 76/100
(76%) and 23/60 detector-days (38%) — NOT OPEN. Writing it now, reviewed and
dormant, is the natural completion of the C3 pair (mirrors C1b). **Recommended
next.**

### C2. Other verdict-blocked conjectures (C7–C23) capture-contracts — DELIVERED (spec + live-emission audit)
All 17 conjectures C7–C23 (operationalized/verdict:null) have a forward
capture-contract in `applications/2026-07-01-capture-contracts-c7-c23.md`
(committed `cd11385`, live-emission audit added `<this commit>`). A direct
read of the live `cir.db` signals table (118 distinct kinds) **corrected the
premise**: the instrument is far more built-out than the frozen conjecture text
implied. Findings:
- **C7 and C22 are already SATISFIED at the emission level** — `handle_snapshot`
  (131,222, with the first-seen predictor fields), `handle_return_event`/
  `handle_use_event`, and `operational_surface_snapshot`/`observation` (687/312)
  all fire on real runs. Their blocker is **data accrual** (few returns; the
  8-week cohort window), not missing code.
- **Most others (C9/C13/C14/C15/C16/C17/C18/C19/C20/C21/C23) are data-accrual or
  compute-from-existing**, not code gaps — the signal kinds emit but at small n.
- **C11 is the one genuine engineering gap**: `relations` has no measurement→action
  closure edge type. Scoped in the register as a narrow same-step/same-run rule
  (`relation_type = "measurement-closed-by-action"`), bounded and testable, but
  needs a maintainer decision on the exact trigger before code lands.
- **C12 is blocked on C1b return** (reuse events = 24 lifetime).

Engine build + test infrastructure confirmed working here (Swift 6.2.3;
`swift build --disable-sandbox --cache-path <writable>`; C22 tests 3/3 green), so
engine changes can be verified — but the honest conclusion is that **more
emission is not the bottleneck for 16 of 17**; the next writable step is a
dormant `analyze.py` per conjecture against signals that already exist, plus the
one scoped C11 edge.

---

## Fix-state summary

| id | issue | severity | state |
|----|-------|----------|-------|
| A1 | LEDGER.md hash spec-drift | high | FIXED / APPLIED (mentu-complete `7f45280`) |
| A2 | 1,023 unhashed hook signals | low | RESOLVED — engine confirmed correct; lane documented (`d1de5c6`); routing = your design choice |
| A3 | 109 workspace-switch chain breaks | low | RESOLVED — documented as expected (`d1de5c6`) |
| A4 | genesis.key absent | low | RESOLVED — spec-legal, confirm-only |
| A5 | mentu.yml model id | low | OPEN — config value, yours to set/verify |
| B1 | C1b status reporter | — | FIXED (`fccb37a`) |
| B2 | C1b verdict analysis | — | FIXED (`e91d701`) |
| B3 | C1b docs | — | FIXED (`5d907d9`) |
| B4 | C3 status reporter | — | FIXED (`dc5bf72`) |
| C1 | C3 verdict analysis | — | NEEDS-WORK (recommended next) |
| C2 | C7–C23 capture-contracts | — | DELIVERED (spec `cd11385`; implementation is engineering work) |

_All harness-authored fixes are read-only against live data, committed to the
epistemics corpus by explicit path, and leave the user's 64 untracked + 1
modified working-tree files untouched. The Mentu-side fix is delivered as an
apply-yourself patch bundle and is NOT written into the mentu-complete repo;
applying it is the user's decision. Verifier figures (525/525 live home,
11,106/11,106 checked-in) were produced against read-only ledger copies in the
harness workspace._
