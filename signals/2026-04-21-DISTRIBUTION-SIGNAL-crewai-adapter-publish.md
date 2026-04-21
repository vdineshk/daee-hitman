---
signal_type: DISTRIBUTION_REQUEST
origin: DAEE-HITMAN
run: 2026-04-21 RUN-001
target_agents: [CEO/Dinesh]
deadline: 2026-04-24
conviction: 7/10
kill_date: 2026-05-12
---

# Action required: publish `dominion-observatory-crewai` v0.1.0 to PyPI

## What

Hitman v1 RUN-001 shipped `adapters/dominion-observatory-crewai/` — a CrewAI
`BaseEventListener` subclass that converts CrewAI's `MCPToolExecutionCompletedEvent`,
`MCPToolExecutionFailedEvent`, and `MCPConnectionFailedEvent` into Observatory
`report(...)` calls. 20/20 tests pass against real `crewai==1.14.2` event types
on Python 3.11.

Namespace pre-check (verified 2026-04-21T12:19 UTC):

- `pypi.org/pypi/dominion-observatory-crewai/json` — **404 (free namespace)**
- `pypi.org/pypi/dominion-observatory-sdk/json` — 200 / v0.2.0 / uploaded 2026-04-15T06:14:53Z
- `pypi.org/pypi/dominion-observatory-langchain/json` — 200 / v0.1.0 / uploaded 2026-04-15T10:43:37Z

## Why this is a kill move

CrewAI has 100K+ certified developers and a native MCP event surface since
1.0. Observatory already has the SDK + LangChain adapter shipped; the CrewAI
slot is **uncontested and strategically adjacent**. Every install of this
package is a permanent telemetry pipeline that SPIDER / Strategist cannot
backfill. `EXTERNAL_DEMAND_COUNT` is gated on getting this into agents, not on
building more Worker features.

## Exact 2-min Dinesh action

1. From local `daee-hitman` checkout on this branch:
   ```
   cd adapters/dominion-observatory-crewai
   python -m pip install build twine
   python -m build
   python -m twine upload dist/*
   ```
2. Confirm live:
   ```
   curl -sS 'https://pypi.org/pypi/dominion-observatory-crewai/json' | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['version'])"
   ```
   Expect `0.1.0`.
3. Reply with timestamp + upload_time returned by PyPI.

## Success metric (kill 2026-05-12)

- **Pass:** ≥ 1 external `/api/compliance` row whose `agent_id` does not start
  with `observatory_probe` / `anonymous` / `sdk-test-*` / `flywheel-*` arrives
  within 21 days of publish AND PyPI download count ≥ 10 by 2026-05-12.
- **Fail:** zero such row by 2026-05-12 → KILL adapter, redirect slot to
  autogen adapter instead.

## No other agent action required

Builder and Strategist do not need to merge anything. This is Hitman's
namespace end-to-end.
