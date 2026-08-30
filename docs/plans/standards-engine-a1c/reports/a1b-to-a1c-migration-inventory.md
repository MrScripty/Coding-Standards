# A1b To A1c Migration Inventory

**Status:** Binding input to A1c implementation planning

**Baseline:** accepted A1b implementation
`84412f22fa9fe082f089eaa347c30c23f185ffee`, tree
`8e0f96a61fcea2398418b17d16a061c20f7463f5`

**Target decision:** [A1c ADR](../../../decisions/standards-engine-a1c.md)

No external Standards Engine consumer, retained A1b store, non-test
`open_persisted` caller, or operational backup/restore caller was found by the
accepted audit or A1c current-tree discovery. Migration is therefore an atomic
repository-coordinated replacement. This inventory does not authorize source
mutation.

## Component Dispositions

| A1b component or representation | Current consumers | A1c disposition | Migration and deletion owner | Required evidence |
| --- | --- | --- | --- | --- |
| `standards_identity` encoding and domain-separated hashing | Contracts, Authority, Metadata, Policy Impact, Graph, Analysis, Engine | Retain and narrow to representation-preserving framing and hashing; add only material framing needed by snapshot content and aggregate identities | Identity owner | Existing identity fixtures plus snapshot path/raw-byte framing and cross-domain inequality |
| `standards_contracts` with `jsonschema` and `referencing` | Generated facade, Engine tools, domain contract tests, Verifier | Retain as the sole Draft validator and public contract compiler | Contracts owner | Official/independent Draft evidence, reachable-definition generation, freshness, public producer behavior |
| `standards_authority.capture.GitCaptureSource` and Git command sanitization | Engine snapshot bootstrap; Verifier and suite-input Git observations share sanitization | Move exact Git object and sanitized command behavior to new neutral `repository_git`; reject caller-selected revision at Engine boundary | Repository Git owner | Hostile `GIT_*`, corrupt/missing/type-mismatched object, exact commit, index output, Linux/Windows/macOS Git cases |
| `standards_authority.capture.NativeCaptureSource` and Linux/ext4 platform checks | A1b Engine construction and Authority tests only | Delete; Git object capture is the sole A1c canonical source | Repository Git and Snapshot owners | Public creation has no native fallback; former platform cases receive explicit retirement dispositions |
| `standards_authority` generic envelope, reference, codec-set, repository, memory store, object-kind dispatch, and `put_if_absent` model | Every authority wrapper, Engine composition, Authority tests | Delete after aggregate cutover; no compatibility layer | Snapshot and domain owners | Absence checks, no private imports, aggregate identity/replay and contradiction tests |
| `standards_authority` SQLite one-row object store | Generic Authority repository and recovery tests | Replace with the Snapshot Module's root/content/analysis aggregate schema | Snapshot owner | Transaction, collision, reference retention, quarantine, purge, interruption, integrity, closed-copy tests |
| `standards_authority` backup/restore and `RecoveryReceipt` | Tests only; no operational caller | Delete; closed-store copy is file administration outside the Engine Interface | Snapshot owner and deployment administrator | Public/export absence and closed-store movement documentation/test |
| `ExecutionClosure`, `AuthorityBoundValue`, operation roots, and transitive stored-object traversal | Engine navigation and Analysis authority validation | Delete persisted closure objects; validate direct dependencies once in domain state/codecs and composition-root traversal | Analysis and Engine owners | Missing, contradictory, cycle, unsupported dependency cases and cold replay |
| Engine `OperationAuthorityContract`, role requirements, selections, and compatibility objects | Engine construction and A1b tests | Delete stored objects; retain stable operation IDs and material operation revisions in the canonical interface declaration | Contracts and Engine owners | Operation-reachable generation and affected-operation compatibility fixtures |
| `StandardsAuthorityView` and semantic authority selections | Every Engine operation | Delete; operations take a snapshot root and compile exact domain material from its bytes | Engine composition owner | No ambient source access, equal snapshot input gives equal projection, missing root is typed |
| `ContentSnapshotV2` public authority object and handle | Engine bootstrap, inspect, domain authority codecs | Replace with internal deduplicated content sets owned by unique public snapshot roots | Snapshot owner | Content integrity/dedup tests and proof that content IDs are absent from public results |
| Metadata semantic corpus and policy-unit models/loaders | Policy Impact, Graph, Analysis, Engine, Verifier | Retain; refactor loaders to consume an immutable content source rather than repository paths | Metadata owner | Filesystem and snapshot-source parity, locator and lifecycle fixtures |
| `standards_metadata.authority` codec wrapper | Generic Authority and Engine | Delete after snapshot-source parity; semantic corpus remains Metadata-owned | Metadata owner | Public exports and private-import closure; metadata behavior parity |
| Applicability contracts, programs, truth states, and reverse fact dependencies | Router, Policy Impact, Analysis | Retain unchanged unless exact A1c contract integration requires a material correction | Applicability owner | Existing complete operator/type/state fixtures |
| Policy-impact compiler and semantic models | Graph, Analysis, Engine, Verifier | Retain; consume snapshot-backed corpus/source | Policy Impact owner | Existing compile and source-validation behavior plus snapshot parity |
| `standards_policy_impact.authority` codec wrapper | Generic Authority, Graph authority, Engine | Delete; compiled policy impact is derived from snapshot bytes | Policy Impact owner | Deterministic compile and no stored-wrapper reachability |
| `graph_engine` neutral registry and traversal | Standards Graph, Analysis, Verifier | Retain | Graph Engine owner | Existing graph behavior and traversal fixtures |
| Standards Graph semantic composition | Analysis, Engine navigation, Verifier | Retain; compile from snapshot-backed metadata and policy impact | Standards Graph owner | Current graph parity and snapshot-local compilation |
| `standards_graph.authority` codec wrapper | Generic Authority and Engine | Delete | Standards Graph owner | No wrapper exports/imports and graph behavior parity |
| Analysis change, impact, obligation, reading, routing, and coverage semantics | Engine and repository tests | Retain and simplify around one immutable aggregate | Analysis owner | Existing behavior scenarios plus aggregate transition, dormant decision, and local coverage cases |
| Analysis authority codecs, coverage authority wrappers, trust objects as independent stored kinds | Generic Authority, Analysis kernel, Engine | Replace with domain-owned records inside one `AnalysisState` aggregate; evidence and authorization remain exact fields | Analysis owner | Cold replay, decision reuse/revalidation, child inspection, invalid dependency and authorization cases |
| Analysis `suite_inputs.py` repository-global horizon input | Coverage loader and tests | Delete from product Analysis; suite-input freshness remains Verifier-owned | Analysis and Verification owners | Unrelated repository changes preserve coverage; false-empty horizon evidence remains blocking |
| Engine `authority.py` codecs/views/contracts | Engine and tests | Delete | Engine owner | Absence and replacement facade tests |
| Engine composition and four operation implementations | Generated facade and tests | Rewrite to resolve snapshot roots, compile domain material, and use aggregate Analysis | Engine owner | Eight public caller workflows, typed errors, cold process, no live source after capture |
| Engine rendering and agent tools | Agent-facing facade tests | Retain and update for snapshot operations and composite child handles | Engine Interface owner | Text and structured result parity, no hidden content/store fields |
| Public schema v11, interface declaration, generated Python, agent tools, examples, and identity fixtures | Engine facade, tests, Verifier contract projection | Atomically replace with v12 facade and handle v5; no v11 reader | Contracts and Engine owners | Generation freshness, Draft validation, complete variants, old-version rejection |
| Navigation handles and stored navigation authority objects | Query/inspect tests | Replace with snapshot-bound deterministic projections; do not persist navigation results | Engine and domain owners | Repeated/cold projection equality and inspect reconstruction |
| Analysis handle and immutable-state transition | Prepare/resolve/inspect tests | Retain the single-state model; scope material identity to exact snapshot roots and aggregate decisions | Analysis owner | Branching, idempotence, decision-order normalization, prior-analysis reuse |
| Independently stored context, requirement, observation, coverage, certificate, and trust handles | Inspect tests and generated schema | Replace with composite analysis-child handles backed by the aggregate and derived index | Analysis and Contracts owners | Every advertised child inspectable after cold reopen; no independent storage rows |
| Coverage requirements, attestations, certificates, and completion equality | Analysis and standards-change governance | Retain semantics; store authored attestations/evidence in state and derive requirements/certificates from dependency-local inputs | Analysis and Verification owners | False-empty, exact subject/disposition equality, local invalidation, stale evidence rejection |
| `standards_engine`, Analysis, Metadata, Graph, and Policy Impact package manifests | Package verifier and imports | Replace Authority dependencies with Snapshot, Repository Git, Identity, or no dependency according to the ADR graph | Package owners | Python package contract and import graph verification |
| `standards_verifier` Git consumers | Package, suite-input, reachability, migration checks | Move to `repository_git`; do not depend on Snapshot | Verification owner | Existing hostile environment/index/reachability fixtures |
| A1b Authority/contract/public-cutover suites and fixtures | Complete checkpoint | Replace atomically with A1c snapshot, contract, aggregate, migration, and package-closure suites; do not extend retained Bash checkers | Verification owner | Registered Python suites, intended negative diagnostics, no stale historical source assertions |
| Policy-impact node catalog, package relationships, suite registry, coverage horizon, and attestations | Repository graph, coverage audit, complete checkpoint | Update once after final A1c paths and relationships freeze; regenerate/renew only mechanically selected affected authority | Graph, Planning, Analysis, and audit owners | Exact selected-consumer/disposition equality and valid certificates after final horizon freeze |
| Package READMEs and Engine contract README | Agents and maintainers | Update to the accepted A1c Interface and ownership | Owning package | Documentation traceability and no superseded behavior |
| `.standards-engine/authority.sqlite3` and A1b schema v1 | No retained non-test state | Unsupported and not migrated; A1c uses a distinct store identity/path | Snapshot and deployment owners | Cold start, explicit unsupported old-store outcome, no converter or fallback |

