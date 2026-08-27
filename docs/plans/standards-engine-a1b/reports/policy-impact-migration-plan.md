# A1b Policy-Impact Consumer Migration Plan

**Status:** Proposed planning authority

## Reason

A1b creates three implementation Modules and retires several registered
implementation artifacts. Those are semantic-consumer changes under the
accepted compiled policy-impact authority. They are not incidental filesystem
moves.

The atomic cutover must update the supplemental node catalog and source-owned
relationships in the same proposed authority view, analyze prior/current
impact, assign every selected consumer a disposition, freeze the final horizon,
register every owner-local attestation source before that freeze, and renew
mechanically stale coverage.

Foundation Modules are working-tree checkpoints, not separately committed
repository boundaries. The first implementation commit contains the
foundations and this complete semantic-consumer migration together, so no
committed tree contains new implementation consumers without their catalog,
relationship, disposition, and coverage authority.

## Catalog Dispositions

| Artifact | A1b disposition |
| --- | --- |
| `tools/standards_engine/contracts/a1-contract.schema.json` | Retain and update |
| `tools/standards_engine/contracts/a1-interface.toml` | Add as the closed public operation and capability authority |
| `tools/standards_engine/contracts/examples/a1-examples.json` | Retain; replace every v10 request, result, and inspection example with v11 values |
| `tools/standards_engine/contracts/identity-fixtures.json` | Retain; replace v1 normalized expectations with the complete v2 domain/version matrix |
| `tools/standards_engine/contracts/generated/agent-tools.json` | Retain and regenerate from the v11 per-operation closure |
| `tools/standards_engine/contracts/README.md` | Retain and update contract, generation, validation, and version instructions |
| `tools/standards_contracts/pyproject.toml` | Add as the direct dependency and package contract |
| `tools/standards_contracts/requirements.lock` | Add as the exact hash-checked resolution |
| `tools/standards_contracts/standards_contracts/__init__.py` | Add as the narrow compiler/projection public Interface |
| `tools/standards_contracts/README.md` | Add as the package Interface and operation guide |
| `tools/standards_identity/pyproject.toml` | Add as the stdlib-only identity package contract |
| `tools/standards_identity/standards_identity/__init__.py` | Add as the narrow encoding/hashing public Interface |
| `tools/standards_identity/README.md` | Add as the identity encoding and hashing Interface guide |
| `tools/standards_authority/pyproject.toml` | Add as the Identity-backed authority package contract; Authority and Contracts have no dependency in either direction |
| `tools/standards_authority/standards_authority/__init__.py` | Add as the narrow exact-list content-capture, envelope-integrity, SQLite direct-lookup, explicit-codec-injection, roots-only closure, backup, and recovery public Interface; domain codec sets retain semantic construction, identity, dependency extraction, and decoding |
| `tools/standards_authority/README.md` | Add as the exact-list capture, SQLite schema-v1 repository, codec injection, closure, backup, and recovery Interface guide |
| `evaluation/standards-effectiveness/policy-units/dependencies.toml` | Retain and add one reviewed revision-1 unit for the exact `Requirement And Ownership` heading |
| `evaluation/standards-effectiveness/policy-units/cross-platform.toml` | Add one reviewed revision-1 unit for the exact `Filesystem Paths` heading |
| `evaluation/standards-effectiveness/policy-impact/topic.cross-platform.toml` | Add source-owned Cross-Platform implementation, package, fixture, and suite relationships |
| `evaluation/standards-effectiveness/policy-units/security.toml` | Add one reviewed revision-1 unit for the exact `Filesystem Containment` heading |
| `evaluation/standards-effectiveness/policy-impact/topic.security.toml` | Add source-owned descriptor-relative containment implementation, fixture, and suite relationships |
| `evaluation/standards-effectiveness/policy-units/registry.toml` | Retain and register the new Cross-Platform and Security sidecars in the canonical policy-unit corpus |
| `evaluation/standards-effectiveness/policy-impact-registry.toml` | Retain and register the new Cross-Platform and Security declaration sources in the closed relationship corpus |
| `evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml` | Retain and register the new owner-local Cross-Platform and Security attestation sources |
| `evaluation/standards-effectiveness/policy-coverage/attestations/topic.dependencies.toml` | Retain and add reviewed attestations for the final frozen Requirement And Ownership coverage requirements |
| `evaluation/standards-effectiveness/policy-coverage/attestations/topic.cross-platform.toml` | Add reviewed attestations for the final frozen Cross-Platform coverage requirements |
| `evaluation/standards-effectiveness/policy-coverage/attestations/topic.security.toml` | Add reviewed attestations for the final frozen Security coverage requirements |
| `tools/standards_engine/README.md` | Retain and update the public v11 facade and unsupported-version behavior |
| `tools/graph_engine/graph_engine/__init__.py` | Retain; expose every Graph Engine symbol required by another Module, including the contained-path contract |
| `tools/standards_engine/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13` and declare every directly imported internal package, including Contracts, Authority, and Identity |
| `tools/standards_applicability/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; remain stdlib-only |
| `tools/standards_applicability/standards_applicability/__init__.py` | Retain as the literal public export authority |
| `tools/standards_metadata/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare Authority and Identity directly |
| `tools/graph_engine/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; remain stdlib-only |
| `tools/standards_policy_impact/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare Graph Engine, Applicability, Authority, Identity, and Metadata directly |
| `tools/standards_policy_impact/standards_policy_impact/__init__.py` | Retain as the literal public export authority; add its exact immutable object codec set |
| `tools/standards_graph/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare Graph Engine, Authority, Identity, Metadata, and Policy Impact directly |
| `tools/standards_graph/standards_graph/__init__.py` | Retain as the literal public export authority; add its exact immutable object codec set |
| `tools/standards_analysis/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare Graph Engine, Applicability, Authority, Identity, Metadata, and Policy Impact directly |
| `tools/standards_verifier/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare every directly imported Engine Module, including Contracts |
| `tools/standards_verifier/standards_verifier/__init__.py` | Retain and replace the version-only root with a literal public export contract for `repository_graph_main`, `git_reachability_main`, `verifier_main`, `generated_artifacts_main`, `numeric_audit_main`, and `numeric_retirements_main` |
| `tools/standards_verifier/standards_verifier/entrypoints.py` | Add as the sole owner of repository-entrypoint parsing, diagnostics, default-root injection, and domain dispatch |
| `tools/standards_verifier/standards_verifier/python_packages.py` | Add as manifest-owned package/dependency projection and AST import analysis |
| `tools/standards_verifier/standards_verifier/checks/python_package_contract.py` | Add as the typed direct-import and public-root conformance check |
| `tools/standards_verifier/tests/test_python_package_contract.py` | Add focused parser, export-resolution, ownership, and diagnostic tests |
| `tools/query_edges.py` | Retain as a Verifier-owned repository entrypoint; replace private Graph Engine and Verifier imports with one public Verifier adapter |
| `tools/verify_git_reachability.py` | Retain as a Verifier-owned repository entrypoint; replace ambient private Verifier imports with the public root |
| `tools/standards_verifier/verify.py` | Retain as a Verifier-owned repository entrypoint; replace ambient alternate-root import with the canonical Verifier root |
| `tools/standards_verifier/generate_inventory.py` | Retain as a Verifier-owned repository entrypoint; replace ambient alternate-root import with the canonical Verifier root |
| `tools/standards_verifier/generate_numeric_audit.py` | Retain as a Verifier-owned repository entrypoint; replace ambient alternate-root import with the canonical Verifier root |
| `tools/standards_verifier/generate_numeric_retirements.py` | Retain as a Verifier-owned repository entrypoint; replace ambient alternate-root import with the canonical Verifier root |
| `docs/plans/standards-engine-a1b/reports/dependency-and-dialect-decision.md` | Retain as the reviewed selection authority |
| `docs/plans/standards-engine-a1b/reports/a1b-dependency-provenance.md` | Add as exact implementation resolution evidence |
| `tools/standards_engine/contracts/generate_contract.py` | Retire; replace with `tools/standards_contracts/standards_contracts/projection.py` |
| `tools/standards_engine/contracts/validate_contracts.py` | Retire; replace with `tools/standards_contracts/standards_contracts/compiler.py` |
| `tools/standards_engine/standards_engine/_generated_contract.py` | Retain and regenerate |
| `tools/standards_engine/standards_engine/__init__.py` | Retain and update; export the Engine codec set and generated public facade algebra |
| `tools/standards_engine/standards_engine/tools.py` | Retain and update |
| `tools/standards_engine/standards_engine/engine.py` | Retain; inject exact owner-local codec sets, compose reference-only StandardsAuthorityViews, store four executable OperationAuthorityContractV2 values, and mechanically derive roots-only side- and role-qualified ExecutionClosureV2 values from owner-produced AuthorityBoundValues |
| `tools/standards_engine/standards_engine/rendering.py` | Retain; render the exhaustive generated v11 result algebra, including `FactRequirementWork` |
| `tools/standards_engine/standards_engine/model.py` | Retire; it is only a compatibility re-export over the generated algebra |
| `tools/standards_metadata/standards_metadata/serialization.py` | Retire; replace with `tools/standards_identity/standards_identity/encoding.py` |
| `tools/standards_metadata/standards_metadata/__init__.py` | Retain; remove retired serialization exports and export only Metadata-owned contracts plus its exact immutable object codec set |
| `tools/standards_analysis/standards_analysis/snapshots.py` | Retire; replace capture with `tools/standards_authority/standards_authority/capture.py` and storage with `repository.py` |
| `tools/standards_analysis/standards_analysis/__init__.py` | Retain; remove retired serializer/snapshot exports and expose only Analysis-owned types, transitions, and its exact immutable object codec set |
| `tools/standards_analysis/standards_analysis/resolution.py` | Retain pure analysis transition behavior and update dependencies |
| `tools/standards_analysis/standards_analysis/results.py` | Retain pure domain projection and update dependencies |
| none | Add `tools/standards_contracts/standards_contracts/compiler.py` |
| none | Add `tools/standards_contracts/standards_contracts/projection.py` |
| none | Add `tools/standards_identity/standards_identity/encoding.py` |
| none | Add `tools/standards_authority/standards_authority/repository.py` for generic envelope integrity, explicit codec dispatch, in-memory storage, and SQLite schema-v1 direct lookup/backup |
| none | Add `tools/standards_authority/standards_authority/capture.py` for exact-list Git/native capture into logical-path/raw-byte ContentSnapshotV2 values |
| `.gitignore` | Retain and add only local Standards Authority SQLite runtime files; authored authority remains text in Git |

The listed Engine Module manifests form one exact source-tree dependency
closure. They are not independently published artifacts in A1b, so the plan
does not invent a wheel-build backend or claim a local distribution-install
contract. `standards_identity`, `standards_applicability`, and Graph Engine are
stdlib-only. `standards_contracts` declares exact direct external requirements
for `jsonschema` and `referencing`; its lock closes transitives.
`standards_authority` declares Identity only and owns its closed internal
envelope proof. `standards_contracts` and `standards_authority` have no
dependency in either direction. Domain Modules that persist objects declare
Authority and export the exact owner-local codec sets admitted in
`c7-design-proposal.md`. Every manifest also owns one canonical
source-tree public import root and exact repository entrypoint set. Every root
owns exported symbols through the closed statically resolvable `__all__`
profile. Every other manifest declares exactly the internal packages imported
directly by its production source: no missing direct requirement, transitive
satisfaction, unused internal requirement, unowned source, private child,
root-form unexported child, star, or dynamic cross-Module import is accepted.
Every listed manifest uses `requires-python = ">=3.11,<3.13"`.

Milestone 3 derives governed source ownership and the direct-import graph from
the Git index, manifests, and production Python syntax. One AST-backed verifier
resolves root `__all__` values and rejects below-root, root-form unexported,
star, and literal or dynamic cross-Module imports. It does not copy `__all__` or
maintain another package or symbol allowlist. The cutover then creates clean
CPython 3.11 and 3.12 environments, installs the exact external lock, changes to
a directory outside the repository, supplies the reviewed checkout root as the
sole `PYTHONPATH`, enables Python safe-path mode, imports every
manifest-owned public Module root and export, and executes every exact
repository entrypoint against isolated inputs. This is the reproducible
execution contract the repository actually uses. A newly required local wheel,
independently published distribution, build backend, public root, or import
outside this graph is a re-plan trigger.

## Public Import Systemic Dispositions

The A1b cutover audits the complete current production family before mutation.
These are stable path dispositions, not a mutable file-count assertion:

| Current consumer | Current boundary | A1b disposition |
| --- | --- | --- |
| `tools/standards_policy_impact/standards_policy_impact/compiler.py` | Imports `graph_engine.errors` and `graph_engine.paths` below the public root | Update to Graph Engine root exports; add `contained_path` to the root contract |
| `tools/standards_verifier/standards_verifier/repository_graph.py` | Imports `graph_engine.manifest` below the public root | Update to the existing public `load_registry` export |
| `tools/standards_analysis/standards_analysis/serialization.py` | Imports Metadata serialization below the public root | Retire with the generic Analysis serializer |
| `tools/standards_engine/contracts/validate_contracts.py` | Imports Metadata serialization and the old generator through private paths | Retire; public validation moves to `standards_contracts` |
| `tools/standards_engine/contracts/generate_contract.py` | Old contract-tool implementation and private self-import target | Retire; projection moves to `standards_contracts` |
| `tools/standards_engine/standards_engine/tools.py` | Imports the old private contract validator | Update to the `standards_contracts` public root |
| `tools/query_edges.py` | Imports Graph Engine CLI and Verifier repository composition privately through ambient path mutation | Update to one Verifier public repository-graph CLI adapter and register the script in the Verifier manifest |
| `tools/verify_git_reachability.py` | Imports Verifier reachability internals through ambient path mutation | Update to the Verifier public root and register the script in the Verifier manifest |
| `tools/standards_verifier/verify.py` | Imports Verifier CLI through the alternate ambient `standards_verifier` root | Update to the canonical Verifier root and prove safe-path execution from outside the checkout |
| `tools/standards_verifier/generate_inventory.py` | Imports generated-artifact behavior through the alternate ambient `standards_verifier` root | Update to the canonical Verifier root and prove safe-path execution from outside the checkout |
| `tools/standards_verifier/generate_numeric_audit.py` | Imports numeric-audit behavior through the alternate ambient `standards_verifier` root | Update to the canonical Verifier root and prove isolated safe-path execution |
| `tools/standards_verifier/generate_numeric_retirements.py` | Imports numeric-retirement behavior through the alternate ambient `standards_verifier` root | Update to the canonical Verifier root and prove isolated safe-path execution |
| `tools/standards_engine/standards_engine/__init__.py` | Computes facade exports from the compatibility model | Replace with the closed local-star `__all__` profile over generated v11 exports plus literal facade exports |
| Every other governed production Python source | Uses only current package roots or own-package imports at the inventory base | `reviewed-no-change`; the final Git-index-derived verifier proves the classification and any new sibling triggers re-planning |

The dependency-owned relationship migration adds the new package-contract
policy unit, every catalog-listed manifest, public root, and repository
entrypoint, the canonical entrypoint-adapter module, the AST projection/check,
its focused test, the registered public cutover suite, and its
positive/negative fixtures. Generated Contract
relationships additionally select the generated output, facade root, compiler
prelude, and their two private-import fixture families. The final relationship
report records every exact natural key; no global relationship count is an
oracle.

The following current generic-serializer consumers become explicit semantic
consumers. They are retained unless stated otherwise:

| Current consumer | A1b disposition |
| --- | --- |
| `tools/standards_analysis/standards_analysis/serialization.py` | Retire; domain files import identity hashing directly and define typed semantic keys locally |
| `tools/standards_analysis/standards_analysis/facts.py` | Retain; construct fact-contract, requirement, observation, and ordering records explicitly |
| `tools/standards_analysis/standards_analysis/coverage.py` | Retain; construct coverage-view, requirement, attestation, certificate, and content-fingerprint records explicitly |
| `tools/standards_analysis/standards_analysis/impact.py` | Retain; construct impact-trace and projection records explicitly |
| `tools/standards_analysis/standards_analysis/obligations.py` | Retain; construct obligation, scope, fact-value, evidence-owner, and decision-dependency keys explicitly |
| `tools/standards_analysis/standards_analysis/reading.py` | Retain; replace generic serialized ordering and deduplication with typed reading-selection keys |
| `tools/standards_analysis/standards_analysis/resolution.py` | Retain; construct analysis-root identity and typed transition-conflict keys |
| `tools/standards_analysis/standards_analysis/results.py` | Retain; replace generic operation ordering and deduplication with typed result keys |
| `tools/standards_metadata/standards_metadata/policy_units.py` | Retain; advance policy-unit structural encoding to v2 |
| `tools/standards_engine/standards_engine/engine.py` | Retain; remove serializer-backed state storage and candidate deduplication |

These paths are added to the supplemental catalog when a policy-impact
relationship selects their semantics. The package-contract verifier test is an
explicit systemic consumer because it owns the parser/export-resolution oracle.
Other package tests remain suite inputs rather than individually authored
relationship authority unless the final horizon audit proves a missing
semantic consumer.

The catalog rows above are the stable semantic-consumer identities. Package
tests remain registered suite inputs. A package-private support file may be
created inside its admitted Module write set only when it implements one listed
consumer without creating a second authority or public Interface. A new
production responsibility, public entry point, semantic consumer, source split,
or unresolved ownership decision requires re-analysis and a plan write-set
amendment before mutation.

## Fixture And Generated-Artifact Authority

| Artifact | Authority classification | A1b derivation and review rule |
| --- | --- | --- |
| `reports/a1-contract-v11.schema.json` | Authored proposed public-shape authority | Independently admit its exact bytes and SHA-256 before implementation; promote it byte-for-byte to the canonical production schema at cutover. Any shape change requires re-planning. |
| `reports/a1-interface-v11.toml` | Authored proposed operation/capability authority | Independently admit its exact bytes and SHA-256 before implementation; promote it byte-for-byte to the canonical production interface at cutover. Any operation or capability change requires re-planning. |
| `contracts/examples/a1-examples.json` | Authored public contract fixtures | Manually replace v10 values with reviewed v11 operation/result/inspection examples. Validate through the production compiler; no generator writes this file. |
| `contracts/identity-fixtures.json` | Authored expected-value oracle | Manually replace v1 expectations and add independently reviewed identity-v2 framing/domain cases. Both the identity implementation and facade tests consume it; no implementation generates its expected digests. |
| `contracts/generated/agent-tools.json` | Disposable checked-in generated projection | Regenerate deterministically from the canonical v11 schema plus `a1-interface.toml`; freshness requires byte equality and manual edits are invalid. |

The two authored corpora are independent evidence inputs, not projections of
the code they test. The generated agent-tool file is output, not semantic
authority. This distinction is preserved in source headers, package docs, and
suite registration.

## Existing Relationship Dispositions

| Policy source | Current relationship disposition | Proposed relationship authority |
| --- | --- | --- |
| `topic.contracts.generated-semantic-conformance` | Replace `generate_contract.py`; retain Router, profile, Build, Tooling, prompts, generated algebra, facade, tool adapter, fixture, and suite | Add `a1-interface.toml`, compiler, and projection; projection replaces the old generator edge |
| `topic.contracts.schema-dialect-and-vocabulary` | Retain profile, Dependencies, schema, fixture, and suite; replace generator and validator | Compiler replaces validator; compiler plus projection replace the old generator relationship |
| `topic.contracts.identity-versus-instance-equality` | Retain Applicability, reproduction report, and suite; retire metadata serializer, local validator, generated-validator meaning, and model intermediary | Add identity encoder, contract compiler, policy-unit structure owner, and all typed Analysis identity/order consumers listed above |
| `topic.architecture.authority-scope-admission` | Retain the accepted profile, planning, implementation, schema, generator, generated model, facade, fixture, and suite relationships | Add StandardsAuthorityView composition, exact owner codec injection, stable roles, separate operation-authority contracts, AuthorityBoundValue production, and the execution-closure audit; the view references semantic authorities without acquiring them |
| `topic.contracts.declaration-and-semantic-authority` | Retain the accepted declaration/executable/domain-owner relationships | Add domain-owned semantic object constructors and AuthorityBoundValue projections; the generic repository validates envelopes but does not own domain semantics |
| `topic.contracts.version-scope-and-invalidation` | Retain the accepted version-scope consumers; replace A1 snapshot/resolution invalidation behavior | Add exact path/byte ContentSnapshotV2, StandardsAuthorityView, separate OperationAuthorityContractV2 values, roots-only ExecutionClosureV2, direct consumed-trust authority, and material navigation/analysis identities; remove copied version bags, complete views, hypothetical-future closure, and locator/metadata invalidation |
| `topic.architecture.immutable-authority-closure` | Retain engine, analysis transition/result, fixture, suite, and Persistence; replace snapshot compiler | Add exact-list content capture, generic SQLite authority repository, explicit owner-local codec injection, StandardsAuthorityView, roots-only side/role closure derivation, direct consumed-trust objects, and cold-reconstruction suite |
| `topic.dependencies.implementation-versus-dependency` | Retain Router, profile, prompts, fixture, and suite | Add contract package manifest, exact lock, compiler, and dependency provenance report |
| `topic.dependencies.requirement-and-ownership` | New projection of the existing `Requirement And Ownership` heading at semantic revision 1 | Add every catalog-listed Engine Module manifest and public root, the Verifier-owned repository entrypoints and adapter module, package-contract projection/check/test, and registered public-cutover fixtures and suite |
| `profile.boundary.generated-contract.semantic-closure` | Retain Contracts, Verification, Build, Dependencies, schema, generated algebra, tool adapter, fixture, and suite; replace generator | Add interface contract, compiler, and projection; projection replaces the generator edge |
| `topic.cross-platform.filesystem-paths` | New projection of existing `topics/cross-platform.md` `Filesystem Paths` heading at semantic revision 1 | Add Authority repository/capture, its required-real suite, and the Cross-Platform package/README projection |
| `topic.security.filesystem-containment` | New projection of existing `topics/security.md` `Filesystem Containment` heading at semantic revision 1 | Add descriptor-relative Authority repository/capture and its containment/race suite |

`standards_engine/rendering.py` follows generated-semantic-conformance and the
Generated Contract profile because it must exhaustively project the public
result algebra. The Metadata and Analysis package initializers follow
identity-versus-instance-equality and immutable-authority-closure respectively
because their public exports must remove the retired serializer and snapshot
authorities. Engine composition and the Authority public root additionally
follow authority-scope admission, declaration/semantic authority, and version
scope because they select references, dispatch semantic owners, and derive
material invalidation without becoming umbrella semantic authority.

Relationship declarations remain source-owned in their current module files.
`policy-impact-registry.toml` remains the sole closed membership authority for
those files. The new Cross-Platform and Security files are added there
explicitly; neither filesystem presence nor policy-unit registration implies a
relationship source. No generic graph manifest or path inference creates these
replacements.

The new policy units for Dependencies Requirement And Ownership, Cross-Platform
Filesystem Paths, and Security Filesystem Containment do not change normative
prose. Their revision 1 is a reviewed bootstrap assertion that
the exact canonical module, locator, resolved content/structure, and initial
implementation relationships represent the already accepted meaning. Each
locator must resolve exactly once and its module must own its declaration.
Planning admission reviews the identity/locator; final A1b coverage
independently audits the frozen relationship and horizon state before
attestation.

## Natural-Key Replacement Map

Migration evidence uses the stable natural key
`(source, relation, consumer)`. One old relationship may split into several
new relationships:

| Source | Old consumer | Disposition | Proposed consumer or rule |
| --- | --- | --- | --- |
| `topic.contracts.generated-semantic-conformance` | `tools/standards_engine/contracts/generate_contract.py` | replace/split | `a1-interface.toml`, contract compiler, and projection compiler |
| `topic.contracts.schema-dialect-and-vocabulary` | `tools/standards_engine/contracts/generate_contract.py` | replace/split | contract compiler and projection compiler |
| same | `tools/standards_engine/contracts/validate_contracts.py` | replace | contract compiler |
| `topic.contracts.identity-versus-instance-equality` | `tools/standards_metadata/standards_metadata/serialization.py` | replace/split | identity encoder and domain-owned identity/order consumers |
| same | `tools/standards_engine/contracts/validate_contracts.py` | replace | contract compiler |
| same | `tools/standards_engine/standards_engine/_generated_contract.py` | correct | generated models retain shape only; contract compiler owns validation |
| same | `tools/standards_engine/standards_engine/model.py` | retire/split | generated handle shapes, authority repository, and domain identity constructors |
| `topic.architecture.immutable-authority-closure` | `tools/standards_analysis/standards_analysis/snapshots.py` | replace/split | authority capture and repository |
| `topic.architecture.authority-scope-admission` | no current edge for StandardsAuthorityView composition or execution-closure derivation | add missing consumers | Engine composition, exact codec injection, stable roles, separate operation-authority contracts, AuthorityBoundValue producers, and the closure audit |
| `topic.contracts.declaration-and-semantic-authority` | no current edge for owner-local authority decoding | add missing consumers | domain constructors, exact codec sets, and projections; generic repository remains envelope-only and independent of public Contracts |
| `topic.contracts.version-scope-and-invalidation` | A1 schema, generator, generated model, facade, snapshot, and resolution use umbrella interface/component versions | correct/split | exact logical-path/raw-byte content identity, authority-view selection identity, per-operation role/dynamic-role identity, roots-only material closure, exact consumed-trust authority, and owner-local material navigation/analysis identity |
| `topic.architecture.immutable-authority-closure` | no current edge for reference-only view and structural dependency closure | add missing consumers | StandardsAuthorityView, roots-only ExecutionClosureV2, exact ProviderAuthorityV1/AuthorizationGrantV1 consumption, explicit owner-local codec dispatch, SQLite storage, exact-list capture, and mutation/cold-process verification |
| `profile.boundary.generated-contract.semantic-closure` | `tools/standards_engine/contracts/generate_contract.py` | replace/split | interface contract, contract compiler, and projection compiler |
| same | no current edge for `contracts/generated/agent-tools.json` | add missing consumer | generated agent-tool projection |
| same | no current edge for `contracts/examples/a1-examples.json` | add missing consumer | public serialized example corpus |
| `topic.contracts.identity-versus-instance-equality` | no current edge for `contracts/identity-fixtures.json` | add missing consumer | identity v2 and domain-version fixture authority |
| `topic.dependencies.implementation-versus-dependency` | no current implementation edge | add/split | contract package manifest, exact lock, compiler, dependency decision, and implementation provenance report |
| same | no current edge for the new Identity and Authority package manifests | add missing consumers | exact stdlib-only Identity and Identity-backed Authority package contracts; Contracts and Authority remain independent |
| `topic.dependencies.requirement-and-ownership` | no current policy unit or implementation edge | add | exact existing-heading unit; every catalog-listed Engine Module manifest and public root; package-contract projection, check, focused test, fixtures, and suite |
| same | no current edge for `tools/query_edges.py` or `tools/verify_git_reachability.py` | add missing consumers | Verifier-owned repository entrypoints using only public package roots |
| same | no current edge for the Verifier-local repository entrypoints | add missing consumers | canonical-root updates through the new `entrypoints.py` owner and safe-path execution for `verify.py`, `generate_inventory.py`, `generate_numeric_audit.py`, and `generate_numeric_retirements.py` |
| same | no current edge for `tools/standards_policy_impact/standards_policy_impact/compiler.py` | add missing consumer | replace private Graph Engine imports with root exports |
| same | no current edge for `tools/standards_verifier/standards_verifier/repository_graph.py` | add missing consumer | replace private Graph Engine manifest import with the root export |
| same | no current edge for `tools/standards_engine/standards_engine/tools.py` | add missing consumer | replace private contract-tool import with the Contracts public root |
| same | no current edge for the retiring Analysis serializer and old contract tools | retire/classify | record their retirement as closure of private cross-Module imports rather than silently excluding them from the final scan |
| `topic.contracts.generated-semantic-conformance` | no current edge for root-plus-private-child verification | add missing consumers | generated output and handwritten facade positive export fixture plus below-root and root-form private-child fixture families |
| `topic.contracts.generated-semantic-conformance` | no current edge for contract/public package documentation | add | contract package and Standards Engine public-facade documentation |
| same | no current edge for `tools/standards_engine/standards_engine/rendering.py` | add missing consumer | exhaustive generated v11 result rendering |
| `topic.contracts.identity-versus-instance-equality` | no current edge for identity package documentation | add | identity Interface documentation |
| same | no current edge for `tools/standards_metadata/standards_metadata/__init__.py` | add missing consumer | remove retired generic-serialization public exports |
| `topic.architecture.immutable-authority-closure` | no current edge for authority package documentation | add | capture, publication, recovery, and resolution Interface documentation |
| same | no current edge for `tools/standards_analysis/standards_analysis/__init__.py` | add missing consumer | remove retired snapshot/storage public exports |
| `topic.cross-platform.filesystem-paths` | no current policy unit or implementation edge | add | Cross-Platform sidecar; Authority repository/capture, README/package contract, required-real fixture, and suite |
| `topic.security.filesystem-containment` | no current policy unit or implementation edge | add | Security sidecar; descriptor-relative Authority repository/capture, containment/race fixture, and suite |
| Policy-unit registry | no Cross-Platform or Security source | update | Register both reviewed sidecars; unregistered sidecars are invalid and do not enter metadata or graph composition |
| Policy-impact registry | no Cross-Platform or Security declaration source | update | Register both source-owned relationship files; unregistered files do not enter relationship compilation or graph projection |

Every relationship not listed as replaced, corrected, retired, or split is
retained by the same natural key and must compile with identical semantics.
The final report records compiled old and new edge IDs; this plan does not
hardcode a mutable relationship count.

## Required Cutover Evidence

1. Compile accepted-base and proposed catalogs and relationship sets from their
   exact closed registries.
2. Require the admitted declaration-source additions and every expected natural
   key to appear in migration evidence. An otherwise-valid fixture omitting one
   admitted source must reach the exact migration-completeness diagnostic; the
   relationship compiler continues to compile only its registered input.
3. Record every removed, retained, added, or corrected node and edge by stable
   natural key; do not assert a fixed global count.
4. Run analysis from every changed policy-unit source and retain all traces.
5. Assign each selected consumer `updated`, `reviewed-no-change`,
   `not-applicable` with rationale, or `blocked`.
6. Require exact equality between selected consumers and disposition subjects.
7. Create the final owner-local Dependencies, Cross-Platform, and Security
   attestation source files and register each exact source in the closed
   attestation-source registry.
8. Freeze schema, interface contract, package manifests, lock, suites, catalog,
   relationships, horizon providers, canonical corpora, and attestation-source
   registrations.
9. Derive the final horizon and requirements from the frozen view.
10. Renew every stale authored attestation through the existing authorization
    and evidence path, then compile certificates.
11. Require exact equality between required and certified coverage subjects.

Any source registration or coverage-relevant authority change after step 8
invalidates the renewal and requires re-planning before new attestations are
authored.

Any blocked or unmapped consumer blocks A1b acceptance. An empty result is not
proof of no impact without valid independent coverage.
