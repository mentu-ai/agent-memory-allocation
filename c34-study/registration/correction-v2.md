# C34 registration correction v2 (2026-08-13)

**Scope:** closes the findings of the M1 non-author verification of the C34
registration (cb73654). Authored by the orchestrating session (the registration
author was session-limited); to be re-verified by the M1 verifier before M2.
Every prior registration byte is preserved; where this document and the
2026-08-12 registration conflict, this document governs. Nothing here changes
a threshold, a floor, a model pin, or the verdict map.

## C-1 (closes F1, THE M2 BLOCKER) — the experimental prompts are registered

The registration pinned the models but not the prompts, and the prompts are
the treatment. The following are carried BYTE-VERBATIM from C29's committed
harness (`analyses/c29-curation-vs-search-sufficiency/generate_questions.py`
lines 40–55 and `run_policies.py` lines 22–56, at their committed state as of
cb73654) and are frozen for C34. `A_PROMPT` is not carried (deviation D-1
drops arm A).

From `generate_questions.py`:

```
Q_PROMPT = """From the document body below, write ONE factual question that
can be answered ONLY from this text. The answer MUST be an exact contiguous
string copied from the text, 3-15 words. Classify the question as "lookup"
(single fact) or "synthesis" (relates two parts of the text).
Reply with ONLY a JSON object: {{"question": "...", "answer": "...",
"qtype": "lookup|synthesis"}}

DOCUMENT BODY ({rp}):
{body}"""

S_PROMPT = """Write a one-line summary (max 140 characters) of what this
document is and contains, useful for deciding whether to open it.
Reply with ONLY the summary line.

DOCUMENT BODY ({rp}):
{body}"""
```

From `run_policies.py`:

```
COMMON = ("\nReply with your final line exactly as 'ANSWER: <the answer>' — "
          "the answer should be the exact wording from the document.")

B_PROMPT = """Answer the question using the markdown corpus in the current
directory. Use Grep/Glob to find relevant files and Read to inspect them.
Be efficient.{common}

QUESTION: {q}"""

C_PROMPT = """Answer the question about the markdown corpus in the current
directory. Below is an INDEX of every file (path — one-line digest).
Protocol: consult the index first; if it already answers the question, answer
directly. Otherwise Read the FEWEST files needed (paths are relative to the
current directory). Do not read more than necessary.{common}

INDEX:
{index}

QUESTION: {q}"""

D_PROMPT = """Answer the question from the single document below.
Do not use any tools.

DOCUMENT ({rp}):
{doc}

QUESTION: {q}{common}"""
```

M2 implements exactly these strings. Any deviation discovered at M2 is a
registration matter, not an implementation choice.

## C-2 (closes F2) — README.md exemption, the clause-6 claim, and snapshot pinning

1. `README.md` (repository root) is EXEMPTED from rule R by name. Reason,
   per the verifier's evidence: its C29 status-board row carries the parent's
   headline numbers and an actionability asymmetry toward arm C (an explicit
   statement that index-trusting answers are usually wrong). The direction is
   conservative, but it is the single highest-salience leak and the file most
   about C29 while being path-clean. Corpus arithmetic after exemption:
   141 files, 1,162,998 bytes; the ≥135 floor HOLDS.
2. The registration's §1 claim that clause 6 "removes every document about
   this study or its parent" is corrected to: clause 6 is a PATH filter; the
   content property is approximated, not guaranteed, and the residual
   self-reference is a disclosed limitation (as §Known limitations already
   stated). The stronger sentence is withdrawn.
3. The M3 corpus snapshot is taken from the git TREE STATE OF cb73654 (the
   registration commit), not the working tree at M3 time. Consequence:
   nothing the observatory beat or any session writes between registration
   and M3 — including README/status refreshes or new packets — can enter the
   corpus. The corpus is fully determined as of this correction.

## C-3 (closes F3) — deviation D-7 named

C29's frozen operationalization required "Corpora (>=2, real...)"; C34 runs
one corpus from one repository. This is the study's purpose (a single
shippable public corpus) and its cost is the already-stated single-operator
bound; it is hereby a NAMED deviation (D-7), not a silent one.

## C-4 (closes F5) — generation-input rule frozen

