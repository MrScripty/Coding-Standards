# Typed routing-edit pilot

**Plan status:** Verifying
**Acceptance status:** pending
**Admission:** `start`, user-authorized implementation of the typed routing-edit pilot.
**Base:** `cbf9cdd2d7627d2c45f0001486a8872ab6b5206d`, interface 44.
**Current phase:** T1 implemented and locally verified; external acceptance pending.
**Next slice:** T2 — exact-diff supported-runtime CI and independent review.

## Outcome and boundaries

Replace JSON-backed logical edits only for put/remove routing facts and rules with
explicit immutable authored values and edit variants. Remove repeated JSON parsing
and stored redundant kind/target/facet fields in this family. Preserve exact public
and persisted representations, normalization order, identities, facet collisions,
atomic rule/fact changes, generated TOML/Markdown, semantics and failure timing.
There is no new API, migration, expression evaluator or compatibility path. Other
StructuredEdit families and the already integrated capture/reuse work stay unchanged.

The latest main/source tree and artifact are verified. The executable Router
selected 24 applicable modules with no unanswered conditions. Core, Implementation,
Verification, Planning, Documentation, Build, Development Proportionality, library,
generated-contract/IPC/persistence profiles, architecture/replay, contracts/schema/
protocol/evolution, security, diagnostics, code design and performance guide the
slice. Work is restricted to a clean task-owned checkout and disposable test stores.
The user's actual repository, unrelated ZIP changes, host configuration and remote
refs are not write targets.

## Binding design and composed review

1. The existing logical parser owns request-to-edit construction and facet conflict
   checks. Four explicit edit classes derive kind/target/facet from their selected
   fact or rule; callers cannot separately set contradictory discriminator fields.
   Immutable authored declarations retain exact values and array order. They are
   not compiled FactContracts or bound applicability programs.
2. Preserve current shape checks and their AuthoringError meanings. Compound
   declaration values are captured structurally, with no normalize/evaluate pass.
   The applicability owner still validates a fact domain and expression against
   the final co-edited context. Unknown references, revision changes, conflicting
   targets and dependent removals fail in the same projection stage as before.
3. A small routing-family value module owns immutable declaration storage and
   serialization. The existing logical-authoring module retains its parser checks,
   so the value module never imports the compiler or its validation helpers. It interprets no expression operator, fact type or semantics.
   Existing parser checks are reused at the same boundary; the existing routing
   projection owns file edits and the existing compiler owns semantic validation.
   No shared general-purpose freeze framework, second grammar or new package API
   is introduced for this pilot.
4. Use typed variants for routing collection, routing staging and module attribution.
   Non-routing edits keep their current behavior; their broad conversion redesign
   is not admitted. Canonical JSON remains necessary at actual identity/persistence
   and deterministic order boundaries, not as the in-memory routing-edit payload.
5. Exact sorted map order must match the old canonical-JSON round trip, including
   nested expressions. Authored arrays and numbers remain as supplied; semantic
   normalization belongs to the applicability compiler. Returned dictionaries are
   fresh and cannot mutate retained authored values. Any additional failure-stage
   change discovered during differential tests triggers repair or a scoped re-plan.
6. Meaningful verification compares both exact representations and independent
   semantic outcomes: original baseline producer, fresh candidate consumer, logical
   projection files, conflicts, identities, selected contexts and cold readback.
   Count JSON decodes separately from whole-operation latency/memory; do not promise
   overall speed improvements based only on an inner-operation microbenchmark.
7. Existing schemas, catalog variants, interface 44, stored versions, compilation
   identity/resource policy, evidence and publication semantics remain unchanged.
   A process restart loads new implementation code; no setting/store reset is needed.

## Write set and acceptance

Production: `tools/standards_engine/standards_engine/logical_authoring.py` and the
new routing-family value module. Add directly required consumers only when their
current decoding assumptions are demonstrated, keeping this contract/scope intact.
Tests: focused typed-routing unit/differential tests, logical workflow replay and
real-stdio coverage; necessary old test expectations remain at their owners.
Maintenance: Engine README, plans index, this plan/ledger/issues/report, a scoped
link in the prior refinement plan, and the generated suite-input manifest.
Normative standards, public schemas, generators, dependency pins, database formats
and user/operator resources are excluded.

- A1: the four edits use immutable explicit variants with derived facets/kinds;
  source and returned nested value mutation cannot change the stored edit.
- A2: baseline/candidate normalization, serialized payloads, IDs, order and facet
  conflicts match. Reads of baseline-produced revisions require no migration.
- A3: routing semantics are evaluated at the existing stages; invalid revision,
  fact/expression/reference/target and dependent-removal cases preserve outcomes.
- A4: mixed/same-set edits and incremental replay preserve exact projected files,
  impacted modules, review/readiness, evidence and no-publication constraints.
- A5: measured routing-edit JSON decodes disappear. All existing schemas/catalogs,
  state formats, resource lifetimes and non-routing representations are preserved.
- A6: focused/affected tests, static and generated checks, structural verification
  and exact patch reconstruction pass. Supported-runtime CI and independent review
  are separately required for Accepted status when unavailable locally.

T1 implements and tests the pilot. T2 integrates the exact candidate with locked CI
and independent review. Expand to another edit family only after this pilot's
representation and maintenance benefits are reviewed; expansion is not part of T1.

## Implementation disposition

T1 is Implemented. A1–A5 have local representative and differential evidence;
A6 has local test/static/packaging evidence with supported-runtime CI and independent
review remaining required. See [verification](reports/verification.md) for exact
counts, the stopped initial campaign, final-source boundary and limitations. No
claim of acceptance, whole-operation speedup or actual model qualification is made.
T2 is the only next slice; another edit-family conversion requires new admission.
