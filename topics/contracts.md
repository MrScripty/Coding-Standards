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

When a change affects schema dialects, generated contracts, or contract version invalidation, follow [Declaration And Semantic Authority](contracts/schemas.md#declaration-and-semantic-authority).

## Version Scope And Invalidation

When a change affects schema dialects, generated contracts, or contract version invalidation, follow [Version Scope And Invalidation](contracts/schemas.md#version-scope-and-invalidation).

## Generated Contract Semantic Conformance

When a change affects schema dialects, generated contracts, or contract version invalidation, follow [Generated Contract Semantic Conformance](contracts/schemas.md#generated-contract-semantic-conformance).

## Schema Dialect And Vocabulary

When a change affects schema dialects, generated contracts, or contract version invalidation, follow [Schema Dialect And Vocabulary](contracts/schemas.md#schema-dialect-and-vocabulary).

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

## Protocol Outcome Projection

When a change projects domain outcomes into a protocol or adapts a protocol boundary, follow [Protocol Outcome Projection](contracts/protocols.md#protocol-outcome-projection).

## Protocol Adapter Proof

When a change projects domain outcomes into a protocol or adapts a protocol boundary, follow [Protocol Adapter Proof](contracts/protocols.md#protocol-adapter-proof).

## Contract Classes

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Contract Classes](contracts/evolution.md#contract-classes).

## Cross-Language Contract Selection

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Cross-Language Contract Selection](contracts/evolution.md#cross-language-contract-selection).

## Coordinated Breaking Replacement

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Coordinated Breaking Replacement](contracts/evolution.md#coordinated-breaking-replacement).

## Persisted Evolution

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Persisted Evolution](contracts/evolution.md#persisted-evolution).

## Persisted Contract Artifacts

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Persisted Contract Artifacts](contracts/evolution.md#persisted-contract-artifacts).

## Public And Independently Deployed Evolution

When a change affects contract compatibility, persisted representations, or independently changing consumers, follow [Public And Independently Deployed Evolution](contracts/evolution.md#public-and-independently-deployed-evolution).

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
