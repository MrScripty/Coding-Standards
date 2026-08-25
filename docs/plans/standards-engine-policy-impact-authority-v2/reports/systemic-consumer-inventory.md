# Systemic Consumer Inventory

## Boundary

- Inventory base: commit `cb6abdb89afaa4fca25706cd42f621a8c762480f`,
  tree `24328086a11f9370a615ff62254de9aa1d825931`.
- Invariant: one owner decides supplemental artifact classification,
  relationship-kind semantics, target compatibility, graph projection,
  policy semantics, provenance, and coverage fingerprints.

## Consumers And Dispositions

| Consumer | Current dependency | Required disposition |
| --- | --- | --- |
| `standards_policy_impact.compiler` | Hardcoded kind table plus generic manifest parser | Replace with the v2 internal contract and one compiled authority. |
| `standards_policy_impact.model` | Edge-only graph contribution and raw catalog path | Replace with immutable typed catalog and complete graph/semantic/coverage projections. |
| Policy-impact registry, catalog, and declarations | Version 1 files; untyped supplemental nodes; implementation edges labeled as references | Migrate the registry, catalog, and all eight declaration sources atomically to v2; apply the exact admitted relation mapping to the three affected sources and schema-only migration to the other five. |
| Edge-source registry | Registers the catalog and relationship provider separately | Remove the catalog source; retain one policy-impact provider registration. |
| `standards_graph.repository` | Reconstructs a `ManifestSource` for the catalog | Consume only the compiled provider contribution. |
| `standards_verifier.policy_impact` | Switches on relation and repository path shape | Consume compiler validity and report typed compiler diagnostics; retain only specialized content checks selected by artifact kind. |
| `standards_verifier.repository_graph` | Composes catalog and edge sources separately | Consume the one compiled contribution. |
| `standards_analysis.coverage` | Reparses the catalog and creates its own projection | Consume compiler-provided discovery fingerprints and the versioned horizon adapter. |
| A1 canonical schema | Exposes repository declaration and compiler-internal semantic types | Replace with v10 operation closure and `PolicyRelationshipInspection`. |
| Contract generator and generated Python/tool projections | Reproduce the v9 public/internal coupling | Regenerate from v10 and prove complete reachable closure. |
| Standards Engine facade, inspection, and rendering | Serializes compiled semantic internals | Adapt compiled authority to the operation-shaped public result. |
| Snapshot and analysis reconstruction | Accepts v2 handles/state and v9 interface versions | Replace with v3 handle/state identities and explicit predecessor unsupported outcomes. |
| Policy-impact, graph, analysis, verifier, and engine tests | Test split loaders or public internal shapes | Replace with Interface-level compatibility, identity-set, closure, unsupported-version, and cold-process evidence. |
| Coverage horizon and attestations | Bind provider/kind/catalog/horizon predecessor contracts; one active Verification unit has no predecessor certificate | Advance the horizon, renew predecessor coverage, establish initial coverage for the uncovered unit, and prove exact active-unit/requirement/certificate equality after freeze. |
| Package documentation | Describes predecessor composition or public shapes | Update to the accepted v2/v10 Interface and ownership. |
| Historical A1 v9 plan and acceptance evidence | Records the accepted predecessor | Retain unchanged as historical evidence. |

No normative standards document, policy-unit identity, locator, or semantic
revision changes in this prerequisite. Three relationship declaration sources
change target relation classification; all eight registered sources migrate to
source schema version 2. Provider-wide identity changes require the renewal or
initial-coverage disposition recorded for every active policy unit in
[coverage-subject-inventory.tsv](coverage-subject-inventory.tsv).
