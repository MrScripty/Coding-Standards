# Standards Engine

`tools/standards_engine/` is the typed composition facade for standards
navigation, immutable analysis, and controlled authoring. Callers use canonical
IDs and opaque handles; repository paths, metadata layouts, graph declarations,
store locations, and source locators remain internal unless explicitly
inspected.

The public operations are snapshot-bound `query`, immutable-state `prepare` and
`resolve`, handle-based `inspect`, and the admitted A2 authoring operations
`create_proposal`, `find_proposals`, `revise_proposal`, `query_proposal`, and
`analyze_proposal`, followed by `review_proposal` and `apply_proposal`.
Proposal creation
stores exact non-Git replacement material under an immutable revision and a
durable proposal head; revision advances that head only from its exact expected
revision, and stale requests publish nothing. Discovery and internal revision
readback reconstruct opaque identities after process replacement and revalidate
persisted authority before use. `query_proposal` overlays one exact historical
revision on its retained base snapshot and sends the resulting material through
the same compiler, Router, and neutral standards graph as A1c `query`. Its
results and continuations are revision-anchored projections and do not mint
snapshot or inspect handles. The facade owns and closes its Engine/store
lifecycle when opened from a repository. `analyze_proposal` derives normalized
policy-unit changes from one exact revision and its base, then creates the same
immutable A1c Analysis state used by `prepare` and `resolve`. Exact revision
identity participates in cold replay without treating projected material as a
snapshot. `review_proposal` accepts only a complete current revision analysis
with no `requires-change` disposition and three explicit evidence-backed
consumer, impact, and audit acceptances. The Engine derives the proposal head,
configured `refs/heads/main`, and Standards Verifier `complete` checkpoint,
then publishes one immutable content-bound readiness aggregate under an atomic
proposal-head guard. `apply_proposal` accepts only that readiness handle,
obtains current apply authorization, creates and validates a deterministic
candidate in a private local clone, and runs the Standards Verifier `complete`
checkpoint against the exact checkout before import. It records immutable
verified intent, advances only `refs/heads/main` with an expected-target
compare-and-swap, observes the exact candidate, and records an immutable
applied outcome before returning `applied`. Ambiguous post-verification
publication or persistence returns the durable application handle as
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
