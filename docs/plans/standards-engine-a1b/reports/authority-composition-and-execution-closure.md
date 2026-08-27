# A1b Authority Composition And Execution Closure

**Status:** Proposed planning authority

**Replacement base:** commit
`396144ad9a75c948484d1e564fab73c857bd6f4d`

## Trigger

Candidate C5 `4f69f9940b806ca602f44dab7aa00c1df4db8abd`, tree
`88f963e33240415e891182a7e3891db4386e87f3`, is rejected. Its
structural closure corrected C4's copied version bags, but the stored snapshot
still included non-material Git lineage, AnalysisRoot still included complete
base/proposed views, Authority and Contracts had an unnecessary dependency,
and the required role/object catalog remained unspecified. A single aggregate
Engine profile would also make operation requirements ambient or invalidate
unrelated operation families.

The authority-scope, immutable-closure, and version-scope standards at
replacement base `396144ad` make the systemic correction mandatory. This
report replaces C5's lineage, complete-view analysis, Authority/Contracts
dependency, and aggregate-profile decisions. It does not admit
implementation.

## Canonical Terms

- **ContentSnapshot:** immutable canonical captured entries and bytes, scope,
  exclusions, nested content, and its payload contract. Git commit and source
  tree OIDs are capture locators only. It owns no interpretation or lineage.
- **SemanticAuthorityObject:** one immutable, owner-validated compatibility
  promise or compiled semantic view. Creating one requires a coherent owner,
  lifecycle, change reason, and deletion-test benefit. A shared file, build,
  generator, or release is insufficient.
- **StandardsAuthorityView:** a content-addressed composition manifest selecting
  one ContentSnapshot and the exact SemanticAuthorityObjects available for
  standards operations. It owns selection and cross-reference coherence only.
- **AuthorityBoundValue:** an internal value paired with the direct authority
  object references actually consumed to produce it. Domain Modules return this
  form to the composing kernel; callers never construct it.
- **ExecutionClosure:** a generated immutable record containing the exact
  transitive authority-object closure used by one operation family. It owns no
  policy, parsing, routing, graph, analysis, authorization, provider, or
  projection semantics.
- **OperationAuthorityContract:** one immutable Engine-owned semantic object
  for exactly one of route, read, related, or analysis. It owns that family's
  required roles and cross-role coherence rules.

`StandardsAuthorityView` is the public composition input.
`ExecutionClosure` is the narrow generated dependency evidence bound by a
semantic result. They are deliberately different identities.

## Authority Direction

```text
ContentSnapshot
      +
owner-local SemanticAuthorityObjects
      |
      v
StandardsAuthorityView
      |
      +--> MetadataView / RoutingView / GraphView / ImpactView / CoverageView
      |         each returned as AuthorityBoundValue
      |
      +--> query family
      |       -> generated Route/Read/Related ExecutionClosure
      |       -> NavigationResult
      |
      `--> base/proposed analysis composition
              + transition-only provider/authorization authorities
              -> generated AnalysisExecutionClosure
              -> immutable AnalysisState
