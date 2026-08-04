# Milestone 7 Row 25 Implementation Prompt Decomposition

## Owner Contract

`workflows/implementation.md` is the sole projection owner for the versioned
implementation prompt. Frozen snapshot sections establish identifier lineage
only; they do not override current canonical workflow authority.

Planning owns active-plan state, findings, delegation, and re-planning;
Verification owns evidence and acceptance; Commit owns staged review and commit
procedure. The prompt routes through Implementation and cannot copy those
contracts, preserve a legacy checklist, or act as a second router.

## Exact Dispositions

`STD-0852` through `STD-0858` receive exact `index` dispositions to
`workflows/implementation.md`. No normative movement is required because the
useful snapshot semantics already exist in canonical workflows.

## Ordered Children

1. `25.1a`: establish Planning-owned `start`, `continue`, and `verify`
   admission plus explicit repository-relative plan identity consumed by
   Implementation, with focused no-inference evidence.
2. `25.1b`: replace the tracked checklist with one thin, versioned,
   path-neutral Implementation entrypoint; record seven exact dispositions and
   focused positive and negative projection evidence.

Child `25.1a` may touch Planning, Implementation, its focused fixtures/checker,
plan, and ledger. Child `25.1b` may touch the prompt, dispositions, focused
fixtures/checker, plan, ledger, and affected shared cursor assertions.

## Child 25.1 Plan Identity Replan

The invocation must supply one explicit repository-relative `plan.md` path.
Implementation owns identity presence and plan semantics. Security owns path
resolution, canonicalization, traversal and symlink-escape rejection,
containment, and validation/use safety. Cross-Platform applies conditionally
when filesystem representation affects resolution. Planning owns plan
structure, implementable lifecycle state, linked artifact consistency, and
exactly one next slice.

Missing identity is Implementation `unavailable`; contradictory identity is
Implementation `invalid`; traversal or repository escape is Security `invalid`;
missing root or resolution facts are Security `unavailable`; unsupported
filesystem mechanics are Security `unsupported`; invalid plan structure is
Planning `invalid`, and missing required plan facts are Planning `unavailable`.

Implementation links to these owners and does not copy their algorithms. Do not
scan for an active plan, select by filesystem order or recency, infer a
conventional path, use conversation history as authority, or create a
repository-global pointer. A future default-selection mechanism requires
downstream evidence and a separate replan.

## Child 25.1 Lifecycle Admission Replan

The invocation supplies one explicit operation. Planning owns admission:

- `start` accepts only `Planned` and transitions it to `Active`;
- `continue` accepts only `Active` and preserves that state; and
- `verify` accepts `Implemented` or `Verifying` and transitions
  `Implemented` to `Verifying` when verification begins.

`Blocked` is `unavailable` with its blocker. `Deferred` is `unavailable` until
its revisit authority activates it. `Accepted` and `Superseded` are `invalid`
for execution; a known replacement is diagnostic context only. Missing or
inferred operation is `unavailable`, and a state/operation mismatch is
`invalid`. The presence of a next slice does not grant execution authority.

Implementation transports the explicit operation and consumes Planning's
decision without copying this admission table. The accepted transition and its
ledger update occur in the same coherent slice.

## Child 25.1 Concurrent Admission Replan

Admission includes an explicit expected revision of the selected plan.
Planning owns the decision against that revision; Concurrency owns stale-read
and conditional-transition semantics. The serial integration owner alone may
change shared plan and ledger state. Delegated workers receive read-only plan
context and cannot advance lifecycle state.

Before transition or next-slice advancement, compare the authoritative current
revision with the admitted revision and apply the state change only when they
match. A mismatch is `invalid` stale admission and requires rereading the plan
and obtaining a new decision. Do not retry the old operation automatically.
This contract protects plan-state mutation; it does not reserve external
resources, prevent independent analysis, or authorize overlapping write sets.

Do not introduce lock files, leases, scheduler infrastructure, state-only Git
commits, or duplicate execution with later reconciliation as fallback.

## Re-plan Triggers

Stop if the expected-revision representation has no canonical source or cannot
support conditional replacement, plan identity requires repository-global
mutable state, snapshot
lineage must be regenerated, the prompt needs an independent
lifecycle or generation system, copied canonical procedure must remain, one
identifier needs multiple dispositions, or implementation requires files
outside the approved write set.
