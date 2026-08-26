# Standards Engine A1b Contract And Authority Foundations

**Status:** Proposed

This decision supersedes the contract-compilation, identity encoding, snapshot
capture, persisted-state storage, and public result-projection clauses of
[Standards Engine Navigation And Analysis](standards-engine-navigation-analysis.md).
It preserves A1's four-operation read-only facade, immutable analysis kernel,
policy-impact authority, graph boundaries, and separation from A2 controlled
authoring.

## Context

A1 established one read-only Standards Engine facade and one content-addressed
analysis lifecycle. Its supporting implementation nevertheless has three
coupled defects:

1. the canonical schema, local validator, generator, and generated decoder each
   implement part of the same contract semantics;
2. one recursive NFC serializer is used for schema equality, semantic ordering,
   and content identity even though those domains have different rules; and
3. inspectable handles do not share one direct immutable storage and resolution
   contract, so some values depend on owner maps, scans, or process-local state.

The accepted standards recovery requires A1b to replace these foundations
before A2 may be reviewed. Repository inventory found no independently deployed
A1 consumer and no retained persisted A1 state. A coordinated breaking
replacement is therefore simpler than compatibility readers, writers, or state
conversion.

## Decision

### Module graph

Add three narrow Modules:

```text
standards_identity
  `-- Python standard library

standards_contracts
  |-- jsonschema
  |-- referencing
  `-- Python standard library

standards_authority
  |-- standards_identity
  `-- Python standard library

standards_engine
  |-- standards_authority
  |-- standards_contracts
  `-- existing domain Modules
```

`standards_identity` owns deterministic identity encoding version 2 and
domain-separated hashing. It preserves strings and object keys
codepoint-for-codepoint and exposes no generic equality, normalization,
semantic sorting, deduplication, defaulting, or field-selection operation.
Domain Modules construct their own typed identity records before hashing.

`standards_contracts` owns contract loading, the admitted projection profile,
same-resource reference configuration, public-definition reachability, stable
diagnostic adaptation, generated public models, and agent-tool projections. It
does not implement JSON Schema keywords. `jsonschema.Draft202012Validator` is
the sole executable Draft 2020-12 validator.

`standards_authority` owns immutable storage and direct resolution for every
public inspectable object. It is not a general object database: the object-kind
vocabulary is closed, objects are immutable and content addressed, and no
enumeration, mutable index, graph traversal, garbage collection, remote store,
or arbitrary blob API is exposed.

`standards_analysis` retains change classification, impact selection, fact and
obligation semantics, coverage decisions, immutable analysis normalization,
projection, and transitions. It loses snapshot capture and state storage.
`standards_engine` remains the composition root and exhaustively adapts domain
outcomes to generated public results.

### Contract compiler

The internal Interface is:

```python
contract = compile_contract(schema_source, interface_source)
decoded = contract.decode(definition_id, unknown_value)
json_value = contract.to_json_value(decoded)

artifacts = compile_projections(contract, targets)  # build time only
```

`compile_contract` verifies the schema with
`Draft202012Validator.check_schema`, installs an immutable
`referencing.Registry` containing only the root resource, computes the exact
closure reachable from the four public operations, and rejects projection
constructs that generated Python or agent-tool targets cannot preserve.
Runtime retrieval, remote references, custom vocabularies, format assertion,
keyword overrides, and dynamic references are prohibited.

The canonical JSON Schema owns only serialized request, result, submission,
inspection, and public-handle shapes. A closed `a1-interface.toml` owns public
operation names, input and result roots, interface versions, and capability
selection. Domain Modules own identities, cross-field invariants,
authorization, state transitions, policy meaning, and projection lifecycle.
Version 11 removes all `x-standards-engine-*` annotations from the schema.
The exact proposed machine-readable authorities are the planning
[`a1-contract-v11.schema.json`](../plans/standards-engine-a1b/reports/a1-contract-v11.schema.json)
and
[`a1-interface-v11.toml`](../plans/standards-engine-a1b/reports/a1-interface-v11.toml).
Implementation compiles those admitted bytes in isolation and promotes them
unchanged at the atomic cutover; it does not discover or invent public shapes.

Generated models own immutable representation and field mapping. Construction
first invokes the same compiled validator used by every other contract entry
point; generated code contains no schema fragment or keyword interpreter.
Schema defaults remain annotations and are not injected into instances.

Contract failures expose stable project fields: outcome, code, definition,
instance JSON Pointer, schema JSON Pointer, keyword, and nested causes.
Dependency exceptions and message text do not cross the Module boundary.

