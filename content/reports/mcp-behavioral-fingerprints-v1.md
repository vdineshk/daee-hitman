# MCP Server Behavioral Fingerprints: A Probe-Based Baseline Dataset for AI Agent Worm Detection

**Published by:** Dominion Observatory  
**Version:** 1.0 (2026-04-28)  
**Data period:** 2026-04-08 to 2026-04-28 (20 days)  
**Observatory endpoint:** https://dominion-observatory.sgdata.workers.dev  
**Machine-readable companion:** [`content/data/mcp-behavioral-fingerprints-v1.json`](../data/mcp-behavioral-fingerprints-v1.json)  
**Schema:** [`content/data/schema/v1.json`](../data/schema/v1.json)  
**License:** MIT

> **Cite this dataset as:** Dominion Observatory, "MCP Server Behavioral Fingerprints v1.0," 2026-04-28, https://github.com/vdineshk/daee-hitman/blob/main/content/reports/mcp-behavioral-fingerprints-v1.md

---

## Abstract

Recent work demonstrates that AI agents using the Model Context Protocol (MCP) are susceptible to worm-style propagation — most notably ClawWorm (2026), which showed that a self-replicating attack can traverse a production MCP ecosystem. A critical gap identified in this literature: "to a traditional SIEM, this behavior is indistinguishable from a worm" (source: behavioral security analysis, 2026). No public behavioral baseline exists against which anomalous MCP server behavior can be compared.

This dataset fills that gap. Using 20 days of probe-collected behavioral data across 4,584 MCP servers (35,117 total interactions as of 2026-04-28), we publish:

1. **Behavioral fingerprint profiles** for MCP servers across three behavioral classes: high-trust, degraded, and compromised-indicative
2. **Deviation thresholds** derived from the healthy baseline that function as candidate Indicators of Compromise (IoC) for worm-style behavioral change
3. **A probe methodology** that any observatory or SIEM operator can replicate

This is, to our knowledge, the first public behavioral baseline dataset for MCP servers designed specifically for worm-detection and anomaly-detection applications.

---

## Background: Why Behavioral Fingerprinting Matters for MCP Worm Detection

### The attack surface

The Model Context Protocol connects AI agents to external tool servers. A compromised MCP server can:
- Return modified tool responses that propagate malicious instructions to connected agents
- Silently redirect agent tool calls to attacker-controlled endpoints
- Inject prompt payloads that cause agents to compromise other servers they connect to

ClawWorm demonstrated that this propagation mechanism is real and operational at production scale in 2026. Cisco's AI Security Framework independently classified 14 MCP-specific threat types, confirming the threat taxonomy is non-trivial.

### The detection gap

Existing detection approaches focus on static analysis (reviewing MCP server source code) or network-layer monitoring (flagging unusual traffic). Neither catches behavioral compromise — a server that passes static analysis and generates normal-looking traffic volumes but has been modified to return subtly different responses.

Behavioral fingerprinting fills this gap. A server's behavioral signature — its success rate distribution, latency profile, tool call response patterns, and authentication behavior — is relatively stable over time and difficult for an attacker to perfectly replicate after compromise. Deviation from the established behavioral fingerprint is a candidate IoC.

### Why Observatory data enables this

Dominion Observatory has collected probe-based behavioral data across 4,584 MCP servers since 2026-04-08. The observatory sends standardized probe calls at regular intervals (96 probes/24h, ~4/hour) and records six behavioral dimensions per interaction: `agent_id`, `server_url`, `success`, `latency_ms`, `tool_name`, `http_status`.

This multi-server, longitudinal, probe-standardized dataset is uniquely suited for behavioral baseline construction. No other public dataset of this scope exists for MCP servers as of publication.

---

## Observatory Methodology

**Probe parameters (as of v1.0):**
- Probe frequency: 96 probes / 24-hour period (~4/hour, 5-minute health-check intervals)
- Agent identifier: `observatory_probe`
- Probe types: health check (`_keeper_healthcheck`, `_keeper_tool:*`) and functional probes
- Data collection period: 2026-04-08 onwards (continuous)
- Total interactions recorded: 35,117 (2026-04-28)
- Total servers in observatory: 4,584
- Directly monitored servers in compliance API (with behavioral profiles): 9 (as of v1.0)

**Six behavioral dimensions recorded per interaction:**

| Dimension | Type | Description |
|---|---|---|
| `agent_id` | string | Identifier of the agent making the call |
| `server_url` | string | MCP server endpoint URL |
| `success` | boolean | Whether the call returned a non-error result |
| `latency_ms` | integer | Round-trip latency in milliseconds |
| `tool_name` | string | MCP tool or method called |
| `http_status` | integer | HTTP response status code |

---

## Behavioral Fingerprint Profiles

### Class A — High-Trust Behavioral Profile (Trust Score ≥ 90)

Derived from 8 continuously-monitored MCP servers over 20 days.

