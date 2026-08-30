# Core Standards

**Standards metadata**

- ID: `core`
- Role: `core`
- Level: `MUST`
- Applies when: A project adopts this standards library.
- Does not apply when: The project has not adopted this standards library.
- Requires: `none`
- Specializes: `none`
- Verification: Routed scenario review and the acceptance evidence selected for the change.
- Canonical owner: `CORE-STANDARDS.md`

These are the universal invariants. Load additional guidance through
[STANDARDS-ROUTER.md](STANDARDS-ROUTER.md), not by reading the entire library.

## Objective And Scope

- Preserve the requested externally meaningful outcome through implementation
  and verification.
- State the exact behavior, contract, or decision a change owns.
- Keep changes inside an explicit write set. Record and separately disposition
  relevant findings outside it.
- Do not replace the requested objective with an easier proxy.

## Simplicity And Ownership

- Separate concerns that change for different reasons. Do not split coherent
  behavior merely to reduce file or line counts.
- Give each policy, state, lifecycle, contract, and generated artifact one
  canonical owner.
- Keep business policy independent of transport, UI projection, persistence,
  runtime wiring, and diagnostics unless the domain itself requires coupling.
- Make dependencies point toward stable contracts and owned abstractions.
- Do not create a second source of truth to avoid changing the real owner.

Simplicity is the reduction of entanglement and reasoning load, not the
minimization of files, types, dependencies, abstractions, or lines. A boundary
is useful when it lets a maintainer understand or change one concern without
also understanding unrelated transport, lifecycle, persistence, runtime, UI,
timing, or diagnostics policy.

Keep one coherent concern together when its invariants, lifecycle, inputs,
outputs, and failure behavior form one decision. Introduce a named boundary
when it separates independently changing decisions, establishes one owner, or
makes an invariant enforceable. More named components can be simpler when each
removes unrelated context from the others.

Do not select a design from a file-length threshold, type count, dependency
count, call-site count, repository layout, incumbent abstraction, or smallest
diff. If material ownership, invariants, lifecycle, failure, or change facts
are unresolved, return the applicable typed diagnostic or record the decision
before implementation rather than choosing the fewest visible constructs.

### Code And Terminology Discipline

Use the least code and structure that make the owned behavior, invariants,
lifecycle, failures, and side effects clear. Additional structure is justified
when it separates independently changing decisions, enforces an invariant,
removes repeated reasoning, or supports demonstrated variants. It is not
justified by speculative reuse, a preferred construct count, an incumbent
pattern, or the smallest visible diff.

Create an abstraction only when callers can safely ignore a concern that the
abstraction owns. Keep its material lifecycle, ordering, state authority,
failure behavior, and side effects visible in the contract. One call site may
justify a boundary and many call sites may not; call count does not decide.

Consolidate repeated implementations when they express the same owned
contract and independent copies create divergence risk. Keep superficially
similar implementations separate when their owners, invariants, lifecycle, or
change axes differ. Do not apply blanket extraction, reuse, or duplication
rules.

Delete code, aliases, adapters, flags, comments, and conditional code branches
that have no current owner or supported contract. Preserve a path only for a
real active consumer, retained state, deployment overlap, or other declared
lifecycle obligation. Unverified future use and incumbent presence are not
retention authority.

Choose names from domain meaning, role, unit, ownership, lifecycle, and
observable effect at the narrowest useful scope. Use one term for one concept
within a contract and distinguish different concepts even when their
implementations look alike. Rename when current terminology misstates the
owned concept; do not keep or copy a name solely for consistency with an
incumbent, framework convention, or generic naming recipe.

Missing or contradictory ownership, invariant, consumer, lifecycle, or domain
meaning requires a typed diagnostic or a recorded decision before structural
change. Do not fall back to fixed call counts, blanket DRY, universal brevity,
speculative extension points, existing terminology, or copied examples.

### Simple, Easy, And Complection

For these standards, **simple** describes an artifact whose distinct concerns
are not interleaved. **Easy** describes an approach that is familiar, nearby,
available, or convenient to a particular person or environment. Easy and simple
may coincide, but neither proves the other.

