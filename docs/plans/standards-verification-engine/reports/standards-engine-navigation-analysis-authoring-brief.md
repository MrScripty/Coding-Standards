# Development Brief: Standards Engine Navigation and Analysis (Plan A1)

## Status

This brief records proposed requirements for Plan A1 of the agent-facing Standards Engine. It is a non-authorizing investigation report; its proposals become durable authority only through an accepted `plan.md` and architectural decision.

Current planning authority is the
[Standards Engine Navigation and Analysis plan](../../standards-engine-navigation-analysis/plan.md).

This brief covers navigation and read-only analysis only. Controlled authoring is a separate future product that requires its own brief after A1 proves the interface. A1 must preserve compatible identity and snapshot concepts, but it does not authorize proposal storage, mutation, application, or recovery implementation.

Existing future work remains separate:

- **Plan B:** Evidence-oracle policy and projection-check correction.
- **Plan C:** External project application and standards-upgrade baselines.

The active plan remains the sole owner of implementation admission, blockers, recovery sequencing, and the next slice.

---

# 1. Motivation

Coding Standards is a growing, selectively read knowledge system. Developers and agents are not expected to read the entire repository before making or interpreting a change.

The Standards Engine must therefore let an agent:

- Describe its work using typed facts.
- Discover relevant standards without knowing repository paths.
- Retrieve authoritative policy by canonical identity.
- Navigate declared dependencies and impact relationships.
- Identify uncertainty rather than silently guessing.
- Analyze a proposed standards change.
- Receive a bounded work queue containing questions, affected policies, and required reviews.
- Eventually create and modify standards without editing metadata tables directly.

The engine does not determine whether arbitrary prose is semantically correct. It deterministically identifies relevant authority, relationships, uncertainty, and review obligations.

---

# 2. Core Mental Model

```text
Agent or software
       │
       │ typed requests and submissions
       ▼
┌────────────────────────────────────┐
│ Standards Engine                   │
│                                    │
│ • route and retrieve               │
│ • navigate relationships           │
│ • compare standards snapshots      │
│ • prepare impact packets           │
│ • resolve questions and reviews    │
└─────────────────┬──────────────────┘
                  │
     ┌────────────┼───────────────┐
     ▼            ▼               ▼
 Standards    Generic graph    Standards
 metadata       engine         documents
```

The engine is the agent-facing interface.

Packets are immutable results produced by the engine. They provide canonical handles, required work, and valid next operations. They are not a replacement command language.

---

# 3. Delivery Boundaries

## Plan A1: Navigation and analysis

A1 provides:

- Neutral canonical metadata access.
- Routing from typed facts.
- Executable projection of Router-owned decisions without a second routing authority.
- Policy retrieval by canonical ID.
- Relationship navigation.
- Snapshot construction and comparison.
- Policy-unit identity.
- Representation, structural, and semantic change classification.
- Prior/current graph comparison.
- Three-valued applicability.
- Consumer-audit declarations and generated certificates.
- Immutable analysis packets.
- Questions, obligations, dispositions, and reading plans.
- Safe reuse of previous decisions.
- Typed Python and agent-tool interfaces.
- End-to-end route/read and prepare/resolve agent fixtures.

A1 analyzes supplied base and proposed snapshots. It does not own proposal mutations.

## Future controlled authoring

Controlled authoring is outside A1. After A1 acceptance, a new brief may investigate change sessions, proposal revisions, mutations, semantic acceptance, authorization, coherent application, verification, and recovery.

Any future authoring design must reuse A1 snapshot, identity, query, impact, applicability, and packet semantics rather than creating a second analyzer. It must use a distinct apply-eligible report type and must not return application success before post-write verification passes.

## Plan B: Evidence-oracle recovery

Plan B remains inactive. It will address:

- Limits on claims made by automated evidence.
- Raw source versus rendered representation.
- Copied explanatory prose.
- Classification of the 27 checks targeting the central evaluation README.
- The preserved M6-I71 projection regression.

## Plan C: External project baselines

Plan C remains inactive. It will add:

- Project-owned standards application baselines.
- Policy-to-project bindings.
- Project-change impact analysis.
- Standards-upgrade impact analysis.
- Reuse of project-specific semantic decisions.

Basic navigation is foundational A1 behavior, not a Plan C feature.

---

# 4. Historical Recovery Evidence and Accepted Boundary

The prior accepted revision was:

```text
da65fddd80326a3d2b548ce59294fbfcc76bfe43
```

Its tree was `5b3f262e3139dcf7346f0a5b13cdf5196942cda2`. That revision
contained this verification failure:

| Field | Value |
|---|---|
| Suite | `rust-binding-callback-task` |
| Check | `documentation-projection` |
| Failure | `ASSERT.TEXT_REQUIRED` |
| Required representation | `...checks selected task representation,` |
| Actual representation | Markdown wraps between `task` and `representation` |

The check intended to show that documentation describes the registered suite
and its responsibilities. It actually checked only byte-adjacent wording.

At the time of the original investigation, the worktree also contained
uncommitted M6-I72 changes affecting overlapping surfaces. These observations
were evidence for the then-active plan and did not themselves declare a blocker
or authorize a recovery slice.

## Accepted recovery disposition

The active verification-engine plan selected one coherent M6-I72 slice that
also owned the narrow M6-I71 representation repair. The accepted recovery
boundary is:

| Identity | Value |
|---|---|
| Commit | `13a9f48b95ed7532f480e4604d9dfa23443e8f43` |
| Git tree | `c27a1e2bbf52244c5b30eb1d21381be6e5c86d68` |
| Accepted slice | M6-I72 Rust binding executor delegation |

