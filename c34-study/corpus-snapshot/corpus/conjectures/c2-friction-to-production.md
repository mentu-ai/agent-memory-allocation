---
id: c2
name: friction-to-production
status: operationalized
lineage:
  - epistemic-main/canon/foundational-documents/the-law-of-epistemic-acceleration.md
verdict: null
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-07-13
  gate: "CHECKED 2026-07-13 (analyses/c2-friction-to-production/gate_check.py, read-only, availability-only): span 8.1/8 weeks MET; inclusion bar FAILED 1/10 under all three admissible readings (strict recipe family 1/10, coarse project family 1/10, workspace-via-run_id 1/10) -> GATE CLOSED, TEST NOT ATTEMPTED; conjecture waits (frozen rule: no bar-lowering after seeing data). Substrate finding: strata are ephemeral projects — 219 strict families, ~90% alive exactly one ISO week; the only >=5-mature-week stratum is the infra zombie ane-fortress (7 wks); best workspace 'unknown' (8 wks). Any rev.3 re-operationalization is a new frozen revision (owner's call). Also gates C6."
  watch: [packets/2026-06-14.md, packets/2026-06-16.md, packets/2026-06-28.md, packets/2026-06-29.md, packets/2026-06-30.md, packets/2026-07-13.md]
---

# C2 — Friction-to-production

## Claim

The ratio of friction to production in a workspace predicts whether its work compounds
or stalls: rising commitment latency and a growing fraction of stuck commitments
precede falling throughput.

## Origin

The 2025 corpus proposed the friction-to-production ratio with a specific threshold
(F/P ≤ 0.5) marking the transition to self-sustaining growth. The threshold was never
derived; the directional claim is retained, the constant is dropped. If a real
threshold exists, it will be estimated from data.

## Operationalization

**Datasets**:
- `~/.mentu/commitments/` (11,889 JSON files): `created_at`, `updated_at`, `state`
  (claimed/closed/approved), `tags` (incl. `sequence:<name>`), `actor`. Exclude
  `.tmp` files.
- `~/.mentu/audit.jsonl`: per-call `durationMs` as an effort proxy per period.

**Measures** (per workspace/sequence tag, per week):
- **Friction**: median open→close latency of completed commitments; *stall fraction* =
  share of commitments still `claimed` after 7 days.
- **Production**: closes+approvals per week.
- **Test**: does friction at week *t* predict production at weeks *t+1..t+2*
  (within-workspace, lagged correlation)? Do stalled workspaces (top-quartile stall
  fraction) show declining close rates relative to low-friction workspaces?

## Predictions (stated 2026-06-10, before analysis)

- **P1**: Stall fraction correlates negatively with subsequent weekly throughput.
- **P2**: Workspaces with rising median latency show falling close rates over the
  following weeks; low-latency workspaces hold or grow.
- **P3**: The relationship is monotonic but not necessarily thresholded — we do not
  predict a sharp 0.5-style cliff.

## Falsification criteria

- No lagged association between friction measures and throughput across workspaces
  (|r| small, sign unstable) → **refuted**.
- Association exists but is fully explained by workspace age or commitment volume →
  **revised**.

## Known limitations

Commitment titles like "Step: x" indicate much of the volume is machine-generated
sequence steps; human-initiated and machine-generated commitments must be segmented
(via `actor` and tags) before interpreting friction as anything like cognitive effort.

## First test attempt (2026-06-10): INCONCLUSIVE — instrument mismatch

The registered source proved stale and the substituted lifecycle surface measures
machine pacing, not friction: closes are near-instant (median 2.4 min), stall
conflates abandonment, 65% of commitments are workspace-unattributed, and only 3
strata qualified. The limitation paragraph above turned out to be the headline.
Full record: `results/2026-06-10-c2-friction-to-production.md`.

## Revised operationalization (rev. 2, frozen 2026-06-10 before any rev. 2 analysis)

1. **Actors**: exclude `workflow` auto-steps; keep human- and agent-initiated
   commitments only (`actor` field segmentation).
2. **Production surface**: weekly run successes per recipe family from
   `cir-run-outcomes.jsonl` (post-regime records carry `randomization_arm`;
   production counts use all runs regardless of arm).
3. **Friction surface**: per workspace/recipe-week — `audit.jsonl` per-method
   `durationMs` medians and error rates, plus genuinely-open commitment age
   from `cir.db` lifecycle events.
4. **Inclusion bar**: ≥10 strata with ≥5 mature weeks each, or the test is not
   attempted.

**Predictions (re-frozen, same direction)**: P1 — friction measures at week *t*
correlate negatively with production at *t+1*; P2 — rising friction trends
precede falling production; P3 — monotonic, no assumed threshold.

**Accrual gate**: `cir-run-outcomes.jsonl` currently spans ~3.5 weeks — too thin
for weekly lag analysis. Run rev. 2 when it spans **≥8 weeks** (~mid-July 2026)
AND the inclusion bar is met. If the bar still fails, the conjecture waits; no
lowering the bar after seeing data.
