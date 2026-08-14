# Plan: harden our ways, fix from root, test again (2026-08-12)

**Companion to** `essays/2026-08-12-what-the-burned-pilot-taught.md`. The
essay states the lessons; this plan operationalizes them. Author decisions are
marked ☐; everything else is standing work.

## Phase H — harden the method (standing rules, program-wide)

1. **Dead-run rule.** Every gate ships with a companion test that constructs
   a total failure the gate must catch. Installed instances: C33
   `provider_output_not_degenerate`, entrypoint/panel probes in the freeze
   audit, the sealed-400-envelope transport regression, Operon r3 adversarial
   envelope fixtures. Standing obligation: any NEW gate lands with its dead
   run in the same commit.
2. **Green-review rule.** No fully-green result is believed until a
   non-author adversarial pass fails to refute it. Operationalized as the
   builder-audits-executor inversion; applies equally to orchestrator
   summaries (two were corrected today by the inversion).
3. **Enumerate-then-freeze rule.** No pre-registration pins behavior of a
   surface we do not control (APIs, platforms, export formats) without
   either an empirical enumeration from real instances or an explicitly
   budgeted reality probe. Templates: r3 envelope model (enumerated from four
   real exports); the one-call schema-acceptance probe (budgeted, accounted).
4. **Denominator rule.** Every zero/null is reported with its denominator and
   exercised-status (`not_exercised` vs `zero_events`), in operational
   reports as well as registered analyses.
5. **Cost-of-knowledge ledger.** Each discovered truth is recorded with what
   it cost (the transport-failure gate: 70 calls + 5 discordance levels; the
   envelope model: two producer-session pairs). Purpose: bias future designs
   toward cheap discovery (probes before pilots, enumeration before freezes).

6. **Hash-freezing is not archiving.** A manifest of hashes proves integrity
   only while the files exist. Discovered 2026-08-12 (§X1 of the memory-
   allocation disposition): 1,996 of 2,337 frozen-manifest transcripts had
   been deleted by harness rotation, leaving C26/C27/C28 permanently
   non-re-derivable from their own manifests (all surviving files verify
   byte-exact; C29 unaffected — its evidence is its own committed run
   records). Standing rule: every future retroactive probe SNAPSHOTS its
   corpus into committed or archived storage before analysis; a hash-only
   freeze is not a freeze. Candidate observatory gate-event: manifest
   liveness checks on each beat.

## Phase F — fix from root (known remaining gaps)

1. C33 suite-replay byte-identity is recorded but not mechanically enforced
   by the freeze audit (deferred 2026-08-12); fold into the next unavoidable
   freeze cycle. The verdict-bearing analyzer path already enforces identity.
2. Operon: two producer sessions under r3 remain to be run; the r3 protocol
   carries the robust envelope model. If r3 stops again, the next revision
   revisits whether a closed envelope model is achievable at all on this
   platform, per the r2 stop note's meta-finding.
3. Blind-spot registry: each new audit blind spot found (four to date) gets a
   dead-run test in the same repair, and is listed in the relevant audit
   contract's comments so the class stays visible.

## Phase T — test again (the C33 confirmation decision)

Pilot-v2b is sound: real inference, zero integrity findings, and a real
result — Haiku schema-valid proposal rate 12% at episode level, zero
discordant pairs, H never diverged from P. Three registered-path options:

☐ **T1 — Run the Haiku confirmation as registered.** Affordable (projected
  ≈696/900 if Stage 1 resembles the pilot). Produces the adjudicated
  model-conditional verdict M3 needs to seal the manuscript and reach the
  blind Operon gate. The likely finding is honest but thin: non-inferiority
  assembled largely from concordant ties, with enforcement exercised only by
  the constructed challenge panel.

☐ **T2 — Register a Sonnet successor study** (new conjecture id, own
  registration, own benchmark pilot cohort via the already-analyzed
  benchmark-extension mechanism, own budget), pre-registered BEFORE any
  Sonnet data exists. This is the clean way to act on the pilot's lesson: the
  model change is a new registered experiment informed by C33, not an
  outcome-driven mutation of C33. A higher-validity model would exercise the
  gate against real proposed actions — the substantive question C33's pilot
  could not reach.

☐ **T3 — NOT this: switching C33 itself to Sonnet.** Changing the registered
  model after seeing pilot behavior is an outcome-informed change to the
  estimand's conditioning — the exact class of move this corpus exists to
  prevent. Recorded here as rejected-by-policy unless the author explicitly
  overrides with a dated correction that names it as outcome-informed.

Recommended combination: T1 then T2 — complete the registered arc (cheap,
unlocks the manuscript), and pursue the substantive question in a clean
successor registration.