The accepted slice:

- Preserved the exact M6-I71 reproduction in a durable report.
- Rejoined the equivalent Markdown source representation without implementing
  Plan B's broader evidence policy.
- Migrated the M6-I72 executor-delegation checker to one declarative suite.
- Passed all 218 declarative suites, 386 verifier tests, 35 graph tests,
  focused mutation evidence, numeric lifecycle, and generated freshness.
- Recorded the accepted commit and tree in the active plan and ledger.

This satisfied the recovery prerequisite for creating Plan A1. The linked A1
plan is now `Planned`, but A1 implementation is not admitted. The plan must
first accept its architectural decision and canonical schemas, then record the
exact implementation base when implementation is explicitly started. The
historical failing revision remains recorded as failing rather than being
relabeled as green.

## Durable regression owner

The M6-I71 evidence is owned by the
[documentation-projection regression report](m6-i71-documentation-projection-regression.md).
It records the exact failing revision and tree, suite and check, required and
actual representations, reproduction command, intended and actual property,
narrow repair, and future Plan B disposition.

---

# 5. Module Architecture

```text
standards_engine
  ├── standards_metadata
  └── standards_analysis

standards_analysis
  ├── standards_metadata
  └── graph_engine

standards_verifier
  ├── standards_metadata
  └── graph_engine
```

The Standards Engine façade is the composition root.

Lower modules must not depend on the façade or form cycles.

## Implementation responsibilities

| Module | Loads, validates, projects, or implements |
|---|---|
| `standards_engine` | Composes the public typed interface and tool adapters over lower modules |
| `standards_metadata` | Loads, validates, and projects corpus membership and canonical module-owned IDs, aliases, paths, `Requires`, and `Specializes` metadata |
| `standards_analysis` | Executes Router-owned routing projections and implements applicability evaluation, impact selection, packets, obligations, and reading plans |
| `graph_engine` | Implements domain-neutral graph storage and traversal |
| `standards_verifier` | Implements deterministic suite execution and verifier diagnostics while consuming neutral metadata and graph mechanics |

Canonical standards documents and metadata remain the authority for IDs, paths, relationships, and routing decisions. Implementation responsibility in a Python module does not transfer that authority. The graph engine remains domain-neutral and does not know what “policy,” “semantic review,” or “documentation” means.

---

# 6. Neutral Metadata Module

Create:

```text
tools/standards_metadata/
```

It should provide:

- Explicit corpus membership loading.
- Canonical module discovery.
- Canonical ID resolution.
- Alias resolution.
- Canonical document-path resolution.
- `Requires` metadata loading.
- `Specializes` metadata loading.
- Neutral structural validation.
- Deterministic immutable corpus views.

It must not own:

- Policy-impact meaning.
- Applicability.
- Verifier predicates.
- Analysis packets.
- Semantic decisions.
- A duplicate module catalog.

## Known consumers

The A1 planning inventory must identify every metadata consumer, including at least:

- `standards_verifier`
- `standards_analysis`
- Repository graph-provider composition
- `tools/query_edges.py` through that provider
- Tests and generated-artifact producers

## Cutover rules

Do not retain parallel production authorities.

1. Inventory all consumers.
2. Implement the neutral metadata API.
3. Compare old and new normalized outputs.
4. Compare corpus membership, IDs, aliases, paths, `Requires`, and `Specializes`, including the existing transitive graph groups.
5. Treat unexplained differences as blocking.
6. Switch the inventoried consumers in one bounded cutover.
7. Remove the old neutral-loading implementation.
8. Keep verifier-specific diagnostics in the verifier.

Temporary comparison code is cutover evidence, not another production loader.

---

# 7. Authority Model

## Authored authority

| Authority | Owner |
|---|---|
| Policy meaning | Standards documents |
| Module identity and document path | Canonical module metadata |
| Policy-unit identity and module-relative locator | Policy-unit sidecar |
| Semantic revision | Accepted policy-unit declaration |
| Policy-impact relationships | Policy-impact declarations |
| Audit scope and attestation | Audit declarations |
| Review decisions | Authorized submissions |

## Generated artifacts

| Artifact | Purpose |
|---|---|
| Graph indexes | Efficient traversal |
| Source snapshots | Exact input identity |
| Representation and structural digests | Change detection |
| Consumer-audit certificates | Bind reviewed audit declarations to exact inputs |
| Navigation results | Relevant policy handles |
| Analysis packets | Immutable work queue |
| Reading plans | Ordered relevant material |
| Completed analysis reports | Completed analysis evidence |
| Text rendering | Human-readable projection |

Generated artifacts must not become competing policy authority.

---

# 8. Public Interface

## A1 Python interface

```python
query(
    snapshot: StandardsSnapshotHandle,
    request: QueryRequest,
) -> NavigationResult | RejectedResult

prepare(
    request: AnalysisRequest,
) -> PendingPacket | CompletedAnalysisReport | RejectedResult

resolve(
    packet: PacketHandle,
    submission: Submission,
) -> PendingPacket | CompletedAnalysisReport | RejectedResult

inspect(
    handle: InspectableHandle,
) -> InspectionResult | RejectedResult
```

`AnalysisRequest` binds supplied base and proposed snapshots. `query` binds every route, read, and related operation to one immutable standards snapshot. `NavigationResult` and every returned policy handle repeat or embed that snapshot identity.

`prepare` returns `CompletedAnalysisReport` directly when the exact initial analysis has no outstanding obligations. It must not require an empty `resolve` call. `InspectionResult` is a tagged result family for snapshot, navigation, packet, policy, report, and certificate inspection; it is not limited to provenance-only data.

