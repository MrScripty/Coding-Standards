# Policy-Impact Authority V2 Milestone 0 Candidate

**Status:** `Implemented`

**Implementation base:** commit
`95cb97babff778497857e9e6be44ddc81e446564`, tree
`1d85875000ddbf75256a4ec85e12fffcf196e04f`

**Exact-head restart:** commit
`e9f054b9`

This record covers the coordinated internal-authority and public-contract
cutover. It does not claim current coverage, complete cold-process execution,
prerequisite acceptance, A1b implementation, or A2 admission. The exact commit
and tree containing this implementation are recorded by the first clean
Milestone 1 ledger entry rather than asserted recursively by this report.

## Implemented Boundary

- One internal version 2 authoring contract owns artifact kinds, relationship
  kinds, graph groups, propagation, evidence rules, and target compatibility.
- The compiler produces one immutable graph, semantics, provenance, and
  coverage-fingerprint view. Graph composition, analysis, and verification
  consume that result without reparsing the supplemental node catalog.
- All registered declaration sources use schema version 2. Schema version 1
  and mixed catalog-edge authority reject without a compatibility loader.
- Supplemental artifacts carry explicit typed identity. Implementation
  consumers use `implementation-projection`; admitted canonical references
  retain `reference-projection`.
- The admitted relationship-migration TSV is executable evidence: its exact
  replacement identity set equals the compiled relationships selected by its
  source/consumer keys. The test derives the set from the inventory and stores
  no mutable relationship total.
- Seven retained negative cases execute through the production compiler and
  verifier Adapter. The obsolete owner-wide enforcement inference case and its
  declaration were removed.
- Public A1 schema version 10 exposes operation-shaped relationship inspection
  and removes the three compiler-internal declaration, semantics, and program
  definitions. Query, prepare, resolve, and inspect reject old handles as
  unsupported before ordinary argument validation.
- Persisted state and navigation identities use their accepted version 3
  domains. The directory store and state decoder reject old versions rather
  than interpreting them under the new contract.

## Exact Negative Evidence

| Case | Exact diagnostic |
| --- | --- |
| `duplicate-edge` | `POLICY_IMPACT.DUPLICATE_EDGE` |
| `unknown-owner` | `POLICY_IMPACT.UNKNOWN_OWNER` |
| `unknown-consumer` | `POLICY_IMPACT.UNKNOWN_CONSUMER` |
| `missing-applicability` | `POLICY_IMPACT.APPLICABILITY` |
| `malformed-relation` | `POLICY_IMPACT.RELATION` |
| `path-escape` | `PATH.OUTSIDE_REPOSITORY` |
| `missing-file` | `INPUT.UNAVAILABLE` |

The registered `negative-fixtures` check was invoked independently of the
coverage-blocked current-structure check and returned no assertion diagnostic.
No test accepts an arbitrary nonzero result or a different failure reached
earlier in fixture setup.

## Current Coverage Requirements

The following subjects and requirement handles were derived mechanically from
the current canonical corpus, compiled v2 authority, and horizon version 3.
They are the exact expected stale-coverage boundary entering Milestone 1.
These rows are evidence, not authored coverage authority.

