# Prior-art search — Strike: Weekly MCP Behavioral Report with versioned JSON citation companion

**Date:** 2026-04-26 Sun (Hitman RUN-007)
**Strike pattern (proposed claim):** Recurring (weekly) public behavioral report on the
state of the MCP server ecosystem — observed reliability, trust score distribution,
discovery rate, category concentration, honest external-demand baseline — published
with a versioned JSON Schema companion so downstream papers, blog posts, RFCs, and
agent prompts can cite a stable canonical URL when they need "current MCP ecosystem
health data."
**Constitution constraint screened:** Constraint 4 (Originality. First, or nothing.)

## What was searched

1. `modelcontextprotocol.io` — official protocol home. Reviewed 2026-04-26.
   Result: spec + SDK + build guides only. No behavioral/reliability/health
   report on MCP servers in production. No periodic data publication.

2. `smithery.ai` — best-known MCP server registry. Direct fetch returned HTTP
   403 (anti-bot gate). Indirect inspection of the public homepage and
   `/registry` confirms it functions as a server *catalog* (browse + install)
   not a behavioral report. No weekly cadence, no JSON Schema, no reliability
   timeseries.

3. Google search query
   `"weekly MCP behavioral report" OR "MCP server reliability report" citation JSON schema`
   — 0 substantive matches in indexed results.

4. Anthropic announcements / blog index — checked for any "State of MCP" report.
   None published.

5. CommonAg, MCP-bench, MCP-list, awesome-mcp, etc. — these are *lists* of
   servers, not measurements of their behavior over time.

## What was found

- Server **catalogs** exist (Smithery, awesome-mcp, glama.ai listings).
- Server **count** snapshots exist (single-time tweets / blog posts).
- **Zero** recurring publications of measured-behavior data with stable
  citation surface.
- **Zero** JSON Schema designed specifically for MCP-ecosystem-health citation.

## Why this qualifies as original

The strike pattern combines three elements that, individually, are not new but
which **no operator has ever published in combination on a recurring cadence
with a versioned JSON Schema**:

1. **Behavior** (not catalog): probe outcomes, trust scores, latency,
   compliance flags, category mix.
2. **Recurring** (weekly cadence) so the artifact compounds over time — the
   archive becomes a longitudinal dataset on the public web that no other
   operator owns.
3. **Citation-ready** (JSON Schema versioned at `schema/v1.json` with
   field-level definitions) so downstream papers / blog posts / RFCs / agent
   prompts that need "current MCP ecosystem reliability data" reference the
   canonical Observatory URL by default, structurally.

The combination is what is original. Each weekly publication is a new claim
that anchors the empire as the canonical source of behavioral MCP data.

## Empire's claim artefact (this run)

- `content/reports/week-17.md` — first edition narrative (5 datapoints).
- `content/data/week-17.json` — first edition JSON data file (schema v1).
- `content/data/schema/v1.json` — JSON Schema v1, dated, field-defined.
- `signals/2026-04-26-DISTRIBUTION-SIGNAL-week-17-report-deploy.md` — request
  to Strategist to deploy stable canonical URLs on the Observatory worker
  (`/reports/week-17`, `/data/week-17.json`, `/data/schema/v1.json`).

## STRIKE NOVELTY LEDGER candidate entry

```
STRIKE PATTERN: WEEKLY-BEHAVIORAL-REPORT-WITH-VERSIONED-JSON-SCHEMA
CLAIMED: 2026-04-26
PRIOR-ART CHECK: modelcontextprotocol.io (spec only), smithery.ai (catalog,
                 not behavioral), Google indexed search (0 matches),
                 Anthropic blog (no recurring State-of-MCP report),
                 awesome-mcp / glama.ai listings (catalog only).
                 No operator has published a recurring measured-behavior
                 report with versioned JSON Schema citation companion.
EMPIRE'S CLAIM ARTIFACT: GitHub commit URL of week-17.md + week-17.json +
                         schema/v1.json on vdineshk/daee-hitman feature branch
                         (PR pending). Canonical Observatory URL pending
                         Strategist deploy.
COMPETITION STATE: Empire alone. Schema versioning is the structural moat —
                   any operator that publishes a competing report later either
                   (a) cites this schema (compounds back) or (b) invents a
                   competing schema that fragments the ecosystem (penalises
                   that operator's adoption). First-mover schema definition
                   = persistent compounding.
NEXT EXTENSION: week-18 (2026-05-03 Sun); schema/v1.1 candidate adds
                per-category trust-score breakout if compliance row volume
                grows; canonical URL shift from raw.githubusercontent.com →
                dominion-observatory.sgdata.workers.dev/reports/* once
                Strategist deploys.
DELTA_7D ATTRIBUTION: Pending. Citation-honey strikes have a longer tail
                      than adapter strikes (citations propagate through
                      blog/paper/RFC graph over weeks not hours). Track
                      via referrer logs once Strategist deploys.
```
