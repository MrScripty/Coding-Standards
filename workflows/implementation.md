# Implementation Workflow

**Standards metadata**

- ID: `workflow.implementation`
- Role: `workflow`
- Level: `MUST`
- Applies when: Source, tests, standards, configuration, or generated artifacts will change.
- Does not apply when: The task is read-only analysis.
- Requires: `core`
- Specializes: `none`
- Verification: Focused slice checks, staged-scope review, and objective acceptance.
- Canonical owner: `workflows/implementation.md`

## Before Editing

1. Inspect repository status.
2. Identify one coherent behavior or contract change.
3. Declare the exact write set and affected acceptance evidence.
4. Do not start when unrelated dirty files overlap the write set or make
   verification ambiguous.
5. Read only routed standards and directly affected source context.

When a written plan governs the change, require its explicit canonical
repository-relative `plan.md` path and explicit `start`, `continue`, or `verify`
operation. Consume the Planning workflow's path, operation, lifecycle,
current-authority, and acceptance decisions. Consume revision, stale-state,
compatibility, and reconciliation decisions only when Router applicability
selects the Concurrent Plan Integration profile. Ordinary implementation must
not request or invent those records. Do not scan for a plan, infer an operation,
copy the lifecycle table, or treat a next slice as authority.

A written plan is required when material sequencing, independently owned
contract, migration, coordination, rollout, risk, or acceptance complexity
cannot be held unambiguously in the task. A bounded coherent change may state
its exact write set inline and proceed without a plan. Touching a public,
generated, persistence, process, language, or user-interface boundary does not
by itself require one.

## Slice Contract

Each slice must:

- deliver one usable behavior, contract, or information-architecture outcome;
- preserve the requested objective and current canonical owners;
- avoid compatibility shims, fallback behavior, or duplicate state unless an
  actual contract requires them;
- return typed diagnostics when facts cannot support a valid decision;
- include focused regression or acceptance evidence; and
- leave the repository in a coherent state.

Keep the complete coherent change in one slice unless separation materially
improves independent acceptance, risk containment, dependency ordering,
conflict isolation, rollback, or feedback. Do not split it by file count, layer
count, diff size, or commit cadence. Discovering another directly affected file
does not itself require re-planning; stop only when the discovery changes the
objective, ownership, contract, risk, or acceptance scope.

Do not broaden a slice merely because nearby code could be improved. Record
relevant findings with severity, evidence, owner, and disposition.

## Editing

- Work with existing unrelated changes; never revert them implicitly.
- Update source and its focused tests or fixtures together.
- Update generated artifacts from their source in the same slice.
- Remove replaced behavior when the new canonical behavior is accepted; do not
  retain speculative legacy paths.
- Use comments only for non-obvious invariants, safety, or ownership.
- Request explicit authority before destructive or permission-sensitive work.

## Disabled And Incomplete Behavior

Classify unavailable behavior before editing:

- remove deliberately unsupported capability from every advertised and
  registered surface;
- represent temporary disablement explicitly at the owning boundary; or
- keep incomplete implementation unreachable from production consumers.

Temporary disablement must identify the owning capability, affected surfaces,
reason, tracking authority, conditions for re-enabling or permanent removal,
and a review or expiration trigger when indefinite disablement is not part of
the product contract. Record this authority where maintainers and affected
consumers can discover it; do not require a copied comment template, one
configuration location, or a workaround when none is valid.

A flag, configuration value, route registration, command, control, or published
capability must agree with the selected lifecycle state. Do not advertise or
register unavailable behavior and then return empty data, dummy values, false
success, a silent no-op, or an unrelated substitute. Test-only placeholders
must be isolated by the test boundary and must not become production behavior.

Return the owning boundary's typed `unavailable`, `unsupported`, or `invalid`
outcome when a requested capability cannot be provided. Missing lifecycle
ownership, tracking authority, or re-enable/removal criteria is `unavailable`;
do not infer them or preserve an incumbent stub as fallback.

## Verification

Use [Verification Workflow](verification.md).

Verification must cover the changed behavior and any boundary whose contract
changed. A passing build, startup smoke, or method-level test is not a substitute
for the selected acceptance level.

## Change-Description Evidence

Select the change context reviewers and integrators require from affected risk,
contracts, accepted decisions, alternatives, behavioral effects, migration or
operational consequences, and Verification claims. Identify the owned artifact
for each required fact and link durable rationale rather than copying it into a
temporary review record.

The selected evidence may reside in an active plan, change request, review
record, commit, issue, or another project-owned artifact. Its location does not
change what the evidence proves. Require a problem statement, constraints,
rationale, alternatives, behavioral summary, or verification result only when
the affected facts make that information material.

Do not default to a pull request, hosting provider, template, fixed headings,
checkbox list, command, or duplicated durable rationale. A template transports
selected evidence; empty headings and checked boxes are not evidence.

Contradictory evidence or ownership requirements are `invalid`. Missing required
context, rationale, acceptance evidence, or owning artifact is `unavailable`.
A review mechanism unable to represent or link the selected evidence is
`unsupported`; do not substitute a conventional template, omit the fact, or
infer successful review from template completion.

## State And Findings

When an active plan exists:

- follow [Planning Workflow](planning.md);
- keep objective, current decisions, lifecycle state, blockers, and exactly one
  next slice current;
- update the active plan when current authority, lifecycle, blockers,
  acceptance, or next-slice state changes;
- update `execution-ledger.md` at accepted-slice boundaries and for material
  deviations or verification results;
- do not edit planning artifacts solely because another commit is created;
- put findings and dispositions in `issues.md`;
- transition `Implemented` to `Verifying` and then `Accepted` only when the
  named evidence passes;
- replace superseded decisions rather than appending competing authority; and
- stop for re-planning when evidence changes scope, ownership, objective, or
  acceptance fidelity.

Without an active plan, record out-of-scope issues in the repository's normal
issue or review artifact rather than expanding the change silently.

## Commit Boundary

Follow the [Commit Workflow](commit.md). Implementation owns the coherent slice;
the commit workflow owns staged review, branch and worktree applicability,
integration mechanism, branch-history review scheduling, terminal lifecycle,
cleanup authority, and rewrite authority.

History maintenance is not an implicit implementation right. Never rewrite
shared history.
