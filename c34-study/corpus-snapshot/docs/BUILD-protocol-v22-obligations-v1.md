# BUILD — Protocol v2.2 Obligations (regime assimilation) v1

**Date:** 2026-07-06
**Compiles with:** `/scaffold docs/BUILD-protocol-v22-obligations-v1.md` (all phases mechanical; no SESSION/HUMAN items except the two named escalations)
**Depends on:** `instruments/2026-07-06-protocol-v22-regime-boundary-and-impact.md` (the impact audit this build executes — read it FIRST; it is the requirements source) · the corpus constitution (`README.md`, `CLAUDE.md` hard rules 1–6) · `mentu-complete` @ commit `949a018` (READ-ONLY reference)
**Executor:** claude-opus-4-8, working in `/Users/rashid/Desktop/epistemics`.
**Scope:** the four obligations from the impact audit — C25 co-intervention declaration, return-base-rate §2 verifier update, evidence-carrying-execution anchor re-grounding, provenance-map update. Nothing else.

---

## 0. Why this build exists

Protocol v2.2 (mentu-complete commits `c013b64..949a018`, 2026-07-05/06) changed the
instrument this corpus measures with: chain-verification semantics were corrected
(adjacency → canonical ancestry), a `lane_cutover` marker went live at
**2026-07-06T05:13:24Z**, `steer_message` became an embeddable CIR kind mid-C25-accrual,
MCP telemetry rows left `ledger.jsonl`, and new signal kinds entered the substrate. The
impact audit declared the regime boundary; this build discharges the four obligations it
names. **The corpus's honesty depends on declaring instrument changes before readouts —
that is why this runs now, while the C25 gate is still closed (0/150).**

## 1. Executor constitution (constitutional — no exceptions)

1. **Never edit** frozen frontmatter fields (claim, predictions, falsification criteria,
   `verdict`, `result`), anything in `results/`, `corpus/supported/`, or
   `corpus/refuted/`. Corrections are new dated documents. Before EVERY commit run:
   `git diff --stat results/ corpus/supported/ corpus/refuted/` → MUST be empty.
2. **Observer-effect rule.** Read Mentu data ONLY via direct file reads and
   `sqlite3 -readonly` / Python `mode=ro`. NEVER invoke the `mentu` binary or MCP CIR
   paths — they write access telemetry into the quantities this corpus measures. For
   ledger verification use `python3 <mentu-complete>/protocol/tools/verify_ledger.py`
   (a standalone read-only script), never `mentu verify-ledger`.
3. **mentu-complete is a read-only reference** at commit `949a018`
   (`/Users/rashid/Desktop/mentu-core-workspace/children/spine/mentu-complete`). No
   edits, no builds, no CLI runs there. Verify the commit before grounding file:lines:
   `git -C <mentu-complete> rev-parse --short HEAD` — if it moved past `949a018`,
   ground against the actual HEAD and record which.
4. **C25 discipline.** The gate is CLOSED (0/150). You may add *reporting-only* code
   and markers. You may NOT touch P1/P2 verdict logic, thresholds, the frozen
   predictions/falsification, the pre-arm baseline (organic offer 0.0222%), or the gate
   condition itself. Any amendment to `analyze.py` must be additive output, guarded so
   the adjudication path is byte-equivalent when the new population is empty.
