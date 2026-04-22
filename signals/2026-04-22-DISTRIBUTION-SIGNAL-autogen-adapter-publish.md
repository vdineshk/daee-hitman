---
signal_type: DISTRIBUTION_REQUEST
origin: DAEE-HITMAN
run: 2026-04-22 RUN-003
target_agents: [CEO/Dinesh]
deadline: 2026-04-25
conviction: 7/10
kill_date: 2026-05-13
---

# Action required: publish `dominion-observatory-autogen` v0.1.0 to PyPI

## What

Hitman v1 RUN-003 shipped `adapters/dominion-observatory-autogen/` — a
framework-agnostic wrapper around `autogen_core.tools.BaseTool` that intercepts
`run_json`, measures latency, and emits a single Observatory report per tool
invocation. Works transparently for MCP-bridged tools produced by
`autogen-ext-mcp` and for native Python tools.

19/19 unit tests pass on Py 3.11 against duck-typed stand-ins; `python -m build`
produces a 7.9 KB wheel + 7.5 KB sdist cleanly.

Namespace pre-check (verified this run, HARD RULE 3 compliant):

- `https://pypi.org/pypi/dominion-observatory-autogen/json` — **404 (free namespace)**
- `https://pypi.org/pypi/dominion-observatory-crewai/json` — 200 / v0.1.0 / uploaded 2026-04-21T12:55:15Z (shipped by RUN-001 + this CEO action)
- `https://pypi.org/pypi/dominion-observatory-sdk/json` — 200 / v0.2.0
- `https://pypi.org/pypi/dominion-observatory-langchain/json` — 200 / v0.1.0

## Why this is a kill move

Microsoft AutoGen is the #2 agent framework by GitHub stars after LangChain;
AutoGen v0.4 standardised on `autogen_core.tools.BaseTool` as the single
dispatch point, which means one wrapper covers both hand-written Python tools
AND every MCP-bridged tool from `autogen-ext-mcp`. The namespace is free.
Every install is a permanent telemetry pipeline neither SPIDER nor Strategist
can backfill.

This strike extends the adapter-monopoly thesis: owning
`dominion-observatory-*` on PyPI across crewai / autogen / llamaindex before
competitors land means any agent developer who searches for "my framework +
observability + MCP" finds Observatory first. Crewai was RUN-001. This is
RUN-003. Llamaindex is RUN-004.

## Exact 2-min Dinesh action

1. From local `daee-hitman` checkout on the merged main branch (this PR):
   ```
   cd adapters/dominion-observatory-autogen
   python -m pip install build twine
   python -m build
   python -m twine upload dist/*
   ```
2. Confirm live:
   ```
   curl -sS 'https://pypi.org/pypi/dominion-observatory-autogen/json' \
     | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['version'])"
   ```
   Expect `0.1.0`.
3. Reply with the `upload_time` PyPI returns so RUN-004 can anchor its
   measurement window.

## Success metric (kill 2026-05-13)

- **Pass:** ≥ 1 external `/api/compliance` row whose `agent_id` does not start
  with `observatory_probe` / `anonymous` / `sdk-test-*` / `flywheel-*` AND
  whose `tool_name` is reachable via an AutoGen `BaseTool.run_json` call
  within 21 days of publish, AND ≥ 10 PyPI downloads by 2026-05-13.
- **Fail:** zero such row by 2026-05-13 → KILL adapter, redirect slot to the
  next experiment in the autogen surface (candidate: PR against
  `microsoft/autogen-ext-mcp` docs referencing the adapter).

## No other agent action required

Builder and Strategist do not need to merge anything. This is Hitman's
namespace end-to-end.
