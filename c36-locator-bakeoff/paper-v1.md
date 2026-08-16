---
title: "Finding More, Fusing Less: A Pre-Registered Locator Bake-off for AI Agents"
author: "Rashid Azarang — Independent Researcher — rashid@mentu.ai"
date: "2026-08-16 · doi:10.5281/zenodo.21969901"
fontsize: 11pt
geometry: margin=1.1in
linkcolor: blue
urlcolor: blue
---

**Companion report to** *Reading More, Finding Less: A Pre-Registered
Anatomy of Progressive Disclosure for AI Agents*
(doi:10.5281/zenodo.21960138). This study is registered as conjecture c36
in the same evidence program; predictions were frozen before any test
question existed, adjudication was mechanical, and the verdict is
**revised** — one prediction failed, and the failure retired a shipped
default. Both outcomes are reported at the same prominence.

# Abstract

The parent study attributed a curated disclosure policy's failure to
mis-routing by its index, but left the *winning* arm's own miss ceiling —
associative search failing to reach the gold document on 19.6–25% of
questions — unattributed. This companion tests the constructive converse:
whether that ceiling is reducible by ranked lexical retrieval, under
pre-registered predictions frozen before any test question existed. On the
parent's frozen 141-document public corpus, with a fresh 115-question set
generated under mechanically enforced gates, four locator arms ran behind
an identical k=8 tool contract. BM25 with per-language analyzers located
the gold document on 93.0% of questions against hardened exact search's
71.3% (+21.7 pp; McNemar p < 1e-5) — the miss ceiling was substantially a
ranking problem. The primary registered prediction passed: the fused
BM25+exact locator beat exact search by +13.9 pp (p = 0.00014) against a
+5.0 pp threshold. But a second frozen prediction — that reciprocal rank
fusion never costs localization against its own best leg — **failed**:
the fusion trailed BM25-alone by 7.8 pp (p = 0.0225), and the
pre-registered ablation rule retired the shipped fusion default
automatically. An off-the-shelf SQLite FTS5 control (89.6%) was not
statistically distinguishable from the custom implementation, assigning
the gain to BM25 as such rather than to our code. Downstream answer
accuracy moved +5.2 pp, decomposing into +7.5 pp from improved
localization partly offset by -2.3 pp of conditional accuracy: reaching
the right document remains the binding stage, replicating the parent's
anatomy on a third, blind question set. The findings were independently
validated by an isolated re-computation session that reproduced 21 of 22
claimed numbers exactly and confirmed the verdict from the raw records.
The full harness, question set, run records, and adjudicator ship for
re-running.

# 1. Why this study exists

The parent study [1] built a per-question localization instrument to show
*why* a curated index-then-hydrate policy loses to grep-then-read: the
index mis-routes, and answers issued without the gold document are almost
always wrong. That anatomy left its winner unexamined. Search reached the
gold document on only 80.4% (private corpus) and 75.0% (public corpus) of
seen-set questions, and nothing in either study decomposed the misses.
A post-hoc decomposition of the private-corpus misses suggested the
dominant profile was same-language morphology and ranking — matches
returned in file order, selection left to the policy — rather than
vocabulary mismatch.

That suggestion is the kind of claim this program does not leave as
interpretation. c36 registered it: if the ceiling is a ranking problem,
a ranked lexical locator should raise localization at bounded cost, and
the registration staked numeric predictions on arm-vs-arm deltas before
a single test question existed.

**Contributions.** (i) A pre-registered, mechanically adjudicated
comparison of locator compositions behind an identical agent tool
contract — a design that, per a live-verified literature sweep
(§6), no published empirical study occupies. (ii) The pre-registered
**retirement of a shipped default**: reciprocal rank fusion, deployed as
the framework's standard locator, failed its frozen never-costs
prediction and was removed by rule, not by judgment. (iii) A third
replication, on fresh blind questions, of the program's central anatomy:
accuracy conditional on reaching the gold document is stable (~50–54%)
across locator quality, so localization gains pass through to answers
nearly one-for-one. (iv) A question-generation protocol whose
constraints are enforced by mechanical gates rather than instructions —
and whose gate-rejection profile itself replicates the parent's finding
that instructed constraints are not constraints.

