# dominion-observatory-autogen

**Microsoft AutoGen (v0.4+) integration for the [Dominion Observatory](https://dominion-observatory.sgdata.workers.dev) — the runtime behavioural trust layer for MCP servers.**

Drop-in wrapper for any `autogen_core.tools.BaseTool` — including MCP-bridged tools from `autogen-ext-mcp` — that adds:

- **Runtime trust telemetry** published to a cross-ecosystem registry of 4,500+ MCP servers.
- **Honest, agent-reported data** — not GitHub stars, not registry manifests.
- **Zero payload leakage** — six fields per report, nothing more.

AutoGen v0.4 standardises on `autogen_core.tools.BaseTool`. Wrapping `run_json` is the one intercept point that covers both native Python tools and MCP-bridged tools, regardless of whether you're driving them from `autogen_agentchat.AssistantAgent`, a raw `ToolAgent`, or your own runtime loop.

---

## Install

```bash
pip install dominion-observatory-autogen
```

Python 3.10 – 3.13. Requires `autogen-core >= 0.4.0` (installed by your project, listed under the `autogen` extra) and `dominion-observatory-sdk >= 0.2.0` (pulled in automatically).

---

## One-line wiring

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from dominion_observatory_autogen import instrument_tool

# Load MCP tools from a server (autogen-ext-mcp style).
raw_tools = await mcp_server_tools(
    StdioServerParams(command="uvx", args=["my-mcp-server"])
)

# Wrap each tool so every call emits a single anonymised Observatory report.
tools = [
    instrument_tool(
        t,
        agent_id="acme-scheduler@1.2.0",
        server_url="https://my-mcp-server.example.com/mcp",
    )
    for t in raw_tools
]

agent = AssistantAgent(
    name="planner",
    model_client=model_client,
    tools=tools,
)
```

Works identically for tools you hand-roll as `BaseTool` subclasses — anything with an async `run_json` is instrumentable.

---

## What gets sent

Exactly these six fields per tool invocation, and nothing else:

| Field         | Example                                         |
| ------------- | ----------------------------------------------- |
| `agent_id`    | `acme-scheduler@1.2.0`                          |
| `server_url`  | `https://my-mcp-server.example.com/mcp`         |
| `success`     | `true` / `false`                                |
| `latency_ms`  | `142`                                           |
| `tool_name`   | `get_holidays`                                  |
| `http_status` | `200` on success, `500` on raised exception     |

Not sent: tool arguments, tool outputs, user IDs, prompts, IP addresses, auth tokens. Satisfies Singapore PDPA and is compatible with EU AI Act Article 12 logging.

On raised exceptions, `success=false` and `http_status=500`; the original exception is re-raised unchanged so your agent's error handling is unaffected.

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

- **Defensive**: every Observatory call is wrapped in a broad `except` so a network hiccup, import failure, or SDK validation error never disturbs the agent loop.
- **Zero side effects on import**: both the `autogen_core` and `dominion_observatory` imports are deferred or optional; this package stays importable without either installed.
- **Transparent wrapper**: `ObservatoryInstrumentedTool` forwards every attribute (`name`, `description`, `schema`, `args_type`, `return_type`) to the inner tool, so any AutoGen code path that introspects a tool keeps working.
- **No telemetry without attribution**: wrapping a tool with `server_url=None` runs the tool normally but emits no report. This is the safe default for local Python tools that have no MCP server identity.
- **Scope**: v0.1.0 covers tool-level instrumentation. A future v0.2.0 will add a streaming helper that consumes `autogen_agentchat.messages.ToolCallExecutionEvent` and derives `server_url` from tool metadata.

---

## Development

```bash
# From the adapter directory:
pip install -e ".[autogen,test]"
pytest
```

---

## Part of the Dominion Agent Economy Engine

This adapter is maintained by the DAEE-HITMAN distribution sub-agent. Source lives at [vdineshk/daee-hitman](https://github.com/vdineshk/daee-hitman) under the MIT licence. File issues there.
