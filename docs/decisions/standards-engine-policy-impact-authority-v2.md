# Standards Engine Policy-Impact Authority V2

**Status:** Accepted

This decision supersedes only the policy-impact ownership,
relationship-kind version 1, public repository-declaration exposure, compiled
semantic inspection, and associated version clauses in
[Standards Engine Navigation And Analysis](standards-engine-navigation-analysis.md).
This decision did not replace the remaining A1 architecture at that time.
Later [A1b](standards-engine-a1b.md) and [A1c](standards-engine-a1c.md)
decisions supersede the architecture scopes they identify. The version 9
acceptance remains historical evidence; see the [decision index](README.md).

The Standards Engine will replace the split policy-impact catalog, relationship,
verification, coverage, and public-schema interpretations with one compiled
authority owned by `standards_policy_impact`. The Module will load one versioned
internal authoring contract, the registered supplemental artifact catalog, the
fact catalog, and source-owned relationship declarations; validate artifact
kinds and relation/target compatibility; and emit one immutable projection
containing graph nodes, groups, edges, executable policy semantics, provenance,
and coverage fingerprints. This decision is a recovery-enabling replacement of
the policy-impact portions of the accepted A1 design, not the broader A1b
contract-compiler, equality, or immutable-storage redesign.

## Context

The accepted A1 boundary currently assigns parts of one invariant to four
places. `standards_policy_impact` owns relationship-kind behavior but accepts
any canonical target. `standards_graph` separately loads supplemental catalog
nodes and groups. `standards_verifier` infers relation compatibility from
repository paths. `standards_analysis` reparses the raw catalog to derive
coverage. The public A1 schema additionally exposes repository declaration and
compiler-internal semantic shapes even though no public operation accepts those
authoring values.

This duplication first appeared as a Router projection verifier failure. The
same audit then found implementation artifacts labeled as references. A local
verifier dispatch would preserve the duplicated authority and allow the same
class of defect to recur.

## Decision

### One Internal Authority

`standards_policy_impact` owns:

- internal authoring-contract, catalog, relationship-kind, and provider
  versions;
- the closed supplemental `artifact_kind` vocabulary;
- relationship kinds, graph groups, propagation, traversal, evidence
  requirements, and allowed target kinds;
- catalog, declaration, source-owner, evidence-owner, and relation/target
  validation;
- graph-node, graph-group, graph-edge, semantic, provenance, and coverage
  projections; and
- typed policy-impact diagnostics.

The internal serialized contract is
`tools/standards_policy_impact/contracts/policy-impact-authoring-v2.toml`.
Repository TOML files remain authored authority. Every registered relationship
declaration source uses source schema version 2 after the atomic cutover; all
eight current sources migrate together, including sources whose relationship
content does not otherwise change. Source schema version 1 is rejected and no
compatibility loader remains. No caller parses declarations after compilation.
Canonical module and policy-unit identity remains owned by `standards_metadata`;
generic graph storage and traversal remains owned by `graph_engine`.

Every supplemental catalog node has one explicit `artifact_kind`. Version 2
admits `documentation`, `enforcement-suite`, `fixture`,
`implementation-artifact`, `prompt`, `routing-projection`, and `template`.
The existing `authority` value remains a separate reading/evidence role and is
not an artifact classifier. Canonical modules use their metadata-owned role
rather than duplicate catalog entries.

Version 2 adds `implementation-projection`. Its targets must be supplemental
`implementation-artifact` nodes. `reference-projection` targets canonical
reference modules. The other relations use exact module roles or exact
supplemental artifact kinds declared by the internal contract. Repository paths
are content locations, never classification authority.

The version 2 compatibility matrix is:

| Relationship kind | Admitted target class |
| --- | --- |
| `normative-consumer` | Canonical non-reference module |
| `router-projection` | Canonical module with role `router`, or supplemental `routing-projection` |
| `prompt-projection` | Supplemental `prompt` |
| `template-projection` | Supplemental `template` |
| `reference-projection` | Canonical module with role `reference` |
| `documentation-projection` | Supplemental `documentation` |
| `fixture-projection` | Supplemental `fixture` |
| `enforcement-suite-projection` | Supplemental `enforcement-suite` with one registered suite ID |
| `implementation-projection` | Supplemental `implementation-artifact` |

An alias resolves to its canonical node before compatibility is checked, but
authored relationship sources and consumers remain canonical IDs. Unknown,
retired, aliased-as-canonical, multiply classified, or incompatible targets are
typed compiler failures.

The compiler's `GraphContribution` contains the supplemental nodes and groups
as well as policy-impact edges. `standards_graph`, `standards_analysis`, and
`standards_verifier` consume only the compiled result. The separate catalog
graph source, verifier path dispatch, and analysis raw-catalog parser are
removed in the coordinated cutover.

### Public Contract

Public A1 version 10 contains only definitions reachable from `query`,
`prepare`, `resolve`, and `inspect`. It removes `PolicyImpactDeclaration` from
the public root and replaces `CompiledPolicyImpactSemantics` in relationship
inspection with `PolicyRelationshipInspection`, an operation-shaped value
containing source and consumer scopes, normalized applicability, evidence
owner, rationale, propagation, and relationship kind. Repository declaration
paths, compiled-program internals, and dependency fingerprints remain internal.

Interface/schema version advances from 9 to 10, result projection from 1 to 2,
snapshot/navigation/analysis handle schemas and identity domains from 2 to 3,
and analysis contract/schema from 5/2 to 6/3. Coverage view, requirement,
attestation, and certificate contracts and identity domains advance from 1 to
2. The policy-impact internal authoring contract, declaration source schema,
catalog, relationship-kind, and provider contracts advance from 1 to 2; the
independent coverage-horizon provider advances from 2 to 3. Graph-engine,
applicability-language, metadata, evidence, and authorization contracts do not
change.

The policy-impact edge identity algorithm remains version 1. Reclassified
relationships receive new IDs because relation is part of the natural key;
retained relationships retain their IDs. Version 9 handles and persisted
states are reported as unsupported under version 10. No repository-owned or
supported external persisted production state exists to migrate, so no
compatibility loader or offline converter is introduced.

## Considered Options

- A Router-only verifier correction was rejected because it fixes one target
  while retaining three competing compatibility authorities.
- Adding `implementation-projection` only to A1 v9 was rejected because it
  preserves public/internal enum duplication and violates the accepted public
  version-migration rule.
- Broadening `reference-projection` was rejected because references and
  implementations have different meanings and consumers.
- Performing all A1b redesign work now was rejected because equality,
  general contract compilation, and immutable authority storage are independent
  changes not required to restore this invariant.

## Consequences

All active policy units are certified once after the provider, catalog,
declarations, public contract, suite registry, and horizon are frozen.
Canonical metadata owns current subject membership; coverage compilation owns
current requirements. Every current requirement uses the same attestation,
evidence, authorization, identity, validation, and certificate path. Version 2
introduces no renewal or initial-establishment semantic category.

For migration audit only, a generated transition projection joins the current
subject set to certificates compiled from exact predecessor commit
`4baa63118a72fd0c185fc1d950dc149ab0c1808c`, tree
`5a4d6d6786fa7a6ca8b373ca221a8eb1c90fa995`. Predecessor presence cannot
change certification behavior or identity. Exact active-unit, requirement,
attestation, and certificate subject sets must be equal at acceptance.
Future internal relationship kinds do not require a public contract migration
unless an operation-shaped public result itself changes. A2 remains inactive,
and historical A1 version 9 acceptance remains unchanged as historical
evidence.