# 2. Registration

The conjecture (c36) and its registration were committed 2026-08-16 with
five frozen predictions and a mechanical verdict mapping, **before the
question set existed** — a deliberate tightening of the program's usual
order, so no prediction could be informed even by the questions' surface
difficulty. All predictions are arm-vs-arm deltas on one fresh
confirmatory set, making them robust to difficulty shifts between
question sets. Localization means the gold document appears in the arm's
k=8 hit list.

| # | Frozen prediction | Threshold |
|---|---|---|
| P1 | fused (L2) beats exact (L0) on localization | >= +5.0 pp |
| P2 | fused never trails BM25-alone (L1) | Δ >= 0 pp |
| P3 | Spanish-gold subset gain | >= +8.0 pp, adjudicated only at n >= 25 |
| P4 | cost bounds | build <= 15,000 ms; added query <= 500 ms |
| P5 | downstream accuracy does not regress | Δ >= 0 pp |

Verdict mapping, frozen: *refuted* if L2-L0 <= 0; *supported* if P1, P2,
P4 pass, P3 passes or is underpowered, and P5 passes; *revised*
otherwise. Interpretation cannot change the outcome.

# 3. Design

**Corpus.** The parent study's frozen public snapshot: 141 markdown
documents (1,162,998 bytes), every file hash re-verified against the
committed manifest at each run setup; any mismatch aborts.

**Arms.** Four locators behind one pinned contract (k=8 hits, snippets
<=240 chars, identical read primitives, same answerer, prompts, scoring
and adjudicator — the locator is the only variable):

- **L0** — hardened exact search (ripgrep-class term matching with
  deterministic heuristic ranking); the baseline, and the direct
  analogue of the parent's winning policy's search tool.
- **L1** — Okapi BM25 (k1=1.2, b=0.75) over an in-memory index with
  per-language (Spanish/English) Snowball analyzers and field boosts.
- **L2** — reciprocal rank fusion (k=60) of L0 and L1's rank lists;
  the framework's shipped default and the primary registered arm.
- **L4** — SQLite FTS5 (`porter unicode61`, BM25 ranking) behind the
  same contract: an off-the-shelf external control that separates "BM25
  the idea" from our implementation. Descriptive only; staked by no
  prediction.

A fifth registered arm (cross-lingual dense retrieval) was not built or
run; its pre-registered activation trigger had not fired.

**Questions.** A fresh set, because the seen sets' results are published
and a prediction frozen against a known baseline is not blind. The
generator reused the parent study's frozen prompt and model verbatim, but
every constraint became a mechanical acceptance gate with
reject-and-regenerate (max 3 attempts per document): answer verbatim in
the body; **3–15 words counted by the validator, not instructed to the
model**; not recoverable from the question itself; present in at most two
corpus documents; not degenerate. Of 141 documents, 115 yielded an
accepted question; 26 exhausted their attempts and are excluded and
listed. The gates fired 227 times (length 75, multi-document 59, verbatim
46, degenerate 45, in-question 2) — the parent measured a 30% violation
rate when the same length constraint was merely instructed, and this
profile is that finding reproduced from the enforcement side. The
salted-split rule assigned all 115 to the confirmatory set (the
registered 120+10 could not be met from the yield; the shortfall and its
disposition were recorded before any arm ran, and no rule was altered
after the yield was known).

**Downstream policy (P5).** One locate per question per arm; the answerer
(a small fixed model) receives the full bodies of the arm's top-8
documents in rank order (truncated at 6,000 chars with visible markers)
and answers in a fixed format. One model call per question per arm — a
bounded hydrate-all policy that makes the locator the only varying input.
Consequence, stated plainly: absolute accuracies here are not comparable
to the parent's agentic-loop numbers; only the L2-L0 delta is
interpreted, which is all P5 stakes.

