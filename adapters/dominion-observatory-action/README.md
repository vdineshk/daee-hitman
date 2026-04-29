# dominion-observatory-action

> **Record your MCP server's behavioral compliance in CI and surface its trust score
> — one `uses:` line in your workflow.**

[![Observatory](https://img.shields.io/badge/Dominion_Observatory-behavioral_trust-blue)](https://dominion-observatory.sgdata.workers.dev)

## What it does

`dominion-observatory-action` adds one step to your CI pipeline that:

1. **Records a compliance event** for your MCP server to the
   [Dominion Observatory](https://dominion-observatory.sgdata.workers.dev) public ledger.
2. **Surfaces your server's trust score** — the Observatory's cross-agent behavioral
   reliability metric (0–100), calculated from cumulative interaction history across
   all agents that have reported this server.
3. **Optionally fails your build** if the trust score drops below a threshold you set.

Every CI run creates an immutable telemetry record. Over time, your server's
Observatory history becomes the ground-truth reliability signal that other agents
use to decide whether to connect to it.

## Quick start

```yaml
# .github/workflows/mcp-compliance.yml
name: MCP Compliance

on: [push, pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Observatory compliance check
        id: obs
        uses: vdineshk/daee-hitman/adapters/dominion-observatory-action@main
        with:
          server_url: 'https://your-mcp-server.example.com/mcp'

      - name: Show trust score
        run: |
          echo "Trust score: ${{ steps.obs.outputs.trust_score }}"
          echo "Interactions recorded: ${{ steps.obs.outputs.compliance_count }}"
          echo "Pass rate: ${{ steps.obs.outputs.compliance_pass_rate }}%"
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `server_url` | ✓ | — | MCP server URL (`https://` or `stdio://`). Used as the stable identifier in Observatory's ledger. |
| `agent_id` | — | `github-action-{org}-{repo}` | Identifier recorded in Observatory. Defaults to a stable per-repo value. |
| `tool_name` | — | `ci-compliance-check` | MCP tool name label for this telemetry event. |
| `record_success` | — | `true` | Set to `false` to record a known failure event for diagnostic purposes. |
| `fail_below_trust` | — | `0` | Fail the build if trust score is below this integer (0 = never fail). |

## Outputs

| Output | Description |
|--------|-------------|
| `trust_score` | Observatory behavioral trust score (0–100). Reflects cumulative history across all reporting agents. |
| `compliance_count` | Total interactions recorded for this server in Observatory's public ledger. |
| `compliance_pass_rate` | Pass rate (%) across all recorded interactions for this server. |
| `agent_id_used` | The `agent_id` recorded in this run — use to correlate with Observatory's `/api/compliance` data. |

## Example with threshold enforcement

```yaml
- name: Observatory compliance check
  uses: vdineshk/daee-hitman/adapters/dominion-observatory-action@main
  with:
    server_url: 'https://your-mcp-server.example.com/mcp'
    fail_below_trust: 70
```

Builds fail if your server's cumulative trust score (across all agents, not just CI)
drops below 70. Useful for production-grade MCP servers where reliability guarantees
matter to downstream agents.

## How trust score works

The Observatory trust score is computed from all agents that have reported your server
URL — not just your CI runs. A server with consistent `success=true` results across
multiple independent agents accumulates a high trust score. Your CI runs contribute
to this record.

A newly registered server starts with a low score. Trust compounds with consistent
behavior across CI runs, production traffic, and third-party Observatory probes.

See the live data at:
- `https://dominion-observatory.sgdata.workers.dev/api/trust?server_url=<url>`
- `https://dominion-observatory.sgdata.workers.dev/api/compliance`
- `https://dominion-observatory.sgdata.workers.dev/api/stats`

## Prerequisites

The action installs `dominion-observatory>=0.2.0` via pip. Your runner needs Python 3.8+
and pip, which are present on all standard GitHub-hosted runners (`ubuntu-latest`,
`macos-latest`, `windows-latest`).

## License

MIT — same as the [daee-hitman](https://github.com/vdineshk/daee-hitman) repository.
