# Operon-c36 v1 — launch instructions (two sessions, human-run)

A proportionate instantiation of the Operon supplied-export pattern for the
c36 companion result. Two separately closed Claude Science sessions, no
coordinator, byte-pinned attachments per `MANIFEST-C36-V1.md`. The paper is
built only after both returns are dispositioned.

## Custody rules (carried from the v0.9.9-r6 jurisprudence)

1. Each session is a **new, no-prior-chat** top-level session.
2. Attach the folder contents exactly; do not add, rename, or
   open-and-resave any file.
3. Export a session **only after it has completed** and emitted its final
   JSON output. An export of a still-running session is a
   `SUPPLIED_INPUT_CUSTODY_DEFECT` and voids that session (the r5 lesson).
4. One attempt per session per revision. A defective session costs the
   session, not the revision — relaunch requires a new revision string.

## Session V — validation (adversarial recomputation, no web needed)

Attach everything in `inputs-v/` (20 files + SESSION-V-PROMPT.md), then paste:

> Execute the attached `SESSION-V-PROMPT.md` exactly. You are an independent
> validator: recompute every number from the attached raw records with your
> analysis tooling, trust no stated figure, attempt refutation, and end with
> the single JSON object the prompt's output contract specifies. Do not
> consult the web or any file not attached.

## Session L — literature positioning (web required)

Attach everything in `inputs-l/` (3 files + SESSION-L-PROMPT.md), then paste:

> Execute the attached `SESSION-L-PROMPT.md` exactly. Verify every citation
> live before it enters your output, quote one load-bearing sentence
> verbatim per work, and end with the single JSON object the prompt's
> output contract specifies. Do not read any local file beyond the
> attachments.

## Return handling

Bring both final JSON objects (or full exports) back to the working
session. Disposition: every Session V defect is adjudicated
adopt/decline-with-reason in a dated disposition document; Session L's
`recommended_confrontations` become mandatory citations in the companion
paper's related-work section; a Session V `noncompliant` blocks the paper
build until resolved. Title selection happens after disposition.
