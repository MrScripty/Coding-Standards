# Standards Engine Navigation And Analysis

**Status:** Accepted

The repository will provide a read-only Standards Engine facade over neutral
metadata, generic graph traversal, and standards-specific analysis. A1 uses one
versioned JSON Schema document as its machine contract, binds every operation to
immutable repository inputs, and exposes typed results to Python and agent-tool
callers. This preserves one authority for transport shape while keeping policy
meaning in standards documents and keeping controlled authoring outside A1.

## Context

Canonical standards metadata is currently discovered by verifier-owned code,
while routing, graph navigation, policy-impact review, and future agent callers
need the same neutral facts. The repository also lacks one contract for typed
navigation, snapshot comparison, impact obligations, iterative resolution, and
bounded audit coverage. Letting each consumer define those concepts would
create competing metadata loaders, schemas, and completion rules.

The accepted development brief and active plan separate read-only navigation
and analysis from controlled authoring. A1 must be independently useful without
proposal storage, repository mutation, semantic acceptance, or application
authority.

## Decision

### Module boundaries

The dependency direction is:

```text
standards_engine
  |-- standards_metadata
  |-- standards_applicability
  |-- standards_policy_impact
  `-- standards_analysis

standards_applicability
  `-- Python standard library

standards_policy_impact
  |-- standards_applicability
  |-- standards_metadata
  `-- graph_engine

standards_analysis
  |-- standards_applicability
  |-- standards_metadata
  |-- standards_policy_impact
  `-- graph_engine

standards_verifier
  |-- standards_policy_impact
  |-- standards_metadata
  `-- graph_engine
