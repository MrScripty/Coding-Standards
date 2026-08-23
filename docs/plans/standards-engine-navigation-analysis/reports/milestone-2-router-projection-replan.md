# Milestone 2 Router Projection Replan

## Trigger

The accepted Router expresses general applicability through human-readable
condition tables. Existing executable fixtures cover verifier-change and
language-profile scenarios but do not form a complete general route provider.
Python cannot deterministically derive typed applicability expressions from
those English conditions. Hardcoding equivalent decisions in the engine would
create a second routing authority.

## Impact Review

The accepted generic graph query for both `router` and
`STANDARDS-ROUTER.md` returned the same incident set: its `core` requirement
and incoming Planning and Commit projections. Router is not marked globally
audited, so an empty outgoing policy-impact result was not treated as proof of
no consumers.

A bounded manual review covered the current entrypoints and executable routing
surfaces relevant to this projection:

| Consumer | Disposition | Reason |
| --- | --- | --- |
| `STANDARDS-ROUTER.md` | `reviewed-no-change` | Normative routing meaning remains unchanged. |
| `README.md` | `reviewed-no-change` | It delegates applicability to Router and contains no executable rules. |
| `prompts/planning.md` | `reviewed-no-change` | It delegates to Router without copying route conditions. |
| `prompts/implement-plan.md` | `reviewed-no-change` | It delegates to Router and retains its conditional profile wording. |
| `prompts/full-codebase-standards-refactor.md` | `reviewed-no-change` | It delegates to Router without defining selection semantics. |
| `evaluation/standards-effectiveness/fixtures/routing/verifier-change-decisions.tsv` | `reviewed-no-change` | Its current cases become executable equivalence evidence for the registered projection without changing their authority. |
| `evaluation/standards-effectiveness/fixtures/routing/verifier-change-routes.tsv` | `reviewed-no-change` | Its exact direct and closure outcomes are exercised through the public route API without changing expected policy. |
| `evaluation/standards-effectiveness/fixtures/routing/language-profile-decisions.tsv` | `reviewed-no-change` | It remains valid negative and specialization evidence; general route projection adds direct API coverage separately. |
| `evaluation/standards-effectiveness/suites/s1-routing.toml` | `reviewed-no-change` | Existing declarative route evidence remains valid; public API equivalence is owned by the engine integration test. |
| `tools/standards_verifier/standards_verifier/checks/metadata_route.py` | `reviewed-no-change` | It remains a downstream fixture checker and does not become routing authority. |

Historical migration plans, legacy indexes, ordinary links, and module-specific
checks were reviewed as contextual evidence, not registered as semantic
consumers merely because they mention Router. This review makes no global
Router-consumer completeness claim.

## Decision

Add one registered reviewed executable projection at
`evaluation/standards-effectiveness/router-projection.toml`.

- `STANDARDS-ROUTER.md` remains normative policy authority.
- The projection contains typed fact declarations and module-selection rules;
  it does not redefine canonical IDs, paths, `Requires`, or `Specializes`.
- `standards_analysis` owns generic typed three-valued expression loading and
  evaluation. Missing contextual facts produce `unknown`; malformed
  declarations reject loading.
- `standards_engine` loads the projection, selects direct modules, and obtains
  dependency closure from `standards_graph`.
- The projection file participates in snapshot identity. It is executable
  reviewed projection state, not generated graph authority.
- Existing verifier-change routes and new public route tests provide exact
  equivalence evidence. Python contains no policy-specific fact-to-module
  decision table.

The projection uses a small number of typed category sets rather than one
boolean per Router row. Known set membership is false when absent; an unknown
category remains unknown and creates a bounded category question instead of
dozens of per-rule questions.

## Rejected Alternatives

| Alternative | Rejection |
| --- | --- |
| Parse Router condition prose | Deterministic code cannot recover arbitrary English applicability meaning. |
| Hardcode route rules in Python | Creates competing policy authority and increases maintenance cost. |
| Support only verifier-change cases | Does not satisfy general typed navigation. |
| Treat omitted facts as false | Silently converts unknown applicability into exclusion. |
| Make the projection normative policy | Duplicates Router meaning and forces broad policy-consumer migration. |

## Acceptance

- Projection schema, fact references, types, operators, targets, and duplicate
  rules are validated before routing.
- Known category sets select exact direct modules and graph-derived closure.
- Missing category facts remain visible as typed unresolved questions.
- Existing verifier-change expected direct and closure sets match public route
  results.
- Route output feeds same-snapshot canonical `read` without repository paths.
- Router policy text and unrelated consumers remain unchanged.