A1b relies on the maintained dependency for Draft semantics. It does not copy,
run, or reproduce the complete official JSON Schema test corpus and does not
claim to re-certify Draft 2020-12. Repository tests prove only the selected
adapter, admitted projection profile, known A1 regressions, diagnostics,
generation, and public integration.

### Equality and identity domains

The domains are independent:

| Domain | Owner | Rule |
| --- | --- | --- |
| JSON Schema instance validity and equality | `jsonschema.Draft202012Validator` | Dependency-defined Draft 2020-12 behavior |
| Applicability value equality | `standards_applicability` | Its explicit versioned domain semantics, including deliberate NFC handling where already specified |
| Content identity | `standards_identity` plus each domain owner | Codepoint-preserving identity encoding v2 over a typed domain record |
| Ordering and deduplication | Owning domain Module | Typed semantic keys, not generic identity bytes |
| Raw content digest | Owning content producer | SHA-256 over exact bytes |

Identity encoding v2 accepts JSON `null`, Boolean, integer, string, array, and
string-keyed object values and rejects floating point and lone surrogates. Its
byte grammar fixes scalar escaping, minimal integer rendering, key order,
separators, and UTF-8 output. Domain hashing uses SHA-256 over a framed magic,
domain, ID prefix, and encoded payload with fixed big-endian lengths; output is
`<prefix>:sha256:<lowercase-hex>`. The complete byte grammar and fixtures are
binding in the
[identity/version matrix](../plans/standards-engine-a1b/reports/identity-version-object-matrix.md).
The encoder performs no semantic work.

Every directly stored inspectable replaces its former domain ID with the one
authority-object handle. Non-stored identities formerly using the recursive NFC
serializer advance their domain. Existing applicability digests, policy-impact
edge IDs, graph IDs, and raw byte digests remain unchanged only after focused
evidence proves they do not consume the retired encoder and their semantic
input is unchanged.

### Dependency selection

Adopt `jsonschema` 4.26.0 as the sole Draft 2020-12 implementation. Declare
`referencing` directly because `standards_contracts` uses its public immutable
registry Interface. An A1b-owned hash-checked lock records the complete exact
resolution for CPython 3.11 and 3.12 on Linux x86-64 with glibc 2.17 or newer.
The selected native artifacts carry the exact
`manylinux_2_17_x86_64.manylinux2014_x86_64` tags. Other architectures, musl,
and source builds are unsupported in A1b. Ambient installations are not
satisfaction evidence.

Package manifests own direct requirements, the supported Python range, and one
canonical source-tree public import root. The corresponding package
`__init__.py` owns exported symbols. One AST-backed Standards Verifier contract
derives every production cross-Module import and rejects imports below another
Module's root as well as literal or dynamic import bypasses. The verifier does
not copy `__all__` or maintain a package or symbol allowlist. Import smoke proves
that manifest-owned roots load; it does not decide boundary compliance.

The lock owns selected transitive versions and wheel hashes. Security,
provenance, supported-target, and licensing evidence are bound in the
[dependency decision](../plans/standards-engine-a1b/reports/dependency-and-dialect-decision.md).
No third-party source, wheel, or conformance corpus is copied into repository
history.

### Immutable authority repository

Every public handle directly addresses one immutable object:

```text
AuthorityObjectEnvelope v1
  object_kind
  payload_contract
  payload

object id = identity(
  domain="coding-standards:authority-object:v1",
  id_prefix=envelope.object_kind,
  value=envelope,
)
```

The internal Interface is:

```python
snapshot_handle = authority.capture(source_adapter, capture_request)
handle = authority.put(typed_object)
typed_object = authority.get(handle)
```

`standards_authority` owns capture orchestration and the Git-tree and mutable
manifest source adapters. `capture` validates scope, exclusions, paths,
symlinks, nested repositories, entry metadata, content digests, source
stability, contract versions, nested-object publication, and root publication.
The source adapter supplies observations through one bounded capture view; it
does not construct handles or stored envelopes.

Clean Git capture resolves one exact commit/tree and reads bytes from Git
objects, never the worktree. Dirty-Git and non-Git capture perform the admitted
two-pass manifest protocol: discover typed entries and first digests, read and
encode exact bytes, then re-read included bytes and relevant entry metadata.
Any difference returns `SNAPSHOT.SOURCE_CHANGED` as `unavailable` and
publishes no root. Unsupported filesystem representations reject explicitly.
This preserves the accepted source-race boundary while moving its owner out of
`standards_analysis`.

