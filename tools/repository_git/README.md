# Repository Git

`repository_git` is a repository-neutral Adapter for bounded Git subprocess
execution, exact object reads, current-`HEAD` binding, explicit gitlink
traversal, Git-index observations, and isolated expected-target publication.

The package owns no standards semantics, snapshot lifecycle, SQLite storage,
or public Engine operation. Callers resolve one revision and retain that exact
value while loaders request files. Worktree changes and later commits cannot
substitute bytes for the retained revision.
The Adapter can also return the exact sorted path observation for a retained
commit tree; callers persist that observation when later deterministic
projections must survive worktree or branch replacement.

Write-capable callers provide one exact base revision and path-component-safe
replacement values. The Adapter creates a private local clone, preserves
tracked executable modes, constructs a deterministic conventional commit, and
checks the candidate filesystem and index against that object. Publication
accepts only a still-active candidate issued by that Adapter instance,
revalidates it, imports its objects without a destination ref, and
updates only `refs/heads/main` through Git's expected-old-object
compare-and-swap. Replacement staging uses literal path semantics, and the
private clone retains no canonical-repository remote. The source worktree and
index are not staging authority.

All Git subprocesses receive a sanitized environment, bounded output, and a
fixed timeout. Missing objects are `unavailable`; malformed or contradictory
objects are `invalid`; unsupported object modes, path encodings, and output
sizes are `unsupported`.

Git remains the established implementation for object resolution and reported
object type. This Adapter locally interprets only the leading commit-tree field
and raw tree-entry framing so it can verify exact returned object hashes and
traverse explicitly mapped gitlinks without pathspec or worktree semantics. The
read-only implementation-versus-dependency comparison is recorded in the
[A1c corrective decision](../../docs/plans/standards-engine-a1c-repair/reports/dependency-and-version-decisions.md).
The write-capable re-evaluation is recorded in the
[A2 decision](../../docs/decisions/standards-engine-a2.md#repository-git-dependency-re-evaluation).
Re-evaluate again before materially extending the selected local publication
contract.
