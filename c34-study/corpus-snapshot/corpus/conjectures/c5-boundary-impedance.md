---
id: c5
name: boundary-impedance
status: operationalized
lineage:
  - epistemic-main/canon/law-suites/laws-of-epistemic-impedance-and-transmission.md
verdict: null
---

# C5 — Boundary impedance

## Claim

Knowledge transfers lossily across boundaries: a signal is less likely to be reused —
and arrives with less trust — when it crosses a workspace or device boundary than when
it is consumed where it originated.

## Origin

The 2025 corpus's impedance/transmission laws were among its strongest analogies
(boundaries reflect part of what hits them). The reflection/transmission coefficients
are dropped until they can be computed from data; the attenuation claim is retained.

## Operationalization

**Datasets**:
- `~/.mentu/cir.db`: `signals` (origin `workspace`), reuse linkage via
  `used_signal_ids` in run outcomes and `relations` (citing signal's workspace vs
  cited signal's workspace).
- Root + nested `ledger.jsonl`: `workspace` field on every op; 23 known workspaces.
- api-server Neon Postgres `cir_signals` (`device_id`, `asserted_confidence`): same
  question across devices, where reachable; otherwise scoped to local workspaces.

**Measures**:
- Within-workspace vs cross-workspace reuse rate: of signals used by runs/citations,
  what fraction crossed a boundary, normalized by opportunity (availability of
  cross-workspace signals to the consumer)?
- Confidence at point of use for crossed vs native signals.

## Predictions (stated 2026-06-10, before analysis)

- **P1**: Reuse rate is materially higher within-workspace than cross-workspace after
  normalizing for availability.
- **P2**: Crossed signals carry lower effective confidence at use than native ones.

## Falsification criteria

- Cross-workspace reuse matches or exceeds within-workspace reuse after normalization
  → **refuted** (would suggest the CIR substrate has already dissolved the boundary —
  itself a major result for the substrate thesis).

## Known limitations

Normalization is the hard part: most signals are never candidates for cross-boundary
use. The analysis must define the opportunity set carefully (e.g., semantic-similarity
matched pairs) or the result is selection bias dressed as impedance.

## Normalization design

The current design is recorded in
`instruments/2026-06-19-c5-normalization-design.md`. It defines two non-pooled
surfaces: exposure-conditional run reuse, and availability-matched citation reuse.
Future analysis code must pass the pure guardrail tests in
`analyses/c5-boundary-impedance/` before any C5 verdict is adjudicated.
