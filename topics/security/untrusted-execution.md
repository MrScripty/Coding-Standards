# Untrusted Execution And Delegated Authority

**Standards metadata**

- ID: `topic.security.untrusted-execution`
- Role: `topic`
- Level: `MUST`
- Applies when: Executed behavior has less permitted authority than its host, a component exercises protected authority for a less-trusted caller, or a product promises execution isolation.
- Does not apply when: Execution remains within one trusted authority and no delegated protected operation or separate isolation guarantee is affected.
- Requires: `topic.concurrency`, `topic.security`
- Specializes: `none`
- Verification: Claim-selected authority, delegation, composition, output-admission and lifecycle decision cases, with the required environment and affected consuming paths.
- Canonical owner: `topics/security/untrusted-execution.md`

## Effective Authority Across Execution

### Protection Claim And Effective Authority

For each protection claim, identify the protected resources and operations,
the actor's relevant capabilities, required useful behavior, permitted effects,
and trusted enforcement owners. Distinguish confidentiality, integrity,
availability, and restrictions on delegated actions when those properties are
part of the claim. Keep the inventory bounded to the declared actor and
resources; its completeness must follow from the supported interfaces and
capabilities, not from the routes a test happened to sample.

Account for authority available directly, inherited through execution state
or handles, passed to descendants, or exercised through reachable services.
Choose the execution boundary and granted capabilities from that inventory.
An operating-system user, filesystem layout, process boundary, or named policy
establishes only the properties its effective mechanisms enforce.

### Delegation And Composed Enforcement

Before exercising protected authority for a caller, establish the initiating
actor and the requested operation, resource, destination, and limits required
by the authorization contract. Bind that authority to the actual effect,
including indirect targets and subsequent delegation when they are in scope.
A component may grant a deliberately limited operation without giving the
caller its own credentials. Credential confidentiality and permission to use
a credential-backed operation remain separate claims.

Assign an enforcement owner to every restriction across supported entrypoints
and relevant lifecycle states. Establish the effective policy of the deployed
composition, including inherited permissions, ambient services, and policy
overrides that can change the claim. When a layer is changed or disabled,
re-establish the affected guarantees for the remaining composition.

Select mechanisms that preserve the required useful operations and restrict
the disallowed effects. The existing [Security](../security.md) authority owns
identity, permission, credential disclosure and filesystem containment.

### Admission Of Execution Output

Treat output from less-trusted execution as untrusted at its destination
boundary. Establish the destination representation, permitted interpretation
and effects before importing or publishing it with greater authority.
Configuration, executable metadata, references and callbacks supplied by the
producer acquire only the authority explicitly admitted by that contract.

Validation and admission must cover the representation actually consumed and
the lifetime over which its proof is used. Successful execution or well-formed
serialization does not establish that importing the output is authorized.
Apply the existing Contracts and Persistence owners for validation, durable
publication, interruption and recovery; this detail adds no mandatory importer
phase sequence or output format.

### Lifetime And Evidence

Establish each selected restriction before the actor can exercise the affected
capability and preserve it through the claim's lifecycle. Before a transition
that depends on prior activity losing its effects, follow
[Concurrency's cessation contract](../concurrency.md#cessation-of-effects-before-resource-transition).

Select evidence that observes both required useful behavior and the forbidden
effect at the relevant entrypoint and environment. Distinguish an operation
being denied, an effect confined to private state, and protected shared state
remaining unchanged. Use the existing Verification owner to select adequate
construction guarantees, controls and observations; sampled denial is evidence
for its declared domain.

When authority or enforcement cannot be established, preserve the owning
operation's typed unavailable or unsupported outcome; reject contradictory
authority or a violated restriction as invalid. Keep the affected protection
claim unestablished. This detail does not mandate a sandbox product, process
split, credential broker, fixed threat-model template or permanent test harness.
