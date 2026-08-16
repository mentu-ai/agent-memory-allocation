# ORDER-PROOF — the commit chain, exported for bundle-only readers

Every pre-registered claim in this study rests on an ordering: predictions
and thresholds committed before the data that adjudicates them existed. The
repository's git history is the authority for that ordering; this file is a
verbatim export of the relevant commits (hash, author timestamp, subject) so
a reader holding only the deposit can check the chain without repository
access. Timestamps are author times with their UTC offset as recorded. The
first policy-run provider call is `2026-08-14T01:07:02Z` (call ledger seq
297, bucket `smoke`; the entries before it are the reality probe, question
generation and digest authoring); every registration, correction v2–v4,
harness, adjudicator and question-freeze commit below precedes it. Correction v5 (2026-08-14) is
post-run by design: it redacts a client-token list in bundle copies only and
changes no threshold, prediction, scoring rule or verdict.

## Program and C29 chain (cited in the paper's availability section)

    4b86195  2026-07-18T22:04:39-06:00  M0: register agent-memory-allocation program — BUILD doc, transcript instrument, C26–C29 pre-registrations (predictions frozen before any probe), board rows
    5572eba  2026-07-19T10:26:08-06:00  M3 gate 1: C29 harness — DESIGN (layers realization recorded), pinned models, generator/runner/adjudicator, committed before question generation
    5d63e0a  2026-07-19T11:22:22-06:00  M3 gate 2: C29 question set + index FROZEN before any policy run
    dc5bfca  2026-07-19T22:03:51-06:00  M3 verdict: C29 SUPPORTED — grep-then-read beats layered disclosure on every measured axis (72.5% vs 47.1%; P1-P4 pass at full coverage)

## C34 chain (registration → instrument → freeze → runs → verdict)

    cb73654  2026-08-12T19:17:20-06:00  register C34: public curation-vs-search replication at power
    b42fe73  2026-08-13T09:48:29-06:00  registration: C34 correction v2 — pin the five treatment prompts verbatim, exempt README.md, snapshot from cb73654 tree, close M1 findings F1-F12
    129f638  2026-08-13T13:58:34-06:00  registration: C34 correction v3 — fix G1/G2 factual errors, name D-8/D-9, record dead branches as verified preconditions
    c219742  2026-08-13T14:25:31-06:00  C34 M2: rule R, self-contained, enumerating the pinned cb73654 tree
    b3d49f8  2026-08-13T14:25:46-06:00  C34 M2: harness — prompts frozen byte-verbatim, symmetric hydration, budget ledger
    1e61ec6  2026-08-13T14:26:02-06:00  C34 M2: frozen adjudicator, smoke gate, and every verdict branch under test
    c1e3544  2026-08-13T14:27:48-06:00  C34 M2: instrument note — what was built, what is absent, and the M3-M7 commands
    9f4ca58  2026-08-13T15:31:38-06:00  C34: close M2 verification findings G-M2-1,2,3,5,6 before the corpus snapshot
    6e933ec  2026-08-13T15:33:25-06:00  C34 M3: corpus snapshot — 141 files, 1,162,998 bytes, committed bytes not a manifest
    97b6b6f  2026-08-13T15:36:01-06:00  C34 M3: note + the post-snapshot test correction
    727f293  2026-08-13T18:03:32-06:00  C34 M4: seal the order gate — probe passed, 141/141 questions validated (13 regens, 0 drops, branch=full), index authored 141/141, 297/387 authorized calls
    bfb4919  2026-08-13T18:13:34-06:00  registration: C34 correction v4 — degeneracy flag, index-leak and provenance annotations, non-adjudicating sensitivity table
    9315a22  2026-08-13T18:22:19-06:00  registration: C34 correction v4 erratum 1 — three factual corrections from the v4 verification
    fd91518  2026-08-13T18:28:42-06:00  C34: implement correction v4's annotations and non-adjudicating sensitivity rows
    4d9ac14  2026-08-13T19:10:58-06:00  C34 M5: seal the excluded smoke — 30/30 records, ledger 327/950 (smoke exactly 30), audit passed with zero findings, replays byte-identical
    6185329  2026-08-13T19:11:44-06:00  C34 M5 correction: commit the runner-written canonical smoke audit (2026-08-13, sha 09deca63) and remove the operator's mis-dated duplicate — the leak gate caught the duplication; the two files were byte-identical
    7b95e02  2026-08-13T19:46:29-06:00  C34 M6: seal the confirmatory — 360/360 records, zero errors, zero retries, ledger 687/950 (confirmatory exactly 360, reserve untouched)
    c1627af  2026-08-14T07:26:56-06:00  results: seal C34 verdict REVISED (headroom_not_established_on_marginal_tokens; P1 +12.5pp, P3' and P5 replicated, sensitivity rows flip nothing; replays byte-identical)
    c0924db  2026-08-14T07:36:34-06:00  C34: close the queued findings S-1, S-2, S-3, G-M3-1 and the edit-script rule
    8e77eb2  2026-08-14T07:39:20-06:00  C34 M8: bundle builder — and the release gate it FAILED
    25c4e90  2026-08-14T08:44:16-06:00  C34 M8: correction v5 (bundle-only redaction) and the bundle that now passes its own gate

## How to verify

Inside the repository: `git log --format="%h %aI %s" -- analyses/c34-public-curation-vs-search-replication instruments/ results/` reproduces this listing; `git show <hash>` inspects any commit. From the bundle alone, the chain above is a claim by export; its cross-checks are the call ledger's hash chain (`call-ledger.jsonl`, 687 entries, reservation-before-dispatch on all 390 records), the salted split that regenerates only from the committed pre-run salts, and the question set's frozen content hashes.
