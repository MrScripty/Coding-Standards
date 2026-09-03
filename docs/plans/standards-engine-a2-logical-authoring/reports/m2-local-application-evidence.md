# Milestone 2 Local Application Evidence

**Status:** `Accepted`

## Outcome

The Standards Engine now applies the complete logical proposal topology to the
configured local canonical Git ref. Agents continue to supply only canonical
standards IDs, authored content, explicit semantic decisions, rationale,
evidence, and opaque handles. The Engine alone resolves and serializes
standards files, generated projections, SQLite aggregates, Git trees, commits,
and the local ref update.

Milestone 2 deepens the existing A1c/A2 composition. It adds no public
operation, graph, analyzer, store, background worker, compatibility layer,
generic document editor, remote operation, or caller-owned persistence seam.

## Repository And Commit Contract

Repository Git accepts one exact base revision, path-safe candidate files with
explicit executable decisions, exact removals, and one validated conventional
commit message. It constructs the candidate through Git blob/index plumbing in
a private local clone, removes paths before additions so both directory/file
replacement directions are valid, rejects conflicting or no-effect topology,
and proves the checkout and index agree with the exact candidate object.

Relocation is an explicit removal plus addition; the Adapter does not infer
rename meaning. Candidate blobs, the candidate commit, and post-verifier file
observations share the same size bound. The configured worktree and index never
act as staging authority.

Authoring derives the commit material before readiness publication. The subject
uses the imperative conventional form `feat(standards): apply standards
change: <purpose summary>`. The body contains the cumulative explicit purpose
rationales. Parent, tree, modes, message, and deterministic construction all
participate in candidate identity.

## Application And Recovery

The Engine compares the logical projection's retained base path observation
with its exact proposed path observation, rejects incomplete or colliding
authority, and sends only changed/added authority bytes plus exact removals to
Repository Git. Mechanically authored standards authorities use canonical
regular non-executable mode; changing a previously executable authority
normalizes it.

The exact complete checkpoint runs against the candidate checkout. Repository
Git revalidates that active candidate after the external verifier and before
Authoring durably admits the application; publication validates it again.
Invalid or unsupported verifier drift therefore remains a typed pre-admission
rejection. Failed verification returns only bounded public code, outcome,
suite, and check identifiers; raw messages and repository paths remain private.

After admission, every non-applied result retains the application handle for
observation-only recovery. Unknown publication remains publication-unavailable;
a known compare-and-swap target divergence uses the existing target-diverged
recovery code. Success still requires local ref publication, exact observation,
and durable applied-outcome persistence. No path retries, rebases, rolls back,
pushes, or infers success.

## Verification

The accepted production implementation passed:

- Repository Git: 11 of 11 tests, including add/modify/remove/relocate, both
  directory/file replacement directions, exact modes/message/parent/tree,
  stale and uncertain ref updates, no-effect/conflicting topology, bounded
  candidate objects, post-verifier drift, and source worktree/index isolation;
- Authoring and logical compilation: 25 of 25 tests;
- Contracts: 20 of 20 tests;
- Analysis: 86 of 86 tests;
- canonical generated-artifact and suite-input projection: 19 of 19 tests;
- changed-source Ruff formatting/check and repository diff hygiene; and
- an independent bounded correction audit with no remaining blocker.

The required-real add/retire workflow ran the production complete verifier
twice per test, published both commits locally, inspected their exact topology,
modes, parent, and message, closed and reopened SQLite/Engine state, read the
created standard, and proved the retired standard was no longer navigable. It
passed on:

- Linux CPython 3.11: 1 test in 694.321 seconds; and
- Linux CPython 3.12: 1 test in 699.315 seconds.

After the bounded review corrections, the full review/application failure and
recovery composition passed on:

- Linux CPython 3.11: 1 test in 753.446 seconds; and
- Linux CPython 3.12: 1 test in 813.348 seconds.

At the final staged boundary, the corrected create/retire workflow passed again
on CPython 3.11 in 610.781 seconds and CPython 3.12 in 646.718 seconds. The exact
staged repository also passed 270 of 270 declarative suites and all seven
retained Bash checkers with no failure or blocked suite.

Together these tests exercise the changed application path through real Git,
SQLite, generated contracts, complete candidate verification, typed negative
results, admission, publication, observation, recovery, and process reopen.

## Acceptance Mapping

- **LA-A4:** satisfied. The complete Engine-owned topology and exact
  proposal-specific commit are verified before atomic local publication.
- **LA-A5:** satisfied. Application reuses the accepted A1c compiler,
  navigation, Analysis, Snapshot, Authoring, Repository Git, and verifier
  owners without a parallel mechanism.
- **LA-A6:** satisfied. Invalid closure/candidate state, verification outcomes,
  stale targets, publication uncertainty, observation failure, and persistence
  failure remain typed and cannot become partial success.
- **LA-A7:** satisfied. The changed public workflow passes the supported Linux
  CPython 3.11 and 3.12 runtimes through real Git/SQLite boundaries, cold
  reopen, target races, and interruption recovery.

Remote publication and automatic semantic authorship remain explicitly out of
scope. Milestone 3 owns the final objective-wide artifact/deletion audit; it
does not reopen the accepted reversible M2 design without a named objective or
standards violation.
