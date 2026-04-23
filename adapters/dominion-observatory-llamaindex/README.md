# dominion-observatory-llamaindex

LlamaIndex integration for the [Dominion Observatory](https://dominion-observatory.sgdata.workers.dev) — the behavioural trust layer for the AI agent economy. Instrument `llama_index.tools.mcp.McpToolSpec` so every MCP tool call your LlamaIndex agent makes emits a single six-field runtime telemetry report.

Nothing sensitive ever leaves your process: only `agent_id`, `server_url`, `success`, `latency_ms`, `tool_name`, and `http_status`. No prompts, no tool arguments, no tool outputs, no user IDs, no network metadata. Singapore PDPA compliant, EU AI Act Article 12 compatible.

## Why

The Observatory already watches 4,500+ MCP servers via direct probes + user reports. What it cannot see on its own is what real LlamaIndex agents experience against those servers in production — which tools actually work for which agents at what latency, and which servers quietly fail under real traffic. This adapter closes that gap.

## Install

```bash
pip install 'dominion-observatory-llamaindex[llamaindex]'
```

The `[llamaindex]` extra pulls in `llama-index-tools-mcp>=0.4.0`. The package itself only hard-depends on `dominion-observatory-sdk>=0.2.0`, so it is safe to install first in layered Dockerfiles.

## Usage — drop-in replacement

Swap `McpToolSpec` for `ObservatoryMcpToolSpec`:

```python
from llama_index.tools.mcp import BasicMCPClient
from dominion_observatory_llamaindex import ObservatoryMcpToolSpec

client = BasicMCPClient("https://my-mcp-server.example.com/mcp")

spec = ObservatoryMcpToolSpec(
    client=client,
    agent_id="acme-scheduler@1.2.0",
    # server_url is inferred from client.command_or_url when omitted.
)

tools = await spec.to_tool_list_async()
# Hand `tools` to any LlamaIndex agent (ReActAgent, FunctionAgent, Workflow, etc.).
```

Every tool returned by `to_tool_list_async()` will emit one Observatory report per `call_tool` invocation, whether the call succeeds, fails at the MCP level (`CallToolResult.isError=True`), or raises an exception.

## Usage — wrap an existing spec

If a user already has an `McpToolSpec` somewhere downstream, `instrument_tool_spec` clones its config into an instrumented replacement without touching the original:

```python
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from dominion_observatory_llamaindex import instrument_tool_spec

client = BasicMCPClient("https://my-mcp-server.example.com/mcp")
spec = McpToolSpec(client=client, allowed_tools=["query"])
spec = instrument_tool_spec(
    spec,
    agent_id="acme-scheduler@1.2.0",
)

tools = await spec.to_tool_list_async()
```

## `agent_id` conventions

- Required. Must be a non-empty string.
- The strings `anonymous` and `observatory_probe` are reserved for Observatory internals and are rejected at construction time.
- Recommended shape: `<app>-<role>@<semver>`, e.g. `acme-scheduler@1.2.0`. That way the Observatory can distinguish deploys when you bump versions.

## `server_url` resolution

- If passed explicitly, that value wins.
- Otherwise the wrapper reads `client.command_or_url` (the field `BasicMCPClient` uses), then `client.url`, then `client.server_url`.
- If none of those produce a non-empty string, telemetry is disabled for the spec — tool calls still execute normally. This is the safe default for stdio MCP servers that have no URL identity.

## What is reported

Exactly six fields per invocation, nothing else:

| field         | type   | value                                                      |
|---------------|--------|------------------------------------------------------------|
| `agent_id`    | str    | stable app identifier you passed to the constructor        |
| `server_url`  | str    | MCP server URL (explicit or derived from the client)       |
| `success`     | bool   | `True` if the call returned and `isError` was falsy        |
| `latency_ms`  | int    | wall-clock elapsed around `client.call_tool(...)`          |
| `tool_name`   | str    | the MCP tool name dispatched                                |
| `http_status` | int    | `200` on success, `500` on error (MCP-level or exception) |

## Failure policy

- An exception raised by `call_tool` is caught long enough to emit a `success=False, http_status=500` report, then re-raised unchanged. Your agent code sees the original traceback.
- A report emission failure (network error, SDK import error, SDK bug) is suppressed at DEBUG level. **Telemetry never breaks the agent's critical path.**
- If the Observatory SDK is absent at runtime, the wrapper still runs and logs a one-line DEBUG message per dropped report.

## Privacy posture

- No tool arguments are sent.
- No tool outputs are sent.
- No user IDs, chat history, prompts, or embeddings are sent.
- `agent_id` is opaque to the Observatory — pick any stable identifier that does not personally identify an end-user. Recommended: application build ID.

## Part of the Dominion Agent Economy Empire

This adapter is part of a family:

| Package                             | Framework        | PyPI                                                                  |
|-------------------------------------|------------------|-----------------------------------------------------------------------|
| `dominion-observatory-sdk`          | framework-free   | https://pypi.org/project/dominion-observatory-sdk/                    |
| `dominion-observatory-langchain`    | LangChain        | https://pypi.org/project/dominion-observatory-langchain/              |
| `dominion-observatory-crewai`       | CrewAI           | https://pypi.org/project/dominion-observatory-crewai/                 |
| `dominion-observatory-autogen`      | Microsoft AutoGen| https://pypi.org/project/dominion-observatory-autogen/                |
| `dominion-observatory-llamaindex`   | LlamaIndex       | this package                                                          |

## Licence

MIT. See `LICENSE`.
