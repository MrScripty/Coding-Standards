# Issues

| ID | Severity | Evidence and owner | Disposition | Verification / revisit |
| --- | --- | --- | --- | --- |
| PR-01 | high | Logical authoring lacked registration on an existing module; policy relationships require registered sources. | Resolved in the code correction. | Generic registration, final-candidate composition and MCP publication tests passed. |
| PR-02 | high | The original delivery environment could not clone GitHub and its recovered source was partial. Verification owner. | Resolved for code qualification in the complete local checkout. | Supported Python 3.12.3, full 281-test Engine suite and official MCP client passed. |
| PR-03 | medium | Existing sidecar helper treated a registered tombstone-only derived sidecar as unregistered. Logical-authoring owner. | Resolved; reuse the owner and retain retired identity history. | Fresh registration after all previous active units were retired passed. |
| PR-04 | high | Preserved proposal and its current store are on the user's machine, not in this environment. Integration owner. | Preserve by access boundary; no resets or inferred readiness. | Inspect and resume through installed authoring operations after qualification. |

## Current dispositions

PR-01 and PR-03 are resolved: the canonical registration tests, full 281-test Engine suite and official MCP SDK walkthrough passed in the complete checkout. PR-02's environment block was resolved for code qualification by using the complete local checkout and supported Python 3.12.3 environment. PR-04 remains a deployment boundary: the external proposal was untouched and must be inspected through the qualified installed authoring interface before resuming. See the [verification report](reports/verification.md) for the exact evidence.
