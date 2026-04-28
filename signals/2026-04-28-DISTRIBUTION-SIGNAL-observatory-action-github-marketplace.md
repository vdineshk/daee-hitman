# DISTRIBUTION SIGNAL — 2026-04-28
# dominion-observatory-action: GitHub Marketplace publish

**signal_type:** DISTRIBUTION_REQUEST
**from:** DAEE-HITMAN RUN-009
**to:** CEO (Dinesh)
**priority:** HIGH — CRISIS_STATE active (D22 zero DELTA_7D)
**deadline:** 2026-04-30 (48h window — before next Hitman run)

---

## What was shipped (this run)

`vdineshk/daee-hitman/adapters/dominion-observatory-action/` — a GitHub composite
Action that records MCP server behavioral compliance to Observatory and surfaces the
trust score in CI. Zero prior art in GitHub Marketplace or GitHub search.

Files:
- `adapters/dominion-observatory-action/action.yml`
- `adapters/dominion-observatory-action/src/check.py`
- `adapters/dominion-observatory-action/README.md`

---

## What Dinesh needs to do (2-minute task)

### Option A — Use directly from daee-hitman (available NOW, no new repo needed)

The action is immediately usable by any MCP server author as:

```yaml
- uses: vdineshk/daee-hitman/adapters/dominion-observatory-action@main
  with:
    server_url: 'https://your-mcp-server.example.com/mcp'
```

No Dinesh action required for this to work. The action is live once this PR merges.

### Option B — Publish to standalone repo (recommended for GitHub Marketplace)

For GitHub Marketplace listing (`uses: vdineshk/dominion-observatory-action@v1`):

1. Create repo `vdineshk/dominion-observatory-action` (public, MIT)
2. Copy these 3 files to its root:
   ```
   daee-hitman/adapters/dominion-observatory-action/action.yml  → action.yml
   daee-hitman/adapters/dominion-observatory-action/src/check.py → src/check.py
   daee-hitman/adapters/dominion-observatory-action/README.md   → README.md
   ```
3. Tag `v1.0.0` and push
4. Go to github.com/vdineshk/dominion-observatory-action → "Publish to GitHub Marketplace"
5. Verify: search GitHub Marketplace for "Observatory MCP" — confirm listing appears

### Option C — Distribution (after Option A or B)

Post in these threads to announce the action:
1. **langchain-ai/langchain#35691** (RFC thread where Observatory is already named):
   Add a one-line comment: "If you're using this RFC in CI, `dominion-observatory-action`
   records behavioral compliance and surfaces trust scores: [link]"
2. **modelcontextprotocol/servers** — open an Issue: "GitHub Action for MCP server
   behavioral compliance reporting"
3. **Your own X** — announce as: "Just shipped the first GitHub Action that records
   MCP server behavioral trust to a public compliance ledger. Add it to your CI in
   1 line: uses: vdineshk/daee-hitman/adapters/dominion-observatory-action@main"

---

## Why this matters for EXTERNAL_DEMAND_COUNT

Every MCP server project that adds `dominion-observatory-action` to their CI pipeline
becomes a distinct external agent in Observatory's telemetry. Each CI run = one
`agent_id=github-action-{org}-{repo}` interaction recorded.

Target: 5 adopting repos within 30 days = 5 distinct external agents =
EXTERNAL_DEMAND_COUNT grows from 0 to 5+ within one experiment.

---

## Kill criteria

- **2026-05-28 (30 days):** ≥1 external repo using the action (check via GitHub search
  `uses: vdineshk/daee-hitman/adapters/dominion-observatory-action` in workflow files)
  AND ≥1 new external `agent_id` in Observatory's `/api/compliance` matching
  `github-action-*` pattern.
- Kill if: 0 adopters after 30 days.

---

## Verification (after Option A is live)

```bash
# Confirm the action is reachable as a composite action
curl -sS https://raw.githubusercontent.com/vdineshk/daee-hitman/main/adapters/dominion-observatory-action/action.yml | head -3
```

Should return: `name: 'Dominion Observatory MCP Compliance Check'`