---

# 9. Typed Agent Tools

Agents should use structured tool calls, not a custom command-string language.

Possible tool registrations:

```text
standards_query
standards_prepare
standards_resolve
standards_inspect
```

Example route request:

```json
{
  "snapshot": "standards-snapshot:4a091f...",
  "request": {
    "kind": "route",
    "facts": {
      "language": "rust",
      "changes_persisted_representation": true,
      "changes_public_api": false
    }
  }
}
```

Example result:

```json
{
  "kind": "navigation-result",
  "navigation_id": "navigation:7f29",
  "snapshot": "standards-snapshot:4a091f...",
  "reading_plan": [
    {
      "target": "profile.boundary.persistence",
      "reason": {
        "kind": "routing-fact",
        "fact": "changes_persisted_representation"
      }
    },
    {
      "target": "topic.contracts",
      "reason": {
        "kind": "requires",
        "source": "profile.boundary.persistence"
      }
    }
  ],
  "unresolved_questions": [],
  "next_operations": [
    {
      "operation": "query",
      "snapshot": "standards-snapshot:4a091f...",
      "request": {
        "kind": "read",
        "target": "profile.boundary.persistence"
      }
    }
  ],
  "summary": "Two standards are relevant."
}
```

The agent follows structured fields. It does not parse text headings such as `READ` or `NEXT`.

A deterministic text rendering may be provided for humans, logs, and chat interfaces, but it is not authoritative.

---

# 10. Schema Authority

Python models, JSON schemas, agent-tool definitions, and documentation must not become independently maintained interfaces.

```text
Canonical interface schema
          │
          ├── Python request/result types
          ├── JSON validation schemas
          ├── Agent-tool definitions
          ├── Text-renderer contracts
          └── Reference documentation
```

The A1 ADR must select one canonical schema representation and define how every projection is generated or mechanically validated.

Verification must fail when:

- Generated schemas are stale.
- Tool definitions differ from canonical requests.
- Result variants are missing from projections.
- Enum values differ.
- Text renderers depend on undeclared fields.
- Documentation examples fail schema validation.

---

# 11. Canonical Serialization and Identity

Content-addressed snapshot, navigation, packet, obligation, completed-report, and certificate IDs require canonical serialization.

Example:

```text
SHA-256(
  "coding-standards:packet:v1\0"
  + canonical_identity_bytes
)
```

Use distinct domain prefixes:

```text
coding-standards:snapshot:v1
coding-standards:packet:v1
coding-standards:navigation:v1
coding-standards:obligation:v1
coding-standards:analysis-report:v1
coding-standards:certificate:v1
```

## Required rules

| Concern | Rule |
|---|---|
| Object fields | Canonical schema-defined representation |
| Map keys | Deterministic lexical ordering |
| Arrays | Preserve semantically meaningful order |
| Enums | Canonical strings |
| Unicode | Defined normalization, preferably NFC for model strings |
| Booleans | Canonical JSON values |
| Integers | Canonical base-10 JSON |
| Floating point | Prohibited in identity-bearing schemas unless explicitly specified |
| Missing versus null | Distinct |
| Encoding | UTF-8 |
| Schema version | Included |
| Hashing | Domain-separated |

Raw representation digests hash source bytes without Unicode normalization. Structural digests follow the versioned parser’s normalization contract.

## Excluded from identity

- Human summary.
- Text rendering.
- Formatting.
- Generation timestamp.
- Logging identifiers.
- `next_operations`.
- Display-only ordering.
- Explanatory command examples.

Generation timestamps remain provenance only. Identical declarations and exact inputs must produce identical certificate identities.

---

# 12. Snapshot Contract

## Clean Git source

Record:

- Git tree ID as content identity.
- Commit ID as provenance.
- Declared snapshot scope.
- Submodule identities.
- Relevant contract and tool versions.

Commit ID alone is not content identity.

## Dirty or non-Git source

Generate a deterministic content manifest containing:

- Normalized relative path.
- Entry type.
- Relevant file mode.
- File content digest.
- Symlink target string.
- Submodule or nested-repository identity.
- Inclusion or exclusion status and reason.

Include:

- Relevant tracked files.
- Relevant untracked files.
- Explicit exclusions.

Git ignore status alone must not establish irrelevance.

## Symlinks

- Do not follow by default.
- Hash the target string.
- Detect targets escaping the declared root.
- Reject escaped resolution if a provider would read through the link.
- Allow an escaping link only as inert content when no provider follows it.

## Submodules

Record the parent gitlink. If content is in analysis scope:

- Bind the checked-out revision.
- Detect divergence from the gitlink.
- Detect relevant dirty or untracked content.
- Produce a nested content manifest when necessary.

## Tool versions

Record:

- Analysis contract version.
- Schema versions.
- Analyzer version.
- Metadata API version.
- Graph-engine version.
- Parser versions.
- Applicability-language version.
- Evidence-provider contract versions.

Implementation versions enter decision fingerprints only when they can change the decision’s evaluation.

## Standards integrity closure

The standards snapshot scope must be derived from the existing canonical-corpus and edge-source registries, extended to include every new authored input that can change navigation or analysis.

The integrity closure includes at least:

- Canonical corpus membership declarations.
- Canonical module metadata, including IDs, aliases, paths, `Requires`, and `Specializes`.
- Registered dependency and policy-impact edge sources.
- Policy-unit declarations and module-relative locators.
- Audit declarations and explicit exclusions.
- The canonical interface schema and its authored source.
- Router-owned declarations or fixtures used to produce executable routing.
- Applicability fact schemas and relationship applicability declarations.

