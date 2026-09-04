# Dependencies

**Standards metadata**

- ID: `topic.dependencies`
- Role: `topic`
- Level: `MUST`
- Applies when: A change adds, selects, resolves, installs, updates, removes, audits, or changes ownership of a software, toolchain, service, build, test, runtime, or system dependency, or decides to implement difficult standardized semantics instead of adopting an established implementation.
- Does not apply when: No dependency requirement, implementation-versus-adoption decision, declaration, resolution, provisioning, or lifecycle behavior changes.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Dependency requirement, ownership, selection, resolution, authorization, satisfaction, and lifecycle decision fixtures plus affected real resolver and consumer evidence.
- Canonical owner: `topics/dependencies.md`

## Dependency Authority

Select a dependency only from an explicit requirement and consumer contract.
The contract identifies the capability, owning execution boundary, lifecycle
phase, supported targets and environments, release or deployment constraints,
and evidence required to prove satisfaction.

Dependencies owns requirement, candidate comparison, selection, declaration
ownership, resolution, provisioning authorization, satisfaction, update, and
removal policy. Release owns published artifact and consumer acquisition
information. Security owns trust and untrusted-input authorization. Resilience
owns failure, retry, and degradation. Language and framework profiles own
mechanisms. Launcher only projects an accepted dependency procedure.

## Requirement And Ownership

Declare each dependency at the narrowest boundary that owns and executes it.
Shared declarations require evidence that multiple owned consumers use the
same requirement; centralized version coordination does not erase consumer
ownership. Incidental transitive availability, workspace hoisting, global
installation, ambient search paths, and another package's declaration are not
satisfaction evidence.

Classify runtime, build, test, development, generated, optional, and system
requirements from actual consumer and lifecycle facts. Do not infer ownership
or criticality from repository layout, dependency category, package-manager
convention, or current installation state.

## Candidate Selection

Compare supported candidates against the complete requirement. Applicable
facts may include capability and API fit, target support, maintenance and
support commitments, license, security evidence, provenance, transitive and
operational cost, performance, size, interoperability, release model,
migration cost, and independent-consumer constraints.

Use only facts material to the selected contract and record the decision
proportionally to its risk. Popularity, recency, download count, line count,
transitive count, standard-library status, ecosystem ranking, or one maintainer
signal cannot select or reject a candidate by itself. Do not choose an
in-house implementation, incumbent package, largest framework, smallest
package, or first available alternative as fallback.

Inspection output is candidate evidence, not selection authority. A dependency
graph, reverse-dependency path, transitive count, or standard-library
alternative can inform applicable contract facts but cannot independently
accept or reject a candidate.

## Implementation Versus Dependency

Treat a decision to implement difficult standardized semantics locally instead
of adopting an established implementation as a dependency-selection decision.
This applies to schemas, protocols, parsers, serializers, cryptography,
scheduling, and comparable domains where correctness depends on a substantial
external or standardized semantic surface.

Compare the local implementation and candidate dependencies against the same
complete requirement, including:

- required semantic surface and extension behavior;
- conformance, compatibility, and official or independent test support;
- supported targets, provenance, and licenses;
- update, vulnerability, and security-response ownership;
- failure and unsupported-domain behavior;
- implementation and long-term maintenance cost; and
- the continuing cost of keeping a local subset correct.

Record why the selected option satisfies the requirement and how its semantic
claims will be maintained. A preference against dependencies, a small current
input set, sunk implementation cost, or absence of an immediate failing test
does not justify local implementation. If required candidate or maintenance
facts are missing, return `unavailable`; if no supported option meets the
requirement, return `unsupported`; and if the decision contradicts known
contract facts, return `invalid`.

Apply this comparison when creating a local standardized implementation,
materially extending its semantic surface, or renewing its dependency and
maintenance decision. The later existence of a candidate dependency does not
by itself require automatic deletion of an unchanged accepted local
implementation; re-evaluate it at one of those lifecycle triggers against the
current requirement and ownership facts.

A thin Adapter that delegates the standardized semantics to an established
dependency is not a second implementation of those semantics. A
domain-specific product may own distinct local semantics even when it uses an
established dependency internally. Judge both by their real Interface,
delegation, added behavior, failure contract, and maintenance ownership. Do not
describe a pass-through reimplementation as an Adapter or invent nominally
distinct domain behavior merely to avoid the dependency comparison.

## Resolution And Reproducibility

Select manifest constraints, lock or snapshot material, feature sets, target
variants, source identity, integrity data, and resolver mode from the artifact,
consumer, release, and deployment contracts. Applications, published
libraries, tools, system packages, and independently resolved consumers may
require different strategies.

The selected resolution must be reproducible to the degree required by its
claim and must preserve enough identity to audit the dependency actually
consumed. Do not impose one lockfile, exact pin, version range, workspace
override, update cadence, registry, or resolver command universally. Do not
silently use an unlocked, cached, ambient, transitive, global, or alternate
resolution when required material is missing.

## Compatibility And Lifecycle

Define update, replacement, and removal obligations from every owned consumer,
published contract, persisted or wire representation, generated artifact,
supported target, and deployment unit affected by the dependency. Candidate
version labels and changelogs are inputs; they do not prove compatibility.

Before mutation, identify the current consumed identity, proposed identity,
contract changes, migration requirements, rollback or recovery authority, and
claim-matched evidence. Resolve the candidate in an isolated or reviewable
state when the selected tool supports it. Do not update an unrelated
dependency, broaden constraints, accept a resolver-selected version, or retain
an incumbent solely because compatibility evidence is unavailable.

