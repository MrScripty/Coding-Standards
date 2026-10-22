# Principle audit of the CodeRabbit standards proposals

Audit date: 2026-10-04.

The CodeRabbit findings do not establish a missing underlying principle that
requires a new normative rule, or a reason to remove an existing principle.
The earlier drafts mostly elaborate principles already present in the accepted
standards. Recommend one concise clarification of evidence reuse, optional
reference examples, and a separate generality review of the existing
serialization restriction. Do not adopt the detailed new normative sections
as written.

## Authority, scope and method

Compared the three [draft proposals](proposals.md) with 40 exact, snapshot-bound
Coding Standards MCP authoring reads. The accepted source revision is
`dcc56f26e884ade260770beceba2501d3746200d`; the retained snapshot is
`snapshot:v1:eda55cdb-e388-4385-a610-ed634d82096e`.
The two saved proposal revisions were read back through `query_proposal`.
Proposal 1 has submitted wording but no saved MCP candidate because its
submissions were rejected. This audit supplies no formal Engine review decision.

Re-read all 138 formal finding summaries and 28 discussion observations in
`CodeRabbit_Audit_MrScripty_2026-10-04.zip`, checked its coverage statistics and
check-observation data, and used the earlier finding crosswalk for traceability.
The ZIP SHA-256 is
`97658b671252aef1e1890f03567185495cb7d227827bdb9cd92cd4ba6e68115a`.

The earlier classification was 95 covered reports, 17 clarification
opportunities, 19 recipe opportunities, 6 advisory or conditional reports and
1 withdrawn report. A clarification or recipe opportunity is not a missing
principle. The 131 reports in the first three groups already map to existing
principles; the six conditional reports depend on project authority rather
than establishing universal obligations.

This is a policy-content and generality audit, not a reproduction of current
project defects or a fresh inspection of their implementations. Original
standards adoption and version at the time of each finding remain unknown.
Repeated findings alone do not prove that a principle is absent, ineffective,
or available to the implementing agent.

[Exact MCP content, quote evidence and graph observations](principle-audit-evidence.json)
are retained for this comparison. [Source finding records and user constraints](evidence.md)
provide the archive context. The original proposals and their MCP states remain
unchanged.

## Principle comparison

| Underlying principle | Existing owner and coverage | Finding evidence | Decision |
| --- | --- | --- | --- |
| Evidence supports only the claim, scope and material conditions it establishes. | Verification: Acceptance Is A Set Of Claims, Coverage And Durable Evidence Records; Contracts: Invariant Contracts; Build: Invalidation And Incrementality. | CR-0099, CR-0110, CR-0115, CR-0118, CR-0119, CR-0123, CR-0124, CR-0129. | Existing principle. A short reuse clarification is useful; a new identity policy and mandatory receipt procedure are unnecessary. |
| A completeness conclusion needs proof covering the promised population or result. | Verification: Acceptance Paths And Boundaries; Oracles: Property And Differential Evidence; Contracts: Runtime Decoding At Boundaries. | CR-0098, CR-0103, CR-0116, CR-0117, CR-0127, CR-0128, CR-0131, CR-0136. | Existing principle. Keep membership, Git-state and truncated-comparison illustrations in references. |
| Expected semantics require independent or otherwise authoritative justification. | Oracles: Evidence Oracle Boundaries; Generated Contract profile: Semantic Closure. | CR-0103, CR-0104, CR-0125, CR-0135. | Explicitly covered. No new principle or duplicate policy scope. |
| A claimed invariant must survive the complete operation, including publication and relevant observation effects. | Contracts: Invariant Contracts; Build: Inputs, Outputs, And Side Effects; Persistence: Durable Mutation Contract; Core: Change Integrity. | CR-0056, CR-0059, CR-0130, CR-0132, CR-0137. | Existing principle. An observer's own write is an application of the same postcondition. |
| Verification must observe the intended resource, valid preconditions and owned lifecycle. | Verification: Test Design, Test Data Authority And Lifecycle, Async Completion And Failure Evidence; Concurrency: Isolate Verification Resources; Cross-Platform: Platform Support Contract. | The 16 O3 reports, plus CR-0029. | Existing principle. Optional context-specific examples can help; no sandbox requirement. |
| Required invariant enforcement follows the supported contract and proof lifetime. | Contracts: Invariant Contracts; Persistence: Durable Mutation Contract where applicable. | CR-0100, CR-0112, CR-0114; conditional discussion DC-025. | Explicitly covered, including build modes. Python examples need no new rule. |
| A selected review or tool gate proves only the property and scope it actually examines. | Verification: Quality Gates And Execution Location, Supporting Gates And Claim-Directed Diagnosis; Tooling: Tooling Authority, CI Orchestration And Scheduling. | PR coverage observations; CR-0069, CR-0070, CR-0091, CR-0107 as related scope examples. | Existing principle. Omit the proposed separate Review Evidence Scope rule; retain an optional illustration. |
| Choose a mechanism from the invariant, authority, capability, lifecycle and cost. | Core: Simplicity And Ownership; Verification: Test Data Authority And Lifecycle; Concurrency: Select Coordination From The Invariant. | CR-0008, CR-0029, CR-0063, CR-0064, CR-0068, CR-0089, CR-0133 illustrate context-sensitive decisions. | Preserve the principle. Separately review the serialization restriction for unnecessary specificity. |