Question generation reads `body[:8000]` after frontmatter strip, carried
verbatim from C29 for comparability. Disclosed consequence on this corpus:
51 of 141 files exceed 8,000 bytes; ~26% of corpus bytes are unreachable to
the generator, concentrating gold answers toward document heads. Whether this
favors either arm is unknown; comparability with the parent is the reason for
carrying it unchanged.

## C-5 (closes F6) — reality probe ordered first

The two-call reality probe (1 generator + 1 answerer) runs BEFORE any other
provider call — ahead of question generation, not after M4 as the BUILD's M5
placement implied. The budget table already listed it first; the BUILD
ordering is corrected to match. Reason: Phase-H rule 3 — availability is
bought before the generation budget is spent, not assumed.

## C-6 (closes F7) — P5(b) denominator rule

P5(b) (">=80% of pooled non-hydrated answers incorrect") adjudicates only if
the pooled non-hydrated denominator across B and C is >= 20. Below 20 the
conjunct is `not_exercised` (Phase-H rule 4), is reported as such with its
denominator, and P5 adjudicates on P5(a) alone. Reason for 20: caps any
single question's influence on the conjunct at 5 percentage points; the
parent's denominator was 69.

## C-7 (closes F8) — regeneration order registered

If validated drops occur, regeneration proceeds in ascending question id
until the 45-call sub-ceiling binds; files still unregenerated when it binds
are recorded as dropped, and the shortfall rule applies to the validated
count.

## C-8 (closes F9) — tie prose corrected

P3' uses `>=`: an exact wrong-stop tie PASSES P3'. The registration's tie
paragraph incorrectly offered `no_wrong_stop_tax_at_power` as the reason for
a tie outcome; that reason is reachable only when P3' FAILS (strict
inequality in C's favor... i.e. wrongstop(C) < wrongstop(B) is not required;
precisely: the reason names a failed P3'). On a tie the frozen operator
governs and P3' passes; the prose is corrected to match the operator. No
operator changes.

## C-9 (closes F10) — clause order registered

Rule R's rejection ledger buckets by first matching clause in the order
size -> audit -> selfref (the order the registration's 3/5/4 ledger used).
`corpus_rule.py` must additionally emit ALL matching clauses per rejected
file, so the ledger is order-annotated rather than order-dependent.

## C-10 (closes F11) — power conventions named

The registered 98.4% / 96.2% power figures are normal-approximation values;
Fisher-exact equivalents are 97.8% / 94.8%. The demonstrator's 19.0% figure
is Fisher exact (recomputed 18.8%). All are design statistics only and
non-adjudicating; each future statement of a power figure names its
convention.

## C-11 (closes F12) — provenance phrasing tightened

"Extends from exactly that family" is corrected to: rule R admits files from
nine repository locations; the releasability guarantee is the uniform
zero-flag audit (clause 5) plus the paper/-and-analyses/ exclusion (clause
3), not descent from the previously-audited 17. The verifier's empirical
sweep of the 121 files outside docs/+essays/ found no third-party markers;
the guarantee remains the mechanism, not the provenance.

## C-12 (closes F4's reporting risk; no criteria change) — verdict legibility

§Release binding gains: if the machine verdict is `revised` for a
P4-marginal reason (`headroom_not_established_on_marginal_tokens` — the
foreseeable outcome, since the parent's own B sits at 2.85x against the 3x
bar), the M7 results document and the v2 import MUST present the P1 / P3' /
P5 outcomes at equal prominence with the verdict word, so the
curation-vs-search answer stays legible beside a headroom verdict that is
orthogonal to it.

## C-13 (attribution note from the verifier's Item 2) — D-2/D-6 provenance

D-2 and D-6 deviate not only from the conjecture's P3 text but from C29
DESIGN.md D5 (which froze the arm-conditional hydration rule the harness
implemented). Recorded so the deviation ledger cites the correct frozen
sources.

---

Corpus arithmetic after this correction, for the M1 re-verification:
ACCEPTED 141 files / 1,162,998 bytes (README.md exempted); ledger
size 3 / audit 5 / selfref 4 / named-exemption 1; floor >=135 HOLDS;
ceiling untriggered; snapshot source = tree of cb73654.
