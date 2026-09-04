# Detached-Head Reachability Reconciliation

## Reconstructed Set

The pre-cleanup branch and worktree inventories contain 208 distinct detached
worktree heads. Git ancestry from the 136 recorded branch tips classifies:

- 61 detached heads as reachable from at least one recorded branch tip; and
- 147 detached heads as registration-only in the recorded pre-cleanup state.

Eleven of the registration-only heads are the exact OIDs reported by review as
previously classified unique. The contextual inventory is
[protected-detached-heads.tsv](../inventories/protected-detached-heads.tsv).

These counts are report projections, not stored acceptance inputs. The exact
OID rows and refs are authoritative.

## Protection

All 208 detached heads are protected conservatively under exact
`refs/recovery/historical-worktrees/<short-oid>` refs. The four-column
[protected OID manifest](../inventories/protected-oids.tsv) records each OID as
`archived`; no row uses discard authority.

The reusable verifier reported:

```text
Verified protected OID set: total=208 protected=208 discard_authorized=0
```

For every row it proved that the OID exists as a commit and that the named
archive ref resolves to that exact OID. It did not use reflogs, worktree
registrations, dangling-object suppression, or inferred patch equivalence.

## Corrected Evidence Boundary

The historical `git fsck --no-dangling` result remains object-integrity
evidence only. It did not establish whether an OID remained reachable from a
retained ref after administrative pruning. Current acceptance compares the
explicit pre-cleanup protected set with exact post-recovery refs.

No garbage collection, object pruning, branch deletion, worktree mutation,
history rewrite, or remote operation occurred during recovery. Removing these
recovery refs requires separate future authority after every OID has another
accepted retained, archived, or discard-authorized disposition.
