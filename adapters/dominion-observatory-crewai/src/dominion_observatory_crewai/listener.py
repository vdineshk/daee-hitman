"""ObservatoryCrewAIListener — CrewAI event listener that reports MCP tool
execution outcomes to the Dominion Observatory.

The listener subscribes to the four MCP-scoped events CrewAI >= 1.0 emits on
its event bus (``crewai.events.types.mcp_events``) and turns each one into a
single ``dominion_observatory.report`` call.

It is deliberately defensive: every Observatory call is wrapped so an import
error, network hiccup, or SDK validation failure never propagates back into
the user's Crew. The listener logs at DEBUG and keeps the crew running.
"""

from __future__ import annotations

import logging
from typing import Any

from crewai.events.base_event_listener import BaseEventListener
from crewai.events.event_bus import CrewAIEventsBus
from crewai.events.types.mcp_events import (
    MCPConnectionFailedEvent,
    MCPToolExecutionCompletedEvent,
    MCPToolExecutionFailedEvent,
)


__version__ = "0.1.0"

_LOGGER = logging.getLogger("dominion_observatory_crewai")

_CONNECTION_TOOL_NAME = "_mcp_connection"
_RESERVED_AGENT_IDS = frozenset({"anonymous", "observatory_probe"})


def _default_agent_id(event: Any) -> str | None:
    """Best-effort extraction of a stable agent_id from a CrewAI MCP event.

    The dominion-observatory-sdk (>=0.2.0) requires a non-empty, non-reserved
    agent_id. We prefer the caller's explicit configuration; if none was
    provided we derive one from the event's agent_role, falling back to the
    agent_id field on the event itself.
    """

    candidate = getattr(event, "agent_id", None) or getattr(event, "agent_role", None)
    if not candidate:
        return None
    candidate = str(candidate).strip()
    if not candidate or candidate in _RESERVED_AGENT_IDS:
        return None
    return candidate


def _http_status_from_error_type(error_type: str | None) -> int | None:
    """Map CrewAI's MCP error_type taxonomy to an HTTP-ish status code.

    Observatory's payload schema includes an optional ``http_status`` field. We
    report a best-effort code so Observatory's aggregations bucket the failure
    reason without us shipping the raw error string.
    """

    if not error_type:
        return None
    t = error_type.strip().lower()
    if t in {"timeout"}:
        return 504
    if t in {"authentication", "auth", "unauthorized"}:
        return 401
    if t in {"validation"}:
        return 400
    if t in {"network", "connection_failed", "connection_error"}:
        return 502
    if t in {"server_error", "internal"}:
        return 500
    return None


