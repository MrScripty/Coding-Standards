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

Regenerate or verify the exact Bash checker structure inventory:

```bash
python3 tools/standards_verifier/generate_inventory.py --write
python3 tools/standards_verifier/generate_inventory.py --check
```

The generated inventory measures structure only. It does not infer canonical
owner, semantic risk, or migration disposition from a filename or shell
mechanism; those remain reviewed planning decisions.

Suite and registry TOML is strict. Unknown keys, schema versions, check kinds,
operators, dependencies, and paths fail with typed diagnostics. Configuration
cannot execute commands, import modules, evaluate code, interpolate environment
variables, or write files.

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
