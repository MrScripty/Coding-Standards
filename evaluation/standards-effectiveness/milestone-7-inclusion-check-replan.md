# Milestone 7 Inclusion Check Re-plan

## Re-plan Finding

The M6-T11 row-36 probe must prove that every exact
identifier/owner/disposition record declared by the bounded row-36 evidence is
present in the source-wide canonical consolidation dispositions. The canonical
table intentionally contains records for later migration rows, so exact ordered
or set equality is not the required invariant.

The verifier's existing `relation` check exposes `left` and `right` projections
and supports only ordered equality and unique-set equality. Filtering the
source-wide table to equality would require copying row 36's identifier list
into suite configuration. That would create a second identity authority and
the update churn this migration is removing.

`left` and `right` also describe notation rather than evidence roles. They are
especially unclear beside the standards graph's `Requires` and `Specializes`
edges and the migration plan's parent/child decomposition vocabulary.

## Accepted Design

Add one strict generic `inclusion` check with public `members` and `container`
roles:

```toml
[[checks]]
id = "row-36-disposition-lineage"
type = "inclusion"

[checks.members]
# bounded records that must be represented

[checks.container]
# larger canonical collection in which every member must occur
```

The check means: every unique projected `members` row must occur in the unique
projected `container`; the container may contain additional rows. File,
header, column, order, predicate, and split projection behavior reuses the
existing strict table-projection contract.

`members` and `container` are verifier evidence roles only. They do not create
standards ownership, routing, dependency, specialization, parent/child, or
execution-order relationships.

## Typed Contract

- Unknown fields, malformed sides, unknown columns, invalid projection order,
  invalid predicates, invalid split configuration, and unequal projection
  widths remain typed configuration errors.
- Missing inputs remain typed unavailable outcomes.
- Duplicate projected rows on either side are invalid because multiplicity
  cannot be silently discarded.
- A member absent from the container produces one stable typed assertion
  diagnostic that identifies the missing projected records.
- An empty configured side is invalid under the existing table/header/schema
  rules; an empty result after valid filtering is evaluated by the inclusion
  relation and is not replaced by inferred records.
- No count, identifier list, owner, path, or relation direction is inferred
  from filenames, ordering, graph shape, or prose.
- No Bash callback, command execution, compatibility alias, alternate
  `left`/`right` inclusion form, or equality fallback is permitted.

The existing `relation` check remains the canonical exact-equality assertion.
It is not renamed and its `left`/`right` schema is not broadened. The new check
is a separate operation because containment and equality have different
semantics and diagnostics.

## Thin Slices

### M6-E1: Inclusion Engine Contract

**Allowed write set:**

- `tools/standards_verifier/standards_verifier/checks/inclusion.py`;
- `tools/standards_verifier/standards_verifier/checks/__init__.py`;
- `tools/standards_verifier/tests/test_engine.py`;
- `tools/standards_verifier/README.md`;
- active plan and execution ledger.

Implement the strict parser and assertion. Focused tests must cover passing
containment with extra container rows, missing members and stable diagnostics,
duplicate member projections, duplicate container projections, malformed
configuration, unavailable input, path containment, projection-width mismatch,
filtering, and split projection. Run engine self-tests, all declarative suites,
plan checks, and diff integrity. Commit this engine capability independently;
do not admit row 36 in the same commit.

### M6-T11: Row 36 Admission

After M6-E1 is accepted, rebuild the disposable row-36 suite with
`type = "inclusion"`, using row-36 owner validation as `members` and canonical
consolidation dispositions as `container`. The suite must derive the complete
bounded identity relation without copied identifiers or cardinalities.

Re-run the disposable suite, live checker, architecture-pattern reference,
layered-pattern, monorepo-pattern, data-authority, and execution-train gates.
Only then admit the row-36 package and exact incident-edge dispositions in a
separate planning commit.

### M6-T11 Acceptance

Register the admitted suite, run focused and affected verification, delete the
legacy Bash checker, regenerate derived graph artifacts, accept the package and
edge dispositions, run all declarative suites and the complete mixed suite,
update the plan and ledger, and create one atomic implementation commit.

## No-fallback And No-legacy Rule

The design does not preserve row 36 by wrapping or executing its Bash checker.
M6-E1 adds only a generic native assertion. M6-T11 may delete the legacy
checker only after the native suite proves the complete current contract and
all independent gates pass. If inclusion cannot represent a required row-36
invariant, implementation stops with typed diagnostics and re-plans instead of
filtering away evidence or weakening equality.

## Re-plan Triggers

Re-plan before implementation if:

- a projected member may validly occur more than once;
- containment needs keyed joins, transformed values, cardinality ranges, or
  partial-column matching beyond existing exact projections;
- row 36 requires a standards-graph edge rather than evidence inclusion;
- an existing equality suite would need a compatibility conversion;
- implementing the check requires command execution, inferred identity lists,
  copied counts, or files outside the bounded write set;
- fresh graph or owner evidence changes row 36's package boundary.

