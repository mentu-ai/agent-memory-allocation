# Core concepts and frameworks audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/`
- `Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/frameworks/`

No predecessor files were edited. Live data checks used direct reads of
`~/.mentu/cir.db` and `~/.mentu/training/cir-run-outcomes.jsonl`.

## Decision

Admit **C9 pattern crystallization utility**:
`corpus/conjectures/c9-pattern-crystallization-utility.md`.

The core-concepts/frameworks corpus repeats one loop often enough to deserve a real
test: signals become memory, repeated traces become patterns, and patterns feed future
orchestration. The live CIR proves the middle step exists: 6,214 certified
`crystallize/pattern` signals with source clusters. It does not yet prove utility.

The first readiness analyzer is in
`analyses/c9-pattern-crystallization-utility/analyze.py`. Its current expected state
is `INSTRUMENT INSUFFICIENT`: pattern creation and source linkage exist, but pattern
ids do not appear in run outcome injection/use arrays.

## Live readiness digest

- crystallized patterns: 6,214;
- source-linked patterns: 6,214/6,214;
- crystallization span: 2026-06-14 to 2026-06-19;
- pattern id intersections with run outcome arrays: 0;
- measured pattern-use runs: 0;
- verdict readiness: `INSTRUMENT INSUFFICIENT`.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| CIR pattern crystallization | **Admitted as C9** | Live CIR already creates pattern signals; next question is whether they get exposed and used. |
| Cognitive archaeology | **Folded into C9 / future instrument** | The transcript-as-event-ledger idea is strong, but current data does not expose validated transcript archaeology loops separately. |
| Return as intelligence | **Already C1/C1b** | Kept as core lineage, but the strong form was already tested/refuted as instrumented and fair-test C1b is live. |
| Epistemic handles | **Already C7** | Crawlio LACS gives the concrete handle substrate. |
| Cost/coherence/validation stack | **Already C8** | Guardrails vs dividend now has its own conjecture. |
| Epistemic triad | **Vocabulary, not claim** | Structure/memory/interaction remains an organizing frame. It is too definitional to test directly. |
| CI-OS/DCOS/epistemic computer | **Architecture lineage** | Most measurable residues are now split across C5-C9 rather than admitted as one giant platform claim. |
| Canvas/product thesis | **Not corpus science** | Useful product strategy, but it is not a measurable claim against the current instrument. |

## Next push

Wire pattern exposure into the selector/outcome path:

- record when a crystallized pattern is eligible for retrieval;
- record when a pattern is selected/injected;
- record when a pattern is cited/used in the footer channel;
- preserve the raw source-cluster ids so pattern exposure can be compared with
  raw-source exposure.

Until those fields exist, pattern crystallization is a substrate capability, not yet
a proven intelligence mechanism.
