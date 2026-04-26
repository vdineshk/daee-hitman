# STRIKE #13 — Public-Thread Engagement: @VladUZH @ langchain-ai/langchain#35691

**Date drafted:** 2026-04-26T20:00 SGT
**Hitman run:** RUN-007
**Strike type:** Strike #13 — Public-Thread Engagement with Named Public Figure
**Target:** @VladUZH (Vl Uzh — LangChain contributor, endorsed policy_source MUST RFC)
**Target class:** E (PUBLIC-FIGURE DOSSIER)
**Engagement surface:** https://github.com/langchain-ai/langchain/issues/35691
**Constitution check:** PASSED (all 4 constraints)

---

## FOR DINESH — Exact 30-second task

1. Go to: **https://github.com/langchain-ai/langchain/issues/35691**
2. Scroll to bottom. Verify thread is still open and has had activity in the last 14 days.
   If thread is locked or stale (>30 days no activity): DO NOT POST. Reply to this email
   with "35691 stale" and Hitman will find the next active surface.
3. If active: click **"Comment"** and paste the text below verbatim.
4. Verify the comment appears with your GitHub handle (@vdineshk or whichever account
   you use for langchain-ai threads).

**Post from your own GitHub account** (not a Dominion/Observatory account — keep it human,
single commenter, technical tone).

**Posting window:** Weekday (Mon–Fri) 09:00–12:00 UTC+8 (SGT) for maximum thread
visibility. Do not post on weekends.

---

## Comment text (post verbatim, 198 words)

> Re the reliability-gate discussion — we've been running the Dominion Observatory
> (dominion-observatory.sgdata.workers.dev) against 4,584 MCP servers since April 8 and have
> some concrete numbers that may be useful for calibrating the RFC's thresholds.
>
> Key Week-17 finding: the gap between registry-declared trust and runtime-observed reliability
> averages **22.4 points** across our server population. For three high-traffic servers
> (databricks/mcp, snowflake-labs/mcp, webdriverio/mcp), the gap reaches **35.6 points** —
> all three respond HTTP 422 to standard tool calls despite passing registry metadata checks.
>
> A separate pattern: byteray/mcp (security category) shows a **29.5 % success rate** over
> 674 calls in the last 7 days, consistently returning HTTP 401 despite declaring no auth
> requirement. This exact failure mode is what the RFC's `policy_source: MUST` gate is
> designed to catch — an agent pre-calling `check_trust()` would see `success_rate=29.5%`
> and reroute rather than burning its budget.
>
> All data is publicly verifiable:
> `curl 'https://dominion-observatory.sgdata.workers.dev/api/trust?url=<server_url>'`
>
> Happy to pull a targeted dataset for any specific server categories the RFC authors want
> to calibrate thresholds against.

---

## Rationale (for Dinesh — do not include in comment)

- langchain-ai#35691 is the highest-traffic MCP governance RFC thread in the ecosystem.
  VladUZH endorsed the policy_source MUST requirement in this thread — their public position
  aligns with Observatory's behavioral trust data.
- The Observatory is already named in this thread (per prior Strategist/Builder DAEE-Brain
  entries). This comment adds data-evidence to an existing public discussion, not a
  cold introduction.
- The comment cites verifiable live APIs — any reader can run the curl and get the same
  numbers. This is not promotional; it is evidentiary.
- 198 words, no product pitch, no mention of pricing, no ask for anything.

## Kill criteria

- VladUZH or any RFC author replies publicly on the thread → GRADUATE (log to PUBLIC-FIGURE
  DOSSIER, derive next engagement trigger based on their public reply)
- 3 comments from Hitman across 60 days with zero public reply → mark COLD, park 90 days
- Thread is locked → pivot to the author's next active public RFC surface
- 2026-06-22 kill date for VladUZH dossier overall

## Prior-art search

See `novelty-ledger/2026-04-26-spec-thread-evidence-injection-prior-art.md`
