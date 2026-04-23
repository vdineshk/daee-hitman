"""Unit tests for the dominion-observatory-llamaindex MCP tool spec wrapper.

Tests shim two things before importing the adapter under test:

    1. ``dominion_observatory`` (the SDK) — so no real HTTP call is made
       and the SDK need not be installed to run these tests.
    2. ``llama_index.tools.mcp.base`` — a minimal stub ``McpToolSpec`` whose
       ``_create_tool_fn`` hits a fake ``client.call_tool`` recorded on the
       client. This keeps tests hermetic: we do not need llama-index-core,
       llama-index-tools-mcp, or the real ``mcp`` package to verify the
       instrumentation contract.
"""

from __future__ import annotations

import sys
import types
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock

import pytest


# ---------------------------------------------------------------------------
# Shim 1: dominion_observatory SDK
# ---------------------------------------------------------------------------
_report_mock = MagicMock()
_fake_sdk = types.ModuleType("dominion_observatory")
_fake_sdk.report = _report_mock
sys.modules.setdefault("dominion_observatory", _fake_sdk)


# ---------------------------------------------------------------------------
# Shim 2: llama_index.tools.mcp.base.McpToolSpec
# ---------------------------------------------------------------------------
class _FakeCallToolResult:
    """Minimal MCP CallToolResult shim with the ``isError`` attribute."""

    def __init__(self, *, is_error: bool = False, payload: Any = None) -> None:
        self.isError = is_error
        self.payload = payload


class _FakeClient:
    """Minimal ClientSession stand-in.

    Supports ``call_tool(name, kwargs)`` returning either a canned result or
    raising a canned exception. Exposes ``command_or_url`` so server-URL
    inference can be exercised.
    """

    def __init__(
        self,
        *,
        command_or_url: str | None = None,
        result: Any = None,
        raises: Exception | None = None,
    ) -> None:
        if command_or_url is not None:
            self.command_or_url = command_or_url
        self._result = result if result is not None else _FakeCallToolResult()
        self._raises = raises
        self.call_count = 0
        self.last_tool: str | None = None
        self.last_kwargs: Dict[str, Any] | None = None

    async def call_tool(self, tool_name: str, kwargs: Dict[str, Any]) -> Any:
        self.call_count += 1
        self.last_tool = tool_name
        self.last_kwargs = dict(kwargs or {})
        if self._raises is not None:
            raise self._raises
        return self._result


class _StubMcpToolSpec:
    """Shim for llama_index.tools.mcp.base.McpToolSpec.

    Stores the config in the same attribute names the real class uses, so
    the ``instrument_tool_spec`` factory's attribute reads line up.
    """

    def __init__(
        self,
        client: Any,
        allowed_tools: Optional[List[str]] = None,
        global_partial_params: Optional[Dict[str, Any]] = None,
        partial_params_by_tool: Optional[Dict[str, Dict[str, Any]]] = None,
        include_resources: bool = False,
    ) -> None:
        self.client = client
        self.allowed_tools = allowed_tools
        self.global_partial_params = global_partial_params
        self.partial_params_by_tool = partial_params_by_tool
        self.include_resources = include_resources


_base_mod = types.ModuleType("llama_index.tools.mcp.base")
_base_mod.McpToolSpec = _StubMcpToolSpec
_mcp_mod = types.ModuleType("llama_index.tools.mcp")
_mcp_mod.base = _base_mod
_tools_mod = types.ModuleType("llama_index.tools")
_tools_mod.mcp = _mcp_mod
_li_mod = types.ModuleType("llama_index")
_li_mod.tools = _tools_mod
sys.modules.setdefault("llama_index", _li_mod)
sys.modules.setdefault("llama_index.tools", _tools_mod)
sys.modules.setdefault("llama_index.tools.mcp", _mcp_mod)
sys.modules.setdefault("llama_index.tools.mcp.base", _base_mod)


# Import under test AFTER both shims are in place.
from dominion_observatory_llamaindex import (  # noqa: E402
    ObservatoryMcpToolSpec,
    instrument_tool_spec,
)
from dominion_observatory_llamaindex.mcp_instrument import (  # noqa: E402
    _derive_server_url,
    _normalise_server_url,
    _validate_agent_id,
)


@pytest.fixture(autouse=True)
def _reset_report():
    _report_mock.reset_mock()
    _report_mock.side_effect = None
    yield


# ---------------------------------------------------------------------------
# agent_id validation
# ---------------------------------------------------------------------------
def test_validate_agent_id_accepts_plain_string():
    assert _validate_agent_id("acme@1.0.0") == "acme@1.0.0"


def test_validate_agent_id_strips_whitespace():
    assert _validate_agent_id("  acme@1.0.0  ") == "acme@1.0.0"