## Why the proposed new rules are mostly redundant

### Retained evidence identity

Verification already states:

> Evidence satisfies only the claim it actually proves.

Contracts also says that successful earlier validation does not authorize stale
proof. Verification requires sufficient durable reproduction and interpretation
context, and Build derives invalidation from material inputs rather than
defaulting to always rerun or never rerun.

Together, those principles already reject using an old result to justify a
changed claim without establishing applicability. The reported executable,
renderer, workload and aggregate mismatches are different manifestations of
that same problem.

The useful improvement is to make the reuse decision explicit at Verification's
existing evidence-context owner. Suggested clarification:

> When reusing evidence, establish that its scope and material validity
> conditions still support the current claim.

This is an explanation of the existing obligation, not a new proof system.
Existing records, construction guarantees, invariance reasoning or a focused
rerun can establish applicability. A source change does not automatically
invalidate every prior observation; the required claim and material conditions
decide that.

The original draft's blanket rerun wording is too easy to interpret as rejecting
valid transfer or reasoning. Lists of executables, renderers, hashes and receipt
fields should be reference examples selected only when relevant.

**Recommendation:** optionally update the existing Verification paragraph with
the concise clarification. Do not create a separate retained-identity rule or
require universal identity records. Current principles already justify
rejecting the reported unsupported qualifications.

### Complete inventories and comparisons

Verification already requires the complete promised result. Oracles identifies
the actual compared domain and forbids silently narrowing a claim to the cases
the comparator happens to support. Contracts requires every invariant needed
to construct a validated representation.

An empty loop cannot establish a required nonempty population, and comparison
of only shared positions cannot establish equal complete sequences. These
follow from the selected contract; they are not new universal collection rules.

The proposed instruction to reject unexpected members also needs the owning
contract's extra-member policy. Some contracts accept extension fields, project
a subset, or permit empty populations. Counts can be sufficient when independent
construction guarantees already establish identity and membership.

Likewise, a Git diff is adequate for a claim limited to the state it observes.
It is inadequate for a broader protected-state claim that includes omitted
index, untracked or ignored state. The general decision is to match observation
to claim, not to inventory all Git state for every project.

**Recommendation:** no new completeness principle. Move the specific failure
patterns to optional references; preserve construction proofs and actual
population semantics.

### Observation and publication effects

CR-0130 reports a preservation check that passes before its own receipt creates
a protected addition. Existing invariant, permitted-side-effect, write-boundary
and publication-postcondition requirements already cover this.

Persistence explicitly distinguishes completion of one write from consistency
of the complete invariant. The relevant mechanism might be an appropriate
output location, staging, a transaction, or another contract-specific guarantee.

