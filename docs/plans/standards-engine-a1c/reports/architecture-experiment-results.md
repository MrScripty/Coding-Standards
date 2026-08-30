# A1c Architecture Experiment Results

**Status:** `Blocked` on snapshot discovery scope

**Prototype:** [snapshot-aggregate-prototype.py](snapshot-aggregate-prototype.py)

## Executed Boundary

Run from the repository root:

```bash
python3 docs/plans/standards-engine-a1c/reports/snapshot-aggregate-prototype.py
```

The self-checking prototype uses one disposable temporary SQLite file and
prints the complete relevant state after every transition. It imports no A1b
production package and creates no retained database.

## Results

| Experiment | Result | Disposition |
| --- | --- | --- |
| A1C-E1 snapshot Interface | Tagged and explicit Interfaces can drive equal behavior over one internal Snapshot Module. Explicit methods keep create, find, delete, and undelete schemas and capabilities distinct; the tagged operation adds request-kind dispatch without removing domain behavior. | Prefer explicit methods, subject to resolving discovery scope. Do not create four independent internal authority owners merely because four caller commands exist. |
| A1C-E2 identity separation | Two roots created over the same current canonical bytes received distinct snapshot handles and one shared content identity. Quarantining or purging one did not affect the other. | Accept content identity plus independent snapshot-root lifecycle identity as the candidate model. |
| A1C-E3 aggregate persistence | Two analysis aggregates retained children inside aggregate payloads. A derived child index supported cold inspection without independently storing each child as semantic authority. Root purge removed its aggregate and index transactionally. | Continue the aggregate candidate. The prototype does not yet prove the complete A1b analysis algebra or production performance. |
| A1C-E4 discovery summary | Two equal-content roots created at one logical time had equal content, commit, creation time, and lifecycle. Only their opaque handles differed. | Blocked: the product must decide the catalog scope or provide non-semantic caller context before `find` is usable after agent loss. |
| A1C-E5 operation/version authority | Both public Interface candidates reused one Snapshot Module and one state model; no stored per-method authority object was needed by the exercised behavior. | Continue testing one facade contract with domain-owned compatibility rather than presuming one persisted authority record per method. |
| A1C-E6 evidence substitution | External-schema, identity separation, transaction, cold-reopen, failure-outcome, and lifecycle evidence remain necessary. Backup/restore and independently durable child authority were not needed by the exercised workflows. | Incomplete until the discovery blocker is resolved and the composed candidate can be tested against the full A1b claims. |

## Observed Cases

The executable probe passed these named cases:

- `same-content-isolation`;
- `child-inspection`;
- `quarantined-discovery`;
- `undelete`;
- `cold-reopen` without reading the canonical source;
- `expiry-and-shared-content`;
- `transactional-purge`;
- `interface-parity`; and
- `invalid-config-rejected`.

The final first-root purge retained one canonical-content row because the
second root still owned it. Purging the second root removed the content,
aggregate records, and derived child index. Minimal tombstones retained only
the purged snapshot IDs and purge times so later use could return
`SNAPSHOT.EXPIRED` without retaining deleted authority.

## Discovery Blocker

The product supports developers and agents across projects, but the discovery
contract does not yet say whether one store is scoped to one project/harness or
shared across several projects. That distinction determines what `find` must
return.

### Option A: deployment-scoped catalog

Each configured store belongs to one project or harness context. `find`
returns that store's snapshot roots. Commit provenance, lifecycle, creation
order, and handles are sufficient because project selection happens before the
Standards Engine Interface is invoked.

This has the smallest Coding Standards Interface, but movement and
administration occur per configured store. Sharing one snapshot across project
stores requires administrative copying or a future explicit transfer design.

### Option B: shared catalog with caller context

One store serves several projects. Snapshot creation receives an opaque caller
context or display label, and `find` can filter or display it. The value is not
standards meaning, content identity, authorization, or Git provenance.

This makes a shared store usable, but creates additional questions: who owns
the context, whether it is required or unique, whether it can be renamed, how
authorization filters it, and whether moving a snapshot preserves it.

### Option C: opaque handles and timestamps only

Return every root and make the agent infer the intended one from handle,
commit, and creation time.

Reject this option. The reproduced equal-content case contains no reliable
selection fact, so this would move storage coordination back to callers and
defeat the purpose of engine-owned snapshot discovery.

## Provisional Recommendation

Prefer Option A if the deployment contract can guarantee one project or
harness context per store. It removes project identity from Coding Standards
and keeps snapshot discovery local. If one physical store must serve multiple
projects, select Option B explicitly and model its context as non-semantic
catalog metadata rather than hiding it in labels, paths, handles, or content
identity.

Do not continue with public contract or production persistence design until
the product owner selects the store scope. The choice changes Interface input,
authorization, movement, and discovery behavior.

## Prototype Limits

- Canonical bytes are a bounded stand-in for complete corpus capture and
  validation.
- Authorization is represented by separate method boundaries, not a real
  authorization Adapter.
- Tombstones demonstrate one way to preserve `SNAPSHOT.EXPIRED`; their
  retention policy remains an A1C-003 design question.
- The derived child index demonstrates lookup mechanics, not production scale
  or the complete analysis projection.
- The temporary SQLite experiment ran on Linux only and proves no Windows or
  macOS storage behavior.
- Change-set authoring remains outside A1c.

## Conclusion

The two-identity aggregate model survives its first executable deletion and
cold-reopen tests and is materially simpler than assigning an independent
lifecycle to every child. Public snapshot discovery cannot yet be selected.
The next valid step is a product decision about deployment-scoped versus shared
snapshot catalogs, not more storage implementation.