The repository verifies canonical bytes, object ID, envelope, closed object
kind, payload contract, object-local invariants, dependency existence/kind, and
handle-kind match on every read. It deliberately does not own Metadata,
Analysis, Graph, Applicability, authorization, or provider semantics. The bound
analysis kernel validates root-relative semantic coherence while resolving or
projecting an aggregate root; policy and relationship inspection adapters
validate snapshot-relative meaning. Missing content is `unavailable`;
contradictory content is `invalid`; and a well-formed unknown version is
`unsupported`.

The closed A1b object kinds are snapshot root, navigation result, analysis
root, policy inspection, relationship inspection, coverage certificate,
coverage view, coverage requirement, coverage attestation, analysis context,
fact requirement, and fact observation. Snapshot, navigation, and analysis
remain aggregate semantic roots. Child objects are deterministic generated
projections with explicit dependency handles, but they use the same direct
storage and resolution rule as roots.

Every payload field, exclusion, construction order, and dependency edge is
binding in the
[authority-object contracts](../plans/standards-engine-a1b/reports/authority-object-contracts.md).
Stored payloads exclude their own handle; resolution injects the verified
handle into the public projection. The dependency graph is acyclic, and no
context, requirement, observation, coverage object, policy inspection, or
relationship inspection points back to an analysis root.

Every stored payload field participates in its object ID. Presentation-only
fields therefore remain outside stored objects and are derived through the
exact result/presentation contract bound by the enclosing root.
`FactRequirementHandle` addresses only semantic requirement fields;
`PendingResult` joins them with a derived `FactRequirementWork` carrying the
current prompt and dependent-program display. Prompt rewording or another
relationship beginning to use the fact does not change requirement identity.

Coverage views preserve A1's narrower coverage identity: they embed exact
coverage-relevant semantic inputs but exclude the complete snapshot handle and
attestation-source records. Requirements therefore remain stable when their
matching repository-local attestation is committed; certificates bind the
view, requirement, and attestation without referring back to a report or full
snapshot.

Analysis contexts follow the same narrow-identity rule. They embed the changed
policy identities, accepted/proposed semantic revisions and digests, normalized
changes, and proposals, but exclude full snapshot handles, relationship
topology, attestations, and unrelated authority. Analysis roots retain the
complete snapshots for reproducibility. Fact requirements therefore remain
reusable when unrelated repository authority changes.

An analysis root binds the handles of every materialized inspectable child
needed to reproduce its current projection: context, snapshots, fact
requirements and observations, coverage views, coverage requirements,
attestations, and certificates. Dispositions remain handle-free decision
records. This gives cold inspection direct object resolution without asking the
repository to reconstruct domain meaning or letting a root omit a projected
child.

Snapshot capture stores the exact bounded manifest and included bytes needed
to reconstruct metadata, routing, graphs, policy impact, applicability,
coverage, reads, and inspections. Repository paths, worktree bytes, Git object
availability, and process caches are capture inputs only. Analysis roots store
exact authority references and dependency-valid accepted decisions; derived
requirements, obligations, reading plans, certificates, results, and next
operations remain deterministic projections. Navigation roots store the
identity-bearing navigation result and snapshot dependency.

Snapshot payloads represent arbitrary file bytes with padded standard Base64
under the versioned `snapshot-root.v1` payload contract. Base64 is a wire
representation, not text decoding or semantic normalization. The payload also
binds the SHA-256 digest and byte length of each decoded entry; reads verify all
three before returning bytes. This keeps bounded snapshots inside the closed
JSON-valued envelope without adding a second blob store or an arbitrary binary
object API.

File publication is create-only, collision checked, durably synchronized, and
atomic at the object boundary. A failed capture issues no root handle. A
cold process reconstructs every advertised operation and inspection from the
repository and handles alone, without source paths, Git objects, provider
capabilities, process caches, scans, or fresh authorization authority.

The A1b durable adapter is admitted only on Linux ext4. It requires regular-file
hard links within one directory, file and directory `fsync`, and advisory
`flock`. Unsupported filesystems reject before accepting writes. The adapter
stores each complete canonical envelope as one regular file. Reads are
lock-free. Writes use one repository-scoped publication lock that is
coordination state only, never semantic authority or a mutable head:

```text
<store>/.publication.lock
<store>/objects/<object-kind>/<digest-hex>
<store>/objects/<object-kind>/.stage-<unguessable-nonce>
```

Object kinds and digest hex values are validated against the closed envelope
and handle grammars before any filesystem operation. The configured store root
must already exist and be configured by one canonical absolute path. Empty
components, repeated separators, `.`, `..`, and NUL are invalid. The adapter
opens a trusted `/` directory descriptor, then walks every configured component
with descriptor-relative `openat` using
`O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC`. It verifies each result with
`fstat`, closes superseded descriptors, and retains the final store-root
descriptor. This rejects symlinks in intermediate as well as final components;
one `open` of the complete pathname is prohibited.

