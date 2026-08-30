# Contract Evolution And Degraded Outcomes

**Standards metadata**

- ID: `topic.contracts`
- Role: `topic`
- Level: `MUST`
- Applies when: A change affects data or behavior consumed across a module, process, persistence, package, deployment, or generated boundary.
- Does not apply when: A private implementation detail has no independent consumer, stored representation, or externally observable promise.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Contract and runtime-decoding decision fixtures plus affected producer/consumer claims.
- Canonical owner: `topics/contracts.md`

## Record Contract Facts First

Before selecting compatibility or migration behavior, record:

- canonical producer and policy owner;
- actual consumers and their owners;
- whether producer and consumers deploy atomically or independently;
- whether values persist beyond one coordinated deployment;
- supported prior versions or data states;
- source of truth and whether substitutes preserve the same semantics; and
- public, regulatory, protocol, or platform promises outside repository control.

Unknown facts produce an unresolved-contract diagnostic. Do not select the most
compatible-looking default.

## Contract Artifact Necessity And Authority Placement

Create a contract artifact only when it has a distinct purpose that the
existing authoritative representation does not already satisfy. Valid purposes
include establishing independently consumed authority, enforcing a boundary
invariant, making invalid states unrepresentable, defining a distinct wire or
persistence representation, governing evolution, enabling deterministic
generation, or removing duplicated interpretation.

A DTO, projection, wrapper, schema, interface, or generated artifact that only
mirrors another shape is not justified without a distinct ownership,
validation, representation, evolution, or transport obligation. Convenience,
framework convention, symmetry, and possible future reuse are not sufficient
contract purposes.

Place canonical authority where every selected producer, consumer, validator,
and generator can depend on it without depending on an unrelated
implementation. This may be a dedicated package, an owned schema or generator
input, or a producer-owned module with an appropriate dependency boundary. A
dedicated package is not required when one owner and its consumers can access
the authority without cycles, duplicated definitions, or implementation
coupling.

Record the authority, purpose, consumers, derivation, invalidation, and
evolution class before introducing the artifact. Missing required facts or
authority is `unavailable`; an artifact that contradicts its authority or lacks
a distinct purpose is `invalid`; an unavailable required artifact mechanism is
`unsupported`. Do not fall back to an inferred mirror, duplicated schema,
unrelated implementation dependency, or speculative compatibility artifact.

## Declaration And Semantic Authority

A contract declaration owns only the representation and meanings selected by
its declared responsibility. Before treating one declaration as canonical for
several semantic families, identify the owner of each applicable family, such
as representation, validation, identity, authorization, state transition,
persistence, projection, and compatibility. The list is illustrative;
observable meaning and actual ownership select the families.

An annotation, extension, reference, generated model, or validator may project
or invoke semantics owned elsewhere without transferring that ownership to the
declaration. Record how each referenced owner is resolved and which executable
enforces its semantics. Do not create a second interpreter, redefine domain
policy as declaration metadata, or infer that declaration authority includes
every concern the artifact can describe.

One owner may legitimately hold declaration and executable or domain semantics
when they form one coherent responsibility. Distinct owners are also valid
when the dependency and projection are explicit. Missing semantic authority is
`unavailable`; contradictory authorities or an attempted ownership transfer by
annotation are `invalid`; a well-formed semantic family outside the supported
contract is `unsupported`.

## Version Scope And Invalidation

A version identifies one coherent compatibility or evolution promise. Record
the promise, authority, consumers, supported overlap, invalidation effect, and
the representations or behaviors it governs. Several concerns may share a
version only when they intentionally share that promise; independently
changing promises require independently scoped versions or an explicit version
record that preserves their separate identities.

Classify the role before adding or reusing a version-like value:

- a current-format discriminator rejects representations the current decoder
  does not support, without promising overlap with an older reader;
- an identity-domain revision changes the semantic identity or invalidation
  domain selected by its authority;
- a compatibility version governs producer-consumer combinations supported at
  the same time;
- a migration version identifies an admitted source-to-destination transition;
  and
- an allocation ordinal supplies uniqueness or ordering inside one authority
  and is not a compatibility promise.

One value may serve more than one role only when those roles have the same
authority, consumers, change reasons, and consequences. Similar names,
monotonic integers, shared storage, or simultaneous updates do not establish
that equivalence.

A common file, schema, model, package, generator, build, release, deployment,
or cutover may coordinate changes without creating one version scope. Do not
use an umbrella version to force unrelated consumers to migrate together or to
make an independently compatible concern appear changed.