Removal proves that declarations, lock or snapshot material, feature
selection, generated output, code paths, tooling, release artifacts, and owned
consumer references no longer require the dependency. Search results and
unused-dependency tools are supporting evidence, not complete removal proof.

## Features And Footprint

Select features, optional capabilities, default-feature behavior, target
variants, and dependency placement from actual consumer requirements. Measure
transitive graph, build, binary, bundle, startup, memory, operational, and
support effects only when material to the contract.

Feature gating, dependency splitting, standard-library use, in-house
implementation, and framework avoidance are mechanisms, not defaults. A
library's reusable consumer surface may impose different footprint and target
constraints from an application, but repository layer or artifact label alone
does not select a threshold.

Do not use fixed line counts, transitive counts, package sizes, download
trends, release ages, maintainer counts, or "one purpose" labels as automatic
selection or rejection rules.

## Audit And Review

Derive audit scope and cadence from provenance, security, licensing,
maintenance, compatibility, support, release, and operational risk. Record
which identities and consumers were examined, the authoritative evidence,
findings, disposition owner, deadline or acceptance condition, and required
follow-up.

Automated vulnerability, license, provenance, unused, duplicate, outdated, and
footprint tools prove only their declared detection contracts. Manual review
may cover context unavailable to tools. Neither tool output nor absence of a
finding proves that every dependency obligation is satisfied.

Classify findings through their canonical owner. Security owns vulnerability
and trust response, Licensing owns legal obligations, Release owns publication
effects, and Dependencies owns selection and lifecycle consequences. Do not
silently ignore findings, upgrade everything, remove a dependency, or accept a
warning because a conventional severity or schedule says so.

## Automation And Bootstrap

Automation implements selected dependency checks and procedures; it does not
create policy. Each check declares its owner, inputs, required capability,
environment, evidence, and blocking or advisory outcome. Select local, commit,
pull-request, scheduled, release, or manual execution from the claim and cost.

Tools required to execute dependency checks are dependencies themselves. Give
them explicit ownership, resolution, provisioning authority, and satisfaction
evidence. Do not install audit tools implicitly in a check, depend on ambient
global tools, copy a universal CI workflow, or treat tool startup as proof of
the dependency claim.

## Satisfaction And Provisioning

Define satisfaction evidence for each requirement before provisioning. A
binary presence check, import, version string, manifest entry, lockfile entry,
service response, or package-manager status is sufficient only when the
requirement contract says it proves the required capability and identity.

Install, update, repair, or remove a dependency only with explicit operator or
automation authority and a selected procedure. Re-check the complete
satisfaction contract after mutation and preserve the procedure's diagnostics
and terminal outcome. An already satisfied requirement may be reported without
mutation; an unsupported or inapplicable requirement is not a successful
no-op.

Do not install implicitly during build or run, auto-escalate privileges,
replace a selected dependency, change registries, broaden versions, mutate
unrelated dependencies, or treat attempted installation as proof of success.

### Provisioning Procedure

Represent each requirement as an independently identifiable unit with its own
satisfaction contract and, when provisioning is authorized, its own selected
mutation procedure. Evaluate every declared requirement independently so an
already satisfied requirement is not mutated merely because another
requirement is missing. Grouped resolution or installation is permitted only
when the selected tool owns that transaction and preserves per-requirement
identity, evidence, diagnostics, and terminal outcomes.

The procedure order is:

1. evaluate the declared satisfaction contract;
2. report the accepted already-satisfied outcome without mutation, or identify
   the missing or invalid evidence;
3. obtain explicit mutation authority and execute the selected procedure only
   for requirements that need it;
4. re-evaluate the same satisfaction contract after mutation; and
5. preserve any resolver, provisioning, or verification failure as the
   requirement's terminal outcome.

Function names, process exit codes, command names, status labels, and output
format are projections selected by the owning language, tool, application, or
operator contract. They are not universal dependency policy. A Launcher action
may expose the accepted procedure, but it cannot create missing authority,
replace the satisfaction contract, combine unrelated requirements into one
opaque result, or reinterpret failure as success.

## Typed Outcomes

Return typed `invalid` for contradictory requirements, ownership, constraints,
or authorization; typed `unsupported` when no supported candidate or procedure
meets a valid declared requirement; and typed `unavailable` when required
candidate, resolver, identity, provisioning capability, or evidence cannot be
established. Preserve resolver, verification, and consumer failures when they
are more specific.

Do not continue with an incumbent, transitive, cached, global, standard-library,
in-house, alternate-registry, alternate-version, successful-no-op, skipped
verification, or default-success fallback.

## Verification

Evidence covers applicable:

- requirement and narrow execution-boundary ownership;
- candidate comparison against all material constraints;
- selected source, identity, constraints, features, and target variants;
- reproducible resolution and consumed-artifact identity;
- already-satisfied, missing, unsupported, invalid, and unavailable outcomes;
- explicit mutation authority and post-mutation satisfaction;
- update and removal effects on every owned consumer; and
- compatibility and migration effects across independently changing contracts;
- selected feature and footprint behavior where material;
- audit findings, ownership, disposition, and follow-up;
- automation environment, bootstrap dependencies, and blocking semantics; and
- rejection of ambient, transitive, global, alternate, privilege, and
  default-success fallbacks.
