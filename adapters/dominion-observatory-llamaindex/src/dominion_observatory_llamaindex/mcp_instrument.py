"""Observatory instrumentation for llama_index.tools.mcp.McpToolSpec.

LlamaIndex's MCP integration ships as ``llama-index-tools-mcp``. The core
surface is ``McpToolSpec``, which turns an ``mcp.client.session.ClientSession``
into a list of ``llama_index.core.tools.function_tool.FunctionTool`` objects.
Internally, each tool is backed by a closure produced by
``McpToolSpec._create_tool_fn(tool_name)`` that awaits
``self.client.call_tool(tool_name, kwargs)`` on the hot path.

That closure is the one intercept point that covers every tool exposed by an
MCP server the LlamaIndex agent can reach, regardless of which agent loop
(ReActAgent, FunctionAgent, Workflow, custom) ultimately dispatches the call.
Subclassing ``McpToolSpec`` and overriding ``_create_tool_fn`` wraps the call
with wall-clock timing + a single Observatory report per invocation.

Telemetry discipline:
    * Exactly six fields per report: agent_id, server_url, success,
      latency_ms, tool_name, http_status. Nothing else ever leaves the
      process.
    * A failure to reach the Observatory (network error, SDK missing, SDK
      bug) is suppressed at DEBUG level — telemetry must never break the
      agent's critical path.
    * An MCP-level error result (``CallToolResult.isError=True``) is treated
      as success=False / http_status=500. An exception raised during the
      call is treated the same way and is then re-raised so the caller sees
      the original traceback unchanged.
    * When ``server_url`` is ``None`` and cannot be inferred from the client,
      no report is emitted — the wrapper is a safe no-op for tool specs that
      have no identifiable server URL.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Callable, Dict, List, Optional


__version__ = "0.1.0"

_LOGGER = logging.getLogger("dominion_observatory_llamaindex")

_RESERVED_AGENT_IDS = frozenset({"anonymous", "observatory_probe"})


# ---------------------------------------------------------------------------
# Parent class resolution
# ---------------------------------------------------------------------------
# ``llama-index-tools-mcp`` is declared as an optional extra so this package
# stays importable in layered Dockerfiles that install the adapter ahead of
# the framework. If the framework is absent at import time we fall back to a
# stub parent class whose constructor refuses to run. The error message
# points the user at the correct extras install.
try:  # pragma: no cover — exercised by framework-present integration path
    from llama_index.tools.mcp.base import McpToolSpec as _McpToolSpec

    _HAS_FRAMEWORK = True
except Exception:  # noqa: BLE001 — any ImportError variant is "not installed"
    _HAS_FRAMEWORK = False

    class _McpToolSpec:  # type: ignore[no-redef]
        """Stub placeholder used when ``llama-index-tools-mcp`` is unavailable."""

        pass


_FRAMEWORK_HINT = (
    "llama-index-tools-mcp>=0.4.0 is required to use ObservatoryMcpToolSpec. "
    "Install with: pip install 'dominion-observatory-llamaindex[llamaindex]'"
)


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
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


def _normalise_server_url(server_url: Optional[str]) -> Optional[str]:
    if server_url is None:
        return None
    if not isinstance(server_url, str):
        return None
    stripped = server_url.strip()
    return stripped or None


def _derive_server_url(client: Any) -> Optional[str]:
    """Best-effort derivation of the server URL from the MCP client.

    ``BasicMCPClient`` exposes ``command_or_url`` — the string the user
    passed when constructing the client. For HTTP/SSE transports this is the
    server URL. For stdio transports it is a command, which is not a valid
    ``server_url`` for Observatory purposes; in that case we still return
    the value so callers can see it, but we rely on the caller to pass an
    explicit ``server_url`` when instrumenting stdio tools.
    """

    for attr in ("command_or_url", "url", "server_url"):
        value = getattr(client, attr, None)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


# ---------------------------------------------------------------------------
# Observatory report
# ---------------------------------------------------------------------------
def _report(
    *,
    agent_id: str,
    server_url: str,
    success: bool,
    latency_ms: int,
    tool_name: str,
    http_status: int,
) -> None:
    """Emit a single Observatory report. Never raises.

    The SDK import is deferred so this package stays importable in
    environments where ``dominion-observatory-sdk`` isn't installed (e.g.
    test rigs that shim the symbol).
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


