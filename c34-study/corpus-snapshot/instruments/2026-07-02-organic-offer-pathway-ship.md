# Organic-offer pathway — SHIPPED (C25 intervention, Option A)

*2026-07-02. Dated ship doc required by C25 gate-condition (1) and the
offer-pathway design proposal's acceptance contract
(`applications/2026-07-01-offer-pathway-design-proposal.md` §4). This doc
records the engine commit, the trigger, the frozen lane parameters, and the
regime boundary. It opens no verdict: the C25 gate still requires ≥150
post-intervention runs, and the analyzer enforces that itself.*

## Regime boundary (hard rule)

- **`MENTU_C25_INTERVENTION_AT` = `2026-07-02T18:43:00Z`** — the UTC author
  time of the final shipping engine commit. Machine-readable copy:
  `instruments/c25-intervention-marker.json`.
- Pre- and post-intervention return rates are **never pooled** across this
  boundary, exactly as the footer-diagnostic boundary
  (`2026-07-01T21:18:39Z`) is treated. The pre arm stays the frozen read-only
  baseline in the conjecture (organic offer 0.0222%).

## Engine commits (mentu-complete, branch `main`)

| Commit | What |
|---|---|
| `cb1c44ca5265b6bfaf1f0289237c00b205455de5` | `feat(cir): organic handle-return offer lane (C25 intervention, Option A)` — the lane, brief integration, provenance recording at both runner injection sites, 8 tests |
| `715b35256157f32a610e182469cd00408614d8a0` | `fix(cir): handle-return lane ranks by confidence instead of gating on it` |
| `31444d240e9000f3585e2ff6187c1f9d145cd111` | `fix(cir): handle-return lane matches domain_tags as a handle carrier` |
| `fb85d754c6a1b41aabc35491e7e470f6f1a61edd` | `fix(cir): handle-return lane keeps supersession and derived-debt exclusions` — **the shipping commit; its author UTC is the regime marker** |

All four landed before any post-intervention run accrued; the marker is the
last of them, so the post arm begins only after the final lane semantics were
in place. The deployed binary (`~/.local/bin/mentu`, `com.mentu.engine`,
Developer-ID signed) was built from `fb85d754`.

## The trigger (Option A — C7 handle-return lane)

`mentu-engine/Sources/MentuEngine/CIRHandleReturnLane.swift`, invoked inside
`CIRContextBrief.build` — the single place step briefs are assembled — so it is
live on the **main run path** (SequenceRunner step briefs and LoopRunner live
briefs), not behind any experiment flag.

At step-brief build time the lane surfaces prior **distilled** signals that
share a **stable handle** with the current run's inputs, by **exact identity**:

- **Input handles of a run**: its recipe identity, in bare form (`<recipe>`)
  and typed form (`workflow:<recipe>`, the `mentu.epistemic_handle.v1`
  contract form).
- **Handle carriers on prior signals**, in precedence order: latest
  interpretation `entities`, then `domain_tags`. (Measured 2026-07-02: run
  reflections — the per-run distilled lessons — carry `entities=[]` and
  `domain_tags=[<recipe>]`; entity-only matching never fires on them.)
- Offered ids join `injectedSignalIds` and flow through the **unchanged**
  positioned `CIR_USED:` footer contract, credit adjudication, anti-gaming
  guard, and `footer_present_unpositioned` diagnostic. The lane changes what
  is *offered*, never how use is *proven*.

## Frozen lane parameters (fixed at ship, before any post-arm accrual)

| Parameter | Value | Rationale |
|---|---|---|
| trigger_type | `handle_return_v1` | provenance discriminator |
| max offers per brief | 3 | bounded context, mirrors reflections cap |
| recency window | 30 days | brief's existing window |
| allowed kinds | the brief's distilled-kind list | the "exhaust evidence → 0% citation" lesson holds |
| confidence | **ranks, does not gate** (no 0.35 floor) | measured 2026-07-02: only 6.7% of recent distilled signals clear 0.35, and 0/69 reflections do (avg 0.116) — trust decay outpaces return, so a floor makes the lane dead code; the frozen design says "top-k by recency/confidence" |
| kept guards | low-information body eligibility; usage-debt suppression; supersession exclusion; derived-source-debt exclusion (all at `minimumConfidence: 0`) | a handle match must not return junk, superseded knowledge, or debt laundered through derived wrappers |
| ordering | effective confidence DESC, ts DESC | "top-k by recency/confidence", deterministic |

## Offer provenance (C25 instrument prerequisite 3)

