# Standards Verifier

This repository-local Python 3.11+ engine evaluates strict declarative suites.
It uses only the Python standard library and does not install, download, or
resolve runtime packages.

Run every registered suite:

```bash
python3 tools/standards_verifier/verify.py --all
```

Run the canonical complete repository checkpoint:

```bash
python3 tools/standards_verifier/verify.py --complete
```

Complete mode first verifies the generated Bash migration inventory and graph,
then runs every registered declarative suite once in dependency order, and
finally fail-fast executes each retained Bash verifier in deterministic
inventory order. Retained executable paths are derived from repository files,
not suite or registry configuration. When no Bash verifiers remain, the same
command succeeds after the generated and declarative phases without a special
adapter or fallback. `--complete` is mutually exclusive with selection/listing
options and supports text output only while retained checkers can write their
native output.

Run one suite and its dependencies:

```bash
python3 tools/standards_verifier/verify.py --suite rust-test-style
```

Run engine self-tests:

```bash
python3 -m unittest discover -s tools/standards_verifier/tests -v
```

Regenerate or verify the exact Bash checker structure and dependency graph
artifacts:

```bash
python3 tools/standards_verifier/generate_inventory.py --write
python3 tools/standards_verifier/generate_inventory.py --check
```

The generated artifacts measure structure only. They record exact executable
and frozen-contract references, uniquely resolved verifier/helper dependencies,
strongly connected components, and condensation waves. Missing or ambiguous
targets are typed diagnostics. The generator does not infer canonical owner,
semantic risk, package cohesion, or migration disposition from a filename,
shell mechanism, or graph shape; those remain reviewed planning decisions.
Component list columns use `-` for an empty set and comma-separated repository
paths or component identifiers otherwise.

Create the immutable numeric-comparison audit baseline:

```bash
python3 tools/standards_verifier/generate_numeric_audit.py --write
```

The numeric audit derives canonical scope from current `verify-*.sh` inventory
and records comparisons where an adjacent operand is an exact numeric literal.
It recognizes shell numeric operators and symbolic comparison operators through
two fixed lexical matchers; it does not parse Bash or infer semantic meaning.
Candidate IDs derive from checker path, matcher, exact expression, and repeated
expression occurrence, so unrelated line movement changes diagnostics but not
identity. The generated TSV owns paths, expressions, source positions,
fingerprints, and cardinality and must not be hand-edited. `--write` is
idempotent for identical content and refuses to replace a changed baseline.
It has no current-state check mode because accepted checker retirement must not
rewrite or invalidate historical evidence.

Verify baseline classification and current lifecycle:

```bash
python3 tools/standards_verifier/verify.py --suite numeric-comparison-classification
```

The suite's `numeric_audit_lifecycle` check derives current candidates from the
same canonical collector. Current identities must remain a subset of the
immutable baseline. A missing identity is valid only when its checker is absent
from canonical live inventory and exactly one accepted `checker:<path>` package
row supplies a non-empty owner. A still-live checker, new identity, missing or
ambiguous package, non-accepted package, and unavailable owner produce typed
diagnostics. Baseline, classification, and package schemas are exact. The check
writes no current snapshot, owner map, progress, or count and infers neither
package nor owner from names, routes, source text, or graph relationships.

Suite and registry TOML is strict. Unknown keys, schema versions, check kinds,
operators, dependencies, and paths fail with typed diagnostics. Configuration
cannot execute commands, import modules, evaluate code, interpolate environment
variables, or write files.

The `decision` check has two mutually exclusive canonical forms. The compact
single-output form uses `expected_column`, `default`, and ordered `rules`; its
TSV starts with `case` and ends with that expected column. The multi-output form
uses one exact ordered `input_columns` list and at least two
`[[checks.outputs]]` contracts. Its TSV header must be exactly `case`, the
declared inputs, then the declared output columns. Every output declares
exactly `column`, `default`, and ordered `rules`, and each is evaluated
independently against the same validated row.

