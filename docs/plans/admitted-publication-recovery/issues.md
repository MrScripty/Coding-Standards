# Issues

| ID | Severity | Owner | Finding | Disposition |
| --- | --- | --- | --- | --- |
| APR-1 | high | Engine publication | An admitted application at its unchanged target has no completion action. | Implemented; focused and cold-MCP exact-identity recovery passed. |
| APR-2 | medium | Git / Engine diagnostics | Git stderr exists internally but is omitted from the publication result; update-ref failure also discards it. | Implemented; real lock/permission tests and fixed-phrase disclosure tests passed. |
| APR-3 | high | Deployment operator | Reported read-only .git restriction is plausible but not confirmed here. | Operator supplies authorized writable host; no restriction bypass or manual ref repair. |
| APR-4 | medium | MCP lifecycle | Existing session catalogs remain stale after code replacement. | Document process restart/reconnect; automatic hot reload remains separately scoped. |
| APR-5 | medium | Workflow delivery | Repeated large responses and serial decisions are costly. | Preserve existing decision/evidence semantics; batching and result pagination require a separate measured change. |
| APR-6 | high when applicable | Review evidence owner | An installation can alter a file cited as live review evidence. | Cross-edition drift correctly blocks completion; preserve unchanged evidence or obtain its supported review disposition. Never bypass the digest check. |
