# Architecture

**Standards metadata**

- ID: `topic.architecture`
- Role: `topic`
- Level: `MUST`
- Applies when: A change creates or changes module, layer, service, process, data-authority, composition, dependency-direction, or state-ownership boundaries.
- Does not apply when: No architectural ownership, dependency, lifecycle, or deployment boundary changes.
- Requires: `core`, `topic.contracts`
- Specializes: `none`
- Verification: Architecture decision fixtures plus affected dependency, contract, lifecycle, and cross-boundary evidence.
- Canonical owner: `topics/architecture.md`

## Architecture Authority

Architecture owns placement and direction of responsibilities, authority,
state, dependencies, and runtime composition. Contracts owns boundary
representation and compatibility; Concurrency owns ordering and concurrent
access; Resilience owns failure and degradation; deployment and application
profiles own concrete mechanisms.

## Concern Boundaries

Separate concerns when they change for different reasons, require different
owners or lifecycles, or let callers ignore unrelated policy safely. Keep a
coherent concern together when its invariants, inputs, outputs, lifecycle, and
failure behavior form one decision. Directory and file placement follow those
boundaries; repository shape does not create them.

Select layers, modules, packages, services, or processes from actual ownership,
deployment, trust, scaling, lifecycle, and change facts. Do not require a
universal layer count, layer name, directory tree, source-root README threshold,
or inward-dependency diagram.

## Composed Design Admission

Apply this admission when a material design introduces or changes Modules,
Interfaces, Seams, Adapters, composition roots, or several permanent mechanisms
that together create a new operational or maintenance obligation. Re-run it
when a replacement design changes that composition or observed change
propagation is materially broader than predicted.

Record the produced artifact, not only its proposed parts:

1. independent concerns and their what, who, how, when, where, and why
   dimensions;
2. required and accidental interleavings of state, identity, value, time,
   policy, and mechanism;
3. everything callers, peer Modules, and the composition root must know;
4. representative changes and every owner each change is semantically forced
   to touch;
5. which dependencies carry stable values or Interfaces and which expose
   hidden representation, ordering, lifecycle, policy, or version knowledge;
6. whether the parts can evolve, be verified, fail, and be replaced
   independently;
7. the deletion result for each new permanent Module, Seam, Adapter, registry,
   validator, generator, version, or other mechanism; and
8. necessary inherent complexity, where it is contained, and the cumulative
   machinery retained by the complete design.

A useful Module has Depth: its Interface gives callers Leverage while hiding
more knowledge than it requires them to learn. Evaluate Locality through the
representative changes; a nominal split is still complected when the same
knowledge and verification must propagate through its callers or peer Modules.
Use the deletion test: if deleting a Module makes its complexity disappear, it
was incidental; if the necessary complexity reappears across callers, the
Module was containing it.

A hypothetical Adapter may probe the shape of a possible Seam, but does not
justify permanent generality. Generality requires a current independent reason.
Materially distinct real implementations are evidence; a separately owned
public contract, trust, deployment or lifecycle boundary, or enforceable
invariant may also justify a Seam without multiple current implementations.
Keep test-only or internal Seams inside the Module unless callers need the
variation as part of its Interface.

The admission must be able to keep one deep coherent Module, introduce a Seam,
aggregate adjacent machinery, or delete or decline a guarantee. File, type,
Module, dependency, or test counts are diagnostic inputs, never the verdict.
Missing material artifact or change-path facts are `unavailable`; contradictory
ownership, Interface, or coupling claims are `invalid`.

## Authority Scope Admission

Before a module, schema, manifest, registry, model, interface, or other artifact
becomes canonical for more than one concern, record the responsibility it
owns, the concerns it only references, the owner and lifecycle of each concern,
and the reasons those concerns change. Canonical placement is an ownership
decision; the ability to contain, serialize, validate, generate, or distribute
information does not transfer authority for that information.

Admit one authority scope only when its concerns form one coherent
responsibility with aligned owners, lifecycle, invariants, and change reasons.
When concerns can change independently, keep their authorities independently
replaceable even if one artifact references or packages them together. A
shared file, data format, generator, deployment, release, or repository
location is not evidence of a shared responsibility.

The selected boundary should hide more implementation detail than it exposes
through its interface and localize the complexity required to uphold its
responsibility. If removing one concern would leave unrelated fields,
versions, invalidation, consumers, or policy in place, treat that as evidence
of separate authority unless an explicit shared invariant proves otherwise.

Missing owner, lifecycle, or change facts are `unavailable`; contradictory
authority is `invalid`. Do not fall back to an umbrella artifact, the current
file boundary, or a single version merely because separation requires an
adapter or explicit composition.

## Dependency Direction And Services

Dependencies point toward the owner of the stable contract, not toward a
framework, transport, UI, storage mechanism, or current file location.
Business policy remains usable independently of delivery and infrastructure
mechanisms unless its domain contract requires them. A service boundary
requires an independently meaningful owner or deployment/lifecycle boundary;
test convenience alone does not create one.

## Data And State Authority

Assign every authoritative datum and state transition one owner. Projections,
caches, views, and pending input identify their source and synchronization
contract and cannot become a second authority. Backend, frontend, worker,
process, or database location does not determine ownership by itself.
Optimistic projection is allowed only when its reconciliation and failure
semantics satisfy the selected contract.

## Runtime Composition

Construct concrete infrastructure and long-lived resources at the narrowest
composition boundary that owns their configuration and lifecycle. Consumers
depend on selected contracts and receive dependencies explicitly. Do not create
ambient global infrastructure, duplicate a long-lived owner, or hide runtime
selection inside business policy.

## Immutable Authority Closure

An immutable, replayable, or inspectable handle binds the complete transitive
authority closure required to reproduce every result advertised from that
handle. The closure includes each authority, contract, provider input, and
authorization view whose value can affect the result, referenced through an
exact immutable identity.

Resolution cannot depend on ambient mutable state, an instance-local cache,
the originating process, undeclared providers, fresh authorization, or a live
filesystem or service read that is not itself bound into the closure. Derived
results may be cached, but cache availability and process history cannot change
their meaning.

Persistence owns reopening through real store adapters, and Contracts owns
handle representation and version behavior. If any required authority cannot
be resolved exactly, return `unavailable`; if resolved content contradicts its
identity or closure, return `invalid`; and if the representation or contract
version is well formed but unsupported, return `unsupported`. Do not replace a
missing immutable input with current ambient state.

## Typed Outcomes

Return typed `invalid` for contradictory ownership, dependency, lifecycle, or
authority decisions; typed `unsupported` when a valid required architecture is
not supported by the selected environment; and typed `unavailable` when a
required owner, contract, deployment, lifecycle, or capability fact cannot be
established. Do not fall back to the incumbent structure, a fixed layer model,
backend ownership, framework placement, global state, or the smallest diff.

## Verification

Evidence covers applicable dependency direction, owner uniqueness, independent
business-policy tests, contract boundaries, state transitions, projection
reconciliation, composition lifecycle, and real cross-boundary behavior.

After these decisions are complete, the non-normative
[Architecture Pattern Reference](../reference/patterns/architecture.md) may
help communicate an illustrative structural shape. Reference presence does not
select a pattern or establish applicability.
