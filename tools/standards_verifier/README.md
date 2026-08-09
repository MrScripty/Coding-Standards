# Standards Verifier

This repository-local Python 3.11+ engine evaluates strict declarative suites.
It uses only the Python standard library and does not install, download, or
resolve runtime packages.

Run every registered suite:

```bash
python3 tools/standards_verifier/verify.py --all
```

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

Suite and registry TOML is strict. Unknown keys, schema versions, check kinds,
operators, dependencies, and paths fail with typed diagnostics. Configuration
cannot execute commands, import modules, evaluate code, interpolate environment
variables, or write files.

The bounded `exact_text` check compares a contained regular file's raw bytes
with inline expected TOML text encoded as UTF-8. It performs no newline,
whitespace, Unicode, or encoding normalization and accepts only `id`, `type`,
`path`, and `expected` fields.

The `edge_dispositions` check validates migration packages against the exact
generated executable graph. Packages opt into exactly one configured mode.
`edge-dispositions` requires every outgoing `executable_reference`,
`helper_dependency`, and `verifier_dependency` edge to have one exact manifest
row. `edge-free` prohibits manifest rows and requires the generated graph to
contain no outgoing executable edges. Admitted edge-free packages must retain
their checker; accepted edge-free packages must not. Admitted edge packages
must name present edges; accepted edge packages retain their historical rows
while their checker and graph edges are absent.

Each edge row has one of these dispositions and replacement forms:

| Disposition | Replacement form |
| --- | --- |
| `native-engine` | `assertion:<suite-path>#<check-id>` |
| `independent-gate` | `checker:<path>` |
| `suite-requires` | `suite:<source-suite-id>-><target-suite-id>` |
| `same-owner-package` | `package:<package-id>` |
| `external-owned-artifact` | `artifact:<path>` |
| `invalid/unresolved` | `unresolved:none` |

Native assertions must name an existing check in a registered package-owned
suite. Suite requirements must name an actual registry `requires` edge whose
source suite is in the package write set. Retained checkers and external
artifacts must equal the current edge target. Replacement and evidence paths
are repository-contained regular files. An `invalid/unresolved` row may
document an admitted blocker but cannot be accepted. The check never infers a
disposition from graph shape or executes a replacement.

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
