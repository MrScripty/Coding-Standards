# Standards Metadata

`tools/standards_metadata/` owns neutral loading and structural validation of
the repository's canonical standards corpus. Canonical documents own module
IDs, paths, roles, applicability, `Requires`, `Specializes`, verification text,
and ownership. The corpus manifest owns membership only.

The package returns immutable metadata views and neutral typed failures. It
does not depend on verifier suites or diagnostics, policy-impact declarations,
analysis packets, or graph storage. Consumers translate failures at their own
boundary.

Run the focused tests:

```bash
python3 -m unittest discover -s tools/standards_metadata/tests
```
