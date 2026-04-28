#!/usr/bin/env python3
"""
Dominion Observatory MCP Compliance Check — GitHub Action probe script.

Records a compliance event to Observatory and surfaces the server's trust
score and interaction history. Called by action.yml; reads inputs via env vars.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

OBSERVATORY_BASE = "https://dominion-observatory.sgdata.workers.dev"
GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT", "")


def set_output(name: str, value) -> None:
    if GITHUB_OUTPUT:
        with open(GITHUB_OUTPUT, "a") as fh:
            fh.write(f"{name}={value}\n")
    else:
        print(f"OUTPUT: {name}={value}")


def gha_warning(msg: str) -> None:
    print(f"::warning::{msg}")


def gha_error(msg: str) -> None:
    print(f"::error::{msg}")


def _default_agent_id(repo: str) -> str:
    clean = repo.lower().replace("/", "-").replace("_", "-")
    return f"github-action-{clean}"


def _fetch_json(url: str, timeout: int = 15):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read())


def record_interaction(agent_id: str, server_url: str, tool_name: str, success: bool) -> bool:
    """Submit one compliance event to Observatory via the Python SDK."""
    try:
        from dominion_observatory import report
        report(
            agent_id=agent_id,
            server_url=server_url,
            success=success,
            latency_ms=0,
            tool_name=tool_name,
            http_status=200 if success else 500,
        )
        return True
    except Exception as exc:
        gha_warning(f"Observatory report() failed (non-blocking): {exc}")
        return False


def fetch_trust(server_url: str) -> int:
    try:
        enc = urllib.parse.quote(server_url, safe="")
        data = _fetch_json(f"{OBSERVATORY_BASE}/api/trust?server_url={enc}")
        return int(data.get("trust_score", 0))
    except Exception as exc:
        gha_warning(f"Could not fetch trust score: {exc}")
        return 0


def fetch_compliance(server_url: str) -> tuple[int, int]:
    """Return (total_count, pass_count) for this server_url."""
    try:
        rows = _fetch_json(f"{OBSERVATORY_BASE}/api/compliance?limit=200")
        server_rows = [r for r in rows if r.get("server_url") == server_url]
        passed = sum(1 for r in server_rows if r.get("success", True))
        return len(server_rows), passed
    except Exception as exc:
        gha_warning(f"Could not fetch compliance data: {exc}")
        return 0, 0


def main() -> None:
    server_url = os.environ.get("_OBS_SERVER_URL", "").strip()
    raw_agent_id = os.environ.get("_OBS_AGENT_ID", "").strip()
    tool_name = os.environ.get("_OBS_TOOL_NAME", "ci-compliance-check").strip() or "ci-compliance-check"
    record_success = os.environ.get("_OBS_RECORD_SUCCESS", "true").lower() not in ("false", "0", "no")
    fail_below = int(os.environ.get("_OBS_FAIL_BELOW", "0") or 0)
    repo = os.environ.get("_OBS_REPO", "unknown/unknown")

    if not server_url:
        gha_error("server_url input is required")
        sys.exit(1)

    agent_id = raw_agent_id if raw_agent_id else _default_agent_id(repo)

    print(f"Dominion Observatory MCP Compliance Check")
    print(f"  server_url : {server_url}")
    print(f"  agent_id   : {agent_id}")
    print(f"  tool_name  : {tool_name}")
    print(f"  recording  : {'success' if record_success else 'failure'}")

    # 1 — Record interaction
    recorded = record_interaction(agent_id, server_url, tool_name, record_success)
    if recorded:
        print(f"  ✓ Compliance event recorded to Observatory")

    # Brief pause so the just-recorded event appears in the compliance list
    time.sleep(1)

    # 2 — Fetch trust score
    trust_score = fetch_trust(server_url)

    # 3 — Fetch compliance stats
    total, passed = fetch_compliance(server_url)
    pass_rate = int(passed / total * 100) if total > 0 else 0

    print(f"\nObservatory results for {server_url}:")
    print(f"  Trust score          : {trust_score} / 100")
    print(f"  Recorded interactions: {total}")
    print(f"  Pass rate            : {pass_rate}%")
    print(f"  Observatory ledger   : {OBSERVATORY_BASE}/api/compliance")

    set_output("trust_score", trust_score)
    set_output("compliance_count", total)
    set_output("compliance_pass_rate", pass_rate)
    set_output("agent_id_used", agent_id)

    if fail_below > 0 and trust_score < fail_below:
        gha_error(
            f"Trust score {trust_score} is below the required threshold of {fail_below}. "
            f"Check {OBSERVATORY_BASE}/api/trust?server_url={urllib.parse.quote(server_url, safe='')} "
            f"for the full behavioral history."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