**Representative servers:**
- `sg-cpf-calculator-mcp.sgdata.workers.dev` — trust 92.4, 4,211 interactions
- `sg-workpass-compass-mcp.sgdata.workers.dev` — trust 92.4, 4,210 interactions
- `sg-gst-calculator-mcp.sgdata.workers.dev` — trust 92.4, 4,216 interactions
- `sg-weather-data-mcp.sgdata.workers.dev` — trust 92.4, 4,211 interactions
- `asean-trade-rules-mcp.sgdata.workers.dev` — trust 92.2, 4,194 interactions
- `sg-regulatory-data-mcp.sgdata.workers.dev` — trust 92.1, 4,213 interactions
- `sg-finance-data-mcp.sgdata.workers.dev` — trust 92.1, 4,206 interactions
- `sg-company-lookup-mcp.sgdata.workers.dev` — trust 91.9, 4,195 interactions

**Behavioral fingerprint (Class A baseline):**

| Dimension | Baseline value | Acceptable range | Deviation threshold (IoC candidate) |
|---|---|---|---|
| success_rate | 99.3%–99.9% | ≥ 97.0% | Drop > 3% from 7-day rolling average |
| latency_health_check_ms | 4–6 ms | < 15 ms | > 3× baseline for ≥ 3 consecutive probes |
| latency_functional_ms | 20–58 ms | < 500 ms | > 5× baseline OR > 3,000 ms sustained |
| http_status_distribution | 99.3%+ 2xx | < 3% non-2xx | > 5% non-2xx in any 1-hour window |
| tool_call_distribution | ~98% health, ~2% functional | — | New tool_names absent from prior 7-day history |
| interaction_density_24h | ~210 probes/day | ± 20% | > 50% unexplained drop (server removal indicator) |

**Interpretation:** A Class A server maintaining all six dimensions within the acceptable range has a behavioral fingerprint consistent with an uncompromised, correctly-operating MCP server.

### Class B — Degraded Profile (Trust Score 50–89)

Servers in this range show one or more dimensions outside the Class A acceptable range but do not exhibit the categorical failure pattern of Class C. Degradation may indicate:
- Intermittent infrastructure issues (not compromise)
- Configuration drift
- Partial service degradation

**Behavioral markers:**
- success_rate: 85%–97%
- Latency spikes: 1.5–3× baseline, non-persistent
- http_status: elevated 5xx rate (3%–10%) with intermittent recovery

**Worm-relevance:** Class B alone is insufficient as an IoC. Transition from Class A → Class B, especially combined with new tool_names or authentication pattern changes, is the compound signal.

### Class C — Compromised-Indicative Profile (Trust Score < 50 or categorical failure)

**Reference case from Observatory data:**
- `mcp.byteray.ai/mcp` — 0% success rate, persistent HTTP 401 across all probes, avg latency 31.8ms

**Behavioral pattern:**
- success_rate: 0% (persistent, not intermittent)
- http_status: 100% 4xx/5xx
- Latency: paradoxically normal (server is responding, not silent) — indicates active rejection, not infrastructure outage

**IoC interpretation:** The byteray pattern is consistent with one of:
1. Authentication credential rotation (server replaced, probe credentials no longer valid) — benign
2. Server takeover with authentication substitution — malicious
3. Intentional probe-blocking (operator choice) — benign

**Discriminating factor:** Cross-reference with prior authentication pattern. If the server previously accepted probes and now returns 401 across all probe types simultaneously, the probability of malicious authentication substitution increases significantly. A gradual 401 increase (mixed with 200) indicates credential rotation; a sudden 100% 401 indicates replacement or takeover.

---

## Worm-Detection Indicator Framework

The following IoC framework is derived directly from the Class A baseline. These are **candidate indicators** — correlation with other signals (network-layer anomalies, content-layer analysis) is recommended before attribution.

### IoC-1: Success Rate Collapse
- **Signal:** success_rate drops > 10% within a 2-hour window, measured against 7-day rolling average
- **Threshold:** < 89% success rate for any server previously in Class A
- **Relevance to worm:** A compromised server that begins returning injected responses may have elevated error rates as the injected content causes downstream failures
- **False positive rate:** Low (Class A servers maintain >98% sustained; drops > 10% are rare without infrastructure cause)

### IoC-2: Latency Bifurcation
- **Signal:** Latency distribution splits into two populations (fast health checks, anomalously slow functional calls)
- **Threshold:** functional_call_latency > 5× health_check_latency baseline for ≥ 5 consecutive probes
- **Relevance to worm:** Server processing injected payloads or performing additional malicious operations will incur processing overhead on functional calls but not on health checks (which typically bypass business logic)
- **Reference latency:** health_check baseline = 4–6ms; functional baseline = 20–58ms; alert threshold ≥ 290ms sustained

### IoC-3: New Tool_Name Emergence
- **Signal:** Tool names appearing in probe responses that are absent from the server's prior 7-day call history
- **Threshold:** Any `tool_name` not present in the prior 168-hour window (rolling 7 days)
- **Relevance to worm:** A compromised server may expose new tool surfaces as part of the attack payload — new attack vectors presented as new tools
- **Implementation:** Maintain rolling 7-day `tool_name` vocabulary per server_url; alert on first appearance of new entries

