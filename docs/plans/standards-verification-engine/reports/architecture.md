# Verification Engine Architecture

## Current Problem

The evaluation suite has 274 Bash verifier entrypoints. At the planning
baseline, 166 contain calls to verifier or helper scripts, 43 parse mutable
document sections with `sed`, and only 13 use the shared decision-table helper.
This creates four recurring costs:

1. policy outcomes are hidden inside shell branches;
2. file shape and process exit behavior become accidental authority;
3. transitive calls rerun checks and make complete-suite cost unpredictable;
4. every new owner or migration package tends to create another parser and
   bespoke diagnostic style.

The existing decision-table and source-index helpers prove that reusable
validation is effective, but they remain Bash implementations surrounded by
per-topic orchestration.

## Ownership Boundary

The engine owns only verification mechanics:

- loading and validating suite contracts;
- resolving contained repository paths;
- parsing supported evidence formats;
- scheduling declared dependencies once;
- evaluating reusable assertions and ordered predicates; and
- reporting typed diagnostics and execution summaries.

Standards documents own policy. Fixture and suite data own selected scenarios,
expected outcomes, required/prohibited evidence, exact rows, and suite
dependencies. The engine must not contain topic names, rule IDs, expected
policy outcomes, migration milestones, or source-specific exceptions.

## Runtime And Packaging

Use Python 3.11 or newer and only its standard library.

Reasons:

- `tomllib`, `csv`, `pathlib`, `json`, `unittest`, and graph/data structures
  cover the required mechanics without package resolution;
- a local package can run directly from the repository without installation;
- typed Python data models and explicit validation are clearer than shell
  positional parsing;
- adding Rust or Go would introduce a compiler/build/lockfile lifecycle before
  verification can run, while a shell rewrite would retain the maintenance
  problem.

The package declares `requires-python >= 3.11`, checks the running interpreter,
and documents the exact invocation. It does not run `pip`, install Python,
download dependencies, or fall back to Bash when the capability is missing.

## Contract Model

One strict registry maps stable suite IDs to TOML suite files and dependencies.
Each suite contains a schema version, owner, description, and ordered checks.
Unknown or duplicate IDs, keys, check kinds, operators, and dependencies are
invalid.

Initial reusable checks are:

- `text`: required and prohibited literals in one contained file;
- `decision`: strict TSV columns/domains plus ordered boolean predicates and an
  explicit default outcome.

Decision checks support one compact output or several independently typed
outputs over one canonical scenario matrix. Multi-output checks declare the
exact ordered input columns and at least two output contracts. Their TSV header
is exactly `case`, declared inputs, then output columns. Each output owns its
default and ordered rules, while predicates may read only declared inputs.
Output evidence therefore cannot feed another output or satisfy itself.
Single-output and multi-output configuration are mutually exclusive; the
engine does not infer a mode, split fixtures, combine outcomes, or fall back to
an executable evaluator.

Measured later families add:

- exact TSV row/set/order/count checks;
- Markdown heading, repository-relative route, and local-link closure checks;
- strict aggregate newline budgets against typed metric tables;
- metadata ownership and dependency graph checks;
- disposition and owner-map agreement;
- plan lifecycle and acceptance-claim checks; and
- source-index closure.

Decision predicates are deliberately bounded to `all`, `any`, `not`, `eq`,
`ne`, `in`, and `not_in` over named table fields; the multi-output form further
restricts them to its declared input fields. Rules are evaluated in declared
order and produce one named outcome for their owning output. There is no
expression string, operator precedence parser, cross-output predicate, variable
interpolation, or executable callback.

## Scheduling

The runner resolves selected suites through the registry, rejects missing
dependencies and cycles, and evaluates the graph in deterministic dependency
order. A suite ID is evaluated at most once per invocation. A failed dependency
blocks dependents with a distinct diagnostic; it is not rerun through another
parent.

Focused execution selects one or more suite IDs. Complete execution selects all
registered suites. During migration, the existing Bash suite and declarative
suite are both required gates; the engine does not execute legacy scripts.

## Diagnostics

Every failure records:

- stable code;
- typed outcome (`invalid`, `unavailable`, or `unsupported`);
- suite and check identity;
- evidence path and row/field when applicable;
- expected and observed values when safe; and
- concise message.

Text output is the maintainer default. JSON output preserves the same fields
for automation. Exit status distinguishes passed assertions from invalid
configuration, unavailable inputs, and unsupported capabilities. Successful
process completion alone is never an acceptance result; the summary names
selected, passed, failed, and blocked suites.

## Security And No Fallback

- Paths must be repository-relative and remain below the resolved repository
  root, including through symlinks.
- Suite configuration cannot launch commands, import modules, evaluate code,
  interpolate environment variables, or write files.
- TOML schema version 1 has one accepted representation. Unknown or older
  representations fail; there is no compatibility parser.
- A missing file, field, dependency, or runtime capability produces a typed
  diagnostic. The engine does not skip the check, infer a default, or invoke an
  old script.
- A migrated script is deleted in the same accepted slice as its replacement.
  Unmigrated scripts remain separate current checks, not fallback behavior.

## Extension Rule

Add a reusable primitive only when its semantics are independent of one policy
owner and its tests can state a stable input/output contract. Prefer composing
existing primitives or correcting an over-broad test. A new primitive requires
positive, negative, malformed-input, and typed-diagnostic tests.

A custom Python check is the last option. It must be side-effect-free, directly
registered, typed, unit-tested, and owned by a named package. The engine never
loads arbitrary module paths from suite configuration.

Routing evidence is split into two composable mechanics. `markdown_links`
resolves only explicit inline local destinations from configured UTF-8 files,
with repository containment and typed missing-target diagnostics. `line_budget`
counts raw newline bytes from configured files and compares them to one unique
positive metric through fixed strict integer-ratio arithmetic. Neither check
contains a route name, policy threshold, expression evaluator, network client,
normalizer, callback, or command surface.

## Migration Sequence

1. Establish the strict kernel and replace one representative leaf checker.
2. Generate exact checker-family and dependency inventory.
3. Migrate low-risk structural leaf packages.
4. Replace shared metadata, plan, disposition, and source-index helpers.
5. Migrate repeated ordered decision packages by owner and risk.
6. Replace transitive calls with registry dependencies and unblock
   Cross-Platform closure.
7. Implement any justified exceptional algorithm as a registered typed Python
   check, retire every Bash verifier/helper and the migration launcher, and run
   final Python engine-only acceptance.

Migration batches share an owner, semantic outcome, dependency set, assertion
family, and verification gate. Adjacency or short script length is not enough.
Shared engine and registry changes integrate serially; frozen disjoint suite
packages may be prepared concurrently.

## Alternatives Rejected

### Expand Generic Bash Helpers

This preserves shell parsing, subprocess composition, inconsistent diagnostics,
and limited structured-data support. It cannot meet the maintenance objective.

### Rust Or Go Binary

A compiled binary offers strong typing and distribution benefits, but this
repository currently has no compiler project, dependency lock, build artifact,
or bootstrap contract. That cost is not justified for deterministic local
document/TSV validation. Reconsider only if downstream distribution requires a
self-contained executable and the build lifecycle has an owner.

### Arbitrary Command Actions

Allowing suites to run shell commands would make the engine a task runner and
preserve bespoke behavior behind configuration. It also weakens path, output,
and side-effect guarantees. Existing scripts remain separate until represented
by a typed primitive.

### General Expression Language

A general DSL would duplicate a programming language, obscure policy review,
and create parser/security/versioning obligations. Bounded ordered predicates
cover the observed decision pattern while remaining inspectable.
