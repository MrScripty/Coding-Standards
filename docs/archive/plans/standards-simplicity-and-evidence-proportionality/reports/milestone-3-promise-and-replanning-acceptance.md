# Milestone 3 Promise And Replanning Acceptance

## Accepted Result

Architecture now derives immutable authority closure from the operations,
result semantics, supported lifetime, and reconstruction promise actually
advertised. In-process use does not imply cold replay. A complete immutable
aggregate may carry the admitted semantic closure without separate identity,
codec, handle, version, ordinal, registry, and lifecycle objects. Separate
records remain appropriate when they have independently changing authority,
consumers, lifetimes, or reconstruction paths.

Contracts now distinguishes a current-format discriminator, identity-domain
revision, compatibility version, migration version, and allocation ordinal.
One value may combine roles only when their authority, consumers, reasons for
change, and consequences coincide. A compatibility matrix is required only for
producer, consumer, and retained-state combinations the project actually
promises concurrently. Atomic coordinated replacement requires a fail-closed
format decision, not a historical compatibility matrix.

Planning now bounds systemic correction by the canonical semantic owner and
reachable consumer population. A new owner, semantic consumer, material risk,
or public or persistence promise expands the audit; another implementation
file inside an already bounded owner does not. Valid repairs include deletion,
consolidation, a smaller Interface, stronger construction or type proof, and
replacement of overlapping evidence. The repaired composition is compared
with the original objective before implementation resumes.

These remain project-agnostic written standards. They prescribe decisions and
outcomes, not an adoption-time enforcement mechanism.

## Standards-Impact Review

The accepted normative graph contains 51 policy units and 108
standards-to-standards routing relationships. Milestone 3 inspected 15 routes
and added eight:

- Immutable Authority Closure retains Persistence and adds Contracts,
  Security, Resilience, Verification, and Generated Contract.
- Version Scope And Invalidation retains its six routes to Library, Generated
  Contract, IPC, Language Bindings, Persistence, and Release.
- Systemic-Finding Re-Planning adds Architecture, Implementation, and
  Verification.

Each target was inspected for its local consequence. Existing contract,
trust, recovery, evidence, boundary, release, planning, and implementation
wording already owns those consequences, so no target repeats the source
procedure. The routes remain because a later source change could require those
standards to be inspected even when this review found no prose conflict.

Fresh graph review corrected the original plan, which had routed Immutable
Authority Closure only to Persistence. The five additional potentially
affected standards are recorded in the disposition manifest and registered in
the source-owned graph declaration. Application code and conformance artifacts
are not counted as standards-impact consumers.

## Repository Conformance Evidence

The existing `contract-authority-scope` suite now owns the generic immutable-
closure fixture as well as its existing authority and version-scope decisions.
This resolves the prior A1c-specific evidence-owner mismatch without creating
another suite or catalog node. Its closure fixture has 13 cases and its
version-scope fixture has 22 cases.

The existing `systemic-finding-replanning` suite now decides 19 bounded-search,
repair, composition, and stopping cases while preserving an isolated missing-
audit negative fixture. No prompt or template procedure was copied and no new
suite was introduced.

The repository's complete policy projection contains 454 relationships. The
346 projections outside the 108 standards-impact routes remain separate
conformance, delivery, routing, and implementation metadata. The retained
A1c-named migration fixture received nine mechanical additions and two
fingerprint corrections solely because its closed-set check inventories the
whole repository projection. No A1c design or implementation was inspected or
changed.

## Verification Record

The two focused owner suites, policy semantic-impact suite, closed migration
suite, and all 227 declarative suites pass. The accepted graph generator
reconstructs the fixed 47-unit/62-relationship baseline and validates all 12
policy-unit dispositions, nine pre-existing revised-owner routes, 46 planned
standards-impact additions, and eight catalog additions against the live
51-unit/108-relationship result.

Final retained-checker, generated-input, link, and diff verification is owned
by Milestone 5.
