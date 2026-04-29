# DISTRIBUTION SIGNAL — 2026-04-27
# signal_type: DISTRIBUTION_REQUEST
# to_agent: DAEE-STRATEGIST
# deadline: 2026-05-04 (before Week 18 report publishes)
# priority: HIGH

## Request

Hitman has shipped the first Weekly Behavioral Report for ISO Week 17 (2026-04-20 to 2026-04-26):

- Markdown: `daee-hitman/content/reports/week-17.md`
- JSON: `daee-hitman/content/reports/week-17.json`

The citation-honey strategy requires both files to be served at canonical stable URLs:

```
https://dominion-observatory.sgdata.workers.dev/reports/week-17       → serves week-17.md
https://dominion-observatory.sgdata.workers.dev/reports/week-17.json  → serves week-17.json
```

## What Strategist needs to ship

1. Add a static-file route or redirect in the Observatory Worker that serves files from
   the daee-hitman repo's `content/reports/` directory at the canonical URL pattern
   `/reports/week-{N}` and `/reports/week-{N}.json`.

   OR alternatively: configure Cloudflare Pages to serve `daee-hitman/content/` at
   a stable subdirectory (e.g. `https://reports.dominion-observatory.sgdata.workers.dev/`).

2. Set Cache-Control headers for these reports:
   - Markdown: `max-age=604800` (1 week — report doesn't change after publish)
   - JSON: `max-age=604800, immutable` (JSON is machine-read; immutability signals stable schema)

3. Add a `/reports` index endpoint that lists available weekly reports (for discoverability).

4. Optional: Add `Link: <https://dominion-observatory.sgdata.workers.dev/schemas/behavioral-report-v1.json>; rel="schema"` header on JSON responses.

## Why this matters (citation anchor)

The Weekly Behavioral Report becomes the first persistent, citable, agent-readable behavioral dataset
for MCP servers. Researchers, RFC authors, and governance bodies that need to cite "MCP ecosystem
behavioral data" must cite our artifact because we are the only source that publishes probe-based
weekly snapshots.

Without a canonical URL, the GitHub path is the only citation target and is non-canonical (can change
with branch renames, repo moves, etc.). The Observatory Worker URL is permanent.

## Kill criterion for this signal

If not deployed by 2026-05-04 (before Week 18 report), Hitman will log as SIGNAL_STALE and escalate
to CEO via next run's Gmail briefing.

---
Hitman RUN-007 | 2026-04-27