### IoC-4: Authentication Pattern Transition
- **Signal:** Sudden shift from predominantly 2xx to predominantly 4xx responses, especially 401
- **Threshold:** > 80% 401 rate in a 1-hour window for a server previously in Class A
- **Relevance to worm:** Server replacement (malicious endpoint substitution) changes authentication requirements
- **Discriminating factor:** Sudden 100% transition (server replaced) vs. gradual increase (credential rotation)

### IoC-5: Interaction Density Anomaly
- **Signal:** Observatory interaction count drops > 50% or increases > 200% versus 7-day rolling average
- **Threshold:** ± 50% deviation from rolling mean interactions_per_day
- **Relevance to worm:** Unexpected density change may indicate server redirection (traffic being silently rerouted to malicious endpoint) or probe-blocking activation

---

## Ecosystem Context

**Observatory aggregate statistics (2026-04-28):**

| Metric | Value |
|---|---|
| Total MCP servers tracked | 4,584 |
| Total interactions recorded | 35,117 |
| Observatory version | 1.2.0 |
| Average trust score (ecosystem) | 53.9 / 100 |
| Observatory probes total | 1,454 |
| Agent-reported interactions total | 33,976 |
| Data collection start | 2026-04-08 |
| High-trust servers (≥ 90) documented | 8 |
| Anomalous servers (0% success) documented | 1 |

**Ecosystem trust score interpretation:**

The average trust score of 53.9 across 4,584 tracked servers indicates that the majority of MCP servers in the public ecosystem have insufficient behavioral history to establish a definitive profile. This is expected for a young ecosystem. The 8 high-trust servers in the compliance API represent the most deeply profiled behavioral baselines available.

**Significance for worm detection:** The 53.9 average means that most MCP servers do not yet have a behavioral baseline — an attacker replacing a low-profile server faces lower detection risk than an attacker replacing a high-profile server. This represents both a current gap and a future opportunity: as Observatory extends deep profiling to more servers, the worm-detection surface increases.

---

## Relationship to Existing Threat Research

| Research | Contribution | Relationship to this dataset |
|---|---|---|
| ClawWorm (2026) | Demonstrates first production MCP worm attack using MCP standard | This dataset provides the behavioral baseline against which ClawWorm-style behavioral changes can be detected |
| Cisco AI Security Framework (2026) | 14-type MCP threat taxonomy including malware categories | Classification framework; this dataset provides behavioral detection signals for the malware categories |
| MITRE ATT&CK ATLAS | AI/ML adversarial technique framework | This dataset proposes new IoC indicators applicable to ATLAS technique documentation for MCP-specific attacks |
| NIS2 Article 21 (Q3 2026) | EU AI system security measures requirement | This dataset provides the behavioral evidence layer organizations need for NIS2 Article 21 compliance audits of their MCP server dependencies |

---

## Limitations and Future Work

1. **Depth vs. breadth:** The 8 deeply-profiled servers in v1.0 represent a small fraction of the 4,584 tracked servers. Future versions will expand the deep-profile set as behavioral history accumulates.
2. **Probe-only baseline:** The current baseline is probe-generated. Real agent traffic may produce different behavioral signatures. Version 2.0 will incorporate agent-reported interaction data to enrich the fingerprint.
3. **Server-side context unknown:** Observatory observes external behavioral signals only. Correlating with server-side logs would improve attribution confidence.
4. **No ground truth compromised servers:** The IoC thresholds in v1.0 are theoretically derived from the healthy baseline. Future validation requires confirmed compromise cases for calibration.

---

## How to Use This Dataset

**For security researchers:** The behavioral fingerprint profiles and IoC thresholds in this document are the baseline. Replicate the Observatory probe methodology against your MCP server inventory and compare against these thresholds. Any server you profile will either match the Class A fingerprint (low worm risk) or deviate in ways that warrant investigation.

**For SIEM operators:** IoC-1 through IoC-5 are translatable directly to SIEM detection rules (Sigma rule format forthcoming). The observatory_probes_24h = 96 data point provides the probe frequency needed to configure detection windows.

**For NIS2 compliance auditors:** Use this dataset as the behavioral evidence layer for MCP server dependency assessment under Article 21. Each MCP server your organization connects to should have a documented behavioral fingerprint on file.

**For AI framework authors (LangChain, LlamaIndex, AutoGen, CrewAI):** The `dominion-observatory-action` GitHub Action (https://github.com/vdineshk/daee-hitman/tree/main/adapters/dominion-observatory-action) enables automated behavioral fingerprint recording from CI pipelines, making per-server baseline construction a CI artifact rather than a manual research task.

---

## Updates and Versioning

This dataset is updated weekly as part of the Observatory's OBSERVABLE-ECOSYSTEM-CADENCE report series. Version history:
- **v1.0 (2026-04-28):** Initial publication. 8 deeply-profiled servers, 20 days baseline, 5 IoC indicators.
- v2.0 (planned 2026-07-28): Expanded server set, agent-reported interaction integration, calibrated IoC thresholds from confirmed cases.

Live data always available at: https://dominion-observatory.sgdata.workers.dev/api/stats
