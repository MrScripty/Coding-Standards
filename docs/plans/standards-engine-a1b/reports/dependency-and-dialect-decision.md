# A1b Dependency And Dialect Decision

**Status:** Proposed planning evidence

**Planning base:** commit `c4408363752b10060f631247f3e2f1fa26eae003`,
tree `84477150bd368a168dd04da3770de55c23bbb817`

## Requirement

A1b needs one executable owner for the standard behavior used by its canonical
contract. The owner must:

- implement JSON Schema Draft 2020-12 instance semantics;
- support the A1b keyword and local-reference profile;
- expose deterministic validation results that can be adapted to stable project
  diagnostics;
- run on the repository's supported Python 3.11-or-newer environments;
- have maintained conformance evidence against the official test suite;
- permit use and distribution under terms compatible with this repository;
- avoid runtime network retrieval; and
- let generated models remain representations rather than validators.

## Candidate Comparison

| Candidate | Semantic coverage | Independent evidence | Maintenance owner | Result |
| --- | --- | --- | --- | --- |
| Current local validator plus generated decoder | Limited maintained subset with two local interpreters | Local differential tests only; known Draft disagreement | Repository owns standardized semantics indefinitely | Rejected |
| Code-first Python model library | Strong Python modeling, but JSON Schema remains a required external representation | Library-specific evidence; schema projection remains | Repository still owns authority reconciliation | Rejected |
| Direct scattered `jsonschema` calls | Mature Draft implementation | Official-suite-backed dependency | Profile, references, and diagnostics duplicated across callers | Rejected |
| `standards_contracts` over `jsonschema` and `referencing` | Mature Draft implementation behind one narrow project Interface | Dependency suite plus exact official external corpus and local profile tests | Dependency owns Draft semantics; repository owns profile and projections | Selected |

## Selected Dependency

Select `jsonschema` version `4.26.0`. Its public
`Draft202012Validator` owns standard keyword semantics. Declare `referencing`
directly because `standards_contracts` uses its immutable registry Interface.
Do not override validator keywords, type checking, or equality.

The implementation slice must create one exact, hash-checked resolution for the
supported verification environments. The lock records the selected versions of
the complete transitive closure, including `attrs`,
`jsonschema-specifications`, `referencing`, and `rpds-py`. Package manifests own
their direct requirements; the lock owns the exact accepted verification
resolution. Ambient installations are not satisfaction evidence.

`rpds-py` includes native distributions and may require a Rust toolchain when a
matching wheel is unavailable. The dependency-resolution milestone must prove
the supported Python 3.11 and 3.12 Linux environments can consume the exact
resolution. A missing compatible artifact is a re-plan trigger, not authority
to use an unlocked alternate version.

## Dialect Profile

The canonical document continues to declare Draft 2020-12. A1b admits the
keywords reachable from public operations after audit. The current candidate
surface is:

```text
$schema, $id, $ref, $defs,
title, description, default,
type, const, enum, oneOf,
required, properties, additionalProperties,
items, minItems, uniqueItems,
minLength, pattern, minimum
```

The audit must classify every `x-standards-engine-*` annotation as one of:

- closed executable contract metadata with a named owner;
- non-semantic documentation removed from the machine schema; or
- unsupported and blocking.

Only same-resource references are admitted. Remote retrieval, format assertion,
custom vocabularies, validator extension, and silent unknown-keyword handling
are excluded. A newly required feature triggers re-planning.

## External Conformance

Independent acceptance uses the official JSON Schema Test Suite at exact commit
`3c25e5f709192aadf67cf7f2eb19771a57131fec`. It is fetched into temporary
storage and is not copied into repository history. The applicable Draft 2020-12
cases run through the same `standards_contracts` validator adapter used by the
public contract compiler.

This evidence is distinct from:

- deterministic generation freshness;
- local schema/model agreement;
- A1b profile and extension tests;
- public facade behavior; and
- identity serialization fixtures.

If the exact corpus or its authoritative source cannot be obtained, the
external-conformance claim is blocked. No bundled substitute or local copied
expectation is accepted.

## Licensing And Provenance

Authoritative package metadata and upstream license files identify the selected
stack as MIT-licensed. A1b consumes installed packages and records exact package
identities; it does not copy package source, wheels, or the external test corpus
into this repository.

The implementation must record:

- exact package names, versions, source locations, hashes, and license
  authorities;
- the repository's use of each direct and transitive package;
- whether any produced distribution bundles third-party code; and
- every resulting notice or attribution placement.

For the currently selected source-only repository and dependency declaration,
no third-party binary or source is redistributed by the repository itself.
Installed package distributions retain their own license metadata. If a future
artifact bundles the packages, wheels, source, or corpus, Licensing and Release
must re-evaluate notice and license-text obligations before publication.

## Security And Updates

The exact resolution is scanned using the accepted dependency-audit procedure.
Security findings remain owned by Security; version selection and lifecycle
consequences remain owned by Dependencies. Updating any selected package
requires rerunning profile conformance, public contract integration, supported
target resolution, provenance, license, and vulnerability evidence.

## Sources

- [`jsonschema` project and supported drafts](https://github.com/python-jsonschema/jsonschema)
- [`jsonschema` 4.26.0 project metadata](https://raw.githubusercontent.com/python-jsonschema/jsonschema/v4.26.0/pyproject.toml)
- [`jsonschema` license](https://raw.githubusercontent.com/python-jsonschema/jsonschema/v4.26.0/COPYING)
- [Official JSON Schema Test Suite](https://github.com/json-schema-org/JSON-Schema-Test-Suite)

## Decision

The dependency-backed contract compiler is selected. Implementation remains
unavailable until the A1b plan and ADR receive independent exact-tree
admission.

