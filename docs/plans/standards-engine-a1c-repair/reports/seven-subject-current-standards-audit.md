# Seven-Subject Current-Standards Audit

## Boundary

This audit covers the seven A1c coverage subjects whose repository attestations
were already older than their policy-unit semantic revisions at repair base
`3faf889185ee0e4eff0b57f2fff3b44185c10072`:

- `topic.architecture.immutable-authority-closure`;
- `topic.contracts.invariant-contracts`;
- `topic.contracts.validation-proof-lifetime`;
- `topic.contracts.version-scope-and-invalidation`;
- `topic.dependencies.implementation-versus-dependency`;
- `workflow.planning.systemic-finding-replan`; and
- `workflow.verification.acceptance-claims`.

The accepted Standards Simplicity And Evidence Proportionality review already
dispositions 64 current relationships from these subjects. Direct compilation
of the current graph proves those 64 triples remain present with no retired or
blocked disposition. A1c contributes another 35 current relationships that
postdate that standards review. This report dispositions those consumers and
reopens two evidence-suite projections whose old text assertions do not decide
the current policy.

## Existing Review Reuse

The following accepted records remain semantic authority for the canonical
policy changes and their 64 unchanged consumers:

- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/policy-impact-dispositions.tsv`;
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-2-evidence-and-proof-acceptance.md`;
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/milestone-3-promise-and-replanning-acceptance.md`; and
- `docs/plans/standards-simplicity-and-evidence-proportionality/reports/final-acceptance.md`.

Reuse is by exact policy subject and current relationship triple, not by report
age or filename. The A1c-specific relationships below receive a fresh current
disposition.

## A1c Consumer Dispositions

| Source | Consumer | Disposition | Current-standards result |
| --- | --- | --- | --- |
| Immutable Authority Closure | `a1c-aggregate-replay` | retain | The registered suite proves cold reconstruction of one immutable analysis aggregate rather than independently authoritative children. |
| Immutable Authority Closure | `a1c-snapshot-lifecycle` | retain | The registered suite proves snapshot aggregate persistence, lifecycle, and exact closure through owner-local operations. |
| Immutable Authority Closure | `tools/standards_engine/tests/test_analysis.py` | update | Milestone 0 repaired current contract and replay closure evidence; complete advertised child-kind cold inspection remains required in Milestone 2. |
| Immutable Authority Closure | `tools/standards_verifier/tests/test_policy_impact.py` | reviewed-no-change | The fixture verifies compiled projection behavior and creates no persistent authority or reconstruction promise. |
| Immutable Authority Closure | `tools/graph_engine/graph_engine/projection.py` | reviewed-no-change | The immutable graph projection is an in-process value with no independent cold-replay promise. |
| Immutable Authority Closure | `tools/graph_engine/graph_engine/registry.py` | reviewed-no-change | The registry owns graph composition and does not persist a second authority lifecycle. |
| Immutable Authority Closure | `tools/repository_git/repository_git/model.py` | reviewed-no-change | Repository Git values are bounded source observations; Snapshot owns durable captured authority. |
| Immutable Authority Closure | `tools/standards_analysis/standards_analysis/coverage.py` | update | Milestone 1 replaces repository-global subject invalidation with exact subject, relationship, consumer, and evidence-suite closure while retaining separate completeness review. |
| Immutable Authority Closure | `tools/standards_analysis/standards_analysis/kernel.py` | reviewed-no-change | The kernel derives work from one AnalysisState and does not persist derived packets, reports, or children as separate authority. |
| Immutable Authority Closure | `tools/standards_analysis/standards_analysis/state.py` | updated | Milestone 0 now separates malformed and unsupported state and binds current domain contracts during cold reconstruction. |
| Immutable Authority Closure | `tools/standards_analysis/standards_analysis/trust.py` | reviewed-no-change | Exact evidence and authorization records enter AnalysisState; live provider execution does not occur during projection. |
| Immutable Authority Closure | `tools/standards_engine/standards_engine/_generated_contract.py` | reviewed-no-change | Generated values are public representation proofs, not independent semantic or persistence authority. |
| Immutable Authority Closure | `tools/standards_engine/standards_engine/engine.py` | updated | Milestone 0 compares first-pass and frozen-replay path and semantic closures and rejects current-domain mismatch on cold load. |
| Immutable Authority Closure | `tools/standards_graph/standards_graph/repository.py` | reviewed-no-change | Repository graph composition derives an in-process graph from immutable Metadata and Policy Impact values. |
| Immutable Authority Closure | `tools/standards_metadata/standards_metadata/source.py` | reviewed-no-change | ContentSource exposes exact immutable path bytes without acquiring snapshot lifecycle or persistence authority. |
| Immutable Authority Closure | `tools/standards_policy_impact/standards_policy_impact/compiler.py` | reviewed-no-change | The compiler derives one immutable relationship value from supplied authority and does not persist another lifecycle object. |
| Immutable Authority Closure | `tools/standards_snapshots/standards_snapshots/errors.py` | reviewed-no-change | Snapshot failure values describe owner-local outcomes and carry no independent authority. |
| Immutable Authority Closure | `tools/standards_snapshots/standards_snapshots/model.py` | reviewed-no-change | Unique snapshot roots and content identity have separate meanings inside one Snapshot-owned aggregate. |
| Immutable Authority Closure | `tools/standards_snapshots/standards_snapshots/module.py` | reviewed-no-change | One Snapshot Module owns create, find, quarantine, undelete, purge, content, and linked-analysis lifecycle. |
| Immutable Authority Closure | `tools/standards_snapshots/standards_snapshots/store.py` | reviewed-no-change | SQLite is hidden storage for the one aggregate; it does not expose a public generic authority repository. |
| Immutable Authority Closure | `tools/standards_verifier/standards_verifier/policy_impact.py` | reviewed-no-change | Verifier independently checks repository projection and does not become runtime semantic authority. |
| Version Scope And Invalidation | `tools/standards_analysis/standards_analysis/kernel.py` | reviewed-no-change | Analysis contract values are scoped to their current representation and semantic identity roles; no umbrella release version is used. |
| Version Scope And Invalidation | `tools/standards_contracts/standards_contracts/projection.py` | reviewed-no-change | Contract projection versions describe the generated public representation and advance independently from domain identities. |
| Version Scope And Invalidation | `tools/standards_engine/contracts/a1-contract.schema.json` | reviewed-no-change | Schema, request, result, and handle values have explicit current roles; the schema does not own domain semantic versions. |
| Version Scope And Invalidation | `tools/standards_engine/standards_engine/_generated_contract.py` | reviewed-no-change | Generated constants mirror owner-scoped schema roles and do not create another version authority. |
| Version Scope And Invalidation | `tools/standards_engine/standards_engine/tools.py` | reviewed-no-change | The facade consumes current request/result/handle contracts without a shared implementation-release gate. |
| Version Scope And Invalidation | `tools/standards_snapshots/standards_snapshots/model.py` | reviewed-no-change | Snapshot handle format, allocation identity, content identity, and store format remain distinct roles. |
| Version Scope And Invalidation | `prompts/implement-plan.md` | reviewed-no-change | Implementation preserves admitted owner-scoped versions and rejects umbrella invalidation. |
| Version Scope And Invalidation | `prompts/planning.md` | correct | The current instruction incorrectly scopes identity invalidation to a compatibility promise. It must require role classification and separate current-format, identity, compatibility, migration, and allocation consequences. |
| Version Scope And Invalidation | `templates/PLAN-TEMPLATE.md` | correct | The simplicity probe must distinguish version roles, actual overlap promises, and identity-invalidation scope rather than recording one undifferentiated line. |
| Implementation Versus Dependency | `prompts/planning.md` | reviewed-no-change | It requires an established dependency comparison over maintained subset, conformance, security, maintenance, and unsupported-domain cost. |
| Implementation Versus Dependency | `prompts/implement-plan.md` | reviewed-no-change | It stops on an unreviewed implementation-versus-dependency decision without forcing adoption or retroactive deletion. |
| Systemic-Finding Re-Planning | `prompts/planning.md` | correct | It still requests sibling producer/consumer inventory. It must bound the canonical owner and reachable consumer population and admit proportional stop and replacement alternatives. |
| Systemic-Finding Re-Planning | `prompts/implement-plan.md` | correct | It must expand only for a new semantic owner, reachable consumer, material risk, or promise and must not treat another file inside a bounded owner as a new design scope. |
| Systemic-Finding Re-Planning | `templates/PLAN-TEMPLATE.md` | correct | The audit fields must capture the bounded owner/population, expansion facts, deletion or proof-substitution alternatives, stop evidence, and repaired-composition comparison. |

## Reopened Evidence Dispositions

| Consumer | Disposition | Reason |
| --- | --- | --- |
| `contract-authority-scope` | update | Its prompt and template assertions preserve the older compatibility-centric wording and do not prove the current version-role distinction. |
| `systemic-finding-replanning` | update | Its prompt and template assertions require the superseded unbounded sibling inventory instead of the current owner/reachability stopping rule. |

## Complete Relationship-Group Closure

The five directly stale files are not the complete change closure. Repository
graph traversal produces these additional obligations:

- The `policy-impact` and `semantic` groups contain the same 53 incident
  relationships to the three projections and two suites. Group membership does
  not duplicate authority. Twenty-five unique policy subjects select at least
  one changed consumer.
- The three projection files are registered inputs to 14 suites:
  `a1c-public-cutover`, `commit-consolidation-dispositions`,
  `concurrent-plan-integration`, `contract-authority-scope`, `core-simplicity`,
  `evidence-oracle-boundaries`, `implementation-versus-dependency`,
  `plan-implementation-entrypoint`, `plan-template-projection`,
  `planning-consolidation`, `policy-semantic-impact`, `root-index-closure`,
  `source-index-closures`, and `systemic-finding-replanning`.
- The suite-dependency graph adds no reverse dependent suite. Existing required
  suites of `a1c-public-cutover` and `concurrent-plan-integration` remain part
  of focused execution but require no source change.
- Through evidence-owner suite closure, 41 policy subjects depend on at least
  one changed suite fingerprint. The union of direct semantic and evidence
  dependencies is 44 policy subjects.
- The `standards-requires`, `standards-specializes`, and combined
  `standards-dependencies` groups were reviewed for Architecture, Contracts,
  Dependencies, Planning, and Verification. No canonical module text,
  metadata, prerequisite, or specialization changes in this correction, so
  those navigation relationships and their dependent standards require no
  edit.

The 44 subjects whose local requirement identities can change are:

`core.simplicity-and-complection`,
`profile.boundary.generated-contract.applicability`,
`profile.boundary.generated-contract.semantic-closure`,
`router.generated-contract-profile-applicability`,
`topic.architecture.authority-scope-admission`,
`topic.architecture.composed-design-admission`,
`topic.architecture.immutable-authority-closure`,
`topic.contracts.declaration-and-semantic-authority`,
`topic.contracts.generated-semantic-conformance`,
`topic.contracts.schema-dialect-and-vocabulary`,
`topic.contracts.version-scope-and-invalidation`,
`topic.dependencies.implementation-versus-dependency`,
`topic.dependencies.requirement-and-ownership`, all thirteen `workflow.commit`
subjects, `workflow.planning.acceptance-claims`,
`workflow.planning.active-plan-fields`, `workflow.planning.artifact-model`,
`workflow.planning.completion`,
`workflow.planning.concurrent-integration-routing`,
`workflow.planning.concurrent-work`, `workflow.planning.current-state`,
`workflow.planning.findings`, `workflow.planning.lifecycle`,
`workflow.planning.milestones-and-slices`,
`workflow.planning.plan-admission`,
`workflow.planning.projection-completeness`, `workflow.planning.replanning`,
`workflow.planning.repository-isolation`,
`workflow.planning.systemic-finding-replan`,
`workflow.planning.written-plan-applicability`,
`workflow.verification.evidence-oracle-boundary`, and
`workflow.verification.negative-fixture-isolation`.

For every incident relationship not marked `correct` above, the disposition is
`reviewed-no-change`: the correction preserves the existing projection clauses
owned by that source policy and changes only the version-role or bounded
systemic-audit clause. Twelve of the 14 suite definitions remain byte-unchanged
and must pass focused execution. The two changed suites retain all other checks
and policy consumers while replacing only their outdated text oracle.

The remaining seven subjects are not mechanically invalidated by these shared
projection and suite changes. They still require current authority where their
own semantic revision is newer. Consequently final completion remains exact
51-subject attestation and certificate equality, not a 44-subject subset.

## Audit Result

The A1c architecture remains aligned with the new immutable-closure,
invariant, proof-lifetime, dependency, and acceptance-claim policies after the
Milestone 0 repairs and the active dependency-local coverage correction. No
new runtime Module, authority artifact, version, store, or public operation is
required.

Five authored projection/evidence corrections are required before current
attestations can be generated:

- `prompts/planning.md`;
- `prompts/implement-plan.md`;
- `templates/PLAN-TEMPLATE.md`;
- `evaluation/standards-effectiveness/suites/contract-authority-scope.toml`;
  and
- `evaluation/standards-effectiveness/suites/systemic-finding-replanning.toml`.

These paths were outside Milestone 1's previously admitted write set. The
blocked replan now proposes them explicitly; updating them remains unavailable
until that expanded boundary is admitted. They are only the authored delta,
not the acceptance closure. The standards-aligned repair also reviews all 53
incident semantic relationships, executes the 14 selected suites and their
declared requirements, regenerates the suite-input manifest, derives the exact
44-subject invalidation set, and finishes with all 51 current attestations and
certificates. It adds no policy unit, relationship, fixture family, checker,
package, or parallel authority.
