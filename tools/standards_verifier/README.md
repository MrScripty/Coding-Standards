# Standards Verifier

This repository-local Python 3.11+ engine evaluates strict declarative suites.
It uses the hash-locked A1b dependency environment; it does not download or
resolve packages while verification is running.

Create an isolated environment with the admitted lock before invoking the
Verifier:

```bash
python3 -m venv /tmp/coding-standards-verifier
/tmp/coding-standards-verifier/bin/python -m pip install \
  --require-hashes --only-binary=:all: \
  -r tools/standards_contracts/requirements.lock
```

Run every registered suite:

```bash
PYTHONPATH="$PWD" /tmp/coding-standards-verifier/bin/python -P \
  tools/standards_verifier/verify.py --all
```

Run the canonical complete repository checkpoint:

```bash
PYTHONPATH="$PWD" /tmp/coding-standards-verifier/bin/python -P \
  tools/standards_verifier/verify.py --complete
```

Complete mode runs every registered Python suite once in dependency order.
It has no generated migration preflight, retained-process phase, adapter, or
fallback. `--complete` is mutually exclusive with selection and listing
options and supports both text and JSON output.

Library consumers use `run_complete_verification(repo_root)` to receive the
same Python-only checkpoint as one structured result. Suite execution itself
does not write progress output or substitute process-global streams.

Run one suite and its dependencies:

```bash
PYTHONPATH="$PWD" /tmp/coding-standards-verifier/bin/python -P \
  tools/standards_verifier/verify.py --suite rust-test-style
```

Run engine self-tests:

```bash
PYTHONPATH="$PWD" /tmp/coding-standards-verifier/bin/python -P \
  -m unittest discover -s tools/standards_verifier/tests -v
```

Report every reviewed semantic consumer and projection for one covered policy
owner:

```bash
python3 tools/query_edges.py \
  --node workflow.planning \
  --group policy-impact \
  --direction outgoing
```

The generic command loads only sources registered by
`evaluation/standards-effectiveness/edge-source-registry.toml` and emits
deterministic TSV. The policy manifest declares one edge once and places it in
the `policy-impact` and `semantic` groups; the upstream graph engine derives
incoming and outgoing indexes and reports declaration provenance. Querying
`workflow.planning` or `workflows/planning.md` therefore returns the same edge
set. Group membership does not duplicate an edge, and transitive traversal is
rejected because these groups do not permit it.

The standards verifier is a downstream policy adapter. It validates canonical
owner metadata, contained consumers, supported policy relations, non-empty
applicability, registered evidence owners, duplicate semantic identities, and
current policy-unit coverage certificates. Every semantic consumer, including
an enforcement suite, is selected only by an explicit compiled relationship.
Hyperlinks, lexical similarity, standards `Requires`, and suite ownership do
not create semantic impact edges. The retired temporary Bash checker graph did
not create them either. The independent coverage horizon and authorized audit
detect missing consumers; missing edges require an explicit declaration
correction.

Repository graph composition reads canonical standards membership from
`evaluation/standards-effectiveness/canonical-module-corpus.toml`. That
paths-only manifest declares every metadata-bearing canonical document once.
Each document's metadata remains the sole authority for its logical ID, role,
path alias, `Requires`, and `Specializes`; the normative/routable view is
derived by excluding the `reference` role. Semantic validation suites do not
select graph membership, and corpus, node, role, and edge counts are derived
observations rather than stored acceptance values.

Suite and registry TOML is strict. Unknown keys, schema versions, check kinds,
operators, dependencies, and paths fail with typed diagnostics. Configuration
cannot execute commands, import modules, evaluate code, interpolate environment
variables, or write files.

The `plan_contract` check validates one contained UTF-8 Markdown plan against
the repository's lifecycle, objective-evidence, final-projection, and
composed-design structure. A suite declares whether the plan is `valid` or
`invalid` and may bind an invalid fixture to its exact diagnostic. The check
does not execute a helper, accept callbacks, infer compatibility forms, or
decide whether cited evidence semantically proves an objective.

