# Milestone 7 Remaining Trust And Lifecycle Re-plan

## Purpose

This planning report replaces the premature Milestone `7.4c` final-closure
handoff. It audits the remaining trust-boundary work and records the lifecycle
dependency exposed by `F025` and `F026`. The accepted generic Concurrency slice
and the subsequent Rust Async decomposition refine its original next-slice
handoff.

This report is planning evidence. It does not own normative concurrency,
security, interop, cross-platform, async, or binding policy.

## Re-plan Trigger

After Milestone `7.4b3g`, the rolling gate still reports:

- 641 undisposed frozen identifiers;
- 31 legacy sources;
- 30 proposed canonical owners;
- 16 missing canonical owners; and
- 90 trust-boundary identifiers across seven remaining owner groups.

Final legacy-index review, disposition closure, and duplication acceptance
cannot begin while those facts remain. The prior `7.4c` next-slice decision is
superseded; `7.4c` remains reserved for actual closure after the rolling
remainder reaches zero.

## Binding Decisions

1. Keep the trust-boundary wave active.
2. Insert a bounded lifecycle bridge before dependent Rust security and
   language-binding consolidation.
3. Establish generic concurrency ownership before the Rust async
   specialization.
4. Do not make async runtime creation, spawned-task ownership, cancellation,
   or shutdown canonical in the Rust language-binding profile. Bindings consume
   the selected lifecycle owner and adapt host mechanisms at the boundary.
5. Do not mechanically accept preliminary owner-map destinations. The
   cross-platform, interop, and Rust binding sources still mix policy,
   workflow, packaging, generated commands, examples, and compatibility
   concerns; each later slice must re-check ownership before disposition.
6. Keep independent trust-boundary groups queued, but name only one next
   integration slice.
7. Keep `7.4c` as final legacy-index and duplication closure, not as the next
   implementation slice.

No compatibility copy, permissive fallback, alternate runtime, untracked task,
or weaker verification path is introduced by this re-plan.

## Remaining Groups

[milestone-7-trust-lifecycle-groups.tsv](milestone-7-trust-lifecycle-groups.tsv)
freezes the current counts and dependencies:

- the seven trust-boundary groups total 90 identifiers;
- generic Concurrency contributes 17 lifecycle identifiers;
- the Rust Async specialization contributes 9 lifecycle identifiers;
- generic owners precede language specializations; and
- owner state records which canonical modules still need to be established.

The lifecycle bridge changes dependency order, not the ownership wave assigned
to either module. It does not authorize general lifecycle or launcher
consolidation ahead of the remaining trust-boundary work.

## Findings And Sequence

- `F025`: async runtime and task lifecycle belong to composition/lifecycle
  owners, while binding adapters own only host adaptation.
- `F026`: spawned work must be tracked, Rust path use must not rely on a
  check-then-use race, and typed errors cannot become catch-all unsupported
  delegation.
- `F016`: the broken graceful-shutdown reference remains assigned to the later
  generic Security/network slice.
- Preliminary destinations for native loading, CI matrices, cross-language
  contract maintenance, binding packaging, generation commands, and version
  publication require owner review before implementation.

The accepted serial dependency sequence is:

1. `7.4b4a`: accept this planning-only re-plan;
2. `7.4b4b`: establish the generic concurrency contract and resolve `F019`;
3. `7.4b4c`: decompose the Rust Async specialization after `7.4b4b`;
4. `7.4b4d` through `7.4b4g`: establish the Rust Async specialization in the
   dependency order frozen by the
   [Rust Async decomposition](milestone-7-rust-async-decomposition.md);
5. decompose dependent Rust binding and Rust security sections against those
   accepted owners through the
   [F025/F026 dependent Rust decomposition](milestone-7-f025-f026-decomposition.md);
   and
6. return to independent trust-boundary groups one owner-bounded slice at a
   time.

Generic Concurrency, Rust Async, and the dependent Rust planning decomposition
are accepted. Only `7.4b5b` is now implementation-ready; later dependent Rust
items remain frozen sequence constraints until their pre-slice review.

## Slice 7.4b4a: Planning-Only Re-plan

**Allowed write set:**

- this report;
- `milestone-7-trust-lifecycle-groups.tsv`;
- `milestone-7-trust-lifecycle-next-slice.tsv`;
- `verify-milestone-7-trust-lifecycle-replan.sh`;
- `milestone-7-decomposition.md`;
- evaluation README, findings, active plan, and execution ledger.