**Scoring.** A word-boundary containment rule adjudicates (closing a
substring false-positive class the parent disclosed); the parent's exact
rule is computed alongside descriptively. The two agree within 0.9 pp
everywhere; no outcome depends on the choice.

# 4. Results

## 4.1 Localization (n = 115, gold in  top-k)

| Arm | @8 | @3 | @1 |
|---|---|---|---|
| L0 exact | 71.3% | 60.9% | 43.5% |
| **L1 BM25** | **93.0%** | **84.3%** | **65.2%** |
| L2 fused | 85.2% | 73.0% | 53.9% |
| L4 FTS5 control | 89.6% | 76.5% | 55.7% |

Paired-design statistics (exact McNemar, computed in independent
validation and adopted here as descriptive): L1 vs L0, 28-vs-3 discordant
pairs, p < 1e-5. L2 vs L0, 17-vs-1, p = 0.00014. L2 vs L1, 2-vs-11,
p = 0.0225.

## 4.2 Adjudication

| # | Measured | Outcome |
|---|---|---|
| P1 | +13.9 pp (85.2 vs 71.3) | **pass** (threshold +5.0) |
| P2 | -7.8 pp (85.2 vs 93.0) | **fail** |
| P3 | subset n = 0 | underpowered; not adjudicated |
| P4 | 193.7 ms build; +147.4 ms/query (difference of per-arm medians) | **pass** (bounds 15,000 / 500) |
| P5 | +5.2 pp (43.5 vs 38.3) | **pass** |

**Verdict: revised** — the primary prediction passed and an adjudicated
secondary failed. The verdict was computed by the frozen analyzer and
independently re-derived from the raw records (§7).

## 4.3 The anatomy, a third time

Accuracy conditional on reaching the gold document: 53.7% (L0, n=82) and
50.0% (L2, n=98). Accuracy otherwise: 0.0% (n=33) and 5.9% (n=17). The
+5.2 pp downstream gain decomposes into +7.5 pp from localization,
partly offset by -2.3 pp of conditional accuracy. Localization is where
the outcome is decided; comprehension of a reached document is roughly
constant across locator quality. This is the parent's central mechanism
reproduced on a blind question set with a different policy shape.

# 5. The fusion retirement

The interesting failure. RRF was adopted on the standard warrant —
fusion "consistently yields better results than any individual
system" [2] — and the registration staked exactly that: P2, fusion never
costs localization against its own best leg. It cost 7.8 points.

The literature, swept and live-verified after adjudication, shows the
*phenomenon* is documented: RRF is parameter-sensitive and beatable by
learned or calibrated alternatives [3]; a "weakest link" path can drag a
hybrid blend below its best component [4]; and an industry deployment
found fusion's recall gains neutralized under fixed depth and latency
contracts [5]. What those studies do not contain is this design: a
*prior, frozen* prediction that fusion would not cost localization,
mechanically adjudicated, with the shipped default retired by rule on
the result. c36's claim is the pre-registered retirement, not the
discovery that fusion can fail.

Mechanistically, the configuration matches [4]'s weakest-link condition
in its most extreme form: one leg (BM25) is a calibrated ranking; the
other (exact) returns matches in file order with heuristic scoring —
closer to an unranked set than a ranking. RRF assumes rank positions
carry comparable information in both lists; here the exact leg's
positions are substantially noise, and fusing noise into a good ranking
degrades it. Two concessions bind: the RRF constant was fixed at k=60
and never swept, so parameter sensitivity [3] is a live confound; and no
published work isolates the specific ranked-with-unranked fusion
condition, so the mechanism reading, while consistent with the data,
is not itself adjudicated.

The external control disciplines the success story the same way the
registry disciplined the failure: FTS5 at 89.6% is not statistically
distinguishable from our 93.0% implementation on this n. BM25 as such
carries the gain; the custom per-language implementation is not yet shown
to add anything. That is the honest sentence, and it is cheaper to write
now than to retract later.

# 6. Related work

Positions here follow a live-verification discipline: every citation was
opened at source during an isolated literature session, one load-bearing
sentence quoted verbatim and checked, before entering this section.
Author lists are omitted where not independently verified; identifiers
are the citation.