Generated packets, certificates, graph indexes, tool definitions, and text renderings are not authored snapshot inputs. Their identities and freshness remain bound to the authored closure and relevant implementation contract versions.

Adding a new declaration kind to navigation or analysis requires adding its authoritative source to this closure. An unregistered declaration must not silently influence an analysis result.

---

# 13. Policy-Unit Identity

A policy unit is identified independently of its current source location.

```toml
[[policy_unit]]
id = "workflow.verification.evidence-oracle-boundary"
module = "workflow.verification"
heading_path = ["Evidence", "Oracle boundaries"]
semantic_revision = 3
```

The document path derives from canonical module metadata.

The sidecar must not duplicate:

- Document paths.
- Module aliases.
- Corpus membership.
- Module dependencies.

Verification must require every locator to resolve exactly once.

## Change dimensions

| Field | Meaning |
|---|---|
| `representation_digest` | Exact source representation |
| `structural_digest` | Canonical parsed structure |
| `semantic_revision` | Accepted reviewed meaning |

Possible classifications:

- `unchanged`
- `representation-only-candidate`
- `possibly-semantically-changed`
- `semantically-changed`
- `unresolved`

A structural match does not prove semantic equivalence for arbitrary prose.

## A1 proposal state

A1 compares accepted and externally supplied proposed snapshots but does not accept policy meaning.

For an existing policy, a proposed snapshot must retain the accepted `semantic_revision`. Proposed semantic state lives in an `AnalysisRequest.semantic_proposals` overlay, not in the accepted policy-unit sidecar.

Each overlay entry binds:

- Canonical policy ID.
- Accepted semantic revision, or `none` for an addition.
- Proposed semantic revision.
- Proposed semantic intent.
- Relevant proposed structural digest.

```text
accepted semantic revision: 3
proposed semantic revision: 4
semantic state: proposed
```

For a newly added policy:

```text
accepted semantic revision: none
proposed semantic revision: 1
semantic state: proposed
```

A proposed snapshot that directly represents an unreviewed semantic revision as accepted is invalid. The semantic overlay is part of `AnalysisRequest` and packet identity. A future controlled-authoring proposal may own the same overlay and project it into `AnalysisRequest`, but only a separately authorized future application workflow may promote a proposed revision into accepted canonical authority.

An A1 `CompletedAnalysisReport` may establish that impact analysis is complete for the supplied accepted and proposed snapshots. It does not accept a proposed semantic revision or authorize canonical application. A future authoring design must use a distinct `ApplyReadyChangeReport` after obtaining semantic, relationship, and lifecycle approvals.

## Lifecycle

- IDs are immutable and globally unique.
- Moving retains the ID and updates the locator.
- A semantic-preserving rename may retain the ID.
- Splitting creates successors and retires the original.
- Merging creates a successor and retires the predecessors.
- Retirement creates a permanent tombstone.
- Retired IDs are never reused.
- Aliases represent identity continuity only.
- Splits and merges are successor relationships, not aliases.
- Existing `STD-xxxx` migration identities do not automatically become policy-unit IDs.
- Legacy mappings require explicit review.

---

# 14. Navigation

A1 must support at least these typed query variants:

- Route from task or change facts.
- Read canonical policy content.
- Retrieve related policies.
- Inspect provenance and source resolution.

Every query requires an immutable snapshot handle. Every navigation result, policy handle, relationship handle, and derived next operation binds the same snapshot. A route result from one snapshot cannot be followed by a read against another snapshot without creating a new navigation result.

Native Python callers may use a snapshot-bound engine view as convenience syntax, but the canonical interface and agent-tool schema retain the explicit snapshot identity.

Normative task-to-module routing remains owned by the Standards Router. A1 must consume a generated or mechanically validated executable projection of that authority and the existing typed routing fixtures. It must not hardcode an independent fact-to-module decision table in Python.

Route results must apply the existing `Requires` and `Specializes` graph contracts and named traversal groups exactly as their canonical owners define them. A1 may compose those results with policy-unit scope and applicability, but it must not redefine the meaning or traversal direction of either relationship.

An agent should be able to navigate without repository paths:

```text
typed route request
       │
       ▼
canonical policy IDs
       │
       ▼
typed read request
       │
       ▼
authoritative policy content
       │
       ▼
typed related request
       │
       ▼
declared dependencies and impact relationships
```

A navigation result should include:

- Canonical targets.
- Authority classification.
- Selection reasons.
- Required dependencies.
- Unresolved routing questions.
- Typed valid next operations.
- Optional explanatory summary.

---

# 15. Graph and Policy-Impact Semantics

The generic graph stores and traverses nodes and edges. Policy meaning stays in the standards-analysis adapter.

Policy-impact declarations may:

- Reference canonical source and target IDs.
- Declare relationship kind.
- Declare source and consumer scopes.
- Declare propagation direction.
- Declare typed applicability.
- Identify evidence ownership.
- Reference audit coverage.

They must never redefine canonical IDs, aliases, paths, membership, `Requires`, or `Specializes`.

Analysis must compare the accepted and proposed graphs.

```text
Impact candidates =
  relevant edges from accepted graph
  union
  relevant edges from proposed graph
```

This prevents an accidentally deleted edge from hiding its previous consumer.

Inferred or lexical relationships may be discovery candidates. They must not become authoritative edges without review.

## Change-type impact contract

