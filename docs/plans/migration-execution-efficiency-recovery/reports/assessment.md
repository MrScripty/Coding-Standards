# Recovery Assessment

## Ownership Diagnosis

The generic standards are not the source of the remaining two-commit migration
ceremony. Planning already defines one coherent slice independently of file or
commit count, and Concurrent Plan Integration applies only to stale-capable
outstanding proposals. The correction belongs to the verification-engine
migration procedure.

Commit already requires terminal worktree cleanup. The missing behavior is a
task-terminal postcondition in implementation projections, not broader cleanup
authority.

## Current Measurements

| Observation | Derived value | Meaning |
| --- | --- | --- |
| Worktree registrations | 385 | Administrative entries, not live directories |
| Prunable registrations | 384 | Historical review scope; not deletion authority |
| Live worktrees | 1 | Canonical worktree only |
| Local branches | 137 | Must not be bulk-deleted |
| Local commits ahead of `origin/main` | 736 | Material backup and review risk |
| Temporary graph | 86 nodes / 86 components | Every current component is singleton |
| Registered declarative suites | 190 | Fast phase suitable for frequent focused/all-declarative checks |
| Retained Bash verifiers | 82 | Mixed checkpoint remains the expensive phase |

## Component Churn

Current component IDs are ordinal positions in the sorted component list.
Deleting one checker changes the position, and therefore the ID, of every later
component. Node rows copy those IDs, while component dependencies and inbound
component references also use them. The values are explicitly non-authoritative,
but their instability creates review and merge noise.

The smallest correction keeps every existing column and derives each component
ID from the exact sorted canonical member set. Unrelated insertion, deletion,
or ordering then leaves existing identities unchanged. Membership changes still
change the affected component identity, which is the correct semantic result.

## Follow-Up Boundaries

- Historical branch and worktree cleanup needs a separate plan, refreshed
  inventory, unique-commit protection, and explicit destructive authority.
- Publishing `main` or a backup ref needs explicit remote-write authority.
- Downstream pilots remain parent Milestone 8 work and are required before
  objective success, not before this internal migration recovery.
