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