The generic graph deterministically traverses the groups selected by its caller. The standards-analysis module owns the policy-specific rules that choose seed identities, scopes, accepted and proposed relation sets, applicability evaluation, and generated obligations.

For every change, A1 first derives:

```text
seed identities = relevant accepted identities
                  union relevant proposed identities
                  union declared predecessor and successor identities

candidate relations = applicable selected groups from the accepted graph
                      union applicable selected groups from the proposed graph
```

The adapter then applies these deterministic change-type rules:

| Change type | Required seeds and obligations |
|---|---|
| Modification | Seed the stable policy ID in both snapshots. Traverse the union of accepted and proposed relevant relations. Generate one consumer-review obligation for every reached applicable consumer. Preserve unresolved applicability as an obligation. |
| Addition | Seed the proposed policy ID and its owning module. Traverse proposed relations plus the existing `Requires` and `Specializes` groups selected by their canonical contracts. Require proposed semantic revision 1, consumer-audit coverage, and dispositions for every reached consumer. |
| Removal | Seed the accepted policy ID and traverse its accepted relations even when the proposed node is absent. Generate obligations for every former consumer, unresolved reference, retirement or successor claim, and affected audit scope. |
| Move | Seed the stable ID at both accepted and proposed locations. A same-module move generates representation and projection obligations as applicable. A cross-module move also seeds both owning modules, compares their `Requires` and `Specializes` closure, and generates ownership-transfer impact-review and affected-consumer obligations. |
| Split | Seed the accepted predecessor and every proposed successor. Traverse the predecessor's accepted relations and every successor's proposed relations. Require each former consumer to have exactly one current disposition or explicit successor mapping, plus coverage for every successor and a lifecycle-impact review. |
| Merge | Seed every accepted predecessor and the proposed successor. Traverse the union of all predecessor accepted relations and successor proposed relations. Require every former consumer to have exactly one current disposition or explicit mapping to the successor, plus successor coverage and a lifecycle-impact review. |

The accepted plan and ADR must define the exact named graph groups used by each rule. A1 must use the existing generic traversal rather than reimplementing graph closure.

## Unmapped normative changes

Policy-unit coverage need not partition every explanatory sentence. It must, however, prevent changed normative content from escaping impact analysis.

Any changed normative scope not covered by exactly one valid policy-unit locator generates a mandatory `unmapped-normative-change` obligation with conservative whole-artifact review scope. If A1 cannot determine whether uncovered changed content is normative, it generates the same obligation with the normative classification retained as unresolved.

This obligation is mandatory rather than an optional conservative-selection optimization. It cannot be cleared merely because no policy-impact edge was found.

---

# 16. Applicability

A1 owns a typed, side-effect-free, three-valued applicability language. It must not reuse verifier predicates.

Initial fact types:

- Boolean.
- Enum.
- String.
- Typed set.
- Canonical identity reference.

Initial operators:

- `all`
- `any`
- `not`
- `equals`
- `in`
- `contains`
- `exists`

Results:

| Result | Meaning |
|---|---|
| `true` | Relationship applies |
| `false` | Relationship does not apply |
| `unknown` | Valid expression lacks required facts |
| Invalid | Expression or data violates the schema |

Invalid conditions reject preparation:

- Unknown operator.
- Unsupported syntax.
- Malformed value.
- Type mismatch.
- Invalid fact reference.

Missing contextual facts produce `unknown`, not rejection.

## Evaluation contract

Applicability facts have three evidence states:

```text
known(value)
known-absent
unknown
```

Omitting a required fact means `unknown`; it does not mean false or known-absent. `null` is a value only for a fact whose schema explicitly permits it.

Boolean composition uses these truth tables:

| Expression | Result |
|---|---|
| `not true` | `false` |
| `not false` | `true` |
| `not unknown` | `unknown` |
| `all` with any `false` | `false` |
| `all` with no `false` and at least one `unknown` | `unknown` |
| `all` with only `true` | `true` |
| `any` with any `true` | `true` |
| `any` with no `true` and at least one `unknown` | `unknown` |
| `any` with only `false` | `false` |

Empty `all` and `any` expressions are invalid rather than implicit identities.

`exists` evaluates as follows:

| Fact state | `exists` result |
|---|---|
| `known(value)`, including permitted `null` | `true` |
| `known-absent` | `false` |
| `unknown` | `unknown` |

Value comparison evaluates as follows:

| Operand state | `equals`, `in`, or `contains` result |
|---|---|
| All operands are known and type-compatible | Deterministic Boolean comparison |
| Required fact is known-absent | `false` |
| Any result-determining operand is `unknown` | `unknown` |
| Operand types are incompatible | Invalid expression or fact set |

`in(element, set)` and `contains(set, element)` are equivalent after canonicalization. A declared set has mathematical set semantics; duplicate submitted members are invalid rather than silently normalized.

Additional rules:

- Contradictory values for the same canonical fact are invalid.
- Fact and identity aliases resolve before evaluation.
- Alias conflict or unresolved alias is invalid.
- Equality and set membership require type-compatible canonical values.
- An unknown set or element fact produces `unknown` unless another operand already determines the enclosing `all` or `any` result.
- Evaluation order may short-circuit operationally, but the result and diagnostics must be deterministic.

## Conservative read selection

If applicability or structured scope is unresolved, analysis may select an entire artifact for review:

```text
applicability: unknown
review_scope: whole-artifact
selection_reason: structured-scope-analysis-unsupported
```

The applicability remains unknown.

Conservative review selection must never convert `unknown` to `true`.

---

# 17. Consumer-Audit Coverage

An empty edge query does not prove that an owner has no consumers.

