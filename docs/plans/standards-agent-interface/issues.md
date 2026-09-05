# Standards Agent Interface Issues

| ID | Severity | Finding and evidence | Objective relationship / owner | Disposition | Verification / revisit trigger |
| --- | --- | --- | --- | --- | --- |
| I1 | Design constraint | The existing 19-operation MCP surface removes transport work but retains native lifecycle bookkeeping. | Core objective; Engine facade owner | Resolved across Milestones 1–3 | Fixed before/after navigation and authoring scenarios; exact authority retained |
| I2 | Acceptance prerequisite | MCP client registration was not established in the preceding implementation turn. Subprocess protocol tests do not establish actual client usability. | A7; integration owner | Resolved: official MCP SDK 1.29.1 stdio client completed isolated walkthroughs | Real-client lookup, authoring, stale-state, and recovery walkthrough before acceptance |
| I3 | Design constraint | Current routing already returns causes/questions and Router reads expose facts. Reimplementing them in MCP would duplicate authority. | A3; Engine projection owner | Resolved: shared fact projection and same-pass routing explanations in Milestone 2 | Reviewed fixture expectations and native-route comparison; expand owner scope only on a demonstrated gap |

| I4 | Test fixture defect | Native readiness regression assumes a consumer disposition absent from the accepted corpus; identical StopIteration reproduced at milestone 2 (`d97e1028`). | A8; Engine test owner | Correct the fixture to assert and resolve its actual coverage-only obligation | Rerun native readiness regression; production review behavior unchanged |

All four findings are resolved within the admitted scope. See the milestone
reports for the deciding evidence. SDK walkthroughs establish real protocol-client
consumption; they do not claim a model-driven coding session or personal client
registration.