No normative standard, final disposition, owner map, wave inventory, generated
artifact, template, lockfile, package file, runtime integration, or downstream
repository belongs to this slice.

**Acceptance gate:** the checker proves the exact current owner counts, the
90-identifier trust remainder, the 26-identifier lifecycle bridge, the exact
next-slice proposal, zero-or-complete disposition-backed lifecycle handoff, and
parent-decomposition linkage.
Plan lifecycle, shell syntax, whitespace, and all standards-effectiveness
regressions pass.

## Accepted Slice 7.4b4b: Generic Concurrency Contract

[milestone-7-trust-lifecycle-next-slice.tsv](milestone-7-trust-lifecycle-next-slice.tsv)
freezes these identifiers:

- `STD-0263` through `STD-0268`; and
- `STD-0270` through `STD-0272`.

**Outcome:** `topics/concurrency.md` becomes the generic owner for shared-state
coordination, nonblocking async/lifecycle paths, observed failures, and
cancellation propagation.

**Allowed write set:**

- `topics/concurrency.md` (new canonical topic);
- `CONCURRENCY-STANDARDS.md`;
- `STANDARDS-ROUTER.md`;
- `README.md`;
- `evaluation/standards-effectiveness/fixtures/concurrency/ownership-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-concurrency-policy.sh`;
- this re-plan checker for lifecycle/disposition handoff only; and
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No language-specific standard/profile, launcher profile, generated artifact,
template, lockfile, or downstream repository belongs to this slice.

**Required semantics:**

- immutable or otherwise thread-safe data does not acquire a lock merely
  because multiple threads can access it;
- shared mutable invariants use an explicit synchronization, ownership,
  message-passing, atomic, or transactional strategy;
- callbacks and other externally controlled code do not execute while the
  owner holds a lock;
- related invariants remain coordinated without mandating one universal lock;
- async request and lifecycle paths do not perform blocking work directly;
- asynchronous failures have an explicit observation owner;
- cancellation propagates through owned asynchronous work;
- inability to establish required ownership or lifecycle behavior returns the
  operation's typed failure rather than selecting another mechanism; and
- generic policy remains language- and runtime-neutral.

**No fallback:** failed coordination or lifecycle proof cannot use unprotected
shared mutation, fire-and-forget work, callbacks under locks, synchronous
blocking in an async path, discarded errors, ignored cancellation, or a
language-specific mechanism presented as universal policy.

**Focused evidence:** decision fixtures cover immutable data, shared mutation,
callback-under-lock rejection, related invariants, blocking async work,
observed and discarded failures, cancellation propagation, and
language-specific exclusions. The checker validates exact dispositions,
metadata, routing, legacy replacement, and absence of prohibited fallback
examples.

**Acceptance gate:** `F019` is resolved; all nine identifiers have exact final
dispositions; the generic owner is routed; retained language-specific sections
cannot override it; and focused plus affected regressions pass.

## Accepted Slice 7.4b4c: Rust Async Decomposition

[milestone-7-rust-async-decomposition.md](milestone-7-rust-async-decomposition.md)
separates profile applicability, owned runtime lifecycle, blocking/mutex
mechanisms, and cancellation/observability into four serial implementation
slices. It records `F045`, freezes all nine Rust Async identifiers, and fully
specifies only `7.4b4d`.

No normative profile, legacy replacement, final disposition, generated
artifact, runtime integration, package file, or downstream repository changes
in the planning slice.

## Accepted Slice 7.4b5a: Dependent Rust Decomposition

[milestone-7-f025-f026-decomposition.md](milestone-7-f025-f026-decomposition.md)
separates the remaining `F025`/`F026` binding architecture, runtime adaptation,
typed delegation, path-authority, and listener-lifecycle concerns into five
serial implementation slices. It freezes ten undisposed identifiers and fully
specifies only `7.4b5b`.

No normative profile, legacy replacement, final disposition, generated
artifact, package file, lockfile, runtime integration, or downstream
repository changes in the planning slice.

## Re-plan Triggers

- Generic concurrency cannot express the required lifecycle contract without a
  new role or shared taxonomy.
- A proposed identifier must split across canonical owners and one disposition
  cannot represent that split.
- Resolving `F019` requires editing a language-specific or launcher owner.
- The next slice cannot distinguish normative policy from retained
  language-specific reference material.
- Verification cannot reject callbacks-under-lock, blocking, discarded-error,
  or ignored-cancellation fallback.
