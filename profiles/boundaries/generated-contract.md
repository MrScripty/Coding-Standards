# Generated Contract Boundary Profile

**Standards metadata**

- ID: `profile.boundary.generated-contract`
- Role: `profile`
- Level: `PROFILE`
- Applies when: A schema or generator produces program-facing models, validators, tool definitions, bindings, configuration, or another consumed representation.
- Does not apply when: Generation produces no representation interpreted by a program consumer, or the change preserves the generated contract and all of its consumers unchanged.
- Requires: `core`, `workflow.verification`, `workflow.build`, `topic.contracts`, `topic.dependencies`
- Specializes: `topic.contracts`
- Verification: Generated-contract routing, semantic-conformance, freshness, public-consumer, unsupported-domain, and reconstruction evidence.
- Canonical owner: `profiles/boundaries/generated-contract.md`

## Applicability

Select this profile when a canonical declaration and generator or compiler
produce a representation that a program consumes as models, validation,
dispatch, tool definitions, bindings, configuration, or another executable
contract. Generated documentation, reports, or copied data do not select it
unless a program consumer relies on their generated representation.

Select the Language Binding profile only for a genuine native/host or
cross-language representation. Select IPC only for a process, message,
plugin-host, or independently deployed boundary. Select Persistence only for
durable generated or consumed state. The presence of serialization, another
language in the repository, or a checked-in output does not establish those
additional boundaries.

Missing consumer or boundary facts leave routing `unavailable`; contradictory
facts are `invalid`. Do not route to a smaller contract profile when required
applicability facts are unresolved.

## Semantic Closure

Apply the complete generated-contract semantics owned by Contracts. Record the
canonical declaration, exact dialect and vocabulary, supported semantic
surface, generator and executable semantics owners, reachable public
operations, generated outputs, and actual producer and consumer entry points.
Also record the declaration's authority scope, independently changing semantic
owners it references, and each version's compatibility and material
invalidation scope. A declaration may project or invoke independently owned
semantics; generation does not transfer those authorities to the declaration
or justify one umbrella version.

Build owns deterministic derivation and stale-output rejection. Verification
owns claim and oracle sufficiency. Dependencies owns the decision to adopt an
established implementation or maintain difficult standardized semantics
locally. This profile specializes their application to the generated boundary;
it does not duplicate their policy.

Acceptance distinguishes source freshness, shape agreement, semantic
conformance, and public consumer behavior. It includes explicit rejection of
unsupported source behavior and uses an independent reference or official
corpus when several local implementations interpret an external contract.
Generated output, copied expectations, or agreement among local projections
cannot be the sole semantic oracle.

Return `invalid` for incomplete reachable closure, stale output, contradictory
semantics, or incomplete producer/consumer proof; `unsupported` for a
well-formed source construct outside the declared support set; and
`unavailable` when required declaration, generator, consumer, oracle, or
dependency-decision authority cannot be obtained. Do not partially generate,
silently omit semantics, or fall back to inferred consumer shape.

## Composed-Design Projection

Generation may make authoring easy without making the produced artifact simple.
For this profile, the produced artifact includes the generated Interface, its
consumers, the generator, runtime interpretation, and compatibility and
invalidation promises. Automating their coordinated propagation does not prove
that they can change independently.
