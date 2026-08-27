# A1b Authority Composition And Execution Closure

**Status:** Proposed planning authority

**Replacement base:** commit
`396144ad9a75c948484d1e564fab73c857bd6f4d`

## Trigger

Candidate C4 `b92ed7828982723d0118294ea1a09f30001ad25e`, tree
`125b53038737628af82271a2eee6ec29aa8b6bf6`, is rejected. Its
object-specific version records corrected C3's ambient reconstruction defect,
but they still copied independently owned compatibility promises into snapshot,
navigation, analysis, and child records. Query also accepted only a snapshot
while routing semantics were required to reproduce the result. Adding another
field would repair one omission while preserving the omission class.

The later authority-scope and version-scope standards at replacement base
`396144ad` make the systemic correction mandatory. This report replaces C4's
version-record and snapshot-as-semantic-root decisions. It does not admit
implementation.

## Canonical Terms

- **ContentSnapshot:** immutable captured bytes, normalized manifest, scope,
  exclusions, nested content, and the capture contract that determines those
  facts. It owns no interpretation of the captured content.
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
mutable heads, and lineage do not enter semantic identity.

## Authority-Scope Matrix

| Object or Module | Owned responsibility | Referenced authority | Lifecycle and change reason | Explicit exclusions | Deletion test |
| --- | --- | --- | --- | --- | --- |
| ContentSnapshot / `standards_authority` capture | Exact bounded content observation and capture consistency | Capture-contract semantic identity and nested ContentSnapshots | Changes only when captured content, scope, exclusion, nesting, or capture meaning changes | Metadata, parsers, routing, graphs, policy impact, coverage, public wire shape | Deleting it recreates byte capture, race detection, and immutable content reconstruction in every domain |
| Owner-local SemanticAuthorityObject | One Module's executable semantic compatibility promise or compiled semantic view | Only the typed upstream objects used by that Module | Changes when that one promise or compiled meaning changes | Unrelated Module contracts, releases, generators, wire versions | Deleting it recreates interpretation, validation, and compatibility logic across consumers |
| StandardsAuthorityView / `standards_engine` composition | Authority selection, required-role closure, and cross-reference coherence | One ContentSnapshot plus typed SemanticAuthorityObject references | Changes when selected authority changes | Copied semantic payloads, versions, providers, authorization decisions, executable behavior | Deleting it makes every caller select and reconcile the same authority set |
| AuthorityBoundValue / owning domain Module | Semantic value plus direct dependencies consumed by its construction | Exact direct authority references | Ephemeral implementation value; no independent public lifecycle | Manually authored dependency lists | Deleting it makes dependency capture optional and recreates shadow closure bookkeeping |
| ExecutionClosure / composing kernel | Canonical transitive dependency set for one operation family | Roots reported by AuthorityBoundValues and their stored DAG dependencies | Changes only when a material execution dependency changes | Semantic payloads, result projection versions, storage formats, timestamps | Deleting it forces every result and replay path to rediscover or copy dependency closure |
| NavigationResult / `standards_engine` | Normalized query meaning and semantic result | Exact query-family ExecutionClosure | Changes when request meaning, semantic output, or material query dependency changes | Complete StandardsAuthorityView and public projection version | Deleting it recreates query result identity and inspection in each adapter |
| AnalysisState / `standards_analysis` | Immutable requested change plus every dependency-valid accepted decision | Base/proposed views, exact AnalysisExecutionClosure, and materialized child decisions | Functional transitions create independent successor values | Mutable session, latest head, packet/report identity, derived presentation | Deleting it recreates decision normalization and replay state in the facade |
| AuthorityObjectRepository / `standards_authority` | Envelope integrity, create-only persistence, direct lookup, dependency existence/kind, and acyclic storage | Owner-provided typed object and identity | Storage-format lifecycle only | Domain decoding, semantic identity selection, policy coherence, execution | Deleting it recreates persistence, lookup, integrity, and publication in every owner |
| Public contract projection / `standards_contracts` and facade | Serialized request/result/inspection/handle shapes and exhaustive adaptation | Domain result plus selected projection contract | Wire compatibility lifecycle | Domain identity, execution closure, policy meaning | Deleting it recreates schema traversal and public adaptation in every operation |
| Provider and authorization adapters | Trusted claims and authorization decisions over declared immutable inputs | Exact transition request and immutable external-input authority | Independent transition-time lifecycle | Global StandardsAuthorityView membership and caller-minted authority | Deleting them recreates trust adaptation and evidence validation in analysis |