| Subject | Current requirement |
| --- | --- |
| `topic.architecture.immutable-authority-closure` | `coverage-requirement:sha256:d634ac8028327f10438fa4b5c2f6a92045150c039fb61b269b3d99605df72f03` |
| `workflow.commit.per-commit-boundary` | `coverage-requirement:sha256:1477b1a88ab420969916df5a269c234eccf4821f024a9f4042aaac7bdd79708f` |
| `workflow.commit.isolation-applicability` | `coverage-requirement:sha256:53727bea87197df55a8c5bad34ec5e9477e7ca2a94e0f7cc8ed319d642f7d093` |
| `workflow.commit.branch-context` | `coverage-requirement:sha256:74f230752b60d50aa714be8420513473a275c2d1470c114102672f335a320fb0` |
| `workflow.commit.integration-mechanisms` | `coverage-requirement:sha256:a94e65ead099eb4e57f23ebbe8a226b1343c559c42a3b8c4611edbf4c2721fec` |
| `workflow.commit.cherry-pick-lineage` | `coverage-requirement:sha256:849e743c5c371ca6e2cc7dc7ef9468ff3bb2314a8fa9ae5a76d6f70b95c44712` |
| `workflow.commit.terminal-branch-lifecycle` | `coverage-requirement:sha256:0f99989227e437db33629d9940d6ac7aaa0ed0775cf881fd7b0691af56995e15` |
| `workflow.commit.worktree-lifecycle` | `coverage-requirement:sha256:88f0a46e6faadbdf55032ef5ce0d06aa54f72382bce562ce292907c3a41bcea5` |
| `workflow.commit.branch-history-review` | `coverage-requirement:sha256:319bdf7b4735f0eb411c2c3ceac67d5b476334dbd11d16c68df34c444085fa3b` |
| `workflow.commit.hook-bypass-authority` | `coverage-requirement:sha256:a2238acd41ce964ea24b72d75e55db91b5d42d95c5e9a047519d2c2b29facea1` |
| `workflow.commit.rewrite-authority` | `coverage-requirement:sha256:c9ff3c2d95b477016bb44a309a3387fff44a4d4cace1454b7e3539bc973697c9` |
| `workflow.commit.topology` | `coverage-requirement:sha256:188d94b7756ac0f40490513852aeb92aa1b7169fcdf74084ebdbb24566b190f7` |
| `workflow.commit.commit-message` | `coverage-requirement:sha256:ce39493273fed42dbadcf48da16d3da9e81b1856a7b5a2a20e6b6994fe0251bd` |
| `workflow.commit.invalid-outcomes` | `coverage-requirement:sha256:a81c15df4fc6a79b150534ceaafa82c24f7835df4afe2622ba0db26b57ce191a` |
| `topic.contracts.generated-semantic-conformance` | `coverage-requirement:sha256:94247fe7d0a3b6a079f4992a74c476ff64daeadc3ae991d5a50a41918d8e490f` |
| `topic.contracts.schema-dialect-and-vocabulary` | `coverage-requirement:sha256:a93be23bf30cae2f967a649c5171ac57aebfb0eccc8dacf0a286f8fc14dac636` |
| `topic.contracts.identity-versus-instance-equality` | `coverage-requirement:sha256:d39621cbaad0f29add3993a94f633678d3795b709e68b43abfb87258ee583e44` |
| `topic.dependencies.implementation-versus-dependency` | `coverage-requirement:sha256:da3527add574018e1d76b7befdc7e076471ca2a008678f3404b3657bf8e59736` |
| `profile.boundary.generated-contract.applicability` | `coverage-requirement:sha256:686d99c504ffc290db7f1f8bd038bc2c78da018ff948137d6a2f144979ebf5d1` |
| `profile.boundary.generated-contract.semantic-closure` | `coverage-requirement:sha256:ce911f272fcff1edc7519b3bb147d94529503301888c56f9878e7ae3b636e685` |
| `workflow.planning.written-plan-applicability` | `coverage-requirement:sha256:4fddcc518ee71e37d5738928a15d9101b974093fe0722d3845a41d604e60189e` |
| `workflow.planning.artifact-model` | `coverage-requirement:sha256:7da1627b49430b379e7ae67e8c969fb4da8562453dc132984f4e6ebd9ea43231` |
| `workflow.planning.active-plan-fields` | `coverage-requirement:sha256:e1876c45419f7dfca220b45a3679ae0c45ed6216cca9d45f79a8bb910753f6d1` |
| `workflow.planning.lifecycle` | `coverage-requirement:sha256:79cad697ecd97e90a753891d0f731892f46b1ac5f13c297d2ba580de97c7e01a` |
| `workflow.planning.plan-admission` | `coverage-requirement:sha256:8948f4a27438ed0a832fd32d5b37e71effd84f12e9c920237318a449f2445194` |
| `workflow.planning.concurrent-integration-routing` | `coverage-requirement:sha256:e5d9fd751411a0d5229c6873491532870112ea7f810a35795ae2187fe425809c` |
| `workflow.planning.repository-isolation` | `coverage-requirement:sha256:c449122550523473ed3221c3ec3e217088c49963bc16a073a74f78e59169b85a` |
| `workflow.planning.projection-completeness` | `coverage-requirement:sha256:266dd17c7d6c44e97db614551373c16dfa402fd824d2ebed71f21edd04b77fe2` |
| `workflow.planning.acceptance-claims` | `coverage-requirement:sha256:1ee3238778eee7f42235bb94500504a7110c97b31718f882a0ab6b8561043235` |
| `workflow.planning.milestones-and-slices` | `coverage-requirement:sha256:f90ab1c0e0d1907810dc6337d3faea76a2d64702e227ea16b451c55475eaa6fb` |
| `workflow.planning.current-state` | `coverage-requirement:sha256:76e6b50435c8a07b47e05db1e1e1644554576b510f01dc022541553eb86df612` |
| `workflow.planning.replanning` | `coverage-requirement:sha256:ead22f13cf92a87486960eb9c9ffed3ecbfb05aa8545e7756dc93813ec059331` |
| `workflow.planning.systemic-finding-replan` | `coverage-requirement:sha256:969baefd3e0c515a542cede68ef1ee32137edf46569faa001d8e408faab17101` |
| `workflow.planning.findings` | `coverage-requirement:sha256:93b7ef765beb46c88ab9e18c8a4c0db79d80820b43f1bdefa10536a714b68774` |
| `workflow.planning.concurrent-work` | `coverage-requirement:sha256:2ef015ec3b99cd045e6f386dd21778447d6b6fff38d9d39cb9ce42c31d545ef6` |
| `workflow.planning.completion` | `coverage-requirement:sha256:7bc739acfe8539be80000ec9b3b7b3b8f827f68f47e1bf86f16d4f563d1dbabf` |
| `router.generated-contract-profile-applicability` | `coverage-requirement:sha256:d1c5349c04b6626fed3b398be2ebad777cc96739c9f0385437330ad0c45705c3` |
| `workflow.verification.acceptance-claims` | `coverage-requirement:sha256:6434e1378b5a0392cf097bf1291e9668f1343dfab0e7a8b86a3448312dc23d49` |
| `workflow.verification.evidence-oracle-boundary` | `coverage-requirement:sha256:580e47d822946a85440f4f6a0ab5ba9c7d254f2dee246472815f08137f68632e` |
| `workflow.verification.negative-fixture-isolation` | `coverage-requirement:sha256:4eba0e3b2d5e4360c18e54c8801e6dcb3d4006d17b4000a27de5011c072e6463` |
| `workflow.verification.differential-evidence` | `coverage-requirement:sha256:b46a6320d374973a0cba3667c625d890a495dece92995f73b55cafc2880d4d2d` |

