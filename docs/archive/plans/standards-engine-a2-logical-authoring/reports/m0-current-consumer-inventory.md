# Milestone 0 Current Consumer And State Inventory

**Status:** `Accepted`

**Observed:** `2026-09-03`

**Repository baseline:** `fddcdeb36c3ce704948a880e97b6cabcf700f5e6`

## Result

The refreshed repository inventory found no independently deployed runtime
consumer, registered package entry point, or tracked retained database. The
only discovered callers of the A2 proposal contract are repository-owned
generated projections, examples, tests, and the fresh-process platform
harness. Coordinated replacement of the repository-shaped authoring contract
is therefore admitted; a compatibility reader, dual public shape, store
migration framework, or deprecation overlap is not.

This is a bounded current-tree result. External deployments and copied stores
cannot be discovered from this repository. Discovery of either is a re-plan
trigger, not a reason to add speculative compatibility machinery now.

## Runtime And Version Inventory

| Authority | Current value | Milestone disposition |
| --- | --- | --- |
| Public Standards Engine schema | interface `19` | Replace atomically with interface `20`; no v19 authoring overlap. |
| Analysis request | contract `4` | Preserve. Logical edits mechanically produce its existing change descriptors and semantic proposals. |
| Analysis state/result projection | contract `5` | Preserve. Coverage attestations and reviewer decisions remain Analysis-owned. |
| Public handle schema | `5` | Preserve. Add only the admitted opaque non-standard consumer handle. |
| Authoring revision aggregate | contract `1` | Replace with contract `2`, normalized logical change-set history, and a new revision identity domain. |
| Snapshot SQLite store | exact schema `2` | Preserve. Its generic immutable aggregate storage already carries the replacement material without a table/schema change. |
| Supported runtimes | Linux CPython `3.11` and `3.12` | Preserve and verify through fresh processes. |
| Application target | configured local `refs/heads/main` | Preserve; no remote operation or remote Adapter. |

An encountered v1 proposal aggregate after cutover is an unsupported retained
authoring format. It is not silently reinterpreted as logical intent. Snapshot,
Analysis, readiness, application, and recovery identities keep their existing
domains unless their owned material actually changes in a later milestone.

## Reachable Consumer Dispositions

| Population | Evidence in the current tree | Disposition |
| --- | --- | --- |
| Generated Python facade | `tools/standards_engine/standards_engine/_generated_contract.py` | Regenerate from interface v20. |
| Generated agent tools | `tools/standards_engine/contracts/generated/agent-tools.json` | Regenerate from the same schema and interface manifest. |
| Contract examples and documentation | `contracts/examples/a1-examples.json`, contract README, Engine README | Replace repository-shaped examples and explain logical authoring limits. |
| Tool dispatcher | `standards_engine/tools.py` | Preserve operation roots; decode the new create/revise payloads. |
| Authoring Module | `standards_engine/authoring.py` | Replace mutations with immutable normalized change-set history and proposal-head CAS over v2 identities. |
| Proposal projection and Analysis composition | `standards_engine/engine.py` | Compile logical history into the same A1c `CompiledSnapshot`; mechanically derive current Analysis inputs. |
| Behavioral tests and platform harness | `tools/standards_engine/tests` | Replace fixtures coherently and add logical lifecycle/negative/cold-reopen coverage. |
| Contract compiler consumer | `tools/standards_contracts` | Preserve compiler; regenerate and verify exact projections. |
| Analysis, identity, and metadata test consumers | repository-owned package tests | Update only affected coordinated fixtures; preserve their semantic contracts. |
| Snapshot persistence | `tools/standards_snapshots` exact schema v2 | Preserve unchanged. No second store or migration path. |
| Candidate Git publication | `tools/repository_git` | Preserve through Milestone 1; extend only in Milestone 2 for hidden add/replace/remove topology and proposal-specific commit material. |
| Complete verifier | `tools/standards_verifier` | Preserve as the application oracle; current candidate inputs are generated, not frozen in Engine behavior. |
| Historical A2 prototypes | tracked prototype artifacts | Preserve as history; never import or treat them as contract authority. |

## Standards Representation Dispositions

| Representation owner | Engine responsibility | Semantic authority retained by |
| --- | --- | --- |
| Canonical module Markdown and metadata envelope | Resolve placement, preserve or render authored body, and serialize the exact envelope. | Caller-supplied title, role, level, applicability, exclusions, verification, `Requires`, and `Specializes`; canonical metadata validation. |
| Canonical module corpus | Add/remove the derived owner path and order deterministically. | Canonical module ID and lifecycle intent supplied by the caller. |
| Policy-unit registry and owner sidecars | Add/remove sources, locate registered sections, update module/heading placement, lifecycle fields, and semantic revisions. | Explicit policy-unit IDs, placement anchors, semantic revisions, successors, rationale, and evidence. |
| Policy-impact and broader semantic declarations | Serialize explicit put/remove declarations into their existing owners and registry. | Caller-supplied relationship kind, endpoints, applicability, scope, evidence owner, and rationale; policy-impact compiler. |
| Non-standard relationship consumers | Resolve an opaque snapshot-bound consumer handle to the current catalog identity. | Existing policy-impact node catalog and caller selection; the Engine does not invent a consumer. |
| Coverage definitions | Derive requirements from the compiled logical candidate. | Existing coverage compiler. |
| Coverage attestations and authorization | Materialize accepted review state during application when current coverage authority requires it. | Existing `resolve`, authorization, and review contracts; never an authoring guess. |
| Standards graph and Router projection | Recompile from the candidate authorities; update generated projections only through their current generators. | Existing graph, metadata, policy-impact, Router, and generator owners. |
| Generated suite-input inventory | Refresh mechanically for exact changed candidate content. | Existing suite-input generator and complete verifier. |

## Persistence And Deployment Search Boundary

- `repository-entrypoints = []` remains true for the Standards Engine package.
- A tracked-file search found no `.sqlite`, `.sqlite3`, `.db`, or `.db3` file.
- A non-test current-tree search found no production construction or
  registration of `StandardsEngine` outside its package.
- The default `.standards-engine/snapshots-v1.sqlite3` location is an
  implementation default, not evidence that a retained store exists.
- User directories, unpublished packages, other machines, and external
  registries were intentionally not searched.

Every discovered consumer has an update, preserve, derive, reject, or later-
milestone disposition. There is no unresolved reachable consumer blocking
Milestone 1.
