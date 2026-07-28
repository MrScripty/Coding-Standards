# Commit Workflow

**Standards metadata**

- ID: `workflow.commit`
- Role: `workflow`
- Level: `MUST`
- Applies when: A repository change will be committed or local history maintenance is explicitly requested.
- Does not apply when: Work is read-only and creates no repository change.
- Requires: `core`, `workflow.implementation`
- Specializes: `none`
- Verification: Commit authority fixtures and staged-scope review.
- Canonical owner: `workflows/commit.md`

## Per-Commit Boundary

Before every commit:

1. inspect repository status;
2. confirm only the declared slice write set is staged;
3. review the staged diff and generated-file effects;
4. run the focused and affected verification selected for the slice;
5. update active plan, issue, and ledger state when those artifacts exist; and
6. create one atomic conventional commit that describes the coherent outcome.

Per-commit review concerns the index and the current slice. Do not require a
full unpushed-history audit before every atomic commit.

## Branch-History Review

Review the complete branch range at boundaries where its sequence matters:

- milestone or implementation-wave closure;
- pre-push;
- pull-request preparation or update;
- release preparation; or
- an explicit history-maintenance request.

Use an explicit intended base and inspect the commit graph, staged/unstaged
state, and cumulative diff. Identify accidental regressions followed by fixes,
misleading boundaries, fixup commits, and unintended merge topology.

History review produces findings. It does not itself authorize rewriting.

## Rewrite Authority

Rebase, amend, reset, squash, commit dropping, and merge-topology rewriting
change existing history. Perform them only when all conditions hold:

- the maintainer or user explicitly authorized the rewrite and its scope;
- the exact commit range and intended base are known;
- every affected commit is confirmed unshared and unpushed;
- no collaborator, worktree, automation, or dependent branch relies on the
  existing commit IDs;
- the original tip is preserved in a named recoverable Git reference;
- the worktree and index state are understood and preserved; and
- affected verification will be rerun after the rewrite.

If any fact is unknown, return a history-maintenance diagnostic and leave the
existing commits intact. Never infer rewrite authority from a request to
implement, commit, clean up, or prepare a pull request.

Shared or pushed history is immutable under this workflow. Correct it with a
new atomic commit unless the repository owner invokes a separate,
explicitly-governed emergency procedure.

## Topology

Linear-history cleanup and merge-topology rewriting are different operations.
When an authorized range contains merges:

- preserve or intentionally replace integration semantics;
- use merge-aware tooling;
- inspect the graph before and after;
- verify every retained parent relationship; and
- stop if the intended topology is ambiguous.

Do not flatten merges as a default cleanup strategy.

## Commit Message

Use the repository's conventional commit format. The subject states the
observable change in imperative mood. The body explains material rationale,
scope, and contract effects when the subject is insufficient.

Keep command logs and verification output in the plan ledger, pull request, or
completion record rather than the commit message.

## Invalid Outcomes

Stop with a typed process diagnostic when:

- unrelated dirty files overlap or make staged scope ambiguous;
- required verification did not pass;
- the intended base or commit range is unresolved;
- rewrite authority or unshared status is missing;
- recovery of the original history is not established; or
- the requested rewrite would alter shared history.

Do not use reset, stash, amend, rebase, or an unrelated cleanup commit as an
implicit fallback for an unresolved repository state.
