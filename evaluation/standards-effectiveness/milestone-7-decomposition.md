# Milestone 7 Rolling Decomposition

## Purpose

This report decomposes the remaining role migration into dependency-ordered
waves while keeping the active plan concise. It is planning evidence, not a
normative standards owner.

At Milestone 7.3d acceptance, 698 frozen identifiers remained across 33 source
files and 33 proposed canonical owners. Eight proposed owners already existed;
25 did not. The preliminary owner map is an audit input, not authority for a
mechanical move.

## Binding Sequence Decisions

1. Use rolling-wave decomposition. The report fixes domain order while the
   active plan fully specifies only the next implementation slice.
2. Correct unsafe or contradictory guidance before making affected text
   canonical.
3. Establish generic topics and boundary profiles before language
   specializations that depend on them.
4. Create a missing owner only with a useful policy/profile/reference result;
   empty owner stubs are prohibited.
5. Bound slices by one observable contract. A slice may cross legacy sources
   or canonical modules only when atomic replacement is required to eliminate
   competing guidance.
6. Treat source-file closure as a consequence, not a sequencing goal.
7. Keep the active plan, shared dispositions, router, metadata contracts, and
   shared fixtures under one serial integration owner.
8. Replace moved legacy text with links or a demonstrated migration index.
   Do not retain compatibility copies or fallback rules.

## Wave Map

[milestone-7-waves.tsv](milestone-7-waves.tsv) assigns every remaining proposed
owner to exactly one wave. Counts describe the frozen identifiers still
associated with each proposed owner; they do not pre-approve final
dispositions.

| Wave | Remaining IDs | Primary outcome |
| --- | ---: | --- |
| Trust boundaries | 137 | Resolve critical containment, validation, FFI, conversion, and unsafe-contract findings. |
| Lifecycle and runtime | 59 | Resolve lock safety, task ownership, runtime ownership, and recovery semantics. |
| Process and dependencies | 334 | Consolidate universal, planning, implementation, verification, tooling, and dependency ownership. |
| Application and boundaries | 84 | Complete concern and application/boundary profiles. |
| Reference and index closure | 84 | Extract non-normative catalogs, close routing indexes, and run final duplication review. |

Within a wave, an accepted slice may reveal a dependency that changes later
ordering. Record the evidence, replace the affected later sequence, and retain
only one next slice.

## First Implementation Slice: 7.4b1

**Outcome:** Canonical filesystem containment and platform path-identity
contracts replace unsafe string-prefix guidance atomically.

**Frozen identifiers:** The exact proposal is recorded in
[milestone-7-first-slice.tsv](milestone-7-first-slice.tsv):

- `STD-0289` through `STD-0293`;
- `STD-0584` through `STD-0587`.

**Allowed write set:**

- `topics/security.md` (new canonical security topic);
- `topics/cross-platform.md` (new canonical cross-platform topic);
- `SECURITY-STANDARDS.md`;
- `CROSS-PLATFORM-STANDARDS.md`;
- `STANDARDS-ROUTER.md`;
- `README.md`;
- focused containment decision fixtures and checker;
- consolidation dispositions, evaluation README, findings, plan, and ledger.

No language profile, reference recipe, metadata schema, generated inventory,
template, lockfile, or downstream repository belongs to this slice.

**Required semantics:**

- containment is component-boundary-aware and cannot use string-prefix tests;
- canonical identity accounts for symlinks and platform filesystem behavior;
- trusted root and candidate resolution semantics are explicit;
- creation beneath a non-existing target is anchored through an existing,
  validated parent or a stronger platform capability;
- operation-time race exposure is addressed by capability/handle-relative
  operations or revalidation appropriate to the threat model;
- display normalization is not treated as filesystem identity;
- case and Unicode comparison follow the actual filesystem contract rather
  than one universal comparison mode; and
- inability to establish safe containment returns a typed diagnostic instead
  of accepting, guessing, or falling back.

Unsafe C# and TypeScript examples are removed, not preserved as reference.
Cross-platform guidance owns construction and platform identity; Security owns
untrusted containment. Neither topic overrides the other.

**Focused evidence:**

- decision fixtures cover traversal, sibling-prefix confusion, symlink escape,
  canonical-root handling, non-existing targets, platform comparison facts,
  and unresolved-safe-resolution diagnostics;
- exact disposition coverage for the nine frozen identifiers;
- metadata/dependency checks for both new topics;
- router and legacy-link checks;
- rejection checks for `StartsWith`/`startsWith` containment examples and
  normalization-only security claims; and
