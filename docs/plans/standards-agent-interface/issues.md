# Standards Agent Interface Issues

| ID | Severity | Finding and evidence | Objective relationship / owner | Disposition | Verification / revisit trigger |
| --- | --- | --- | --- | --- | --- |
| I1 | Design constraint | The existing 19-operation MCP surface removes transport work but retains native lifecycle bookkeeping. | Core objective; Engine facade owner | Address across Milestones 1–3 | Fixed before/after navigation and authoring scenarios; exact authority retained |
| I2 | Acceptance prerequisite | MCP client registration was not established in the preceding implementation turn. Subprocess protocol tests do not establish actual client usability. | A7; integration owner | Establish an isolated client connection during implementation | Real-client lookup, authoring, stale-state, and recovery walkthrough before acceptance |
| I3 | Design constraint | Current routing already returns causes/questions and Router reads expose facts. Reimplementing them in MCP would duplicate authority. | A3; Engine projection owner | Reuse existing domain outputs in Milestone 2 | Reviewed fixture expectations and native-route comparison; expand owner scope only on a demonstrated gap |

No implementation defect is declared fixed by this planning record. Add findings
with their evidence and disposition as implementation proceeds.