Domains always cover every TSV column exactly. Multi-output rules may reference
only declared inputs, never `case` or another output, so expected evidence
cannot derive itself or influence a sibling decision. Defaults and rule
outcomes must belong to the corresponding output domain. Mismatches retain
`ASSERT.DECISION_OUTCOME` and identify the output column in `field`. Mixed
single/multi forms, inferred columns, fewer than two outputs, duplicate columns,
and output-to-output predicates are invalid; the engine does not select a
fallback representation.

The bounded `exact_text` check compares a contained regular file's raw bytes
with inline expected TOML text encoded as UTF-8. It performs no newline,
whitespace, Unicode, or encoding normalization and accepts only `id`, `type`,
`path`, and `expected` fields.

The `markdown_links` check accepts one explicit non-empty `paths` list and
requires every inline repository-local Markdown destination to exist relative
to its containing UTF-8 document. It skips only `http://`, `https://`, and
`mailto:` destinations, removes fragments before resolution, and treats a
fragment-only destination as the containing file. Absolute targets and parent
or symlink escapes are invalid; missing sources or targets are unavailable. It
does not fetch URLs, validate anchors, decode destinations, parse reference
links, infer files, or normalize content.

The `line_budget` check counts raw newline bytes across one explicit non-empty
`paths` list. It reads one exact two-column `metric`/`value` TSV, requires one
unique configured key with a positive ASCII decimal value, and applies a
strict integer ratio: `observed * maximum_denominator < baseline *
maximum_numerator`. Both ratio values are required positive integers and
equality fails. The check has no expression language, inferred metric, default
ratio, unit conversion, command action, or content normalization.

The `markdown_structure` check reads one contained UTF-8 Markdown file and
requires its complete ordered set of ATX heading lines (`#` through `######`)
to equal one explicit non-empty unique `headings` list. It also counts raw
newline bytes and requires that count to be less than or equal to one explicit
positive `maximum_lines` value. Missing inputs are unavailable; invalid UTF-8,
escaping paths, heading drift, and line-limit excess are typed failures. The
check does not parse prose, normalize content, infer headings or thresholds, or
freeze unrelated bytes.

The `markdown_headings` check reads one contained UTF-8 Markdown file, selects
ATX headings outside fenced code blocks at one explicit level from 1 through 6,
and applies each configured required and prohibited literal to every selected
heading line. At least one heading must match the level, and at least one
literal constraint must be configured. Violations identify the source line.
The check has no regular-expression configuration, inferred level, heading
inventory, count, line limit, callback, command execution, or content
normalization.

The `markdown_section_text` check reads one contained UTF-8 Markdown file and
selects exactly one configured ATX heading outside fenced code blocks. Its
section extends through nested headings and ends before the next heading of
equal or higher level, or at end of file. Configured required and prohibited
literals apply only to that bounded section. Missing or duplicate start
headings fail explicitly. The check has no regular-expression configuration,
inferred boundary, whole-file snapshot, callback, command execution, copied
inventory, count, compatibility representation, or fallback.

The `markdown_heading_cardinality` check reads one contained UTF-8 Markdown
file, selects one configured ATX heading level outside fenced code blocks, and
requires its derived state to be `empty`, `single`, or `nonempty`. A failed
assertion reports semantic states (`empty`, `single`, or `multiple`) rather
than a number for consumers to interpret. The check has no exact count,
minimum, maximum, range, heading-text predicate, Setext mode, alternate
scanner, regular expression, callback, command, compatibility representation,
package-specific branch, Bash execution, or fallback.

The `path_state` check accepts explicit unique `present` and `absent` path
sets; at least one set must be non-empty, and a path cannot occur in both.
Paths remain repository-contained after symlink resolution. Present paths may
be files, directories, or valid symlinks; missing paths and broken symlinks are
unavailable. Absent paths reject files, directories, valid symlinks, and broken
symlinks. Absolute paths, parent traversal, and symlink escapes are invalid.
The check derives cardinality and does not scan a corpus, inspect content,
infer paths, invoke commands, or ignore an unexpected filesystem object.

