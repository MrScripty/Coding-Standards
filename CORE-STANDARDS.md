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

## Reading And Applying These Standards

Read Core, then use the Router to select the workflows, topics, and profiles
that match the task. Requires means an unconditional prerequisite; Specializes
identifies a refinement of a broader concept. A related link is a route to
additional guidance when its stated condition applies, not a request to read
all descendants.

MUST states an obligation within its applicability. SHOULD is the recommended
starting point; depart when a concrete project constraint justifies it.
Profiles refine shared obligations for a technology or boundary. References
provide examples and explanation rather than additional requirements.

Apply governing external requirements and explicit project public contracts,
persisted contracts, and accepted architectural decisions first, then Core,
applicable profile mechanisms, and selected workflows and topics. A profile
cannot silently weaken the generic obligation it specializes. Identify an
actual conflict and obtain an explicit, owned, justified exception; do not
claim that an overridden obligation was satisfied.

When a standard asks for a contract or decision, start from the existing code,
accepted design, tool configuration, and consumer requirements. For routine
reversible choices, use a suitable established convention and explain a
material departure. Record reasoning in proportion to the consequence; an
ordinary local choice does not require a separate approval or design document.

A developer who lacks material facts should state the missing fact and its
consequence in ordinary prose and continue independent work. References to
invalid, unsupported, or unavailable do not require production error variants
for development uncertainty. Machine interfaces use their declared diagnostic
contract; production behavior uses the owning domain's failure contract.

## Objective And Scope

- Preserve the requested externally meaningful outcome through implementation
  and verification.
- State the exact behavior, contract, or decision a change owns.
- Keep changes inside an explicit write set. Record and separately disposition
  relevant findings outside it.
- Do not replace the requested objective with an easier proxy.

## Simplicity And Ownership

Keep one coherent concern together. Separate concerns that change for different
reasons, and give each state, contract, policy, and lifecycle one owner. A useful
abstraction lets callers ignore a decision it owns without hiding material
failure, ordering, or resource obligations. Compare the knowledge required of
callers before and after; fewer files or types do not by themselves mean a
simpler design.

Consolidate implementations of the same contract when copies risk divergence;
keep superficially similar code separate when its invariants or owners differ.
Use domain terms, remove unsupported dead paths, and add reuse machinery for a
current need. When choosing structure or terminology, follow
[Code Design And Ownership](topics/code-design.md).

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

- For a behavior change or defect, add a focused regression test before or
  with the implementation when existing evidence does not already prove the
  property. A construction proof or existing test can suffice when it covers
  the actual risk; explain material limits.
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
