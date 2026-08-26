# Standards Engine A1b Contract And Authority Foundations

**Status:** Proposed

This decision supersedes the contract-compilation, identity-module placement,
snapshot capture, persisted-state storage, and public result-projection clauses
of [Standards Engine Navigation And Analysis](standards-engine-navigation-analysis.md).
It preserves A1's four-operation read-only facade, immutable analysis-state
kernel, policy-impact authority, graph boundaries, and separation from A2
controlled authoring.

## Context

A1 correctly established one read-only Standards Engine facade and one
content-addressed analysis lifecycle. Its supporting implementation nevertheless
has three coupled defects:

1. the canonical schema, local validator, generator, and generated decoder each
   implement part of the same contract semantics;
2. JSON Schema instance equality is incorrectly implemented with A1 identity
   canonicalization; and
3. snapshot and analysis handles do not share one storage owner for their
   complete immutable authority closure.

The accepted standards recovery requires A1b to replace these foundations
before A2 may be reviewed. Repository inventory found no independently deployed
A1 consumer and no retained persisted A1 state. A coordinated breaking
replacement is therefore simpler than compatibility readers, writers, or state
conversion.

## Decision

### Module graph

Add three narrow modules:

```text
standards_identity
  `-- Python standard library

standards_contracts
  |-- standards_identity
  |-- jsonschema
  `-- referencing

standards_authority
  |-- standards_contracts
  `-- standards_identity

standards_engine
  |-- standards_authority
  |-- standards_contracts
  `-- existing domain modules
```

`standards_identity` owns A1's versioned NFC-normalizing identity encoding,
raw-byte digests, and domain-separated hashes. It exposes no generic equality
operation. Moving this implementation out of metadata corrects dependency
direction without changing existing identity bytes.

`standards_contracts` owns contract compilation, the admitted schema profile,
Draft 2020-12 execution, local-reference resolution, reachable-definition
closure, deterministic diagnostic adaptation, generated public models, and
agent-tool projections. It has no metadata, graph, analysis, repository-path,
store, or facade dependency.

`standards_authority` owns immutable capture and resolution for three typed
roots: snapshot, analysis, and navigation. It is not a general object-graph
framework. In-memory and directory-backed storage are private adapters behind
one Interface.

`standards_analysis` retains change classification, impact selection, fact and
obligation semantics, coverage decisions, immutable analysis-state
normalization, projection, and transition. It loses snapshot capture and state
storage. `standards_engine` remains the composition root and converts internal
domain outcomes exhaustively into the public result algebra.

### Contract compiler

The internal Interface is:

```python
contract = compile_contract(schema_source)
decoded = contract.decode(definition_id, unknown_value)
json_value = contract.to_json_value(decoded)

artifacts = compile_projections(contract, targets)  # build-time only
```

`compile_contract` selects the fixed A1b Draft 2020-12 profile. Standard keyword
behavior is delegated without overrides to `jsonschema.Draft202012Validator`.
An explicit immutable `referencing.Registry` admits only the root resource and
same-resource references. Runtime network retrieval is prohibited.

`standards_contracts` owns strict parsing, keyword admission, reference policy,
definition reachability, project annotations, stable diagnostics, model
construction, and deterministic projection. Generated models own only immutable
representation, field mapping, and calls into the compiled contract. They do
not contain schema fragments or an independent keyword interpreter.

Contract failures expose a stable code, outcome, definition, instance JSON
Pointer, schema JSON Pointer, keyword, and nested causes. Dependency exceptions
and message text do not cross the module boundary.

Every public operation must have a complete reachable request and result
closure. Agent-tool projections include only the closure reachable from that
operation. Unreachable public definitions and unsupported reachable keywords
are invalid contract compilation; they are never silently omitted.

Closed executable annotations may direct projection, authority, identity, and
contract compilation. Free-form invariant or state-machine prose is not machine
authority. Cross-field invariants, authorization, and transitions remain owned
by their domain modules unless an annotation has a closed schema and named
executable owner.

### Equality domains

The three equality domains are independent:

| Domain | Owner | Rule |
| --- | --- | --- |
| JSON Schema instance equality | Draft 2020-12 validator | Same JSON type, codepoint string equality, mathematical number equality, recursive array/object equality |
| Applicability value equality | `standards_applicability` | Its explicit, versioned domain semantics |
| A1 identity canonicalization | `standards_identity` | Existing NFC-normalizing identity format version 1 |

Identity bytes are never used to decide JSON Schema `const`, `enum`, or
`uniqueItems`. Preserving identity format version 1 avoids unrelated handle and
decision churn; only identities whose semantic inputs or explicit domains
change advance.

### Dependency selection

Adopt `jsonschema` 4.26.0 as the Draft 2020-12 semantics implementation. Declare
`referencing` directly because A1b uses its public registry Interface. Record
the complete resolved transitive closure and hashes in an A1b-owned lock
artifact; installation and verification must use that lock rather than ambient
packages. The direct package manifests continue to state the runtime
requirements they own.

The dependency decision and licensing disposition are recorded in the
[dependency and dialect report](../plans/standards-engine-a1b/reports/dependency-and-dialect-decision.md).
No third-party source or test corpus is copied into the repository. Independent
acceptance obtains an exact official JSON Schema Test Suite revision into
temporary storage. An unavailable oracle is a blocked claim, not a passing
fallback.

