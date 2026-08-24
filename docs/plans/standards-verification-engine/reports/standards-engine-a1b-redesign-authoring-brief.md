# Development Brief: Standards Recovery And Standards Engine A1b Redesign

## Status And Authority

This brief is a non-authorizing design and sequencing report. It gives the
developer the required work before controlled authoring Plan A2 or any later
Standards Engine plan continues. It does not start implementation, reopen a
completed plan by itself, authorize a contract migration, or change a standards
policy.

Plan A1 is recorded as accepted at implementation commit
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`, with final acceptance in the
[A1 acceptance report](../../standards-engine-navigation-analysis/reports/a1-final-acceptance.md).
That record remains historical authority for what was reviewed and accepted at
that exact tree. This brief records newly identified risks and a corrective
successor design; it does not silently relabel earlier evidence.

The newly identified external-contract disagreement and the wider root-cause
audit make A1b a prerequisite for A2. Until A1b receives its own accepted plan,
implementation, migration, and independent acceptance:

- Plan A2 remains inactive.
- Controlled authoring, proposal mutation, canonical application, and recovery
  remain unavailable.
- Plan C external-project baselines remain inactive.
- Existing A1 behavior may be inspected and used as migration input, but it is
  not sufficient authority for extending the engine into mutation.

The future A1b `plan.md`, not this brief, must own implementation admission,
write sets, exact milestones, lifecycle state, blockers, and the next slice.

---

## 1. Required Sequence

Use this dependency order:

```text
standards audit
    -> standards recovery plan
    -> standards and semantic-graph implementation
    -> independent standards acceptance
    -> A1b plan and superseding ADR
    -> A1b implementation and migration
    -> independent A1b acceptance
    -> separate A2 review and admission
```

Do not combine standards correction, A1b runtime replacement, and A2 authoring
into one plan or acceptance result. Each transition requires its own exact-tree
evidence.

The standards recovery is complete only when the policies, Router
applicability, policy-unit identities, semantic consumers, prompts, templates,
fixtures, and executable enforcement agree. A1b planning is unavailable while
that recovery remains pending, blocked, incomplete, or only documented in this
brief.

---

## 2. Executive Finding

A1's central product architecture is worth preserving:

- one read-only Standards Engine facade;
- neutral metadata and graph mechanics below the facade;
- standards-specific analysis outside the generic graph engine;
- explicit snapshot and analysis handles;
- one immutable content-addressed analysis state;
- deterministic pending and complete projections; and
- controlled authoring kept outside A1.

The repair history did not replace those decisions. It repeatedly repaired two
supporting seams:

1. schema declaration, executable validation, generated models, serialization,
   and public results did not share one complete semantic implementation; and
2. snapshot and analysis handles did not initially close over all immutable
   authority needed for reads and cold-process inspection.

The process also accepted weak evidence for some of those claims. Generated
freshness, passing suite totals, and agreement between two locally maintained
implementations were treated as stronger evidence than they were.

A1b should preserve the product model while replacing the contract-compilation
and immutable-authority foundations that made these failures likely.

---

## 3. Critical Newly Identified Contract Defect

A1 declares JSON Schema Draft 2020-12 as its schema dialect. The official JSON
Schema data model defines instance equality as follows:

- values must have the same JSON type;
- strings are equal only when they are equal codepoint-for-codepoint;
- numbers are equal when they have the same mathematical value;
- arrays compare item-for-item; and
- objects compare corresponding property names and values without property
  order significance.

See [JSON Schema Core section 4.2.2](https://json-schema.org/draft/2020-12/json-schema-core.html#section-4.2.2)
and [`uniqueItems` in the validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation.html#section-6.4.3).

Accepted A1 instead uses its identity-bearing canonical serializer for schema
`const`, `enum`, and `uniqueItems` equality. That serializer NFC-normalizes
strings and object keys. Current tests therefore require composed `"é"` and
decomposed `"e\u0301"` to compare equal during schema validation.

Those tests prove agreement between A1's canonical validator and generated
decoder, but both implementations disagree with the declared Draft 2020-12
string-equality contract. No documented A1 extension vocabulary explicitly
redefines JSON Schema instance equality.

The local evidence is the
[identity serializer](../../../../tools/standards_metadata/standards_metadata/serialization.py),
[contract validator](../../../../tools/standards_engine/contracts/validate_contracts.py),
[contract generator](../../../../tools/standards_engine/contracts/generate_contract.py),
and [generated-contract differential tests](../../../../tools/standards_engine/tests/test_generated_contract.py).

This exposes a deeper ownership error:

```text
JSON Schema instance equality
        !=
