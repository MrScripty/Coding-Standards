# Dependencies

**Standards metadata**

- ID: `topic.dependencies`
- Role: `topic`
- Level: `MUST`
- Applies when: A change adds, selects, resolves, installs, updates, removes, audits, or changes ownership of a software, toolchain, service, build, test, runtime, or system dependency.
- Does not apply when: No dependency requirement, declaration, resolution, provisioning, or lifecycle behavior changes.
- Requires: `core`, `workflow.verification`, `workflow.release`
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
- rejection of ambient, transitive, global, alternate, privilege, and
  default-success fallbacks.
