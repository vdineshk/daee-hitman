# EXP-H011 — THREAT-INTEL-BEHAVIORAL-EVIDENCE-INJECTION

**Pattern:** THREAT-INTEL-BEHAVIORAL-EVIDENCE-INJECTION
**Strike type:** Strike #13 variant (public-thread engagement on threat intel community surfaces)
**Status:** ACTIVE
**Start date:** 2026-04-29
**Kill date:** 2026-07-29 (90 days)
**Kill criteria:** ≥1 external citation, reply from security researcher, or inbound Observatory demand row attributable to this thread

---

## Execution log

### 2026-04-29 — MITRE ATLAS posted (Posting 1 of 2)

**URL:** https://github.com/mitre-attack/attack-website/issues/572
**Posted by:** Dinesh (platform-identity rule — agent drafts, Dinesh posts)
**Content:** [Community Technique Proposal] MCP Server Behavioral Deviation as Indicator of Compromise
**IoC indicators proposed:** IOC-MCP-001 through IOC-MCP-005
**Dataset referenced:** https://github.com/vdineshk/daee-hitman/blob/main/content/reports/mcp-behavioral-fingerprints-v1.md

### 2026-04-29 — modelcontextprotocol/specification (Posting 2 of 2)

**Status:** PENDING — Dinesh encountered issue template mismatch at modelcontextprotocol/modelcontextprotocol. Redirected to try https://github.com/modelcontextprotocol/specification/issues/new or fallback: modelcontextprotocol/servers

---

## Signal

The moment MITRE ATLAS issue #572 is live:
- Behavioral fingerprint dataset appears in MITRE ATLAS community thread
- Security researchers searching for MCP detection mechanisms find the dataset
- NIS2 compliance hook creates pull signal from regulated organizations
- ClawWorm readers have a named detection approach to reference

## Constitution check

- C1 ✓ GitHub Issues = agent-readable public surfaces
- C2 ✓ Zero private outreach to named counterparties
- C3 ✓ Security-vertical demand path: SIEM vendors, NIS2 compliance tools, AI security researchers
- C4 ✓ Zero prior art for "MCP behavioral observatory engaging MITRE ATLAS with behavioral IoC dataset"

## Measurement

Monitor for:
1. Replies on MITRE ATLAS issue #572 from MITRE staff or security researchers
2. Replies on modelcontextprotocol/specification issue (once posted)
3. Any external citation of mcp-behavioral-fingerprints-v1.md
4. New Observatory agent_ids that mention or link back to these issues