Include a contract version in content identity, cache invalidation, persisted
handles, replay closure, or regeneration inputs only when a change to that
version can materially change the reproduced meaning. Representation-only
change does not invalidate semantic identity unless the selected contract
proves that effect. Record that proof rather than coupling every available
version defensively.

Require a compatibility matrix only for producer, consumer, and persisted-state
combinations the selected contract actually promises concurrently. An atomic
coordinated replacement needs a fail-closed current-format decision, not a
historical compatibility matrix by default. Do not infer retained readers,
cross-engine migration, or every pairwise version combination from hypothetical
consumers or from the presence of several version-like fields. Each admitted
overlap names its owner, evidence, retirement condition, and cumulative support
cost.

Missing promise, consumer, or invalidation facts are `unavailable`;
contradictory scopes or identity coupling to an unrelated version are
`invalid`; and a well-formed version outside the supported promise is
`unsupported`. Do not fall back to lockstep increments, broad cache busting, or
the version already present on a containing artifact.

## Producer-Consumer Semantic Preservation

A structured contract governs every meaning selected by its canonical
authority, not only field names or readable representation. Record which shape,
optionality, discriminants, defaults, constraints, identifiers, ordering,
labels, descriptions, and compatibility behavior affect producer output,
consumer decisions, persisted identity, or operator action. A category is not
contractual merely because it appears in this list; authority and observable
use select the applicable semantics.

Each producer proves that its emitted value satisfies the selected contract.
Each consumer proves that it accepts and preserves the selected semantics it
uses. A projection, form, menu, runtime object, generated configuration, or
stored artifact is a new destination representation when it transforms those
semantics and must satisfy its own explicit destination contract.

A consumer may intentionally omit, transform, or reinterpret a source semantic
only when the destination contract authorizes that behavior and the affected
compatibility and persistence outcomes are explicit. Successful parsing,
matching field names, a producer test, documentation of the transformation, or
visual similarity does not prove destination conformance.

Missing authority, consumer facts, or destination contract is `unavailable`;
contradictory output, silently dropped selected meaning, or incomplete proof is
`invalid`; a well-formed source variant outside the destination support set is
`unsupported`. Do not fall back to inferred defaults, nearby labels, source
ordering, guessed enum meaning, omitted constraints, or the original source
representation when destination proof is absent.

## Generated Contract Semantic Conformance

A generated contract has one canonical declaration authority and one
identified executable semantics owner for every supported keyword, extension,
or construct. Inventory every public operation and traverse every definition
reachable from those operations. A generator that copies visible field names
but omits reachable variants or selected semantics is incomplete.

The destination representation preserves every meaning selected by its
contract, including applicable types, fields, requiredness, optionality,
defaults, constraints, discriminants, variants, ordering, normalization,
equality, and typed failures. Unsupported source behavior is rejected
explicitly; it is not partially generated or interpreted through a convenient
local subset.

Generate deterministically from the canonical declaration and reject stale
outputs. Prove generated freshness separately from shape agreement, semantic
agreement, and behavior through the actual public producer and consumer entry
points. A fresh artifact is not evidence that the generator implemented the
complete selected semantics.

When multiple executables interpret the same declaration, prove the supported
dialect against an independent reference or official conformance corpus.
Comparing the local executables remains useful consistency evidence but cannot
be the only external-conformance oracle.

## Schema Dialect And Vocabulary

Before implementing or generating from a schema, declare the exact dialect,
vocabularies, extensions, and supported keyword and annotation inventory.
Identify the authority and executable semantics owner for each supported
element, including traversal and reference behavior. A filename, media type,
schema-like shape, or parser success does not identify a dialect or support
set.

Reject an unknown required dialect, vocabulary, keyword, extension, or
reachable construct as `unsupported`. Return `unavailable` when the selected
authority or required conformance evidence cannot be obtained, and `invalid`
when an implementation claims support while omitting or contradicting selected
semantics. Do not infer support from nearby keywords, local examples, another
implementation, or the subset exercised by current fixtures.

## Identity And Instance Equality

Keep schema-instance equality, domain-value equality, and content-identity
canonicalization as separate contracts. Each equality relation declares its
owner, applicable types, normalization behavior, duplicate semantics, and
consumer purpose. A normalization selected for stable identifiers does not
change instance equality unless the schema or domain contract explicitly says
so.