```

`standards_engine` is the composition root and agent-facing facade.
`standards_metadata` loads and validates repository-owned corpus membership and
module metadata. `standards_applicability` compiles typed fact schemas,
applicability programs, and request fact sets and evaluates them without
repository or domain dependencies. `standards_policy_impact` compiles source-owned typed
policy-impact declarations into one neutral graph contribution and one typed
semantics index. `standards_analysis` owns policy-unit comparison, impact
selection, packets, obligations, reading plans, questions, and audit
certificates. `graph_engine` remains domain-neutral. The verifier consumes the
neutral and policy-specific Modules but is not their owner.

Canonical documents remain authoritative for module IDs, aliases, paths,
`Requires`, `Specializes`, and policy meaning. A registered generic catalog
owns non-module nodes and the existing `policy-impact` and `semantic` group
contracts. Policy-unit declarations own stable unit identities,
module-relative locators, accepted semantic revisions, and policy-impact source
identity. Module-owned typed policy-impact declaration files are the sole
relationship authority, but every relationship source is an active policy unit
contained by that owner module. Compiled graph edges, semantics indexes, graph
indexes, packets, reports, and certificates are projections, not authority.

### Public interface

A1 exposes four operations:

```python
query(snapshot, request) -> NavigationResult | RejectedResult
prepare(request) -> PendingPacket | CompletedAnalysisReport | RejectedResult
resolve(packet, submission) -> PendingPacket | CompletedAnalysisReport | RejectedResult
inspect(handle) -> InspectionResult | RejectedResult
```

Native Python requests and results are typed projections of the canonical
contract. Agent tools carry the same structures as JSON. An optional CLI or
text renderer may project those results for humans, but no command-string
language or formatted prose is an input authority.

A trusted source provider creates the initial `SnapshotHandle` when the engine
or tool session is established. It gives the caller a handle, not a repository
path or loader configuration. Snapshot compilation is an internal provider
seam in A1, not a fifth caller-authored operation. Every subsequent query and
analysis call carries the issued handle explicitly; adapters must not replace a
missing or stale handle with the ambient current tree.

Expected domain outcomes return `RejectedResult`. Violated internal invariants,
unhandled variants, corruption, and nondeterministic serialization remain
programming errors rather than domain rejections.

### Canonical contract authority

[`a1-contract.schema.json`](../../tools/standards_engine/contracts/a1-contract.schema.json)
is the sole machine authority for A1 request, result, handle, submission,
declaration, certificate, and analysis-artifact shapes. It uses JSON Schema
Draft 2020-12 plus documented `x-standards-engine-*` annotations for projection,
identity, authorization, and state-machine metadata that JSON Schema does not
natively express.

Python models, JSON validation, agent-tool definitions, examples, and text
renderers must be generated from or mechanically checked against this schema.
The contract validator rejects unsupported schema keywords in the maintained
subset, validates every example against its declared definition, and checks
identity fixtures. A new projection cannot introduce fields, enums, variants,
defaults, or state transitions absent from the schema.

This choice avoids a repository-specific interface language and avoids a new
third-party dependency. If the contract grows beyond the maintained JSON
Schema subset, that is a re-plan trigger rather than authority to add an
independent validator model.

The projection mechanism is fixed as follows:

- `generate_contract.py` will generate the Python request/result algebra into
  `tools/standards_engine/standards_engine/_generated_contract.py` and the agent
  tool definitions into `tools/standards_engine/contracts/generated/`.
- Generated files are read-only projections and are checked with a deterministic
  `--check` mode; runtime code does not parse the schema to discover behavior.
- JSON payload validation uses the canonical schema and its maintained subset.
- Examples are validated directly against their named schema definitions.
- The text renderer is a handwritten exhaustive adapter over the generated
  result union. Conformance tests instantiate every result variant and reject a
  missing renderer branch; rendered prose never feeds engine state.

The public package entry points will be:

- `standards_metadata.__init__`: immutable corpus views, resolution, and neutral
  metadata diagnostics;
- `standards_applicability.__init__`: immutable fact schemas, applicability
  programs, fact sets, evaluation results, and typed neutral failures;
- `standards_analysis.__init__`: snapshot comparison, `prepare`, `resolve`, and
  analysis inspection contracts;
- `standards_policy_impact.__init__`: compilation of registered typed
  declarations into a neutral graph contribution and policy semantics index;
  and
- `standards_engine.__init__`: `StandardsEngine`, generated public request and
  result types, snapshot-bound `query`, agent-tool adapters, and text rendering.

Internal loaders, graph providers, schema generators, and document locators are
not re-exported through the facade.

Contract version `2` has one representation. It deliberately replaces version
1 to add compiled policy-impact declarations, fact-free `always`
applicability, and derived policy-impact identities. All current producers and
consumers must switch together; version 1 is not a runtime fallback. A further
incompatible field, variant, identity, applicability, state-machine, or
completion change requires a new contract version and an explicit migration
decision. Unknown versions are `unsupported`.

Before the first runtime projection was accepted, version 1 was clarified to
represent both canonical whole-artifact modules and registered structured
policy units during read and inspection. This closes an omission demonstrated
by the already accepted module-ID route examples; it has no predecessor runtime
representation to migrate. After runtime acceptance, adding or changing either
declaration variant follows the version-migration rule above.

Generic graph edge identities are represented by the distinct `EdgeId` type.
Most graph providers retain their own registered or derived identity contracts.
Compiled policy-impact identities are the deliberate exception: the
`standards_policy_impact` compiler derives
`policy-impact:v1/<encoded-source>/<encoded-relation>/<encoded-consumer>` from
one unique natural key. Each segment is UTF-8 encoded and every byte outside the
unreserved URI character set is percent encoded with uppercase hexadecimal.
This framing is injective even when canonical IDs contain colons or other
separators. Duplicate natural keys are invalid. The A1 cutover records every
former ID and its canonical replacement, then removes the former identities
without aliases, hashes, lookup fallback, or dual runtime authority.

### Serialization and identity

Identity-bearing values use UTF-8 canonical JSON with schema-defined fields,
lexically ordered object keys, semantically ordered arrays, NFC-normalized model
strings, canonical enum strings, JSON booleans, and base-10 integers. Floating
point values are prohibited. Missing and `null` remain distinct. Raw
representation digests hash source bytes without normalization.

Identity is SHA-256 over a domain prefix, a NUL byte, and canonical identity
bytes. The domains are:

```text
coding-standards:snapshot:v1
coding-standards:navigation:v1
coding-standards:packet:v1
coding-standards:obligation:v1
coding-standards:analysis-report:v1
coding-standards:certificate:v1
```

Human summaries, text rendering, timestamps, logging IDs, display-only order,
and derived `next_operations` are excluded. Certificate timestamps live only in
a provenance envelope. Equal declarations and derived inputs therefore produce
equal certificate IDs.

### Snapshots and policy identity

A clean Git snapshot uses its tree object as content identity and records its
commit only as provenance. Dirty and non-Git inputs use a deterministic manifest
covering relevant tracked and untracked entries, explicit exclusions, entry
types, modes, content digests, symlink target strings, and nested repository or
submodule state. Symlinks are not followed by default. A provider that would
follow an escaping link must reject the snapshot.

Policy-unit IDs are immutable and independent of source location. A declaration
references a canonical module and module-relative heading locator; the document
path is derived through `standards_metadata`. Moves retain identity. Splits and
merges use predecessor and successor relationships, not aliases. Retirement
creates a permanent tombstone, and retired IDs are never reused.

Representation digests, structural digests, and accepted semantic revisions
remain distinct. Structural equality may classify a representation-only
candidate but cannot prove semantic equivalence. Proposed semantic state is an
`AnalysisRequest` overlay and cannot modify accepted policy-unit authority.

### Applicability and audit coverage

The canonical A1 JSON Schema owns serialized applicability expressions, fact
declarations, fact values, and evaluation-result shapes.
`standards_applicability` owns their executable semantics. Its Interface is:

```python
schema = compile_fact_schema(declaration)
program = schema.compile(expression)
facts = schema.bind(raw_facts)
result = program.evaluate(facts)
```

Fact schemas, programs, and fact sets are immutable. One schema compiles many
programs; one bound fact set evaluates many programs. A program rejects a fact
set from another schema identity. Its dependency digest binds applicability
language version, normalized expression, and exact referenced fact definitions
through domain-separated canonical serialization. Mechanically maintained
conformance tests prove that runtime operators, types, states, and projections
agree with the canonical JSON Schema; Python runtime classes do not generate or
redefine the public serialized contract.

The language contains `always`, `all`, `any`, `not`, `equals`, `in`,
`contains`, and `exists`. Empty fact schemas are valid. `always` references no
facts and evaluates to `true`. Aliases resolve to canonical fact IDs during
program compilation and fact binding; supplying both names is invalid. Known
nullable values, known absence, and unknown remain distinct. Missing or
explicitly unknown facts produce `unknown` when material, and evaluation
returns the exact canonical unresolved facts responsible for that result.
`all`, `any`, and `not` use the documented Kleene three-valued truth tables and
never coerce unknown.

Malformed expressions, unknown operators, invalid arity, undeclared facts,
type errors, alias conflicts, incompatible fact schemas, and out-of-domain enum
values are typed invalid failures. Unsupported language versions are typed
unsupported failures. Repository unavailability remains an Adapter concern.
Router and analysis policy own questions and explanatory text. Policy-impact,
analysis, engine, and verifier callers translate neutral failures into their
own diagnostics. Whole-artifact review may accompany an unknown result but
cannot turn it into `true`.

Analysis derives a `CoverageAuditRequirement` from the exact compiled authority
view, policy-unit semantic revision and structural state, relationship set,
applicability contract, fact schema, and registered audit horizon. An authorized
reviewer may submit a `CoverageAttestation` for that exact requirement. A
generated immutable `ConsumerCoverageCertificate` binds the attestation to
those derived inputs. It certifies consumer-discovery coverage only; it never
contains a report or change-specific disposition.

`CompletedAnalysisReport` references every certificate used and separately
owns the change-specific dispositions. Completion requires exact equality
between required coverage subjects and valid certificate subjects, plus exact
equality between reached consumer obligations and dispositions. A successful
empty consumer set therefore requires a current certificate without creating a
report/certificate identity cycle. Timestamps are excluded from certificate
identity.

Accepted and proposed applicability contexts are independently bound to their
authority view's fact schema. Equal schemas may share one immutable fact set;
different schemas use separately validated fact sets. Until schema evolution is
implemented, it returns `FACT_SCHEMA_EVOLUTION_UNSUPPORTED` rather than
silently becoming a permanent schema-equality invariant.

### Graph composition

A1 uses existing named groups and never duplicates graph storage or traversal.
The generic `policy-impact` group permits incoming and outgoing discovery, but
domain impact propagation is independently fixed by the policy
relationship-kind contract. Current kinds propagate from source to consumer and
are non-transitive. Generic group direction therefore does not authorize
semantic propagation. Dependency and specialization traversal follows each
existing group's transitive policy.

`standards_policy_impact` owns relationship-kind contract version 1 as a small
versioned Python table inside the module. It admits the eight current relation
kinds. Every admitted kind belongs to the existing `policy-impact` and
`semantic` groups, propagates from source to consumer, is traversable, and
requires an explicitly authored `evidence_owner`. There is no declaration-level
propagation override in version 1. Changing these semantics is contract
evolution, not configuration. The compiler validates every evidence owner
against the registered evidence-owner nodes and never guesses from a consumer.

| Change type | Accepted graph groups | Proposed graph groups |
| --- | --- | --- |
| modification | `policy-impact` | `policy-impact` |
| addition | none for an absent policy; current owner context only | `policy-impact`, `standards-requires`, `standards-specializes` |
| removal | `policy-impact` | none for the removed policy; current owner context only |
| same-module move | `policy-impact` | `policy-impact` |
| cross-module move | `policy-impact`, `standards-requires`, `standards-specializes` | `policy-impact`, `standards-requires`, `standards-specializes` |
| split | predecessor `policy-impact` | every successor `policy-impact` |
| merge | every predecessor `policy-impact` | successor `policy-impact` |

The candidate set is the union of the named accepted and proposed traversals.
`semantic` is not selected because it is broader than reviewed policy-impact
propagation. `standards-dependencies` is not selected because its combined view
would hide whether `Requires` or `Specializes` selected an obligation. An edge
present in several selected groups remains one edge with all selected
provenance; group membership does not duplicate it.

Changed normative content outside exactly one valid policy-unit locator creates
a mandatory `unmapped-normative-change` obligation. Missing edges or absent
audit coverage cannot be interpreted as no impact.

Policy-impact relationships originate from coherent policy units, not module
IDs. Modules remain document, navigation, `Requires`, and `Specializes`
identities. A module-level relationship query derives an aggregation over the
module's contained policy units and exposes unmapped normative coverage; it
does not create module-source edge authority. A broad legacy relationship may
split into several policy-unit relationships when it projected independently
changeable policies. Semantic mapping dispositions, not legacy edge-count
equality, govern the cutover.

### State, authorization, and completion

Packets and obligations are immutable and content-addressed. A changed bound
input always makes the old packet stale. A new packet may reuse a prior decision
only when the decision kind's declared dependency fingerprint is equal in full.
Unknown or incomparable dependencies reopen the decision.

`next_operations` is derived from current state and is guidance, not
authorization. Trusted adapters inject capability context outside
caller-authored request and submission payloads. A1 distinguishes
`standards.read`, `standards.analyze`, `standards.review.consumer`,
`standards.review.impact`, and `standards.review.audit`; one capability does not
imply another.

`CompletedAnalysisReport` is returned only when final reached consumer-review
obligation IDs exactly equal valid current disposition IDs and every other
question, obligation, authorization, evidence, applicability, and audit
condition is resolved. It records analysis completion only. It cannot accept
policy meaning, authorize a relationship, or permit repository application.

## Considered Options

- Keep neutral metadata inside `standards_verifier`: rejected because analysis,
  graph composition, and agent navigation would depend on verifier ownership or
  duplicate the loader.
- Make Python classes the schema authority: rejected because agent-tool and
  cross-process JSON consumers would need a second independently maintained
  contract or a repository-specific generator language.
- Add a custom interface-definition language: rejected because JSON Schema can
  express the required transport algebra and a custom language would add more
  parser and maintenance surface.
- Add a third-party schema package now: rejected because the accepted contract
  can be admitted and checked with the standard library; a dependency is not
  yet justified.
- Select the broad `semantic` or combined `standards-dependencies` groups:
  rejected because they weaken relation-specific explanations and can select
  relationships outside the current A1 contract.
- Combine controlled authoring with A1: rejected because mutation,
  authorization, application, and recovery require a stronger separate
  lifecycle and acceptance model.
- Add an edge-keyed policy semantics sidecar: rejected because generic topology
  and policy semantics would remain two declarations that must be synchronized.
- Replace every graph relationship with one policy compiler: rejected because
  `Requires`, `Specializes`, suite dependencies, nodes, and graph groups
  already have correct independent authorities.

## Consequences

- Milestone 1 must cut every inventoried metadata consumer to one neutral API in
  one bounded migration and remove the old neutral loader.
- A1 implementation must preserve explicit snapshot handles at transport
  boundaries even if native Python offers a snapshot-bound convenience view.
- Contract evolution requires an explicit contract version and projection
  conformance evidence; compatibility behavior is not inferred.
- Analysis can be conservative but cannot silently resolve uncertainty.
- Policy-impact compilation rebuilds the complete registered declaration set.
  Reuse decisions depend on exact fingerprints over every relevant declaration,
  node, kind, fact, evidence, audit, and group contract rather than an assumed
  incident-edge-only invalidation rule.
- A future controlled-authoring design may reuse A1 identities and reports but
  must define a distinct apply-eligible result and post-write recovery contract.

## Affected Boundaries

- `tools/standards_engine/contracts/a1-contract.schema.json`
- `tools/standards_applicability/`
- future `tools/standards_metadata/`
- future `tools/standards_analysis/`
- `tools/standards_policy_impact/`
- `tools/standards_graph/`
- future `tools/standards_engine/`
- `tools/standards_verifier/standards_verifier/canonical_modules.py`
- `tools/standards_verifier/standards_verifier/repository_graph.py`
- `tools/query_edges.py`
- `tools/graph_engine/README.md`
- canonical corpus and edge-source registries
- policy-unit, policy-impact, and consumer-audit declarations

## Supersession

This decision supersedes the earlier combined direction in which A1 also owned
controlled authoring and in which prose command examples could be interpreted
as the agent interface. It does not supersede the accepted generic graph-engine
decision or verification-engine architecture. It specializes them for the A1
Standards Engine boundary.
