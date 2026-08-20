# Planning Proportionality Recovery Issues

| ID | Severity | Finding | Owner | Disposition | Verification |
| --- | --- | --- | --- | --- | --- |
| PPR-001 | high | Generic Planning mandates a concrete cryptographic transition protocol without aligned prompts, templates, or executable construction and validation. | `workflow.planning` | Fix in Milestone 2 by separating the generic invariant from conditional profile and reference mechanism. | Ordinary-plan and concurrent-profile positive and negative scenarios |
| PPR-002 | high | Active plans contain accepted execution history despite assigning that history to ledgers and reports. | `workflow.planning` | Fix after historical authority migration in Milestones 3 and 4. | Structural review and plan-consumer absence proof |
| PPR-003 | high | Verifiers consume accepted active-plan narration as machine authority, making compaction unsafe. | Verification owners | Exact inventory accepted; migrate `PPR-C1` and `PPR-C2` in Milestone 3. | [Consumer dispositions](reports/active-plan-consumer-dispositions.tsv) and complete verification |
| PPR-004 | medium | Planning requires semantic typed outcomes but could be misread as requiring one serialized program representation. | Planning and concurrent-profile owners | Clarify in Milestone 2. | Manual and automated scenario review |
| PPR-005 | resolved | The exact active-plan consumer disposition table creates real documentation references that stale the generated checker inventory. | Verification-engine generated evidence | Regenerated the four affected artifacts in the reopened Milestone 1 gate; the edges remain non-authoritative observations. | Generator check, exact edge-source review, and complete mixed checkpoint passed |
