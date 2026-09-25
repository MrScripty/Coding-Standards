# Issues

| ID | Severity | Evidence and owner | Disposition | Verification / revisit |
| --- | --- | --- | --- | --- |
| PR-01 | high | Logical authoring lacks registration on an existing module; policy relationships require registered sources. | Fix in this slice. | Generic registration, final-candidate composition and MCP publication tests. |
| PR-02 | high | The local environment cannot clone GitHub and the available recovered source is partial. Verification owner. | Continue bounded source work; qualify only claims reached by actual checks. | Full checkout with locked runtime is required for complete package/MCP acceptance. |
| PR-03 | medium | Existing sidecar helper treats a registered tombstone-only derived sidecar as unregistered. Logical-authoring owner. | Fix in this slice because new registration must preserve the owner's retired identity history. | Register a fresh unit after all previous active units were retired; tombstones retained. |
| PR-04 | high | Preserved proposal and its current store are on the user's machine, not in this environment. Integration owner. | Preserve by access boundary; no resets or inferred readiness. | Inspect and resume through installed authoring operations after qualification. |

## Current dispositions

PR-01 and PR-03 are implemented in source; their complete canonical/runtime acceptance is blocked by PR-02. The new schema and generated consumers are verified. PR-04 remains a deployment boundary: the external proposal was untouched and must be inspected through the qualified installed authoring interface before resuming. No issue is closed by assuming that isolated checks replace its required real evidence.