The matrix is the admission inventory. It is not an executable dependency
manifest. Executable dependency closure comes only from AuthorityBoundValues
and stored object references.

## Structural Closure Algorithm

1. Resolve the supplied StandardsAuthorityView directly and verify its content
   and selected authority references.
2. Validate required roles and cross-reference coherence for the requested
   operation. Missing required authority is `unavailable`; a contradictory
   selection is `invalid`; a recognized but unsupported semantic contract is
   `unsupported`.
3. Invoke each owning domain Module. Every compiled or interpreted value is an
   AuthorityBoundValue whose direct dependencies are produced by that same
   construction path.
4. Compose the result from those values. The composing kernel unions their
   direct references and traverses the immutable object DAG to obtain the exact
   transitive dependency set.
5. Canonicalize references by typed `(object_kind, semantic_id)`, reject a
   cycle, missing dependency, kind contradiction, or same-key/different-value
   conflict, and publish the ExecutionClosure.
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
| Content capture meaning | Capture contract owned by `standards_authority`; material capture changes affect ContentSnapshot identity |
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

Provider and authorization authorities do not belong to every
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
objects, decisions, and ExecutionClosure. It does not invoke live providers or
request fresh authorization. Creating a successor may require those
transition-time authorities.

## Repository Interface

`standards_authority` exposes one small internal Interface:

```python
content = capture(source_adapter, capture_request)
handle = put(domain_object)
domain_object = get(handle)
```

`put` receives an object already validated by its owning Module and verifies
the closed envelope, owner-issued semantic identity, direct dependency
existence/kind, and acyclic DAG. Generated object-kind dispatch selects the
owner's decoder and validator. The repository never interprets a generic
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
analysis handle. Results expose their exact ExecutionClosureHandle. Callers
never supply subordinate semantic-authority handles, operation closures,
provider objects, authorization objects, or version maps.

## Required Mutation And Reconstruction Evidence

The operation-dependency evidence must cover every selected authority role:

| Mutation | Required identity result |
| --- | --- |
| Captured bytes, manifest, scope, exclusion, nesting, or capture semantics change | ContentSnapshot and every material dependent closure change |
| Routing authority changes | Route closure/result change; unrelated read and analysis identities remain stable |
| Metadata or parser meaning changes | Metadata view and every actual dependent closure change; ContentSnapshot remains stable |
| Graph or policy-impact meaning changes | Related/analysis dependents change; unrelated route/read identities remain stable |
| Coverage authority changes | Coverage and affected analysis identities change; navigation remains stable |
| Provider or authorization authority changes | Only affected analysis transition/state changes |
| Authority unused by an operation changes | That operation closure and result remain byte-identical |
| Storage envelope or public result projection changes without semantic change | Semantic object, closure, and result IDs remain stable |

Additional required evidence:

- every public handle resolves directly in a fresh process after repository
  source, process caches, live providers, and authorization services are
  removed;
- existing analysis projection succeeds without transition-time authorities,
  while a new transition requiring unavailable authority publishes nothing;
- adding a new executable dependency without an AuthorityBoundValue reference
  fails construction or a mutation-closure test;
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
- storage envelope or wire representation must enter domain semantic identity;
  or
- a new public operation, compatibility layer, A2 behavior, or mutable head is
  required.