@pytest.mark.parametrize("bad", ["", "   ", "anonymous", "observatory_probe"])
def test_validate_agent_id_rejects_bad_values(bad):
    with pytest.raises(ValueError):
        _validate_agent_id(bad)


def test_validate_agent_id_rejects_non_string():
    with pytest.raises(TypeError):
        _validate_agent_id(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# server_url helpers
# ---------------------------------------------------------------------------
def test_normalise_server_url_strips_and_nulls_empty():
    assert _normalise_server_url("  https://x/mcp  ") == "https://x/mcp"
    assert _normalise_server_url("") is None
    assert _normalise_server_url("   ") is None
    assert _normalise_server_url(None) is None
    assert _normalise_server_url(42) is None  # type: ignore[arg-type]


def test_derive_server_url_uses_command_or_url_first():
    c = _FakeClient(command_or_url="https://srv/mcp")
    c.url = "https://other/mcp"  # ignored in favour of command_or_url
    assert _derive_server_url(c) == "https://srv/mcp"


def test_derive_server_url_falls_back_to_url_attr():
    c = _FakeClient()
    assert not hasattr(c, "command_or_url")
    c.url = "https://srv/mcp"
    assert _derive_server_url(c) == "https://srv/mcp"


def test_derive_server_url_returns_none_when_no_attr():
    c = _FakeClient()
    assert _derive_server_url(c) is None


# ---------------------------------------------------------------------------
# Construction guards
# ---------------------------------------------------------------------------
def test_constructor_rejects_reserved_agent_id():
    with pytest.raises(ValueError):
        ObservatoryMcpToolSpec(
            client=_FakeClient(command_or_url="https://srv/mcp"),
            agent_id="anonymous",
        )


def test_constructor_auto_derives_server_url_from_client():
    spec = ObservatoryMcpToolSpec(
        client=_FakeClient(command_or_url="https://srv/mcp"),
        agent_id="acme@1.0.0",
    )
    assert spec._server_url == "https://srv/mcp"


def test_constructor_explicit_server_url_wins_over_client_attr():
    spec = ObservatoryMcpToolSpec(
        client=_FakeClient(command_or_url="https://wrong/mcp"),
        agent_id="acme@1.0.0",
        server_url="https://right/mcp",
    )
    assert spec._server_url == "https://right/mcp"


def test_constructor_no_server_url_when_client_has_no_identity():
    spec = ObservatoryMcpToolSpec(
        client=_FakeClient(),  # no command_or_url attr
        agent_id="acme@1.0.0",
    )
    assert spec._server_url is None


def test_constructor_forwards_parent_class_kwargs():
    client = _FakeClient(command_or_url="https://srv/mcp")
    spec = ObservatoryMcpToolSpec(
        client=client,
        agent_id="acme@1.0.0",
        allowed_tools=["only_this"],
        global_partial_params={"k": "v"},
        partial_params_by_tool={"only_this": {"a": 1}},
        include_resources=True,
    )
    assert spec.client is client
    assert spec.allowed_tools == ["only_this"]
    assert spec.global_partial_params == {"k": "v"}
    assert spec.partial_params_by_tool == {"only_this": {"a": 1}}
    assert spec.include_resources is True


# ---------------------------------------------------------------------------
# _create_tool_fn — success path
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_successful_call_emits_single_success_report():
    client = _FakeClient(
        command_or_url="https://srv/mcp",
        result=_FakeCallToolResult(is_error=False, payload={"ok": True}),
    )
    spec = ObservatoryMcpToolSpec(client=client, agent_id="acme@1.0.0")
    fn = spec._create_tool_fn("get_holidays")

    result = await fn(country="SG")

    assert client.call_count == 1
    assert client.last_tool == "get_holidays"
    assert client.last_kwargs == {"country": "SG"}
    assert getattr(result, "isError") is False

    _report_mock.assert_called_once()
    kwargs = _report_mock.call_args.kwargs
    assert kwargs["agent_id"] == "acme@1.0.0"
    assert kwargs["server_url"] == "https://srv/mcp"
    assert kwargs["success"] is True
    assert kwargs["tool_name"] == "get_holidays"
    assert kwargs["http_status"] == 200
    assert isinstance(kwargs["latency_ms"], int) and kwargs["latency_ms"] >= 0


# ---------------------------------------------------------------------------
# _create_tool_fn — MCP-level error (isError=True)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_is_error_result_emits_failure_report_without_raising():
    client = _FakeClient(
        command_or_url="https://srv/mcp",
        result=_FakeCallToolResult(is_error=True, payload={"msg": "tool said no"}),
    )
    spec = ObservatoryMcpToolSpec(client=client, agent_id="acme@1.0.0")
    fn = spec._create_tool_fn("flaky_tool")

    result = await fn(arg="x")

    assert client.call_count == 1
    assert getattr(result, "isError") is True

    _report_mock.assert_called_once()
    kwargs = _report_mock.call_args.kwargs
    assert kwargs["success"] is False
    assert kwargs["http_status"] == 500
    assert kwargs["tool_name"] == "flaky_tool"


# ---------------------------------------------------------------------------
# _create_tool_fn — exception path
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_exception_emits_failure_report_and_propagates():
    boom = RuntimeError("network down")
    client = _FakeClient(command_or_url="https://srv/mcp", raises=boom)
    spec = ObservatoryMcpToolSpec(client=client, agent_id="acme@1.0.0")
    fn = spec._create_tool_fn("search")

    with pytest.raises(RuntimeError, match="network down"):
        await fn(q="hello")

    _report_mock.assert_called_once()
    kwargs = _report_mock.call_args.kwargs
    assert kwargs["success"] is False
    assert kwargs["http_status"] == 500
    assert kwargs["tool_name"] == "search"
    assert kwargs["server_url"] == "https://srv/mcp"


# ---------------------------------------------------------------------------
# _create_tool_fn — no server_url means no report
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_no_server_url_emits_no_report_but_still_runs():
    client = _FakeClient(
        result=_FakeCallToolResult(is_error=False, payload={"ok": True})
    )  # no command_or_url attr
    spec = ObservatoryMcpToolSpec(client=client, agent_id="acme@1.0.0")
    assert spec._server_url is None
    fn = spec._create_tool_fn("anything")

    result = await fn()

    assert client.call_count == 1
    assert getattr(result, "isError") is False
    _report_mock.assert_not_called()


@pytest.mark.asyncio
async def test_no_server_url_swallows_no_report_on_exception_either():
    client = _FakeClient(raises=ValueError("bad arg"))
    spec = ObservatoryMcpToolSpec(client=client, agent_id="acme@1.0.0")
    assert spec._server_url is None
    fn = spec._create_tool_fn("x")

    with pytest.raises(ValueError):
        await fn()

    _report_mock.assert_not_called()


# ---------------------------------------------------------------------------
# Telemetry never breaks the user
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_report_sdk_failure_is_suppressed():
    _report_mock.side_effect = RuntimeError("SDK went sideways")
    client = _FakeClient(
        command_or_url="https://srv/mcp",
        result=_FakeCallToolResult(is_error=False, payload={"ok": True}),
    )
    spec = ObservatoryMcpToolSpec(client=client, agent_id="acme@1.0.0")
    fn = spec._create_tool_fn("resilient")

    # Must not raise even though the SDK mock blows up.
    result = await fn()
    assert getattr(result, "isError") is False


# ---------------------------------------------------------------------------
# instrument_tool_spec factory
# ---------------------------------------------------------------------------
def test_instrument_tool_spec_mirrors_original_config():
    client = _FakeClient(command_or_url="https://srv/mcp")
    original = _StubMcpToolSpec(
        client=client,
        allowed_tools=["a", "b"],
        global_partial_params={"g": 1},
        partial_params_by_tool={"a": {"p": 2}},
        include_resources=True,
    )

    wrapped = instrument_tool_spec(
        original,
        agent_id="acme@1.0.0",
        server_url="https://explicit/mcp",
    )

    assert isinstance(wrapped, ObservatoryMcpToolSpec)
    assert wrapped.client is client
    assert wrapped.allowed_tools == ["a", "b"]
    assert wrapped.global_partial_params == {"g": 1}
    assert wrapped.partial_params_by_tool == {"a": {"p": 2}}
    assert wrapped.include_resources is True
    assert wrapped._server_url == "https://explicit/mcp"
    assert wrapped._agent_id == "acme@1.0.0"


def test_instrument_tool_spec_rejects_non_spec():
    with pytest.raises(TypeError):
        instrument_tool_spec(
            "not a spec", agent_id="acme@1.0.0"  # type: ignore[arg-type]
        )


def test_instrument_tool_spec_derives_server_url_from_client_when_omitted():
    client = _FakeClient(command_or_url="https://srv/mcp")
    original = _StubMcpToolSpec(client=client)
    wrapped = instrument_tool_spec(original, agent_id="acme@1.0.0")
    assert wrapped._server_url == "https://srv/mcp"


# ---------------------------------------------------------------------------
# Version sanity
# ---------------------------------------------------------------------------
def test_version_string_shape():
    import dominion_observatory_llamaindex as mod

    assert isinstance(mod.__version__, str)
    parts = mod.__version__.split(".")
    assert len(parts) == 3 and all(p.isdigit() for p in parts)
