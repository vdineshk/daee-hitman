"""CrewAI event listener for the Dominion Observatory.

Public surface:
    - ObservatoryCrewAIListener: subclass of crewai.events.BaseEventListener
      that reports MCP tool-execution behaviour (success, latency, error class)
      to the Dominion Observatory via the dominion-observatory-sdk.

Every payload carries exactly six fields: agent_id, server_url, success,
latency_ms, tool_name, http_status. No prompts, tool arguments, tool outputs,
user IDs, or network metadata are ever exfiltrated. This satisfies Singapore
PDPA and is compatible with EU AI Act Article 12 logging.
"""

from dominion_observatory_crewai.listener import (
    ObservatoryCrewAIListener,
    __version__,
)


__all__ = ["ObservatoryCrewAIListener", "__version__"]