Validators, generated decoders, identity serializers, applicability
evaluators, and persisted-handle implementations use the equality relation
owned by their selected contract. Agreement between two local implementations
does not establish that either matches an external schema dialect. Test
cross-type numeric and Boolean values, Unicode representations, collection
uniqueness, constants, and enumerations only where those cases belong to the
declared domain.

Contradictory equality authorities are `invalid`; a required relation outside
the supported dialect or domain is `unsupported`; and a missing equality
authority is `unavailable`. Do not reuse canonical identity bytes as a general
validation comparator or silently normalize values at a boundary whose
contract requires codepoint-preserving comparison.

## Runtime Decoding At Boundaries

When a value enters through a trust, process, persistence, plugin, queue, or
independently deployed boundary, treat its representation as unknown until an
executable decoder or smart constructor proves the applicable contract.

A validated value is a construction result, not a type annotation. Successful
parsing or deserialization proves only that a representation was readable. A
type assertion, generic object check, producer-side static type, or partial
field check cannot establish runtime validity.

Before constructing a validated value, check every invariant required by that
value, including those that apply:

- aggregate shape, required fields, optionality, and extra-field policy;
- discriminants and the complete selected variant;
- field domains, bounds, identifiers, and cross-field relationships;
- supported contract or schema versions; and
- explicit normalization and defaulting rules.

The decoder must return either the validated representation or a typed
diagnostic:

- `invalid` for malformed data, failed constraints, or incomplete proof;
- `unsupported` for a well-formed version or variant outside the supported
  contract; or
- `unavailable` when required decoding capability or contract material cannot
  be obtained.

The validated representation must not expose an unchecked mutable alias that
can invalidate the proof after construction. Passing the validated value
inward does not authorize reuse of the original unknown representation.

Values created and kept inside one trusted in-process boundary do not require a
redundant runtime decode when their constructor already enforces the same
invariants. Crossing a new applicable boundary, changing contract version, or
losing the validated representation requires decoding again.

Do not fall back to a cast, the original input, an alternate unchecked shape, a
permissive default, or a weaker decoder when proof is missing. No particular
schema or validation library is mandatory; the observable proof and typed
outcomes are.

## Inbound And Outbound Boundary Proof

Apply the complete applicable contract in both directions. Inbound validation
proves that unknown input may enter the owning boundary. Outbound validation
proves that a produced value may cross its destination boundary. Validation in
one direction does not prove the other direction, and successful transport,
serialization, parsing, or operation completion does not prove the value's
contract.

For inbound values, establish the runtime-decoding proof above before business
logic consumes the value. For outbound values, first classify the operation or
protocol outcome, then prove the complete destination representation before
emitting it or treating it as a successful result. Error, rejection, and
degraded representations have contracts too; do not parse or reinterpret one
as a successful payload merely because its representation is readable.

Code inside one trusted boundary consumes an intact proof-bearing
representation without redundant validation. A new destination, contract
version, representation, or trust boundary requires the proof applicable to
that crossing.

Return a typed boundary outcome that preserves the failed obligation:

- `invalid` when the representation or required invariants fail;
- `unsupported` when a well-formed outcome, version, or variant is outside the
  selected contract; or
- `unavailable` when required contract, decoding, encoding, or outcome
  classification capability is absent.

The owning protocol or adapter may specialize these outcomes into its declared
mechanisms. Contracts does not mandate HTTP status checks, exception throwing,
response wrappers, middleware, or a particular decoder. Do not treat a default
body, empty object, alternate parser, guessed status, successful transport, or
the original unchecked value as a valid fallback.

## Protocol Outcome Projection

Classify the authoritative operation outcome before projecting it through a
protocol. Record the outcome authority, applicable protocol and version,
supported outcome variants, status or control metadata, response
representation, disclosure decision, consumers, and evidence that each
projection preserves the selected meaning.

The selected protocol contract decides how an outcome is represented. A
transport-level success may carry a rejected application outcome only when that
is an explicit supported representation; a transport-level failure does not by
itself classify the operation. Status, headers or equivalent control metadata,
and body must describe one consistent selected outcome. Serialization,
readability, a status class, or a familiar envelope does not establish that
consistency.

Do not infer a universal mapping from outcome names to HTTP status codes or
other protocol controls. A protocol may define different mappings for
different operations, versions, consumers, or externally governed promises.
Likewise, no JSON envelope, human-readable message field, error code, empty
body, or response wrapper is a default. Security selects what may be disclosed;
Diagnostics selects reporting projections without changing the operation
outcome.

