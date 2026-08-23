# Standards Graph

`tools/standards_graph/` adapts canonical standards metadata and explicitly
registered standards relationship manifests to the repository-neutral graph
engine. It owns standards graph projection, not canonical metadata, generic
traversal, suite execution dependencies, or policy applicability.

The stable provider ID `standards-verifier.metadata-dependencies` predates this
module and remains unchanged because provider identity is durable graph
provenance, not implementation ownership.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_graph/tests
```
