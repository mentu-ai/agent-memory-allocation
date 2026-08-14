# 2026-07-06 — Return-base-rate §2 re-derivation under reference verifier v2

*Instrument note. Discharges Obligation 2 of the protocol v2.2 impact audit
(`instruments/2026-07-06-protocol-v22-regime-boundary-and-impact.md`). This is an
**instrument correction, not a data change**: the ledger bytes are untouched; only the
chain-classification semantics changed (adjacency → canonical-ancestry). Touches no
frozen prediction, verdict, or result. Records the exact re-derivation behind the §2
edits in `paper/return-base-rate-paper.md` (draft v1.3).*

## Semantics change

The reference verifier this corpus uses — `protocol/tools/verify_ledger.py` in
`mentu-complete` — was reimplemented for protocol v2.2 (2026-07-05):

- **verifier v1** (line-adjacency semantics): a "break" was any row whose `prevHash`
  did not equal the *immediately preceding* row's hash. Under v1 the paper's ledger
  showed **109 breaks** (108 coinciding with workspace-context switches), argued
  *statistically* to be session boundaries.
- **verifier v2** (canonical-ancestry semantics, 2026-07-05): a break is a *missing
  ancestor* (a `prevHash` that resolves to no earlier row). Forks (a `prevHash`
  reused by concurrent appends) are typed **non-fatal** concurrency artifacts; the
  first hashed row is a genesis/import anchor, not a break. The fork root cause —
  concurrent appends under per-symlink append locks — is **fixed upstream**
  (`mentu-complete` `c013b64`). This converts the session-boundary reading from a
  statistical inference into a mechanical fact.

## Pinned bytes

No separate frozen copy of `ledger.jsonl` is stored in the repo; provenance is the
counts-based dataset digest embedded in the paper prose (12,129 signals / 11,106
hashed). The §2 numbers were computed on the **2026-06-28 cut** of the shared engine
ledger `mentu-complete/.mentu/ledger.jsonl` — exactly its **first 12,129 lines** (last
row `ts` = 2026-06-28T19:27:27Z), which contain exactly 11,106 hashed rows, reproducing
both frozen counts.

- Pinned prefix (first 12,129 lines) sha256: `d138a1cd06eb7d6a1a0b678683b63e7f4f028403befda3241f9f9cb7ea22e5b3`
- `mentu-complete` HEAD at re-derivation: `949a018`

## Command + verbatim output (read-only standalone verifier)

```
$ python3 mentu-complete/protocol/tools/verify_ledger.py --json \
      <(head -n 12129 mentu-complete/.mentu/ledger.jsonl)
{
  "path": "/dev/fd/11",
  "signals_total": 12129,
  "hashed": 11106,
  "unhashed": 1023,
  "unhashed_pre_cutover": 1023,
  "unhashed_post_cutover": 0,
  "content_ok": 11106,
  "content_bad": 0,
  "content_integrity": 1.0,
  "chain_canonical_ok": 11106,
  "chain_breaks": 0,
  "chain_forks": 62,
  "genesis_anchor": { "line": 5, "prevHash": "2de327a4cca7b771" },
  "cutover_present": false,
  "first_bad": [],
  "first_break": [],
  "ok": true
}
EXIT=0
```

For the record, the **full live ledger** (12,187 lines, grown past the cut, includes
the `lane_cutover` marker) verifies identically in kind: content_ok 11,164/11,164
(100%), chain_breaks 0, chain_forks 62, unhashed_post_cutover 0, ok true.

## Old → new classification (identical bytes)

| Quantity | verifier v1 (adjacency) | verifier v2 (canonical-ancestry) |
|---|---|---|
| Content-hash integrity | 11,106 / 11,106 (100%) | **11,106 / 11,106 (100%)** — unchanged |
| Chain "breaks" | 109 | **0 missing-ancestor breaks** |
| Typed concurrency forks | (not classified) | **62** (non-fatal; root cause fixed, `c013b64`) |
| Genesis/import anchor | (counted as a break) | **1** (line 5, `prevHash 2de327a4…` → prior file) |
| Unhashed hook-lane rows | 1,023 | 1,023 (0 post-cutover) |
| Per-workspace chain model | rejected at 3,436 breaks | historical (v1); retained as method detail |

## Frozen-number verdict

The load-bearing frozen number — **100% content integrity, 11,106/11,106** — is
**preserved** on the identical bytes. No number the paper presents as frozen changes;
escalation (a) is NOT triggered. The paper's integrity story strengthens (statistical →
mechanical) while its headline result is unchanged. Ledger bytes untouched.