Return:

- `unavailable` when the authoritative outcome, protocol contract,
  representation, disclosure decision, adapter capability, or required
  evidence cannot be obtained;
- `invalid` when status, control metadata, body, or disclosure contradicts the
  selected outcome or representation; or
- `unsupported` when a well-formed outcome or representation has no supported
  projection in the selected protocol contract.

Do not guess a status or envelope, map an unknown failure to a default internal
error, treat transport success as operation success, expose raw diagnostic text,
switch representations or decoders, retry, recover, or emit a partial response
as a fallback. Illustrative HTTP mechanisms are isolated in the
[HTTP projection recipes](../reference/recipes/http.md).

## Protocol Adapter Proof

A producer adapter accepts an already authoritative operation outcome, selects
the exact operation and protocol-version projection, constructs its complete
response representation, proves status or control metadata, body, and
disclosure consistency, and only then emits the response. A shared error type,
middleware layer, exception mapping, or response wrapper is optional mechanism,
not outcome authority.

A consumer adapter treats the received response as unknown. It selects the
applicable operation and protocol-version contract, validates all required
status or control metadata, headers, content type, and body variant, constructs
the validated outcome representation, and only then exposes that outcome to its
caller. Checking status before body, body before status, or both in one decoder
is a mechanism decision; neither status nor body alone proves the outcome when
the selected contract requires both.

Producer and consumer proof must agree on every selected variant, including
success, rejection, failure, empty, and degraded responses. A protocol may
explicitly represent an application error through successful HTTP transport;
that is valid only when producer and consumer contracts select and prove the
same representation. Conversely, a status convention cannot hide a body that
contradicts it.

Adapters do not select disclosure, diagnostic reporting, retry, recovery, or
degradation policy. Security owns disclosure, Diagnostics owns reporting
projection, Resilience owns retry and recovery, and Verification owns claims
that clients, intermediaries, or monitoring systems interpret the projection.

Return `unavailable` when the adapter, mapping, decoder, disclosure decision,
consumer facts, or evidence is absent; `invalid` for incomplete proof,
contradictory response parts, unsafe disclosure, duplicate or partial emission,
or a false interpretation claim; and `unsupported` for a well-formed response
variant outside the selected contract.

Do not substitute a generic error, raw message, default internal-error mapping,
status-only or body-only interpretation, alternate decoder, successful
transport, retry, recovery, or duplicate response. Preserve the typed outcome
when complete adapter proof cannot be established.

## Validation Proof Lifetime

Validation authority belongs to the proof-bearing representation produced by
the applicable decoder or smart constructor, not to the fact that validation
happened earlier. Record the complete contract and version whose invariants the
representation establishes.

The proof remains authoritative only while the validated representation is
retained, its invariants cannot be changed through an unchecked alias, the
applicable contract is unchanged, and the value remains inside the boundary
for which that proof applies. Code inside that boundary consumes the validated
representation directly; it does not decode the same unchanged value again.

Establish new proof after the validated representation is lost, after unchecked
mutation, when the applicable contract or required invariants change, or when
the value crosses a new trust, process, persistence, plugin, queue, or
independently deployed boundary. The new boundary applies its complete current
contract to the current input; validation of a prior value or representation
does not carry forward.

A boolean validation flag, validation-history record, type annotation, or
equality with a previously validated value is not a validated representation.
Missing capability returns typed `unavailable`; a well-formed unsupported
contract returns `unsupported`; failed proof returns `invalid`.

Do not fall back to the original unknown input, stale proof, unchecked mutable
alias, implicit trust across a new boundary, permissive defaults, or a weaker
decoder. Do not discard an intact proof-bearing representation merely to
mandate redundant validation.

## Invariant Contracts

State each material invariant as an observable contract owned by the value,
operation, state transition, or boundary that must preserve it. Record the
applicable domain, required state, and the transitions that may establish,
preserve, or invalidate it.

Preconditions describe facts a caller or upstream owner must establish before
an operation. Postconditions describe facts the operation guarantees on each
declared outcome. Internal assumptions are not preconditions unless a real
caller can establish and verify them. Do not transfer an implementation
obligation to a caller merely to simplify the implementation.

Select enforcement points from the invariant's authority, corruption impact,
trust boundary, mutation paths, and proof lifetime. Construction, transition,
boundary, persistence, and read-time checks are different decisions. Build
mode alone does not decide which invariants remain enforced, and successful
earlier validation does not authorize stale proof.