## Exact Production Path Sets

These sets are the binding production write identities used by the active
plan. They do not authorize implementation until their milestone is active.
Paths are listed by identity rather than by mutable file, relationship, or test
counts. A needed path outside these sets changes migration scope and triggers
re-planning.

### Foundation

- `tools/standards_identity/README.md`
- `tools/standards_identity/standards_identity/__init__.py`
- `tools/standards_identity/standards_identity/encoding.py`
- `tools/standards_identity/tests/test_identity.py`
- `tools/repository_git/README.md`
- `tools/repository_git/pyproject.toml`
- `tools/repository_git/repository_git/__init__.py`
- `tools/repository_git/repository_git/errors.py`
- `tools/repository_git/repository_git/model.py`
- `tools/repository_git/repository_git/repository.py`
- `tools/repository_git/tests/test_repository.py`
- `tools/standards_snapshots/README.md`
- `tools/standards_snapshots/pyproject.toml`
- `tools/standards_snapshots/standards_snapshots/__init__.py`
- `tools/standards_snapshots/standards_snapshots/errors.py`
- `tools/standards_snapshots/standards_snapshots/model.py`
- `tools/standards_snapshots/standards_snapshots/module.py`
- `tools/standards_snapshots/standards_snapshots/store.py`
- `tools/standards_snapshots/tests/test_module.py`
- `tools/standards_snapshots/tests/test_store.py`

