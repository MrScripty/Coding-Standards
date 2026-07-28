# Contract Evolution And Degraded Outcomes

**Standards metadata**

- ID: `topic.contracts`
- Role: `topic`
- Level: `MUST`
- Applies when: A change affects data or behavior consumed across a module, process, persistence, package, deployment, or generated boundary.
- Does not apply when: A private implementation detail has no independent consumer, stored representation, or externally observable promise.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Contract decision fixtures and affected producer/consumer claims.
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