Use:

```text
Compiled authority view
          │
          ▼
Derived CoverageAuditRequirement
          │
          ▼
Authorized CoverageAttestation
          │
          ▼
Immutable ConsumerCoverageCertificate
```

## Coverage requirement and attestation

Analysis mechanically derives a `CoverageAuditRequirement` containing:

- Exact accepted or proposed authority view.
- Covered policy-unit identity and scope.
- Accepted or proposed semantic revision and structural/content digest.
- Relationship kinds and compiled relationship-set digest.
- Audit-horizon provider, version, membership, and digest.
- Applicability-contract and fact-schema digests.
- Required evidence classes.

An authorized reviewer authors a `CoverageAttestation` containing only the
requirement handle, a `complete` conclusion, evidence, explicit exclusions,
rationale, and auditor provenance. It does not repeat snapshots, relationships,
horizon members, obligations, reports, or dispositions. If the audit finds a
missing consumer, no complete attestation or certificate is produced; the
relationship authority must be corrected and analysis repeated.

## Generated certificate

Derived fields include:

- Requirement and attestation digests.
- Exact authority view and policy-unit semantic and structural state.
- Resolved canonical identity and source location.
- Resolved audit-horizon and relationship-set digests.
- Applicability-contract and fact-schema digests.
- Schema and tool-contract versions.
- Evidence digests.

The generator rejects mismatched scope, semantic revision, structural state,
authority view, relationship set, applicability contract, fact schema, horizon,
or evidence. Certificate identity excludes generation timestamps.

A certificate makes this bounded claim:

> No additional applicable consumers were identified under the declared owner, scope, audit horizon, relationship kinds, applicability contract, and audited revision.

It does not claim coverage outside that horizon.

The audit horizon must be selected by a deterministic registered provider, not by an arbitrary caller list. It identifies the modules, policy units, edge sources, and other consumer classes capable of consuming the covered owner under the declared relationship kinds.

## Invalidation

Renew coverage when:

- The owner changes semantically.
- The resolved audit-horizon membership changes.
- A policy unit is added to or could enter the resolved audit horizon.
- A relevant relationship changes.
- A changed unit within or potentially entering the horizon may introduce a new dependency.
- Applicability semantics change.
- A locator becomes unresolved.
- Required evidence becomes unavailable.

Without valid coverage, return an unaudited or unresolved result—not an empty successful impact set.

Coverage certificates certify consumer-discovery completeness and may be
reused while their dependencies remain equal. They never contain or depend on
change-specific dispositions. `CompletedAnalysisReport` references the exact
certificates used and separately owns dispositions. Completion requires exact
coverage-subject/certificate equality and exact reached-obligation/disposition
equality.

A global corpus-membership change triggers horizon recomputation, not automatic certificate invalidation. If the registered horizon provider proves that the resolved horizon and every other certificate dependency are unchanged, the certificate may remain valid. A provider or classification change that could alter horizon membership requires renewal.

---

# 18. Analysis Packets

A packet is an immutable typed navigation and work-queue result.

It contains:

- Packet identity.
- Base and proposed snapshots.
- Changed policy units.
- Prior/current graph traces.
- Deterministic findings.
- Questions.
- Typed obligations.
- Required dispositions.
- Reading plan.
- Coverage state.
- Decision-reuse provenance.
- Derived next operations.
- Optional summary.

The default text rendering should remain compact. Technical details are available through `inspect`.

## Obligation contract

Every obligation has:

- Stable ID.
- Typed kind.
- Reason.
- Target canonical ID.
- Relevant scope.
- Permitted submissions.
- Current state.
- Valid next operations.

Example kinds:

- `applicability-question`
- `consumer-review`
- `coverage-renewal`
- `semantic-impact-review`
- `relationship-impact-review`
- `lifecycle-impact-review`

Obligation identity should remain stable across packet revisions when its defining dependencies remain unchanged.

## Dispositions

Consumer-review outcomes are:

- `updated`
- `reviewed-no-change`
- `not-applicable`
- `blocked`

Evidence requirements:

| Result | Required evidence |
|---|---|
| `updated` | Actual relevant proposed change and explanation |
| `reviewed-no-change` | Reviewed scope, revision, and rationale |
| `not-applicable` | Resolved applicability facts and reason |
| `blocked` | Blocking condition and missing authority or evidence |

An `updated` disposition must correspond to an actual proposed change in the affected scope.

## Exact CompletedAnalysisReport invariant

Let:

```text
R = IDs of all consumer-review obligations reached by the final
    accepted/proposed graph union, scope rules, and applicability result

D = obligation IDs named by valid current consumer dispositions
```

A report may be complete only when:

```text
R == D
```

The equality is set equality, and the implementation must additionally prove:

- Every reached consumer-review obligation has exactly one disposition.
- No disposition names an obligation outside the final reached set.
- No duplicate disposition exists for an obligation.
- Every disposition is bound to the current packet and dependency fingerprint.
- No stale disposition was imported.
- Every required non-consumer obligation is resolved under its typed contract.
- No applicability result required for acceptance remains `unknown`.
- No required question remains unanswered.
- No current disposition is `blocked`.
- Required evidence and authorization are valid.
- Required audit coverage is current.

`complete` is a derived state computed from these invariants. It must not be an independently authored Boolean or an unchecked assertion in a report.

For A1, completeness means that the analysis obligations required by the request are resolved. It does not promote proposed semantic state. A future `ApplyReadyChangeReport` may reference a `CompletedAnalysisReport`, but it must remain a distinct type with separately authorized semantic, relationship, and lifecycle acceptance.