Document an invariant when its owner, meaning, enforcement point, invalidation,
or failure outcome is not evident from the type and implementation. Keep the
contract with its canonical owner; do not require a copied comment template or
repeat the same authority at every call site.

Verification selects evidence that can prove the invariant and its relevant
failure mode. Evidence may be a focused example, property check, model,
contract fixture, integration path, static proof, or other objective-aligned
method. Do not require one test per sentence or infer adequate evidence from a
test name.

Before selecting a violation outcome, classify its source and reachable
consequence. Distinguish arbitrary or adversarial input, operational failure,
a contained programming defect, invalid state that can escape through a public
or trust boundary, and corruption of authoritative state. Select rejection,
immediate failure, a typed public outcome, recovery, or another mechanism from
that classification and the owned operation contract; no mechanism is
universally correct for every invariant.

Immediate failure with trace-led diagnosis is valid for a contained
programming defect when it prevents invalid state from escaping or corrupting
authority and no public, availability, or recovery contract requires another
outcome. Arbitrary or adversarial input must follow its boundary and Security
contract. Operational failure, escaping invalid state, and authoritative-state
corruption preserve their selected typed outcome or recovery obligation; a
diagnostic alone cannot satisfy those contracts.

An invariant violation is `invalid`. Missing authority, classification,
enforcement capability, selected outcome, or required evidence is
`unavailable`; a well-formed contract variant outside the supported set is
`unsupported`. Do not substitute debug-only enforcement, logging without the
selected outcome, silent corruption, an unchecked state, or a weaker
invariant. Panic, recovery, rejection, or graceful termination is valid only
when it is the selected outcome rather than a fallback.

## Contract Classes

| Class | Required evolution policy |
| --- | --- |
| `internal-coordinated` | Replace producer and all consumers atomically. Remove the old shape in the same change; do not add a compatibility shim. |
| `persisted` | Define supported source states, migration or rejection behavior, rollback/data-retention needs, and round-trip evidence. |
| `public-versioned` | Follow the published compatibility and versioning promise; deprecate or version when independent consumers need overlap. |
| `distributed-independent` | Negotiate or explicitly reject versions because producer and consumer deployments may overlap. |
| `generated` | Change the canonical source and generator, regenerate deterministically, and verify producer/consumer consistency. |

A boundary may have more than one class. For example, a generated public binding
requires both generated-source consistency and the public versioning promise.

## Cross-Language Contract Selection

Using more than one implementation language does not select a compatibility
policy or make either implementation authoritative. Apply every applicable
contract class, then record one canonical authority for the effective wire or
schema contract. The authority may be a schema, protocol specification,
generator input, or explicitly owned producer contract; serializer defaults
and a consumer's inferred shape are not authorities.

For an `internal-coordinated` contract, update the authority, producer, and
every consumer atomically and remove the rejected representation in the same
change. For a `generated` contract, update the canonical source and generator
before regenerating every affected producer and consumer. For a `persisted`,
`public-versioned`, or `distributed-independent` contract, follow its declared
migration, compatibility-window, or negotiation policy and reject unsupported
versions explicitly. Cross-language use does not justify dual reads, dual
writes, guessed schemas, or an indefinite old-shape path.

For language bindings, classify each affected artifact independently: native
adapter API, canonical generator input, generated source, host package, native
package, stable ABI, wire representation, and persisted representation. One
release may coordinate several artifacts, but a shared release input or
version identifier does not give them one compatibility promise.
Common build or release provenance may establish source-to-artifact
consistency evidence; it does not select a compatibility class, compatibility
window, or lockstep version relationship.

Select canonical generation authority from the applicable contract: an owned
schema or protocol, declared generator input, or explicitly owned producer
contract. A compiled implementation artifact, source annotation, generated
consumer output, or whichever input a framework accepts is not canonical by
default. When generation applies, record the authority, generator capability,
affected outputs, deterministic derivation, and producer/consumer consistency
evidence before producing or publishing an output.

Regenerate only affected outputs when their canonical generation input or
generator changes. An unrelated private implementation change does not require
regeneration. When regeneration applies, update the canonical input and
generator first, derive every affected output deterministically, and verify
each supported producer/consumer path. Do not hand-edit generated output or
regenerate from inferred consumer shape.

