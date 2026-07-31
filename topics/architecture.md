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
