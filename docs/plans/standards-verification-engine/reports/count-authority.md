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
| Declared finite contract | Explicit schema framing or arity, fixed identity or status protocol, or exact expected member projection | Derive cardinality and validation from the declared contract |
| Historical snapshot | Immutable versioned rows or exact projection | Do not replace membership with a scalar total |
| Structural multiplicity | Empty, unique, exactly one selected identity | `0` and `1` operators remain valid |
| Policy threshold | Named ratio, limit, or budget owned by policy data | Allowed when the number is itself the contract |

Classify from authoritative purpose, never from literal value, operator, source
language, filename, or graph relationship. When more than one description
appears applicable, use this precedence:

1. `policy-threshold` when the number itself is named normative policy;
2. `historical-snapshot` when immutable completed-state evidence owns it;
3. `declared-finite-contract` when an explicit schema, identity, enumerated set,
   framing rule, or status protocol owns it;
4. `structural-multiplicity` when it expresses only zero/one presence, absence,
   uniqueness, or exactly-one selection; and
5. `mutable-aggregate` when it summarizes a changing current inventory.

Every selected class requires positive evidence. The last item is not a default.
If no class is established, classification stops for explicit exception
admission instead of inferring from syntax or choosing the nearest category.

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

E1 is accepted. The strict table schema rejects `row_count`; all eight suites
retain exact membership evidence, including the GUI case-key projection. The
registered `reference_inventory` assertion derives exact literal-containing
file membership from contained UTF-8 evidence and returns typed diagnostics for
missing, extra, duplicate, unavailable, invalid UTF-8, and escaping paths. The
package passes 15 focused tests, all 138 engine tests, Python compilation, all
106 declarative suites, fresh generated evidence, both plan checks, diff
integrity, and all 170 canonical mixed entrypoints.

### VE043-A1: Remaining Numeric Audit

Classify every remaining numeric comparison by the taxonomy above. Migrate
confirmed mutable aggregates through their owning package. Exact semantic sets
move to projections or relations; historical membership moves to exact rows;
reporting totals are derived. Do not build a Bash-expression parser solely to
police scripts that the migration is deleting.

The historical total of 359 has no frozen rows, extraction rule, baseline
revision, or exact locations and is non-authoritative context. The selected
recovery machine-generates one immutable verifier-scoped lexical candidate
snapshot and derives its cardinality. Candidate identity, path, expression,
source diagnostics, fingerprint, owner, normal disposition, progress, and
totals remain derived. A separate reviewed layer records only generated
candidate identity and irreducible taxonomy class. Exact coverage, class
domain, lifecycle drift, and exception absence are verified; no owner migration
is admitted before generated baseline and classification acceptance.

G1 implements the generated baseline with two fixed lexical matcher families:
shell numeric operators and symbolic comparison operators with at least one
exact numeric-literal operand. Stable candidate identity derives from checker
path, matcher, exact expression, and repeated-expression occurrence; line and
column remain diagnostics. The machine-generated TSV also owns exact source
text and fingerprint. It contains no semantic class, owner, disposition,
package, progress, or expected cardinality, and an existing changed baseline
cannot be overwritten.

G1 is accepted. The generated snapshot currently contains 708 derived rows
across the canonical 170-verifier scope; both values are runtime reports, not
expected policy data. Fourteen focused tests cover deterministic identity,
exact rendering, idempotent write, immutable-change refusal, malformed and
duplicate snapshots, unavailable and invalid UTF-8 inputs, and containment
escapes. All 152 engine tests, Python compilation, all 106 declarative suites,
existing graph freshness, both plan checks, diff integrity, and all 170
canonical mixed entrypoints pass. C1 is next and may add semantic classes but
must not restate generated candidate facts.

C1 preflight reaches an owner-join re-plan trigger. The baseline's current
candidate-bearing verifier paths have no exact overlap with checker subjects in
the package manifest because those package subjects are already migrated.
README dependency classes, rule-owner maps, and graph edges do not own current
checker semantics. The recommended recovery keeps exact semantic-class coverage
in C1, derives standard action from taxonomy, and defers owner resolution to
the existing package-admission review. L1 then requires every candidate
disappearance to join the accepted package and its canonical owner.

Option 1 is selected. C1 now owns only exact candidate-ID-to-semantic-class
coverage and uses existing generic table and relation assertions. It contains
no owner field and cannot authorize modification or acceptance. Package
admission remains the sole checker-owner decision, and L1 must join every
candidate disappearance to an accepted package with an explicit canonical
owner. This preserves graph relationships without a duplicate mutable owner
map or an inferred fallback.

C1 schema preflight reaches a second re-plan trigger. Repeating an empty
exception-rationale cell on every normal classification row adds manually
maintained data, while existing generic assertions cannot enforce its
conditional authority. The recommended recovery uses only candidate identity
and semantic class. A separate exception artifact and exact join are admitted
only if semantic review discovers a real taxonomy exception; absence of that
artifact means no exception is authorized.

Schema Option 3 is selected. The C1 table contains exactly candidate identity
and semantic class. No exception artifact or exception field is admitted. If
review finds a candidate outside the five classes, work stops for a separately
owned exception-artifact and exact-join decision rather than recording a
sentinel, free-form rationale, or default class.

The first semantic-review batch reaches a taxonomy-precedence re-plan trigger.
Historical counts can also be zero/one multiplicity; explicitly enumerated
sets can resemble mutable aggregates; and header, field-arity, and status
comparisons are finite contracts not named by the current row/key wording. The
recommended recovery retains five compact classes but classifies by
authority-first precedence: policy threshold, immutable history, explicit
finite schema/identity/protocol contract, zero/one presence or uniqueness, then
current mutable aggregate. Syntax does not select the class.