**Recommendation:** no new observer-effect rule. Use this finding as an
illustration of applying postconditions across the whole owned operation.

### Fixtures, readiness, platform capability and optimized Python

Verification already requires independent fixture identity, material
preconditions and the receiving claim's context. It selects sharing and
coordination from mutation, concurrency, ordering, resource cost and the proved
boundary. Concurrency permits exclusive ownership or an explicit coordination
contract that proves the invariant.

CR-0008 asks for test-controlled release waits not to expire; CR-0064 asks for a
bounded observation watchdog. Those are compatible because the waits own
different responsibilities. Neither finding supports a universal timeout rule.

CR-0068 and CR-0133 concern inherited Git settings redirecting commands into the
wrong repository. CR-0029 concerns removing necessary proxy and TLS capability.
Together they support selecting the environment facts material to the operation,
rather than either accepting all ambient state or clearing everything.

Contracts already states:

> Build mode alone does not decide which invariants remain enforced, and
> successful earlier validation does not authorize stale proof.

Python optimization is a concrete example of that existing principle. The
supported execution contract decides which modes matter; the example cannot
require optimized-mode support for every Python project.

**Recommendation:** retain proposal 2 only as optional reference material, with
each example tied to its existing owner and circumstances. No new fixture,
timeout, optimization or sandboxing principle.

### Review completion and scope

The archive reports bot activity on 139 of 150 PRs and completed code review on
45. This does not establish that all 150 required a review gate, that the
remaining PRs violated one, or that completed reviews covered their final heads.
A completed zero-finding review can be valid evidence; an empty finding list
alone cannot establish its completion or scope.

Verification already derives gates from named claims, scope and authority.
Tooling expressly assigns evidence meaning to Verification and owns
orchestration. A new Tooling rule about the meaning of review evidence would
repeat that responsibility.

**Recommendation:** omit proposal 3's new normative section. If useful, explain
review completion, scope and transfer in an optional reference under the existing
evidence principles. Do not infer a mandatory reviewer, cadence, receipt or
full-file scope from these coverage statistics.

## Existing wording that merits a generality review

Concurrency's Isolate Verification Resources currently says:

> Serialization is a valid selected mechanism only when the owner records the
> shared invariant, exclusion scope, and reason independent ownership cannot be
> established.

The first paragraph of that section permits explicit coordination that proves
the invariant. Verification selects sharing and synchronization from the actual
resource contract and cost. Requiring independent ownership to be impossible
can be read as imposing a preferred mechanism beyond those general principles.

A deliberate shared fixture may be appropriate even when separate fixtures
are technically possible. Conversely, serialization cannot establish a claim
that requires overlapping execution or hide unknown interference.

**Recommendation:** review this qualification and, if that restrictive meaning
is confirmed, replace the impossibility condition with a requirement to justify
the selected coordination against the invariant, lifecycle, required parallel
evidence and cost. Preserve resource ownership, cleanup and adequate proof.
This removes a potentially overprescriptive constraint, not an underlying
principle.

This is an editorial generality issue discovered by comparing the standards.
The CodeRabbit reports do not demonstrate a defect caused by the serialization
restriction, so it is not counted as a confirmed archive-derived policy gap.
The heading's “isolation” refers to resource ownership or coordination, not a
project implementing an operating-system sandbox.

## Sweep of the remaining finding categories

The broader reports reinforce existing owners rather than introducing new
principles. Counts below are reported formal findings, including advisory
reports and the single withdrawal; category frequency does not establish need.

