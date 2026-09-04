# Contract Evolution

**Standards metadata**

- ID: `topic.contracts.evolution`
- Role: `topic`
- Level: `MUST`
- Applies when: A change affects contract compatibility, persisted representations, or independently changing consumers.
- Does not apply when: No compatibility promise, persisted representation, or independently changing consumer is affected.
- Requires: `topic.contracts`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `topics/contracts/evolution.md`

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
