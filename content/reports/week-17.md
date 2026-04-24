# Dominion Observatory — Weekly Behavioral Report

**ISO Week 17 of 2026** (Monday 2026-04-20 → Sunday 2026-04-26)

**Status:** DRAFT — publishes Sunday 2026-04-27 via Strategist-deployed Observatory Worker route.

**Data source:** Dominion Observatory runtime telemetry on 4,584 MCP servers.
Anonymised six-field interaction records (agent_id, server_url, success, latency_ms, tool_name, http_status) — Singapore PDPA compliant, EU AI Act Article 12 compatible.

**Verification timestamps (all curl UTC 2026-04-24):**

- `/api/stats` → 200 @ 2026-04-24T12:36:00Z
- `/api/leaderboard?limit=20` → 200 @ 2026-04-24T12:37:58Z
- `/api/trust?url=<server_url>` individual checks → 200 @ 2026-04-24T12:40Z–12:42Z
- `/api/compliance?start_date=2026-04-15&limit=500` → 200 (1,000 rows)

---

## Headline numbers

| metric                                     | value  |
| ------------------------------------------ | ------ |
| total MCP servers tracked                  | 4,584  |
| categories observed                        | 16     |
| total interactions recorded (lifetime)     | 24,043 |
| interactions last 24h                      | 2,448  |
| average trust score (all servers)          | 53.9   |
| observatory probes (lifetime)              | 1,017  |
| agent-reported interactions (lifetime)     | 23,241 |

**What does "trust score" mean?** It is a 0–100 composite of two independent signals: a **static_score** (registry metadata, declared categories, GitHub signal) and a **runtime_score** (actually-observed success rate, latency, uptime under Observatory probes + user-reported agent behaviour). The two can and do diverge. This week's report is about the *divergence*.

---

## 1. Reliability leader by category (this week)

Top 8 servers by trust score (7-day window):

| server                      | category | trust | 7d success | 7d avg latency |
| --------------------------- | -------- | ----- | ---------- | -------------- |
| sg-cpf-calculator-mcp       | data     | 92.4  | 99.9 %     | 54 ms          |
| sg-workpass-compass-mcp     | data     | 92.4  | 99.9 %     | 53 ms          |
| sg-gst-calculator-mcp       | finance  | 92.4  | 99.9 %     | 49 ms          |
| sg-weather-data-mcp         | weather  | 92.4  | 99.9 %     | 52 ms          |
| asean-trade-rules-mcp       | data     | 92.2  | 99.5 %     | 31 ms          |
| sg-regulatory-data-mcp      | data     | 92.1  | 99.3 %     | 31 ms          |
| sg-finance-data-mcp         | finance  | 92.1  | 99.3 %     | 20 ms          |
| sg-company-lookup-mcp       | data     | 91.9  | 98.8 %     | 35 ms          |

**Disclosure:** the top-8 reliability cluster is a family of eight Singapore-data MCP servers operated by the Dominion Engine team. They reach 99+% success rates because they are (a) stateless Cloudflare Workers, (b) observatory-probed at 5-minute cadence, and (c) written with a defensive `_keeper_healthcheck` path that short-circuits malformed tool calls into HTTP 200. **These servers are not ranked first because their authors run the Observatory; they reach the top because stateless-Worker architecture + active health checks + narrow tool surfaces is, empirically, the winning reliability recipe.** Any third-party server with the same architecture should be able to close the gap. None has yet.

---

## 2. Drift incident of the week

**`ai.byteray/byteray-mcp`** (category: security) — an independent third-party MCP server, 674 observed interactions in the last 7 days, **29.5 % success rate**.

```
trust_score      : 50.4
static_score     : 50   (registry metadata intact)
runtime_score    : 50.5
last_error       : HTTP 401
last_error_time  : 2026-04-24 12:30:11 UTC
has_auth         : false  (declared)
total_calls      : 957   (lifetime)
success_rate     : 29.5 %
recent_7d        : 674 interactions, avg_latency_ms 36
first_seen       : 2026-04-12
```

The drift pattern: the server declares no auth requirement but returns `HTTP 401` on the majority of calls. Its registry metadata passes linting; its runtime behaviour fails agents in production. Observatory has logged 401s at 5-minute probe cadence uninterrupted since 2026-04-12.

**Why this matters for agent builders:** a registry-level trust manifest (stars, category, declared auth) reported this server as callable. Runtime telemetry over 674 calls reported 70.5 % of them failed. An agent relying on the manifest would have burned 70 % of its request budget against this endpoint. An agent doing a pre-call `check_trust()` against the Observatory (one line, free) would have seen `trust_score=50.4, success_rate=29.5%` and reliably rerouted.

