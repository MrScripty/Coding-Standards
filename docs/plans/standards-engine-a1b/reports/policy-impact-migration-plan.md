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
and renew mechanically stale coverage.

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
| `tools/standards_authority/pyproject.toml` | Add as the identity-backed authority package contract |
| `tools/standards_authority/standards_authority/__init__.py` | Add as the narrow capture/storage public Interface |
| `tools/standards_authority/README.md` | Add as the capture, storage, publication, and recovery Interface guide |
| `evaluation/standards-effectiveness/policy-units/cross-platform.toml` | Add one reviewed revision-1 unit for the exact `Filesystem Paths` heading |
| `evaluation/standards-effectiveness/policy-impact/topic.cross-platform.toml` | Add source-owned Cross-Platform implementation, package, fixture, and suite relationships |
| `evaluation/standards-effectiveness/policy-units/security.toml` | Add one reviewed revision-1 unit for the exact `Filesystem Containment` heading |
| `evaluation/standards-effectiveness/policy-impact/topic.security.toml` | Add source-owned descriptor-relative containment implementation, fixture, and suite relationships |
| `evaluation/standards-effectiveness/policy-units/registry.toml` | Retain and register the new Cross-Platform and Security sidecars in the canonical policy-unit corpus |
| `tools/standards_engine/README.md` | Retain and update the public v11 facade and unsupported-version behavior |
| `tools/standards_engine/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13` and declare every directly imported internal package, including Contracts and Authority |
| `tools/standards_applicability/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; remain stdlib-only |
| `tools/standards_metadata/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare Identity directly |
| `tools/graph_engine/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; remain stdlib-only |
| `tools/standards_policy_impact/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare Graph Engine, Applicability, and Metadata directly |
| `tools/standards_graph/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare Graph Engine, Metadata, and Policy Impact directly |
| `tools/standards_analysis/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare Graph Engine, Applicability, Identity, Metadata, and Policy Impact directly |
| `tools/standards_verifier/pyproject.toml` | Retain; restrict A1b to `>=3.11,<3.13`; declare every directly imported Engine Module, including Contracts |
| `docs/plans/standards-engine-a1b/reports/dependency-and-dialect-decision.md` | Retain as the reviewed selection authority |
| `docs/plans/standards-engine-a1b/reports/a1b-dependency-provenance.md` | Add as exact implementation resolution evidence |
| `tools/standards_engine/contracts/generate_contract.py` | Retire; replace with `tools/standards_contracts/standards_contracts/projection.py` |
| `tools/standards_engine/contracts/validate_contracts.py` | Retire; replace with `tools/standards_contracts/standards_contracts/compiler.py` |
| `tools/standards_engine/standards_engine/_generated_contract.py` | Retain and regenerate |
| `tools/standards_engine/standards_engine/__init__.py` | Retain and update |
| `tools/standards_engine/standards_engine/tools.py` | Retain and update |
| `tools/standards_engine/standards_engine/engine.py` | Retain and update |
| `tools/standards_engine/standards_engine/rendering.py` | Retain; render the exhaustive generated v11 result algebra, including `FactRequirementWork` |
| `tools/standards_engine/standards_engine/model.py` | Retire; it is only a compatibility re-export over the generated algebra |
| `tools/standards_metadata/standards_metadata/serialization.py` | Retire; replace with `tools/standards_identity/standards_identity/encoding.py` |
| `tools/standards_metadata/standards_metadata/__init__.py` | Retain; remove retired serialization exports and export only Metadata-owned contracts |
| `tools/standards_analysis/standards_analysis/snapshots.py` | Retire; replace capture with `tools/standards_authority/standards_authority/capture.py` and storage with `repository.py` |
| `tools/standards_analysis/standards_analysis/__init__.py` | Retain; remove retired serializer/snapshot exports and expose only Analysis-owned types and transitions |
| `tools/standards_analysis/standards_analysis/resolution.py` | Retain pure analysis transition behavior and update dependencies |
| `tools/standards_analysis/standards_analysis/results.py` | Retain pure domain projection and update dependencies |
| none | Add `tools/standards_contracts/standards_contracts/compiler.py` |
| none | Add `tools/standards_contracts/standards_contracts/projection.py` |
| none | Add `tools/standards_identity/standards_identity/encoding.py` |
| none | Add `tools/standards_authority/standards_authority/repository.py` |
| none | Add `tools/standards_authority/standards_authority/capture.py` |

The listed Engine Module manifests form one exact source-tree dependency
closure. They are not independently published artifacts in A1b, so the plan
does not invent a wheel-build backend or claim a local distribution-install
contract. `standards_identity`, `standards_applicability`, and Graph Engine are
stdlib-only. `standards_contracts` declares exact direct external requirements
for `jsonschema` and `referencing`; its lock closes transitives.
`standards_authority` declares Identity. Every other manifest declares exactly
the internal packages imported directly by its production source: no missing
direct requirement, transitive satisfaction, or unused internal requirement is
accepted. Every listed manifest uses `requires-python = ">=3.11,<3.13"`.

