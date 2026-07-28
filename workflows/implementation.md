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
2. Identify the smallest useful behavior or contract change.
3. Declare the exact write set and affected acceptance evidence.
4. Do not start when unrelated dirty files overlap the write set or make
   verification ambiguous.
5. Read only routed standards and directly affected source context.

A large plan is required when sequencing, ownership, migration, concurrency, or
cross-layer acceptance cannot be held unambiguously in the task. A bounded local
fix may proceed without one.

## Slice Contract

Each slice must:

- deliver one usable behavior, contract, or information-architecture outcome;
- preserve the requested objective and current canonical owners;
- avoid compatibility shims, fallback behavior, or duplicate state unless an
  actual contract requires them;
- return typed diagnostics when facts cannot support a valid decision;
- include focused regression or acceptance evidence; and
- leave the repository in a coherent state.

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

## Verification

Use [Verification Workflow](verification.md).

Verification must cover the changed behavior and any boundary whose contract
changed. A passing build, startup smoke, or method-level test is not a substitute
for the selected acceptance level.

## State And Findings

When an active plan exists:

- keep objective, current decisions, status, blockers, and next slice current;
- put dated command output and completed-slice detail in its execution ledger;
- replace superseded decisions rather than appending competing authority; and
- stop for re-planning when evidence changes scope, ownership, or objective.

Without an active plan, record out-of-scope issues in the repository's normal
issue or review artifact rather than expanding the change silently.

## Commit Boundary

Before committing:

1. Confirm only the declared write set is staged.
2. Review the staged diff.
3. Run affected checks.
4. Use one conventional commit describing the coherent outcome.
5. Do not include command logs in the commit message.

History cleanup is a maintainer action, not an implicit implementation right.
Never rewrite shared history.
