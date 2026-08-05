# Milestone 7 Row 39 Process Coordination Decomposition

## Re-plan Trigger

The planned single-owner review could not confirm
`reference/patterns/architecture.md` as the owner of `STD-0093` through
`STD-0105`. The frozen material combines normative process exclusion, identity,
platform capability, stale-state recovery, service lifecycle, retry, readiness,
transport, diagnostics, and evidence claims with diagrams and pseudocode.

A non-normative reference cannot own those decisions. Continuing under the
single-owner assumption would preserve competing policy and violate reference
non-authority.

## Owner Contract

Existing canonical owners remain authoritative:

- Architecture owns service placement, participant responsibility, and
  lifecycle authority.
- Concurrency owns exclusion invariants, atomicity, and coordination selection.
- Contracts owns instance identity, representation meaning, and observable
  operation outcomes.
- Cross-Platform owns supported process-identity capabilities and target
  evidence, not one operating-system API.
- Resilience owns stale-state classification, readiness failure, bounded retry,
  and recovery authority.
- Security owns listener exposure and liveness obligations when a network
  boundary applies.
- Diagnostics owns selected reporting; stale reclamation does not require a log
  by default.
- Verification owns evidence sufficiency and benefit claims.

`reference/patterns/architecture.md` may retain only conditional structural
illustrations after those owners select the applicable facts.

## Exact Ownership

The owner-validation table gives every identifier exactly one primary retained
owner and one disposition. Split outcomes may link other applicable owners, but
the reference never becomes normative.

- `STD-0093` and `STD-0099` remain discoverable reference indexes.
- `STD-0094` and `STD-0095` route exclusion and coordination selection to
  Concurrency without universal PID-file rules.
- `STD-0096` routes instance identity semantics to Contracts and removes the
  fixed JSON representation.
- `STD-0097` routes target capability to Cross-Platform and removes fixed Linux
  and Windows mechanisms.
- `STD-0098` routes stale-state recovery to Resilience and removes mandatory
  logging.
- `STD-0100` and `STD-0103` route service placement and lifecycle authority to
  Architecture without fixed ownership models.
- `STD-0101`, `STD-0104`, and `STD-0105` retain only qualified illustration and
  consequence material.
- `STD-0102` routes creation exclusion to Concurrency while preserving linked
  Contracts, Resilience, Security, and lifecycle authority.

## Ordered Children

1. `39.1` migrates `STD-0093` through `STD-0098`, retains at most one
   conditional process-coordination illustration, and removes PID-file,
   liveness, cleanup, platform-API, and logging defaults.
2. `39.2` migrates `STD-0099` through `STD-0103`, retains one conditional
   discover-or-create convergence map, and removes connect-first, creation-lock,
   backoff, health, and fixed lifecycle-model defaults.
3. `39.3` migrates `STD-0104` and `STD-0105`, retains only qualified pseudocode
   and consequences, closes row 39, and leaves P32 open for immutable row 40.

## Reference Selection

The high-level process-coordination and discover-or-create maps can communicate
one arrangement after canonical decisions are complete. Fixed PID-file
contents, process-start-time APIs, cleanup instructions, mandatory diagnostics,
retry behavior, and ownership catalogs are removed because they are mechanisms
or policy defaults rather than architecture illustrations.

Reference examples must name selected facts, variation points, rejection
conditions, and affected evidence. They cannot establish applicability.

## Bounded Write Sets

Child `39.1` may touch the process-instance section of
`ARCHITECTURE-PATTERNS.md`, `reference/patterns/architecture.md`, one focused
fixture and verifier, six exact dispositions, this row checker, plan, and
ledger.

Child `39.2` may touch the discover-or-create section of the legacy source,
the Architecture reference, one focused fixture and verifier, five exact
dispositions, this row checker, plan, and ledger.

Child `39.3` may touch the remaining discover-or-create example and benefit
material, the Architecture reference, one focused fixture and verifier, two
exact dispositions, this row checker, plan, and ledger.

Canonical topic, workflow, and profile files remain read-only unless focused
decisions prove a policy gap, which triggers re-planning. Shared dispositions,
legacy source, reference owner, checker, plan, and ledger remain serial. No
child may edit generated maps, immutable train, package manifest, router,
lockfile, template, configuration, or downstream repository.

## Verification Gates

Each child requires focused positive and typed negative decisions, exact
disposition proof, prohibited-default checks, preservation of unrelated legacy
sections, row-checker success, execution-train advancement, plan structure,
shell syntax, and diff integrity.

Row 39 closure is focused. P32 remains open until row 40 completes, so no row
39 child may claim the package complete or consume its deferred package gate.

## Typed Outcomes And No Fallback

Missing identity, exclusion, lifecycle, target capability, readiness, recovery,
transport, diagnostic, or evidence facts retain their canonical typed outcome.
Contradictory facts are `invalid`, unavailable required facts are `unavailable`,
and unsupported target mechanisms are `unsupported`.

Do not select a PID file, process start time, cleanup action, connection-first
flow, creation lock, retry, backoff, health probe, lifecycle model, listener,
log, incumbent service, or example as fallback. Legacy wording is removed or
replaced when its child is accepted and cannot remain alternate authority.

## Re-plan Triggers

Stop if focused decisions prove missing canonical policy, require a new owner,
require retaining fixed PID or platform mechanisms, make the reference
normative, change an exact ownership decision, require more than three semantic
children, require files outside a child write set, change P32 membership, edit
generated or immutable artifacts, or prevent focused verification from proving
the child outcome.