Select shared or independent artifact versions from actual publication,
deployment, package-resolution, and consumer compatibility contracts. Do not
force native libraries and host packages into lockstep or independent versions
without those facts. A syntactically additive change is compatible only when
every applicable consumer contract permits it; exhaustive variants, required
behavior, defaults, fields, generated APIs, persisted state, and ABI or wire
representations may make it breaking.

Evidence must match the selected contract and deployment facts. Prove the
canonical authority, the producer's emitted representation, and each affected
consumer's accepted and rejected representations. Coordinated contracts
require complete producer/consumer evidence from the atomic change.
Independently deployed contracts require supported-version and
unsupported-version evidence across the promised overlap. Generated contracts
also require deterministic regeneration and source-to-output consistency.

Return `unavailable` when the canonical authority or required contract
capability cannot be obtained, `unsupported` when a well-formed version lies
outside the declared support policy, and `invalid` when the representation or
required producer/consumer proof does not satisfy the selected contract. Do
not guess from serializer defaults, preserve an old representation as a
compatibility shim, try a second shape, or report success with incomplete
consumer evidence.

## Coordinated Breaking Replacement

Breaking replacement is preferred when all consumers and persisted states are
owned and updated in one atomic deployment. The change must:

1. update the canonical producer and every consumer;
2. remove the rejected shape and execution path;
3. update fixtures and generated artifacts;
4. return typed diagnostics for stale or invalid input; and
5. verify the complete affected path.

Do not keep dead fields, adapters, aliases, dual reads/writes, or old runtime
paths merely because they existed.

## Persisted Evolution

Persistence requires compatibility only for data states the project actually
commits to retain. Define:

- supported source versions;
- ordered and transactional migration where applicable;
- idempotency or explicit one-shot preconditions;
- backup, rollback, and failure behavior;
- typed rejection for unsupported or corrupt states; and
- evidence using representative existing data.

Never delete or overwrite authoritative data as a recovery fallback. Rebuild is
valid only for explicitly disposable derived state whose authoritative source
and reconstruction procedure are known.

## Persisted Contract Artifacts

For a checked-in example, fixture, template, manifest, saved workflow, request,
response, or other persisted artifact derived from a schema, generator, or
producer contract, record the canonical authority, applicable contract version,
derivation method, intended consumers, and whether the artifact is authored
input, authoritative state, or disposable derived output.

Validation proves that the current artifact satisfies its applicable producer
and consumer contracts. Regeneration proves deterministic derivation from the
selected authority; it does not by itself prove that consumers accept the
result or that overwriting the prior artifact is authorized. When regeneration
is selected, preserve authored or authoritative inputs and verify every
affected consumer path before accepting the new output.

Return `invalid` when the artifact contradicts its selected authority or
consumer contract, `unsupported` when its well-formed version or variant is
outside the declared support set, and `unavailable` when the authority,
generator, decoder, consumer, provenance, or required evidence cannot be
obtained. Do not accept a stale artifact, infer authority from the checked-in
shape, regenerate from a consumer guess, overwrite authoritative input, copy a
producer snapshot as consumer proof, or report success because generation or
parsing completed.

## Public And Independently Deployed Evolution

For public or independently deployed consumers:

- state the compatibility window and version negotiation mechanism;
- preserve old behavior only for the promised window;
- keep version-specific handling explicit and testable;
- reject unsupported versions with typed diagnostics; and
- remove expired compatibility paths through a planned breaking release.

Speculative consumers do not justify indefinite compatibility.

## Degraded Outcomes

Degraded behavior is valid only when its source is authoritative enough for the
operation and its semantics remain true. Record:

- provenance and freshness;
- operations allowed while degraded;
- differences visible to callers or users;
- recovery and invalidation behavior; and
- acceptance claims for the degraded path.

If no semantically valid result exists, return a typed outcome such as:

- `unavailable` when a required capability or resource is absent;
- `invalid` when input or stored state violates the contract;
- `unsupported` when a version or capability is outside the supported set; or
- `deferred` when valid work is durably queued for later execution.

Do not return defaults, partial values, empty collections, stale cache entries,
or alternate execution paths unless the contract explicitly defines them as
valid results.

## No Implicit Fallback

Fallback is a contract decision, not an exception-handling convenience. It
requires:

- an owner with authority to define the substitute;
- semantic fidelity for the requested operation;
- an observable degraded state;
- bounded staleness or validity rules; and
- focused and objective-level evidence.

When any requirement is missing, preserve the typed diagnostic rather than
guessing, silently retrying another backend, or carrying forward old behavior.
