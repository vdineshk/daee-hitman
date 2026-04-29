# Prior-Art Search Log — RUN-010
## Strike Pattern: "Cross-Ecosystem Spec Oracle Positioning"
## Target: ERC-8004 ethereum-magicians.org/t/erc-8004-trustless-agents/25098 post #77
## Date: 2026-04-29

### What was searched (5 surfaces minimum, C4 requirement)

1. **Target thread itself** (ethereum-magicians.org/t/erc-8004-trustless-agents/25098)
   - Page 5 (most recent): Searched for MCP trust/behavioral data references.
   - `wanderosity` post: "Has anyone looked at ERC-8004 as a trust substrate for open agent/MCP networks?" — NO ANSWER EXISTS in the thread. Question is open.
   - No reference to Dominion Observatory, behavioral trust oracles, or MCP behavioral data in any thread post found.
   - Verdict: **ZERO prior engagement** of Observatory with this thread.

2. **ERC-8004 EIP spec page** (eips.ethereum.org/EIPS/eip-8004)
   - Validation registry references off-chain data but names no specific oracle providers.
   - No mention of MCP behavioral data sources.
   - Verdict: **no prior art**.

3. **GitHub — search "ERC-8004 MCP behavioral trust"**
   - No repos found combining ERC-8004 Validation registry with MCP behavioral oracle data.
   - Smithery, Glama, mcp.so: static metadata scorers only, not behavioral attestation. Not referenced in ERC-8004 discussions.
   - Verdict: **no prior art**.

4. **Web search — "ERC-8004 MCP server behavioral oracle 2026"**
   - Returned: coindesk.com/markets/2026/01/28, eco.com/support, backpack.exchange/articles
   - None reference a live MCP behavioral data source as ERC-8004 Validation input.
   - Verdict: **no prior art**.

5. **Web search — "ERC-8004 validation oracle off-chain behavioral data"**
   - tokmakoff (Axiom Agentics) proposed hybrid model on-thread but named no specific data source.
   - alftom proposed EAS extension but focused on schema, not behavioral data.
   - No project claims the MCP behavioral oracle position for ERC-8004 validation.
   - Verdict: **no prior art**.

### Relationship to existing STRIKE NOVELTY LEDGER entries

- **Entry 2: "Live-API-Verifiable Spec-Thread Evidence Injection"** (claimed 2026-04-26, LangChain #35691)
  — Same pattern class (spec thread comment with live-API-verifiable data) but different ecosystem (Ethereum ERC vs GitHub MCP RFC) and different mechanism (connecting ERC-8004 Validation registry to Observatory, not LangChain observability RFC).
  — The LangChain claim covers the GitHub/MCP RFC ecosystem. This claim extends to the Ethereum EIP ecosystem.
  — Verdict: **extension of prior pattern to new ecosystem** — qualifies as new STRIKE NOVELTY LEDGER sub-entry or new entry "Cross-Ecosystem Spec Oracle Positioning."

### Originality verdict

**ORIGINAL.** No other project has publicly positioned MCP behavioral data (runtime success/failure/latency from real agent calls) as an off-chain assessment oracle for ERC-8004's Validation registry, either in the thread or in any findable public artifact. Empire executes first.

### Kill date for this engagement: 2026-05-20
### Success metric: ≥1 reply from thread participant OR ≥1 new external agent_id in /api/compliance attributable to Ethereum ecosystem

### Source tags
- verified-at: 2026-04-29T10:30Z
- method: WebFetch(ethereum-magicians.org) + WebSearch("ERC-8004 MCP behavioral oracle")
- thread: ethereum-magicians.org/t/erc-8004-trustless-agents/25098
- spec: eips.ethereum.org/EIPS/eip-8004