The `git_index_paths` check accepts one nonempty unique `tracked` path list and
requires exact membership in one fixed engine-owned, NUL-delimited Git index
read. Paths are validated lexically as repository-relative index identities;
tracked working-tree deletions therefore remain valid. Missing members report
`present-untracked` or `absent-untracked`, but filesystem state never replaces
index authority. Missing Git, nonzero Git, invalid UTF-8, and malformed output
are typed. Repository/index override environment variables are removed so the
selected repository root remains authoritative. The check has no mode, glob,
pathspec, directory expansion, ignore query, staged-content or history
operation, configurable command, flag, root, or environment, package-specific
branch, Bash execution, compatibility representation, or fallback.

The `reference_inventory` check reads one exact candidate TSV and one exact
manifest TSV, using explicitly configured headers and path columns. It resolves
every listed path as a contained regular file, selects candidate UTF-8 files
containing one non-empty exact literal, and requires exact selected-versus-
manifest path-set equality. Duplicate or empty paths, malformed tables,
invalid UTF-8, and escaping paths are invalid; missing evidence is unavailable;
missing or extra manifest membership fails the assertion. It has no glob,
regular expression, command, callback, inferred candidate set, normalization,
network access, or policy-specific branch.

The `table` check has no scalar row-count field. Exact finite membership is
expressed through projections or relations; mutable inventory cardinality is
derived from canonical membership. A configured `row_count` is an unknown
field and fails rather than using a compatibility parser.

The `inclusion` check compares two strict projected table sources named
`members` and `container`. Every unique projected member row must occur in the
unique projected container; additional container rows are valid. Both
collections support the same explicit path, exact header, selected columns,
source or lexical order, predicate, and single-field split contract used by
table relations. Duplicate projections are invalid, missing members fail with
a typed assertion, and missing inputs remain unavailable. The roles describe
evidence containment only: they do not create metadata graph edges, ownership,
parent/child decomposition, dependencies, or execution order. The check does
not infer members, counts, filters, direction, or aliases and does not execute
commands or fall back to equality or Bash.

The `repository_subjects` check reads one strict projected table source named
`subjects`, whose projection selects exactly one column. Each unique non-empty
value must be explicitly typed as `checker:<repository-path>` or
`suite:<registered-id>`. Checker subjects must resolve to contained regular
non-symlink files; suite subjects must name IDs in the registry already loaded
by the engine. Missing subjects are unavailable, while unknown types, path
escapes, symlinks, empty identities, and duplicate projected subjects are
invalid. The check does not infer a subject type, accept suite paths, load a
second registry, execute a checker, skip an unavailable subject, or fall back.

The `key_coverage` check reads strict projected table sources named `keys` and
`records`, each selecting exactly one column. The key projection must be
non-empty, unique, and contain no empty value. Every derived key must occur in
at least one record; unrelated records and multiple records for a key are
valid. Missing coverage is a typed assertion. The check derives both key and
record identities from canonical tables and has no copied key list, exact
count, inferred join, one-record constraint, compatibility representation, or
fallback.

The `table_text_absence` check reads one strict projected table source named
`literals` and one contained UTF-8 `path`. Its projection must select unique,
non-empty literals, and every derived literal must be absent from the target
file. Missing inputs are unavailable; invalid UTF-8, duplicate or empty
literals, and present literals are typed failures. It performs no text or path
normalization and has no copied literal list, regular-expression mode,
callback, command execution, compatibility representation, or fallback.

The `keyed_relation` check derives one nonempty unique key column from a strict
projected `keys` table source, then resolves exactly one `expected` and one
`observed` record for every key. Each record source declares one key column and
an equal-width nonempty value-column list; corresponding value tuples must
match. Explicit record predicates and unrelated rows are permitted. Missing,
duplicate, and mismatched keyed records fail separately. The check has no key
list, range, count, mode, composite or many-valued join, implicit column or
filter, query language, callback, command, package-specific branch,
compatibility representation, Bash execution, or fallback.