## Verification

| Surface | Result |
| --- | --- |
| Policy-impact compiler | 8 tests passed, including exact migration-set equality |
| Standards graph | 2 tests passed |
| Standards analysis | 82 tests passed |
| Standards verifier | 379 tests passed |
| Focused public contract and version tests | 14 tests passed |
| Contract validation | 32 examples, 8 identity fixtures, 4 operation envelopes, and 141 definitions passed |
| Generated projection freshness | Passed |
| Scoped Ruff and Git diff validation | Passed |
| Registered declarative suites | 223 passed; only `policy-semantic-impact` failed at `COVERAGE.ATTESTATION_VERSION` |
| Generated migration inventory and graph | Passed |
| Retained migration checkers | All 53 current checkers passed without source changes |

The Standards Engine repository-backed analysis and navigation classes stop at
the same production attestation-version failure during setup. Their focused
contract, rendering, unsupported-version, compiler, graph, analysis, and
verifier dependencies pass. This is the only permitted M0 checkpoint blocker
and is owned by the frozen-authority certification work in Milestone 1.

## Disposition

Milestone 0 source work is implemented. Milestone 1 must now freeze the exact
authority, author one valid attestation per derived requirement through the
accepted coverage Interface, generate certificates, execute the existing
genuine cold-process reconstruction, and run the complete acceptance boundary.
No current attestation or certificate is accepted by this report.
