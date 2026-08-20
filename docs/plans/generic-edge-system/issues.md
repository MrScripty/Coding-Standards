# Generic Directed Edge System Issues

| ID | Status | Finding | Owner | Disposition | Evidence |
| --- | --- | --- | --- | --- | --- |
| GES-001 | open | Policy impact owns bespoke storage, reverse lookup, and query mechanics downstream of the needed neutral capability. | Generic edge recovery | Migrate in Milestone 2 and delete old authority. | Graph inventory |
| GES-002 | open | Suite dependency and metadata relation checks duplicate dependency closure or cycle mechanics. | Generic edge recovery | Adapt in Milestone 2 while retaining domain declarations and diagnostics. | Graph inventory |
| GES-003 | deferred | The temporary Bash migration graph has specialized SCC, component, and wave semantics under a frozen schema. | Verification-engine migration | Do not modify; revisit only at zero-Bash deletion or a separately demonstrated current need. | Graph inventory |
| GES-004 | resolved | The Planning impact graph omitted a Planning-owned prompt, fixture, and suite. | Policy-impact adapter | Already corrected at the accepted base; migration must preserve all 24 edges and suite-owner closure. | Commit `7ae51ba` |
