"""Microsoft AutoGen (v0.4+) integration for the Dominion Observatory.

Public surface:
    - instrument_tool(tool, *, agent_id, server_url): wrap any
      ``autogen_core.tools.BaseTool`` so its ``run_json`` call emits a single
      Observatory report per invocation.
    - ObservatoryInstrumentedTool: the underlying wrapper class, suitable for
      direct subclassing or manual instantiation.

Every payload carries exactly six fields: agent_id, server_url, success,
latency_ms, tool_name, http_status. No prompts, tool arguments, tool outputs,
user IDs, or network metadata are ever exfiltrated. This satisfies Singapore
PDPA and is compatible with EU AI Act Article 12 logging.
"""

from dominion_observatory_autogen.tool_instrument import (
    ObservatoryInstrumentedTool,
    __version__,
    instrument_tool,
)


__all__ = [
    "ObservatoryInstrumentedTool",
    "instrument_tool",
    "__version__",
]