**Fusion.** [2] (SIGIR 2009) is the confronted warrant. [3] (TOIS 2023)
pre-empts "RRF can lose" and supplies the parameter-sensitivity
concession. [4] (arXiv:2508.01405) names the weakest-link mechanism
across 11 datasets. [5] (arXiv:2603.02153) is the nearest production
analogue of the failure.

**Lexical retrieval for agents.** [6] (arXiv:2605.15184) and [7]
(arXiv:2608.01507) bracket the grep-vs-retrieval question on agent
substrates, the latter concluding for indexable read-only corpora that
retrieval is "the stronger and cheaper option" — c36's direction on a
different substrate. [8] (arXiv:2608.05886) bounds our finding sharply:
BM25 retrieval *below a precision threshold degrades* a downstream
agent — so +21.7 pp is a localization-recall result, not a general
"BM25 helps agents" claim. [12] (BEIR, NeurIPS 2021) grounds BM25's
robustness and explains why the FTS5 control lands where it does.

**Localization binds downstream.** [10] (arXiv:2503.09089) and [11]
(ToolRet, ACL 2025) establish the reach-to-outcome chain on code and
tool substrates; our §4.3 is a third convergence, contributed as a
decomposition rather than a discovery. [14] (RAGGED, ICML 2025) is the
strongest counter-framing — reader noise-robustness, not retrieval, as
the key determinant of RAG stability. The tension is resolved by design
class: RAGGED's readers integrate many retrieved passages under noise;
our policy hydrates a small fixed set, so when the gold document is
absent nothing downstream can recover (0–6% accuracy), which is
precisely the regime where localization binds. Outside that regime
RAGGED's assignment may well dominate; we claim nothing there.

**Method.** [9] (arXiv:2606.22417) is prior art on single-variable
within-harness retrieval ablation with a localization-to-resolution
chain; c36's methodological addition over it is the frozen prior
prediction and the rule-bound retirement. [13] (arXiv:2606.11217, ICML
2026 position) catalogs the researcher degrees of freedom this design
freezes — and the sweep found *no empirical pre-registered
retrieval-composition study for agents*, which is the gap this report
occupies.

# 7. Independent validation

Before this report was written, the frozen artifacts and complete raw
records were handed to an isolated validation session (no web, no
repository access, attachments only) instructed to distrust every stated
number and recompute from records. It reproduced 21 of 22 claimed
numbers exactly — the exception being a ±0.1–0.8 ms estimator ambiguity
in one latency figure against a 500 ms bound — applied the frozen verdict
mapping to its own values, and confirmed **revised** follows. Its
findings were adjudicated in a dated disposition and are incorporated
above: the McNemar statistics (§4.1), the FTS5 non-significance (§5),
the P5 decomposition (§4.3), and the limitations below. A parallel
isolated session performed the literature verification of §6 (13 works,
all live-verified, zero failures).

The validation's declared boundaries are part of the record: it could
not verify the corpus snapshot hashes, the locator build, model
identities, or commit ordering from the attachments alone. The public
bundle exists to close those boundaries: corpus manifest, pinned
harness, run records, and adjudicator ship for external re-running.

# 8. Limitations

1. **One corpus, one harness family, one contract.** All claims are
   scoped to a frontmattered operational documentation corpus behind a
   k=8 contract; [6] shows harness and tool-presentation effects can be
   large independently of the retriever.
2. **The registered measure set was not fully delivered.** Marginal
   tokens were recorded only as prompt characters; index peak RSS was
   not captured in the metrics file; the cross-language subset
   measurement is vacuously empty on this corpus. None touches an
   adjudicated quantity; all were disclosed by the independent
   validation, not by the authors — recorded as such.
3. **P3 (the Spanish-morphology mechanism) is untested**: the public
   corpus carries no Spanish-tagged documents, the registered power
   guard fired, and the mechanism claim awaits a successor on the
   private estate corpus where the subset exists.
4. **RRF k=60 was never swept** (conceded to [3]); the retirement is of
   this configuration on this corpus class, not of fusion in general.
