"""Observatory instrumentation for autogen_core.tools.BaseTool.

AutoGen v0.4+ standardises on ``autogen_core.tools.BaseTool`` as the abstract
base for every callable an agent can dispatch to. MCP-backed tools (for
example the ones built by ``autogen-ext-mcp``) are just ``BaseTool``
subclasses, so wrapping ``run_json`` is the one intercept point that covers
both native Python tools and MCP-bridged tools without caring which the user
wired up.

The wrapper measures wall-clock latency, swallows any Observatory SDK error
(telemetry must never break the agent), and emits exactly one report per
invocation with six fields: agent_id, server_url, success, latency_ms,
tool_name, http_status. Nothing else leaves the process.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Mapping


__version__ = "0.1.0"

_LOGGER = logging.getLogger("dominion_observatory_autogen")

_RESERVED_AGENT_IDS = frozenset({"anonymous", "observatory_probe"})


def _validate_agent_id(agent_id: str) -> str:
    if not isinstance(agent_id, str):
        raise TypeError("agent_id must be a string")
    stripped = agent_id.strip()
    if not stripped or stripped in _RESERVED_AGENT_IDS:
        raise ValueError(
            "agent_id must be a non-empty string and not 'anonymous' or "
            "'observatory_probe'."
        )
    return stripped


def _report(
    *,
    agent_id: str,
    server_url: str,
    success: bool,
    latency_ms: int,
    tool_name: str,
    http_status: int | None,
) -> None:
    """Emit a single Observatory report. Never raises.

    The SDK import is deferred so this package stays importable in
    environments where ``dominion-observatory-sdk`` isn't installed (e.g. test
    rigs that shim the symbol).
    """

    try:
        from dominion_observatory import report

        report(
            agent_id=agent_id,
            server_url=server_url,
            success=success,
            latency_ms=int(latency_ms),
            tool_name=tool_name,
            http_status=http_status,
        )
    except Exception as exc:  # noqa: BLE001 — telemetry must never raise
        _LOGGER.debug("observatory report suppressed: %s", exc)


def _best_effort_base_tool_cls() -> type | None:
    """Import ``autogen_core.tools.BaseTool`` if available; return None otherwise.

    Keeping this package importable without autogen-core lets users install
    ``dominion-observatory-autogen`` ahead of the framework (e.g. in a
    layered Dockerfile) and lets the test suite shim a lightweight stand-in.
    """

    try:
        from autogen_core.tools import BaseTool  # type: ignore[import-not-found]

        return BaseTool
    except Exception:  # noqa: BLE001 — any failure is treated as "not installed"
        return None


class ObservatoryInstrumentedTool:
    """Transparent wrapper around any AutoGen tool that implements ``run_json``.

    The wrapper forwards every public attribute access to the inner tool
    (``name``, ``description``, ``schema``, ``return_value_as_string``, etc.)
    so it passes every duck-typing check AutoGen performs. Only ``run_json``
    is intercepted — that is the one method AutoGen's tool-agent loop calls.

    Parameters
    ----------
    tool:
        The wrapped tool instance. Must expose an async ``run_json`` method
        and a ``name`` attribute.
    agent_id:
        Stable identifier for the reporting agent/app. See README for format
        recommendations. Must not be empty, ``"anonymous"``, or
        ``"observatory_probe"``.
    server_url:
        The MCP server URL this tool ultimately calls. When ``None``, the
        wrapper still runs the underlying tool but emits no telemetry, which
        is the safe default for tools that have no corresponding server
        identity (pure local Python functions).
    """

    def __init__(
        self,
        tool: Any,
        *,
        agent_id: str,
        server_url: str | None = None,
    ) -> None:
        if tool is None:
            raise ValueError("tool must not be None")
        if not hasattr(tool, "run_json"):
            raise TypeError(
                "tool must expose an async 'run_json' method "
                "(autogen_core.tools.BaseTool contract)."
            )
        self._tool = tool
        self._agent_id = _validate_agent_id(agent_id)
        self._server_url = server_url.strip() if isinstance(server_url, str) else None
        if self._server_url == "":
            self._server_url = None

    # Forward attribute reads to the inner tool so callers that introspect
    # ``name``/``description``/``schema``/``args_type`` keep working.
    def __getattr__(self, item: str) -> Any:
        # __getattr__ is only called when the attribute is not found on self.
        return getattr(self._tool, item)

    async def run_json(
        self,
        args: Mapping[str, Any],
        cancellation_token: Any | None = None,
        call_id: str | None = None,
    ) -> Any:
        tool_name = getattr(self._tool, "name", None) or type(self._tool).__name__
        started = time.perf_counter()

        try:
            # AutoGen's BaseTool.run_json signature accepts (args, cancellation_token)
            # positionally and an optional call_id kw. We forward whatever was
            # given so both old and new call sites keep working.
            if call_id is not None:
                result = await self._tool.run_json(
                    args, cancellation_token, call_id=call_id
                )
            else:
                result = await self._tool.run_json(args, cancellation_token)
        except Exception:
            latency_ms = int((time.perf_counter() - started) * 1000)
            if self._server_url is not None:
                _report(
                    agent_id=self._agent_id,
                    server_url=self._server_url,
                    success=False,
                    latency_ms=latency_ms,
                    tool_name=tool_name,
                    http_status=500,
                )
            raise

        latency_ms = int((time.perf_counter() - started) * 1000)
        if self._server_url is not None:
            _report(
                agent_id=self._agent_id,
                server_url=self._server_url,
                success=True,
                latency_ms=latency_ms,
                tool_name=tool_name,
                http_status=200,
            )
        return result


def instrument_tool(
    tool: Any,
    *,
    agent_id: str,
    server_url: str | None = None,
) -> ObservatoryInstrumentedTool:
    """Wrap ``tool`` so its ``run_json`` calls report to the Observatory.

    Convenience factory. Equivalent to ``ObservatoryInstrumentedTool(tool,
    agent_id=..., server_url=...)`` but reads more naturally at call sites::

        from dominion_observatory_autogen import instrument_tool

        tool = instrument_tool(
            my_mcp_tool,
            agent_id="acme-scheduler@1.2.0",
            server_url="https://my-mcp-server.example.com/mcp",
        )

        agent = AssistantAgent(
            name="planner",
            model_client=model_client,
            tools=[tool],
        )
    """

    return ObservatoryInstrumentedTool(
        tool, agent_id=agent_id, server_url=server_url
    )
