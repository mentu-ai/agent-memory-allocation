# Release-claim vetting — Mentu Policy Harness (mentu.ai/news)

*Date: 2026-06-13. Author: Claude (Opus 4.8), under Rashid's mandate.*

*This is NOT corpus material — no new claims, no verdicts. It is the Mentu
commitment protocol applied to a **public statement**: before the Policy Harness
announcement asserts anything, each candidate claim is classified and, where it
touches a tested conjecture, the tie is named. The discipline is the constitution's
rule 1 ("nothing enters as a law") pointed at marketing copy. The 2025 corpus's
central flaw was claims-as-laws-without-measurement; a press release is the easiest
place to relapse, so we route it through here first.*

## Classification key

- **FACT** — mechanically verifiable now (git/license/tests/`gh api`). Assert freely.
- **CONSTRUCTION** — true by the design's structure, demonstrated by the test suite
  (fail-open, boundary-only, capability degradation). Assert as a *property*, present tense.
- **MECHANISM** — a thing the code *does* at a boundary. Assert the action, never the *outcome*.
- **CONJECTURE** — an unmeasured effect/outcome. Do NOT assert. May appear only as
  explicitly-labelled forward-looking intent.
- **CONTRADICTS-VERDICT** — would assert something the corpus has *refuted* or is
  *actively testing*. Forbidden.

## The ledger

| # | Candidate claim | Class | Corpus tie | Verdict |
|---|---|---|---|---|
| 1 | Published, Apache-2.0, at `github.com/mentu-ai/mentu-hooks` (`35e566d`) | FACT | — | **Assert** |
| 2 | One `AgentEvent→Decision` core governs Claude, Codex, Cursor, Gemini, and mentu | FACT (5 rows in `capabilities.py`; e2e "one core, two agents") | — | **Assert** |
| 3 | Fail-open: absent substrate → permissive no-op | CONSTRUCTION (e2e case 1–2) | — | **Assert (property)** |
| 4 | Boundary-only: refuses at decision points, never mid-flight | CONSTRUCTION (CLAUDE.md principle; e2e) | — | **Assert (property)** |
| 5 | Capability-honest: Gemini *cannot* pre-gate → degrades to observe+warn, records `capability_degraded` | CONSTRUCTION (e2e case 8) | — | **Assert** — and lead with it; honesty about what an agent *can't* enforce is the differentiator |
| 6 | The secret-leak gate *refuses to commit* a diff matching a credential pattern at the commit boundary | MECHANISM | — | **Assert the mechanism.** NOT "prevents leaks / makes you safe" (outcome, unmeasured) |
| 7 | The context-window gate *refuses* a >200-line sub-agent return, directing it to a file | MECHANISM | — | **Assert the mechanism.** NOT "saves context / improves results" |
| 8 | Trust-banded tool-permission gate exists (trust from the ledger) | MECHANISM exists | **C1b (live experiment)**; applications-map #2 (trust-scaled autonomy is a *proposal*, not shipped) | **Assert the mechanism exists.** Do NOT claim trust-driven autonomy or that trust "earns" authority — that loop is unshipped and under test |
| 9 | "~80% of the logic is host-agnostic" | MEASURED → **does not hold for the shipped package** | — | **Cut the number.** Measured 2026-06-13: 1621 core / 893 adapter non-blank LOC = **64% core**. The "~80%" described the *legacy hooks*, not this package. Say "the per-agent adapters are thin translation shims; the policy lives in one shared core" — no contested percentage |
| 10 | The observe tier + CIR turns cross-agent activity into **learning / compounding intelligence / a moat** | CONJECTURE (unestablished) | **C1** verdict is *"refuted (strong form), as instrumented"* — NOT a refutation of recursive intelligence as a principle ("refuted as-implemented, not retired as an idea"). The finding: the return loop is **open** — knowledge is delivered but 0/54 runs recorded measured usage, most likely an attribution/format gap (the instrument can't yet *see* usage; directional success even favors injection, 42.6% vs 30.5%, p=0.086). **C1b** is live. | **Do not assert it as a delivered/measured outcome** — because it is *unestablished and under active test*, NOT because the idea is false. The observe tier produces an **audit trail** (FACT — it writes typed signals); claim that. Recursive intelligence is a legitimate open thesis the corpus is still testing — it may be claimed as *direction/intent* if labelled as such, never as a shipped result |
| 11 | "Makes your agents safer" / "prevents incidents" | CONJECTURE (outcome) | — | **Cut.** Assert mechanisms (6,7), let the reader infer. No incident/outcome claim is measured |
| 12 | "The governance dual of the Mentu Protocol" | POSITIONING (analogy, not empirical) | The Mentu Protocol (MIT, already announced) | **OK as framing** — it's a narrative tie, not a measurement claim |
| 13 | Cursor's gate was a hardcoded auto-approve; the harness wires the real verdict | FACT (the `{"continue":true}` hardcode is gone) | — | **Assert** |
| 14 | The migration is behavior-preserving — legacy hooks pinned by golden vectors before rewiring | FACT (53 goldens, `--verify` clean) | — | **Assert** (engineering credibility; matches the page's concrete voice) |

## The rule this produces (for the writer)

**Assert the architecture and the mechanisms; describe the audit trail; never assert an
outcome as a delivered, measured result.** The harness *is* one core over five agents,
*refuses* at boundaries, *degrades* honestly, and *records* what happened. It is **not**
(yet, and not in this post) *shown* to make agents safer, smarter, or to compound
knowledge. Note carefully what the corpus actually says: C1's verdict is *"refuted (strong
form), as instrumented"* — the current build delivers injected knowledge but can't yet
measure it being consumed (the return loop is open) — and the result is explicit that this
is *"refuted as-implemented, not retired as an idea."* Recursive / return-as-intelligence
remains a live, legitimate thesis (C1b is testing it now); it must not be asserted as a
*shipped result*, but it is fair game as stated *direction*. A post that respects that line
is both honest and, by this page's concrete-over-hype standard, *stronger*.

## Not a verdict

Nothing here graduates or refutes a conjecture. It records that the release copy was
disciplined against the corpus on 2026-06-13, and names the two live ties (C1/C1b) the
copy must not cross. If the post later wants to claim a governance *outcome*, that is a
new conjecture — it enters `corpus/conjectures/`, gets a measurement procedure and frozen
predictions, and is tested. It does not enter as a sentence in a press release.