A1 identity canonicalization
```

Identity canonicalization may intentionally normalize strings when computing
an A1 identity. Schema validation must use the equality rules of the selected
schema dialect unless A1 declares and versions a custom vocabulary that
explicitly changes those rules. A1b must separate these two domains.

The A1b plan must reproduce this defect before correction and treat it as a
blocking contract finding. A2 cannot rely on A1 validation while the declared
dialect and executable behavior disagree.

---

## 4. Problem Inventory

### 4.1 Declaration authority was mistaken for semantic authority

The canonical JSON Schema was called the sole machine authority, but several
implementations interpreted it:

- the contract validator;
- the Python generator;
- the generated decoder;
- canonical serialization and equality helpers;
- internal analysis-domain models;
- public Standards Engine result adaptation;
- agent-tool projection; and
- acceptance fixtures.

One authoritative declaration does not create one executable semantic owner.
When multiple interpreters independently implement the declaration, their
agreement must be proved against the external contract and against every
supported semantic feature.

### 4.2 Generation was initially partial

Earlier candidates generated field names while omitting types, defaults,
constraints, nested variants, complete result shapes, or native result
classes. Later candidates added those properties incrementally.

The design lacked a mechanically enforced definition of the complete reachable
public contract closure. A generator could therefore be fresh relative to its
own incomplete algorithm while still omitting schema-owned meaning.

### 4.3 Equality and validation semantics were duplicated

Python equality, custom type-sensitive equality, canonical serialization, and
JSON Schema equality were used at different repair stages. This caused or hid:

- Boolean/integer confusion;
- Unicode normalization disagreement;
- `uniqueItems` disagreement;
- `const` and `enum` disagreement; and
- regular-expression full-match versus search behavior.

Repair V eliminated disagreement between two local implementations but did not
compare either implementation with the declared external dialect.

### 4.4 Immutable handles did not imply immutable authority closure

Snapshot-bound reads could reach live worktree bytes. Cold-process child
inspection could depend on instance caches, fresh providers, or fresh execution
authorization rather than immutable persisted state.

The interface promised immutability and reconstruction, but the implementation
still possessed ambient capabilities that could violate the promise.

### 4.5 Public result ownership was porous

Native `prepare` and `resolve` paths returned analysis-domain result classes
after the canonical schema was supposed to own public result shapes. Generated
code also imported an internal metadata module instead of the documented public
package entry point.

The public interface existed in documentation, but package structure and tests
did not initially make crossing that interface difficult.

### 4.6 Acceptance oracles were incomplete

Examples include:

- negative plan fixtures that failed before reaching their claimed defect;
- diagnostic substring matching instead of complete expected output;
- a differential matrix that covered Unicode but omitted Boolean/integer cases;
- generated freshness being counted as semantic conformance; and
- two locally maintained implementations serving as each other's oracle.

### 4.7 Routed standards were incomplete

The A1 plan selected Architecture, Contracts, Verification, Tooling, and
Persistence, but omitted at least:

- Build, despite changing generators and generated outputs;
- Library, despite creating reusable Python packages; and
- Dependencies, despite choosing to implement a JSON Schema subset rather than
  adopt an established implementation.

IPC applicability also needs an explicit decision for independently consumed
agent-tool messages. The current Router points generated host-language APIs to
the Language Binding profile, while that profile's own applicability requires a
native library exposed to another language. Generic schema-to-language
generation does not fit that wording cleanly.

### 4.8 Repair remained too local after systemic findings

Once a duplicated equality implementation, incomplete generator, ambient
authority source, or invalid oracle was found, the next review should have
audited the entire owning seam. Instead, several repairs addressed the latest
reported example and exposed a sibling defect in the next review.

### 4.9 Semantic policy coverage is incomplete

Current stable policy-unit declarations cover Planning and Commit extensively
but do not yet give Contracts, Architecture, Build, Library, Persistence,
Dependencies, or generated-contract policy the same heading-scoped identity
and consumer coverage.

A normative change to these owners can conservatively produce whole-artifact
work, but current policy-impact traversal cannot yet identify all precise
consumers needed for this recovery. The standards recovery must add that
authority before relying on A1b-generated reading or impact plans.

---

## 5. Standards Recovery Requirements

Create and independently accept a standards-recovery plan before creating the
A1b implementation plan. The recovery plan should address the following policy
changes as one coherent standards outcome, while allowing implementation slices
only where they provide independent acceptance or risk reduction.

### 5.1 Evidence-oracle policy

Activate the relevant part of the previously deferred Plan B work before A1b.
Verification should establish these rules:

- Evidence may claim only a property its observation mechanism can decide.
- An expected property needs authority independent of the subject being tested.
- Agreement between two projections derived from the same faulty semantic
  implementation proves consistency, not external conformance.
- Deterministic generation proves freshness, not semantic completeness.
- Exact literals prove literal identity only when literal identity is the
  contract.
- A negative fixture must satisfy all unrelated preconditions and prove that
  the intended diagnostic or failure point was reached.
- Coordinated updates to a subject and its copied expected literal do not
  independently establish correctness.
- Mutation evidence proves detection of the sampled mutation, not completeness
  outside the sampled domain.
- Property and differential tests must identify the property, input domain,
  independent oracle, and unsupported domain.

Recommended stable policy units include:

- `workflow.verification.evidence-oracle-boundary`
- `workflow.verification.negative-fixture-isolation`
- `workflow.verification.differential-evidence`

The final identities and heading placement belong to the standards-recovery
plan.

### 5.2 Generated-contract semantic conformance

Add a generic generated-contract rule owned by Contracts and a corresponding
boundary profile if profile-specific routing remains useful. Do not stretch the
Language Binding profile to cover generation that has no native/foreign
language interface.

The policy should require:

- one canonical declaration authority;
- one identified executable semantics owner for each supported keyword or
  extension;
- an exact dialect and vocabulary declaration;
- an exact supported keyword and annotation inventory;
- complete traversal of every definition reachable from a public operation;
- preservation of types, fields, requiredness, optionality, defaults,
  constraints, discriminants, variants, ordering, normalization, equality, and
  typed failures selected by the destination contract;
- deterministic generation and stale-output rejection;
- public producer and consumer evidence through the actual package entry
  points;
- explicit separation between source freshness, shape agreement, semantic
  agreement, and user-path behavior; and
- rejection of unsupported schema behavior instead of partial generation.

When several executables interpret one schema, require conformance to an
independent reference or official test corpus for the supported dialect. Local
implementations may additionally be compared with each other, but they cannot
serve as the only oracle.

Recommended stable policy units include:

- `topic.contracts.generated-semantic-conformance`
- `topic.contracts.schema-dialect-and-vocabulary`
- `topic.contracts.identity-versus-instance-equality`

The Router should select a new generic Generated Contract profile when a schema
or generator produces program-facing models, validators, tool definitions,
bindings, configuration, or another consumed representation. The profile should
require Core, Verification, Contracts, and Build. Language Binding should
specialize it only when an actual native/host or cross-language boundary exists.

### 5.3 Immutable authority closure

Architecture should make this state invariant explicit:

> An immutable, replayable, or inspectable handle binds the complete transitive
> authority closure needed to reproduce every advertised result. Resolution
> from that handle cannot depend on ambient mutable state, an instance-local
> cache, the originating process, undeclared providers, or fresh authorization.

Persistence should continue to own reopening through real store adapters.
Contracts should own handle versioning and stale or unsupported representations.
Verification should require post-capture mutation and cold-process
reconstruction through the public interface.

Recommended stable policy unit:

- `topic.architecture.immutable-authority-closure`

### 5.4 Implementation-versus-dependency decisions

Extend Dependencies applicability to include a decision to implement rather
than adopt an established implementation for difficult standardized semantics,
including schemas, protocols, parsers, serializers, cryptography, scheduling,
and similar domains.

The decision must compare:

- required semantic surface;
- candidate conformance and compatibility;
- official or independent test support;
- supported targets and licenses;
- update and security ownership;
- implementation and long-term maintenance cost;
- extension and failure behavior; and
- the cost of keeping a local subset correct.

A recorded decision that merely states that a dependency is undesirable is not
sufficient.

Recommended stable policy unit:

- `topic.dependencies.implementation-versus-dependency`

### 5.5 Systemic-finding re-planning

Planning should distinguish an isolated defect from evidence that an owning
seam or semantic family is incomplete.

When a finding reveals duplicated semantic authority, incomplete projection,
ambient authority, a public/internal leak, or an invalid oracle, re-planning
must:

1. identify the invariant family;
2. inventory every implementation and consumer of that invariant;
3. inspect sibling operations and representations;
4. replace local example-by-example acceptance with a class-level acceptance
   claim; and
5. admit the next repair only after the complete audit has dispositions.

Recommended stable policy unit:

- `workflow.planning.systemic-finding-replan`

### 5.6 Router correction and routing-completeness evidence

Add a Router fixture for this observable scenario:

> A reusable Python package consumes a JSON Schema, generates Python result
> models and agent-tool definitions, validates structured messages, persists
> immutable content-addressed state, and exposes results to an independent tool
> consumer.

The expected route should account for:

- Core and Router;
- Planning, Implementation, Verification, Documentation, Build, and Tooling;
- Architecture, Contracts, Dependencies, and applicable Diagnostics/Security;
- Library;
- the generic Generated Contract profile;
- Persistence; and
- IPC only when the actual process or independent-deployment facts select it.

Language Binding applies only when the selected design has a genuine
native/host or cross-language representation.

Planning and implementation entry points should consume this route rather than
copying a static list. Missing required routing remains unresolved or invalid;
it cannot silently produce a smaller reading plan.

### 5.7 Policy-unit and semantic-consumer migration

Create stable policy-unit declarations for every new or materially changed
heading. Audit prior and current graph state before adding relationships.

At minimum, review these consumer families:

| Policy owner | Consumer families to audit |
| --- | --- |
| Evidence-oracle policy | Verification suites, declarative fixtures, plan checkers, documentation projections, prompts, and acceptance reports |
| Generated-contract conformance | Router, Build, Tooling, Language Binding, generated outputs, schema validators, generators, package facades, and contract tests |
| Identity versus instance equality | Canonical serializer, schema validator, generated decoder, identity fixtures, applicability values, and persisted handles |
| Immutable authority closure | Snapshot providers, snapshot stores, analysis-state stores, inspection paths, authorization/provider views, and cold-process tests |
| Implementation-versus-dependency | Router, Planning prompts, ADR expectations, dependency fixtures, and toolchain manifests |
| Systemic-finding re-plan | Planning prompts, implementation prompts, plan templates, issue records, and plan lifecycle fixtures |

Each selected consumer receives `updated`, `reviewed-no-change`,
`not-applicable` with a reason, or `blocked`. A discovered permanent dependency
becomes authoritative metadata, followed by reanalysis from the changed tree.

An empty result is acceptable only when current consumer coverage proves it is
complete.

### 5.8 Standards recovery acceptance

The standards recovery is accepted only when:

1. every changed policy has a stable identity and exact locator;
2. prior and current policy-impact relationships have been compared;
3. every selected consumer has a complete disposition;
4. Router applicability and non-applicability fixtures pass;
5. prompts, templates, documentation, fixtures, and executable support agree;
6. evidence-oracle fixtures distinguish valid and invalid oracles;
7. generated-contract fixtures distinguish freshness, shape, semantics, and
   public-path evidence;
8. immutable-authority fixtures require cold-process reconstruction;
9. no acceptance relies on old plan narration or copied expected prose;
10. current registered verification passes from one clean exact tree; and
11. an independent review accepts the exact standards implementation tree.

Only that acceptance may activate A1b planning.

---

## 6. A1b Design

### 6.1 Preserve the deep external module

The caller-facing Standards Engine should remain a deep module. Unless A1b
planning finds a concrete incompatible requirement, preserve the conceptual
interface:

```python
query(snapshot, request) -> NavigationResult | RejectedResult
prepare(request) -> AnalysisResult | RejectedResult
resolve(analysis, submission) -> AnalysisResult | RejectedResult
inspect(handle) -> InspectionResult | RejectedResult
```

Callers should continue to use canonical IDs and opaque handles without knowing
repository paths, graph providers, schema traversal, persistence layout, or
internal analysis types.

The facade is the external seam and the primary behavioral test surface.

### 6.2 Introduce one deep contract-compilation module

Create one pure in-process module, provisionally called
`standards_contracts`, that owns executable contract semantics below the
facade. The final package name belongs to the A1b ADR.

Its small conceptual interface is:

```python
contract = compile_contract(schema_source, dialect)
value = contract.decode(definition_id, unknown_value)
json_value = contract.to_json_value(definition_id, value)
projections = contract.generate(selected_targets)
```

The module hides:

- dialect and vocabulary loading;
- reference resolution;
- normalized contract intermediate representation;
- supported-keyword validation;
- runtime instance validation;
- public-definition reachability;
- immutable model construction;
- generated projection construction;
- exhaustive variant metadata; and
- conformance diagnostics.

Do not expose internal schema walkers or per-keyword helpers through the public
Standards Engine interface.

`to_json_value` above means conversion to the contract's ordinary JSON data
model. It does not produce identity bytes, normalize values for identity, or
define instance equality. Identity canonicalization belongs to its separately
versioned owner.

The A1b ADR must select one of these semantic mechanisms:

1. adopt a mature Draft 2020-12 implementation and build the A1 projection
   compiler over its validated results; or
2. own an explicitly limited dialect implementation that passes the applicable
   official JSON Schema tests and an independently reviewed local extension
   suite.

The first is the default recommendation. The second requires a recorded
Dependencies decision proving why ownership is justified.

Generated models should contain representation and construction mechanics, not
an independent implementation of JSON Schema semantics. Runtime validation
should use the selected contract program before constructing a public model.
If runtime schema parsing is unacceptable, compile the schema into an immutable
generated contract program and prove that the program is semantically
equivalent to the selected dialect implementation.

### 6.3 Separate three equality domains

A1b must name and independently own:

| Equality domain | Governing contract |
| --- | --- |
| JSON Schema instance equality | Selected schema dialect and vocabularies |
| A1 domain-value equality | Applicability or analysis policy when it intentionally differs from JSON Schema |
| Identity canonicalization | Versioned A1 identity and serialization contract |

Do not reuse identity bytes as schema equality merely because they are
deterministic. Do not use Python equality as any of these domains without a
proof that Python's behavior exactly implements the selected contract.

If A1 intentionally wants NFC-equivalent values to collapse in applicability
sets, declare that as an A1 domain contract outside JSON Schema validation. The
schema may still validate the serialized representation under Draft 2020-12.

### 6.4 Introduce one immutable authority repository

Create a deep module that owns content-addressed snapshot and analysis-state
storage, provisionally called the immutable authority repository.

Its conceptual responsibilities are:

```python
snapshot_handle = capture(source_adapter)
snapshot = load_snapshot(snapshot_handle)
analysis_handle = store_analysis(analysis_state)
analysis = load_analysis(analysis_handle)
artifact = inspect_handle(any_supported_handle)
```

The module must guarantee:

- every stored object is immutable and content-addressed;
- each handle identifies its exact schema and semantic contract versions;
- the stored object graph includes the complete transitive authority closure
  needed for every advertised read and inspection;
- later worktree or provider mutation cannot change a result for an issued
  handle;
- a fresh process can reconstruct and inspect every public handle;
- caches are disposable accelerators and never authority;
- source providers run only during explicit capture;
- evidence and authorization providers run only during state construction or
  transition, not reprojection; and
- corrupt, missing, old-version, or incomplete object graphs return the exact
  typed outcome selected by the contract.

Git-tree and manifest capture are adapters at the source-capture seam.
In-memory and directory-backed stores are adapters at the persistence seam.
These are real seams because production and test/local implementations have
different mechanisms under the same observable contract.

After capture, engine operations should not possess a repository path or live
source-provider capability. Make the invalid ambient-read state difficult to
represent rather than relying on call-site discipline.

### 6.5 Use one public request and result algebra

The Standards Engine package should export only the schema-governed public
request, result, handle, submission, and rejection types.

Internal analysis modules may use domain-specific types, but they remain inside
the implementation. A single exhaustive adapter converts an internal outcome
to the public algebra. The adapter should be generated or mechanically checked
from the complete public result closure, and an unhandled variant should fail
generation or verification.

Every public operation test must call the package's documented entry point and
assert the exported public result class. Tests of internal analysis types do not
prove the facade contract.

Add import-graph verification that generated output and facade code depend only
on documented package entry points. Internal package imports are invalid even
when runtime behavior is otherwise correct.

### 6.6 Keep domain modules independent

Preserve these ownership directions unless A1b analysis disproves them:

- `graph_engine` owns domain-neutral topology and traversal;
- `standards_metadata` owns canonical corpus and policy-unit metadata;
- `standards_applicability` owns applicability-language semantics;
- `standards_policy_impact` owns typed policy-impact compilation;
- `standards_graph` composes standards graph providers;
- `standards_analysis` owns standards-change analysis and immutable state
  transitions;
- the contract-compilation module owns executable schema semantics and
  generated contract projections;
- the immutable authority repository owns snapshot/state persistence and cold
  reconstruction; and
- `standards_engine` composes those modules behind the caller interface.

Canonical identity serialization may move out of `standards_metadata` if the
dependency audit shows that its meaning is broader than metadata. If moved,
place it in the narrowest neutral owner that can be consumed without cycles and
perform one atomic consumer migration. Do not add a forwarding compatibility
wrapper without a real consumer requirement.

### 6.7 Keep plan lifecycle mechanics outside A1b runtime

The plan-checker oracle defects require standards and verification repair, but
A1b should not absorb plan lifecycle authority into the Standards Engine
runtime. A separate future change may replace Markdown lifecycle parsing with
structured authority if its own plan proves that need.

A1b should consume only the accepted standards and contract artifacts required
for its runtime objective.

---

## 7. Contract And State Migration

Before choosing compatibility behavior, inventory every current consumer of:

- Standards Engine public Python imports;
- generated Python models;
- agent-tool definitions;
- A1 schema definitions and examples;
- snapshot handles;
- analysis handles and persisted analysis states;
- certificate and inspection handles;
- identity domains and canonical serialization;
- directory-backed state; and
- current validator and generator commands.

Classify each as:

- internal coordinated;
- public versioned;
- persisted;
- independently deployed; or
- disposable derived state with a proven reconstruction source.

If every consumer and retained state is repository-controlled, prefer one
coordinated breaking replacement. Remove the old runtime and generated
projection in the same accepted cutover. Do not add dual decoders, dual writes,
fallback equality, or indefinite aliases.

If retained external or persisted consumers exist, define an explicit version
and migration contract before implementation. Old handles must never be
interpreted under new semantic versions. Return typed `unsupported` for an old
well-formed version unless an admitted migration owns its conversion.

A1b will likely require new versions for:

- the interface contract;
- schema/dialect semantics;
- snapshot identity when bound semantic contracts change;
- analysis identity when validation or authority closure changes; and
- persisted state representation if object closure changes.

The plan must decide exact version changes from the consumer and identity audit.
This brief does not assign version numbers.

---

## 8. Recommended Planning And Implementation Sequence

### Phase 0: Preserve and reproduce

- Record the accepted A1 commit and tree.
- Reproduce every historical A1 repair family.
- Add a focused reproduction showing that the current validator accepts
  canonically equivalent but codepoint-distinct strings for `const`/`enum` and
  rejects them as duplicates for `uniqueItems`.
- Compare the result with the official Draft 2020-12 equality contract.
- Record A2 as blocked by A1b.

Completion criterion: the exact current behavior, declared external contract,
and disagreement are independently reproducible without changing runtime code.

### Phase 1: Standards recovery

- Create and admit the standards-recovery plan.
- Implement sections 5.1 through 5.7.
- Run prior/current impact analysis.
- Complete every selected consumer disposition.
- Independently accept the exact standards tree.

Completion criterion: every standards-recovery acceptance item in section 5.8
is satisfied and no required consumer is blocked.

### Phase 2: A1b contract and dependency decisions

- Inventory consumers and retained state.
- Evaluate mature JSON Schema implementations and the local-ownership option.
- Select the dialect, vocabulary, extension, and dependency contracts.
- Define the three equality domains.
- Define the complete public-definition closure.
- Define immutable authority repository invariants.
- Produce a superseding A1b ADR and contract migration decision.

Completion criterion: an independent architecture and contract review accepts
the design and every unresolved decision in section 11 has an owner and result.

### Phase 3: Contract compiler

- Implement the selected contract-compilation module.
- Establish official or independent dialect conformance.
- Generate immutable public models and agent-tool projections from the complete
  reachable public closure.
- Prove stale-output detection, semantic mutation detection, and public
  producer/consumer behavior.
- Remove superseded validation and generation semantics in the same accepted
  cutover for this owner.

Completion criterion: one executable semantics owner governs every supported
schema feature, and no independent local validator or generated decoder
reimplements those semantics.

### Phase 4: Immutable authority repository

- Implement exact snapshot capture and content storage.
- Implement immutable analysis-state storage.
- Implement fresh-process reconstruction for every public handle.
- Make query, prepare, resolve, and inspect depend only on resolved immutable
  views after capture.
- Remove live-read and instance-cache authority paths.

Completion criterion: every public handle survives capture, persistence,
process destruction, reconstruction, and identical inspection; later source
mutation cannot affect it.

### Phase 5: Facade and public algebra cutover

- Convert every public operation to the generated public request/result
  algebra.
- Make result conversion exhaustive.
- Verify documented public imports and reject internal-package dependencies.
- Run real typed-agent route/read, prepare/resolve, and inspection workflows.
- Remove former public domain-result leakage and compatibility paths.

Completion criterion: every caller-visible operation and result crosses only
the documented facade, while internal modules remain replaceable behind it.

### Phase 6: Migration and deletion

- Apply the accepted coordinated replacement or explicit state migration.
- Reject unsupported old versions and handles according to the accepted
  contract.
- Remove superseded generators, validators, serializers, caches, adapters,
  fixtures, imports, and identity domains that have no retained consumer.
- Re-run consumer inventory and dependency inspection.

Completion criterion: one production path remains for each owned semantic
decision, and every inventoried predecessor has a disposition.

### Phase 7: A1b acceptance

- Run focused contract, store, facade, and migration claims.
- Run current broad repository verification.
- Verify exact generated freshness and semantic conformance independently.
- Record the exact implementation commit and tree.
- Obtain independent Standards and specification review.
- Publish an A1b acceptance report without rewriting prior A1 history.

Completion criterion: every criterion in section 9 is satisfied at one clean
exact tree. Only then may a separate review consider A2 admission.

---

## 9. A1b Acceptance Criteria

A1b is complete when:

1. The selected schema dialect and vocabularies are explicit and executable.
2. Draft 2020-12 behavior agrees with the applicable official test corpus or a
   separately maintained reference implementation across every supported
   keyword.
3. Codepoint-distinct Unicode strings remain distinct for JSON Schema instance
   equality unless an explicit custom vocabulary owns different semantics.
4. Identity normalization is separately versioned and never reused implicitly
   as schema equality.
5. Boolean and numeric values follow the selected JSON Schema data-model
   equality and type rules.
6. `pattern` and every other supported keyword follow the selected dialect.
7. Every public definition reachable from query, prepare, resolve, and inspect
   is represented by the generated public algebra.
8. Generator freshness, shape conformance, semantic conformance, and public
   workflow claims are separately evidenced.
9. Public operations return only documented generated result types or typed
   rejections.
10. Generated and facade code import dependencies only through documented
    package entry points.
11. Every snapshot read uses immutable captured bytes.
12. Every advertised handle can be reconstructed and inspected in a fresh
    process without live source, execution providers, or instance caches.
13. Post-capture source mutation cannot change results for an issued handle.
14. Caches can be deleted without changing observable results.
15. Missing, corrupt, incomplete, and unsupported stored objects return their
    declared typed outcomes.
16. Old handles and states are migrated or rejected under one explicit
    versioning decision.
17. No dual validator, equality, serializer, generated-model, or state-authority
    production path remains without an actual retained consumer.
18. Existing A1 route/read, related, prepare/resolve, impact, coverage, and
    inspection behavior remains satisfied except for explicitly superseded
    semantics.
19. Every standards and runtime consumer inventory row has a disposition.
20. Current focused and broad verification passes from one clean exact tree.
21. Independent review reports no unresolved blocking Standards or
    specification finding.
22. A2 remains inactive until that acceptance is committed.

---

## 10. Required Behavioral Scenarios

The A1b plan should include at least these claim-directed scenarios.

### Contract semantics

- Boolean supplied for integer `const` and `enum` authority.
- Integer supplied for Boolean `const` and `enum` authority.
- Mathematically equal JSON numbers where the supported data model permits
  them.
- Composed and decomposed Unicode strings under JSON Schema equality.
- Composed and decomposed Unicode strings under identity canonicalization.
- Object key order under JSON Schema equality.
- Array order under JSON Schema equality.
- `uniqueItems` across null, Boolean, number, string, array, and object values
  supported by the contract.
- Non-anchored regular-expression matching.
- Every supported string, numeric, array, object, composition, reference, and
  annotation keyword.
- Unsupported keyword, dialect, vocabulary, and extension.
- A schema mutation for each supported semantic feature that changes the
  compiled result and affected public behavior.

### Generated closure and facade

- Every operation input and result variant.
- Every nested request, submission, handle, inspection, and rejection variant.
- Required, optional, defaulted, constant, constrained, and extra-field rules.
- Public `query`, `prepare`, `resolve`, and `inspect` return classes.
- Exhaustive text rendering where retained.
- Agent-tool projection through the real tool consumer.
- Stale generated output after source or compiler changes.
- Internal-package import introduced into generated output.

### Immutable authority

- Clean Git, dirty Git, and non-Git capture.
- Tracked and untracked files, file modes, symlinks, gitlinks, nested state, and
  explicit exclusions.
- Worktree mutation after snapshot issuance.
- Source deletion after snapshot issuance.
- Fresh process with no original caches.
- Fresh process with no execution provider capability.
- Reconstruction of snapshot, navigation, analysis, context, fact requirement,
  fact observation, coverage, certificate, and other advertised handles.
- Corrupt or incomplete object graph.
- Unsupported stored schema or identity version.
- Cache deletion and deterministic reprojection.

### Evidence and migration

- A negative fixture that is otherwise valid and reaches exactly the intended
  diagnostic.
- A copied expected value that changes with the subject and therefore cannot
  serve as an independent oracle.
- Two local implementations that agree but disagree with the external
  reference.
- Old A1 handle with no supported migration.
- Representative retained state through an admitted migration, if retained
  state exists.
- Complete coordinated replacement when no retained consumer exists.

---

## 11. Decisions Required Before A1b Coding

Resolve these questions explicitly in the A1b plan and ADR:

1. Is the contract truly JSON Schema Draft 2020-12, or a named A1 dialect with
   explicit custom vocabularies?
2. Which vocabularies and keywords are supported?
3. Which external implementation and official test corpus are authoritative
   conformance references?
4. Will A1b adopt an established validator or own a local subset, and why?
5. Which behaviors belong to schema instance equality, A1 domain equality, and
   identity canonicalization?
6. Does A1 identity still require NFC normalization, and for which fields?
7. Where should canonical identity serialization live after dependency review?
8. What is the smallest interface of the contract-compilation module?
9. What exact object closure must each public handle retain?
10. Which source and persistence adapters are real variants?
11. Which current A1 states and handles have actual retained consumers?
12. Is replacement internal-coordinated, persisted, public-versioned, or
    independently deployed?
13. Which contract and identity versions must change?
14. Are agent-tool calls an IPC or independently deployed contract in the real
    execution topology?
15. Which generated or runtime paths can be deleted atomically?
16. Which policy-unit IDs and semantic relationships own the standards
    recovery?
17. Which evidence is independent enough to accept dialect conformance?
18. Which exact tree must A1b preserve as the migration base?

An unresolved material answer blocks implementation. Do not select a convenient
default or preserve the current mechanism merely because it exists.

---

## 12. Risks And Guardrails

- Do not patch the Unicode case alone. It demonstrates equality-domain
  conflation and requires a complete semantic audit.
- Do not call a custom dialect Draft 2020-12 while changing core equality or
  vocabulary semantics implicitly.
- Do not replace two local validators with a third local validator and use
  agreement as acceptance.
- Do not generate validation logic independently into every model.
- Do not expose schema walkers, persistence adapters, or store layout through
  the Standards Engine interface.
- Do not preserve live repository access after snapshot capture.
- Do not use an in-memory cache as cold reconstruction authority.
- Do not add ports for hypothetical adapters; use internal seams unless two
  real adapters exist.
- Do not retain old and new contract paths without an inventoried consumer and
  explicit lifecycle.
- Do not infer migration authority from checked-in old states.
- Do not make A1b a vehicle for controlled authoring, external-project
  baselines, arbitrary semantic judgment, or a graph-engine rewrite.
- Do not mark standards recovery or A1b accepted from implementation-owned
  evidence alone when independent acceptance is required.
- Do not advance A2 because implementation is mostly complete; A1b's exact
  acceptance is its prerequisite.

---

## 13. Required Deliverables

The complete recovery should produce:

1. A standards-recovery plan with exact policy and graph write sets.
2. Accepted standards changes for evidence oracles, generated contracts,
   immutable authority closure, dependency selection, systemic re-planning,
   and Router applicability.
3. Stable policy-unit declarations and audited policy-impact relationships.
4. Standards fixtures and executable enforcement for the new policies.
5. A standards-recovery independent acceptance report.
6. An A1b consumer and retained-state inventory.
7. An A1b plan with exact lifecycle, milestones, gates, and next slice.
8. A superseding A1b ADR and contract/version migration decision.
9. A contract dialect and conformance report.
10. A contract-compilation module with generated public projections.
11. An immutable authority repository with cold-process evidence.
12. One coordinated facade and public-algebra cutover.
13. A predecessor-removal or retained-state migration report.
14. An exact-tree A1b candidate report.
15. An independent A1b acceptance report.

No deliverable in this list implicitly authorizes the next one. Follow the
accepted plan lifecycle at each transition.

---

## 14. Desired Outcome

After A1b, the system should retain A1's useful caller experience while making
its strongest invariants structural:

```text
canonical schema and explicit dialect
        -> one compiled semantic contract
        -> generated public algebra and tool projections
        -> one deep Standards Engine facade

captured source adapters
        -> immutable content-addressed authority repository
        -> reproducible snapshot and analysis views
        -> query / prepare / resolve / inspect
```

The redesign succeeds when a caller can use the same small Standards Engine
interface while maintainers can replace schema, storage, or internal analysis
mechanisms at their own seams without duplicating meaning or weakening proof.

Only an independently accepted A1b boundary may become the prerequisite for
planning and admitting controlled authoring Plan A2.
