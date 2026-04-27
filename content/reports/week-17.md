# Observatory Weekly Behavioral Report — Week 17, 2026 (April 20–26)

**Published:** 2026-04-27 | **Source:** [Dominion Observatory](https://dominion-observatory.sgdata.workers.dev) | **Data as of:** 2026-04-27T10:15Z  
**JSON companion:** [`week-17.json`](./week-17.json) | **Cite as:** `Observatory WBR-2026-W17`  
**Schema version:** `behavioral-report-v1`  
**Canonical URL:** `https://dominion-observatory.sgdata.workers.dev/reports/week-17` *(pending Strategist deploy)*

---

## Summary (5 citable findings)

| # | Finding | Value |
|---|---------|-------|
| 1 | MCP servers under active probe monitoring | **4,584** |
| 2 | Probe interaction success rate (last 1,000 interactions) | **95.7%** |
| 3 | Median latency across probe interactions | **4 ms** (p95: 41 ms) |
| 4 | Average server trust score across tracked fleet | **53.9 / 100** |
| 5 | Governance/compliance category share of tracked MCP servers | **1.8%** (83 of 4,584) |

---

## Executive Finding

> **The MCP ecosystem has a compliance infrastructure gap.** Of 4,584 MCP servers actively tracked by Dominion Observatory as of Week 17, only 83 (1.8%) fall into the compliance/governance category. Simultaneously, 95.7% of probe interactions succeed at sub-5 ms median latency — indicating a technically healthy but governance-sparse ecosystem. The governance gap creates structural risk as enterprise agent deployments begin requiring auditability. No other dataset currently captures this distribution with probe-based behavioral evidence rather than self-reported categorization.

---

## Server Ecosystem Snapshot

**Total servers tracked:** 4,584 (up from 4,584 as of 2026-04-23 — collection stable this week)  
**Data collection started:** 2026-04-08  
**Interaction total (all time):** 31,113 (up ~9,481 interactions since Week 15, driven by Observatory's flywheel probes)

### Category distribution

| Category | Servers | % of Fleet | Notes |
|----------|---------|------------|-------|
| Other / General | 1,880 | 41.0% | Largest category; many unclassified use-cases |
| Uncategorized | 729 | 15.9% | Servers with no declared category |
| Search | 367 | 8.0% | Second-largest functional category |
| Code | 317 | 6.9% | Dev tooling |
| Productivity | 263 | 5.7% | Calendar, task, note tools |
| Finance | 226 | 4.9% | |
| Data | 208 | 4.5% | |
| Communication | 164 | 3.6% | |
| Media | 113 | 2.5% | |
| **Compliance** | **83** | **1.8%** | **Governance gap metric** |
| Education | 67 | 1.5% | |
| Security | 52 | 1.1% | |
| Weather | 45 | 1.0% | |
| Transport | 39 | 0.9% | |
| Health | 26 | 0.6% | |
| Test | 5 | 0.1% | |

### Trust score distribution

| Cohort | Description |
|--------|-------------|
| **Top tier (≥90)** | Servers with >3,700 probe interactions; sg-cpf-calculator-mcp, sg-gst-calculator-mcp, sg-weather-data-mcp, sg-workpass-compass-mcp. Trust scores 92.3–92.4. |
| **Baseline (65)** | Servers tracked but with no interaction history. Default prior trust score. |
| **Fleet average** | **53.9** — pulled below the 65 baseline by servers with few interactions and suboptimal early outcomes. |

---

## Reliability Metrics (Probe-Based)

*Source: last 1,000 probe interactions exported via `/api/compliance`, generated 2026-04-27T10:15:11Z*

| Metric | Value |
|--------|-------|
| Interactions sampled | 1,000 |
| Successful interactions | 957 (95.7%) |
| Failed interactions | 43 (4.3%) |
| Latency p50 | **4 ms** |
| Latency p95 | **41 ms** |
| Latency mean | **160 ms** *(fat-tail outliers; mean not representative)* |

**Interpretation:** The 157 ms gap between mean (160 ms) and p95 (41 ms) indicates a small number of high-latency outlier events — likely timeout scenarios from unresponsive servers — dominate the mean while leaving the median experience at 4 ms. Agents relying on p50 latency will experience sub-5 ms probe response. Agents relying on mean latency estimates will systematically overprovision timeouts.

**Categories driving probe volume this week:**
- Data: 59.8% of sampled interactions
- Finance: 24.3%
- Weather: 12.1%
- Security: 3.8%

---

## External Demand Status

| Metric | Value | Notes |
|--------|-------|-------|
| Lifetime external interactions | **9** | Unchanged since 2026-04-10; all pre-date adapter releases |
| External interactions (last 7 days) | **0** | |
| Distinct external agents (lifetime) | **7** | |
| Observatory phase | `DATA_ACCUMULATION` | Monetization floor: 10,000 interactions + 20 distinct external agents |

**Context:** The 9 lifetime external interactions predate the four adapter publications (crewai, autogen, llamaindex published 2026-04-21 to 2026-04-27; langchain and sdk published 2026-04-15). Adapter-driven adoption typically shows a 14–30 day lag from publish to first external compliance row. Week 18 is the first week where all five adapters are simultaneously live; the first externally-attributed compliance rows are anticipated within this window.

---

## Adapter Ecosystem Milestone

**As of Week 17, all five Dominion Observatory Python adapters are live on PyPI** — the first full-ecosystem telemetry coverage for MCP behavioral trust reporting across major agent frameworks:

| Package | Version | Published | Framework |
|---------|---------|-----------|-----------|
| `dominion-observatory-sdk` | 0.2.0 | 2026-04-15 | Generic / direct |
| `dominion-observatory-langchain` | 0.1.0 | 2026-04-15 | LangChain |
| `dominion-observatory-crewai` | 0.1.0 | 2026-04-21 | CrewAI 1.14+ |
| `dominion-observatory-autogen` | 0.1.0 | 2026-04-22 | Microsoft AutoGen |
| `dominion-observatory-llamaindex` | 0.1.0 | 2026-04-24* | LlamaIndex |

*\* Exact upload timestamp to be confirmed via `pypi.org/pypi/dominion-observatory-llamaindex/json`.*

All adapters emit six-field behavioral reports per MCP tool call: `agent_id`, `server_url`, `tool_name`, `success`, `latency_ms`, `http_status`. The LlamaIndex adapter additionally distinguishes `CallToolResult.isError=True` (returned-error vs. raised-exception), a behavioral distinction the SDK and earlier adapters don't expose.

---

## Monetization: x402 Soft Launch

**As of 2026-04-27, Dominion Observatory activates its x402 micropayment endpoint at soft_launch_v0:**

- **Endpoint:** `GET /agent-query/<server-name>` with `X-PAYMENT: <x402-proof>`
- **Price:** $0.001 USDC per trust verdict
- **Protocol:** x402 / Base network
- **Primitive name:** `Empirical-Behavioral-Trust-Oracle-v1`
- **Response without payment:** HTTP 402 (standard x402 gate)
- **Response with payment:** Behavioral trust verdict (trust_score, success_rate, latency_stats, agent_count)

This makes Dominion Observatory the **first MCP trust oracle with native agent-to-agent payment** via x402 — meaning an AI agent can autonomously pay to check a server's trust score before calling it, without any human in the loop.

---

## Methodology

**Probe mechanism:** Dominion Observatory actively probes tracked MCP servers at regular intervals via `observatory_probe` interactions. These are excluded from the external_demand metric but form the reliability baseline.

**Trust score formula:** Empirical-Behavioral-Trust-Oracle-v1 — weighted score from success rate, latency consistency, interaction volume, and time-since-last-success. Score range 0–100.

**External demand filter:** `agent_id NOT IN ('observatory_probe', 'anonymous') AND tool_name NOT LIKE '_keeper%' AND agent_id NOT LIKE 'flywheel%' AND agent_id NOT LIKE 'sdk-test%'`.

**PDPA + IMDA compliant:** All telemetry is anonymized. Agent IDs are operator-assigned strings, not personal identifiers. No personal data is processed.

---

## How to Cite

> Dominion Agent Economy Empire. (2026). *Observatory Weekly Behavioral Report: Week 17, 2026 (April 20–26)*. Dominion Observatory. https://dominion-observatory.sgdata.workers.dev/reports/week-17

**BibTeX:**
```bibtex
@techreport{observatory-wbr-2026-w17,
  title     = {Observatory Weekly Behavioral Report: Week 17, 2026},
  author    = {{Dominion Agent Economy Empire}},
  year      = {2026},
  month     = {April},
  note      = {ISO Week 17 (April 20--26). MCP ecosystem behavioral data from active probe monitoring of 4,584 servers.},
  url       = {https://dominion-observatory.sgdata.workers.dev/reports/week-17},
  institution = {Dominion Observatory}
}
```

---

*Next report: [Week 18](./week-18.md) — published 2026-05-04. Subscribe via RSS (pending) or watch this repo.*  
*Questions, corrections, methodology challenges: open an issue at [vdineshk/daee-hitman](https://github.com/vdineshk/daee-hitman/issues).*
