# Schemas And Generated Contracts

**Standards metadata**

- ID: `topic.contracts.schemas`
- Role: `topic`
- Level: `MUST`
- Applies when: A change affects schema dialects, generated contracts, or contract version invalidation.
- Does not apply when: No schema dialect, generated contract, or contract-version invalidation changes.
- Requires: `topic.contracts`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `topics/contracts/schemas.md`

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
