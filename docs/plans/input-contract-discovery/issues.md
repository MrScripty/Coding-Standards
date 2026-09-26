# Findings and acceptance gates

- D1 — Open: actual client/model qualification. The user reported native declarations
  losing essential fields. Discovery now supplies a separately tested access path;
  this execution has no installed/authenticated Codex and did not run a model turn.
  Owner: host/operator. Use the opt-in harness and inspect the actual exposure surface.
  Retain compatibility until each supported deployment has an accepted path.
- D2 — Open: supported environment. Local CPython 3.13.5/rpds-py 2026.5.1 differ from
  supported locked CPython 3.11/3.12/rpds-py 2026.6.3. Owner: integration. Run the
  updated tree in locked CI. The baseline's successful CI is not new-change evidence.
  Integration follow-up (2026-09-26): supported local CPython 3.12.3 with locked
  dependency versions passes the contracts environment check without a skip;
  see verification.md and execution-ledger.md. CI remains a separate gate.
- D3 — Open: independent review. Owner: integration. Review the exact diff and
  evidence before acceptance; implementation self-review does not replace this gate.
- D4 — Resolved: three explicit application-catalog test assertions omitted the new
  read-only observation. They now enumerate it without weakening purpose exclusions.
- D5 — Resolved: the reference CLI listed native operations but initially described
  only the focused MCP subset. Its observers now use its full published surface;
  cold tests cover native-operation discovery without a Git repository or store.
- D6 — Resolved: checking only that discovery was called could accept guesses about
  unread fields. Qualification now requires the exact used definitions before each
  authoring call and tests the nested-oneOf counterexample against weaker checks.