The adapter verifies the retained root's owner and mode through `fstat` and
performs all later opens, directory creation, links, unlinks, and status checks
relative to retained directory descriptors. It never returns to a concatenated
absolute path. Symlinks, non-regular final objects, and staging names outside
the reserved grammar reject. The store root is owned by the effective user and
is not group/world writable. Directories are `0700` and lock, staging, and
final files are `0600` independent of ambient umask.

Before its first write, the adapter reads the opened root descriptor's mount ID
from `/proc/self/fdinfo`, resolves that exact ID in Linux
`/proc/self/mountinfo`, and requires filesystem type `ext4` and a writable
mount. It then runs a private descriptor-relative capability probe in the store
root for same-directory hard linking, file/directory `fsync`, and advisory
locking. Probe artifacts are removed and the root directory is flushed before
acceptance. Missing or contradictory mount/capability evidence is `unsupported`,
not a weaker fallback.

The threat model excludes a malicious process with the same effective user,
which could alter any owner-writable local store regardless of this API.
Untrusted callers and other users may race path components; retained directory
descriptors prevent those changes from redirecting operations. Before success,
the adapter repeats the complete component-by-component walk from the trusted
`/` descriptor and requires the resulting `(device, inode, mount ID)` to equal
the retained descriptor. Any changed, missing, or newly symlinked component is
`unavailable` and never returns a handle. Lexical aliases using `.`, `..`, or
repeated separators are invalid rather than normalized; a symlink alias is
invalid; and two accepted canonical absolute paths denote the same root only
when their final device, inode, and mount ID are equal. The path string itself
never enters authority-object identity.

1. derive the final handle before I/O;
2. acquire the descriptor-relative repository publication file with exclusive
   advisory `flock`;
3. create the `objects` and closed object-kind directories when absent; after
   each creation, open the child descriptor, `fsync` it, and `fsync` its parent
   before proceeding;
4. while holding the lock, remove every regular file in the reserved staging
   namespace, then create one uniquely named staging file with
   `O_CREAT|O_EXCL|O_NOFOLLOW` relative to the object-kind directory;
5. write the exact canonical envelope bytes and `fsync` the staging file;
6. create the absent final filename with a directory-relative same-directory
   hard link from the staging file; this atomic create-only step never replaces
   existing content;
7. when the final name already exists, read and verify it before deciding
   idempotent success or identity collision;
8. `fsync` the object-kind directory, unlink the staging name in `finally`,
   `fsync` that directory again, revalidate the configured root identity,
   release the lock, and return only after final-object verification.

Publication ordering does not affect the identity or result for different IDs.
If another writer publishes the same ID first, the later writer reads and
verifies the final object:
byte-identical content is idempotent success; different content is an identity
collision and `invalid`; existing content is never overwritten.

An interruption before the hard link leaves only a non-resolvable staging
file. An interruption after the hard link may leave the caller with an unknown
outcome, but retrying the same immutable `put` deterministically
returns the same verified handle. Dependencies publish before an aggregate
root, so interruption may leave unreachable immutable objects but never a
published root with missing dependencies. A process crash releases the
publication lock; the next writer cleans abandoned staging files before
starting. Normal and failure paths clean their own staging file in `finally`.
This bounded internal staging cleanup is not object enumeration, garbage
collection, a public Interface, or semantic authority.

### Public cutover

Preserve:

```python
query(snapshot, request) -> NavigationResult | RejectedResult
prepare(request) -> AnalysisResult | RejectedResult
resolve(analysis_handle, submission) -> AnalysisResult | RejectedResult
inspect(handle) -> InspectionResult | RejectedResult
```

Submissions contain caller claims, not preconstructed authority objects. In
particular, a coverage-attestation submission names the current requirement
and supplies conclusion, evidence, exclusions, rationale, and auditor
provenance. The bound kernel obtains authorization from the trusted execution
context, validates the claim against current work and evidence contracts, and
constructs the stored attestation and handle. Callers cannot mint a handle or
author their own authorization record.

Use one atomic production replacement. Isolated foundation Modules may be
built and tested before cutover, but the canonical schema, generated algebra,
facade, domain consumers, catalog, relationships, suites, and coverage
authority change in one accepted v11 boundary.