5. **Commits:** in THIS repo, descriptive message ending with the Claude trailer
   (`Co-Authored-By: Claude <noreply@anthropic.com>` per repo practice), one commit per
   milestone, **do not push**. (Note: this is the epistemics convention — the opposite
   of mentu-complete's no-trailer rule. Do not confuse them.)
6. **Escalation triggers** (stop the milestone, write `docs/escalations/<date>-<slug>.md`,
   continue with the others): (a) O2's pinned ledger snapshot cannot be located AND the
   live-file re-derivation materially changes a number the paper presents as frozen;
   (b) O1 diagnosis shows steer-derived offers are structurally indistinguishable in the
   outcome rows (then the amendment becomes a documented limitation, not code);
   (c) any required edit would touch a frozen field.

## 2. Milestones

Execution order: **O1 → O4 → O2 → O3** (O1 is time-sensitive — it must precede any C25
accrual progress; O4 is small and unblocks the papers' provenance references; O2 and O3
are independent paper passes).

---

### O1 — C25 co-intervention marker + reporting-only analyzer amendment

**Why.** `steer_message` became embeddable + CIR-ingested (engine deploy
2026-07-06T08:54:43-06:00, commit `949a018`) — a new potential return channel landing
inside the C25 accrual window. Declared in the impact audit; this milestone makes the
declaration machine-readable and wires the reporting stratification BEFORE the gate can
open. Precedent: `instruments/c25-intervention-marker.json` +
"Known dilution noted pre-accrual: C1b withheld arm halves offer exposure" (README C25 row).

**O1.1 — Marker.** Create `instruments/protocol-v22-cointervention-marker.json`, exactly
the c25-marker shape:

```json
{
  "conjecture": "c25",
  "cointervention_at": "2026-07-06T14:54:43Z",
  "engine_commit": "949a018",
  "trigger_type": "steer_message_embeddable_v22",
  "ship_doc": "instruments/2026-07-06-protocol-v22-regime-boundary-and-impact.md",
  "note": "Protocol v2.2 made steer_message CIR-ingested and embeddable mid-accrual: a new retrievable-content class that can surface in briefs. Does not modify the C7 handle-offer mechanism P1 measures. Steer-derived offers must be reported separately at readout; never pooled silently."
}
```

(The timestamp is `949a018`'s commit time converted to UTC. Verify the conversion
yourself: `git -C <mentu-complete> log -1 --format=%cI 949a018`.)

**O1.2 — DIAGNOSE FIRST, then amend the analyzer (reporting-only).** Read
`analyses/c25-return-intervention/analyze.py` (`load_with_provenance`, `build_post_arm`,
`_offered`) and determine whether an offer row exposes the offered signal's *kind* (or
id, joinable read-only against the CIR store's `signals.kind`). Two outcomes:
- **Distinguishable** → add a reporting block: among post-intervention offered runs,
  count offers whose offered signals include kind `steer_message`; print one line
  (`steer-derived offers: k/n`) in the report section. Adjudication inputs (P1/P2
  numerators/denominators, thresholds) byte-identical — prove it by running the
  analyzer before and after (it prints GATE NOT OPEN; both outputs must be identical
  except nothing, since the gate path prints before any report).
- **Indistinguishable** → escalation (b): no code; write the limitation into O1.3's note.

**O1.3 — Dated amendment note.** `instruments/2026-07-06-c25-cointervention-amendment.md`
(≤ 1 page): what was added, why reporting-only, the diagnosis outcome, and the sentence
"predictions, falsification, thresholds, and the gate untouched." Update the README C25
row's *status text only* (the non-frozen prose after the gate condition) to append:
"v2.2 co-intervention declared (steer_message embeddable 2026-07-06) —
`instruments/protocol-v22-cointervention-marker.json`."

**Verification:** marker JSON parses (`python3 -c "import json;json.load(open(...))"`);
`python3 analyses/c25-return-intervention/analyze.py` still prints GATE NOT OPEN and
exits 0; `git diff results/ corpus/supported/ corpus/refuted/` empty; grep the frozen
frontmatter of `corpus/conjectures/*c25*` is untouched (`git diff corpus/conjectures/ | grep -E "^\+.*(prediction|falsification|verdict)"` → empty).

---

### O4 — Provenance map: the v2.2 instrument section

**Why.** `instruments/mentu-instrument.md` is the provenance map analyses trust; it
predates v2.2. Precedent section: "⚠️ Regime boundary: 2026-06-10T12:19Z".

**Work.** Add a new section "⚠️ Regime boundary: protocol v2.2 (2026-07-05/06)" after
the existing regime-boundary section, covering exactly:
1. **New stores**: `.mentu/cache/model-responses/` (content-addressed response blobs,
   2 MB cap, truncation markers) + `model-responses/manifests/<runId>.calls.jsonl`
   (per-run call manifests); `.mentu/mcp-telemetry.jsonl` — **MCP tool-call rows moved
   here out of `ledger.jsonl`** (any analysis expecting them in-ledger sees the lane
   frozen at the cutover).
2. **New signal kinds** in ledger/CIR: `steer_message` (embeddable, human intent),
   `model_call` / `tool_call` (7-day default half-life — same policy family as
   `temporal_result`), `call_lane`, `fork`, `session_anchor`, `lane_cutover`.
3. **Chain semantics**: canonical-ancestry verification; `lane_cutover` live at
   2026-07-06T05:13:24Z (1,023 grandfathered unhashed rows; post-cutover unhashed rows
   are violations); forks typed non-fatal, root cause (per-symlink locks) fixed;
   reference verifier = `mentu-complete/protocol/tools/verify_ledger.py` (v2,
   canonical-ancestry semantics, 2026-07-05) — name BOTH verifier versions so old
   numbers remain interpretable.
4. **Data-quality caveats delta**: steered runs now visible (`steer_message`);
   fork ancestry verifiable (`prefix_head_hash`); call lane covers ONLY engine
   in-process calls (child-agent calls out of lane — C1b Stage-2 unchanged).

**Verification:** `grep -c "v2.2" instruments/mentu-instrument.md` ≥ 3;
`grep -c "mcp-telemetry" instruments/mentu-instrument.md` ≥ 1; section ordering intact
(the 2026-06-10 boundary section still present above the new one).

---

### O2 — Return-base-rate paper §2: corrected verifier semantics

**Why.** Draft v1.2 (§2 "Ledger") reports 109 chain breaks with a statistical
session-boundary argument, computed under the OLD adjacency-semantics verifier. The
corrected reference verifier classifies the same bytes as 0 breaks + 62 typed forks +
1 genesis/import anchor, and the fork mechanism is root-caused (per-symlink locks) and
fixed upstream. The paper's integrity story strengthens; the load-bearing number (100%
content integrity, 11,106/11,106) is unchanged. This is an instrument correction, not a
data change — and it must land before submission.