One invocation catalog owns every validated registry entry and every suite body
loaded for that invocation. Listing validates the registry without parsing suite
bodies. Focused execution parses only the selected dependency closure, while
`--all` and `--complete` parse every registered suite. An unrelated malformed
suite therefore does not block listing or ordinary focused execution; a
malformed selected suite or dependency remains a typed failure.

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

Predicate leaves compare one field with a literal through `eq`, `ne`, `in`, or
`not_in`, or compare two declared row fields through `eq_field` or `ne_field`
with an exact `other_field`. Field comparison does not evaluate expressions,
coerce values, infer columns, or permit a multi-output rule to reference an
output column.

The bounded `exact_text` check compares a contained regular file's raw bytes
with inline expected TOML text encoded as UTF-8. It performs no newline,
whitespace, Unicode, or encoding normalization and accepts only `id`, `type`,
`path`, and `expected` fields.

The `text` check applies fixed required and prohibited literals to one
contained UTF-8 file. `text` and `markdown_section_text` accept an optional
`match_case` value of `sensitive` or `insensitive`; omitted configuration keeps
the existing sensitive contract. Insensitive matching uses deterministic
Unicode case folding for both content and configured literals. It does not
enable regular expressions, Unicode normalization, inferred variants, or
approximate matching. Case-equivalent duplicates and required/prohibited
contradictions are invalid under the selected mode.

The `markdown_links` check accepts exactly one source: an explicit non-empty
`paths` list or one strict projected table source named `members` that selects
one nonempty unique path column. It requires every inline repository-local
Markdown destination to exist relative to its containing UTF-8 document. It
skips only `http://`, `https://`, and `mailto:` destinations, removes fragments
before resolution, and treats a fragment-only destination as the containing
file. Absolute targets and parent or symlink escapes are invalid; missing
sources or targets are unavailable. It does not fetch URLs, validate anchors,
decode destinations, parse reference links, infer files, or normalize content.

The `markdown_link_coverage` check reads one contained UTF-8 Markdown `path`,
one explicit comparison `identity`, and one strict projected table source named
`members`, which must select exactly one nonempty unique column. The
`repository-path` identity requires each member to name a contained regular
file and compares normalized local target paths after removing fragments. The
`destination` identity requires each member to be a local destination whose
target exists and compares the exact source-relative destination, including
any fragment. Unrelated local links and repeated document destinations are
valid; external destinations cannot satisfy either mode. Empty, duplicate,
missing, or uncovered members, malformed tables, invalid UTF-8, path escapes,
unknown identities, and unknown configuration produce typed diagnostics. The
check has no default identity, copied target list or count, reference-link
parser, URL fetch, anchor-existence validation, glob, regular-expression
configuration, command execution, optional member, compatibility schema, or
fallback. Use a separate `markdown_links` check when every document link,
rather than every declared member, must have an available target.

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
optional `scope` is `subtree` or `body`; omitted scope retains the `subtree`
default. A subtree extends through nested headings and ends before the next
heading of equal or higher level. A body ends before the next heading of any
level. Either scope ends at end of file when no boundary exists. Configured
required and prohibited literals apply only to that bounded section. Missing
or duplicate start headings fail explicitly. Section-heading selection remains
exact and case-sensitive regardless of literal `match_case`. The check has no
regular-expression configuration, inferred boundary, whole-file snapshot,
callback, command execution, copied inventory, count, compatibility
representation, or fallback.

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

The `baseline_markdown_headings` check reads one exact section inventory,
disposition table, expected-gap table, and summary-owned baseline commit. It
uses the fixed repository Git adapter to derive removed ATX Markdown headings
between that baseline and the current tree, then requires every removed
undisposed section identity to equal the expected-gap membership. Each explicit
classification maps to `present` or `absent` and validates the corresponding
current heading state. Headers, identifiers, locations, classifications,
reasons, baseline identity, and Git output are strict and typed. The check has
no configurable command, revision, pathspec, diff flag, heading syntax,
fallback baseline, copied source list, shell bridge, compatibility parser, or
arbitrary action.

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

