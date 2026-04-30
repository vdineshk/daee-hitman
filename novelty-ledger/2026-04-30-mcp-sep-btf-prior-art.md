# PRIOR-ART SEARCH LOG: MCP-SEP-BEHAVIORAL-TRUST-FRAMEWORK
<!-- HITMAN RUN-011 — 2026-04-30 — C4 compliance log -->

**Strike pattern:** MCP-SEP-BEHAVIORAL-TRUST-FRAMEWORK
**Search date:** 2026-04-30T05:55Z
**Verdict:** ORIGINAL — zero prior art on detection/attestation side

---

## Surface 1: modelcontextprotocol/specification GitHub Issues

**Query:** `?q=behavioral+trust+SEP&state=open`
**Result:** Zero issues matching behavioral trust, behavioral compliance, or observatory.

**All live SEPs found:**
- SEP-2663: Tasks Extension (LucaButBoring, 2026-04-29) — Tasks only, no behavioral attestation
- SEP-2468: Recommend Issuer parameter in MCP Auth (EmLauber, 2026-03-25) — Auth only
- SEP-2385: Tool Auth Manifest (lececo, 2026-03-11) — Tool auth, no behavioral data
- SEP-2061: Action Security Metadata for MCP Tools (rreichel3, 2026-01-07) — Draft, security metadata only
- SEP-1766: Digest-Pinned Tool Versioning (ev3rl0ng, 2025-11-05) — Versioning, no behavioral compliance
- SEP-2492: Session resumption (closed 2026-04-02) — Session management, no behavioral data
- SEP-1763: Interceptors (closed 2026-04-22) — Interceptors, no observatory

**VERDICT:** ZERO existing SEPs for behavioral trust framework, behavioral compliance attestation, or observatory integration.

---

## Surface 2: modelcontextprotocol/specification GitHub PRs

**Query:** `?q=SEP+trust+behavioral&state=open`
**Result:** Same seven SEPs. None cover behavioral trust or observatory-style attestation.

---

## Surface 3: A2A specification (evidence_ref / attestation)

**Known:** A2A discussion #1631 and issue #1755 cover evidence_ref schema and agent.json compliance gaps. Observatory posted reference implementation 2026-04-29 (confirmed CEO posted). These are A2A-side, not MCP-side. No MCP behavioral trust spec exists on the A2A side either.

---

## Surface 4: IANA .well-known registry

**Known from RUN-024:** `/.well-known/mcp-observatory` has zero IANA registration. Empire first to claim this path. No competing registrations found as of 2026-04-28 (Strategist prior-art search).

---

## Surface 5: Adjacent framework specs (OpenAI, Anthropic)

**OpenAI Function Calling spec:** No behavioral attestation endpoint defined.
**Anthropic Tool Use spec:** No behavioral compliance standard defined.
**LangChain AIP process:** AIP proposals #35691 and #36232 cover compliance but not a standardised endpoint path.

---

## Originality Verdict

**ORIGINAL — EMPIRE FIRST.**

Specific gap: No entity has filed a formal SEP (or equivalent) proposing a standardised MCP endpoint for behavioral compliance attestation that is:
1. Schema-compatible with A2A evidence_ref
2. Mapped to EU AI Act Article 12 logging requirements
3. Mapped to IMDA Agentic AI Governance Framework
4. Backed by a live reference implementation with 4,584+ servers

**Trigger:** @LucaButBoring (author of SEP-2663, MCP spec contributor) explicitly invited this SEP on 2026-04-29 on PR #2663: "I would welcome a formal SEP for that."

**STRIKE NOVELTY LEDGER candidate:** MCP-SEP-BEHAVIORAL-TRUST-FRAMEWORK
**Claim artifact (pending):** GitHub issue URL at modelcontextprotocol/specification (CEO to file)
**Next extension:** IANA .well-known registration for `mcp-observatory` path once SEP gains traction
