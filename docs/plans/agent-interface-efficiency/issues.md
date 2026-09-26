# Findings

- E1 — qualification: local Python is outside the supported locked environment.
  Owner: integration. Run the unchanged locked CI checks before accepted integration.
- E2 — client qualification: configured Codex/MCP SDK clients are not present locally.
  Owner: host operator. Retain default compatibility mode; run the optional client
  harness before selecting native presentation for that deployment. Raw stdio tests
  prove protocol consumption, not client rendering or model behavior.
- E3 — acceptance: independent external review is not available in this execution.
  Owner: integration. Review the base-pinned diff and evidence before acceptance.
