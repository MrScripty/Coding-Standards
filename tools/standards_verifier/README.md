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