| Reported category | Count | Existing principle families | Representative reports |
| --- | ---: | --- | --- |
| Evidence / CI / test reliability | 46 | Claim-directed evidence, authoritative oracles, fixture lifecycle, gate scope and measurement fidelity. | CR-0002, CR-0099, CR-0125 |
| Documentation / contract drift | 17 | Current canonical authority, evidence-scoped status, documentation selected from actual consumer needs. | CR-0001, CR-0051, CR-0076 |
| Resource bounds & performance | 12 | Owned resource limits, representative measurement, cost and lifecycle bounds. | CR-0003, CR-0050, CR-0074 |
| Lifecycle & cancellation ownership | 9 | Owned async work, valid state transitions, cessation of relevant effects and cleanup. | CR-0004, CR-0005, CR-0018 |
| Compatibility & environment | 4 | Declared capability and supported targets; preserve material environment and identity facts. | CR-0006, CR-0029, CR-0067 |
| Error handling & availability | 14 | Classified failures, scoped degradation, preserved typed outcomes and observed completion. | CR-0009, CR-0017, CR-0038 |
| Validation & identity correctness | 13 | Complete authoritative contracts, proof lifetime, correct identity and error classification. | CR-0012, CR-0058, CR-0083 |
| Security & privacy | 8 | Least authority, declared execution trust, secure transport and controlled disclosure. | CR-0013, CR-0031, CR-0057 |
| Filesystem / data integrity | 8 | Complete durable mutation, authoritative-state preservation, publication and recovery. | CR-0037, CR-0044, CR-0056 |
| Maintainability / clarity | 3 | Explain material meaning proportionately; formatting and lint policy follow project authority. | CR-0052, CR-0102, CR-0108 |
| Numerical / scientific correctness | 3 | Domain-owned invariants, complete observable outcomes, bounded failure and independent evidence. | CR-0093, CR-0096, CR-0106 |
| Accessibility / user interface | 1 | Meaningful task information through required modalities and evidence at the actual interaction boundary. | CR-0138 |

The licence-attribution report CR-0023 is also covered by Licensing's existing
requirement to preserve terms and required notices; its documentation category
does not make licensing a new principle.

The six conditional reports—CR-0052, CR-0062, CR-0091, CR-0102, CR-0107 and
CR-0108—do not establish universal heading rules, runner budgets, Cargo option
ordering, pin comments, CI trigger paths or memory-layout comments.

CR-0105 was explicitly withdrawn and supplies no evidence for a new rule or
production refactor. The 28 discussion observations preserve hypotheses,
pre-existing follow-ups and deployment assumptions as such; they are not
28 additional independently validated defects. Docstring check observations
do not justify a universal “document every function” principle.

## Delivery and effectiveness are separate questions

The authoring MCP returned `current` application exposure for 7 of the 40
inspected modules and `unreviewed` for 33. The exact module list is in the
audit evidence. This means the principles exist in accepted authoring content;
it does not establish that an application-purpose agent can receive all of
them through its qualified reading path.

Before attributing downstream failures to weak principles, inspect relevant
application qualification, routing, selected references and actual agent
decisions. Current uncommitted repository changes are outside this accepted
snapshot and may affect a later published view. This audit does not resolve
qualification or certify historical delivery.

The Verification acceptance-claims scope has declared policy-impact consumers
across topics, workflows, profiles, planning prompts and the plan template.
Any later normative revision must review that actual closure. The queried
Concurrency edges concerned its cessation-of-effects scope; they are not proof
that every consumer of the serialization wording has already been registered.
Graph presence, authoring reads and this audit are not material-review or
publication approvals.

## Disposition of the existing drafts

| Draft | Audit disposition |
| --- | --- |
| 1: Retained identity and inventories | Do not adopt as written. Consider one concise clarification in existing Verification text; retain detailed examples separately. Its failed MCP submission remains a failed submission. |
| 2: Fixture and Python recipes | Potentially useful reference-only addition. Check example accuracy, scope and discoverability; it adds no normative principle. The saved MCP draft remains unreviewed. |
| 3: Review Evidence Scope | No distinct new normative principle is justified. Recommend omitting this addition and using a scoped reference example if needed. The saved MCP draft remains unreviewed. |

No standards, policy registrations, application declarations or proposal
decisions were changed by this audit. Recommendations to omit draft rules are
not recommendations to delete the existing evidence, invariant, ownership,
coordination, security or lifecycle principles.
