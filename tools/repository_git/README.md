# Repository Git

`repository_git` is a repository-neutral Adapter for bounded Git subprocess
execution, exact object reads, current-`HEAD` binding, explicit gitlink
traversal, Git-index observations, and isolated expected-target publication.

The package owns no standards semantics, snapshot lifecycle, SQLite storage,
or public Engine operation. Callers resolve one revision and retain that exact
value while loaders request files. Worktree changes and later commits cannot
substitute bytes for the retained revision.

`read_session(revision)` gives one bulk-read owner bounded reuse of fully
verified Git objects. The owner closes the session when its operation ends.
Entries are keyed by the configured repository, object ID, expected object type,
and hash algorithm. Each miss performs the ordinary header, size, framing,
and object-hash checks. Path, mode and explicit gitlink interpretation still
run for every file request. A fresh session verifies its first reads again.

The defaults retain at most 8 MiB of object payload and 1,024 entries; callers
may select smaller bounds or zero retention. Entry bookkeeping is bounded by
the entry cap separately from payload. Evicted and oversized valid objects use
the same verified read path. The session is single-owner and contains no child
process beyond those already owned by an individual Git command. Earlier
verified objects remain immutable operation inputs; the session is not a
continuous audit of the underlying disk. Ordinary `read_file` retains its
independent, uncached observation boundary.

The Adapter can also return the exact sorted path observation for a retained
commit tree; callers persist that observation when later deterministic
projections must survive worktree or branch replacement.

Write-capable callers provide one exact base revision, path-component-safe file
values with explicit executable decisions, exact removals, and one validated
conventional commit message. The Adapter creates a private local clone, writes
blobs and the candidate index without traversing caller-selected filesystem
paths, rejects conflicting or no-effect topology, constructs a deterministic
commit from the exact parent, tree, and message, and checks the candidate
filesystem and index against that object. An active candidate can be
revalidated after an external read-only check and is revalidated again before
publication. File-size observation precedes content reads, so verifier drift
cannot bypass the candidate object bound. An explicit removal plus addition
represents relocation; the Adapter does not infer rename semantics. Publication
accepts only a still-active candidate issued by that Adapter instance,
revalidates it, imports its objects without a destination ref, and
updates only `refs/heads/main` through Git's expected-old-object
compare-and-swap. Removal staging uses literal path semantics, and the
private clone retains no canonical-repository remote. The source worktree and
index are not staging authority.

Candidate blobs and the constructed commit must fit the same object bound used
by exact reads, so publication cannot create content that a subsequent Adapter
read rejects by size. All Git subprocesses receive a sanitized environment,
bounded output, and a fixed timeout. Missing objects are `unavailable`;
malformed or contradictory objects are `invalid`; unsupported object modes,
path encodings, and output sizes are `unsupported`.

Git remains the established implementation for object resolution and reported
object type. This Adapter locally interprets only the leading commit-tree field
and raw tree-entry framing so it can verify exact returned object hashes and
traverse explicitly mapped gitlinks without pathspec or worktree semantics. The
read-only implementation-versus-dependency comparison is recorded in the
[A1c corrective decision](../../docs/archive/plans/standards-engine-a1c-repair/reports/dependency-and-version-decisions.md).
The write-capable re-evaluation is recorded in the
[A2 decision](../../docs/decisions/standards-engine-a2.md#repository-git-dependency-re-evaluation).
Re-evaluate again before materially extending the selected local publication
contract.
