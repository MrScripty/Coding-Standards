# Standards Recovery Consumer Dispositions

**Status:** `Milestone 1 candidate evidence`

**Admitted policy-implementation base:** commit
`59ecd309ae85db9d1f194ca3b49a23e79df51c62`, tree
`669b9d98b3c4baccc96e5bac29ceee06e532dda0`

## Scope And Authority

This report assigns one disposition to every consumer selected by the
pre-policy scope audit. It does not replace the suite registry, the audit's
exact non-registry path list, policy-impact declarations, coverage
attestations, or final acceptance evidence.

Consumer membership is the admitted `W/S/E/R` closure:

- `W` is the exact Milestone 1 write set in the active plan.
- `S` is resolved from the audit-selected suite IDs through the canonical
  suite registry and each suite's registered inputs.
- `E` is the audit's exact non-registry consumer list.
- `R = (S union E) - W` is protected and was not modified.

Where a row below names an audit section or suite ID set, the disposition
applies independently to every exact member resolved by that authority. A path
present in more than one set is canonicalized before assignment. Conflicting
assignments are invalid; none are present in this candidate.

## Updated Consumers

| Consumer | Disposition evidence |
| --- | --- |
| `STANDARDS-ROUTER.md` | Adds observable Generated Contract applicability while keeping IPC and Language Binding conditional. |
| `workflows/verification.md` | Adds evidence-oracle, negative-fixture, and differential-evidence policy units. |
| `topics/contracts.md` | Adds generated semantic conformance, dialect/vocabulary, and equality-domain policy units. |
| `topics/architecture.md` | Adds immutable authority closure. |
| `topics/dependencies.md` | Adds the implementation-versus-dependency decision contract. |
| `workflows/planning.md` | Adds systemic-finding class audit and replanning. |
| `profiles/boundaries/generated-contract.md` | Adds the routed Generated Contract profile and semantic closure. |
| `prompts/planning.md` | Projects routed authority, oracle selection, dependency decisions, and systemic audits. |
| `prompts/implement-plan.md` | Projects implementation stops and admitted evidence/decision boundaries. |
| `templates/PLAN-TEMPLATE.md` | Adds only the material oracle and systemic-audit records. |
| `evaluation/standards-effectiveness/canonical-module-corpus.toml` | Registers the Generated Contract profile as one canonical module. |
| `evaluation/standards-effectiveness/router-projection.toml` | Adds the versioned boundary fact member and stable profile-selection rule. |
| `evaluation/standards-effectiveness/policy-units/*.toml` paths in `W` | Register exact, non-overlapping semantic owners for every changed policy heading. |
| `evaluation/standards-effectiveness/policy-impact*.toml` paths in `W` | Compile source-owned relationships to canonical modules and cataloged consumers. |
| `evaluation/standards-effectiveness/fixtures/routing/generated-contract-decisions.tsv` | Covers positive, negative, conditional, and unresolved boundary decisions. |
| `evaluation/standards-effectiveness/fixtures/routing/generated-contract-routes.tsv` | Covers complete required-module routing. |
| `evaluation/standards-effectiveness/fixtures/verification/evidence-oracle-decisions.tsv` | Separates independent evidence from freshness and local agreement. |
| `evaluation/standards-effectiveness/fixtures/contracts/generated-contract-conformance-decisions.tsv` | Separates closure, freshness, semantics, public behavior, and equality domains. |
| `evaluation/standards-effectiveness/fixtures/architecture/immutable-authority-decisions.tsv` | Covers captured authority, storage, process, mutation, and ambient-state outcomes. |
| `evaluation/standards-effectiveness/fixtures/dependencies/implementation-versus-dependency-decisions.tsv` | Covers local implementation, dependency adoption, unsupported semantics, and unavailable decisions. |
| `evaluation/standards-effectiveness/fixtures/planning/systemic-finding-replan-decisions.tsv` | Covers isolated and systemic findings with complete and incomplete audits. |
| `evaluation/standards-effectiveness/fixtures/planning/systemic-finding-missing-audit.md` | Isolates the exact missing-systemic-audit failure outside the retained Bash glob. |
| Six recovery suite definitions and their registry entries | Enforce each policy family through the Python verifier and register exact horizon inputs. |
| `tools/standards_analysis/tests/test_routing.py` | Replaces mutable catalog totals with stable Generated Contract fact/rule semantics. |
| `tools/standards_policy_impact/tests/test_compiler.py` | Replaces mutable relationship totals with complete graph/semantics identity-set equality. |

## Registry-Derived Existing Suites

Every definition and registered input resolved from the following audit-owned
suite IDs is `reviewed-no-change`:

| Policy family | Suite IDs |
| --- | --- |
| Verification/oracles | `acceptance-claims`, `verification-quality-gates`, `verification-ownership`, `testing-acceptance-paths`, `testing-focused-design`, `testing-gates-diagnosis`, `testing-coverage-documentation` |
| Contracts/generated semantics | `contract-artifact-selection`, `contract-boundary-proof`, `contract-invariants`, `contract-planning-boundary`, `contract-semantic-preservation`, `testing-persisted-contract-artifacts` |
| Architecture/immutable authority | `architecture-data-authority-pattern`, `architecture-durable-workflow-pattern`, `architecture-owner-contract`, `persistence-owner-contract` |
| Dependencies | `dependencies-owner-contract`, `dependencies-population`, `dependency-audit-lineage`, `dependency-standards-consolidation`, `coding-dependency-route` |
| Planning/systemic findings | `planning-admission`, `planning-consolidation`, `policy-semantic-impact`, `plan-template-projection`, `full-review-prompt-entrypoint`, `plan-implementation-entrypoint` |
| Router/profile | `root-index-closure`, `language-index-closure`, `coding-dependency-route`, `router-legacy-route-closure` |
| Supporting owners | `build-owner-contract`, `tooling-owner-contract`, `documentation-traceability-policy`, `implementation-change-evidence`, `licensing-owner-contract` |

These suites continue to enforce their existing owners. The six new recovery
suites own the new behavior; no retained suite or Bash checker was extended to
simulate that ownership.

## Exact Non-Registry Consumers

The paths in each named audit group receive the following disposition. The
pre-policy scope audit remains the exact path authority.

| Audit-owned group | Disposition | Evidence |
| --- | --- | --- |
| Supporting standards, profiles, projections, and durable reports not listed under Updated Consumers | `reviewed-no-change` | Build, Tooling, Documentation, Implementation, Licensing, Library, Persistence, the full-review prompt, PR template, historical A1 reports, and the Standards Verification plan retain compatible ownership. |
| Retained migration-owned plan checkers | `reviewed-no-change` | Existing behavior is unchanged. New negative and systemic scenarios run only through registered Python suites. |
| A1 contract, runtime, and composition sources | `reviewed-no-change` | Recovery records A1 behavior and the known schema-equality nonconformance; runtime correction remains A1b scope. |
| Existing Python-verifier adapters | `reviewed-no-change` | Existing generic decision, text, path, metadata, graph, and checkpoint adapters execute the new suites without source changes. |
| Focused accepted-A1 and verifier tests other than the two Updated Consumers | `reviewed-no-change` | Existing assertions remain applicable. Three admitted live-authority cardinality replacements remain sequenced after Milestone 2 coverage renewal. |
| `profiles/boundaries/language-bindings.md` | `reviewed-no-change` | Selected only when a genuine native/host or cross-language boundary exists. Generated output alone does not select it. |
| `profiles/boundaries/ipc.md` | `reviewed-no-change` | Selected only when a process or independent-deployment boundary exists. Generated output alone does not select it. |
| Dependency and toolchain manifests | `not-applicable` | Recovery adds no third-party implementation dependency and incorporates no external files. The reference-only specification decision remains separately recorded. |

## Policy-Subject Reconciliation

| Policy-unit source | Consumer projection result |
| --- | --- |
| `workflow.verification.evidence-oracle-boundary` | Prompts, plan template, Documentation, fixture, and enforcement suite are represented. |
| `workflow.verification.negative-fixture-isolation` | Isolated negative fixture and Python enforcement suites are represented; retained checkers remain review-only migration consumers. |
| `workflow.verification.differential-evidence` | Contract fixture, independent reproduction report, and enforcement suite are represented. |
| `topic.contracts.generated-semantic-conformance` | Router/profile, Build/Tooling, prompts, generator/generated/public artifacts, fixture, and suite are represented. |
| `topic.contracts.schema-dialect-and-vocabulary` | Profile, dependency policy, schema/generator/validator, fixture, and suite are represented. |
| `topic.contracts.identity-versus-instance-equality` | Identity serializer, schema validator, generated validator, applicability values, persisted handles, reproduction report, and suite are represented. |
| `topic.architecture.immutable-authority-closure` | Persistence, engine inspection, snapshots/state/results, fixture, and suite are represented. |
| `topic.dependencies.implementation-versus-dependency` | Router/profile, planning and implementation prompts, fixture, and suite are represented. |
| `workflow.planning.systemic-finding-replan` | Planning and implementation prompts, plan template, positive/negative fixtures, and suite are represented. |
| `router.generated-contract-profile-applicability` | Executable Router projection, profile, prompts, routing fixtures, and suite are represented. |
| `profile.boundary.generated-contract.applicability` | Router prose/projection, prompts, routing fixtures, and owner suite are represented. |
| `profile.boundary.generated-contract.semantic-closure` | Contracts, Verification, Build, Dependencies, generated/public artifacts, fixture, and suite are represented. |

All declaration applicability is explicit `always`; no predicate was inferred
from rationale or a repository path. Every evidence owner resolves to one
registered suite. No selected consumer has a `blocked` disposition.

## Deferred Coverage Work

Milestone 1 freezes the relationship and horizon authority. Milestone 2 must
derive the resulting coverage requirements, renew attestations once, generate
valid certificates, and prove exact subject equality before final acceptance.
The expected stale-attestation result before that renewal is not a blocked
consumer disposition and does not authorize runtime or protected-test edits.