### Immutable authority repository

The internal Interface is:

```python
snapshot_handle = authority.capture(source_adapter)
analysis_handle = authority.commit(analysis_root)
navigation_handle = authority.commit(navigation_root)
root = authority.resolve(handle)
```

Capture is trusted bootstrap, not a fifth public Standards Engine operation.
The initial directory adapter stores each bounded snapshot as one atomic bundle
containing its manifest and included bytes. Analysis and navigation roots are
separate immutable records that reference snapshots. The Interface permits a
future blob-deduplicating adapter without exposing storage layout, but A1b does
not implement a generic DAG, garbage collector, remote store, mutable index, or
arbitrary object kind.

A snapshot root binds its exact sorted manifest, scope, exclusions, entry
types, modes, symlink targets, nested snapshot references, included source
bytes, and semantic compiler versions needed to reconstruct metadata, routing,
graphs, policy impact, applicability, and coverage. Public interface bindings
and implementation-only versions are not snapshot inputs.

An analysis root binds base and proposed snapshots, normalized changes and
semantic proposals, authorization and provider authority views, validated fact
observations, review dispositions, coverage attestations and decisions, exact
evidence and authorization records, and analysis semantic versions. Derived
requirements, obligations, reading plans, certificates, summaries, results,
and next operations are recomputed rather than stored as authority.

A navigation root binds its snapshot and the identity-bearing navigation
projection required for cold inspection. Policy and relationship handles remain
snapshot-scoped. Coverage and certificate handles become snapshot-owned;
analysis context, fact requirement, and observation handles become
analysis-owned. Resolution never scans all states or treats a cache as an
index.

Capture verifies every entry before atomically publishing a root. Directory
publication is create-only, collision-checked, durably synchronized, and root
last. A failed capture issues no handle. A cold process opens only the authority
repository and reconstructs every advertised operation and inspection without
the source path, Git object database, provider capability, prior process cache,
or fresh authorization authority.

### Public cutover

Preserve:

```python
query(snapshot, request) -> NavigationResult | RejectedResult
prepare(request) -> AnalysisResult | RejectedResult
resolve(analysis_handle, submission) -> AnalysisResult | RejectedResult
inspect(handle) -> InspectionResult | RejectedResult
```

Use one coordinated contract version 11 replacement. Advance snapshot,
navigation, and analysis handle schema and identity domains from version 3 to
version 4 because their closure and owner qualification change. Advance the
analysis contract from 6 to 7 and result projection schema from 2 to 3 where
the public representation changes. Preserve applicability contract version 3
and identity format version 1.

Version 10 handles and persisted state are typed `unsupported`. There is no
dual validator, decoder, writer, compatibility re-export, state converter, or
fallback. Remove the old validator, generated keyword walker, snapshot compiler,
analysis-state stores, and internal serialization imports in the same accepted
cutover.

## Consequences

- One established implementation owns Draft semantics; project code owns only
  the narrower profile, projections, and diagnostics.
- Identity normalization remains explicit without contaminating schema
  equality.
- One authority Interface closes capture, persistence, reopening, and
  inspection while keeping domain behavior in its current owners.
- The public replacement is intentionally breaking but has no known external
  migration consumer.
- A new runtime dependency and its transitive native package require exact
  resolution, supported-target, security, provenance, and licensing evidence.
- Cold reconstruction may perform deterministic recompilation; caches improve
  speed but never become authority.

## Rejected Alternatives

### Continue the local Draft subset

Rejected because it preserves two local semantic interpreters and permanent
ownership of standardized equality, references, composition, patterns, and
conformance.

### Make Python classes the contract authority

Rejected because agent tools and other structured consumers still require JSON
Schema. Generating schema from code would move rather than eliminate semantic
projection and would reverse the accepted declaration authority.

### Call the dependency directly from each adapter

Rejected because profile admission, references, diagnostics, reachability, and
version behavior would leak into several callers.

### Store snapshots in analysis and states in the facade

Rejected because it preserves fragmented resolution and process-local lookup.

### Build a generic content-addressed object graph

Rejected because A1b needs only three root kinds and bounded snapshot bytes.
Generic traversal, collection, remote storage, and mutable indexes add no
current Leverage.

### Change identity canonicalization with schema equality

Rejected because the domains are independent. Changing NFC identity bytes
would create broad migration work without correcting any additional A1b
defect.

## Re-Plan Conditions

Re-plan before implementation continues if:

- an external public consumer or retained persisted A1 state is found;
- the contract requires remote references, custom vocabularies, format
  assertion, validator overrides, unsupported recursive projections, or a
  pattern outside the admitted compatibility profile;
- a supported target cannot resolve the locked dependency closure;
- runtime schema parsing is prohibited and a generated validator program is
  proposed;
- any retained project annotation lacks a closed schema and executable owner;
- snapshot size or required streaming invalidates bounded atomic bundles;
- evidence bytes or non-identity capture provenance must become replay
  authority; or
- A2 mutable heads, application authority, or recovery behavior is pulled into
  this module.

## Acceptance

This ADR remains Proposed until the A1b plan is independently admitted. It
becomes Accepted only with A1b implementation and exact-tree acceptance. A2
remains inactive throughout.
