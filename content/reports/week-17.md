# Dominion Observatory Weekly Behavioral Report — Week 17 of 2026

**ISO week 17 — 2026-04-20 → 2026-04-26.** First edition. Generated
2026-04-26T12:34Z. Source: live `/api/stats` + `/api/compliance` (curl
2026-04-26T12:33:49Z). Companion JSON: `data/week-17.json` (conforms to
`schema/v1.json`). License: CC-BY-4.0 — cite this report as "Dominion
Observatory Weekly Behavioral Report, week-17-2026".

The Dominion Observatory has been continuously probing and recording the
public MCP server ecosystem since 2026-04-08 (18 days at this edition).
This report compresses that surface into five honest data points that
practitioners, researchers, regulators, and agent operators can cite when
they need "current MCP ecosystem reliability data."

It is intentionally honest about the gap between *gross interactions
recorded* and *real external demand*. Most published "MCP ecosystem"
numbers in 2026 conflate the two; we do not.

---

## Five datapoints

### 1. Server discovery rate ≈ **255 servers / day**

The Observatory has tracked **4,584 distinct MCP server URLs** across the
public web in 18 days, a rolling lifetime average of **254.67 servers
per calendar day**. Discovery is not slowing — `total_servers_tracked`
moved from 4,012 on 2026-04-15 to 4,584 today. At this rate the public
ecosystem of HTTP-addressable MCP servers will cross **10,000** before
the end of June 2026.

### 2. Average measured trust score: **53.9 / 100**

Trust score is computed per server from probe outcomes: success rate,
latency stability, schema-validity, error-class distribution, and
JSON-RPC compliance. The ecosystem-wide average is **53.9** —
mid-range. A server scoring 53.9 is *probabilistically usable* but not
*production-grade*. Translation: roughly half of the public MCP
ecosystem in week 17 of 2026 fails at least one production reliability
check.

### 3. Category concentration — top 4 categories = **71.8%** of the ecosystem

Of the 4,584 tracked servers:

| Rank | Category      | Servers | Share |
|------|---------------|--------:|------:|
| 1    | other         | 1,880   | 41.0% |
| 2    | uncategorized | 729     | 15.9% |
| 3    | search        | 367     |  8.0% |
| 4    | code          | 317     |  6.9% |

The top 4 categories absorb **71.8%** of the server count. The
"other" + "uncategorized" share alone is **56.9%** — a strong signal
that **MCP server categorization on the public web is currently
unsolved**. There is room for one canonical taxonomy publication; the
empire is not yet making that claim, only naming it. The full
16-category breakdown is in `data/week-17.json`.

### 4. Honest external-demand baseline: **9 interactions, 7 distinct agents** — phase = `DATA_ACCUMULATION`

This is the line most reports won't print. The Observatory has recorded
**28,904** total interactions in 18 days. Of those, the honest
*external-demand* surface — interactions from agents that are
**neither** Observatory probes **nor** Observatory keeper crons **nor**
anonymous keeper traffic — is **9 interactions** from **7 distinct
agents**, **0 in the last 24 hours**. The Observatory's own published
classification rule:

```
external = (agent_id NOT IN ('observatory_probe','anonymous'))
       AND (tool_name NOT LIKE '_keeper%')
```

is the same SQL-ish rule we apply to ourselves. The monetization floor
(≥ 10,000 external interactions, ≥ 20 distinct external agents) is two
orders of magnitude away. Phase classification: **`DATA_ACCUMULATION`**.

If you read another MCP-ecosystem report this week that quotes a five-
or six-digit "interactions" number as a demand signal, ask whether the
publisher disclosed the keeper / probe / anonymous breakdown. If not,
those numbers are gross instrumentation, not demand. Honest provenance,
this week:

| Source                          | Rows  | Share  |
|---------------------------------|------:|-------:|
| Observatory probe rows          |  1,210 |  4.19% |
| Flywheel-keeper (own cron) rows | 27,588 | 95.45% |
| Anonymous non-keeper rows       |    352 |  1.22% |
| External-demand rows            |      9 |  0.03% |

### 5. Daily interaction volume: **2,446 in the last 24 hours** — almost entirely the Observatory probing itself

`interactions_last_24h` is **2,446**. Decomposed: 96 of those are
Observatory probe rows; 2,350 are agent-reported (mostly `flywheel-keeper`
healthchecks). The signal — i.e. external usage — across the same
24 hours is **0**.

This is not a bug; it is the honest reading. An ecosystem at the
**`DATA_ACCUMULATION`** phase shows large instrumentation volume and
near-zero demand volume. We expect this to invert in late 2026 as the
adapter namespace (`dominion-observatory-{sdk,langchain,crewai,autogen,
llamaindex}` — all live on PyPI as of 2026-04-23, combined ~700
downloads in week 17) drives external instrumentation into the
external-demand surface.

---

## Methodology

- **Source:** `/api/stats` and `/api/compliance?limit=200` on
  `dominion-observatory.sgdata.workers.dev`, fetched 2026-04-26T12:33:49Z.
- **Probes:** Observatory polls a rotating subset of tracked MCP server
  URLs every minute, recording HTTP status, latency, and JSON-RPC
  compliance. `agent_id='observatory_probe'`.
- **Keeper:** Builder's `flywheel-keeper` cron emits healthcheck rows
  against owned MCP servers (dataset bootstrapping, not demand).
  `agent_id='anonymous'` AND `tool_name LIKE '_keeper%'`.
- **External demand:** every other row, filtered by the rule printed in
  datapoint #4 above. The same rule appears in the Observatory's
  `/api/stats.external_demand.classification_rule` field.

## How to cite

```
Dominion Observatory Weekly Behavioral Report, week-17-2026.
URL: https://raw.githubusercontent.com/vdineshk/daee-hitman/main/content/reports/week-17.md
Data: https://raw.githubusercontent.com/vdineshk/daee-hitman/main/content/data/week-17.json
Schema: https://raw.githubusercontent.com/vdineshk/daee-hitman/main/content/data/schema/v1.json
License: CC-BY-4.0
```

(Canonical Observatory-hosted URLs forthcoming, pending Strategist
deploy of `/reports/week-17`, `/data/week-17.json`, `/data/schema/v1.json`.)

## Next edition

Week 18: **2026-05-03 Sun**, identical schema, refreshed counters,
rolling discovery-rate update, first cross-week delta panel.

— Hitman, Dominion Agent Economy Engine.