Numeric count-authority migration uses a generated immutable lexical snapshot,
not a manually maintained candidate manifest. The snapshot derives all
mechanical candidate facts and totals from canonical Bash verifier inventory.
It is deliberately semantic-free: later reviewed evidence may classify a
generated identity, but cannot restate its path, expression, owner, normal
disposition, package, progress, or cardinality. Missing, malformed, duplicate,
escaping, invalid UTF-8, changed, unavailable, and unauthorized lifecycle
evidence has typed outcomes.

The `metadata_graph` check parses the nine canonical Markdown metadata fields
without global normalization. Direct mode accepts one non-empty `paths` list
and validates the selected module graph. Fixture-corpus mode accepts one
non-empty `cases` list; each case has a unique `id`, non-empty `paths`, and the
exact ordered `expected` diagnostic-code sequence. The two modes are mutually
exclusive. The check validates field grammar, role and level domains,
canonical-owner equality, module-ID uniqueness, exact relation resolution,
profile-only specialization, self-edges, and cycles in `Requires`,
`Specializes`, and their combined graph. It does not infer targets, consult
legacy owner maps, execute helpers, or fall back to prose or file order.

Metadata diagnostics use the `METADATA.*` family. Configuration defects are
typed `CONFIG.*`, unavailable files remain `INPUT.UNAVAILABLE`, and a fixture
whose observed sequence differs from its declared sequence produces
`ASSERT.METADATA_FIXTURE`.

The `edge_dispositions` check validates migration packages against the exact
generated executable graph. Packages opt into exactly one configured mode.
`edge-dispositions` requires every incident `executable_reference`,
`helper_dependency`, and `verifier_dependency` edge to have one exact manifest
row. `edge-free` prohibits manifest rows and requires the generated graph to
contain no incident executable edges. Admitted edge-free packages must retain
their checker; accepted edge-free packages must not. Admitted edge packages
must name present edges; accepted edge packages retain their historical rows
while their checker and graph edges are absent.

Edge identity is the exact type, source, and target tuple. The package checker
must be exactly one endpoint, which determines direction without a separate
schema field or inferred default. Retained checker and artifact replacements
name the opposite endpoint: the callee for an outbound edge or the caller for
an inbound edge. Accepted packages reject both surviving prerequisites and
dangling callers that still reference the deleted checker.

Each edge row has one of these dispositions and replacement forms:

| Disposition | Replacement form |
| --- | --- |
| `native-engine` | `assertion:<suite-path>#<check-id>` |
| `independent-gate` | `checker:<path>` or `suite:<registered-suite-id>` |
| `suite-requires` | `suite:<source-suite-id>-><target-suite-id>` |
| `same-owner-package` | `package:<package-id>` |
| `external-owned-artifact` | `artifact:<path>` |
| `invalid/unresolved` | `unresolved:none` |

Native assertions must name an existing check in a registered package-owned
suite. A suite-backed independent gate names one registered suite, and its
evidence must equal that suite's exact registry path. It does not create or
require a registry dependency. Suite requirements are distinct: they must name
an actual registry `requires` edge whose source suite is in the package write
set. Retained checkers and external artifacts must equal the endpoint opposite
the package checker. Replacement and evidence paths are repository-contained
regular files. An `invalid/unresolved` row may document an admitted blocker but
cannot be accepted. The check never infers a disposition from graph shape,
replacement syntax, or registry topology, and it never executes a replacement.

## Exit Status

| Status | Meaning |
| --- | --- |
| `0` | Every selected suite passed. |
| `1` | Evidence did not satisfy one or more assertions. |
| `2` | Configuration, usage, or evidence representation is invalid. |
| `3` | A required input or runtime capability is unavailable. |
| `4` | The requested capability is unsupported. |

Diagnostics support human-readable text and structured JSON through
`--format text` and `--format json`.
