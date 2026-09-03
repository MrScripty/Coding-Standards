# Standards Engine

`tools/standards_engine/` is the typed composition facade for standards
navigation, immutable analysis, and controlled authoring. Callers use canonical
IDs, authored policy title/body content, explicit semantics, and opaque handles.
Repository paths, complete files, Markdown metadata envelopes, TOML/JSON
projections, SQLite records, Git refs/object IDs, and source locators remain
private Engine implementation facts unless explicitly inspected.

The public operations are snapshot-bound `query`, immutable-state `prepare` and
`resolve`, handle-based `inspect`, and the admitted A2 authoring operations
`create_proposal`, `find_proposals`, `revise_proposal`, `query_proposal`, and
`analyze_proposal`, followed by `review_proposal` and `apply_proposal`.
In Interface version 20, proposal creation and revision each carry one atomic
`StandardsChangeSet`: an evidence-backed purpose plus explicit standards-domain
edits. The common focused revision names a canonical policy unit and supplies
its title, authored body, and preserve/change semantic intent. Creation,
retirement, registered policy-unit movement, `Requires`/`Specializes` changes,
and policy-impact or broader semantic relationships use other closed edit
variants. No edit accepts paths or serialized repository files.

Each accepted revision appends its normalized change set to an immutable
logical program and advances the durable proposal head only from its exact
expected revision; stale or invalid requests publish nothing. The Engine
privately projects that program to the fixed Markdown, TOML, and JSON
authorities and sends the result through the same compiler, Router, neutral
standards graph, and coverage owners as A1c. Discovery and revision readback
reconstruct the exact logical authority from SQLite after process replacement.
`query_proposal` reads one exact historical revision; its results and
continuations are revision-anchored projections and do not mint Snapshot or
inspection authority. A `related` query for an exact non-standard relationship
consumer returns an opaque `authoring_target` bound to the query Snapshot (or a
proposal's retained base Snapshot). Relationship edits submit that handle;
they never submit the consumer's repository locator as authoring input. The
facade owns and closes its Engine/store lifecycle when opened from a repository.

`analyze_proposal` derives normalized policy-unit changes and A1c semantic
proposals from explicit authoring intent and the compiled base/candidate, then
creates the same immutable A1c Analysis state used by `prepare` and `resolve`.
Authoring callers do not submit `semantic_proposals`; that field remains an A1c
Analysis representation. Exact revision identity participates in cold replay
without treating projected material as a Snapshot. `review_proposal` accepts
only a complete current revision analysis with no `requires-change`
disposition and three explicit evidence-backed
consumer, impact, and audit acceptances. The Engine derives the proposal head,
configured `refs/heads/main`, and Standards Verifier `complete` checkpoint,
derives an imperative proposal-specific conventional subject plus material
rationale from the explicit purpose, then publishes one immutable content-bound
readiness aggregate under an atomic proposal-head guard. `apply_proposal`
accepts only that readiness handle,
obtains current apply authorization, creates and validates a deterministic
candidate with the complete Engine-projected add, modify, relocate, and remove
topology in a private local clone, and runs the Standards Verifier `complete`
checkpoint against the exact checkout before import. Candidate identity binds
the exact parent, tree, executable decisions, and proposal-specific message.
Mechanically authored standards authorities are canonical regular,
non-executable data files; an existing non-canonical executable authority is
normalized when that authority changes. The Engine revalidates the candidate
after the external checkpoint and before durable admission. Failed-verification
results expose only bounded public code, outcome, suite, and check identifiers;
raw verifier messages and repository paths remain private. It records immutable
verified intent, advances only `refs/heads/main` with an
expected-target compare-and-swap, observes the exact candidate, and records an
immutable applied outcome before returning `applied`. Application is local and never
pushes a remote. Every failure after durable application admission returns the
application handle as
`recovery-required`. Application admission atomically records one immutable
readiness-to-application selection with the verified intent.
`recover_application(readiness)` requires separate current recovery authority,
resolves only that selection, and observes the configured canonical ref. An
existing durable outcome returns `applied` without consulting current Git; an
exact candidate at the ref records the missing outcome and returns `applied`.
An unchanged expected target, another target, or unavailable observation stays
explicitly recovery-required. Recovery never stages, verifies, imports,
publishes, retries, rolls back, or scans application records. Application does
not use the configured worktree or index as staging authority and creates no
mutable phase ledger, automatic retry, rollback, or second review lifecycle.
Routing evaluates the registered
Router projection and derives dependency closure from the neutral standards graph.
Read-only change analysis compares exact accepted and proposed authority,
derives fact requirements and impact obligations, validates evidence-backed
decisions, and projects either pending work or a complete result from one
content-addressed `AnalysisState`.

The canonical JSON Schema generates the native request/result algebra and
agent tool definitions. The optional text renderer is presentation only; no
command-string protocol or repository path is part of the agent interface.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_engine/tests
```
