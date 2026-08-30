# Standards Metadata

`tools/standards_metadata/` owns neutral loading and structural validation of
the repository's canonical standards corpus. Canonical documents own module
IDs, paths, roles, applicability, `Requires`, `Specializes`, verification text,
and ownership. Policy-unit sidecars own policy-unit identities, locators,
aliases, lifecycle, and semantic revisions. Corpus manifests own membership
only; this package loads, validates, resolves, and projects those authorities.

The package returns immutable metadata views and neutral typed failures. Every
loader consumes the `ContentSource` Interface, which supplies exact bytes by
normalized logical path. `DirectoryContentSource` adapts repository tools and
fixtures, `RecordingContentSource` records the complete requested closure, and
`FrozenContentSource` replays only those captured bytes. Parsing and semantic
validation never depend on Snapshot, SQLite, Git, verifier suites or
diagnostics, policy-impact declarations, analysis packets, or graph storage.
Consumers translate failures at their own seam.

`load_canonical_standards_corpus` returns one immutable module and policy-unit
view for callers that need both. Module-only consumers can continue to use
`load_canonical_module_corpus` without compiling policy impact.

`project_unmapped_module` uses the same accepted Markdown heading parser to
remove exact, non-overlapping policy-unit scopes from one canonical module and
returns a digest of the remaining representation. Downstream analysis can
therefore detect changed authority outside policy units without copying
locator logic or treating line numbers as identity.

Run the focused tests:

```bash
python3 -m unittest discover -s tools/standards_metadata/tests
```
