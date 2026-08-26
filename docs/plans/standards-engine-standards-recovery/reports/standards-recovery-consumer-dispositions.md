# Standards Recovery Consumer Dispositions

**Status:** `Replan active; two consumer corrections pending`

**Admitted policy-implementation base:** commit
`59ecd309ae85db9d1f194ca3b49a23e79df51c62`, tree
`669b9d98b3c4baccc96e5bac29ceee06e532dda0`

## Scope And Authority

This report assigns one disposition to every consumer selected by the
pre-policy scope audit. It does not replace the suite registry, the audit's
exact non-registry path list, policy-impact declarations, coverage
attestations, or final acceptance evidence.

Consumer membership is the admitted `W/S/E/R` closure:

- `W` is the exact admitted Milestone 1 write set.
- `S` is resolved from the audit-selected suite IDs through the canonical
  suite registry and each suite's registered inputs.
- `E` is the audit's exact non-registry consumer list.
- `R = (S union E) - W` is the prior protected closure.
- `O` is the exact two-test Milestone 2 correction set, and
  `R2 = R - O` remains protected during that correction.

Where a row below names an audit section or suite ID set, the disposition
applies independently to every exact member resolved by that authority. A path
present in more than one set is canonicalized before assignment. Conflicting
assignments are invalid; none are present in the reconciled closure.

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
| `tools/standards_verifier/tests/test_policy_impact.py` | Proves semantic policy-impact projection and owner closure without a mutable relationship total. |
| `tools/standards_engine/tests/test_navigation.py` | `correction-required`: replace its mutable dependency-cause threshold with exact graph-derived cause-set equality while preserving deduplication. |
| `tools/standards_engine/tests/test_analysis.py` | `correction-required`: replace dependent-program and obligation thresholds with exact compiler-derived program and reason-edge sets. |

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
| Focused accepted-A1 and verifier tests not listed under Updated Consumers | `reviewed-no-change` | Existing assertions remain applicable. All admitted live-authority cardinality replacements are complete and independently accepted. |
| `profiles/boundaries/language-bindings.md` | `reviewed-no-change` | Selected only when a genuine native/host or cross-language boundary exists. Generated output alone does not select it. |
| `profiles/boundaries/ipc.md` | `reviewed-no-change` | Selected only when a process or independent-deployment boundary exists. Generated output alone does not select it. |
| Dependency and toolchain manifests | `not-applicable` | Recovery adds no third-party implementation dependency and incorporates no external files. The reference-only specification decision remains separately recorded. |

## Policy-Subject Reconciliation

The separately governed policy-impact authority v2 prerequisite has replaced
the shared compiler, graph, analysis, verifier, public-contract, and coverage
projections used by this report. Its current certification proves exact
policy-unit/requirement/attestation/certificate subject equality through one
compiled Interface. This migration changes no six-policy consumer disposition
below and does not accept standards recovery. The prerequisite and the separate
recovery-resume transition are independently accepted and complete; Milestone 1
reconciliation and Milestone 2 coverage below derive from that admitted
authority.

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
registered suite. The two Standards Engine test consumers above are blocked
pending the admitted semantic-oracle correction; every other selected consumer
remains non-blocked.

## Milestone 1 Reconciliation Evidence

Reconciliation is bound to recovery-resume start commit
`3fa59052960a85c2b85930a156d2061f91a89cfc`, tree
`d72c2a871bc94b08bdb4417c11c3fddb85eb5f57`.

The protected closure was rederived from its owners rather than copied into a
new manifest:

| Set | Canonical set digest | Result |
| --- | --- | --- |
| Audit-selected suite IDs | `sha256:b7f518d73c6b53d619be94b232be1443cfbe9c37fb1d9ad9fed550110888a78f` | Every ID resolves to one registered suite definition. |
| Suite definitions and registered inputs (`S`) | `sha256:28c89662509f3e39d7263c6a308b8846a613d2d23b5a6fd742370d6fd6942af3` | Every registered path resolves. |
| Exact non-registry consumers (`E`) | `sha256:c3b06f4455c0c8a6eb76a29b3c32dbef4c100de4afccc8ff31c4fc551df84150` | Every exact path resolves; no wildcard is present. |
| Milestone 1 write set (`W`) | `sha256:bb4cab1bc88b56afde7b275f1a56428b08fa1b70364ffa18a513dba60512ca21` | Exactly the four admitted Milestone 1 paths were writable. |
| Protected closure (`R`) | `sha256:c793877e1605eca0b5ff21fed71b49d969615269a64cd6e41932ce2f006b66a9` | `R = (S union E) - W`; `W intersect R` is empty. |
| Complete mapped closure (`W union R`) | `sha256:95b73a7db9efa6cdb0ed97817d7b29fd4b378035b36de585a397e1d5fd924e65` | Every mapped consumer has the disposition assigned by this report. |

Compiled comparison across planning baseline `3439aae9540786d9734431e633ea5b62afb50592`,
pre-prerequisite recovery boundary `cb6abdb89afaa4fca25706cd42f621a8c762480f`,
and the current start tree produced canonical migration projection digest
`sha256:c1673d49bdac3097228d4cf12f4ea4a4c2aad128d7a6674b2a396f75f0855ab9`.
Every planning-baseline relationship is materially retained. Recovery adds
only relationships originating from the policy subjects in Policy-Subject
Reconciliation above. The accepted prerequisite migration table exactly
matches its mapped old and new natural-key subsets; its only dispositions are
`retain` and `reclassify`. Every relationship outside that table is identical
across the pre-prerequisite and current sets. For every mapped row,
applicability, scopes, propagation, evidence owner, rationale, groups, and
traversal remain equal; `reclassify` changes only the admitted relation and
derived edge identity.

Every policy subject above resolves to one active canonical policy unit at the
module and heading recorded by the semantic-impact inventory, has nonempty
content and representation/structural digests, and compiles as a relationship
source. Router and profile projections, the six registered recovery suites,
generated contract freshness, canonical contract validation, and focused
metadata, policy-impact, graph, analysis, engine, and verifier behavior all
revalidated without requiring a protected-consumer mutation.

The complete repository checkpoint passed on this exact content through
`python3 tools/standards_verifier/verify.py --complete`. The selected recovery
suites, focused package matrix, contract generation and validation, plan and
lifecycle checks, generated checker inventory, retained migration checks, and
`git diff --check` also passed. These executions verify the named semantic and
set-equality claims above; diagnostic corpus totals are not acceptance oracles.

## Final Coverage Result

Milestone 2 rederived every requirement from the frozen authority and reused
every dependency-valid attestation without modification. The exact active
policy-unit, requirement, attestation, and generated-certificate subject sets
are equal, as recorded in [final coverage evidence](standards-recovery-coverage.md).
This result does not accept the recovery or authorize runtime or protected-test
edits; independent exact-tree acceptance remains pending.
