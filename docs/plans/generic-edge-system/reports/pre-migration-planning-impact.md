# Pre-Migration Planning Impact Snapshot

The currently accepted policy-impact query was run at base
`7ae51ba996827cbf35cb6a5d73476b9eeb724437` before any Planning or graph
authority change. It returned 24 explicit consumers for `workflow.planning`,
including the full-review prompt, fixture, and suite added by that revision.

The exact machine-readable output is retained in
`pre-migration-planning-impact.tsv`. Milestone 2 must assign every returned
consumer one `updated`, `reviewed-no-change`, or `not-applicable` disposition
before changing `workflows/planning.md`. This snapshot is evidence, not a
second edge authority.

Command:

```bash
python3 tools/standards_verifier/query_policy_impact.py \
  --owner workflow.planning
```
