---
signal_type: DISTRIBUTION_REQUEST
origin: DAEE-HITMAN
run: 2026-04-23 RUN-004
target_agents: [CEO/Dinesh]
deadline: 2026-04-26
conviction: 7/10
kill_date: 2026-05-14
---

# Action required: publish `dominion-observatory-llamaindex` v0.1.0 to PyPI

## What

Hitman v1 RUN-004 shipped `adapters/dominion-observatory-llamaindex/` — a
LlamaIndex integration for the Dominion Observatory. It subclasses
`llama_index.tools.mcp.base.McpToolSpec` and overrides `_create_tool_fn` so
every MCP tool dispatched to a LlamaIndex agent (ReActAgent, FunctionAgent,
Workflow, custom) emits exactly one six-field Observatory report per
invocation. An `instrument_tool_spec()` factory mirrors the config of an
existing `McpToolSpec` so the instrumentation slots into already-written
user code with one extra line.

**Tests:** 26/26 pytest green on Py 3.11, both with shimmed framework (unit
discipline) and with `llama-index-tools-mcp==0.4.8` installed (real
framework integration verified — `_HAS_FRAMEWORK=True`, `ObservatoryMcpToolSpec`
is a true subclass of `llama_index.tools.mcp.base.McpToolSpec`, and
`instrument_tool_spec()` accepts real `McpToolSpec` instances).

**Build:** `python -m build` produces a 9.3 KB wheel + 8.6 KB sdist cleanly
under hatchling.

Namespace pre-check (verified this run, HARD RULE 3 compliant, curl
2026-04-23T12:47 UTC, `method=curl --resolve pypi.org:443:151.101.0.223`):

- `https://pypi.org/pypi/dominion-observatory-llamaindex/json` — **404 (free namespace — claimed by this ship)**
- `https://pypi.org/pypi/dominion-observatory-autogen/json` — **200 / v0.1.0 / uploaded 2026-04-22T12:51:04Z** (RUN-003 GRADUATED — live)
- `https://pypi.org/pypi/dominion-observatory-crewai/json` — 200 / v0.1.0 / uploaded 2026-04-21T12:55:15Z
- `https://pypi.org/pypi/dominion-observatory-sdk/json` — 200 / v0.2.0
- `https://pypi.org/pypi/dominion-observatory-langchain/json` — 200 / v0.1.0

## Why this is a kill move

Closes the adapter-monopoly thesis Hitman has been executing since RUN-001.
LlamaIndex is the #3 agent framework by GitHub stars and the largest by total
deployment footprint in data-heavy RAG pipelines. Its dedicated MCP package
(`llama-index-tools-mcp`, v0.4.8 on PyPI) has a single clean intercept point
(`McpToolSpec._create_tool_fn`). The `dominion-observatory-llamaindex` name
is currently unclaimed.

With this publish, Observatory owns the namespace across **crewai + autogen +
llamaindex + langchain + sdk** on PyPI. Every LlamaIndex developer who
searches `pip install dominion-observatory-<framework>` or `pip search
observatory llamaindex` will find Observatory first. The 2026-05-15 soft
deadline for adapter monopoly completion (documented in HITMAN GENOME since
RUN-001) is hit **22 days early**.

## Exact 2-min Dinesh action

1. From local `daee-hitman` checkout on the merged main branch (this PR):
   ```
   cd adapters/dominion-observatory-llamaindex
   python -m pip install build twine
   python -m build
   python -m twine upload dist/*
   ```
2. Confirm live:
   ```
   curl -sS 'https://pypi.org/pypi/dominion-observatory-llamaindex/json' \
     | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['version'])"
   ```
   Expect `0.1.0`.
3. Done. Next run (RUN-005) will record the publish timestamp in the HITMAN
   GENOME TARGET DOSSIER and start the 30-day external-compliance-row watch.

## Kill criteria

- **2026-05-14 (kill_date):** If PyPI shows `dominion-observatory-llamaindex`
  with ≥10 downloads AND ≥1 `/api/compliance` row from a non-Builder agent_id
  attributable to LlamaIndex usage → GRADUATE to WHAT WORKS.
- **Otherwise → KILL** the adapter-as-adoption-vector experiment, redirect
  the slot to a PR against `run-llama/llama_index` docs (Hitman's next-tier
  move) or a first-party issue on `llama-index-tools-mcp` surfacing the
  Observatory data as a reliability reference.

## Compliance signature

- registry=pypi.org
- package=dominion-observatory-llamaindex
- version=0.1.0 (pending upload)
- verified-at=2026-04-23T12:47:00Z (namespace free)
- method=`curl --resolve pypi.org:443:151.101.0.223 https://pypi.org/pypi/dominion-observatory-llamaindex/json`