- affected global ownership, routing, link, plan, and whitespace regressions.

**Acceptance gate:** Finding `F017` is resolved; no active or canonical
guidance presents lexical string-prefix comparison as filesystem containment;
both topic owners route deterministically; every affected identifier has one
final disposition; all focused and affected regressions pass.

## Later-Wave Expansion Rule

Critical payload-validation finding `F018` is decomposed in
[milestone-7-f018-decomposition.md](milestone-7-f018-decomposition.md). Its
generic runtime-decoding contract must be accepted before its IPC
specialization, and both slices precede the next trust-boundary finding.

Critical foreign-memory and binding-conversion findings `F022` and `F023` are
decomposed in
[milestone-7-f022-f023-decomposition.md](milestone-7-f022-f023-decomposition.md).
Generic Interop and Language Binding profiles precede Rust Interop, Security,
Unsafe, and Language Binding specializations. Those six slices remain serial
until both findings are resolved.

After those critical slices were accepted, the rolling gate still reported 90
trust-boundary identifiers and exposed a lifecycle dependency across `F025` and
`F026`. The
[remaining trust and lifecycle re-plan](milestone-7-trust-lifecycle-replan.md)
supersedes the premature final-closure handoff. Generic Concurrency and then
Rust Async precede dependent Rust Security and Language Binding consolidation;
this bounded bridge does not authorize general later-wave expansion.

After generic Concurrency was accepted, the
[Rust Async decomposition](milestone-7-rust-async-decomposition.md) split the
nine specialization identifiers into applicability, owned lifecycle,
blocking/mutex, and cancellation/observability slices. After those slices were
accepted, the
[F025/F026 dependent Rust decomposition](milestone-7-f025-f026-decomposition.md)
froze and completed the ten binding and security identifiers that consume
those owners.

The
[independent trust-boundary re-plan](milestone-7-independent-trust-replan.md)
records the 56-identifier pretrain remainder across six proposed-owner groups after
accepting Rust Cross-Platform, event registration, Rust serialized wire
representation, and the Rust external-input queue contract. Its 61-ID frozen
baseline records accepted `STD-0473`, `STD-0757`, `STD-0824`, `STD-0583`, and
`STD-0601` explicitly. Validation proof lifetime now belongs to Contracts,
while Security owns the consequences of untrusted input. The other Security,
Cross-Platform, Interop, Rust Security, and Rust Language Binding rows stay
blocked on decomposition, final index closure, or missing ownership; the next
planning-only slice established a 47-cluster execution train. Bounded
pre-slice review now occurs at each train cursor and proceeds directly to one
atomic implementation commit when accepted. A separate planning commit is
required only when owner, dependency, scope, or acceptance evidence invalidates
the manifest row.

The
[execution train](milestone-7-execution-train.tsv) covers all 589 remaining
identifiers at train establishment exactly once across five dependency waves.
The manifest is immutable: exact dispositions derive a contiguous completed
prefix and the first wholly remaining cluster is the active cursor. When
pre-slice review finds a mixed-role baseline row,
[milestone-7-execution-decomposition.tsv](milestone-7-execution-decomposition.tsv)
adds ordered owner-coherent children without changing or truncating the
baseline manifest. Children must cover their baseline row exactly, and partial
or out-of-order child disposition is invalid. Every logical cluster runs
focused evidence. Complete fail-fast verification runs at each wave checkpoint
and whenever shared contracts, checker infrastructure, routing, metadata, or
generated artifacts change.

Before starting each later wave:

1. inspect repository status and accepted dependencies;
2. identify the highest-severity unresolved finding in that wave;
3. define one observable owner/contract outcome and exact frozen identifiers;
4. record final dispositions and an exact write set;
5. name focused fixtures and objective-relevant gates;
6. update this report only when wave order or ownership changes; and
7. set exactly one next slice in the active plan.

Do not enumerate hundreds of speculative commits. Do not enter a later wave
while an earlier wave has an unresolved critical finding unless recorded
evidence proves the work independent.

## Re-Plan Triggers

- A proposed owner would duplicate or override an accepted owner.
- Correctness requires a new role, precedence level, or shared taxonomy.
- A frozen section must split across owners and the disposition record cannot
  represent the split without ambiguity.
- A slice needs files outside its approved owner/fixture/index boundary.
- Generic policy cannot be accepted before a specialization needs it.
- A legacy index would retain normative or executable fallback guidance.
- Verification cannot distinguish moved semantics from removed unsafe examples.
