# External review — boundary-repairs slice only

No PR review happened. Acceptance owner decides status. This is an independent, read-only material review.

## 1. Exact scope

- Baseline: `af6b829aae7beba98c7aa523c51c832011587d12` (interface 43)
- Slice source: `e384fffdcf73e43b2f784619f4812e135f5f3393`
- Final production tree: `fa5722c82a2cb6cd260e5cef8001137bbd1e412b` at `7d563f03`
- `source/` is archive of acceptance-record `506656f8`; per task, its production `tools/` files are identical to `7d563f03`
- Full exact patch: `patches/01-boundary-repairs.diff` — 35 `diff --git` entries
- Human-readable core first: `patches/01-boundary-core.diff` — 835 lines, 15 files:
  - `.github/workflows/purpose-separated-engine.yml`
  - `tools/graph_engine/graph_engine/registry.py`, `tools/graph_engine/tests/test_logical_resolution.py`
  - `tools/standards_analysis/standards_analysis/trust.py`, `tools/standards_analysis/tests/test_authority.py`
  - `tools/standards_contracts/standards_contracts/compiler.py`, `runtime.py`, `tests/test_integer_decoding.py`, `tests/test_projection.py`, `tests/test_semantics.py`
  - `tools/standards_engine/contracts/a1-interface.toml`, `standards_engine/engine.py`, `tests/test_evidence_digest_boundary.py`, `tests/test_numeric_boundary.py`, `tests/test_store_path_boundary.py`
- Core excludes huge one-line generated artifacts and docs/READMEs; full patch adds:
  - `a1-contract.schema.json` Digest `maxLength`, `contracts/examples/a1-examples.json`, `contracts/generated/agent-tools.json`, `standards_engine/_generated_contract.py`, `evaluation/.../suite-inputs.json`
  - `tests/test_compiler.py`, `test_runtime_identity.py`, `test_schema_presentation.py`, `test_consumer_publication.py`
  - READMEs, `.agents/.../environment.md`, `docs/plans/boundary-repairs/*`

Out of slice: F01–F03, F08–F10, F12–F16, caches/GC, routing APIs, later slices.

## 2. Source/evidence inspected

Read directly, not via plan claims:

- [SOURCE_IDENTITY.txt](/tmp/coding-standards-external-review-7d563f03/SOURCE_IDENTITY.txt)
- [plan.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/boundary-repairs/plan.md), [issues.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/boundary-repairs/issues.md), [verification.md](/tmp/coding-standards-external-review-7d563f03/source/docs/plans/boundary-repairs/reports/verification.md)
- [01-boundary-core.diff](/tmp/coding-standards-external-review-7d563f03/patches/01-boundary-core.diff:1) fully (1–835); file list + hunks of `01-boundary-repairs.diff` for schema, generated deltas, identity tests, READMEs
- A1: [registry.py](/tmp/coding-standards-external-review-7d563f03/source/tools/graph_engine/graph_engine/registry.py:257), [paths.py](/tmp/coding-standards-external-review-7d563f03/source/tools/graph_engine/graph_engine/paths.py:8), consumers [repository.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_graph/standards_graph/repository.py:51), [context_projection.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/context_projection.py:104)
- A2: [engine.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/engine.py:496), [store.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/store.py:261), [module.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_snapshots/standards_snapshots/module.py:73)
- A3: [runtime.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_contracts/standards_contracts/runtime.py:107), [union_selection.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_contracts/standards_contracts/union_selection.py:31), domain `type is int` checks in `logical_authoring.py`, [tools.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/tools.py:448) `_decode_call`/`propose`
- A4: [trust.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_analysis/standards_analysis/trust.py:47), [logical_authoring.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/standards_engine/logical_authoring.py:143), [a1-contract.schema.json](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/contracts/a1-contract.schema.json:303), generated `_SCHEMA` Digest, [compiler.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_contracts/standards_contracts/compiler.py:28)
- A5: [purpose-separated-engine.yml](/tmp/coding-standards-external-review-7d563f03/source/.github/workflows/purpose-separated-engine.yml:63), `a1-interface.toml`, `a1-examples.json`, `agent-tools.json`, identity test hunks
- Tests in `source/`: `test_logical_resolution.py`, `test_store_path_boundary.py`, `test_integer_decoding.py`, `test_numeric_boundary.py`, `test_evidence_digest_boundary.py`, `test_authority.py`, `test_projection.py`, `test_semantics.py`, `test_compiler.py` hunk

No shell, no test execution. CI counts and verification.md totals were not used as proof.

## 3. Assessment by claim

A1 — Logical isolation: fix moves `if _logical_artifacts is not None` before path-spelling branch. Bare names no longer fall to `(repo_root/requested).exists()`. Registered aliases still early-return; `_logical_artifact` still raises `PathEscapeError` for `..`, absolute, `./`, non-canonical. Filesystem mode unchanged. Negative oracle is independent: real file/dir/symlink/dangling create/remove across bare + nested names, plus `Path.exists`/`resolve` patched to fail. Covers `standards_graph` and projection consumers which pass `logical_artifacts`.

