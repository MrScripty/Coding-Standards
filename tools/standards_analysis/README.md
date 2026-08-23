# Standards Analysis

`tools/standards_analysis/` owns read-only standards snapshot comparison,
policy-unit identity, impact selection, audit coverage, packets, questions,
and resolution. It consumes neutral applicability, metadata, policy-impact,
and graph contracts and does not depend on verifier checks or
repository-writing behavior.

Current implemented foundation:

- canonical JSON and domain-separated identities;
- clean-Git and deterministic manifest snapshots; and
- explicit policy-unit registry, locator, lifecycle, and digest validation.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_analysis/tests
```
