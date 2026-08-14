# Science corpus audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/ese/science/`

The directory contains 315 files across knowledge architecture, epistemic strategy,
thermodynamics, cognitive systems evolution, behavioral intelligence, heuristic
epistemology, and meta-cognitive architectures. No predecessor files were edited.
Live checks used direct reads of `~/.mentu/cir.db` and
`~/.mentu/training/cir-run-outcomes.jsonl`.

## Decision

Admit two readiness-gated conjectures:

- **C11 measurement-action closure**:
  `corpus/conjectures/c11-measurement-action-closure.md`
- **C12 translation bottleneck**:
  `corpus/conjectures/c12-translation-bottleneck.md`

C11 metabolizes Metric Mirage and Dashboard Theater into a feedback-loop claim:
measurement is not closed until it routes to a traceable response.

C12 metabolizes the Translation Bottleneck Law into the existing CIR return chain:
selected evidence -> injected context -> read/brief surface -> used footer ->
outcome row.

## Live readiness digest

An audit snapshot from `analyses/c11-measurement-action-closure/analyze.py`
reported:

- CIR signals: 267350, spanning 2026-03-22T02:03:14+00:00 to
  2026-06-19T07:12:26+00:00;
- measurement events: 187485;
- action proxy events: 15153;
- weak same-run temporal adjacency: 2492/7368 eligible measurements had a later
  action proxy within 24h;
- explicit closure relation edges: 0;
- relation types present: `cites`, `extends`, `supports`, `corrects`, `refines`,
  and `synthesizes`.

Verdict readiness fails because none of the current relation types encode
measurement-caused-action or action-responded-to-measurement.

An audit snapshot from `analyses/c12-translation-bottleneck/analyze.py` reported:

- run rows: 629, spanning 2026-05-17T03:02:48+00:00 to
  2026-06-19T06:38:43+00:00;
- post-footer-fix rows: 26;
- selected rows: 148;
- injected rows: 107;
- brief/read rows: 268;
- used rows: 0;
- selected-not-injected rows: 41;
- injected-not-used rows: 107;
- missing-footer-after-injection rows: 91;
- invalid-used rows: 10;
- unproven-used rows: 91.

Verdict readiness fails because the post-footer-fix C1b window is immature and C5
boundary classes are not yet available as controls.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Metric Mirage | **Admitted as C11** | Gives a measurable closure test for whether observations actually route to response. |
| Dashboard Theater | **C11 lineage** | Same anti-pattern at the interface layer: visibility without decision impact. |
| Translation Bottleneck Law | **Admitted as C12** | Maps cleanly to the selected/injected/read/used/outcome chain already present in run outcomes. |
| Canonical IDs and Source-of-Truth Architecture | **C12/C10 lineage** | Identity preservation is a translation precondition; unresolved identity remains handled by C10. |
| CIR canonical source | **Already metabolized** | Supports C7, C9, C11, and C12; not a standalone claim. |
| Structure debt, coherence debt, entropy, impedance, compounding | **Already metabolized** | Covered by C3, C5, C6, C8, and C10. |
| Meta-cognitive architectures | **Parked** | Outside the current Mentu operational instrument. |
| Wave, quantum, resonance, oscillation suites | **Parked** | Still metaphor-heavy without a better measurement surface than C5/C12. |
| Cultural absorption/status/fear-learning material | **Parked** | Plausible organizational theory, but current data would mostly measure workspace maturity and recipe mass. |

## Next push

Add two instrument edges:

- a CIR relation type or signal field for `measurement_responded_by` /
  `action_responds_to`;
- stable C5 boundary classes on run outcomes.

Those two additions turn C11 and C12 from readiness analyzers into verdict-capable
predictors.
