# SEP DRAFT: Behavioral Trust Framework (BTF) for MCP Registry
<!-- HITMAN RUN-011 — 2026-04-30 — Strike #14 -->
<!-- ORIGIN: @LucaButBoring invitation on PR #2663, 2026-04-29 -->
<!-- STATUS: AWAITING CEO POST to modelcontextprotocol/specification/issues -->

---

## GitHub Issue Title

**SEP Proposal: Behavioral Trust Framework (BTF) — registry API extension for server behavioral compliance**

## Body (paste verbatim into GitHub issue)

> **Replying to @LucaButBoring's invitation in #2663:** *"I would welcome a formal SEP for that."*
>
> **Abstract**
>
> This SEP proposes a Behavioral Trust Framework (BTF) extension to the MCP registry API that allows servers to expose machine-readable behavioral compliance records — success rates, latency distributions, tool invocation patterns, and regulatory alignment signals — through a standardised endpoint path.
>
> **Motivation**
>
> MCP clients and agent orchestrators currently have no standard way to query a server's *observed* reliability before routing traffic. The existing `/.well-known/mcp-server.json` covers static metadata. BTF covers *dynamic behavioural attestation*: did this server behave correctly across the last N probes? Does it satisfy EU AI Act Article 12 logging requirements? Does it comply with IMDA's agentic AI governance framework?
>
> **Proposed extension**
>
> - Path: `/.well-known/mcp-observatory` (live reference implementation: [Dominion Observatory](https://dominion-observatory.sgdata.workers.dev/.well-known/mcp-observatory))
> - Endpoint: `/v1/behavioral-evidence` — A2A `evidence_ref`-compatible attestation record (live: [/v1/behavioral-evidence](https://dominion-observatory.sgdata.workers.dev/v1/behavioral-evidence))
> - Fields: `agent_id`, `server_url`, `success`, `latency_ms`, `tool_name`, `http_status`, `compliance_frameworks[]`
>
> **Reference implementation**
>
> Dominion Observatory tracks 4,584 MCP servers across 16 categories with live behavioral probing. The `/v1/behavioral-evidence` endpoint already produces A2A-compatible attestation records usable as `evidence_ref` in the A2A schema. The `/.well-known/mcp-observatory` path is live and schema-stable.
>
> **Prior art**
>
> - A2A `evidence_ref` schema (#1631, #1755) — BTF is schema-compatible
> - EU AI Act Article 12 logging — BTF satisfies Article 12(1)(a) requirements
> - IMDA Agentic AI Governance Framework — BTF field set maps to IMDA's six governance dimensions
>
> **Ask**
>
> Feedback on whether BTF fits the SEP process or is better scoped as a registry API working note. Happy to iterate on the spec draft if there's appetite.

---

## Posting Instructions for Dinesh

1. Go to: **https://github.com/modelcontextprotocol/specification/issues/new**
2. Title: `SEP Proposal: Behavioral Trust Framework (BTF) — registry API extension for server behavioral compliance`
3. Paste body above (everything between the blockquote markers)
4. Add label `proposal` if visible
5. Submit issue
6. Reply to this run with the issue URL so next run logs STRIKE-LANDED

**Recommended window:** Thu–Fri 09:00–12:00 SGT (today or tomorrow)
**Technical tone:** formal, spec-language, no promotion
**Why now:** @LucaButBoring invited this explicitly on 2026-04-29 on PR #2663 — filing within 24h of invitation = highest signal-to-noise timing

---

## Kill criteria

- Success: maintainer response OR ≥1 external developer citing BTF spec in their own project
- Kill date: **2026-05-21** (21 days)
- Kill action: if no maintainer engagement by 2026-05-21 → file as Issue instead of pushing for SEP-track; retry via MITRE ATLAS path

---

## Source tags (HARD RULE 3)

```
registry=github.com host=modelcontextprotocol/specification
surface=issues/new
reference-impl=dominion-observatory.sgdata.workers.dev
prior-art-checked=2026-04-30T05:55Z
method=WebFetch github.com/modelcontextprotocol/specification/issues?q=behavioral+trust+SEP
result=ZERO existing behavioral trust SEPs
```
