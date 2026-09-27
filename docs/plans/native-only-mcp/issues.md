# Native-only MCP findings and dispositions

| ID | Severity / boundary | Evidence and relevance | Owner | Disposition and required verification |
| --- | --- | --- | --- | --- |
| N-01 | Source-identification risk | Connector head is `52b12268`; the running system is reported at interface 42. Planning used the verified delivered interface-42 overlay. | Implementer/integrator | Confirm the actual integrated checkout before editing. Preserve later changes. Re-plan only for a material contract/owner change; this is not authority to overwrite it with the older commit. |
| N-02 | Functional design observation | The proposed reference-only catalog removes the inliner but slightly increases bytes. Fixture agreement is not model-visible qualification. | Implementer and host operator | Accepted size tradeoff. Run semantic tests and a fresh real native/on-demand path on the candidate. A discoverability failure changes the design; it must not be masked by a no-op flag or unknown-field acceptance. |
| N-03 | Retained-evidence boundary | Historical replay presently chooses native/compatibility from the recording and rebuilds that catalog. New source/interface digests may differ from old recordings. | Qualification owner | Remove alternate live rendering. Preserve original recordings and verdicts. Explicitly report mismatched/retired recordings as outside current-source replay; use their original pinned tooling when retrospective adjudication is required. Keep chronology and source checks. |
| N-04 | Coupled test construction | Three client/replay consumers build an eager catalog solely to obtain private output validators. | Qualification owner | Derive validators from existing canonical result roots through one narrow helper in the current observer owner. Verify they are not supplied to the model. No new production schema authority. |
| N-05 | Possible orphan utility | `map_schema_children` is exported but its only production caller in the bounded inspection is the retiring inliner. | Standards Contracts owner | Reconfirm repository callers, remove the mapper/export/transform-only tests together. Preserve closure/traversal contracts and their semantic regressions. A real independently supported consumer changes this disposition and triggers re-planning. |
| N-06 | Required acceptance environments | Source is implemented and locally verified. Prior native reports do not qualify the new projection or host argument change. Local planning environment is outside the repository's locked runtime. | Host operator, CI owner, independent reviewer | Keep A7–A9 pending. Run the unchanged supported-runtime checks, actual connected-client path and independent material review. Unavailable evidence blocks only its acceptance claim. |
| N-07 | Scope boundary, not a defect | Eager output delivery is independently selectable and still used by validating consumers/tests. Native-only input does not retire it. | Product/integration owner | Preserve output choices/default in this slice and keep the known host explicitly on-demand. Revisit only under a separate explicit decision about output delivery. |

Input compatibility itself has a **remove-now** disposition under the owner's native-only instruction. No requirement to support an unspecified client remains. Unrelated ZIPs, original qualification artifacts and the Standards Library Effectiveness objective remain outside this removal effort.


## Implementation dispositions

N-01: the verified interface-42 delivery was reconstructed after the connector still
returned the older head and direct Git network lookup failed. Source implementation
uses that exact material baseline. File-hash checked patch application is required;
actual later integration differences remain with the integrator, not overwritten.

N-03/N-04/N-05: implemented. Replay no longer constructs a compatibility catalog;
private validators use canonical result roots; the mode/inliner/orphan mapper are
removed and preservation tests retained. Observer edition is 3.

N-08 — test-consumer updates, fixed in N1: the first candidate focused run retained
an obsolete compatibility-size assertion and an observer-edition assertion. They
were corrected at the test owner; production validation was not weakened.

N-06 remains an acceptance limitation: only Python 3.13.5/rpds-py 2026.5.1 is
available locally, not locked 3.11/3.12; actual host config/Codex and independent
review are unavailable. These are explicit N2/CI evidence requirements, not reasons
to reintroduce compatibility. Candidate results are in reports/verification.md.

N-09 — stale trace dimension, fixed in N1: the complete Engine selection found
`test_efficiency_trace.py` still expecting four routing measurements. The native-only
trace now owns two purposes and one shared-evidence comparison. Preserve all
behavioral assertions and rerun that actual cold-stdio scenario. This adjacent
consumer is added to the write set; the plan's composition is unchanged.

N-10 — current example metadata, fixed in N1: two current discovery-result examples
retained old interface numbers. Align those authored current examples to edition 43
and verify their consistency; preserve historical data unchanged.

## Final acceptance disposition

N-03/N-04/N-05/N-08/N-09/N-10 have implemented repairs and passing local evidence.
N-02's size tradeoff is confirmed; actual-client qualification remains with A8.
N-01 is resolved for source production by the verified interface-42 reconstruction
and per-file delivery preconditions; the integrator must preserve later differences.
N-06 blocks A7–A9 at the named environment/operator/reviewer boundaries. N-07 remains
a preserved scope constraint, not an outstanding defect. No compatibility code is
retained to compensate for an unavailable acceptance environment.