An optional table-level `where` predicate scopes non-empty, domain, unique,
projection, and row-constraint assertions to one explicit semantic membership
set. Alternatively, one strict `members` projected table source may select a
single unsplit identity column and name its canonical table `key`. Membership
must be non-empty and unique, and every member must resolve to exactly one
canonical row. Assertions run in declared member order while retaining each
canonical row's original source line. Predicate and member scope are mutually
exclusive. Missing or duplicate canonical rows, empty or duplicate members,
unknown keys or columns, malformed sources, and repository escape are typed
failures. Each named `[[checks.row_constraints]]` supplies an optional `where`
predicate and one required `require` predicate. Every scoped row selected by
the constraint must satisfy that requirement; failures retain the original TSV
line and report `ASSERT.TABLE_ROW_CONSTRAINT` with the constraint ID. Both
predicates use the same fixed `eq`, `ne`, `in`, `not_in`, `all`, `any`, and
`not` grammar as projections and decisions. Unknown columns, duplicate or
empty constraint IDs, missing requirements, and unknown fields are invalid.
The check does not infer membership, derive policy from numeric ID ranges,
copy canonical rows, execute callbacks, combine ambiguous scopes, or fall back
to an unscoped assertion.

Every strict projected table source uses the same parser and reader for path,
exact header, selected columns, order, predicate, and optional single-field
split. Individual checks layer only their source role and row requirements on
that shared contract.

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

The `repository_paths` check reads one strict projected table source named
`paths`, whose projection selects exactly one column and at least one non-empty
value. Repeated values are valid: the check derives the distinct path set in
first-seen order and validates each path once as a contained regular
non-symlink repository file. Identity uniqueness remains the responsibility of
relations, table keys, or another explicit identity contract. Missing files
are unavailable; directories, absolute or parent-traversing paths, symlink
paths and escapes, empty values, malformed tables, and invalid configuration
are typed failures. The check derives paths from current table rows and has no
copied path list, count, owner inference, command execution, compatibility
representation, optional-missing mode, or fallback.

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

Source-index closure is a declarative suite composition rather than an engine
check kind. `markdown_structure` owns exact headings and line ceilings;
`table`, `repository_paths`, `key_coverage`, and `relation` own membership and
identifier evidence; Markdown checks own target and exact-destination coverage;
and table-derived or inline text checks own non-authority and Router exclusion.
The source-index suite and fixtures contain source-index policy. Generic Python
modules contain no source-index schema, migration state, Router prose, or fixed
fixture topology.

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

The downstream `metadata_route` check connects reviewed decision outcomes to
canonical module IDs. Its separate expectation table names exact direct modules
and exact transitive `Requires` closure for every decision case. The check
resolves the current canonical corpus and derives closure through the neutral
graph engine; it does not copy edges into Python, infer modules from prose or
links, or substitute a nearby route. Resolved rows reject unresolved selection
values, unresolved rows reject partial selections, and decision and expectation
case sets must match exactly.

## Git Reachability Evidence

`tools/verify_git_reachability.py` compares an explicit protected commit set
with current Git refs. Its strict TSV schema is:

```text
oid\tcommit_disposition\treference\tauthority
```

`retained` requires the OID to be an ancestor of the named full ref.
`archived` requires the ref to resolve to the exact OID.
`discard-authorized` requires `reference=none` and a nonempty authority record.
The tool rejects malformed or duplicate OIDs, unknown refs or commits,
repository-path escape, archive mismatches, and unreachable retained commits.
It does not create refs, infer a disposition, run cleanup, accept abbreviated
OIDs, or fall back to object-integrity output.

## Exit Status

| Status | Meaning |
| --- | --- |
| `0` | Every selected suite passed. |
| `1` | Evidence did not satisfy one or more assertions. |
| `2` | Configuration, usage, or evidence representation is invalid. |
| `3` | A required input or runtime capability is unavailable. |
| `4` | The requested capability is unsupported. |

Diagnostics support human-readable text and structured JSON through
`--format text` and `--format json`. Assertion diagnostics travel through the
ordinary result path and therefore return status `1`. Execution exceptions are
classified from their typed outcome as invalid (`2`), unavailable (`3`), or
unsupported (`4`), independent of output format. `EngineError` derives that
status from its diagnostic outcome and accepts no separate numeric override.
