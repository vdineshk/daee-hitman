# daee-hitman

DAEE-HITMAN v1.0 — the distribution assassin of the Dominion Agent Economy
Engine. This repository holds every artifact Hitman ships: framework adapters,
external-repo PR drafts, weekly behavioral reports, second-angle content, and
the daily decision log.

## Singular goal

Drive `EXTERNAL_DEMAND_COUNT` on the Dominion Observatory from its current
baseline to **1,000 external agents within 12 months**, with a curve passing
through 50 by Day 60. Every ship in this repo is scored on one metric:
`DELTA_7D` of `external_demand.external_interactions_total` as reported by
`https://dominion-observatory.sgdata.workers.dev/api/stats`.

## Layout

```
adapters/            Framework adapters — Hitman owns the namespace end-to-end.
                     Each subdirectory is an independent publishable package.
  dominion-observatory-crewai/
  dominion-observatory-autogen/      (planned)
  dominion-observatory-llamaindex/   (planned)

content/
  reports/           Weekly Behavioral Reports (Sundays only).
  posts/             Second-angle positioning pieces.
  external-prs/      Full drafts of PRs aimed at other people's repos.
                     Each subdirectory = one prospective PR, branch name,
                     files, PR body, and target coordinates.

decisions/           Daily HITMAN-DAILY-YYYY-MM-DD-RUN-N reports.
genome-failover/     Markdown backup of the HITMAN GENOME written to the Brain.
                     Populated only when Notion MCP fails during a run.
signals/             Outbound DISTRIBUTION_SIGNAL payloads written to
                     DAEE-Intelligence — kept here as a local mirror.
```

## Scope rules

- Push directly to `main` on this repo only.
- Never push to `vdineshk/daee-engine` or `vdineshk/dominion-observatory` —
  open a PR instead.
- Never deploy to the Observatory Worker — that belongs to DAEE-Strategist.
  Request deploys via a `DISTRIBUTION_SIGNAL` entry in DAEE-Intelligence.
- Every artifact carries a kill date. Experiments die without mercy at the
  date unless the metric moved.

## Licence

MIT — see `LICENSE`.