class ObservatoryCrewAIListener(BaseEventListener):
    """CrewAI event listener that publishes MCP telemetry to the Observatory.

    Usage
    -----
    ::

        from dominion_observatory_crewai import ObservatoryCrewAIListener

        # Instantiate once at process start; the listener auto-registers on
        # CrewAI's singleton event bus.
        listener = ObservatoryCrewAIListener(agent_id="acme-scheduler@1.2.0")

        crew.kickoff(...)

    Parameters
    ----------
    agent_id:
        Stable identifier for the reporting agent/app. Required by the
        dominion-observatory-sdk >= 0.2.0. Must not be empty, ``"anonymous"``,
        or ``"observatory_probe"``. If omitted, the listener falls back to the
        per-event ``agent_role``/``agent_id`` fields; events lacking both are
        silently skipped.
    verbose:
        When True, emit an INFO log line per report. Defaults to False.
    """

    verbose: bool = False

    def __init__(self, agent_id: str | None = None, *, verbose: bool = False) -> None:
        self._agent_id: str | None = None
        if agent_id is not None:
            agent_id = agent_id.strip()
            if not agent_id or agent_id in _RESERVED_AGENT_IDS:
                raise ValueError(
                    "agent_id must be a non-empty string and not 'anonymous' or "
                    "'observatory_probe'."
                )
            self._agent_id = agent_id

        self.verbose = verbose
        # BaseEventListener.__init__ calls setup_listeners + validate.
        super().__init__()

    # ------------------------------------------------------------------
    # Core emission helper
    # ------------------------------------------------------------------
    def _report(
        self,
        *,
        agent_id: str,
        server_url: str,
        success: bool,
        latency_ms: int,
        tool_name: str,
        http_status: int | None = None,
    ) -> None:
        """Send a single interaction to the Observatory.

        Wrapped defensively — any exception from the SDK is swallowed so the
        user's Crew is never disturbed by telemetry failure.
        """

        try:
            # Deferred import keeps the package importable even if the SDK is
            # missing at runtime (CrewAI users may install this package and
            # test-mock the SDK).
            from dominion_observatory import report

            report(
                agent_id=agent_id,
                server_url=server_url,
                success=success,
                latency_ms=int(latency_ms),
                tool_name=tool_name,
                http_status=http_status,
            )
            if self.verbose:
                _LOGGER.info(
                    "observatory report sent agent_id=%s server_url=%s tool=%s "
                    "success=%s latency_ms=%s http_status=%s",
                    agent_id,
                    server_url,
                    tool_name,
                    success,
                    latency_ms,
                    http_status,
                )
        except Exception as exc:  # noqa: BLE001 — telemetry must never raise
            _LOGGER.debug("observatory report suppressed: %s", exc)

    # ------------------------------------------------------------------
    # Listener wiring
    # ------------------------------------------------------------------
    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(MCPToolExecutionCompletedEvent)
        def _on_mcp_tool_completed(source: Any, event: MCPToolExecutionCompletedEvent) -> None:
            self._handle_tool_completed(event)

        @crewai_event_bus.on(MCPToolExecutionFailedEvent)
        def _on_mcp_tool_failed(source: Any, event: MCPToolExecutionFailedEvent) -> None:
            self._handle_tool_failed(event)

        @crewai_event_bus.on(MCPConnectionFailedEvent)
        def _on_mcp_connection_failed(source: Any, event: MCPConnectionFailedEvent) -> None:
            self._handle_connection_failed(event)

    # ------------------------------------------------------------------
    # Individual event handlers — kept small and testable
    # ------------------------------------------------------------------
    def _handle_tool_completed(self, event: MCPToolExecutionCompletedEvent) -> None:
        agent_id = self._agent_id or _default_agent_id(event)
        server_url = getattr(event, "server_url", None)
        tool_name = getattr(event, "tool_name", None)
        if not (agent_id and server_url and tool_name):
            return

        latency_raw = getattr(event, "execution_duration_ms", None) or 0
        try:
            latency_ms = max(int(latency_raw), 0)
        except (TypeError, ValueError):
            latency_ms = 0

        self._report(
            agent_id=agent_id,
            server_url=server_url,
            success=True,
            latency_ms=latency_ms,
            tool_name=tool_name,
            http_status=200,
        )

    def _handle_tool_failed(self, event: MCPToolExecutionFailedEvent) -> None:
        agent_id = self._agent_id or _default_agent_id(event)
        server_url = getattr(event, "server_url", None)
        tool_name = getattr(event, "tool_name", None)
        if not (agent_id and server_url and tool_name):
            return

        http_status = _http_status_from_error_type(getattr(event, "error_type", None))

        self._report(
            agent_id=agent_id,
            server_url=server_url,
            success=False,
            latency_ms=0,
            tool_name=tool_name,
            http_status=http_status,
        )

    def _handle_connection_failed(self, event: MCPConnectionFailedEvent) -> None:
        agent_id = self._agent_id or _default_agent_id(event)
        server_url = getattr(event, "server_url", None)
        if not (agent_id and server_url):
            return

        http_status = _http_status_from_error_type(getattr(event, "error_type", None))

        self._report(
            agent_id=agent_id,
            server_url=server_url,
            success=False,
            latency_ms=0,
            tool_name=_CONNECTION_TOOL_NAME,
            http_status=http_status,
        )
