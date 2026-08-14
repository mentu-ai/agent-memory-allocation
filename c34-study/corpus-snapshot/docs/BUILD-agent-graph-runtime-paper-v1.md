# BUILD — The Agent Graph Runtime paper v1

**Date:** 2026-07-30
**Status:** `v0.9.3-internal` complete; `v1.0-preprint` blocked on an
isolation-compliant Operon rerun
**Canonical paper home:** `paper/agent-graph-runtime/`
**Canonical manuscript source:** `paper/agent-graph-runtime/paper.tex`
**Working release:** `v0.9.3-internal`
**Release gate:** memory-disabled, separate-context literature verification and
exact-input blind review with `INDEPENDENCE-ATTESTATION.json`
**Author:** Rashid Azarang

## 0. Objective

Build the architecture-and-systems preprint:

> *The Agent Graph Runtime: A Unified Model for Static, Dynamic, and Hybrid
> Execution*

The paper's defensible thesis separates runtime unity from assurance-profile
uniformity:

> One execution substrate can support multiple graph-lifecycle policies.
> Mentu is the audited reference implementation of this model's
> shared-substrate core: persistent and generated DAG-shaped paths converge on
> a common executable representation, runner, and scheduler while retaining
> policy-specific authority profiles. Interpreted adaptive workflows form a
> distinct runtime tier.

“Audited reference implementation” is a source-backed model-to-system
designation, not a standards certification or comparative rank. It does not
claim that Mentu has one uniform admission profile, that every product surface
is covered by this audit, or that comparative world leadership has been
scientifically certified.

The C30 pilot validates instrumentation for staged execution. It does not
compare static, dynamic, and hybrid outcomes.

## 1. Repository constitution

1. Write only in `epistemics`, on `main`.
2. Do not modify `mentu-complete`, `structural-waste`, frozen C30 fields,
   pilot results, or sealed run bundles.
3. Read Mentu evidence through direct files and read-only Git operations.
   Never invoke Mentu CLI or MCP CIR paths.
4. Pin implementation facts to Mentu commit
   `40bd3f90cf4cfd34cdcf3f885018b5096ec28e6f`.
5. Treat uncommitted Mentu GUI/terminal work as non-load-bearing local
   evidence.
6. Use committed analysis outputs as the numerical source of truth. Manuscript
   prose and figures are projections of those outputs.
7. Commit milestones locally. Never push.

## 2. Claim constitution

Every material claim receives one class:

- `architectural_definition`
- `implementation_fact`
- `pilot_observation`
- `formal_implication`
- `open_hypothesis`
- `excluded_claim`

The paper may currently claim:

- static, dynamic, and staged-hybrid execution are representable as lifecycle
  policies in one abstract model;
- Mentu's static and generated paths share `SequenceDefinition`,
  `SequenceRunner`, and scheduling machinery;
- Mentu serves as the reference implementation of the shared-substrate model
  within this paper;
- staged saved-plan execution preserved executable identity in the C30 pilot;
- saved-plan execution recorded zero planner dispatches in that pilot;
- authoring profile is distinct from runtime authority;
- graph qualification and semantic artifact correctness are distinct gates.

The paper may not claim:

- global uniform admission across Mentu entry points;
- comparative claims that Mentu is globally first, best, or superior to every
  other agent runtime before the Operon and benchmark gates;
- hybrid task, cost, latency, maintenance, or regression superiority;
- deterministic model behavior;
- semantic correctness from graph qualification;
- generality across agent platforms;
- amortization before the registered unchanged-state repetition study.

## 3. Build graph

### P0 — Provenance and research contract

Deliver:

- `SOURCE-MAP.md`
- `RESEARCH-CONTRACT.md`
- `provenance/CLAUDE-SCIENCE-IMPORT.md`
- corrected C30 README status row

Gate:

- current repository heads and dirty states recorded;
- source-map corrections explicit;
- raw Claude Science export remains outside Git;
- `ground_truth.json` recorded as unavailable;
- partial literature searches barred from citation.

### P1 — Scientific substrate

Deliver:

- `DEFINITIONS-AND-BOUNDARIES.md`
- `FORMAL-MODEL.md`
- `CLAIMS-LEDGER.md`
- `spec-map.json`
- `PILOT-EVIDENCE-AUDIT.md`

Gate:

- all four C30 modes derive from separately specified lifecycle coordinates
  over an explicit feasible region, without assuming Cartesian or statistical
  independence;
- general agent graph is not silently equated with Mentu's admitted
  generated-graph v1 strict DAG;
- shared substrate and differentiated authority profiles are distinguished;
- a runtime-replanning counterexample is retained;
- every strong claim has an evidence class and decisive test.

### P2 — Reproduction

