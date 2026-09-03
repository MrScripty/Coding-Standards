# Standards Engine

`tools/standards_engine/` is the typed composition facade for standards
navigation, immutable analysis, and controlled authoring. Callers use canonical
IDs and opaque handles; repository paths, metadata layouts, graph declarations,
store locations, and source locators remain internal unless explicitly
inspected.

The public operations are snapshot-bound `query`, immutable-state `prepare` and
`resolve`, handle-based `inspect`, and the admitted A2 authoring operations
`create_proposal`, `find_proposals`, `revise_proposal`, and `query_proposal`.
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
lifecycle when opened from a repository. Routing evaluates the registered
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