### Cutover-runtime

The atomic cutover may continue modifying every `Foundation` path. Its
additional runtime
paths are:

- `tools/standards_metadata/README.md`
- `tools/standards_metadata/pyproject.toml`
- `tools/standards_metadata/standards_metadata/__init__.py`
- `tools/standards_metadata/standards_metadata/authority.py`
- `tools/standards_metadata/standards_metadata/corpus.py`
- `tools/standards_metadata/standards_metadata/loader.py`
- `tools/standards_metadata/standards_metadata/paths.py`
- `tools/standards_metadata/standards_metadata/policy_units.py`
- `tools/standards_metadata/standards_metadata/source.py`
- `tools/standards_metadata/tests/test_metadata.py`
- `tools/standards_metadata/tests/test_policy_units.py`
- `tools/standards_policy_impact/README.md`
- `tools/standards_policy_impact/pyproject.toml`
- `tools/standards_policy_impact/standards_policy_impact/__init__.py`
- `tools/standards_policy_impact/standards_policy_impact/authority.py`
- `tools/standards_policy_impact/standards_policy_impact/compiler.py`
- `tools/standards_policy_impact/tests/test_compiler.py`
- `tools/standards_graph/README.md`
- `tools/standards_graph/pyproject.toml`
- `tools/standards_graph/standards_graph/__init__.py`
- `tools/standards_graph/standards_graph/authority.py`
- `tools/standards_graph/standards_graph/metadata.py`
- `tools/standards_graph/standards_graph/policy_units.py`
- `tools/standards_graph/standards_graph/repository.py`
- `tools/standards_graph/tests/test_metadata_graph.py`
- `tools/standards_analysis/README.md`
- `tools/standards_analysis/pyproject.toml`
- `tools/standards_analysis/standards_analysis/__init__.py`
- `tools/standards_analysis/standards_analysis/authority.py`
- `tools/standards_analysis/standards_analysis/coverage.py`
- `tools/standards_analysis/standards_analysis/coverage_authority.py`
- `tools/standards_analysis/standards_analysis/kernel.py`
- `tools/standards_analysis/standards_analysis/keys.py`
- `tools/standards_analysis/standards_analysis/state.py`
- `tools/standards_analysis/standards_analysis/suite_inputs.py`
- `tools/standards_analysis/standards_analysis/trust.py`
- `tools/standards_analysis/tests/contract_support.py`
- `tools/standards_analysis/tests/test_authority.py`
- `tools/standards_analysis/tests/test_coverage.py`
- `tools/standards_analysis/tests/test_routing.py`
- `tools/standards_analysis/tests/test_state.py`
- `tools/standards_engine/README.md`
- `tools/standards_engine/pyproject.toml`
- `tools/standards_engine/standards_engine/__init__.py`
- `tools/standards_engine/standards_engine/authority.py`
- `tools/standards_engine/standards_engine/engine.py`
- `tools/standards_engine/standards_engine/rendering.py`
- `tools/standards_engine/standards_engine/tools.py`
- `tools/standards_engine/tests/test_analysis.py`
- `tools/standards_engine/tests/test_analysis_aggregate.py`
- `tools/standards_engine/tests/test_c7_analysis.py`
- `tools/standards_engine/tests/test_navigation.py`
- `tools/standards_engine/tests/test_rendering.py`
- `tools/standards_verifier/README.md`
- `tools/standards_verifier/pyproject.toml`
- `tools/standards_verifier/standards_verifier/__init__.py`
- `tools/standards_verifier/standards_verifier/checks/git_index_paths.py`
- `tools/standards_verifier/standards_verifier/checks/python_package_contract.py`
- `tools/standards_verifier/standards_verifier/entrypoints.py`
- `tools/standards_verifier/standards_verifier/git_reachability.py`
- `tools/standards_verifier/standards_verifier/python_packages.py`
- `tools/standards_verifier/standards_verifier/suite_inputs.py`
- `tools/standards_verifier/tests/test_git_reachability.py`
- `tools/standards_verifier/tests/test_package_manifest_contract.py`
- `tools/standards_verifier/tests/test_python_package_contract.py`
- `tools/standards_verifier/tests/test_suite_inputs.py`

