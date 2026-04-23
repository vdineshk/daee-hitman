"""LlamaIndex integration for the Dominion Observatory.

Public surface:
    - ObservatoryMcpToolSpec: a drop-in replacement for
      ``llama_index.tools.mcp.McpToolSpec`` whose generated tool functions
      emit a single Observatory report per ``call_tool`` invocation.
    - instrument_tool_spec(spec, *, agent_id, server_url=None): factory that
      produces an ``ObservatoryMcpToolSpec`` mirroring an existing
      ``McpToolSpec`` instance's configuration (client, allowed_tools,
      partial params, include_resources).

Every payload carries exactly six fields: agent_id, server_url, success,
latency_ms, tool_name, http_status. No prompts, tool arguments, tool outputs,
user IDs, or network metadata are ever exfiltrated. This satisfies Singapore
PDPA and is compatible with EU AI Act Article 12 logging.
"""

from dominion_observatory_llamaindex.mcp_instrument import (
    ObservatoryMcpToolSpec,
    __version__,
    instrument_tool_spec,
)


__all__ = [
    "ObservatoryMcpToolSpec",
    "instrument_tool_spec",
    "__version__",
]
