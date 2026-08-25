# Standards Graph

`tools/standards_graph/` adapts canonical standards metadata and explicitly
registered relationship providers to the repository-neutral graph engine. It
projects metadata-owned module and policy-unit views and composes the complete
node/group/edge contribution from the compiled `standards_policy_impact`
provider; it does not own or reload relationship and supplemental-artifact
declarations. It owns standards graph composition, not canonical metadata,
generic traversal, suite execution dependencies, or policy applicability.

The stable provider ID `standards-verifier.metadata-dependencies` predates this
module and remains unchanged because provider identity is durable graph
provenance, not implementation ownership.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_graph/tests
```
