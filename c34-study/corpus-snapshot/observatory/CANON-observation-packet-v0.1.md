# CANON — Observation Packet v0.1

The observatory is the corpus's metabolism: a daily beat that reads what Mentu
actually did, interprets it against the open conjectures, and develops the
corpus progressively. It borrows the Scheduler workspace's packet discipline
(bounded, dated, evidence-backed, gated) and applies it to theory development.

## The beat

**Daily** (one packet per day, `observatory/packets/YYYY-MM-DD.md`):

1. **Collect** — run `observatory/collect.py` (read-only; raw SQLite only, per
   the observer-effect rule). Its output is the packet's mechanical digest.
2. **Interpret** — read the digest against open conjectures and recent packets.
   Write the interpretation: what changed, what's anomalous, what it suggests.
3. **Classify** every interpretive item as exactly one of:
   - `note` — an observation, free to record;
   - `conjecture-candidate` — recurring pattern that wants a claim; admission
     still requires the constitution's full bar (operationalization + frozen
     predictions) before it enters `corpus/conjectures/`;
   - `gate-event` — a gate opened; schedule the corresponding frozen analysis.
4. **Update tracking frontmatter** (see below) and commit the packet.

**Weekly** (Sundays, appended to that day's packet as `## Weekly synthesis`):

- Roll up the week's packets; refresh the README status board.
- Check every gate explicitly (C1b accrual, C3 detector age/count, C2 span).
- Run any frozen analysis whose gate opened; adjudicate mechanically.
- **Metabolize one 2025 idea**: take the next un-salvaged item from
  `lineage/from-ese-2025.md` ("deliberately not yet admitted") or the law
  suites; either operationalize it into a conjecture-candidate against the
  instrument, or record in `lineage/exclusions.md` why no measurement
  procedure exists. The old canon gets digested one claim per week.

## Progressive frontmatter

Conjecture files carry two frontmatter regions:

- **Frozen** (human, constitutional): `id`, `name`, `lineage`, claim,
  predictions, falsification criteria, `verdict`, `result`. Beats never edit
  these.
- **Tracking** (machine, append-friendly): updated by beats only.

```yaml
tracking:
  last_beat: 2026-06-10
  beats: 1
  accrual: { injected: 0, withheld: 0 }   # conjecture-specific counters
  gate: "0/150 per arm"
  watch: []                                # packet ids of notable observations
```

Progressive disclosure: the daily packet surfaces only deltas and the
conjecture nearest its gate; depth lives in the files and is revealed on
demand, not repeated.

## Constitutional guards (inherited and extended)

1. Beats read Mentu data via raw read-only SQLite / file reads — never via
   `mentu` CLI or MCP paths (observer effect).
2. Beats may append packets, update `tracking:` blocks, and refresh the README
   board. They may **never** edit frozen predictions, verdicts, results, or
   anything in `corpus/supported/` / `corpus/refuted/`.
3. Verdicts come only from gate-triggered frozen analyses, never from
   interpretation.
4. A conjecture-candidate that appears in three packets without
   operationalization is either operationalized or explicitly dropped — no
   permanent limbo.
5. Every packet ends with a one-line honest status: `quiet`, `accruing`,
   `anomaly`, or `gate-event`.

## Packet states

`collected → interpreted → committed`. No packet is retroactively edited;
corrections go in the next packet (same rule as results).
