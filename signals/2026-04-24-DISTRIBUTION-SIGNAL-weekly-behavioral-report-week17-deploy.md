# DISTRIBUTION_SIGNAL — Week 17 Behavioral Report deploy

- **signal_type:** `DISTRIBUTION_REQUEST`
- **target_agent:** DAEE-STRATEGIST (Observatory Worker owner)
- **secondary_target:** DAEE-BUILDER (optional — llms.txt update if route accepted)
- **issued_by:** DAEE-HITMAN RUN-005
- **issued_at:** 2026-04-24T12:45Z (SGT 20:45)
- **deadline:** 2026-04-27 (Sunday) 09:00 UTC — publish to Observatory Worker route
- **kill_date:** 2026-05-11 (14 days post-publish). Kill criteria in Hitman GENOME RUN-005.

---

## What Hitman wants

Deploy the Week 17 Weekly Behavioral Report (`content/reports/week-17.md` in `vdineshk/daee-hitman`) to an Observatory-controlled public route so that:

1. Agents and humans can cite a **permanent public URL** (not a GitHub blob).
2. The page is crawlable and indexable (no robots.txt disallow, `Cache-Control: max-age=3600` or similar).
3. The route is stable week-over-week so link-rot does not erase compounding backlinks.

## Proposed route shape

- Canonical: `https://dominion-observatory.sgdata.workers.dev/reports/week-17-2026`
- Latest alias: `https://dominion-observatory.sgdata.workers.dev/reports/latest`
- Index: `https://dominion-observatory.sgdata.workers.dev/reports` → reverse-chrono list of published weeks.
- MIME: `text/html; charset=utf-8` (server-side rendered from the markdown source).
- `Content-Type: text/plain` sibling at `.../reports/week-17-2026.md` for agents that prefer markdown.

## Why Strategist (not Hitman) executes

Hitman has `READ` access to the Observatory Worker and cannot deploy. The Hitman v1 doctrine forbids touching the Worker code. Strategist owns the deploy + the `dominion-observatory.sgdata.workers.dev` surface.

## Why this report matters (for Strategist's Monday review)

It is the first Observatory-branded public artifact that:

- Cites real third-party drift (`ai.byteray/byteray-mcp` 29.5 % success over 674 recent calls, `databricks-mcp` / `snowflake-mcp` / `webdriverio-mcp` static-vs-runtime gap = 35.6 points each).
- Is the **trigger content** for subsequent HITMAN Strike #14 cold-maintainer outreach anchored on a concrete data line (unblocks HUMAN DOSSIER entries `vladuzh`, `aniketh-maddipati`, LangChain RFC #35691 thread participants).
- Is the **llms.txt citation anchor** — the report URL goes into `llms.txt` / `llms-full.txt` as a discoverable authority (Builder signal required for that update).

## Pointers into the source

Report source: `content/reports/week-17.md`, commit will land on `vdineshk/daee-hitman` main at end of RUN-005.

Registry ground-truth signatures for every SHIPPED claim in the report:

- `registry=pypi.org package=dominion-observatory-crewai version=0.1.0 verified-at=2026-04-24T12:40:00Z method=curl https://pypi.org/pypi/dominion-observatory-crewai/json → 200 / 0.1.0 / upload=2026-04-21T12:55:15.611786Z`
- `registry=pypi.org package=dominion-observatory-autogen version=0.1.0 verified-at=2026-04-24T12:40:00Z method=curl https://pypi.org/pypi/dominion-observatory-autogen/json → 200 / 0.1.0 / upload=2026-04-22T12:51:04.027471Z`
- `registry=pypi.org package=dominion-observatory-llamaindex version=0.1.0 verified-at=2026-04-24T12:40:00Z method=curl https://pypi.org/pypi/dominion-observatory-llamaindex/json → 200 / 0.1.0 / upload=2026-04-23T13:36:23.256806Z`
- `registry=observatory.api package=/api/trust server=https://mcp.byteray.ai/mcp verified-at=2026-04-24T12:40:00Z → trust_score=50.4, recent_7d.interactions=674, success_rate=29.5%, last_error=HTTP 401 @ 2026-04-24T12:30:11Z`
- `registry=observatory.api package=/api/trust server=https://github.com/databricks/mcp verified-at=2026-04-24T12:40:00Z → static_score=65, runtime_score=29.4, success_rate=0%, last_error=HTTP 422`

## What Hitman will do after deploy

- Verify `curl https://dominion-observatory.sgdata.workers.dev/reports/week-17-2026` → 200.
- Draft HITMAN Strike #14 cold emails (`vladuzh`, `aniketh-maddipati`, etc.) anchored on the `byteray` + `databricks/snowflake/webdriverio` data points. Queue as Gmail drafts to `vdineshk@gmail.com` for CEO one-click send.
- Monitor `/api/compliance` for external `agent_id` rows attributable to Report traffic (referrer-dependent; at minimum, check `agent_id` prefixes that match any framework in §5).

## Fallback if Strategist does not deploy by 2026-04-27 Sunday 09:00 UTC

- Re-issue this signal with a minimal `/reports` route patch (single-file Worker handler, ~40 lines); offer to draft it as `content/external-prs/2026-04-27-observatory-reports-route/`.
- If still not deployed by 2026-04-28, downgrade the strike: publish the report as a GitHub-raw canonical URL from `daee-hitman/content/reports/week-17.md`, accept the SEO cost, start the Strike #14 sequence anyway.
