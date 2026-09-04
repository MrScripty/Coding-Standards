# A1c Binding Assumptions Validation

**Status:** Complete design evidence

**Executable evidence:**
[`a1c-binding-assumptions-prototype.py`](a1c-binding-assumptions-prototype.py)

## Purpose

The binding A1c design depended on three mechanisms that the first aggregate
prototype had not exercised deeply enough:

1. traced roots-only capture without semantic inference in the capture layer;
2. transactional lifecycle of snapshots and multi-root analyses in SQLite; and
3. the complete eight-operation workflow across process and agent boundaries.

This report validates those mechanisms before production work. It does not
substitute representative models for production parity, generated-contract
validation, or required-real platform evidence.

## Result

| Assumption | Result | What is established | Remaining production gate |
| --- | --- | --- | --- |
| Traced roots-only capture | Confirmed with gate | Typed loaders can own references while a neutral content source records exact logical-path reads; replay from only those bytes detects missing, escaped, contradictory, and newly requested inputs. A new declared reference expands closure without capture-layer semantics. | Every production loader must accept the immutable source, and repository-source versus frozen-source compilation must produce equal requested paths and semantic outputs. |
| SQLite aggregate lifecycle | Confirmed with gate | Equal-content roots remain independent; one analysis may depend on several roots; quarantine makes dependent work unavailable; undelete restores it; purge removes every dependent analysis and child index transactionally; shared content remains until its last root is purged; interrupted purge rolls back; cold reopen reconstructs the aggregate. | The selected production schema and transaction implementation must pass failure injection and required-real Linux, Windows, and macOS evidence. |
| Eight-operation workflow | Confirmed with gate | The proposed methods support creation, discovery, navigation, immutable analysis transitions, inspection, quarantine, undelete, expiry, fresh-agent discovery, and coordinator-to-subagent handle transfer without caller-managed hashes, Git revisions, database paths, project labels, or child catalogs. | Generated v12 request and result types, public Adapter behavior, authorization, and exact typed failures must prove the same workflows. |

No binding assumption was contradicted. Production implementation remains
inactive until its milestone is explicitly started.

## Capture Boundary

The capture mechanism has no policy knowledge. It accepts normalized logical
paths, returns exact bytes, and records reads. Domain loaders remain the sole
owners of how manifests, registries, declarations, locators, and other typed
references expand.

The executable case begins from one declared root, follows loader-owned
references, freezes exactly the requested files, and runs the same compilation
again. It proves:

- unrelated available content is excluded;
- adding a typed reference automatically adds its target;
- absolute paths and parent traversal reject;
- a missing requested input rejects;
- contradictory bytes for one logical path reject; and
- a replay-time extra read rejects rather than falling back to ambient state.

The model deliberately does not infer that prose mentions another file. A
semantic reference becomes an authority dependency only when its owning loader
or contract declares that relationship.

## Production Loader Inventory

The current tree shows that closure expansion belongs to several typed owners,
not to one universal repository scanner:

| Root or owner | Current entry point | Dynamic expansion owned by the loader |
| --- | --- | --- |
| Canonical module corpus | `evaluation/standards-effectiveness/canonical-module-corpus.toml` | Manifest members and exact canonical module bytes |
| Policy-unit corpus | `evaluation/standards-effectiveness/policy-units/registry.toml` | Registered sidecars and each unit's owning canonical module locator |
| Router projection | `evaluation/standards-effectiveness/router-projection.toml` | One typed projection plus canonical module identity checks |
| Policy impact | `evaluation/standards-effectiveness/policy-impact-registry.toml` | Authoring contract, node and fact catalogs, suite registry, declaration sources, and suite paths selected by those declarations |
| Coverage horizon | `evaluation/standards-effectiveness/policy-coverage/horizons.toml` | Registered horizon providers, suite definitions, suite inputs, graph sources, and typed member fingerprints |
| Coverage authority | Attestation, authorization, and revocation registries | Registered attestations, evidence, issuer authority, and revocation inputs |
| Public contract | Canonical Engine schema and interface declaration | Reachable schema definitions, examples, and generated projections |

Milestone 5 must refactor these owners to one immutable content-source
Interface. Snapshot storage must not learn their semantics, and Engine capture
must not maintain a parallel list of files beyond the declared roots.

## Aggregate Lifecycle

The SQLite case uses normalized tables for content sets and files, independent
snapshot roots, immutable analysis states, a many-to-many snapshot dependency
table, derived child indexes, and minimal purged-root tombstones.

The important multi-root result is:

```text
snapshot A ---- analysis A
     |          analysis A+B
snapshot B ---- analysis B
```

Quarantining A makes analysis A and analysis A+B unavailable while analysis B
continues to work. Undeleting A restores both unavailable analyses. Purging A
deletes analysis A and analysis A+B, including their child indexes, but leaves
B and its shared content available. Purging B then releases the final content
and analysis rows. An injected interruption after root deletion rolls back the
root, dependent records, and tombstone together.

The prototype also rejects a generated root-ID collision. It does not silently
alias the new root to equal content or retry under an unrecorded identity.

## Agent Workflows

The complete disposable flow exercises:

1. `create_snapshot` twice over equal content;
2. keyset-paginated `find_snapshots`;
3. `query` against a retained root;
4. `prepare` returning an immutable analysis handle and current work;
5. process close and reopen;
6. `inspect` of the analysis and advertised requirement;
7. `resolve` by a later agent invocation without replaying preparation;
8. `delete_snapshot`, typed quarantine refusal, `undelete_snapshot`, and
   restored use; and
9. typed expiry after the configured quarantine period.

The public prototype projections mechanically reject unknown fields and omit
internal content identity, repository revision selection, store location,
project labels, and child catalogs. These shape checks are design evidence,
not a replacement for compiling and validating the canonical v12 schema.

## Limits And Implementation Requirements

- The representative loader proves the content-source protocol, not parity for
  every current production loader. Production parity remains an atomic-cutover
  acceptance requirement.
- Local SQLite proves relational ownership and transaction behavior, not real
  filesystem locking or movement on every supported platform.
- Prototype dictionaries prove workflow sufficiency, not generated contract
  closure or JSON Schema conformance.
- Authorization and deterministic evidence providers remain production
  boundaries. The experiment does not relax or reproduce their semantics.
- Cross-engine stored-state compatibility remains deferred. Cold reopen means
  the same current semantic contracts in a fresh process.

## Decision

Retain the A1c ADR without changing its selected owners or dependency
direction. The three assumptions are sufficiently validated to permit a later
explicit start of the Repository Git and Snapshot foundation. Preserve the
production gates above; failing any of them is a re-plan trigger rather than a
reason to add fallback loading, ambient state, or compatibility machinery.
