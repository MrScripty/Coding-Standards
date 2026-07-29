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
