# Cleanup Authority Boundary

The accepted branch-lifecycle snapshot recorded 137 branches and 353 worktree
registrations. Current planning-time observation reports 137 branches and 385
worktree registrations, including 384 marked prunable by Git. These counts are
derived observations, not cleanup authority.

This plan deliberately separates:

- refreshing current facts;
- pruning an administrative registration;
- removing a filesystem worktree;
- deleting a redundant branch ref; and
- discarding unique or shared history.

Plan creation authorizes none of those mutations. The prior inventories under
`docs/plans/git-branch-lifecycle-policy/` remain historical evidence and seed
the next review, but every mutable fact must be refreshed after explicit plan
start.