Every offer **actually surfaced** appends one record to
`cir-offer-provenance.jsonl` (workspace state dir):
`{run_id, offered_signal_id, trigger_type, trigger_key, recipe, step, ts}` —
`trigger_key` is the matched handle, so provenance is self-documenting. Offer
count is derivable from these records alone, independent of use. Recording
happens at the runner's injection sites only: a prepared-but-withheld brief
(C1b withheld arm) writes **no** offer record.

## Acceptance contract — item by item

1. **Trigger live on the main run path, with fire/no-fire tests** — YES.
   `Tests/MentuEngineTests/CIRHandleReturnLaneTests.swift` (10 tests): fires on
   a matching run; silent on a non-matching run; typed `workflow:` form;
   domain-tag carrier; decayed-confidence return; self-run exclusion;
   provenance shape; empty-offer no-write.
2. **Provenance record per organic offer** — YES (see above).
3. **Footer credit contract and diagnostic unchanged** — YES. The committed
   `misplaced` anti-gaming test and the full `CIRContextBrief` suite (31
   tests) pass unmodified, plus randomizer/accounting/conformance/outcome/
   gateway suites (50 tests).
4. **Marker set; dormant analyzer counts post-intervention runs** — YES.
   `MENTU_C25_INTERVENTION_AT=2026-07-02T18:43:00Z`; machine-readable
   fallback `instruments/c25-intervention-marker.json` wired into the
   analyzer's marker resolution (the wiring its preregistered docstring
   explicitly anticipated). The analyzer remains dormant until ≥150
   post-intervention runs accrue — it enforces this itself.

## Live verification (2026-07-02, engineering — not accrual)

- Step briefs built against the live substrate now organically return prior
  run reflections: recipe `cal-m1` → 1 offer, recipe `crawlio-workbench-m1` →
  2 offers, each `via=<recipe-handle>`, usage contract active. These were
  CLI brief builds, not sequence runs: they write no outcome rows and no
  offer provenance, and cannot accrue to any arm.
- A dedicated probe recipe (`c25-pathway-probe`) exercised the full
  capture→return loop end-to-end; its name classifies it **smoke**, so it is
  excluded from analysis accrual by the frozen `run_class` rule (confirmed:
  analyzer still reports 0/150 after both probe runs). Observed:
  - Run 1 (`run_c25-pathway-probe_1783018062`, 18:47:42Z): no prior
    handle-matched work → lane correctly silent (`not_injected`), run PASS,
    reflection `mem_63bf1014` emitted with `domain_tags=["c25-pathway-probe"]`.
  - Run 2 (`run_c25-pathway-probe_1783018850`, 19:00:50Z): run 1's reflection
    **organically offered** (`injected_signal_ids=[mem_63bf1014]`), offer
    provenance written (`trigger_type=handle_return_v1`,
    `trigger_key=c25-pathway-probe`), usage contract active; the agent
    declared it unused (`cir_verdict=ignored`, `use_rate=0`) — an honest
    Stage-2 outcome recorded through the unchanged credit contract. Stage 0
    (organic offer) is live; Stage 2 (use-when-offered) is exactly what the
    150-run gate will adjudicate.

## Known interactions, stated before accrual

- **C1b is live** (`cir_randomize` on): ~half of post-intervention feature
  runs land in the withheld arm and receive no brief, hence no organic offer.
  The C25 analyzer counts *all* post-marker feature runs in its denominator,
  so C1b dilutes the measured return rate by roughly half. This is noted now,
  before accrual; the frozen analyzer, predictions, and thresholds are
  unchanged and no mid-study parameter will be touched. If P1 clears its
  order-of-magnitude bar under dilution, it clears it a fortiori without.
- **The upstream suppressor found during shipping**: trust decay drives
  distilled-signal effective confidence below the runtime floor within days
  (reflections avg 0.116 vs floor 0.35). The lane routes around the floor by
  design (identity match + kept guards). This is instrument knowledge for a
  future conjecture, not a C25 result.
- The engine emits run reflections with the recipe handle only in
  `domain_tags`; richer capture-time handles (typed entities per
  `mentu.epistemic_handle.v1`) remain the C7-aligned improvement path and are
  NOT required for the lane to fire.

## What this doc does NOT do

It opens no gate by itself, computes no verdict, and changes no frozen
prediction, threshold, or falsification rule. C25's verdict comes only from
the dormant analyzer after ≥150 post-intervention runs, adjudicated
mechanically against the preregistered criteria and ratified by a human.