```

All arrows point from a derived value to immutable upstream authority.
Presentation projections, timestamps, storage locations, process caches,
mutable heads, Git locators, complete input views, and lineage do not enter a
derived semantic identity.

## Authority-Scope Matrix

| Object or Module | Owned responsibility | Referenced authority | Lifecycle and change reason | Explicit exclusions | Deletion test |
| --- | --- | --- | --- | --- | --- |
| ContentSnapshot / `standards_authority` capture | Exact bounded source-neutral selected content and capture consistency | Payload contract and nested ContentSnapshots | Changes only when selected entries, bytes, scope, exclusion, or nesting changes | Git/Adapter locators and observations, metadata, parsers, routing, graphs, policy impact, coverage, public wire shape | Deleting it recreates byte capture, race detection, and immutable content reconstruction in every domain |
| Owner-local SemanticAuthorityObject | One Module's executable semantic compatibility promise or compiled semantic view | Only the typed upstream objects used by that Module | Changes when that one promise or compiled meaning changes | Unrelated Module contracts, releases, generators, wire versions | Deleting it recreates interpretation, validation, and compatibility logic across consumers |
| StandardsAuthorityView / `standards_engine` composition | Operation-contract and semantic-authority selection plus content coherence | One ContentSnapshot, exactly one contract per operation, and typed SemanticAuthorityObject references | Changes when selected authority changes | Copied semantic payloads, ambient role profile, providers, authorization decisions, executable behavior | Deleting it makes every caller select and reconcile the same authority set |
| OperationAuthorityContract / `standards_engine` | One operation family's exact required role-kind pairs and cross-role coherence-rule IDs | No upstream object | Changes only when that operation family's semantic requirements change | Other operation families and public wire representation | Deleting it makes role requirements ambient or duplicates them in composition and replay |
| AuthorityBoundValue / owning domain Module | Semantic value plus direct dependencies consumed by its construction | Exact direct authority references | Ephemeral implementation value; no independent public lifecycle | Manually authored dependency lists | Deleting it makes dependency capture optional and recreates shadow closure bookkeeping |
| ExecutionClosure / composing kernel | Canonical transitive dependency set for one operation family | Roots reported by AuthorityBoundValues and their stored DAG dependencies | Changes only when a material execution dependency changes | Semantic payloads, result projection versions, storage formats, timestamps | Deleting it forces every result and replay path to rediscover or copy dependency closure |
| NavigationResult / `standards_engine` | Normalized query meaning and semantic result | Exact query-family ExecutionClosure | Changes when request meaning, semantic output, or material query dependency changes | Complete StandardsAuthorityView and public projection version | Deleting it recreates query result identity and inspection in each adapter |
| AnalysisState / `standards_analysis` | Immutable material change context plus every dependency-valid accepted decision | Exact transition-closed AnalysisExecutionClosure and materialized child decisions | Functional transitions create independent successor values | Complete base/proposed views, mutable session, latest head, packet/report identity, lineage, derived presentation | Deleting it recreates decision normalization and replay state in the facade |
| AuthorityObjectRepository / `standards_authority` | Envelope integrity, create-only persistence, direct lookup, dependency existence/kind, and acyclic storage | Owner-provided typed object and identity | Storage-format lifecycle only | Domain decoding, semantic identity selection, policy coherence, execution | Deleting it recreates persistence, lookup, integrity, and publication in every owner |
| Public contract projection / `standards_contracts` and facade | Serialized request/result/inspection/handle shapes and exhaustive adaptation | Domain result plus selected projection contract | Wire compatibility lifecycle | Domain identity, execution closure, policy meaning | Deleting it recreates schema traversal and public adaptation in every operation |
| Provider and authorization adapters | Trusted claims and authorization decisions over declared immutable inputs | Exact transition request and immutable external-input authority | Independent transition-time lifecycle | Global StandardsAuthorityView membership and caller-minted authority | Deleting them recreates trust adaptation and evidence validation in analysis |

The exact codec inventory is owned by
[authority-object contracts](authority-object-contracts.md). The role and
operation tables below are the remaining admission inventory. They are review
evidence, not a runtime manifest. Runtime authority comes from owner codec
sets, stored operation-contract records and view selections,
AuthorityBoundValues, and stored object references.

## Derived Role Inventory

Role identity is permanent and never repurposed. This table is the union of the
four exact operation-contract records below, not a separately implemented or
stored profile. Owner is derived from the injected codec sets. The public
schema owns only the `CanonicalId` representation.

| Role ID | Object kind | Selection |
| --- | --- | --- |
| `operation.route` | `operation-authority-contract` | mechanically derived closure-root role for the view's route contract |
| `operation.read` | `operation-authority-contract` | mechanically derived closure-root role for the view's read contract |
| `operation.related` | `operation-authority-contract` | mechanically derived closure-root role for the view's related contract |
| `operation.analysis` | `operation-authority-contract` | mechanically derived closure-root role for the equal analysis contract selected by both views |
| `standards.metadata` | `canonical-standards-corpus` | exactly one corpus coherent with view content |
| `standards.routing` | `routing-projection` | exactly one projection coherent with metadata and view content |
| `standards.graph` | `standards-graph` | exactly one graph coherent with metadata and policy impact |
| `standards.policy-impact` | `compiled-policy-impact` | exactly one compiled set coherent with metadata and view content |
| `standards.coverage` | `coverage-horizon` | exactly one horizon coherent with metadata, graph, policy impact, and view content |

Provider and authorization views are transition roots, not
StandardsAuthorityView roles. Adding, removing, renaming, or repurposing a role
is a re-plan trigger.

## Operation Contracts

Each row is one separately stored `operation-authority-contract.v1` object and
one independently invalidating semantic promise. Its own role is always a root
of that operation's closure.

| Contract ID | Operation | Required role-kind pairs | Coherence-rule IDs |
| --- | --- | --- | --- |
| `operation-contract.route.v1` | route | `standards.metadata` -> `canonical-standards-corpus`; `standards.routing` -> `routing-projection` | `metadata.content`, `routing.metadata-content` |
| `operation-contract.read.v1` | read | `standards.metadata` -> `canonical-standards-corpus` | `metadata.content` |
| `operation-contract.related.v1` | related | `standards.metadata` -> `canonical-standards-corpus`; `standards.graph` -> `standards-graph`; `standards.policy-impact` -> `compiled-policy-impact` | `metadata.content`, `policy-impact.metadata-content`, `graph.metadata-policy-impact` |
| `operation-contract.analysis.v1` | analysis | On accepted and proposed sides: `standards.metadata` -> `canonical-standards-corpus`; `standards.routing` -> `routing-projection`; `standards.graph` -> `standards-graph`; `standards.policy-impact` -> `compiled-policy-impact`; `standards.coverage` -> `coverage-horizon` | `metadata.content`, `routing.metadata-content`, `policy-impact.metadata-content`, `graph.metadata-policy-impact`, `coverage.metadata-graph-policy-impact-content`; both views select this same contract, which is one `transition` root |

There is no aggregate operation-profile identity or version. A route-contract
change cannot invalidate read, related, or analysis results unless one of their
own material authority objects also changes.

## Structural Closure Algorithm

1. Resolve the supplied StandardsAuthorityView directly and verify its content
   and selected authority references.
2. Resolve the selected operation contract from the view's exact
   operation-contract selection and validate only its required role-kind pairs
   and cross-reference coherence. Analysis requires both views to select the
   same analysis contract and roots it once on the `transition` side. Missing
   required authority is `unavailable`; a contradictory selection is
   `invalid`; a recognized but unsupported semantic contract is `unsupported`.
3. Invoke each owning domain Module. Every compiled or interpreted value is an
   AuthorityBoundValue whose direct dependencies are produced by that same
   construction path.
4. Compose the result from those values. The composing kernel unions their
   direct references and traverses the immutable object DAG to obtain the exact
   transitive dependency set.
5. Canonicalize roots by typed `(side, role, object_kind, semantic_id)` and
   dependencies by `(object_kind, semantic_id)`. Reject a cycle, missing
   dependency, kind contradiction, role contradiction, or
   same-key/different-value conflict, and publish the ExecutionClosure.
6. Construct the semantic result identity from the normalized semantic request,
   semantic result, and ExecutionClosure handle. The complete
   StandardsAuthorityView handle and public result-projection version are
   excluded.

No parallel version record, operation dependency list, or ambient kernel
configuration may complete the closure. The operation-dependency matrix used
for review is generated evidence from executable composition and mutation
tests, not accepted runtime authority.

## Version And Identity Scope

| Concern | Owner and identity effect |
| --- | --- |
| Selected-content meaning | `content-snapshot.v1` payload contract owned by `standards_authority`; selected content, scope, exclusions, or nesting affect ContentSnapshot identity while Git/Adapter locators and observations do not |
| Domain semantic compatibility | Exact owner-local SemanticAuthorityObject; affects only closures that transitively use it |
| Request meaning | Operation-family semantic contract; affects that operation's closure or normalized request identity |
| Public result representation | Result-family wire contract; affects serialized compatibility but not semantic result identity |
| Public handle representation | Handle wire contract; affects decoding support but not the represented semantic object's identity |
| Storage envelope | Repository format contract; affects storage decoding and migration, not domain semantic identity |
| Identity algorithm | Scoped to the owning identity domain; it is not a shared release or umbrella version |
| Implementation release | Never an identity input unless it advances an owned semantic compatibility promise |

Semantic IDs are computed from owner-defined material identity records, not by
hashing the complete storage envelope. The envelope carries and verifies the
semantic ID, object kind, storage format, direct dependencies, and payload. Its
format version and the public wire representation are excluded from the
semantic identity record.

There are no `SnapshotVersions`, `NavigationVersions`,
`AnalysisVersions`, generic `VersionMap`, or implementation-version bags.

## Analysis And Trust

Provider and authorization authorities do not belong to any
StandardsAuthorityView. The trusted facade Adapter supplies them explicitly to
analysis preparation or transition execution, outside caller-authored payloads.

A deterministic provider result is one of:

- a typed claim over declared immutable inputs;
- deterministic no-observation; or
- unavailable execution authority.

The first two are validated and materialized with the exact provider authority
reference in the AnalysisExecutionClosure. Unavailability publishes no
successor state. Accepted observations, dispositions, and attestations retain
the evidence and authorization records that justified them. Dormant-valid
decisions remain in AnalysisState; dependency-invalid decisions are removed
during normalization.

Inspecting or projecting an existing AnalysisState uses its persisted semantic
objects, decisions, and transition-closed ExecutionClosure. The closure binds
the role- and side-qualified static authority needed by the current projection
and every advertised valid next transition, including dormant conditional
applicability. It does not invoke live providers or request fresh
authorization. Creating a successor may require new trusted transition-time
authority; accepted provider and authorization views enter that successor.

## Repository Interface

`standards_authority` exposes one small internal Interface:

```python
content = capture(source_adapter, capture_request)
handle = put(domain_object)
domain_object = get(handle)
```

`put` receives an object already validated by its owning Module and verifies
the closed envelope, owner-issued semantic identity, direct dependency
existence/kind, and acyclic DAG. Explicitly injected owner codec sets select the
decoder and validator. The repository never interprets a generic
semantic payload or uses the public JSON Schema as domain authority.

The physical repository remains one create-only object store. Object ownership
does not imply one package, directory, or store per semantic authority.

## Public Interface

```python
query(view, request)
prepare(request)
resolve(analysis_handle, submission)
inspect(handle)
```

Bootstrap is trusted composition and returns a StandardsAuthorityViewHandle.
ContentSnapshotHandle remains inspectable but is not sufficient for query or
analysis. AnalysisRequest contains its base/proposed views and optional prior
analysis handle. Pending and complete projections omit those complete views
and expose the analysis handle, narrow context, and exact
ExecutionClosureHandle. Callers never supply subordinate semantic-authority handles, operation closures,
provider objects, authorization objects, or version maps.

## Required Mutation And Reconstruction Evidence

The operation-dependency evidence must cover every selected authority role:

| Mutation | Required identity result |
| --- | --- |
| Selected entries/bytes, scope, exclusion, or nesting change | ContentSnapshot and every material dependent closure change |
| Git commit or source tree locator changes while the canonical captured record is equal | ContentSnapshot, views, closures, and results remain identical |
| Routing authority changes | Route closure/result change; unrelated read and analysis identities remain stable |
| Metadata or parser meaning changes | Metadata view and every actual dependent closure change; ContentSnapshot remains stable |
| Graph or policy-impact meaning changes | Related/analysis dependents change; unrelated route/read identities remain stable |
| Coverage authority changes | Coverage and affected analysis identities change; navigation remains stable |
| Provider or authorization authority changes | Only affected analysis transition/state changes |
| Authority unused by an operation changes | That operation closure and result remain byte-identical |
| Complete accepted/proposed view gains authority unused by current projection and every advertised successor | Analysis context, closure, state, and result remain identical |
| One operation contract changes | Only that operation family's closure and results change unless another family independently consumes the same changed semantic authority |
| Storage envelope or public result projection changes without semantic change | Semantic object, closure, and result IDs remain stable |

Additional required evidence:

- every public handle resolves directly in a fresh process after repository
  source, process caches, live providers, and authorization services are
  removed;
- existing analysis projection succeeds without transition-time authorities,
  while a new transition requiring unavailable authority publishes nothing;
- adding a new executable dependency without an AuthorityBoundValue reference
  fails construction or a mutation-closure test;
- adding or changing a codec, role, object kind, payload contract, identity
  domain, allowed dependency, or operation-required role outside the exact
  inventories fails admission;
- generated request, result, handle, nested reference, default, constraint, and
  result variant agree with the canonical public schema through independent
  semantic conformance tests;
- exact registered consumers, relationship natural keys, coverage subjects,
  and dispositions are reconciled before authority freeze; and
- no old store, owner map, scan, version bag, ambient completion path, or
  compatibility reader remains reachable after the atomic cutover.

## Re-Plan Triggers

Re-plan if:

- a StandardsAuthorityView must copy semantic payloads or execute domain logic;
- an ExecutionClosure cannot be derived from the same dependencies used by
  execution;
- an owner-local authority lacks a coherent lifecycle, change reason, or
  deletion-test benefit;
- cold inspection of an existing result requires live provider,
  authorization, source, cache, or configuration authority;
- a public result must bind the complete StandardsAuthorityView rather than its
  material closure;
- an analysis root or result needs complete base/proposed views or Git
  commit/tree lineage;
- operation-required roles cannot be owned by one separately invalidating
  operation-authority contract;
- storage envelope or wire representation must enter domain semantic identity;
  or
- a new public operation, compatibility layer, A2 behavior, or mutable head is
  required.
