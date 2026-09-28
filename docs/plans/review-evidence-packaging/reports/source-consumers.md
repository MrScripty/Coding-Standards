# Source-owner and consumer inventory

Inspected at `32e78530096f2884d4c77e0a5a02a0de2ff869fe`, tree
`08759cc18fd2973c105743e050746996fbb67308`. This is a selected implementation
inventory, not a proof that every possible downstream consumer is declared.
No root AGENTS.md or CONTEXT.md was found in this checkout. The current plan index,
Core, routed workflows and existing tool/package contracts supplied admission.

## Existing owners

| Path / API | Observed responsibility | P1 disposition |
| --- | --- | --- |
| `tools/repository_git/repository_git/repository.py`: `GitRepository.read_session`, `read_file`, `revision_paths` | Exact revision-bound file bytes, object checks, bounded sessions and path/mode semantics | Reuse. Source reading must not use archive/worktree bytes or private Engine stores. |
| Same: `git_command`, `git_output`, `sanitized_git_environment` | Bounded Git invocation and output/error adaptation | Reuse; add only packet-needed public read metadata/diff/local-only behavior if required. Do not change existing publication/capture defaults. |
| `tools/repository_git/repository_git/model.py`: `RepositoryRevision`, `RepositoryPath` | Full object IDs and component-safe repository paths | Reuse; unsupported source modes/encodings remain explicit. |
| `tools/repository_git/repository_git/__init__.py` | Public import root | Export any genuinely required new readonly capability; no cross-package private imports. |
| `tools/standards_verifier/standards_verifier/checks/plan_contract.py`: `validate_plan` | Current active-plan structure and lifecycle checks | Use during feature verification; do not copy its private claim parser into the builder or interpret prose as approval. |
| `tools/standards_verifier/standards_verifier/python_packages.py` and `checks/python_package_contract.py` | Package metadata, dependency and entry-point checks | Existing mechanisms should validate the new package; no new verifier engine needed. |
| `evaluation/standards-effectiveness/fixtures/contracts/a1c/python-package-imports.toml` | Explicit checked package population | Add the new package and its appropriate entry-point smoke fixture. |
| `.github/workflows/purpose-separated-engine.yml` | Current Ubuntu/Python 3.12 locked package and structural checks | Add one package test selection; preserve runtime selection and pinned dependency versions. |
| `tools/standards_contracts/requirements.lock` | Existing jsonschema/Git-tool execution environment | Read/reuse. No version change for this work. |
| `docs/plans/routing-fact-ergonomics/{plan.md,issues.md,execution-ledger.md,reports/*}` | Accepted prior change and its source/CI/live/review records | Read-only first example. Never rewrite its decisions or relabel earlier reports. |
| `docs/plans/typed-routing-edits/reports/acceptance-dispositions.md` and six review reports | Closed predecessor acceptance plus preserved advisory/gap records | Read for motivation only; no requalification or status changes. |
| `tools/standards_engine/tests/replay_discovery_qualification.py` | Existing qualification-record parsing/replay with its own semantics | Do not reuse it as a generic evidence validator, run it implicitly, or change it for packaging. Imported outputs remain evidence data. |
| `tools/standards_engine/standards_engine/*` | MCP, validation, applicability orchestration, storage and authority | No production changes or new operation. |

## Proposed new owner

`tools/review_evidence` contains the new request/manifest data contract, assembly,
reader/checker and CLI. A likely small layout is `review_evidence/{model.py,packet.py,
__init__.py,__main__.py}` plus the owned JSON Schema and tests. Exact private file
splits may follow implementation depth; this is not permission to introduce a
framework, plugin mechanism, provider adapter or one wrapper per function.

`model.py` holds validated request/artifact/result values and ordinary JSON-schema
admission; `packet.py` contains the coherent selection/acquisition/inventory/archive
lifecycle; the public root and CLI expose the narrow build/check interface. Git
semantics stay at Repository Git. External local-file reads and ZIP semantics stay
with standard-library/established validators, not a second source identity codec.

Package requirements follow existing `pyproject.toml` conventions, declaring the
current `repository-git` and already hash-locked jsonschema dependency. Inspect
actual import users and smoke fixtures before changing package inventories. The
new package does not depend on Engine or every verifier merely to find review text.

## Source and supplemental revisions for the first example

| Role | Commit | Tree |
| --- | --- | --- |
| Baseline | `ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76` | `6d1f1f8a33d4391c9ab8e315b18bfc25603e1b97` |
| Source candidate | `09d7829df79d2e0c25b8fb9add4b7c47d6368684` | `dffce50ba13e17bc6e55155ca2679a3742f3f658` |
| CI subject | `39d44f007c36684e1ebc546f31a19e20e2e660e5` | `ca0e6c212003fff0d8be2c3d73f2a07b3897bfdd` |
| Later accepted records / inspected source | `32e78530096f2884d4c77e0a5a02a0de2ff869fe` | `08759cc18fd2973c105743e050746996fbb67308` |

The full primary difference contains 49 paths. Five explicit context files in the
planning probe are the contracts runtime, validation feedback, Engine facade,
contract discovery and Analysis routing owner. Their selection is illustrative;
the real reviewer may request more context through a new explicit request.

Source-candidate versus CI-subject differences are `.gitignore`, removal of
`Coding-Standards-agent-workflow-simplification.zip`, and the generated suite-input
manifest. The later records add seven further changed/new documentation paths.
The `tools/` subtree is identical in both comparisons, but neither full tree is the
source tree. The complete path lists are in [probe data](evidence/design-probe.json).
Do not claim exact-commit CI merely from the limited equality.

## Scoped integration

The only live guidance addition outside this plan should be a pointer from the
current tool/plan index and the Engine environment reference to the packet guide.
Do not scatter new normative review obligations throughout standards. Add the new
unit/integration tests and package inventory/CI selection together; refresh the
suite-input manifest using its existing owner. Historical acceptance and delivery
records are sources, never automated rewrite targets.
