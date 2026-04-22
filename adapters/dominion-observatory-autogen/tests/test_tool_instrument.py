"""Unit tests for the dominion-observatory-autogen tool wrapper.

These tests patch the ``dominion_observatory.report`` symbol so no real HTTP
call is made and so the tests do not require the SDK to be installed. The
wrapped tools are duck-typed stand-ins that match ``autogen_core.tools.BaseTool``
surface the wrapper actually depends on (``name`` + async ``run_json``).
"""

from __future__ import annotations

import sys
import types
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# Shim the dominion_observatory SDK so tests don't make a real HTTP call and
# don't depend on the SDK being installed.
# ---------------------------------------------------------------------------
_report_mock = MagicMock()
_fake_sdk = types.ModuleType("dominion_observatory")
_fake_sdk.report = _report_mock
sys.modules.setdefault("dominion_observatory", _fake_sdk)

# Import under test AFTER the shim is in place.
from dominion_observatory_autogen import (  # noqa: E402
    ObservatoryInstrumentedTool,
    instrument_tool,
)
from dominion_observatory_autogen.tool_instrument import _validate_agent_id  # noqa: E402


# ---------------------------------------------------------------------------
# Duck-typed tool stubs — we don't import autogen_core for unit tests.
# ---------------------------------------------------------------------------
class _FakeTool:
    def __init__(self, *, name: str = "get_holidays", raises: Exception | None = None):
        self.name = name
        self.description = f"stub {name} tool"
        self._raises = raises
        self.call_count = 0
        self.last_args: dict | None = None
        self.last_call_id: str | None = None

    async def run_json(self, args, cancellation_token=None, call_id=None):
        self.call_count += 1
        self.last_args = dict(args) if args is not None else None
        self.last_call_id = call_id
        if self._raises is not None:
            raise self._raises
        return {"ok": True, "echo": self.last_args}


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
# Construction guards
# ---------------------------------------------------------------------------
def test_constructor_rejects_none_tool():
    with pytest.raises(ValueError):
        ObservatoryInstrumentedTool(None, agent_id="acme@1.0.0")  # type: ignore[arg-type]


def test_constructor_rejects_tool_without_run_json():
    class _NoRunJson:
        name = "oops"

    with pytest.raises(TypeError):
        ObservatoryInstrumentedTool(_NoRunJson(), agent_id="acme@1.0.0")


def test_constructor_rejects_reserved_agent_id():
    with pytest.raises(ValueError):
        ObservatoryInstrumentedTool(_FakeTool(), agent_id="anonymous")


# ---------------------------------------------------------------------------
# Attribute forwarding
# ---------------------------------------------------------------------------
def test_wrapper_forwards_attribute_access_to_inner_tool():
    inner = _FakeTool(name="lookup_company")
    wrapped = instrument_tool(inner, agent_id="acme@1.0.0")
    assert wrapped.name == "lookup_company"
    assert wrapped.description == "stub lookup_company tool"


# ---------------------------------------------------------------------------
# Successful invocation
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_successful_call_emits_single_success_report():
    inner = _FakeTool(name="get_holidays")
    wrapped = instrument_tool(
        inner,
        agent_id="acme@1.0.0",
        server_url="https://example.com/mcp",
    )
    result = await wrapped.run_json({"country": "SG"}, None)
    assert result == {"ok": True, "echo": {"country": "SG"}}
    assert inner.call_count == 1
    assert inner.last_args == {"country": "SG"}

    _report_mock.assert_called_once()
    kwargs = _report_mock.call_args.kwargs
    assert kwargs["agent_id"] == "acme@1.0.0"
    assert kwargs["server_url"] == "https://example.com/mcp"
    assert kwargs["success"] is True
    assert kwargs["tool_name"] == "get_holidays"
    assert kwargs["http_status"] == 200
    assert isinstance(kwargs["latency_ms"], int)
    assert kwargs["latency_ms"] >= 0


@pytest.mark.asyncio
async def test_call_id_forwarded_when_provided():
    inner = _FakeTool()
    wrapped = instrument_tool(
        inner,
        agent_id="acme@1.0.0",
        server_url="https://example.com/mcp",
    )
    await wrapped.run_json({}, None, call_id="abc-123")
    assert inner.last_call_id == "abc-123"


# ---------------------------------------------------------------------------
# Failure path
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_exception_emits_failure_report_and_reraises():
    boom = RuntimeError("server down")
    inner = _FakeTool(name="get_holidays", raises=boom)
    wrapped = instrument_tool(
        inner,
        agent_id="acme@1.0.0",
        server_url="https://example.com/mcp",
    )
    with pytest.raises(RuntimeError, match="server down"):
        await wrapped.run_json({"country": "SG"}, None)

    _report_mock.assert_called_once()
    kwargs = _report_mock.call_args.kwargs
    assert kwargs["success"] is False
    assert kwargs["http_status"] == 500
    assert kwargs["tool_name"] == "get_holidays"
    assert kwargs["server_url"] == "https://example.com/mcp"


# ---------------------------------------------------------------------------
# server_url gating
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_no_server_url_means_no_report_on_success():
    inner = _FakeTool()
    wrapped = instrument_tool(inner, agent_id="acme@1.0.0", server_url=None)
    result = await wrapped.run_json({}, None)
    assert result == {"ok": True, "echo": {}}
    _report_mock.assert_not_called()


@pytest.mark.asyncio
async def test_no_server_url_means_no_report_on_failure():
    boom = ValueError("bad args")
    inner = _FakeTool(raises=boom)
    wrapped = instrument_tool(inner, agent_id="acme@1.0.0", server_url=None)
    with pytest.raises(ValueError):
        await wrapped.run_json({}, None)
    _report_mock.assert_not_called()


@pytest.mark.asyncio
async def test_empty_server_url_treated_as_none():
    inner = _FakeTool()
    wrapped = instrument_tool(inner, agent_id="acme@1.0.0", server_url="   ")
    await wrapped.run_json({}, None)
    _report_mock.assert_not_called()


# ---------------------------------------------------------------------------
# Defensive behaviour — SDK failures must never propagate
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_sdk_exception_is_swallowed_on_success_path():
    _report_mock.side_effect = RuntimeError("network down")
    inner = _FakeTool()
    wrapped = instrument_tool(
        inner,
        agent_id="acme@1.0.0",
        server_url="https://example.com/mcp",
    )
    # Must not raise.
    result = await wrapped.run_json({}, None)
    assert result == {"ok": True, "echo": {}}
    _report_mock.assert_called_once()


@pytest.mark.asyncio
async def test_sdk_exception_is_swallowed_on_failure_path():
    _report_mock.side_effect = RuntimeError("network down")
    inner = _FakeTool(raises=ValueError("bad"))
    wrapped = instrument_tool(
        inner,
        agent_id="acme@1.0.0",
        server_url="https://example.com/mcp",
    )
    # The ValueError from the inner tool must propagate unchanged; the SDK
    # failure must not mask it.
    with pytest.raises(ValueError, match="bad"):
        await wrapped.run_json({}, None)
    _report_mock.assert_called_once()