---

# 19. Reading Plans

A reading plan is:

> Bounded and complete under the supplied request, declared relationships, resolved applicability facts, and valid audit certificates.

It is not claimed to be globally minimal or omniscient.

Each entry contains:

- Canonical policy or module ID.
- Structured or whole-artifact scope.
- Authority classification.
- Selection reason.
- Selecting fact, edge, or question.
- Deterministic order.
- Conditional or unresolved state.

Ordering:

1. Foundational authority.
2. Required dependencies in topological order.
3. Directly selected policies.
4. Impact consumers.
5. Contextual material.
6. Evidence scopes.

Ties use canonical ID, document identity, and document scope order.

---

# 20. Packet Staleness and Decision Reuse

Every packet binds exact inputs.

If a bound input changes, the packet is stale and cannot be accepted.

A newly prepared packet may import a previous decision only when its narrower dependency fingerprint matches.

## Decision fingerprint

Include as applicable:

- Decision kind and schema version.
- Policy-unit ID.
- Semantic revision.
- Structural digest.
- Representation digest when relevant.
- Resolved module and locator.
- Project-local subject ID when applicable in future plans.
- Exact applicability facts used.
- Relevant relationships and conditions.
- Propagation semantics.
- Audit declaration and certificate.
- Exceptions and revisions.
- Evidence digest.
- Evidence-provider contract version.
- Applicability version.
- Analysis contract version.
- Questions on which the decision depends.

If equality cannot be proven, reopen the decision.

---

# 21. Result Semantics

`RejectedResult` represents expected domain outcomes:

- Invalid input.
- Stale snapshot.
- Unknown canonical ID.
- Unresolved identity.
- Unavailable authority.
- Invalid applicability.
- Ambiguous structural scope.
- Denied authorization.
- Incomplete report.

Each rejection contains:

- Stable code.
- Target or handle.
- Safe explanation.
- Structured details.
- Recoverable next operations where available.

Programming defects remain exceptions:

- Impossible internal state.
- Violated engine invariant.
- Unhandled result variant.
- Nondeterministic serialization.
- Internal corruption.

Adapters may convert exceptions into transport-level internal errors, but must not misrepresent them as expected domain rejections.

---

# 22. Derived Guidance and Text Rendering

`next_operations` derives from the accepted state machine.

It:

- Helps agents choose the next tool call.
- Does not grant authority.
- Does not bypass validation.
- Must agree with actual engine behavior.
- Is excluded from identity.

`summary` is explanatory only. It cannot affect:

- Identity.
- Acceptance.
- Authorization.
- Applicability.
- Decision reuse.
- Audit coverage.

The text renderer:

- Consumes typed results only.
- Contains no independent business logic.
- Is optional for agent operation.
- Must not become a command-language authority.

---

# 23. Authorization

Tool availability does not grant authority.

Authorization context must come from a trusted adapter or execution environment, not self-asserted request fields.

Capabilities should include:

| Capability | Permission |
|---|---|
| `standards.read` | Route, retrieve, relate, and inspect |
| `standards.analyze` | Prepare packets |
| `standards.review.consumer` | Submit consumer dispositions |
| `standards.review.impact` | Submit non-authorizing semantic, relationship, and lifecycle impact classifications |
| `standards.review.audit` | Submit audit declarations attesting completed report coverage |

Read, analysis, consumer-review, impact-review, and audit-review capabilities are independent. A caller that can prepare a packet does not thereby gain authority to submit a disposition, impact classification, or audit declaration.

Future authoring capabilities—including semantic review, relationship review, lifecycle review, proposal mutation, and canonical application—must be designed and authorized in the separate future authoring brief. That brief must require a distinct `ApplyReadyChangeReport` and must complete post-write verification before returning `AppliedResult`; verification failure must produce a non-success outcome with an explicit rollback or recovery contract.

---

# 24. Required A1 Agent Evidence

A1 must include a real typed tool adapter exercised end to end:

```text
Structured route request
        │
        ▼
Standards Engine
        │
        ▼
Structured NavigationResult
        │
        ▼
Agent follows canonical ID
        │
        ▼
Structured read request
        │
        ▼
Authoritative policy content
```

The fixture must prove:

- The caller supplies no repository path.
- The route request binds an immutable standards snapshot.
- Routing returns canonical policy IDs.
- The agent follows an ID using another typed request bound to the same snapshot.
- A follow-up read against a different snapshot cannot continue the original navigation.
- The correct authoritative content is returned.
- Structured fields drive the interaction.
- Text rendering is optional.
- Invalid input is rejected structurally.
- Agent-tool definitions match the canonical schema.

Schemas alone are not sufficient evidence of usability.

## Full analysis workflow fixture

A1 must also exercise its complete new agent-facing workflow through the typed tool adapter:

```text
Structured AnalysisRequest with base and proposed snapshots
        │
        ▼
prepare
        │
        ▼
PendingPacket with changed policy, impact trace, and obligations
        │
        ▼
Agent retrieves every referenced canonical policy
        │
        ▼
Agent submits typed answers and dispositions
        │
        ▼
resolve returns another PendingPacket when obligations expand
        │
        ▼
Agent resolves every final obligation
        │
        ▼
CompletedAnalysisReport satisfying the exact completion invariant
```

This acceptance suite must use representative proposed snapshots for at least:

1. Modification of an existing policy with an existing consumer.
2. Addition of a new policy with proposed semantic revision 1 and required coverage.
3. Removal of a policy whose accepted relations still reach consumers.

For each case, the fixture must prove that:

