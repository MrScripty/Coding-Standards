# Standards Metadata

`tools/standards_metadata/` owns neutral loading and structural validation of
the repository's canonical standards corpus. Canonical documents own module
IDs, paths, roles, applicability, `Requires`, `Specializes`, verification text,
and ownership. Policy-unit sidecars own policy-unit identities, locators,
aliases, lifecycle, and semantic revisions. Corpus manifests own membership
only; this package loads, validates, resolves, and projects those authorities.

The package returns immutable metadata views and neutral typed failures. It
does not depend on verifier suites or diagnostics, policy-impact declarations,
analysis packets, or graph storage. Consumers translate failures at their own
boundary.

`load_canonical_standards_corpus` returns one immutable module and policy-unit
view for callers that need both. Module-only consumers can continue to use
`load_canonical_module_corpus` without compiling policy impact.

Run the focused tests:

```bash
python3 -m unittest discover -s tools/standards_metadata/tests
```
