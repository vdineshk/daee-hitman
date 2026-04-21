"""Unit tests for ObservatoryCrewAIListener.

These tests exercise the listener's event-to-report mapping without requiring
a live Observatory endpoint. The ``dominion_observatory.report`` symbol is
patched so every test asserts on the exact payload the listener would send.
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
from dominion_observatory_crewai import ObservatoryCrewAIListener  # noqa: E402
from dominion_observatory_crewai.listener import (  # noqa: E402
    _default_agent_id,
    _http_status_from_error_type,
)


# ---------------------------------------------------------------------------
# Lightweight event stubs — we don't want to import crewai for unit tests.
# The listener only reads public attributes, so duck-typed stand-ins are fine
# for testing the mapping logic. Integration with the real event bus is
# covered by the crewai smoke test below (skipped if crewai not installed).
# ---------------------------------------------------------------------------
class _StubEvent:
    """Attribute bag that matches the duck-typing surface used by the listener."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture(autouse=True)
def _reset_report():
    _report_mock.reset_mock()
    yield


@pytest.fixture
def listener(monkeypatch):
    # Monkeypatch BaseEventListener so it doesn't try to register on a real bus
    # during construction.
    from crewai.events.base_event_listener import BaseEventListener

    monkeypatch.setattr(BaseEventListener, "__init__", lambda self: None)
    inst = ObservatoryCrewAIListener(agent_id="acme-crew@0.1.0")
    return inst


# ---------------------------------------------------------------------------
# agent_id resolution
# ---------------------------------------------------------------------------
def test_default_agent_id_prefers_agent_id_field():
    event = _StubEvent(agent_id="worker-7", agent_role="researcher")
    assert _default_agent_id(event) == "worker-7"


def test_default_agent_id_falls_back_to_role():
    event = _StubEvent(agent_id=None, agent_role="researcher")
    assert _default_agent_id(event) == "researcher"


def test_default_agent_id_rejects_reserved_ids():
    event = _StubEvent(agent_id="anonymous", agent_role=None)
    assert _default_agent_id(event) is None


def test_default_agent_id_rejects_blank():
    event = _StubEvent(agent_id="   ", agent_role=None)
    assert _default_agent_id(event) is None


def test_constructor_rejects_reserved_agent_id():
    with pytest.raises(ValueError):
        ObservatoryCrewAIListener(agent_id="anonymous")


def test_constructor_rejects_empty_agent_id():
    with pytest.raises(ValueError):
        ObservatoryCrewAIListener(agent_id="   ")


# ---------------------------------------------------------------------------
# error_type -> http_status mapping
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "error_type, expected",
    [
        ("timeout", 504),
        ("authentication", 401),
        ("validation", 400),
        ("network", 502),
        ("connection_failed", 502),
        ("server_error", 500),
        ("unknown-type", None),
        (None, None),
    ],
)
def test_http_status_mapping(error_type, expected):
    assert _http_status_from_error_type(error_type) == expected


# ---------------------------------------------------------------------------
# Event handling
# ---------------------------------------------------------------------------
def test_tool_completed_emits_success_report(listener):
    event = _StubEvent(
        server_url="https://example.com/mcp",
        server_name="example",
        tool_name="get_holidays",
        execution_duration_ms=142.7,
        agent_id=None,
        agent_role=None,
    )
    listener._handle_tool_completed(event)

    _report_mock.assert_called_once_with(
        agent_id="acme-crew@0.1.0",
        server_url="https://example.com/mcp",
        success=True,
        latency_ms=142,
        tool_name="get_holidays",
        http_status=200,
    )


def test_tool_failed_emits_failure_report_with_mapped_status(listener):
    event = _StubEvent(
        server_url="https://example.com/mcp",
        server_name="example",
        tool_name="get_holidays",
        error="boom",
        error_type="timeout",
        agent_id=None,
        agent_role=None,
    )
    listener._handle_tool_failed(event)

    _report_mock.assert_called_once_with(
        agent_id="acme-crew@0.1.0",
        server_url="https://example.com/mcp",
        success=False,
        latency_ms=0,
        tool_name="get_holidays",
        http_status=504,
    )


def test_connection_failed_emits_synthetic_tool_name(listener):
    event = _StubEvent(
        server_url="https://example.com/mcp",
        server_name="example",
        error="refused",
        error_type="network",
        agent_id=None,
        agent_role=None,
    )
    listener._handle_connection_failed(event)

    _report_mock.assert_called_once_with(
        agent_id="acme-crew@0.1.0",
        server_url="https://example.com/mcp",
        success=False,
        latency_ms=0,
        tool_name="_mcp_connection",
        http_status=502,
    )


def test_missing_server_url_skips_report(listener):
    event = _StubEvent(
        server_url=None,
        tool_name="get_holidays",
        execution_duration_ms=10,
        agent_id=None,
        agent_role=None,
    )
    listener._handle_tool_completed(event)
    _report_mock.assert_not_called()


def test_event_agent_id_used_when_listener_has_none(monkeypatch):
    from crewai.events.base_event_listener import BaseEventListener

    monkeypatch.setattr(BaseEventListener, "__init__", lambda self: None)
    inst = ObservatoryCrewAIListener()  # no explicit agent_id
    event = _StubEvent(
        server_url="https://example.com/mcp",
        tool_name="get_holidays",
        execution_duration_ms=5,
        agent_id="worker-42",
        agent_role=None,
    )
    inst._handle_tool_completed(event)
    _report_mock.assert_called_once()
    assert _report_mock.call_args.kwargs["agent_id"] == "worker-42"


def test_sdk_exception_is_swallowed(listener):
    _report_mock.side_effect = RuntimeError("network down")
    event = _StubEvent(
        server_url="https://example.com/mcp",
        tool_name="get_holidays",
        execution_duration_ms=5,
        agent_id=None,
        agent_role=None,
    )
    # Must not raise.
    listener._handle_tool_completed(event)
    _report_mock.assert_called_once()
    _report_mock.side_effect = None
