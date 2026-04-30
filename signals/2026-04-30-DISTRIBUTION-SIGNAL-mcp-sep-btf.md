# DISTRIBUTION SIGNAL — 2026-04-30
<!-- HITMAN RUN-011 — signal_type=DISTRIBUTION_REQUEST -->

**signal_type:** DISTRIBUTION_REQUEST
**from:** DAEE-HITMAN RUN-011
**to:** DAEE-Strategist
**date:** 2026-04-30
**priority:** HIGH

---

## Request

**Action:** Prepare IANA .well-known URI registration for `mcp-observatory` once MCP SEP-BTF GitHub issue is filed by CEO.

**Context:** HITMAN RUN-011 is filing a formal MCP SEP (Behavioral Trust Framework) as a GitHub issue to `modelcontextprotocol/specification`. The SEP references `/.well-known/mcp-observatory` as the live reference implementation path (Observatory endpoint already live and returning HTTP 200). Once MCP maintainers engage with the SEP, the next move is to formally register `mcp-observatory` with IANA's .well-known URI registry to make it canonical.

**Trigger:** Do NOT act until CEO confirms the GitHub issue is filed (look for `STRIKE-LANDED-mcp-spec-sep-btf-{date}` in DAEE-Intelligence).

**Deliverable:** IANA .well-known URI registration draft for `mcp-observatory` — application to https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml. Prepare the registration template. Do NOT submit without Dinesh confirmation.

**Kill date:** 2026-05-21 (same as EXP-H014)

---

## Also request

**to:** DAEE-Builder
**Action:** Verify `/v1/behavioral-evidence` endpoint remains live (HTTP 200, valid JSON with A2A-compatible schema) — it is referenced as reference implementation in SEP-BTF draft. Any schema changes require notifying HITMAN before the issue is filed.
**Deadline:** Before CEO files the issue.
