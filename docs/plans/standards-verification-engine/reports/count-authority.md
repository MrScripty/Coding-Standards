# VE043 Count-Authority Recovery

## Purpose

Eliminate numeric literals that duplicate the cardinality of mutable
inventories. The verification engine must derive observed membership and
cardinality from canonical evidence; migration rows may preserve exact
historical identities but do not co-own a changing global total.

## Count Taxonomy

| Class | Representation | Decision |
| --- | --- | --- |
| Mutable aggregate | Exact observed-versus-manifest set equality; derive count for reporting | Literal expected totals are prohibited |
| Declared finite contract | Exact expected row or key projection | Derive cardinality from the declared set |
| Historical snapshot | Immutable versioned rows or exact projection | Do not replace membership with a scalar total |
| Structural multiplicity | Empty, unique, exactly one selected identity | `0` and `1` operators remain valid |
| Policy threshold | Named ratio, limit, or budget owned by policy data | Allowed when the number is itself the contract |

`line_budget` numerator and denominator values are explicit policy thresholds,
not inventory cardinalities. They remain valid. A table's number of current
rows, current checkers, current consumers, or current packages is a mutable
aggregate and cannot be a literal expectation.

## Measured Findings

The broad Bash scan finds 359 numeric-comparison candidates. This is an audit
queue, not 359 confirmed defects: it includes malformed-row checks, uniqueness,
fixed child identities, policy thresholds, and mutable totals.

Confirmed mutable README-family literals are:

- row 35: 17 dependency rows, category totals 15/1/1, and 26 consumer rows;
- root README consumer audit: 26 consumer rows;
- row 46: stale 33 consumer rows; and
- row 35 and root-audit success messages that repeat those totals.

The root audit already compares exact observed and manifested consumer paths.
Row 45 already preserves the correct historical pattern: exact introduced path
and classification without a global total. Row 46 must use the same model.

The declarative engine's `table` check accepts optional `row_count`. Eight live
suites use it:

- `milestone-7-row-19-structure`;
- `gui-smoke-evidence`;
- `testing-source-closure`;
- `milestone-7-row-29-decomposition`;
- `milestone-7-row-30-decomposition`;
- `milestone-7-row-31-decomposition`;
- `checker-migration-packages`; and
- `milestone-7-f018-decomposition`.

Seven already contain exact projections that make `row_count` redundant. GUI
smoke evidence requires one exact case-key projection before its literal can be
removed.

## Generic Derived-Inventory Contract

The planned `reference_inventory` assertion accepts only:

- one contained candidate TSV path and exact header;
- one candidate path column;
- one contained manifest TSV path and exact header;
- one manifest path column; and
- one non-empty exact UTF-8 literal.

It reads candidate paths from the canonical table, resolves each as a contained
regular file, selects files containing the literal exactly, and requires the
selected path set to equal the manifest path set. It derives cardinality only
for diagnostics. A separate ordinary `table` check owns manifest schema,
classification domains, uniqueness, and exact special identities.

The assertion has no glob, regular expression, shell parser, command execution,
network access, callback, normalization, inferred path, default candidate set,
or policy-specific branch. Missing evidence is typed `unavailable`; malformed
tables, duplicate paths, invalid UTF-8, and containment failures are typed
`invalid`; missing or extra manifest membership is an assertion failure.

## Recovery Sequence

### VE043-R1: Baseline Authority Repair

Remove README-family mutable totals while preserving exact membership,
classification, schema, path existence, historical identity, and the canonical
fail-fast runner. Do not change either README manifest.

The accepted root audit owns current consumer completeness. Row 35 validates
its declared dependency manifest without duplicating its cardinality. Row 46
retains the exact Rust profile consumer and historical 33-to-34 event without
asserting a present total.

R1 implementation exposed a generated-evidence write-set conflict. The
committed recovery plan creates documentation-inbound references to the three
repaired checker paths, and the exact computed-consumer identity creates a new
executable reference. VE044 must reconcile the generated structure inventory
and dependency graph before R1 can satisfy freshness; count semantics and both
README manifests remain unchanged.

VE044 Option 1 is selected. The canonical generator updates the structure
inventory and all three graph artifacts atomically; exact review must show only
derived relationship changes from the accepted plan and R1 checker evidence.

R1 and VE044 are accepted. Exact membership remains canonical, current report
counts are derived, and the regenerated graph is fresh at 170 verifiers / 175
nodes / 855 edges / 171 components. All 170 canonical mixed entrypoints pass.

### VE043-E1: Count-Safe Engine Contract

Remove `row_count` from the table schema with no compatibility parser. Replace
all eight uses with exact projections, add the GUI case-key projection, and add
the generic `reference_inventory` assertion with focused positive and negative
tests. One shared-contract checkpoint covers the coherent engine package.

### VE043-A1: Remaining Numeric Audit

Classify every remaining numeric comparison by the taxonomy above. Migrate
confirmed mutable aggregates through their owning package. Exact semantic sets
move to projections or relations; historical membership moves to exact rows;
reporting totals are derived. Do not build a Bash-expression parser solely to
police scripts that the migration is deleting.

### VE043-P1: README Consumer Package Audit

After `reference_inventory` is accepted, perform a fresh read-only incident-edge
and ownership audit for the root README consumer checker and rows 35, 45, and
46. Admit only a dependency-closed package. Do not leave Bash callers pointing
to a deleted checker, run declarative evidence through a Bash bridge, or retain
dual authority.

## Acceptance

- no README-family checker compares a mutable aggregate to a literal;
- `row_count` is rejected as an unknown table-check field;
- all former `row_count` suites preserve exact membership evidence;
- `reference_inventory` proves missing, extra, duplicate, unavailable, invalid
  UTF-8, and escaping-path outcomes with typed diagnostics;
- M6-RC1 and each shared engine package pass focused tests, all declarative
  suites, graph and plan checks, diff integrity, and the repository-owned
  fail-fast complete-suite runner; and
- no fallback schema, wrapper, inferred default, or duplicate authority remains.
