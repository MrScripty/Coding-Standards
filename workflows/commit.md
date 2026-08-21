# Commit Workflow

**Standards metadata**

- ID: `workflow.commit`
- Role: `workflow`
- Level: `MUST`
- Applies when: A repository change will be committed, local history maintenance is requested, or branch/worktree isolation, integration, lifecycle assessment, or cleanup is being decided or performed.
- Does not apply when: Work is read-only and requires no commit, history, branch, or worktree lifecycle decision.
- Requires: `core`, `workflow.implementation`
- Specializes: `none`
- Verification: Commit authority fixtures and staged-scope review.
- Canonical owner: `workflows/commit.md`

## Per-Commit Boundary

Before every commit:

1. inspect repository status;
2. confirm only the declared slice write set is staged;
3. review the staged diff, generated-file effects, and sensitive-file risk;
4. confirm credentials, secrets, personal configuration, and unintended binary
   artifacts are absent;
5. run the focused and affected verification selected for the slice;
6. update active plan, issue, or ledger state only when current authority,
   lifecycle, blockers, acceptance, next-slice state, an accepted-slice
   boundary, a material deviation, or a material verification result changes;
   do not mirror commit cadence into planning artifacts; and
7. create one atomic conventional commit that describes the coherent outcome.

Per-commit review concerns the index and the current slice. Do not require a
full unpushed-history audit before every atomic commit.

## Branch And Worktree Applicability

Do not require a branch or worktree for every change. Use one when it provides
material isolation for review, concurrent proposals, experimentation, release
maintenance, risk containment, or repository-required checks. The current
integration owner may work directly on the integration branch for a small
serial change when repository controls allow it and no outstanding proposal can
become stale.

Select isolation from those facts, not from file count, commit count, elapsed
time, branch count, worktree count, or a preferred Git ceremony. Preparing work
in another worktree does not make cherry-pick the default integration method.

## Governed Branch Context

For governed branch work, retain enough context to resolve:

- purpose and responsible owner;
- target or integration branch;
- admitted base or revision when concurrency makes it relevant;
- whether the branch is private, shared, or long-lived;
- integration owner; and
- expected terminal disposition.

Use the task, branch name, repository history, plan, pull request, or another
owned artifact that already contains these facts. Do not require a heavyweight
record for a trivial private branch when its name, task, and history make the
contract unambiguous. Missing facts that affect safe integration or cleanup are
`unavailable`; contradictory ownership or target facts are `invalid`.

## Integration Mechanism Selection

Use the least history-transforming mechanism compatible with the accepted
outcome:

- Fast-forward a complete accepted branch when it descends from current target
  authority.
- For a complete private proposal based on stale target authority, an
  authorized owner may rebase it onto fresh authority, resolve conflicts,
  reverify the result, and then fast-forward it.
- Create a merge commit when preserving branch topology has durable review,
  release, or repository value.
- Cherry-pick for selective acceptance, backports, recovery, or another case
  where integrating the complete branch is inappropriate.

Do not cherry-pick merely because work was prepared in another worktree. Do
not rewrite shared or published history without separate explicit authority.
When facts do not support one mechanism, return a history-integration
diagnostic instead of trying another mechanism as fallback.

## Cherry-Pick And Replacement Lineage

When cherry-pick or reconstruction creates a replacement commit, record the
source branch, source commit, accepted replacement commit, integration mode,
verification result, and terminal branch disposition in durable acceptance
evidence. Git ancestry reporting a source commit as unmerged does not prove
that a patch-equivalent accepted replacement remains semantically unintegrated.

Patch equivalence may trigger review, but automated retirement requires an
explicit source-to-accepted mapping. Do not infer acceptance from matching
diffs alone.

## Terminal Branch Lifecycle

Classify every short-lived governed branch or proposal as `integrated`,
`rejected`, `abandoned`, `superseded`, or retained under an explicit long-lived
contract. A retained long-lived branch states its continuing purpose, owner,
synchronization policy, supported consumers, and retirement condition.