A2 — Final-component admission: Engine now `store_path.parent.resolve() / store_path.name` instead of `store_path.resolve()`. Store still owns `lstat` regular-non-symlink check, `RELATIVE_PATH`, `O_EXCL|O_NOFOLLOW` creation. Relative stays cwd-relative; intermediate symlinks permitted; final symlink/dangling/dir rejected with `SNAPSHOT_STORE.UNSUPPORTED_PATH` and byte preservation. Unavailable-parent still `OSError`, explicitly not generalized. Not race-free sandboxing is disclosed in plan + snapshots README.

A3 — Integer normalization: only `type=="integer"` or list with `integer` and without `number`, and only `type(value) is float`, becomes `int` after root `Draft202012Validator` + `_ensure_json_value` (finite, strict JSON). Boolean schemas return value; `const`/`enum`/`default`, number-only, unconstrained preserved; `int` arbitrary precision untouched (no float conversion); new containers (`tuple`/`FrozenMap`/model) avoid input mutation. Sibling `$ref`/`oneOf` + `properties`/`items`/`additionalProperties`, `nullable`/implicit shapes, anonymous `properties` vs map `additionalProperties`, and `$ref`+`oneOf` ordering are handled. `uniqueItems` validated before conversion. Domain `type is int` rules unchanged; floats previously schema-valid but domain-rejected now decode to `int` before domain use. Oracles: independent `Draft202012Validator`, `assertIs(type,…)`, deepcopy, generated `compile_contracts`+`exec`, facade + cold stdio, no-draft + `main` unchanged.

A4 — Digest syntax + live bytes: Analysis now `type is str` + `fullmatch(r"sha256:[0-9a-f]{64}")`; `ResolvedEvidence` still hashes bytes and raises `EVIDENCE_DIGEST_MISMATCH`. Canonical `Digest` adds `maxLength: 71` to `pattern`, fixing Python `re` `$`-before-newline acceptance (`72+` char strings with trailing `\n` now length-rejected; no `<=71` spurious match remains). Compiler only admits existing Draft 2020-12 keyword; `jsonschema` remains executable owner. Shared 17-case corpus checks generated + Analysis + authoring against independent validator; invalid propose yields `INTERFACE.INVALID_ARGUMENTS` with `maxLength` feedback and no draft.

A5 — CI + interface 44: workflow adds six `unittest discover` lines (identity, applicability, graph_engine, standards_graph, snapshots, repository_git) with locked Python 3.12 + `--require-hashes`. Interface bumps 43→44 in `a1-interface.toml`, `a1-examples.json` (3 spots), `agent-tools.json`, identity/presentation/publication tests; Digest `maxLength` present in canonical schema, `agent-tools.json`, `_generated_contract.py`. Freshness assertion retained and previously caught stale examples per verification history.

Ownership, contracts, failures: Graph, SnapshotStore (+Engine composition), Contracts, Analysis, interface edition each retain authority; no new module/dependency. Public delta is only Digest `maxLength` + interface 44; 40 ops, request v6, projection v7, handle/schema/SQLite versions unchanged; valid digests/records need no migration. Each boundary keeps its typed failure and rejects before effects.

## 4. Findings

No blocker found in slice material.

1. Severity: Low | [runtime.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_contracts/standards_contracts/runtime.py:113) | Invariant: validated boolean schemas declare no representation | Impact: root `True` with list/dict returns original mutable object, while `{}` freezes; scalar `items: True/False` path is correct and tested | Disposition: accept; note inconsistency, not exercised by canonical corpus.
2. Severity: Low | [runtime.py](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_contracts/standards_contracts/runtime.py:118) | Invariant: conflicting outer `number` + inner `integer` via `$ref` | Impact: decodes to `int` via inner; no test; canonical corpus has no such conflict | Disposition: accept; document precedence if such schemas ever appear.
3. Severity: Info | [a1-contract.schema.json](/tmp/coding-standards-external-review-7d563f03/source/tools/standards_engine/contracts/a1-contract.schema.json:308) | Invariant: other `^…$` ID patterns (`ObligationId`, `ImpactTraceId`, etc.) still lack `maxLength` | Impact: same `$`-before-newline acceptance remains outside F07a/Digest scope; 325/326 definitions intentionally unchanged | Disposition: follow-up, not this slice.
4. Severity: Info | tests | Invariant: untyped/opaque container aliasing | Impact: `decode` returns same dict/list object for literal/untyped containers; input not mutated but output aliases input | Disposition: accept; tests assert no input mutation, not output independence.

## 5. Gaps (not verified here)

- No execution: byte-exact generator freshness, full suite, reconstruction, retained-state replay, and supported Python 3.11/3.12 CI were not run (read-only session; verification.md records local 3.13.5 + pending locked CI).
- `evaluation/.../suite-inputs.json` regenerated blob and full one-line `_generated_contract.py`/`agent-tools.json` beyond Digest hunks not line-audited.
- README/`environment.md` prose deltas only sampled; `test_registry.py` baseline logical test only located.
- Completeness of “six missing suites” against every `tools/*` not enumerated.

## 6. Recommendation

**Satisfied** for this one boundary-repairs slice on material correctness, ownership, failure stages, and negative-oracle independence.

Qualification for acceptance owner: A6 locked-runtime CI on Python 3.12 with unchanged lock must still pass before `Accepted`; this review does not replace that run.

