# Milestone 2 Evidence And Proof Acceptance

## Accepted Result

Verification now admits permanent tests, validators, integrity checks, hashes,
and related correctness machinery from an identified reachable failure and
material consequence. The admission must name the claim, proof boundary,
oracle, marginal deciding value, lifecycle cost, exact-byte purpose when one
exists, and retention or removal trigger. It compares types, construction,
static analysis, a deeper Interface, existing evidence, normal failure, and
trace-led diagnosis before adding machinery. Mere possibility is insufficient;
a contained programming defect may remain an engineer diagnosis when it has no
public, trust, corruption, or recovery consequence.

Contracts now separates arbitrary or adversarial input, operational failure,
contained programming defects, failures that escape a public or trust boundary,
and authoritative-state corruption. Immediate failure with trace-led diagnosis
is valid for a contained defect when the contract requires neither recovery nor
a typed external outcome. Boundary rejection, typed failure, recovery, panic,
and graceful termination remain valid only when selected by the actual outcome
contract. The existing Validation Proof Lifetime rule remains unchanged: an
intact proof-bearing value is used directly, while mutation, representation
loss, contract change, and a new authority boundary require new proof.

Dependencies now requires an established-tool comparison when standardized
semantics would otherwise be implemented locally. The comparison occurs when
the implementation is created, materially extended, or renewed. It does not
retroactively require deletion of an unchanged accepted implementation. Thin
Adapters may delegate standardized behavior, and domain products may own
distinct local semantics; nominal labels do not establish either case.

These are written decision standards, not an enforcement harness. Adopters
choose whether to apply them through review, existing tools, custom tools, or
no automation.

## Standards-Impact Review

The accepted normative graph contains 51 policy units and 100
standards-to-standards routing relationships, compared with the accepted
Milestone 1 state of 49 units and 68 relationships. Milestone 2 registers two
existing Contracts headings as first-class owners, revises Verification's
Acceptance Claims and Dependencies' Implementation Versus Dependency owners,
adds 32 standards-impact routes, and retains the existing Dependencies to
Generated Contract route after review.

Every routed standard was inspected even though none required copied policy
text:

- Acceptance Claims routes future review to Contracts, Dependencies,
  Diagnostics, Resilience, Security, Planning, Implementation, Documentation,
  Release, Generated Contract, and Persistence.
- Validation Proof Lifetime routes to Generated Contract, IPC, Language
  Bindings, Persistence, Security, Resilience, Verification, Planning, and
  Implementation.
- Invariant Contracts routes to Generated Contract, IPC, Language Bindings,
  Persistence, Verification, Security, Resilience, Diagnostics, Planning, and
  Implementation.
- Implementation Versus Dependency retains Generated Contract and adds
  Planning and Implementation as affected standards.

The target standards already own their local boundary, threat, recovery,
diagnostic, planning, implementation, documentation, release, or persistence
consequences. Repeating the new decision procedures in them would reduce
standard isolation. The edges remain because their purpose is to route a future
agent to inspect potentially affected standards, not to prove that text changed
or to test application software.

## Repository Conformance Evidence

The repository's complete policy projection has 445 relationships. The 345
relationships outside the 100 standards-impact routes are separate conformance,
delivery, routing, and implementation metadata; they are not additional
standards graph boundaries.

- The existing `acceptance-claims` suite gains one 20-case fixture covering
  external input, durable corruption, escaping and contained defects,
  defense-in-depth marginal value, subsumed evidence, construction and type
  proof, trace diagnosis, byte identity, cost, oracle, and retention decisions.
- The existing `contract-invariants` suite consumes 27 invariant-outcome cases
  and the unchanged 16-case proof-lifetime fixture. No parallel suite or
  normative proof-lifetime rewrite was introduced.
- The existing `implementation-versus-dependency` suite consumes 14 lifecycle
  and ownership cases covering thin Adapters, domain products, unchanged local
  implementations, material extension, renewal, and invalid automatic deletion.
- Six new suite/fixture projections are registered separately from the 32 new
  standards-impact relationships. Existing Dependencies conformance projections
  remain in place.

The retained A1c-named relationship-migration fixture received 38 mechanical
additions because its existing checker freezes the repository's complete
projection set. That compatibility bookkeeping neither inspects nor modifies
A1c, does not make A1c a graph consumer, and is not evidence of standards effects
on application software.

## Verification Record

The final candidate passes all 227 registered declarative suites and all 53
retained Bash checkers. The three focused owner suites, policy semantic-impact
checks, generated evidence freshness, plan structure, graph transition check,
and diff hygiene also pass. Generated checker evidence remains at 53 retained
checkers, 57 nodes, 387 conservative reference edges, and 57 components.

The standalone visualization remains in transition state because Milestone 3
is still planned. It reconstructs the fixed 47-unit/62-relationship baseline,
shows the accepted Milestone 1 and Milestone 2 portions, and preserves the
remaining standards-only planned routes without presenting application or
conformance artifacts as standards-impact consumers.
