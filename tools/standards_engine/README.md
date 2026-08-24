# Standards Engine

`tools/standards_engine/` is the typed composition facade for standards
navigation and read-only analysis. Callers use canonical IDs and immutable
snapshot handles; repository paths, metadata layouts, graph declarations, and
source locators remain internal unless explicitly inspected.

The public operations are snapshot-bound `query`, immutable-state `prepare` and
`resolve`, and handle-based `inspect`. Routing evaluates the registered Router
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