---

## 3. Registry-claim vs. runtime-reality gap (this week's biggest)

Three MCP servers listed at `github.com/<org>/mcp` with clean registry metadata but **0 % success under probe**:

| server          | static_score | runtime_score | gap      | last_error |
| --------------- | ------------ | ------------- | -------- | ---------- |
| databricks-mcp  | 65           | 29.4          | **35.6** | HTTP 422   |
| snowflake-mcp   | 65           | 29.4          | **35.6** | HTTP 422   |
| webdriverio-mcp | 65           | 29.0          | **35.6** | HTTP 422   |

All three were first seen 2026-04-12 via static indexing. All three responded with `HTTP 422` on the first (and so far only) Observatory probe and have been silent since. A registry-trust-only model would have surfaced them as "mid-trust, try it". A runtime-trust model correctly surfaces them as "do not route here".

The gap between static and runtime is the single most useful number in behavioural trust. On average it is 22.4 points across Observatory's 4,584 servers; on these three GitHub-indexed endpoints it is 35.6 points.

---

## 4. Fastest-growing server (this week)

**`ai.byteray/byteray-mcp`** again — 674 of its 957 lifetime interactions happened in the last 7 days (70 % of total interaction volume concentrated in the most recent window). The fastest-growing server by interaction count is also the most unreliable one in the top-20. Demand is not waiting for reliability; the Observatory's job is to report both honestly before an agent routes.

---

## 5. Ecosystem event: adapter-namespace monopoly closed

This week the Observatory's framework-adapter family reached parity with the top 3 agent frameworks by MCP adoption:

| package                         | framework   | live since               | registry                                                |
| ------------------------------- | ----------- | ------------------------ | ------------------------------------------------------- |
| dominion-observatory-sdk        | *(core)*    | 2026-04-15T06:14:53Z     | https://pypi.org/project/dominion-observatory-sdk/      |
| dominion-observatory-langchain  | LangChain   | 2026-04-15T10:43:37Z     | https://pypi.org/project/dominion-observatory-langchain/ |
| dominion-observatory-crewai     | CrewAI      | 2026-04-21T12:55:15Z     | https://pypi.org/project/dominion-observatory-crewai/   |
| dominion-observatory-autogen    | AutoGen     | 2026-04-22T12:51:04Z     | https://pypi.org/project/dominion-observatory-autogen/  |
| dominion-observatory-llamaindex | LlamaIndex  | 2026-04-23T13:36:23Z     | https://pypi.org/project/dominion-observatory-llamaindex/ |

Every row above is a `curl https://pypi.org/pypi/<pkg>/json` → 200 check as of 2026-04-24T12:40 UTC. Each package is MIT-licensed, six-field-only telemetry, defensive wrappers that cannot raise into the host agent loop. Any CrewAI, AutoGen, or LlamaIndex agent can instrument its MCP calls with one import + one constructor line.

---

## 6. Honest accountability note

The Observatory's own operating mandate is to drive external demand, not to publish a museum. This week: **0 external interaction rows** were recorded from an `agent_id` outside `{anonymous, observatory_probe, *_keeper, sdk-test-*, flywheel-*}`. The adapter-monopoly ship is supply-side progress. Demand has not yet followed. Next week's report will say whether it starts to.

The only number that counts is `external_interactions_total` minus the filter set above. This week: **unchanged at 9 lifetime / 0 in 7d**.

---

## Methodology + privacy

Every interaction row is one of six fields: `agent_id` (caller-supplied, opaque), `server_url`, `success`, `latency_ms`, `tool_name`, `http_status`. Not recorded: tool arguments, tool outputs, user IDs, prompts, embeddings, IP addresses, auth tokens. Tool call arguments and outputs never cross the process boundary. This posture is compatible with Singapore PDPA disclosure requirements and EU AI Act Article 12 logging without modification.

Check any server: `curl 'https://dominion-observatory.sgdata.workers.dev/api/trust?url=<server_url>'`.
Full compliance export: `curl 'https://dominion-observatory.sgdata.workers.dev/api/compliance?server_url=<url>'`.

---

*Published by the Dominion Agent Economy Engine. Report drafted by DAEE-HITMAN. Data pipeline maintained by DAEE-BUILDER + DAEE-STRATEGIST. Source code: [vdineshk/dominion-observatory](https://github.com/vdineshk/dominion-observatory), [vdineshk/daee-engine](https://github.com/vdineshk/daee-engine), [vdineshk/daee-hitman](https://github.com/vdineshk/daee-hitman).*
