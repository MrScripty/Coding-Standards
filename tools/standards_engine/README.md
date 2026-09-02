# Standards Engine

`tools/standards_engine/` is the typed composition facade for standards
navigation, immutable analysis, and controlled authoring. Callers use canonical
IDs and opaque handles; repository paths, metadata layouts, graph declarations,
store locations, and source locators remain internal unless explicitly
inspected.

The public operations are snapshot-bound `query`, immutable-state `prepare` and
`resolve`, handle-based `inspect`, and the first A2 authoring operations
`create_proposal` and `find_proposals`. Proposal creation stores exact non-Git
replacement material under an immutable revision and a durable proposal head;
discovery reconstructs those opaque identities after process replacement and
revalidates the persisted revision authority before returning a handle. The
facade owns and closes its Engine/store lifecycle when opened from a repository.
Routing evaluates the registered Router
projection and derives dependency closure from the neutral standards graph.
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