An artifact is **complex** or **complected** when otherwise independent concerns
must be understood or changed together because their knowledge, state,
identity, value, time, location, representation, mechanism, or policy is
interleaved. To **compose** is only to place concerns together; composition,
decomposition, and naming do not decide simplicity.

Judge the produced artifact and its evolution, not the ease of authoring,
generation, installation, familiarity, or conformance to an incumbent pattern.
Simplicity evidence asks whether independent concerns can be understood and
changed independently and whether each change exposes only the knowledge it
owns. Counts may locate accumulated cost but cannot decide simplicity.

## Authority And Boundaries

- Validate untrusted input at every trust boundary before constructing a
  validated domain or transport type.
- Preserve units, ranges, optionality, identifiers, error meaning, and
  ownership across boundaries.
- Keep generated artifacts derived from their declared source. Do not edit
  generated output as an independent implementation.
- Use explicit typed outcomes when required facts are unavailable or invalid.
  Do not guess a valid-looking decision.

## Failure And Degraded Behavior

- Propagate failures with enough bounded, non-sensitive context to identify the
  failed operation and owner.
- A fallback or degraded mode is valid only when its data is authoritative for
  that purpose and its semantics satisfy the requested contract.
- Do not convert arbitrary failures into unsupported, empty, default, cached,
  or partial success.
- Do not delete, rebuild, or replace authoritative state unless its lifecycle
  contract explicitly makes it disposable or a verified migration owns the
  replacement.

## Contracts And Compatibility

- Derive compatibility policy from actual consumers, persistence, deployment,
  and authority boundaries.
- Do not add compatibility shims for hypothetical consumers.
- Do not break public, persisted, or independently deployed contracts without
  an explicit versioning or migration path.
- Coordinated internal contracts may be replaced atomically when all producers,
  consumers, generated artifacts, and fixtures change together.

## Lifecycle And Concurrency

- Every long-lived task, process, resource, subscription, and runtime has an
  owner responsible for startup, cancellation, shutdown, and terminal state.
- Do not detach work whose completion or failure affects correctness.
- Do not hold blocking or synchronous guards across suspension points.
- Make retries, cancellation, ordering, and restart behavior explicit when they
  affect observable results.

## Implementation Quality

- Prefer types and APIs that make invalid states difficult to represent.
- Reject stubs, placeholders, silent no-ops, and fake success in production
  paths.
- Reuse an established library for domain logic with difficult parsing,
  protocol, physics, security, or scheduling semantics unless a recorded
  decision justifies owning it.
- Add dependencies only with an owner, purpose, compatible license, and
  verification strategy.
- Keep comments focused on non-obvious invariants, safety reasoning, and
  ownership decisions.

### Semantic Constants And Configuration

Name a value when its domain meaning, unit, policy, protocol identity, tuning
authority, reuse, or coordinated change must be explicit. Keep a self-evident
local literal at its point of use when naming or exporting it would add
indirection without clarifying ownership.

Place a constant or configuration value with the narrowest concern that owns
its meaning and lifecycle. Share it only when multiple consumers intentionally
use the same semantic contract. Central version coordination or convenient
imports do not transfer ownership and do not justify a global constants
container.

Configuration is runtime or deployment-selected only when the owning contract
allows variation. Do not turn invariants into settings, duplicate defaults
across boundaries, infer units from a name, or select a value because it is
already centralized. Missing or contradictory meaning, unit, owner, source, or
override authority requires a typed diagnostic rather than a magic value,
ambient setting, or incumbent default.

## Verification

- Add the smallest test that fails for the defect or missing behavior before or
  with its implementation.
- Run focused checks for the changed behavior and affected static/toolchain
  contracts.
- Use integration, contract, system, user-workflow, environment-gated, and
  release evidence when the objective crosses those boundaries.
- Lower-fidelity evidence cannot satisfy a higher-fidelity acceptance
  criterion.
- Mark work accepted only after its named acceptance evidence passes. Use a
  visible blocked or verifying state when required evidence is unavailable.

## Change Integrity

- Inspect repository state before editing and do not overwrite unrelated work.
- Review the exact staged diff before committing.
- Keep each commit limited to one coherent, verified outcome.
- Never rewrite shared history. Rewriting local history or deleting workspaces
  requires explicit authority.