Milestone 3 derives the direct-import graph from production Python syntax and
compares it with the manifest graph. It then creates a clean CPython 3.11 and
3.12 environment, installs the exact external lock, changes to a directory
outside the repository, supplies the reviewed checkout root as the sole
`PYTHONPATH`, enables Python safe-path mode, and imports every public Module
entry point in one fresh process. This is the reproducible execution contract
the repository actually uses. A newly required local wheel, independently
published distribution, build backend, or import outside this graph is a
re-plan trigger.

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
relationship selects their semantics. Test files remain suite inputs rather
than individually authored relationship authority unless the final horizon
audit proves a missing semantic consumer.

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
| `topic.architecture.immutable-authority-closure` | Retain engine, analysis transition/result, fixture, suite, and Persistence; replace snapshot compiler | Add authority envelope/repository and direct-object cold-reconstruction suite |
| `topic.dependencies.implementation-versus-dependency` | Retain Router, profile, prompts, fixture, and suite | Add contract package manifest, exact lock, compiler, and dependency provenance report |
| `profile.boundary.generated-contract.semantic-closure` | Retain Contracts, Verification, Build, Dependencies, schema, generated algebra, tool adapter, fixture, and suite; replace generator | Add interface contract, compiler, and projection; projection replaces the generator edge |
| `topic.cross-platform.filesystem-paths` | New projection of existing `topics/cross-platform.md` `Filesystem Paths` heading at semantic revision 1 | Add Authority repository/capture, its required-real suite, and the Cross-Platform package/README projection |
| `topic.security.filesystem-containment` | New projection of existing `topics/security.md` `Filesystem Containment` heading at semantic revision 1 | Add descriptor-relative Authority repository/capture and its containment/race suite |

`standards_engine/rendering.py` follows generated-semantic-conformance and the
Generated Contract profile because it must exhaustively project the public
result algebra. The Metadata and Analysis package initializers follow
identity-versus-instance-equality and immutable-authority-closure respectively
because their public exports must remove the retired serializer and snapshot
authorities.

Relationship declarations remain source-owned in their current module files.
No generic graph manifest or path inference creates these replacements.

The two new policy units do not change normative prose. Their revision 1 is a
reviewed bootstrap assertion that the exact canonical module, locator, resolved
content/structure, and initial implementation relationships represent the
already accepted meaning. Each locator must resolve exactly once and its module
must own its declaration. Planning admission reviews the identity/locator;
final A1b coverage independently audits the frozen relationship and horizon
state before attestation.

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
| `profile.boundary.generated-contract.semantic-closure` | `tools/standards_engine/contracts/generate_contract.py` | replace/split | interface contract, contract compiler, and projection compiler |
| same | no current edge for `contracts/generated/agent-tools.json` | add missing consumer | generated agent-tool projection |
| same | no current edge for `contracts/examples/a1-examples.json` | add missing consumer | public serialized example corpus |
| `topic.contracts.identity-versus-instance-equality` | no current edge for `contracts/identity-fixtures.json` | add missing consumer | identity v2 and domain-version fixture authority |
| `topic.dependencies.implementation-versus-dependency` | no current implementation edge | add/split | contract package manifest, exact lock, compiler, dependency decision, and implementation provenance report |
| same | no current edge for the new Identity and Authority package manifests | add missing consumers | exact stdlib-only Identity and identity-backed Authority package contracts |
| `topic.contracts.generated-semantic-conformance` | no current edge for contract/public package documentation | add | contract package and Standards Engine public-facade documentation |
| same | no current edge for `tools/standards_engine/standards_engine/rendering.py` | add missing consumer | exhaustive generated v11 result rendering |
| `topic.contracts.identity-versus-instance-equality` | no current edge for identity package documentation | add | identity Interface documentation |
| same | no current edge for `tools/standards_metadata/standards_metadata/__init__.py` | add missing consumer | remove retired generic-serialization public exports |
| `topic.architecture.immutable-authority-closure` | no current edge for authority package documentation | add | capture, publication, recovery, and resolution Interface documentation |
| same | no current edge for `tools/standards_analysis/standards_analysis/__init__.py` | add missing consumer | remove retired snapshot/storage public exports |
| `topic.cross-platform.filesystem-paths` | no current policy unit or implementation edge | add | Cross-Platform sidecar; Authority repository/capture, README/package contract, required-real fixture, and suite |
| `topic.security.filesystem-containment` | no current policy unit or implementation edge | add | Security sidecar; descriptor-relative Authority repository/capture, containment/race fixture, and suite |
| Policy-unit registry | no Cross-Platform or Security source | update | Register both reviewed sidecars; unregistered sidecars are invalid and do not enter metadata or graph composition |

Every relationship not listed as replaced, corrected, retired, or split is
retained by the same natural key and must compile with identical semantics.
The final report records compiled old and new edge IDs; this plan does not
hardcode a mutable relationship count.

## Required Cutover Evidence

1. Compile accepted-base and proposed catalogs and relationship sets.
2. Record every removed, retained, added, or corrected node and edge by stable
   natural key; do not assert a fixed global count.
3. Run analysis from every changed policy-unit source and retain all traces.
4. Assign each selected consumer `updated`, `reviewed-no-change`,
   `not-applicable` with rationale, or `blocked`.
5. Require exact equality between selected consumers and disposition subjects.
6. Freeze schema, interface contract, package manifests, lock, suites, catalog,
   and relationships.
7. Derive the final horizon and requirements from the frozen view.
8. Renew every stale authored attestation through the existing authorization
   and evidence path, then compile certificates.
9. Require exact equality between required and certified coverage subjects.

Any blocked or unmapped consumer blocks A1b acceptance. An empty result is not
proof of no impact without valid independent coverage.
