# CHANGES-v3.1 — the attribution correction

**Base.** `paper-v3.md`, byte-frozen at sha256
`e5715e78159febf5b0454a1274f57b7267aba70aa8ba52ab16287426919c62a0`, deposited
as DOI 10.5281/zenodo.21947917; v3.1 was created from its exact bytes and
`paper-v3.md` is untouched. The v3 deposit stands; it is superseded on the
related-work attribution corrected here.

**Driver.** A fourth external audit (2026-08-15), verified claim-by-claim
against sources before adoption. Every checked claim reproduced:
(1) Cochran's arXiv:2607.04576 includes an enforced read-only condition
whose tool whitelist blocked corpus-wide search attempts on 39 of 320
enforced runs — v3's assertions that "its agents always retain self-routing"
and that "nobody else's design can produce" the anatomy were false; his paper
also states the harness "recorded only aggregate usage" and names direct read
telemetry as "a target for replication," which is the ground the correction
claims. (2) Yuan et al. arXiv:2603.02473, cited as [12] but never
confronted, reports retrieval-stage dominance and write-strategy
insensitivity — convergent at the stage level with §4's and §6's directions.
(3) Cochran ran Opus 4.8 with an opposite-signed headline and predicts the
opposite capability interaction, making the model-tier confound live.

**What changed (claim sites).**

1. **Abstract**: the false universal ("in every published design the agent
   retains a way to route around the curated index") replaced with the
   instrument claim: published designs measure curated arms by aggregate
   outcome without per-read telemetry; the closest preregistered neighbour
   names that telemetry as a replication target; this paper supplies it.
2. **§1 positioning**: Cochran's enforced condition stated accurately
   (isolation by whitelist, 39/320 blocked); the differentiation moved from
   design to instrument.
3. **§3 ablation paragraph**: same correction at the design site; isolation
   necessary but not sufficient for attribution; isolation + per-question
   gold-file record is the design.
4. **§9 Cochran entry**: rewritten with the enforced arm, the telemetry
   quote, and the relation restated as "§4 is the measurement his
   replication target describes." **§9 unoccupied claim 1**: the instrument
   and its findings, not the isolation. **Claim 2**: the demonstrated
   reversal on C34's data, not the symmetric-rule principle, which is a
   correctness requirement.
5. **§9 Yuan entry added** (previously cited, never confronted): stage-level
   convergence conceded; substrate, instrument, anatomy, and
   pre-registration claimed.
6. **§6**: "the mirror is exact" withdrawn. Replaced with the evidential
   asymmetry stated plainly (408 committed run records + powered replication
   against a single tool-Read measurement on a no-longer-existing corpus
   with 18,780 unadjudicated non-tool mentions); heading and §1 contribution
   3 reworded from "mirror" to "write-side result"; Yuan's write-side
   convergence cited.
7. **§7**: the edit-channel diagnostic exhibit restored in compressed form
   from the v1 deposit — including its own under-recovery bound disclosed in
   the direction that flatters the correction — as the concrete content of
   "the gauge, not the policy, is the deliverable."
8. **§8**: the capability confound elevated to a named live paragraph
   (Opus 4.8 vs Haiku 4.5, opposite signs, Cochran's opposite-direction
   prediction quoted); Limits (b) upgraded from "follow-on" to "decisive
   registered successor."
9. **Front matter and §Data**: supersession chain gains `paper-v3.md` and
   this document; the deposit paragraph carries the new version DOI, the
   concept DOI, and both predecessors.

**What did not change.** No frozen conjecture, analyzer, results document,
or effect table was altered; no verdict re-adjudicated; every number
identical to v3. The figures are unchanged. The title is unchanged: the
anatomy claim survives the correction; the design-exclusivity claim does not,
and it was never in the title.

## Second-pass audit, same day, pre-deposit

A follow-up external audit of the corrected text found three residual sites,
each verified and fixed before the deposit was published (the reserved DOI
was unregistered at fix time; no published byte changed):

10. **Abstract**: the summary clause "the write path is never read back"
    overstated 2 of 157 on a registered population that excludes 296
    untestable files, and retained the withdrawn mirror cadence. Corrected
    to "the write path, on its registered population and measured channel,
    is rarely read back."
11. **§6 title**: "promotion does not produce returns" carried the same
    universal; retitled "promoted memory is rarely read back."
12. **§9 unoccupied claim 1**: "no published neighbor records, per question,
    whether the policy reached the gold document" moved the retired
    universal down a level — recall@k scores gold-reach for retrievers as a
    standard instrument, and Yuan et al. measure retrieval relevance at the
    retriever boundary. Rewritten to state the category difference: the
    unrecorded object is gold-reach for an agent's own read actions (what
    the policy opened), not for a retriever's returned set.
