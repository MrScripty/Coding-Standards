# Standards Verifier

The Verifier evaluates the repository's registered structural checks. Use the
Standards Engine public Interface to verify standards and refresh generated
inputs. Python dependencies come from
[`requirements.lock`](../standards_contracts/requirements.lock).

```bash
printf '%s\n' '{"kind":"verify-repository","refresh_verification_inputs":false}' |
  PYTHONPATH=. python3 -P .agents/skills/standards-engine/scripts/invoke.py verify_repository
```

Inspect `verification.passed` and its diagnostics. Set
`refresh_verification_inputs` to `true` after changing declared inputs. The Engine
owns that generated update. Neither operation certifies policy completeness.

## What the checkpoint checks

| Check kind | Actual observation |
| --- | --- |
| `metadata_graph` | Metadata acceptance or rejection for a corpus or fixture |
| `metadata_route` | Routing results for declared task facts |
| `markdown_targets` | Required navigation destinations, independent of link wording |
| `markdown_links` | Declared links and destinations |
| `markdown_link_coverage` | Navigation coverage of a declared member inventory |
| `plan_contract` | Structured plan lifecycle records |
| `policy_impact` | Declared consumer graph and fixture validity |
| `contract_projection` | Generated Interface agrees with canonical contract |
| `python_package_contract` | Declared Python package boundaries |

The complete checkpoint evaluates all registered declarative suites in dependency
order. It does **not** execute the Python unit-test suites, assess prose quality,
or prove that downstream code follows a standard. The graph cannot discover
undeclared consumers merely by validating its existing registrations.

## Testing the implementation

Run functional tests separately when changing the Engine or Verifier:

```bash
PYTHONPATH=.:tools/standards_verifier python3 -m unittest discover -s tools/standards_verifier/tests
PYTHONPATH=. python3 -m unittest discover -s tools/standards_engine/tests
```

These tests exercise execution, navigation, authoring, publication, and failure
handling. Use the locked environment for both commands. The low-level diagnostic
CLI remains `tools/standards_verifier/verify.py` with `--complete`, `--suite`,
`--list-suites`, and JSON output; Engine callers use `verify_repository`.

## Evidence maintenance

Use Engine `maintain_evidence` to retire obsolete checks, fixtures, certificates,
and registered evidence artifacts. Removing an empty suite also removes its graph
node and preserves surviving prerequisites of dependent suites. Consumer review
ownership is distinct from suite evidence: `review:consumer` binds the policy,
relationship, and consumer content without importing an unrelated suite's inputs.
It supplies no automatic attestation.

Synthetic decision tables, exact-prose checks, historical migration inventories,
and arbitrary document budgets have been retired. Git history and captured
snapshots preserve historical observations; the current runner no longer executes
those retired check kinds. Shared TSV projections remain where navigation and
routing checks consume real inventories.
