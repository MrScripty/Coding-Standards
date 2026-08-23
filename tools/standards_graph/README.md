# Standards Graph

`tools/standards_graph/` adapts canonical standards metadata and explicitly
registered relationship providers to the repository-neutral graph engine. It
composes the generic policy-impact node/group catalog with the compiled
`standards_policy_impact` provider; it does not own relationship declarations.
It projects metadata-owned module and policy-unit views into graph nodes and
owns standards graph composition, not canonical metadata, generic traversal,
suite execution dependencies, or policy applicability.

The stable provider ID `standards-verifier.metadata-dependencies` predates this
module and remains unchanged because provider identity is durable graph
provenance, not implementation ownership.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_graph/tests
```