# ---------------------------------------------------------------------------
# ObservatoryMcpToolSpec
# ---------------------------------------------------------------------------
class ObservatoryMcpToolSpec(_McpToolSpec):  # type: ignore[misc, valid-type]
    """Drop-in replacement for ``McpToolSpec`` that reports to the Observatory.

    Usage::

        from llama_index.tools.mcp import BasicMCPClient
        from dominion_observatory_llamaindex import ObservatoryMcpToolSpec

        client = BasicMCPClient("https://my-mcp-server.example.com/mcp")
        spec = ObservatoryMcpToolSpec(
            client=client,
            agent_id="acme-scheduler@1.2.0",
            # server_url is inferred from client.command_or_url when omitted.
        )
        tools = await spec.to_tool_list_async()

    Parameters
    ----------
    client:
        An ``mcp.client.session.ClientSession`` (typically a
        ``llama_index.tools.mcp.BasicMCPClient``). The parent class already
        validates this.
    agent_id:
        Stable identifier for the reporting agent/app. Must not be empty,
        ``"anonymous"``, or ``"observatory_probe"``.
    server_url:
        The MCP server URL. When ``None`` (default), the wrapper attempts
        ``client.command_or_url`` / ``client.url`` / ``client.server_url``.
        If none of those exist or are strings, telemetry is disabled for
        this spec and tool calls still execute normally.
    allowed_tools, global_partial_params, partial_params_by_tool,
    include_resources:
        Forwarded verbatim to ``McpToolSpec.__init__``.
    """

    def __init__(
        self,
        client: Any,
        *,
        agent_id: str,
        server_url: Optional[str] = None,
        allowed_tools: Optional[List[str]] = None,
        global_partial_params: Optional[Dict[str, Any]] = None,
        partial_params_by_tool: Optional[Dict[str, Dict[str, Any]]] = None,
        include_resources: bool = False,
    ) -> None:
        if not _HAS_FRAMEWORK:
            raise ImportError(_FRAMEWORK_HINT)

        super().__init__(
            client=client,
            allowed_tools=allowed_tools,
            global_partial_params=global_partial_params,
            partial_params_by_tool=partial_params_by_tool,
            include_resources=include_resources,
        )
        self._agent_id = _validate_agent_id(agent_id)

        explicit = _normalise_server_url(server_url)
        self._server_url = explicit if explicit is not None else _derive_server_url(
            client
        )

    # ----- internals ------------------------------------------------------
    def _create_tool_fn(self, tool_name: str) -> Callable:
        """Return an async closure that instruments ``client.call_tool``.

        The closure mirrors the parent class signature (``**kwargs``) and
        preserves both successful return values and exceptions verbatim.
        One Observatory report is emitted per invocation regardless of
        outcome, unless ``self._server_url`` is ``None``.
        """

        agent_id = self._agent_id
        server_url = self._server_url

        async def async_tool_fn(**kwargs: Any) -> Any:
            started = time.perf_counter()
            try:
                result = await self.client.call_tool(tool_name, kwargs)
            except Exception:
                latency_ms = int((time.perf_counter() - started) * 1000)
                if server_url is not None:
                    _report(
                        agent_id=agent_id,
                        server_url=server_url,
                        success=False,
                        latency_ms=latency_ms,
                        tool_name=tool_name,
                        http_status=500,
                    )
                raise

            latency_ms = int((time.perf_counter() - started) * 1000)
            is_error = bool(getattr(result, "isError", False))
            if server_url is not None:
                _report(
                    agent_id=agent_id,
                    server_url=server_url,
                    success=not is_error,
                    latency_ms=latency_ms,
                    tool_name=tool_name,
                    http_status=500 if is_error else 200,
                )
            return result

        return async_tool_fn


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------
def instrument_tool_spec(
    spec: Any,
    *,
    agent_id: str,
    server_url: Optional[str] = None,
) -> ObservatoryMcpToolSpec:
    """Return an ``ObservatoryMcpToolSpec`` mirroring ``spec``'s configuration.

    Useful when user code is already constructing a ``McpToolSpec`` and you
    want to swap in instrumentation without rewriting the surrounding
    call site::

        spec = McpToolSpec(client=client, allowed_tools=["query"])
        spec = instrument_tool_spec(
            spec,
            agent_id="acme-scheduler@1.2.0",
            server_url="https://my-mcp-server.example.com/mcp",
        )
        tools = await spec.to_tool_list_async()

    The returned spec is a fresh instance; the original ``spec`` is left
    untouched. Every configuration field documented on ``McpToolSpec`` is
    forwarded: ``client``, ``allowed_tools``, ``global_partial_params``,
    ``partial_params_by_tool``, ``include_resources``.

    Raises
    ------
    TypeError
        If ``spec`` is not a ``McpToolSpec`` instance (or a subclass).
    ImportError
        If ``llama-index-tools-mcp`` is not installed.
    """

    if not _HAS_FRAMEWORK:
        raise ImportError(_FRAMEWORK_HINT)
    if not isinstance(spec, _McpToolSpec):
        raise TypeError(
            "spec must be a llama_index.tools.mcp.McpToolSpec instance."
        )

    return ObservatoryMcpToolSpec(
        client=spec.client,
        agent_id=agent_id,
        server_url=server_url,
        allowed_tools=spec.allowed_tools,
        global_partial_params=spec.global_partial_params,
        partial_params_by_tool=spec.partial_params_by_tool,
        include_resources=spec.include_resources,
    )