Advance interface/schema 10 to 11, request contract 2 to 3, result projection
2 to 3, analysis contract/schema 6/3 to 7/4, every public handle to schema 4,
and every identity domain listed in the identity migration matrix. Version 10,
old handles, and old persisted states are typed `unsupported`. There is no
dual validator, decoder, serializer, store, compatibility re-export,
converter, alias, or fallback.

The cutover also updates the supplemental node catalog and source-owned
policy-impact relationships for every created, retained, or retired
implementation artifact. It analyzes accepted and proposed authority, assigns
every selected consumer a disposition, freezes the final horizon, and renews
only mechanically stale coverage attestations.

`policy-impact-registry.toml` remains the sole closed authority for declaration
source membership. New Cross-Platform and Security relationship declarations
enter compilation only through explicit registry entries. Policy-unit corpus
membership remains independent metadata authority; neither filenames nor
policy-unit membership imply a relationship source.

## Consequences

- One maintained dependency owns Draft semantics; project code owns only its
  adapter, profile, projections, and diagnostics.
- Identity encoding is simple and representation preserving; domain Modules
  own meaning instead of inheriting normalization from a utility.
- Every public handle has one storage and resolution rule, including cold
  inspection of child artifacts.
- The public replacement is intentionally breaking but has no known external
  migration consumer.
- A new runtime dependency and native transitive wheel require exact
  resolution, target, security, provenance, and licensing evidence.
- Package manifests provide one import-boundary authority consumed by dependency
  comparison, static boundary verification, and isolated import smoke.
- Relationship declarations remain explicit closed inputs, so adding a
  policy-unit sidecar cannot silently add or omit relationship authority.
- Materialized derived objects may be regenerated, but direct storage avoids
  hidden owner maps and makes inspection independent of ambient execution.

## Rejected Alternatives

### Continue the local Draft subset

Rejected because it preserves local ownership of standardized validation and
duplicates semantics already provided by the selected dependency.

### Run the complete official Draft corpus in A1b

Rejected because A1b is not a JSON Schema implementation. Re-certifying the
dependency would expand scope and maintenance without improving the project
adapter. Upstream owns Draft conformance; this repository owns only its use.

### Make Python classes the contract authority

Rejected because agent tools and structured consumers still require JSON
Schema. Generating schema from code would move rather than eliminate the
projection problem and reverse the accepted declaration authority.

### Preserve recursive NFC identity encoding

Rejected because a generic serializer should not silently choose semantic
equivalence for every domain. Version 2 preserves typed input exactly and
forces deliberate normalization into the domain that owns it.

### Store only aggregate roots

Rejected because child-handle inspection would still require owner maps,
state scans, reconstruction context, or cache authority. Direct objects give
all handles one resolution rule.

### Build a generic content-addressed graph

Rejected because the closed A1b object vocabulary needs no public traversal,
collection, arbitrary objects, mutable indexing, or remote storage.

### Discover relationship declarations from the filesystem or policy units

Rejected because file presence and policy-unit membership do not own
relationship-source membership. Policy units may have no outgoing relationship,
and deriving filenames would create path-based semantic authority beside the
closed registry.

### Enforce package boundaries only in the generator or import smoke

Rejected because generator checks omit handwritten facade code and successful
imports do not distinguish a public root from a private submodule. A single AST
verifier consumes manifest-owned roots across all production Modules; focused
generator tests remain implementation evidence rather than the acceptance
oracle.

## Re-Plan Conditions

Re-plan before implementation continues if:

- an external public consumer or retained persisted A1 state is found;
- a reachable public contract requires remote references, custom vocabularies,
  format assertion, validator overrides, dynamic references, unsupported
  projection semantics, or an incompatible pattern;
- a supported target cannot resolve the exact locked dependency closure;
- any `x-standards-engine-*` annotation remains or its replacement lacks a
  closed representation and executable owner;
- an inspectable handle cannot be represented by the closed authority-object
  vocabulary or requires scanning, ambient state, or a mutable index;
- the admitted Linux ext4 filesystem cannot provide same-directory atomic
  create-only hard linking, file/directory durable flush, or advisory-lock
  behavior required by the durable adapter;
- snapshot size or streaming invalidates bounded atomic capture;
- a changed artifact, policy-impact relationship, or coverage consumer falls
  outside the admitted atomic cutover; or
- a required relationship source cannot use the closed policy-impact registry,
  or a Module cannot express its production imports through one manifest-owned
  public root; or
- A2 mutable heads, application authority, or recovery behavior enters A1b.

## Acceptance

This ADR remains Proposed until the A1b plan is independently admitted. It
becomes Accepted only with A1b implementation and exact-tree acceptance. A2
remains inactive throughout.
