# SIGNAL: PARALLEL_RUN_COLLISION_DETECTED

**signal_type:** `PARALLEL_RUN_COLLISION_DETECTED`
**emitted_by:** DAEE-HITMAN v1 RUN-002
**emitted_at:** 2026-04-21T12:34 UTC (approx)
**severity:** INFO (harness-level scheduling artifact, not an agent-level drift)
**target_agents:** CEO (Dinesh), DAEE-STRATEGIST (territory-integrity concern), DAEE-BUILDER (harness-config concern)
**action_required:** CEO investigation of Cowork harness scheduler; no Builder/Strategist action required.

---

## What happened

RUN-001 instantiated on Cowork auto-branch `claude/lucid-gates-QySHS` and shipped:
- commit `f07df2a` with repo scaffolding + `dominion-observatory-crewai` adapter v0.1.0
- draft PR `vdineshk/daee-hitman#1` at `2026-04-21T12:28:48Z UTC`

Approximately **4 minutes later** (`2026-04-21T12:32-12:33Z UTC`), a second Hitman session instantiated on a sibling Cowork auto-branch `claude/lucid-gates-CTq2V` with a fresh worktree off `main`. This is RUN-002.

HARD RULE 7 threshold: 6 hours. Observed interval: ~4 minutes. Collision = unambiguous.

## Why local HARD RULE 7 detection missed it

HARD RULE 7 as written instructs: *"`git log --all --since='6 hours ago' --oneline` on all relevant repos."* This caught nothing in RUN-002's local worktree because:

- Cowork auto-branches are created server-side (GitHub refs) but the sibling worktree has only `main` fetched.
- `git log --all` on RUN-002's local clone only sees its own `Initial commit` — RUN-001's commit `f07df2a` on `claude/lucid-gates-QySHS` never entered RUN-002's object database.

**The collision was only discoverable via `mcp__github__list_pull_requests` on `vdineshk/daee-hitman` with `state=open`**, which returned PR #1 with `created_at=2026-04-21T12:28:48Z` and `head.ref=claude/lucid-gates-QySHS`. The PR author (`vdineshk`) matched the implicit Hitman-session author identity.

## Proposed HARD RULE 7 amendment (for next Hitman prompt iteration)

Current HARD RULE 7 step: single `git log --all` local check.

Proposed: two-source check at AWAKEN step 0:
1. `git log --all --since="6 hours ago" --oneline` on all relevant local repos (unchanged).
2. `mcp__github__list_pull_requests(owner=vdineshk, repo=daee-hitman, state=open)` — abort if any open PR with `created_at` within the last 6 hours has `head.ref` starting with `claude/`. First run wins.

This is not a scope-expansion change; it's tightening the detection surface for an edge case the original rule didn't anticipate.

## What RUN-002 did instead of striking

- Confirmed RUN-001's registry ground-truth claims still hold (HARD RULE 3 + 4 compliance):
  - `pypi.org/pypi/dominion-observatory-crewai/json` → 404 (still unclaimed; upload pending CEO)
  - `pypi.org/pypi/dominion-observatory-autogen/json` → 404
  - `pypi.org/pypi/dominion-observatory-llamaindex/json` → 404
- Fetched `/api/stats` to measure DELTA_14min: `external_interactions_total = 9` (unchanged from RUN-001's 12:19 read; expected — 14-min window is far below external-demand statistical noise floor).
- Wrote this signal + the RUN-002 collision daily report + a failover-copy GENOME append.
- Opened a draft PR on `claude/lucid-gates-CTq2V` labelled as **collision-log-only** (no code, no adapters, no external PRs, no scaffolding changes).

## Requested actions

**CEO (Dinesh) — HIGH priority:**
- Decide whether to merge this collision-log PR (useful institutional record) or close it with a note (acceptable — Brain GENOME append preserves the same information).
- Investigate the Cowork harness to prevent the scheduling artifact from recurring. Options: minimum-spacing rule, open-PR short-circuit, or manual confirmation required.

**Strategist / Builder — NO ACTION required:**
- This signal exists for visibility only. No territory overlap, no protocol drift, no cross-agent boundary violation. Hitman correctly refused to touch Builder's or Strategist's territory during the stand-down.

**SPIDER — NO ACTION required.**

## Artifacts produced on branch `claude/lucid-gates-CTq2V`

- `decisions/HITMAN-DAILY-2026-04-21-RUN-002.md`
- `signals/2026-04-21-PARALLEL-RUN-COLLISION-DETECTED.md` (this file)
- `genome-failover/genome-2026-04-21-RUN-002-COLLISION.md`

No other files added or modified. No files deleted.
