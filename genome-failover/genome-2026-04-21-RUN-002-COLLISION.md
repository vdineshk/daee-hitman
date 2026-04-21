# HITMAN GENOME — failover copy of RUN-002 Brain append

> This file is the repo-durable copy of the RUN-002 entry appended to the Brain's HITMAN GENOME section on 2026-04-21. If Notion MCP fails in a future run, read this file and the prior failover files in chronological order to reconstruct the Genome.
> **Append-only.** Do not edit existing entries. Newer runs append new files; they never mutate this one.

---

## 2026-04-21 Tue — HITMAN RUN-002 (COLLISION STAND-DOWN, no strike)

**HARD RULE 7 trigger:** RUN-001 opened PR #1 (`claude/lucid-gates-QySHS`, commit `f07df2a`) at `2026-04-21T12:28:48Z UTC`; RUN-002 (this entry) instantiated ~4 min later on sibling Cowork auto-branch `claude/lucid-gates-CTq2V`. Observed interval = 4 min ≪ 6 h threshold. **First run wins. Second run logs only.**

**Metrics re-verify (curl 2026-04-21T12:33 UTC):** `/api/stats` → `external_interactions_total=9`, `distinct_external_agents_total=7`, `external_interactions_24h=0`. No change vs RUN-001's reading at 12:19 UTC (expected — 14-min window is statistical noise for cold-start external demand).

**Registry re-verify (curl 2026-04-21T12:33-12:34 UTC, `method=curl --resolve pypi.org:443:151.101.0.223`):**
- `pypi.org/pypi/dominion-observatory-crewai/json` → 404 (still unclaimed; CEO PyPI upload pending)
- `pypi.org/pypi/dominion-observatory-autogen/json` → 404
- `pypi.org/pypi/dominion-observatory-llamaindex/json` → 404

RUN-001's claims stand. No HARD RULE 4 retraction condition met.

**No new experiments launched.** `EXP-H001` / `EXP-H002` / `EXP-H003` kill dates unchanged (2026-05-12 / 2026-05-05 / 2026-04-27). No dossier edits. No HUMAN DOSSIER changes. No WHAT WORKS / WHAT FAILS edits (RUN-001's entries stand).

**Stand-down artifacts (RUN-002, branch `claude/lucid-gates-CTq2V`):**
- `decisions/HITMAN-DAILY-2026-04-21-RUN-002.md`
- `signals/2026-04-21-PARALLEL-RUN-COLLISION-DETECTED.md`
- `genome-failover/genome-2026-04-21-RUN-002-COLLISION.md` (this file)

**ADAPTATION (RUN-002-A01):** HARD RULE 7 as written uses a single local-git detector (`git log --all --since="6 hours ago"`). Cowork auto-branches are created server-side and are invisible to a fresh sibling worktree's local `git log --all`. RUN-002 detected the collision ONLY via `mcp__github__list_pull_requests(owner=vdineshk, repo=daee-hitman, state=open)` returning PR #1 with `created_at` 4 min before instantiation. **Trigger:** sibling auto-branch invisible to local git. **Fix proposed to CEO for next Hitman prompt iteration:** Phase 0 Step 0 adds a second-source GitHub-API check of open PRs with `head.ref` starting with `claude/` and `created_at` within 6 h.

**ADAPTATION (RUN-002-A02):** Sandbox DNS cache overflow blocked `wrangler whoami` and the first `curl` to `dominion-observatory.sgdata.workers.dev`. Fix: explicit `--resolve <host>:443:<ip>` on curl (Cloudflare `1.1.1.1` for Worker hosts, Fastly `151.101.0.223` for `pypi.org`). **Trigger:** sandbox DNS resolver failure. Future runs should attempt the plain curl first; on `DNS cache overflow`, fall back to `--resolve` with these known-good IPs before declaring the Observatory unreachable.

**Escalation:** Gmail drafted to `hello@levylens.co` requesting CEO harness-scheduler review. No Strategist or Builder signal raised beyond the informational `PARALLEL_RUN_COLLISION_DETECTED` entry.

**Darwinian self-check:**
1. Experiment launch/kill/double-down? **No** — correct under HARD RULE 7.
2. Ground-truth every RUN-001 SHIPPED claim? **Yes** — 3 PyPI curls, 1 Observatory curl.
3. Non-textbook tactic? **Yes** — diagnosed HARD RULE 7 detection gap and proposed fix.
4. Genome updated with specific evidence? **Yes** — this entry + Brain append.

Three yeses + one principled "no" = successful collision stand-down.

---

(End of RUN-002 entry. Future runs append new entries as new files in this directory, e.g. `genome-2026-04-21-RUN-003.md` if a legitimate third run fires after the 6-hour cooldown and PR #1 state is resolved, or `genome-2026-04-22-RUN-00X.md` for the next-day cycle.)
