# Active Repository Work

[Standards Library Effectiveness Restructure](standards-library-effectiveness/plan.md)
remains active for manual semantic-ownership reviews D001–D010, downstream pilots,
migration publication, and final acceptance. [Authoring Publication and Evidence
Clarity](authoring-publication-evidence/plan.md) is also active, beginning with its
A1 publication-observation and early-evidence slice. These plans own separate
objectives; neither changes the other's acceptance state.

- [Current plan and next slice](standards-library-effectiveness/plan.md)
- [Execution ledger](standards-library-effectiveness/execution-ledger.md)
- [Issues and resolutions](standards-library-effectiveness/issues.md)
- [Evaluation overview](../../evaluation/standards-effectiveness/README.md)

Completed prerequisites do not close the parent objective. See the
[archive](../archive/README.md) for accepted and superseded plans, and the
[decision index](../decisions/README.md) for current architecture.

## Authoring Publication and Evidence Clarity

[Authoring Publication and Evidence Clarity](authoring-publication-evidence/plan.md)
owns publication receipts, fresh checkout observations, early evidence failures,
explicit evidence binding, guarded reconciliation, and focused blocker/reuse
explanations. It is Active at A1; later milestones remain Planned with their
separate gates. The plan preserves existing publication authorization and records
all acceptance claims as pending until candidate evidence passes.

## Accepted Agent Interface Work

[Standards Agent Interface](standards-agent-interface/plan.md) delivers focused
navigation, explicit-fact discovery and routing explanations, and bound authoring
contexts over the Engine. It is `Accepted`; all three milestones and their acceptance checks are complete. It does not replace the active Standards Library Effectiveness effort.

## Engine Interface Efficiency Verification

[Agent Interface Efficiency](agent-interface-efficiency/plan.md) implements the
user-authorized continuation of the interface-38 workflow simplification: schema
presentation, bounded routed content and request-local evidence reuse. It is
`Verifying`; local implementation evidence and remaining environment/client/review
gates are recorded in its [verification](agent-interface-efficiency/verification.md)
and [findings](agent-interface-efficiency/issues.md). This bounded code-maintenance
slice does not close or replace Standards Library Effectiveness acceptance.

## Schema Projection Cleanup

[Schema Projection Correctness and Ownership](schema-projection-cleanup/plan.md)
repairs schema/data traversal, consolidates its contracts owner and separates MCP
catalog construction from transport. It preserves interface 39 and existing
client mode behavior. Verification and client-dependent compatibility retirement
are recorded in that plan's ledger and findings; this slice does not close the
Standards Library Effectiveness objective.


## Input Contract Discovery

[Input Contract Discovery](input-contract-discovery/plan.md) adds a bounded
model-accessible path to the exact running input contracts while preserving
compatibility mode. Its separate client/model qualification gate remains explicit;
transport/schema checks alone do not close the reported declaration-rendering gap.


## Agent Interaction Quality

[Agent Interaction Quality](agent-interaction-quality/plan.md) implements safe field
feedback, snapshot group vocabulary and compact focused routing. Its measured
catalog costs and conditional compatibility retirement remain explicit. This
code-maintenance slice does not close the parent standards-content objective.

## On-demand output-contract delivery

[Output-contract delivery](output-contract-delivery/plan.md) adds an explicitly
selected smaller MCP catalog and exact paged output discovery while preserving
canonical result validation. Acceptance and actual-host qualifications are recorded
in its [verification](output-contract-delivery/verification.md). It does not replace
the parent Standards Library Effectiveness effort.


## Native-only MCP cutover

[Native-only MCP](native-only-mcp/plan.md) owns retirement of input compatibility,
its live consumers and the schema inliner. Output delivery remains independent;
existing stores and workflow authority are preserved. Source and host qualification
states are recorded separately in that plan and its execution ledger.

## Immutable-work reuse

[Immutable-work reuse](immutable-work-reuse/plan.md) implements audit F01/F08: bounded
exact-capture identity proofs and operation-owned revision decoding. Current lifecycle,
evidence and publication checks stay with their existing owners. It does not close
the parent standards-content objective or introduce new public operation contracts.

## Storage lifecycle

[Storage lifecycle](storage-lifecycle/plan.md) owns audit F02/F03: avoid maintenance
writer admission when no expiry is due and omit the repeated current-store integrity
audit. Expiry, migration, corruption checks and immutable-work reuse retain their
existing owners and semantics. This slice adds no store format or public API.


## Canonical fact ownership and focused revision working set

[Fact ownership and working set](fact-ownership-and-working-set/plan.md) owns the
bounded refinement after the completed boundary, immutable-work and storage-lifecycle
repairs. It preserves material/public contracts while separating fact identity from
presentation and fixing the demonstrated focused-transition cache miss. Snapshot
capture handoff and the typed routing-edit pilot now have separate plans and
acceptance gates.


## Verified snapshot-capture handoff

[Snapshot Capture Handoff](snapshot-capture-handoff/plan.md) implements the deferred
post-admission reuse of the independently proved frozen compilation. It preserves
both capture proof passes and normal durable/lifecycle checks. The prior fact-owner
and working-set changes remain intact. The later typed routing-edit pilot has its
own plan and acceptance gates.


## Typed Routing-Edit Pilot

[Typed Routing-Edit Pilot](typed-routing-edits/plan.md) replaces the internal
representation of put/remove routing facts and rules while retaining canonical
serialization, validation timing, domain behavior and existing stores. Its scope
is one edit family, not the remaining JSON-backed edit kinds. The source sequence
from boundary repairs through this pilot is integrated on `main`. Each of its
six slices is `Accepted` after exact-source locked CI, separate independent
external review, and the acceptance owner's finding dispositions. See the
[six-slice acceptance decision](typed-routing-edits/reports/acceptance-dispositions.md)
for exact commits, CI and review reports. This bounded refactoring sequence is
closed; no further implementation slice in it is admitted.


## Routing-fact ergonomics

[Routing-fact ergonomics](routing-fact-ergonomics/plan.md) owns the separately admitted
focused input improvement, its consumer cutover and actual-agent qualification.
It is Accepted after locked CI, independent review and connected interface-45
qualification. The accepted six-slice refactoring remains closed. Review-evidence
packaging and broader test strengthening are later, separately admitted work.

## Review-evidence packaging

[Review-evidence packaging](review-evidence-packaging/plan.md) owns the local
review packet builder. Its implementation is in progress. Developer handoff ZIPs
are external artifacts and are not repository content.

## Targeted Test Strengthening

[Targeted Test Strengthening](targeted-test-strengthening/plan.md) prepares the five
selected regression-oracle improvements without product changes. Its integration
follows packaging acceptance; neither earlier accepted sequence is reopened.
