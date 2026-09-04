# Milestone 7 Row 46 Rust Authority Closure

## Re-plan Finding

`STD-0827` through `STD-0830` cannot close as one mechanical index update.
`STD-0830` combines baseline routing with API, async, unsafe, feature-contract,
benchmark, performance-claim, verification, and tooling concerns already owned
by canonical specialized modules. The Rust profile also retains a "Detailed
Guidance During Migration" section that declares fully migrated legacy files
canonical.

`languages/rust/RUST-STANDARDS-ADOPTION-NOTES.md` is classified as a
non-normative reference but still states active defaults, including mandatory
Criterion, and routes readers back to `RUST-STANDARDS.md`. It has no inbound
consumer outside the corpus inventory. Leaving it in place would preserve
competing legacy authority after row 46.

## Owner Contract

`profiles/languages/rust/README.md` owns Rust applicability, baseline Rust
verification, and routing to specialized Rust mechanisms. It does not acquire
API, async, unsafe, dependency, release, tooling, performance, verification,
security, interop, binding, or target authority merely because the legacy Rust
index grouped those concerns.

The specialized profiles and generic owners remain canonical. Missing or
contradictory routing facts return a typed diagnostic; the base profile cannot
select a nearby legacy document or convenient default.

## Exact Outcomes

- `STD-0827` becomes one `index` disposition to the canonical Rust profile.
- `STD-0828` becomes one `index` disposition; the manual legacy document table
  becomes concise navigation through the canonical Rust profile.
- `STD-0829` becomes one `split` disposition. The Rust profile owns only the
  specialization boundary and routing; generic owners retain generic policy.
- `STD-0830` becomes one `split` disposition. The Rust profile owns baseline
  routing while Rust API, Async, Unsafe, Tooling, Performance, Verification,
  and other selected owners retain their established contracts.

Every identifier receives exactly one disposition. A split disposition records
delegation; it does not copy specialized rules into the base profile.

## Ordered Children

1. `46.1` removes legacy-authority wording from the canonical Rust profile,
   adds typed no-legacy routing, creates focused profile-authority evidence,
   and registers that verifier in the exact README-consumer inventory. At the
   time of acceptance it was the 34th consumer. Because this amended a shared
   audit contract, the child ran the complete fail-fast suite.
2. `46.2` deletes the obsolete adoption-notes reference, removes its exact
   corpus row, and adds retirement evidence proving no active file or corpus
   route remains. Generated baseline inventories remain frozen history.
3. `46.3` rewrites `RUST-STANDARDS.md` as a concise non-normative migration
   index, records the four exact dispositions, adds focused Rust-index closure
   evidence, closes row 46 and P38, and advances to immutable row 47.

Children are serial because they share row-46 evidence and because the first
child changes the shared README-consumer contract. Planning acceptance does not
change a source, owner, disposition, corpus row, or consumer manifest.

## Consumer Audit Impact

`verify-rust-profile-authority-closure.sh` will directly inspect the canonical
Rust profile README and is the only new direct README consumer. It receives the
existing `rust-profile-index` classification. The historical acceptance event
increased the exact inventory from 33 to 34. The adoption-retirement and
Rust-index verifiers consume that accepted checker rather than creating
additional direct README consumers.

The consumer manifest, audit schema, and historical row-35 evidence remain
serial integration-owner files. The live manifest may shrink as checkers retire
or migrate. The root consumer audit exclusively owns current membership and
derives its current count; row 46 owns only the exact introduced consumer
identity and classification. Existing classifications are unchanged.

## Bounded Write Sets

Planning may touch only this decomposition, owner-validation fixture and
checker, active plan, and execution ledger.

Child `46.1` may touch only the canonical Rust profile, new profile-authority
verifier, README-consumer manifest and audit checker, row-35 checker, row-46
checker, plan, and ledger. Child `46.2` may touch only the adoption-notes file
through deletion, corpus inventory, new retirement verifier, row-46 checker,
plan, and ledger. Child `46.3` may touch only the legacy Rust index, exact
disposition table, new Rust-index verifier, row-46 checker, plan, and ledger.

Specialized canonical owners, generated inventories, immutable train, package
manifest, other consumers, templates, configuration, lockfiles, and downstream
repositories remain read-only.

## Verification Gates

Planning requires exact row and P38 identity, four undisposed source IDs,
current legacy-authority and stale-reference detection, canonical owner
metadata, prospective verifier uniqueness, the historical 33-to-34 consumer
transition and the current exact root-consumer audit,
accepted Rust API, Async, Unsafe, Tooling, Router, and execution-train evidence,
plan structure, shell syntax, and diff integrity.

Each child requires focused source, ownership, no-fallback, and write-set
evidence. Child `46.1` and final child `46.3` run the complete fail-fast suite;
`46.2` runs focused corpus and authority checks. Final acceptance additionally
requires four unique dispositions, no adoption-note file or corpus route,
non-normative index purity, P38 closure, and row-47 activation.

## Typed Outcomes And No Fallback

Do not preserve legacy authority, mandatory Criterion, universal sync/async or
unsafe defaults outside their canonical contracts, manual when-to-use tables,
generic-policy override by proximity, legacy adoption routing, undisposed
identifiers, or a generated-inventory rewrite that treats current cleanup as a
change to the frozen baseline.

Unknown owner, applicability, mechanism, or capability facts remain typed
`unavailable`; contradictory routing is typed `invalid`; an unsupported
mechanism is typed `unsupported` through its owning contract.

## Re-plan Triggers

Stop if canonical specialized owners lack a required semantic contract,
adoption notes have a demonstrated external consumer, deletion requires
preserving a compatibility route, the corpus cannot record retirement without
rewriting frozen generated evidence, more than one direct README consumer is
required, implementation needs files outside a child write set, or focused
evidence cannot prove closure without weakening an accepted owner.
