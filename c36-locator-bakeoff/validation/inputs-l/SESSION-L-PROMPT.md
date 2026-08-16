# CONTEXT-L — c36 literature session (attach with inputs-l/, paste block executes this)

You are an independent literature verifier in a Claude Science session with
web access. Your task is to position the attached c36 result against the
published literature so the companion paper claims exactly what is new and
concedes exactly what is not. Read the three attached documents first; do
not consult any unlisted local file.

The result to position: on a 141-document operational corpus with
pre-registered predictions, (i) BM25 ranked retrieval beat hardened exact
search on gold-document localization by +21.7 pp (93.0% vs 71.3% @8);
(ii) reciprocal rank fusion of the two DEGRADED the better leg by 7.8 pp,
failing its pre-registered prediction and retiring the fusion default;
(iii) an off-the-shelf SQLite FTS5 control landed between them (89.6%);
(iv) downstream answer accuracy moved +5.2 pp, fully accounted for by
localization (accuracy conditional on reaching the gold document was
~50–54% in both arms, ~0–6% otherwise).

## Sweep, with verification discipline

For each of these questions find the strongest published work (arXiv/ACL/
SIGIR/TREC etc.), verify every citation LIVE (open the abstract page; quote
one load-bearing sentence verbatim and say where it is), and mark each work
as OCCUPIES (does what c36 does), ADJACENT (same phenomenon, different
substrate/design), or CONTRADICTS (evidence against c36's findings):

1. When does rank fusion (RRF specifically) underperform its best single
   retriever? Known failure conditions (leg quality asymmetry, unranked
   legs, candidate-pool overlap)?
2. BM25 vs exact/grep-style matching for AGENT document/tool retrieval
   specifically (agentic search, tool-use corpora, code/doc navigation).
3. Pre-registered or ablation-disciplined evaluations of retrieval
   composition for LLM agents.
4. Localization/reach as the binding stage for downstream answer accuracy
   (evidence for or against).

A citation that does not verify live is reported as failed-verification and
never enters the bibliography. Do not pad: five verified works beat fifteen
unverified ones.

## Output contract (your final message, nothing after it)

```json
{
  "protocol": "operon-c36-v1/session-l",
  "works": [
    {"id": "<arXiv id or DOI>", "title": "...", "venue_year": "...",
     "verified": true, "verbatim_quote": "...", "quote_location": "...",
     "relation": "OCCUPIES|ADJACENT|CONTRADICTS",
     "bearing_on_c36": "<one sentence>"}
  ],
  "novelty_assessment": {
    "finding_i_bm25_beats_exact": "<occupied/novel-on-substrate/...>",
    "finding_ii_fusion_degrades": "<...>",
    "finding_iv_localization_binds": "<...>"
  },
  "failed_verifications": ["..."],
  "recommended_confrontations": ["<works the paper MUST cite and engage>"]
}
```
