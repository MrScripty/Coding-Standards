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

These universal invariants apply throughout an adopted project. Use
[Standards Router](STANDARDS-ROUTER.md) to select additional guidance from the
actual task.

## Reading And Applying These Standards

Read Core, then the Router and the applicable workflows, topics, and profiles.
Requires identifies an unconditional prerequisite; Specializes identifies a
refinement. Follow a related link when its stated condition applies. References
supply optional examples and explanation.

MUST states an obligation within its applicability. SHOULD states the
recommended starting point; a concrete project constraint may justify departure.
Apply governing external requirements, explicit project public and persisted
contracts, and accepted architectural decisions first; then Core, applicable
profile mechanisms, and selected workflows and topics. Profiles preserve the
generic obligations they specialize. Resolve an actual conflict through an
explicit, owned, justified exception and identify the obligation being overridden.

Start decisions from existing code, accepted design, tool configuration, and
consumer requirements. Reuse a suitable established convention for routine
reversible choices; explain material departures and record reasoning in
proportion to the consequence. Handle ordinary local choices within existing
authority; they require no separate approval or design document.

State missing development facts and their consequences in ordinary prose and
continue independent work. Machine interfaces use their declared diagnostic
contract; production behavior uses the owning domain's failure contract.

## Objective And Scope

- Preserve the requested externally meaningful outcome through implementation
  and verification.
- State the exact behavior, contract, or decision the change owns.
- Keep changes inside an explicit write set. Record and separately disposition
  relevant findings outside it.
- Demonstrate the requested outcome using evidence that observes it directly.

## Simplicity And Ownership

Keep one coherent concern together. Separate concerns that change for different
reasons, and give each state, contract, policy, and lifecycle one owner. An
abstraction should reduce what callers must know while exposing material
failure, ordering, and resource obligations. Evaluate that knowledge at the
callers and composition points.

Consolidate implementations of the same contract when copies risk divergence.
Keep code with different invariants or owners separate. Use domain terms,
remove unsupported dead paths, and add reuse machinery for a current need.
Follow [Code Design And Ownership](topics/code-design.md) when choosing structure
or terminology.

## Authority And Boundaries

- Validate untrusted input at each trust boundary before constructing a
  validated domain or transport type.
- Preserve units, ranges, optionality, identifiers, error meaning, and ownership
  across boundaries.
- Generate derived artifacts from their declared source.
- Return the declared typed outcome when unavailable or invalid facts prevent
  a valid machine decision.

## Failure And Degraded Behavior

- Propagate failures with bounded, non-sensitive context identifying the failed
  operation and owner.
- Use a fallback or degraded mode only when its data is authoritative for that
  purpose and its semantics satisfy the requested contract.
- Preserve failure meaning; report success only when the promised result exists.
- Preserve authoritative state. Delete, rebuild, or replace it only under an
  explicit disposable-state lifecycle or a verified migration that owns the
  replacement.

## Contracts And Compatibility

- Derive compatibility from actual consumers, persistence, deployment, and
  authority boundaries.
- Add or retain compatibility mechanisms only for actual supported consumers.
- Replace public, persisted, or independently deployed contracts through an
  explicit versioning or migration path with consumer and retained-state
  dispositions.
- Replace coordinated internal contracts atomically with their producers,
  consumers, generated artifacts, and fixtures.
- Select a supported contract that meets current product and deployment needs;
  replace a superseded design when the evidence supports the improvement and
  the required cutover is owned.

## Lifecycle And Concurrency

- Assign an owner for startup, cancellation, shutdown, and terminal state of
  every long-lived task, process, resource, subscription, and runtime.
- Retain ownership of asynchronous work through required completion, cleanup,
  failure handling, and result publication.
- Release blocking or synchronous guards before suspension.
- Make retries, cancellation, ordering, and restart behavior explicit when they
  affect observable results.

## Implementation Quality

- Prefer types and APIs that make invalid states difficult to represent.
- Expose production capability only when its implementation fulfills the
  advertised contract; represent unavailable capability at its owning boundary.
- Reuse an established library for difficult parsing, protocol, physics,
  security, or scheduling semantics unless a recorded decision justifies owning
  the implementation.
- Give each dependency an owner, purpose, compatible license, and verification
  strategy.
- Focus comments on non-obvious invariants, safety reasoning, and ownership.

### Semantic Constants And Configuration

Name a value when its domain meaning, unit, policy, protocol identity, tuning
authority, reuse, or coordinated change must be explicit. Keep self-evident
local literals at their point of use when that preserves clarity.

Place each constant or configuration value with the narrowest concern owning
its meaning and lifecycle. Share it when consumers intentionally use the same
semantic contract. Coordinate versions and imports consistently with that owner.

Allow runtime or deployment selection only where the owning contract permits
variation. Keep invariants fixed and units explicit. Derive defaults across
boundaries from their single semantic owner.
Resolve missing or contradictory meaning, unit, owner, source, or override
authority through the declared diagnostic contract before selecting a value.

## Verification

- For a behavior change or defect, add a focused regression test before or with
  implementation when existing evidence does not already prove the property.
  An adequate construction proof or existing test can suffice; explain material
  limits.
- Run focused checks for changed behavior and affected static/toolchain contracts.
- Use integration, contract, system, user-workflow, environment-qualified, and
  release evidence when the objective crosses those boundaries.
- Match acceptance evidence to the required fidelity and actual observable result.
- Accept work after its named evidence passes. Keep required unavailable evidence
  visible in a blocked or verifying state.

## Change Integrity

- Inspect repository state before editing and preserve unrelated work.
- Review the exact staged diff before committing.
- Keep each commit limited to one coherent, verified outcome.
- Preserve shared history. Obtain explicit authority to rewrite local history
  or delete workspaces.
