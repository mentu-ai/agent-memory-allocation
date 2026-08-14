# 2026-07-08 — CIR exhaust purge + age-only exhaust reaping (regime note)

*Instrument note (same class as `2026-07-06-protocol-v22-regime-boundary-and-impact.md`).
Declares a substrate-level co-intervention on the shared CIR database that several
open conjectures read through. Touches no frozen prediction, verdict, or result.*

## What happened upstream

The 2026-06-10 failure mode ("temporal_result at 74% of the substrate") recurred
under a new emitter. `handle_snapshot` — the C7 returnability telemetry introduced
2026-06-19 (see `2026-06-19-general-epistemic-telemetry-handles.md`) — was never
added to any of the three exhaust defenses (ingest digest list, embedding
eligibility, trust half-life). By 2026-07-08 the substrate held **468,163 signals,
356,500 of them (76%) machine exhaust** (`handle_snapshot` 158,722 at ~8,300/day;
`temporal_result` 197,778), all carrying 384-dim embeddings (the embedding
eligibility gate of engine commit `9862051`, 2026-06-08, was bypassed by stale
deployed binaries), for a 2.2 GB `cir.db`.

The nightly reaper (`cir compact --older-than 90 --below-confidence 0.2`) could
never touch this population: exhaust enters at default confidence ≥ 0.2, and only
2 of 356k rows matched both criteria. Growth was unbounded by construction.

Operationally this stalled recipe runs: the runtime evidence policy's recursive
source-chain eligibility check re-prepares a very large generated SQL statement
per provenance node (`CIRRuntimeEvidencePolicy.sourceChainEligibleSignalIds` →
`CIRStore.queryUsageDebt`; CPU-sampled live on 2026-07-08 — time dominated by
SQLite *parse*, not execution, plus cross-run lock contention), which on the
bloated substrate produced 10+ minute milestone transitions (the caw-w0 hang)
and a 3+ hour dash-test grind.

## The intervention (mentu-complete, deployed 2026-07-08)

1. **`handle_snapshot` gains the 7-day trust half-life** at ingest
   (`CIRIngestPolicy.defaultHalfLifeDays`), same class as `temporal_result`.
2. **`cir compact` gains age-only exhaust pruning**: kinds
   `handle_snapshot`, `temporal_result` (default) are deleted at age > 14 days
   *regardless of confidence*. Signals cited in any derived signal's
   `source_ids` are exempt — provenance chains stay resolvable. Runs in the
   already-seeded nightly temporal with no temporal changes.
3. **Ineligible-embedding sweep**: embeddings (and vec0 rows across all
   registered spaces) are deleted for every signal kind outside
   `CIRIngestPolicy.embeddableKinds`, restoring the 2026-06-08 gate's intended
   state. The vec prune now covers versioned spaces
   (`embeddings_vec__all_minilm_l6_v2_384` etc.), which earlier prunes leaked.
4. **One-time purge** of the accumulated exhaust from
   `~/mentu-home/cir.db` (counts below), followed by VACUUM.
   Full pre-purge snapshot: `~/mentu-home/cir.db.pre-exhaust-purge-20260708.bak`.

## Purge accounting (executed 2026-07-08, engine commit `7a3f85a`)

- Exhaust signals deleted: **233,918** (58,754 handle_snapshot + 175,164
  temporal_result; >14d, uncited), in 69s against the live db.
- Stale signals deleted: **858** — the >90d backlog the nightly prune had been
  unable to touch (its cascade missed `evaluation_gate.correction_id`, so any
  run collecting a referenced correction died on the FK; fixed in `7a3f85a`).
- Exhaust rows retained because cited by derived signals: 31,965
  handle_snapshot + 5,585 temporal_result (provenance exemption). All 2,471
  derived signals verified intact post-purge on the rehearsal clone.
- Embeddings removed: ~234k via prune cascade + **184,209** via the
  ineligible-kind sweep (rehearsal clone: 468,154 → 49,442 embeddings).
- cir.db file size: 2.2 GB → ~0.9 GB after VACUUM (rehearsal: 2213.6 →
  895.9 MB; remaining bulk is <14d exhaust that rolls off nightly).

## Impact on conjectures — never pool across 2026-07-08

- **C7 (handle returnability)**: uncited `handle_snapshot` rows now live ≤ 14
  days and decay with a 7-day half-life. Returnability windows longer than 14
  days become unmeasurable for uncited handles. Cited (consolidated) handles
  persist. Any C7 rate computed over a window spanning this date mixes two
  retention regimes.
- **C1b (consumption channel)**: mechanically unaffected — the footer and
  `context_consumed` channels read per-run signals well inside 14 days. But
  brief *composition* changes (exhaust no longer competes in retrieval and the
  ANN index shrank ~75%), so use-when-offered rates before/after this date are
  not comparable arms.
- **C22 / C25 and any retrieval-mediated measurement**: the vec index and
  candidate pools shrink drastically; ranking dynamics change. Same rule:
  treat 2026-07-08 as a boundary.
- **Run-latency-sensitive observations**: milestone transition times before
  this date include the pathological CIR grind; after, they should not.

## Marker

`instruments/2026-07-08-cir-exhaust-purge-marker.json`