Deliver:

- path-neutral read-only scripts under `analysis/`;
- immutable derived JSON under `results/`;
- generated figures under `figs/`;
- a path-neutral reproduction kit.

Required results:

- five of five persistent-projection identities;
- three of three inspection-to-receipt identities;
- zero saved-plan execution planner dispatches;
- zero run-bundle manifest digest mismatches;
- three distinct discovery repository heads across the five plan stages;
- two human semantic plan rejections;
- one post-run semantic correction;
- zero matched static or dynamic observations;
- no unchanged-state three-repeat series;
- 42 of 42 invariant checks pass;
- comparative verdict barred.

### P3 — Internal preprint

Deliver:

- canonical `paper.tex`;
- `references.bib`;
- bounded, claim-specific `LITERATURE-VERIFICATION.md`;
- private-return disposition without importing the raw export;
- four machine-generated figures;
- `paper-v0.9.3-internal.pdf`, a 22-page internal preprint;
- source archive and build manifest;
- reproduction supplement;
- hardening changelog and integrity sweep.

The PDF must visibly say:

> Internal preprint. Independent literature certification and blind review are
> pending; not for dissemination.

`build.py --mode internal` may build with that gate. `build.py --mode release`
must refuse until the Operon artifacts and their Codex disposition exist.

### P4 — Operon audit and compliant rerun

The 30 July return produced 116 literature records and 36 blind-review
findings. Codex independently resolved metadata for 116 of 116 records,
retained 22 verified citation keys, and dispositioned all 36 findings. These
outputs are accepted as advisory evidence only.

They do not satisfy the release gate:

- automatic project memory entered the literature and blind-review contexts;
- the blind reviewer read result JSON beyond the stipulated PDF and public
  supplement;
- the narrative claim of memory independence is therefore unsupported.

The release-completing rerun must:

- use separate literature and blind-review contexts with project memory
  disabled;
- conduct independent scholarly discovery and full-text/identifier
  verification;
- blind-review exactly the current internal PDF and public reproducibility
  supplement, and no other project artifact;
- bind the exact input and output hashes in
  `INDEPENDENCE-ATTESTATION.json`;
- use distinct addressable context identities for literature and blind review;
- bind the reviewed PDF to the exact canonical TeX, bibliography, builder,
  formal supplements, and generated internal context;
- produce finding/disposition coverage with no unresolved major issue.

Operon findings remain proposals, not automatic edits. Codex must independently
verify and disposition them before a `v1.0-preprint` release build.

## 4. Formal model requirements

The minimal model contains:

1. source authoring;
2. candidate construction;
3. lowering to an executable graph;
4. qualification;
5. optional freeze into an addressable plan;
6. requalification against current state;
7. admission;
8. execution through a substrate;
9. evidence production.

The C30 policy vector is:

`(construction_time, freeze_boundary, authoring_method, execution_substrate)`.

The model must distinguish:

- executable graph identity;
- authority/environment identity;
- output reproducibility;
- semantic correctness.

The worked counterexample is runtime replanning that mutates graph structure or
scheduling semantics inside an admitted epoch. That behavior changes the
execution model and is not merely another policy over the same frozen graph.

## 5. Canonical build

- Tectonic 0.16.9 is the canonical PDF engine.
- Poppler renders every page to PNG for visual inspection.
- Figures are generated from `results/*.json`, never from hand-entered
  manuscript numbers.
- The canonical source archive contains only repository-relative paths.
- The public package excludes raw session exports, transcripts, credentials,
  private paths, and sealed run-bundle contents.

## 6. Acceptance gates

1. **Provenance:** source heads, input hashes, symlink, moved intent path,
   evidence tiers, and missing artifacts are accurate.
2. **Construct:** terms and lifecycle axes have one definition each.
3. **Formal:** invariant checks pass and counterexamples remain visible.
4. **Empirical:** frozen results reproduce and no comparative claim appears.
5. **Claims:** every material claim maps to evidence and a class.
6. **Citations:** bibliography and citations match bidirectionally; unverified
   identifiers block release mode.
7. **Build:** Tectonic succeeds with no missing references or figures.
8. **Visual:** rendered pages show no clipping, overlap, broken glyphs, or
   unreadable tables.
9. **Privacy:** public artifacts contain no local absolute paths or private
   evidence bodies.
10. **Release:** internal mode succeeds with 42 of 42 invariants; release mode
    refuses until a memory-disabled, separate-context exact-input rerun and a
    valid `INDEPENDENCE-ATTESTATION.json` satisfy the external gate. The build
    also rejects basename-only blind paths, shared context identities,
    mixed-version returned artifacts, unverified candidates, stale manuscript
    projections, and any universal novelty certification.