**O2.1 — DIAGNOSE FIRST: locate the paper's pinned ledger bytes.** The §2 numbers were
computed on the 2026-06-28-cut ledger (12,129 signals). Search
`paper/build-return-base-rate/`, `analyses/`, and any dataset-digest notes for a pinned
copy or a sha256 of the exact file analyzed. Outcomes:
- **Pinned copy found** → run the NEW verifier against it:
  `python3 <mentu-complete>/protocol/tools/verify_ledger.py <pinned> --json`. Expect
  0 breaks (or 1 genesis anchor recognized), N forks, unchanged content integrity.
- **No pinned copy** → run against the live ledger AND report both totals (the live
  file has grown; the chain-classification claims are about the same prefix). If any
  number the paper presents as frozen would materially change → escalation (a).
Record the command + output verbatim in O2.3's note.

**O2.2 — Edit the paper (BOTH surfaces, kept consistent).** The canonical doc is
`paper/return-base-rate-paper.md`; the typeset source is
`paper/build-return-base-rate/body.md`. In §2 "Ledger":
- Replace the adjacency-era chain paragraph: under canonical-ancestry semantics
  (verifier v2, 2026-07-05) the chain shows **0 missing-ancestor breaks**; the 109
  previously-reported "breaks" decompose into 62 typed concurrency forks + skip-links +
  1 genesis/import anchor; the fork mechanism is root-caused (per-symlink append locks,
  fixed in mentu-complete `c013b64`) — the session-boundary argument is now mechanical,
  not statistical. Keep the 100% content-integrity sentence verbatim (it is the
  load-bearing claim and did not change).
- Keep the per-workspace-model rejection sentence (3,436 breaks) as historical method
  detail, marked as computed under verifier v1.
- Add one instrument-version footnote: "Chain classification per reference verifier v2
  (canonical-ancestry semantics, 2026-07-05, `protocol/tools/verify_ledger.py`);
  draft v1.2 and earlier used v1 (line-adjacency semantics)."