Taxonomy Option 1 is selected with positive-evidence enforcement. The canonical
procedure above resolves overlaps while retaining explicit per-candidate
review. Mutable aggregate requires an observed changing current inventory and
cannot absorb an unknown case. A candidate with no established class triggers
exception admission rather than receiving a default.

C1 is accepted. The reviewed `numeric-comparison-decisions.tsv` contains only
generated candidate identity and semantic class. Its registered suite uses the
generic table assertion for exact schema, non-empty values, uniqueness, and the
closed taxonomy domain, then a set relation for exact identity coverage against
the immutable generated baseline. No candidate mechanics, owner, action,
package, progress, cardinality, rationale, or exception is repeated in reviewed
data.

Focused positive and negative table/relation evidence passes, as do all 152
engine tests, Python compilation, all 107 registered declarative suites, and
generated graph and numeric-audit freshness. L1 is next and must derive current
progress while rejecting disappearance that lacks exact accepted-package and
canonical-owner evidence.

L1 preflight reaches a capability re-plan trigger. The immutable baseline and
C1 decision coverage are suitable historical authority, and the package table
already owns accepted checker subjects and explicit canonical owners. The
generic relation check is static, however, and cannot compare those records to
the live result of the canonical numeric collector or validate a conditional
set difference. The existing numeric snapshot check instead requires immutable
history to equal current derivation exactly, so it would reject every accepted
checker retirement.

The recommended recovery is one typed, side-effect-free numeric lifecycle check
inside the Python engine. It reuses the canonical collector, rejects new
candidates, and authorizes a missing baseline identity only when its checker is
no longer live and exactly one accepted `checker:<path>` package row supplies a
non-empty owner. All totals remain derived diagnostics. No second current
snapshot, manually maintained owner mapping, callback source, mutable baseline,
or Bash bridge is admitted. The existing strict byte-equality path must be
removed or delegated to the same lifecycle authority in the accepted slice.

L1 selects Option 1. Implementation will add the narrow typed Python lifecycle
check and retire or delegate strict byte equality in the same accepted slice.
The canonical collector derives current membership; immutable baseline and C1
records preserve audit history; accepted package rows remain the only
checker-owner authority. No additional mutable evidence table or expected total
is authorized.

L1 is accepted. The registered lifecycle check derives current candidate
membership and live checker presence, requires exact C1 identity coverage, and
joins every retired checker to one accepted package with an explicit owner. It
rejects new identities and partial disappearance while a checker remains live.
The former byte-equality snapshot check is deleted, leaving immutable write-once
baseline creation and one registered current-state authority. All progress and
cardinality remain derived; baseline, C1, and package rows are unchanged.

### VE043-P1: README Consumer Package Audit

The completed read-only audit supersedes the former assumption that the root
README consumer checker and rows 35, 45, and 46 can be admitted as one package.
The generated graph places row 45 in a two-checker Language Index component and
row 46 in a four-checker Rust closure component. Row 35 dynamically orchestrates
multiple owners. The separate root audit has inbound callers from those groups
and root-index closure and invokes unadmitted S1 routing. None of these subjects
has current migration-package authority.

The lifecycle baseline currently derives 27 row-35 candidates, nine row-45
candidates, 11 row-46 candidates, and eight root-audit candidates. These values
are observations only. Their retirement remains governed by checker absence and
one exact accepted package row with an explicit owner; no count is copied into
package authority.

Option 1 is selected: decompose P1 into an ordered
owner-coherent train for root README/routing infrastructure, Language Index
closure, Rust profile/index closure, and Milestone 7 lifecycle evidence. Freeze
root-index and S1 prerequisites explicitly, transfer executable caller edges
only with accepted registered suites, and integrate shared authority files
serially. A cross-owner mega-package, retained Bash bridge, inferred owner, and
blanket historical retirement remain prohibited.

P1-D1 is read-only. It derives its matrix from current checker behavior,
generated incident edges, registered suites, package authority, and canonical
owner documents. It does not add expected totals, infer an owner, admit a
package, remove a call, or change lifecycle evidence.

P1-D1 freezes ten ordered responsibility packages: S1; row 35; root index;
language index; row 45; Rust adoption retirement; Rust migration index; Rust
profile authority; row 46; then the root README consumer inventory. Root and
language index authority remains with `STANDARDS-ROUTER.md`; Rust index/profile
authority remains with `profiles/languages/rust/README.md`; scenario and row
lifecycle evidence remains with `migration.parent-plan`; dynamic Bash-consumer
inventory remains with `verification-engine.migration` until final retirement.

The audit distinguishes conservative path references from actual behavior.
Generated incident edges remain exact package-lifecycle obligations, but a
checker basename in a command argument, identity assertion, or manifest does
not by itself establish runtime invocation or semantic ownership.

VE045 formerly blocked package admission because existing checks could not prove
exact ordered headings plus explicit line ceilings for three indexes or direct
filesystem absence for retired Rust adoption notes. The accepted recovery adds
generic `markdown_structure` and `absent_paths` checks; it does not convert these
fixed policy and safety contracts into mutable counts or whole-file snapshots.

VE045 Option 1 is selected. The capability slice adds only the two generic
typed checks, their registration and focused tests, implementation
documentation, and serial planning evidence. Package authority remained frozen
until the shared-contract checkpoint passed; no expected count, inferred
default, approximation, or duplicate Bash/custom implementation was admitted.

VE045 is accepted after 16 focused tests, all 179 engine tests, all 107
declarative suites, fresh generated evidence, and all 170 mixed checker
entrypoints passed. Its configured line ceilings remain explicit owner policy;
observed newline counts are derived at runtime and are not copied into migration
authority. The P1 train may now begin with a separate package-1 admission.

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