- The seed rule selects the expected accepted and proposed identities.
- The expected named graph groups are traversed by the generic graph engine.
- The packet exposes canonical handles rather than repository paths.
- The agent retrieves referenced policy through `query`.
- Every reached consumer produces an obligation.
- Iterative resolution preserves or supersedes obligation identities correctly.
- A missing, duplicate, extra, stale, unresolved, or blocked disposition prevents completion.
- `CompletedAnalysisReport` is returned only when reached obligation IDs equal disposition obligation IDs and every other required obligation is resolved.

The modification, addition, and removal cases form the initial A1 pilot. Move, split, and merge remain required behavioral fixtures before their analysis contracts are claimed complete.

---

# 25. Required A1 Behavioral Evidence

A1 fixtures must also cover:

- Clean Git snapshot identity.
- Dirty-tree manifest identity.
- Relevant untracked files.
- Explicit exclusions.
- File modes.
- Symlink target and escape handling.
- Submodule state.
- Integrity closure for policy-unit, audit, schema, routing, and edge declarations.
- `Requires` and `Specializes` discovery, cutover equivalence, and transitive graph groups.
- Router-owned decisions projected into `query(route)` without a second hardcoded authority.
- Representation-only Markdown changes.
- Structural changes.
- Proposed semantic changes.
- Proposed semantic overlay inclusion in packet identity.
- Rejection when a proposed snapshot directly advances accepted `semantic_revision`.
- Proposed semantic revision 1 for a newly added policy.
- Policy movement without identity loss.
- Split, merge, retirement, successor, and alias validation.
- Deterministic modification, addition, removal, move, split, and merge seed rules.
- Prior graph edge deleted in the proposal.
- Mandatory whole-artifact obligation for uncovered or unresolved normative changes.
- Unknown applicability.
- Invalid applicability.
- Complete `not`, `all`, `any`, `exists`, missing, null, contradiction, set-membership, and alias-resolution semantics.
- Conservative whole-artifact read selection.
- Unsupported structured scope.
- Unresolved policy identity.
- Valid and invalid audit coverage.
- Audit-review authorization independent from analysis and consumer-review authorization.
- Global corpus changes that leave a bounded audit horizon unchanged.
- Audit-horizon changes that require certificate renewal.
- Certificate invalidation after horizon or relevant edge changes.
- Deterministic certificate identity without timestamps.
- Packet staleness.
- Valid and invalid decision reuse.
- Stable obligation identity.
- Exact reached-obligation/disposition set equality.
- Rejection of missing, duplicate, extra, stale, unresolved, and blocked dispositions.
- Schema drift.
- Deterministic serialization.
- `next_operations` agreement with state-machine validation.
- Expected rejection versus programming exception behavior.
- Direct `CompletedAnalysisReport` return when preparation finds no obligations.
- Tagged inspection results for every A1 inspectable handle.

---

# 26. Recommended A1 Planning Decomposition

The active A1 plan owns the binding milestones, blockers, gates, and exactly one next slice. The following is a recommended dependency order for that plan, not independent implementation authority:

The clean recovery boundary and creation of A1 in `Planned` are now complete.
The linked plan owns the remaining sequence and may refine it only through its
planning and re-planning contracts.

1. Establish the clean, green accepted boundary.
2. Create A1 in `Planned`.
3. Produce the ADR and canonical schemas.
4. Accept the ADR and schemas.
5. Explicitly admit implementation.
6. Inventory canonical metadata consumers.
7. Define the standards integrity closure.
8. Implement and validate `standards_metadata`, including `Requires` and `Specializes`.
9. Perform the single-authority metadata cutover.
10. Add policy-unit identity, proposal-state, and lifecycle validation.
11. Implement snapshot construction and canonical serialization.
12. Implement navigation by canonical ID.
13. Project Router authority into typed routing and structured reading results.
14. Implement prior/current graph impact analysis and deterministic change-type rules.
15. Implement typed applicability and mandatory unmapped-normative-change obligations.
16. Implement audit declarations and generated certificates.
17. Implement packets, exact completion invariants, reading plans, and reuse.
18. Implement the typed agent adapter.
19. Implement deterministic text projection.
20. Run route/read and full prepare/resolve/CompletedAnalysisReport agent fixtures.
21. Pilot modification, addition, and removal through the complete interface.
22. Run focused and broad behavioral verification.
23. Record the exact accepted A1 result.

---

# 27. Non-Goals

This work does not attempt to:

- Build a GUI.
- Create a custom command language.
- Require agents to parse formatted prose.
- Automatically understand arbitrary policy meaning.
- Infer authoritative edges from lexical similarity.
- Let agents edit graph tables directly.
- Let agents write canonical files before application.
- Replace standards documents with metadata.
- Duplicate canonical paths or module identity.
- Treat an unaudited empty graph result as complete.
- Convert unknown applicability into true or false.
- Permit unsupported scoped writes.
- Add external project baselines during A1.
- Activate the broad evidence-oracle recovery during A1.
- Implement controlled authoring, proposal mutation, canonical application, or recovery during A1.

---

# 28. Desired Outcome

After A1, an agent can:

```text
describe its task
    → receive canonical policy IDs
    → retrieve authoritative policy
    → navigate relationships
    → analyze supplied standards changes
    → answer bounded questions
    → review affected policies
    → produce a complete impact report
```

The A1 result is one agent-facing Standards Engine interface, one canonical metadata projection, a neutral graph implementation, and deterministic snapshot-bound navigation and impact analysis. Evidence from that accepted interface will determine whether and how a separate controlled-authoring module is justified.
