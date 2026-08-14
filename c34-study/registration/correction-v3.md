# C34 registration correction v3 (2026-08-13)

**Scope:** text-only; closes the re-verification findings G1–G5 on correction
v2 (b42fe73). Nothing here changes any threshold, floor, model pin,
verdict-map clause, corpus membership, or adjudication rule beyond what v2
already registered. Authored by the orchestrator; the v2 re-verifier's
findings are applied verbatim. Where v2 and this document conflict, this
document governs.

## G1 — C-4's disclosed-consequence figures corrected (stale across the exemption)

v2 carried pre-exemption numbers against the post-exemption denominator.
Correct figures: **50 of 141 files exceed 8,000 bytes; 292,894 of 1,162,998
corpus bytes (25.2%) are unreachable to the generator.** (v2 said 51/141 and
~26% — README.md, itself >8,000 bytes, left both numerator and byte totals
when exempted.)

## G2 — C-8's parenthetical replaced (it stated the opposite of the rule)

The v2 parenthetical is withdrawn in full. Replacement text:

> `no_wrong_stop_tax_at_power` is reachable only when P3' fails, i.e. only
> when wrongstop(C) < wrongstop(B) strictly. On a tie the frozen `>=`
> operator governs and P3' passes.

## G3 — ledger completeness: D-8 and D-9 named

Two v2 changes of deviation weight enter the deviation ledger:
- **D-8**: rule R gains the named README.md exemption (v2 C-2.1), narrowing
  the corpus; reason and evidence as recorded there.
- **D-9**: P5(b) gains a >=20 pooled-denominator floor with a
  `not_exercised` branch (v2 C-6). Both are dated, pre-data, pre-harness;
  D-8 narrows the corpus and D-9 can only withhold a conjunct, so neither
  can be outcome-shopping.

## G4 — v2 header sentence corrected

v2's "Nothing here changes a threshold, a floor, a model pin, or the verdict
map" was narrowly true but read broader than it delivered. Corrected
statement: no threshold, floor, model pin or verdict-map clause changed;
rule R (D-8) and P5(b)'s adjudication rule (D-9) did change, as named.

## G5 — dead branches recorded as verified preconditions (M2 guidance)

Pinning the snapshot source to the cb73654 tree makes two registered
branches unreachable: the >170 salted-subsample ceiling path and the <135
instrument-insufficient cause. Both are hereby recorded as **verified
preconditions** (the enumeration at cb73654 is fixed at 141), not live
branches: M2 must NOT implement them as executable code paths, and their
dead-run tests are replaced by a single precondition assertion (corpus count
== 141 at sandbox assembly, failing closed on any mismatch). Related
recordings: the generation and digest sub-ceilings (170 each) over-fund the
fixed corpus by 29 calls each; actual maximum need is 869 of the 950
ceiling; registered caps stand and unused sub-ceilings remain
non-transferable. The floor margin (141 vs 135) is permanent, not erodible.

## Re-verifier notes G6–G8 acknowledged (no action)

G6 (margin permanence) and G8 (the C-1/C-6 interlock: pinned prompts close
the only path by which the not_exercised branch could be engineered) are
recorded as properties worth preserving — neither correction may later be
relaxed in isolation. G7: the >=20 floor caps per-question influence at 5pp
and nothing more; at the floor, P5(b) retains ≈11% false-fail probability
against the parent's own 87% rate. "Denominator >= 20" must not be read as
"P5(b) is reliable"; the M7 results document reports the realized
denominator with the conjunct.