Branch refs and worktrees are operational resources, not permanent evidence
databases. Preserve durable rationale and acceptance evidence in commits, pull
requests, issues, plans, ledgers, manifests, or reports. Do not retain a
redundant branch solely to preserve history that durable evidence already owns.

## Worktree Lifecycle And Cleanup Authority

Remove a completed clean worktree when its purpose ends, and prune stale
administrative registrations after confirming that no live worktree owns them.
Never force-remove a dirty, unknown, user-owned, locked, or uniquely committed
worktree through generic automation. Removing a redundant branch ref is not
the same operation or authority as rewriting history reachable by shared refs.

The integration owner may perform predeclared safe cleanup for branches and
worktrees created by the governed task after terminal evidence is recorded.
Delegated workers must not delete resources outside their declared ownership.
Automation may retire a branch only when ownership, integration, and terminal
evidence are unambiguous. Patch-equivalent or cherry-picked branches require
the source-to-accepted mapping before automated retirement. Age and quantity
may trigger review but never independently authorize deletion.

When a governed task creates a worktree, terminal acceptance records its exact
path and classification, then confirms either that the path and its stale
registration are absent from `git worktree list` after safe removal or that an
explicit retained-resource contract names its purpose, owner, and next
disposition. A task-created registration that remains without that contract is
`unavailable` for terminal acceptance. Check only paths created by the task;
this postcondition does not authorize a repository-wide prune or cleanup of
historical, unknown, or other-owner registrations.

Discarding unique commits from a rejected or abandoned branch requires
separate explicit destructive authority naming the branch and unique commits,
confirming they are not accepted, shared, or otherwise required, and recording
the selected recovery or permanent-retirement outcome. Generic cleanup
automation must refuse that operation; rejection alone is not discard
authority.

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

Automation may remind an operator to perform a selected history review and may
report the explicit range, graph, or cumulative diff. It must not infer the
intended base, decide that cleanup is required, or run amend, rebase, reset,
squash, commit-dropping, or topology-changing commands. Missing range or base
facts produce a typed process diagnostic.

## Hook Bypass Authority

Bypassing a repository hook skips an automation mechanism; it does not waive
the underlying implementation, verification, security, or commit obligation.
Permit bypass only when an explicitly authorized procedure identifies the
affected hook, change scope, reason, unmet checks, risk owner, compensating
evidence or containment, and required follow-up.

Record the bypass in the durable location selected by that procedure. A commit
message, emergency label, production incident, tool failure, or operator
urgency does not grant authority by itself. Do not default to a bypass command,
`no-verify` flag, emergency exception, successful no-op, or later repair.

When bypass authority, scope, or required evidence is missing or contradictory,
return a typed process diagnostic and leave the hook enabled. When the selected
procedure cannot be executed in the repository or toolchain, report the
unsupported mechanism rather than silently committing through another path.

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
observable change concisely in imperative mood. The body explains material
rationale, scope, and contract effects when the subject is insufficient.

Keep command logs and verification output in the plan ledger, pull request, or
completion record rather than the commit message.

See the non-normative [Commit Recipe](../reference/recipes/commits.md) for
syntax, staging commands, footer forms, and examples.

## Invalid Outcomes

Stop with a typed process diagnostic when:

- unrelated dirty files overlap or make staged scope ambiguous;
- required verification did not pass;
- the intended base or commit range is unresolved;
- rewrite authority or unshared status is missing;
- recovery of the original history is not established; or
- the requested rewrite would alter shared history;
- branch purpose, target, ownership, or terminal evidence needed for the
  selected operation is unavailable;
- a task-created worktree remains registered without an explicit retained-
  resource contract;
- a replacement commit lacks source-to-accepted lineage; or
- cleanup would affect an unknown, dirty, locked, user-owned, or uniquely
  committed resource.

Do not use reset, stash, amend, rebase, or an unrelated cleanup commit as an
implicit fallback for an unresolved repository state.