5. **Two accepted questions share an identical gold string** across
   different documents (symmetric across arms; worst-case 2/115 on P5).
6. **An adjudicator invocation occurred while records were incomplete**;
   its output was discarded and the final adjudication ran on complete,
   verified-unique records — but the incident is not falsifiable from
   the bundle alone, and successor designs must make the analyzer assert
   record completeness before computing.
7. **The absolute P5 accuracies are policy-bound** (hydrate-all) and not
   comparable to the parent's agentic-loop numbers.

# 9. What this changes, and what comes next

The framework this program instruments shipped `fused` as its default
locator. That default is now evidence-contradicted on this corpus class
and retires per its own pre-registered ablation registry; the redesign
(BM25-primary, with the exact leg as a fallback or rank-aware signal) is
a dated design decision outside this study, and any performance claim
for it requires a fresh registration. Registered successors: the fusion
redesign; the Spanish-mechanism test where its subset exists; and
harness rules adopted from this study's own defects — gold-string
uniqueness as a generation gate, rank lists recorded to fusion depth,
completeness assertions in adjudicators.

The parent study showed an authored index mis-routing an agent that
could have searched. This study shows the search it should have used
was itself leaving a fifth of the corpus unreachable — and that most of
that gap closes with ranking, while the obvious way to *combine*
retrievers made things worse and was caught only because the claim was
staked before the data existed. The gauge, again, is the deliverable.

# Availability

The replication bundle (doi:10.5281/zenodo.21969901) contains the frozen
harness and analyzers, the gated question set with its generation log and
candidate cache, all run records (localization and downstream, both
arms), the adjudication output, the corpus manifest, the registration
and correction lineage, and the two validation session prompts, returns,
and disposition. The parent corpus snapshot is published with the parent
deposit (doi:10.5281/zenodo.21960138). GitHub mirror:
`github.com/mentu-ai/agent-memory-allocation` (`c36-locator-bakeoff/`).

# References

Identifiers were live-verified 2026-08-16; author lists are given only
where independently verified.

1. Azarang, R. *Reading More, Finding Less: A Pre-Registered Anatomy of
   Progressive Disclosure for AI Agents.* 2026. doi:10.5281/zenodo.21960138.
2. Cormack, G.V., Clarke, C.L.A., Büttcher, S. *Reciprocal Rank Fusion
   outperforms Condorcet and individual Rank Learning Methods.* SIGIR
   2009, 758–759. doi:10.1145/1571941.1572114.
3. *An Analysis of Fusion Functions for Hybrid Retrieval.* ACM TOIS,
   2023. doi:10.1145/3596512; arXiv:2210.11934.
4. *Balancing the Blend: An Experimental Analysis of Trade-offs in
   Hybrid Search.* 2025. arXiv:2508.01405.
5. *Scaling Retrieval Augmented Generation with RAG Fusion: Lessons from
   an Industry Deployment.* 2026. arXiv:2603.02153.
6. *Is Grep All You Need? How Agent Harnesses Reshape Agentic Search.*
   2026. arXiv:2605.15184.
7. *Deep Agentic Search for Repository-Level Code Question Answering: An
   Empirical Study.* 2026. arXiv:2608.01507.
8. *CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents.*
   2026. arXiv:2608.05886.
9. *Code Isn't Memory: A Structural Codebase Index Inside a Coding
   Agent.* 2026. arXiv:2606.22417.
10. *LocAgent: Graph-Guided LLM Agents for Code Localization.* 2025.
    arXiv:2503.09089.
11. *Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for
    Large Language Models.* ACL 2025. arXiv:2503.01763.
12. *BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of
    Information Retrieval Models.* NeurIPS 2021 Datasets and Benchmarks.
    arXiv:2104.08663.
13. *Preregistration for Experiments with AI Agents.* ICML 2026 position
    paper. arXiv:2606.11217.
14. *RAGGED: Towards Informed Design of Scalable and Stable RAG
    Systems.* ICML 2025. arXiv:2403.09040.