Files not listed in changed semantic packages remain read-only. Discovery that
their behavior must change, rather than merely continue passing, triggers a
write-set re-plan.

### Cutover-contract

- `tools/standards_contracts/README.md`
- `tools/standards_contracts/tests/test_compiler.py`
- `tools/standards_contracts/tests/test_projection.py`
- `tools/standards_contracts/tests/test_semantics.py`
- `tools/standards_engine/contracts/README.md`
- `tools/standards_engine/contracts/a1-contract.schema.json`
- `tools/standards_engine/contracts/a1-interface.toml`
- `tools/standards_engine/contracts/examples/a1-examples.json`
- `tools/standards_engine/contracts/generated/agent-tools.json`
- `tools/standards_engine/contracts/identity-fixtures.json`
- `tools/standards_engine/standards_engine/_generated_contract.py`
- `tools/standards_engine/tests/test_applicability_contract.py`
- `tools/standards_engine/tests/test_generated_contract.py`

### Cutover-verification

- `evaluation/standards-effectiveness/suite-registry.toml`
- `evaluation/standards-effectiveness/suites/a1b-authority-reconstruction.toml`
- `evaluation/standards-effectiveness/suites/a1b-contract-conformance.toml`
- `evaluation/standards-effectiveness/suites/a1b-public-cutover.toml`
- `evaluation/standards-effectiveness/suites/a1c-aggregate-replay.toml`
- `evaluation/standards-effectiveness/suites/a1c-contract-conformance.toml`
- `evaluation/standards-effectiveness/suites/a1c-public-cutover.toml`
- `evaluation/standards-effectiveness/suites/a1c-snapshot-lifecycle.toml`
- `evaluation/standards-effectiveness/fixtures/architecture/a1b-authority/authority-platform-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/architecture/a1c-snapshots/snapshot-lifecycle-decisions.tsv`
- `evaluation/standards-effectiveness/fixtures/contracts/a1b/python-package-imports.toml`
- `evaluation/standards-effectiveness/fixtures/contracts/a1c/python-package-imports.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1b/missing-admitted-source.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1b/relationship-migration.tsv`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1c/missing-admitted-source.toml`
- `evaluation/standards-effectiveness/fixtures/policy-impact/a1c/relationship-migration.tsv`
- `evaluation/standards-effectiveness/generated/suite-inputs.json`

The new suite files replace the three A1b suites; they do not extend retained
Bash checkers. Registered negative cases assert exact intended diagnostics.

### Cutover-authority

- `evaluation/standards-effectiveness/policy-impact-node-catalog.toml`
- `evaluation/standards-effectiveness/policy-impact/profile.boundary.generated-contract.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.cross-platform.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-impact/topic.security.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/core.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/profile.boundary.generated-contract.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/router.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.architecture.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.contracts.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.cross-platform.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.dependencies.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/topic.security.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.commit.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.planning.toml`
- `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.verification.toml`

Attestation paths are the complete current source list owned by
`attestation-sources.toml`; that registry remains read-only unless final
consumer discovery proves membership itself must change. Each file may change
only when its mechanically derived requirement changes after the complete
cutover
horizon is frozen.

### Cutover-deletions

Every currently tracked path under `tools/standards_authority/` at the accepted
A1b baseline is an exact deletion member. The baseline-bound list is obtained
with:

```bash
git ls-tree -r --name-only 84412f22fa9fe082f089eaa347c30c23f185ffee -- tools/standards_authority
```

The deletion set also contains:

- `tools/standards_metadata/standards_metadata/authority.py`
- `tools/standards_policy_impact/standards_policy_impact/authority.py`
- `tools/standards_graph/standards_graph/authority.py`
- `tools/standards_analysis/standards_analysis/authority.py`
- `tools/standards_analysis/standards_analysis/coverage_authority.py`
- `tools/standards_analysis/standards_analysis/suite_inputs.py`
- `tools/standards_engine/standards_engine/authority.py`
- `tools/standards_engine/tests/test_c7_analysis.py`
- every A1b suite and fixture path named in `Cutover-verification`.

Files that appear in both a replacement set and this set are deleted, not
rewritten. Historical plans, reports, ADRs, and accepted evidence are not
deletion members.

## Consumer Closure

The current production four-operation facade has no external caller in the
repository. The following are nevertheless real migration consumers:

- generated Python and agent-tool public projections;
- Standards Engine and lower package public imports;
- Engine, Analysis, Contracts, Authority, Metadata, Graph, Policy Impact,
  Identity, and Verifier tests;
- Python package-contract enforcement;
- repository graph and package-node authority;
- policy-impact declarations selecting implementation consumers;
- suite registry and generated suite-input evidence;
- coverage horizon, attestations, and certificates; and
- package and contract documentation.

Every consumer is covered by a component row above. A consumer discovered
outside this closure is a re-plan trigger, not an implicit migration.

## Sequencing Constraints

1. Introduce `repository_git` and the Snapshot Module behind their direct
   Interfaces while A1b remains the public facade.
2. Refactor semantic loaders and Analysis to operate on immutable snapshot
   content and one aggregate without adding compatibility fallbacks.
3. Freeze all new package, contract, suite, graph, and policy paths.
4. Atomically cut the Engine facade, generated contract, package graph,
   verification suites, and coverage projection to A1c.
5. Delete generic Authority, owner wrappers, old public forms, and historical
   runtime fixtures in the same replacement boundary.
6. Renew affected coverage authority once, after the final horizon is frozen.
7. Run real platform and cold-process acceptance before A1c is accepted.

Intermediate implementation may use focused direct package tests, but no
milestone may claim complete acceptance while generated, package, graph, or
coverage authority is stale.
