# Epistemic matter and compiler-invocation audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/heap/heap/gemini/epistemic-matter.md.txt`
- `Workspaces/mentu-physics/foundational/blueprint/heap/heap-june-2025/YAML-Design-Principles.md`
- `Workspaces/mentu-physics/foundational/blueprint/heap/heap-june-2025/constitutional-compiler.md.txt`
- `Workspaces/mentu-physics/foundational/blueprint/heap/heap-june-2025/Compiler-Style-Guide.md`

No predecessor files were edited.

## Decision

Admit **C15 compiler invocation readiness**:
`corpus/conjectures/c15-compiler-invocation-readiness.md`.

The audited material asks for YAML, handles, and compiler layers to turn documents
into callable epistemic infrastructure. The admitted claim is narrower and testable:
artifacts with a minimal invocation contract should parse, validate, compose, and
return better than artifacts with ad hoc metadata.

## What was retained

| Idea | Disposition | Why |
|---|---|---|
| Handle Soul plus Body | **C15/C7 lineage** | The Soul gives a durable identity and integrity contract; C15 treats it as a Stage 0 equivalent, not as a complete compiler contract. |
| Progressive YAML activation | **Admitted as C15** | Stage 0, Stage 1, and Stage 2+ fields can be scored before downstream outcomes. |
| Compiler-callable minimum | **Admitted as C15** | `epistemic_id`, `document_type`, roles, function, and trust semantics are concrete predictor fields. |
| Trust semantics | **Admitted as C15/C14 lineage** | Trust boundaries can be scored and later checked against permission/ambiguity repairs. |
| Seven-layer constitutional compiler | **Parked as architecture** | Useful design vocabulary, but not an empirical law until compiler logs and outcomes exist. |
| YAML as poetry/protocol | **Vocabulary only** | Good authoring guidance, but not directly measurable. |

## Readiness posture

`analyses/c15-compiler-invocation-readiness/analyze.py` extracts YAML/frontmatter
specimens from the audited files and checks field coverage for:

- Stage 0 identity fields;
- Stage 1 compiler-callable fields;
- Stage 2+ relationship/evolution/interface fields;
- handle-soul vocabulary.

Current readiness snapshot:

- source files read: 4/4;
- YAML/frontmatter specimens extracted: 43;
- files carrying complete handle-soul vocabulary: 1;
- Stage 0-complete specimens: 5;
- Stage 1-complete specimens: 4;
- Stage 2+ specimens: 23;
- strict compiler-callable specimens (`Stage 0 + Stage 1` in one specimen): 0;
- strict invocation-ready specimens (`Stage 0 + Stage 1 + Stage 2+`): 0.

That last result is important. The source corpus specifies a measurable contract, but
its examples are distributed across stages and sometimes omit the strict combined
minimum. The analyzer preserves that gap instead of treating design intent as
implementation evidence.

C15 still needs first-seen artifact snapshots, compiler validation logs,
relationship-resolution outcomes, and reuse/composition follow-up.

## Next push

Add an `artifact_snapshot` / compiler validation surface to the live instrument:

- `artifact_id`
- `path`
- `content_hash`
- `first_seen_at`
- `frontmatter_hash`
- `compiler_stage_score`
- `missing_invocation_fields`
- `parse_status`
- `validation_status`
- `relationship_resolution_status`
- `reuse_or_composition_events`

That would let C15 test whether compiler-invocable structure improves operational
behavior beyond C7 handle richness and C13 semantic redundancy.
