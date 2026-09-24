# Repository Git

`repository_git` is a repository-neutral Adapter for bounded Git subprocess
execution, exact object reads, current-`HEAD` binding, explicit gitlink
traversal, Git-index observations, and isolated expected-target publication.

The package owns no standards semantics, snapshot lifecycle, SQLite storage,
or public Engine operation. Callers resolve one revision and retain that exact
value while loaders request files. Worktree changes and later commits cannot
substitute bytes for the retained revision.

`read_session(revision)` owns one bounded batch reader and an LRU of verified
objects and decoded trees. Requests remain pinned to the selected revision.
Each cache miss reads a frame from `git cat-file --batch`, then checks header,
size, type, body framing and object hash. Decoded trees retain that verified
object's interpretation; path/mode/gitlink decisions still run for every file.
A fresh session verifies its first reads again. Ordinary `read_file` retains
its independent one-shot observation boundary.

The defaults retain at most 8 MiB of raw payload plus accounted decoded-tree
allocations, and 1,024 entries. Entry bookkeeping is bounded separately by the
entry cap. Oversized values use the same verified uncached path. A session owns
at most one child at a time: crossing an explicit gitlink repository closes the
previous child's stream and lazily starts the selected one. This bounds process
and pipe population independently of the number of repository mappings.

A dedicated exchange worker and bounded stderr drain keep blocking pipe work
inside the existing per-command timeout. Each request gets its own deadline;
there is no total capture deadline. Normal close verifies stdout EOF and exit
status and joins workers. Exceptions abort the owned child (and its process
group on POSIX), join workers and release retained state. A later explicit read
can reopen a failed stream; there is no automatic request replay. Callers use
the session context manager and complete it before accepting a capture.
Earlier verified objects are immutable operation inputs, not a continuous audit
of the source disk. The session remains single-owner, not a concurrent connection.

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
read rejects by size. Git commands and individual batch exchanges receive a sanitized environment,
bounded output, and the existing command timeout. Missing objects are `unavailable`;
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
