# dominion-observatory-crewai

**CrewAI integration for the [Dominion Observatory](https://dominion-observatory.sgdata.workers.dev) — the runtime behavioural trust layer for MCP servers.**

Drop-in event listener for any CrewAI Crew, Flow, or Agent that calls MCP tools. Your MCP calls get:

- **Runtime trust telemetry** published to a cross-ecosystem registry of 4,500+ MCP servers.
- **Honest, agent-reported data** — not GitHub stars, not registry manifests.
- **Zero payload leakage** — six fields per report, nothing more.

CrewAI 1.x ships a first-class event bus and first-class MCP primitives. This adapter just connects them.

---

## Install

```bash
pip install dominion-observatory-crewai
```

Python 3.10 – 3.13. Requires `crewai >= 1.0.0` (installed by your project) and `dominion-observatory-sdk >= 0.2.0` (pulled in automatically).

---

## One-line wiring

```python
from dominion_observatory_crewai import ObservatoryCrewAIListener

# Instantiate once at process start — the listener auto-registers on
# CrewAI's singleton event bus.
observatory = ObservatoryCrewAIListener(agent_id="acme-scheduler@1.2.0")

crew.kickoff(inputs={...})
```

Every `MCPToolExecutionCompletedEvent`, `MCPToolExecutionFailedEvent`, and `MCPConnectionFailedEvent` CrewAI emits is translated into a single `dominion_observatory.report(...)` call.

---

## What gets sent

Exactly these six fields per event, and nothing else:

| Field         | Example                                         |
| ------------- | ----------------------------------------------- |
| `agent_id`    | `acme-scheduler@1.2.0`                          |
| `server_url`  | `https://my-mcp-server.example.com/mcp`         |
| `success`     | `true` / `false`                                |
| `latency_ms`  | `142`                                           |
| `tool_name`   | `get_holidays`                                  |
| `http_status` | `200` / `504` / `401` / ...                     |

Not sent: tool arguments, tool outputs, user IDs, prompts, IP addresses, auth tokens. Satisfies Singapore PDPA and is compatible with EU AI Act Article 12 logging.

For failures, CrewAI's MCP `error_type` taxonomy (`timeout`, `authentication`, `validation`, `network`, `server_error`) is mapped to an HTTP-ish status code so the Observatory can bucket failure modes without receiving any error string.

---

## Choosing a stable `agent_id`

Required by `dominion-observatory-sdk >= 0.2.0`. Must be non-empty and not `"anonymous"` or `"observatory_probe"`.

Recommended patterns:

- `"my-app@1.0.0"` — package-name + version (stable across restarts).
- `str(uuid.uuid4())` persisted to disk on first run (stable per install).
- `f"{environ['HOSTNAME']}/my-service"` — per-deployment.

Do **not** use per-request IDs — you will fragment your own trust history.

---

## Design notes

- **Defensive**: every Observatory call is wrapped in a broad `except` so a network hiccup, import failure, or SDK validation error never disturbs the running Crew.
- **Zero side effects on import**: the `dominion_observatory` SDK is imported lazily inside the report helper.
- **Selective scope**: v0.1.0 hooks only MCP events. Non-MCP `ToolUsageFinishedEvent` coverage is planned for v0.2.0 with an opt-in metadata key.
- **Singleton-safe**: CrewAI's event bus is a global singleton; instantiating the listener more than once registers duplicate handlers. Call it once at process start.

---

## Development

```bash
# From the adapter directory:
pip install -e ".[crewai,test]"
pytest
```

---

## Part of the Dominion Agent Economy Engine

This adapter is maintained by the DAEE-HITMAN distribution sub-agent. Source lives at [vdineshk/daee-hitman](https://github.com/vdineshk/daee-hitman) under the MIT licence. File issues there.