- Bump the draft line to **v1.3** with a one-line change note ("§2 chain semantics
  updated to verifier v2; content-integrity result unchanged").
- Do NOT touch §3–§6 (funnel numbers, C25 preregistration, figures) — the boundary of
  this edit is §2 + the version line.
**Rebuild:** run `paper/build-return-base-rate/build.py`. If the toolchain (pandoc/latex)
is unavailable, leave body.md consistent and note the pending rebuild in O2.3 — do not
half-generate artifacts.

**O2.3 — Dated instrument note.** `instruments/2026-07-06-return-paper-verifier-v2-rederivation.md`:
the verifier command + verbatim output, old→new classification table
(109 breaks → 0 breaks / 62 forks / 1 anchor), and the statement that ledger bytes are
untouched.

**Verification:** `grep -c "verifier v2\|canonical-ancestry" paper/return-base-rate-paper.md` ≥ 1
and same for `paper/build-return-base-rate/body.md`; `grep -c "11,106/11,106\|11106/11106" paper/return-base-rate-paper.md` ≥ 1
(load-bearing number still present); `grep -n "v1.3" paper/return-base-rate-paper.md` ≥ 1;
frozen-dir diff guard empty.

---

### O3 — Evidence-carrying-execution paper: re-ground verification anchors + v2.2 addendum

**Why.** `paper/evidence-carrying-execution/formal/invariant-spec.md` grounds its seven
invariants in `Ledger/Ledger.swift` file:line references + source digests ("Source
digests (verification anchor)"). Commits `c013b64`/`82deb5b`/`949a018` modified that
file (K1's `validateCitation` shifted ~9 lines down; `verify()` rewritten; marker
methods added). The paper's own provenance discipline requires re-verification. And
v2.2 is new material squarely on its thesis.

**O3.1 — Re-ground.** For every file:line citation in `invariant-spec.md` (grep
`Ledger/Ledger.swift:` and any other `mentu-complete` file:line refs): re-locate the
symbol in the tree @ `949a018` (read-only), update the line numbers, and recompute the
source digests exactly the way the spec's "Source digests" section defines them (read
that section first and reproduce its digest command verbatim). Update the digest table
and stamp the grounding commit (`949a018`) next to it.

**O3.2 — v2.2 addendum (new dated section, not a rewrite).** Append to
`invariant-spec.md` (or a sibling `formal/v22-addendum.md` if the spec declares itself
frozen — check its header discipline first) a short section: "Protocol v2.2
strengthens four invariants mechanically", citing with file:line @ `949a018`:
- In-engine canonical-ancestry chain verification (`MerkleLedgerLineage.classify`,
  wired into `Ledger.verify`) — Invariant 4 (provenance preservation) now machine-checked
  end-to-end, orphaned rows fatal.
- Invariant 6 of the protocol ("Inputs Are Events", `steer_message` at both drain
  boundaries) — closes the unrecorded-input hole in Evidence Accompaniment.
- Strict verification-replay (`RunsReplay`, `E_REPLAY_DIVERGED`) + chain-anchored call
  lanes (`call_lane` / `manifest_sha256`) — evidence about execution now carries a
  mechanical reproducibility proof.
- Projections discipline (`StepStatus.cacheKey` revalidation) — cached state can no
  longer silently masquerade as evidence-bearing state.
Update `paper.md`'s draft line v1.1 → **v1.2** with a one-line change note ("verification
anchors re-grounded @ 949a018; v2.2 addendum added"). Do not alter the paper's claims,
numbers, or the RE-DERIVE-not-canon rule (its own BUILD §1).

**O3.3 —** If `evidence/audit.py` / `audit_v2.py` pin source digests of engine files,
re-run them read-only and record outputs; if they fail on the moved lines, update ONLY
their digest/line tables, never their measured numbers.

**Verification:** every `Ledger/Ledger.swift:<n>` citation in invariant-spec.md resolves
to the named symbol at `949a018` (spot-check K1: `validateCitation` body contains
`citationRequired`); `grep -c "949a018" paper/evidence-carrying-execution/formal/*.md` ≥ 1;
`grep -c "v2.2" paper/evidence-carrying-execution/` (recursive) ≥ 2; frozen-dir diff
guard empty.

---

## 3. Completion

One commit per milestone (O1, O4, O2, O3), each ending with the Claude trailer, none
pushed. Final check across the whole build:

```
git log --oneline -4                      # four milestone commits
git diff origin/main..HEAD --stat 2>/dev/null || true
git diff HEAD~4 --stat -- results/ corpus/supported/ corpus/refuted/   # MUST be empty
python3 analyses/c25-return-intervention/analyze.py                    # GATE NOT OPEN, exit 0
```

Print `V22_OBLIGATIONS_COMPLETE` only when all four milestones landed (or their named
escalations are filed) and the frozen-dir guard is empty.
