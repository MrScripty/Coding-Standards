# Repository Git

`repository_git` is a repository-neutral Adapter for bounded Git subprocess
execution, exact object reads, current-`HEAD` binding, explicit gitlink
traversal, and Git-index observations.

The package owns no standards semantics, snapshot lifecycle, SQLite storage,
or public Engine operation. Callers resolve one revision and retain that exact
value while loaders request files. Worktree changes and later commits cannot
substitute bytes for the retained revision.

All Git subprocesses receive a sanitized environment, bounded output, and a
fixed timeout. Missing objects are `unavailable`; malformed or contradictory
objects are `invalid`; unsupported object modes, path encodings, and output
sizes are `unsupported`.

Git remains the established implementation for object resolution and reported
object type. This Adapter locally interprets only the leading commit-tree field
and raw tree-entry framing so it can verify exact returned object hashes and
traverse explicitly mapped gitlinks without pathspec or worktree semantics. The
current implementation-versus-dependency comparison is recorded in the
[A1c corrective decision](../../docs/plans/standards-engine-a1c-repair/reports/dependency-and-version-decisions.md).
Re-evaluate that decision before materially extending the local Git semantic
surface.
