# Serial Plan Commit-Boundary Guardrail

**Status:** Implemented evidence

**Comparison base:** `d06c819b`

## Decision

Plans own semantic work, evidence expectations, and lifecycle state. They do
not own Git commit count, cadence, parentage, branch topology, exact-HEAD
admission, or standalone lifecycle commits. Review binds identified material
content. A report, lifecycle record, or unrelated commit does not invalidate
unchanged reviewed meaning. Commit continues to own coherent commit
boundaries.

This is general Planning and Commit policy. It is not an A1b-only exception.
The existing `workflow.planning.milestones-and-slices` policy unit owns the
Planning meaning and advances from semantic revision 1 to 2. No new policy
unit, suite, fixture authority, verifier, Bash behavior, A1b runtime, or A2
work is introduced.

## Consumer Dispositions

| Consumer | Disposition | Evidence |
| --- | --- | --- |
| `workflows/planning.md` | updated | Owns the plan-versus-Commit boundary, content-bound review, consolidated review rounds, and coherent lifecycle recording. |
| `prompts/planning.md` | updated | Requires plans to avoid Git-topology and state-only commit prescriptions. |
| `templates/PLAN-TEMPLATE.md` | updated | Projects the same boundary into authored plans. |
| `planning-consolidation` | updated | Uses typed decision domains and rejects plan-owned topology, ancestry-bound review, and state-only lifecycle commits. |
| `evaluation/standards-effectiveness/fixtures/planning/consolidation-decisions.tsv` | updated | Covers serial and concurrent applicability, valid content binding, prohibited topology variants, and unavailable concurrency facts. |
| `docs/archive/plans/standards-engine-a1b/plan.md` | reviewed-no-change | The corrective replan already superseded the invalid protocol and declares serial execution. |
| `workflows/commit.md` | reviewed-no-change | Already owns coherent commit boundaries and prohibits cadence-driven splitting. |
| `profiles/workflows/concurrent-plan-integration.md` | not-applicable | A1b is serial; the profile does not govern its integration. |

The Commit policy source `workflow.commit.per-commit-boundary` now has explicit
`fixture-projection` and `enforcement-suite-projection` relationships to the
existing Planning fixture and suite. The compiled policy-impact graph changes
from 251 to 253 relationships. No relationship is removed.

## Coverage Renewal

The registered suite definition and input changed, so the independent coverage
horizon changed even though the policy-unit set remains 44. The old horizon is
`sha256:e459fab25e933f2cead059e0a4c6f790204211a3f95fbe5403508e58a5e11192`.
The frozen replacement horizon is
`sha256:cafd7d1c4997f2d081c5651a1ad4fe19da11e458bb9433d6705e2741f7149e69`.

Every subject was reviewed against the replacement horizon. Existing
dispositions remain applicable except for the explicitly updated consumers
above. No missing or blocked consumer was identified. The exact mechanically
derived requirement replacement is:

| Subject | Old requirement | New requirement |
| --- | --- | --- |
| `profile.boundary.generated-contract.applicability` | `coverage-requirement:sha256:a8fa38cb36253b46d53232154b75f1709d65b6ebdf3ed5a26a9d5e3701daf80c` | `coverage-requirement:sha256:8033b7fdab9ee146b2d634bdfb6a3ae4fe0933e2150f2ab7adb3d1147850c579` |
| `profile.boundary.generated-contract.semantic-closure` | `coverage-requirement:sha256:4ea77dd072426bf304053fc509aa4c846fee721e1d9e7910b14529f75e927a68` | `coverage-requirement:sha256:6142e73c1c1be99ce4ba2ce1257b92a16b469c93234deb0f8bb72327169f7c30` |
| `router.generated-contract-profile-applicability` | `coverage-requirement:sha256:89b765bd8ab13035d65caef83aa1cceeb4bacb57536a133add515526746d41db` | `coverage-requirement:sha256:35953b7add70968017b4778a179ae50af7315f3fc92de10f8e3ebd18de739173` |
| `topic.architecture.authority-scope-admission` | `coverage-requirement:sha256:7be3cb15b7f97d38d86051b422c7fa587ce565b21adbe2afd0f5efe710b2846a` | `coverage-requirement:sha256:52ea5c63bd9c10d1dace2b9f1844a14356948f017a9228e3a0b4e185ee1ff3be` |
| `topic.architecture.immutable-authority-closure` | `coverage-requirement:sha256:cb35a5c7694859b386463e40dbf9869f07bed7189c802ec8554f9aab2641388d` | `coverage-requirement:sha256:5b08cbcd00acee1b3a9ff8320bd21a59ac04363211af8dda873bbd7eca4b484a` |
| `topic.contracts.declaration-and-semantic-authority` | `coverage-requirement:sha256:65731a8dbc66f912849659d77c314ebd18fa36a4ab0a7740e580bf7e5a8ec12a` | `coverage-requirement:sha256:f27525abef5e72b48978fb6ef4b12b836d29817f341decae10dfeb6d623f9f43` |
| `topic.contracts.generated-semantic-conformance` | `coverage-requirement:sha256:901d7eacd8480f4451abfcfa91b8c705b5847915213fda3ceb45da865d653c60` | `coverage-requirement:sha256:61d76d85d8bd8c8fb0d36fd675ac1377779a8c9a87579abe8bb3524b567206ea` |
| `topic.contracts.identity-versus-instance-equality` | `coverage-requirement:sha256:983de8da59245d3d3b29d5722321d28753d6491f2090e7dd77416e1a8c3af3dd` | `coverage-requirement:sha256:c835f3f6043b261dae50cab4990c062658cff49ef7fcf198549dc728c545f92b` |
| `topic.contracts.schema-dialect-and-vocabulary` | `coverage-requirement:sha256:6dff7047c607f9cc6a92b699520a78975ad296509ca3fba0f911e66fce8ddb80` | `coverage-requirement:sha256:3577b2674e2cb284a9d84540f97ee721edb88ba6adcd5d5abd22969a786e2002` |
| `topic.contracts.version-scope-and-invalidation` | `coverage-requirement:sha256:0e1690a636d801148dca0daa3ec86948c4449fd6cf3180f17e7253bb245328af` | `coverage-requirement:sha256:e3f20810dda73723fcefc5c8863038d242d6d492f0c8ffd3d5782e82bf34da3a` |
| `topic.dependencies.implementation-versus-dependency` | `coverage-requirement:sha256:10b96d1562b02306386ea6618d818d3806940c132692f5d467a9906e3843956b` | `coverage-requirement:sha256:f2e0cc40258d14df75c316e2438bf02732f74b72bd586a5790275d853557631f` |
| `workflow.commit.branch-context` | `coverage-requirement:sha256:f29c319904570219aa09ce79a977a840db421a2c2a91c0f348d126f13714f3ae` | `coverage-requirement:sha256:fbc7dc8e088d62787c770c4c3c19bc64e161166f52038e85514a252cb444588b` |
| `workflow.commit.branch-history-review` | `coverage-requirement:sha256:3b07556b2f130afea9ea7d95dcdd55da4a1207ff9384b2426c93a54cd34bbd23` | `coverage-requirement:sha256:8f397604ded4148852ef82c5aa8be02793f052c427bf928e72efae4e275d5db9` |
| `workflow.commit.cherry-pick-lineage` | `coverage-requirement:sha256:307e3f79ad8b116ac3da54ca063f6f032efda25a2a076dbbe5a3b156beebf30e` | `coverage-requirement:sha256:6d7641353d4a9abb72f0181318a2fb8a492abba3e5f2c3fcce89b9c3b73024de` |
| `workflow.commit.commit-message` | `coverage-requirement:sha256:b1407e21f04b7ab60675680a06f0aadd0a11b1f3aa8797146b7285c17688b0b8` | `coverage-requirement:sha256:e19abb21c8cacee47d2d6043d14d828009632f7b92c011473318a29ca8775663` |
| `workflow.commit.hook-bypass-authority` | `coverage-requirement:sha256:9fdfb250f4f0f0286e6d17d8a5254e4ffa0f9b2f5755e9d0983376ec1fc29e30` | `coverage-requirement:sha256:70943e3277e7f28f9279bd0a64c8e8c765e5b2982837764a457491626ca9772f` |
| `workflow.commit.integration-mechanisms` | `coverage-requirement:sha256:7b175637e1a8201db9adad4665a6f9b725d470412e27cbff267e3122bb14a9b7` | `coverage-requirement:sha256:679435d80a0f14f4c262e02761ee02667709d2aef33c8261eed69b7f87cad006` |
| `workflow.commit.invalid-outcomes` | `coverage-requirement:sha256:1cbfbe1e70a4cdc66f8b9f1a6f820e8592be3ecb9bd3d8177f9bf3fe94e541ce` | `coverage-requirement:sha256:35b7fa69ab91ed3a0c71f107d6f8735224d03ad3a334fa64c4db6c4c70969d2d` |
| `workflow.commit.isolation-applicability` | `coverage-requirement:sha256:40f861f7ffe6efb3f12bd6b4623b6cd5341cc022f39fc94783b9804d73799acf` | `coverage-requirement:sha256:c587b1584a9a851c7459babe068190125f26092e455b1ca3ad71982abb00ecf2` |
| `workflow.commit.per-commit-boundary` | `coverage-requirement:sha256:2841085d54814abe2f5d6fae95bd097d858d89314ea405c26fe2e495410e9bee` | `coverage-requirement:sha256:67e3bc334d98f418dcd1380e2916be9c73a00ae320a4782e1f8e1e96960c0898` |
| `workflow.commit.rewrite-authority` | `coverage-requirement:sha256:5f64492f3834336ee9a51bab823d18c60646bbf39e1f9c80883d9e4d5ed44774` | `coverage-requirement:sha256:cf9eb53d6b416077316fc5c4a964470816a9c6bcde2639b5324dcca145b1124b` |
| `workflow.commit.terminal-branch-lifecycle` | `coverage-requirement:sha256:6454d6925771014cc7d9e7d143139f2befb3af9b936d613d3de979f93472770b` | `coverage-requirement:sha256:d7e066fb28ad01f2a96bdef7088aeff9e29b91a86de39bd50e5dbf7aac03dede` |
| `workflow.commit.topology` | `coverage-requirement:sha256:a6706e796d90ef67ba2b812992ef691ecf745f82666b7fdea0ef861a799b6a9c` | `coverage-requirement:sha256:c9f3f184a582d7d11f56387687cd94feacd235befbed4d593599e94de9fc5c83` |
| `workflow.commit.worktree-lifecycle` | `coverage-requirement:sha256:b65159c6f42809bce68958cc95e5df777eefcf4016f4aed17920999dad6d5090` | `coverage-requirement:sha256:5ce5ac3a2a146276fbadeaa119da12a29aeb9c8011e8dfb0a7c453f9125899d3` |
| `workflow.planning.acceptance-claims` | `coverage-requirement:sha256:38c85ce6d13cc9ad0011a6e88a1fee8de457970f8edcd8b97b7381c74b622b05` | `coverage-requirement:sha256:8e85104d80adede6d537fe6f00c663128883d6a3eae91fb74ddd6a5ac8269ad8` |
| `workflow.planning.active-plan-fields` | `coverage-requirement:sha256:40c9168867ea14229634afed0565950631965365757fb48f0d6fb17d638d1131` | `coverage-requirement:sha256:84f7be5d8924ea52da235efb345f5e4b09f689739a348ba714949581840fb988` |
| `workflow.planning.artifact-model` | `coverage-requirement:sha256:6fe935ed6090e34c110d7253541c2c30f24d4070f506fe1998fdf43967d08e29` | `coverage-requirement:sha256:70f8f337d62e5f25e237e9ae0f85ab99fc854ba1c67a792f7649f6e9f4525e95` |
| `workflow.planning.completion` | `coverage-requirement:sha256:adb2fd8604cede01d29cb53b18ec5f77925cbdc21628cd2c0fe29121565fd72b` | `coverage-requirement:sha256:ba02297abdbb959df2d0c72f70de4bcbc2cf41bdfe7f107048b148a7a8745cc0` |
| `workflow.planning.concurrent-integration-routing` | `coverage-requirement:sha256:af81cdda41d2c532c440e652ba913dd33bf6e6fa8b493f8c5970695dc77f775b` | `coverage-requirement:sha256:ee203d56fa43ce03b51cce5812d3772a446d3890a2e8f6b14dd40b494c5ef7aa` |
| `workflow.planning.concurrent-work` | `coverage-requirement:sha256:d19efaf7bdf71c9096eb4c16e8804c1e0b4801a4441087682a724f55a71da570` | `coverage-requirement:sha256:730eee0dabd195c2f61f10f3e100c7d0ee6ff38f5a2982fcc3f4776e501fa403` |
| `workflow.planning.current-state` | `coverage-requirement:sha256:9fd1cfa9e2ccf262c24c356d6b28ba0d88f8ca516aa58e6e3181afce4b2fda7d` | `coverage-requirement:sha256:9b8b415a1294213103375117c56c2ed76d6546eb5f64f646adb6c07a4d6c956c` |
| `workflow.planning.findings` | `coverage-requirement:sha256:c1e2e4784bb440414f2130dbe0ef0a9ed61217cf710565ad8aead3ea08f5af9a` | `coverage-requirement:sha256:b14411a30e471585ec75bad17f00faa2b6bca0280f33dc81ae44c3740ee53611` |
| `workflow.planning.lifecycle` | `coverage-requirement:sha256:083baf8e7d89118b87ac9fe7040c355d31075b42ac926cca2971a5396ecc711e` | `coverage-requirement:sha256:1fbd0b36b56e40f201a72d1933de1604e79ef00b702bc9a128fef573e4dabdbc` |
| `workflow.planning.milestones-and-slices` | `coverage-requirement:sha256:100a731a1f37196c34af58b06b6e110f327ecb4178f036680f31ef112cf7ae81` | `coverage-requirement:sha256:f35274caea03e4c392da561841c6044c01be95bf029e4fe069cf307cfbbba290` |
| `workflow.planning.plan-admission` | `coverage-requirement:sha256:2411a8fd415586be5806a0e52cd84150cea714da2fb413096827a2e5071456b9` | `coverage-requirement:sha256:e53e9350fdc4eb974bc552334873e4919809416314f822e9bbd1c558662de701` |
| `workflow.planning.projection-completeness` | `coverage-requirement:sha256:453fc10e1819b12a026b5262dcbccf6ca8d33061a256cce774e1b9c27fc5c93f` | `coverage-requirement:sha256:43efd6afe21beae5e748906095b3fc52d36e27a8c1f315a304b02b4cc1cd4931` |
| `workflow.planning.replanning` | `coverage-requirement:sha256:01e09cece4f573534cea17b14a2f147c28fa3b3d018e9eb108c37870feb484ab` | `coverage-requirement:sha256:556cac2c0c13086cc3705db5d3bf3bfc916634e956cff3caa1316a1e30dc93e6` |
| `workflow.planning.repository-isolation` | `coverage-requirement:sha256:e461fd7a83971bf83e8c1049d9b0af32dfc978d46a3ed3139cba5c404747668f` | `coverage-requirement:sha256:f777419d8ed461f2fb8e2aeda813919cb332ef0b5d5d6e609c2ae26203579676` |
| `workflow.planning.systemic-finding-replan` | `coverage-requirement:sha256:f8994047f4c504db5f26da7ab3c0f73697d1d24efb090de3954d67fdfe7612db` | `coverage-requirement:sha256:82bd1014ca914f7393641b5595c0d9011c30526995e5a0036147ccae374d927f` |
| `workflow.planning.written-plan-applicability` | `coverage-requirement:sha256:aa2c2cf2de3b4bebbb9f73a7c6a1bd72afed24d41a2d0eefeded72613e51856e` | `coverage-requirement:sha256:d22cfbc7c1ce5d3dd29516b4571843e159300514b048ee028340f265dcdc1b7f` |
| `workflow.verification.acceptance-claims` | `coverage-requirement:sha256:a78c5f73f0e92bb80d4d04887f7dfacce06b04230a2141d2b8340d9a25277d05` | `coverage-requirement:sha256:91c5b352dde270d2442510de5570456fd88406373e3d8caa7b58171e06d9bc2e` |
| `workflow.verification.differential-evidence` | `coverage-requirement:sha256:e71641f3b02bd2d8b50d96c76aa580e1055951642dfbf9fbaf9355ed53fa0dbb` | `coverage-requirement:sha256:ed3db71d36cf432378e6819b29c5b6da158e033debf7663406427bf75e662519` |
| `workflow.verification.evidence-oracle-boundary` | `coverage-requirement:sha256:5ae8af506032d84b3cc0721e1b25c8aca3cecae467d57e912f8bbf4844fc045d` | `coverage-requirement:sha256:68712e5ca7981b33147095170cba412d51670033631a36804785d16e1f177c86` |
| `workflow.verification.negative-fixture-isolation` | `coverage-requirement:sha256:fb6160e5f47943c8d3a522218fd8ed31fc45368faaa5ca7b1abef3ba9dfb87ca` | `coverage-requirement:sha256:1294a18bccb3c2a2922a9e64f541f8aa66fb7f64e5a62a38394fe723f211dac6` |

## Authorization

The repository owner explicitly directed the standards-compliant correction
and continuation on 2026-08-27. That authorization covers the general policy
projection, the existing-suite enforcement change, the two missing semantic
relationships, and renewal of attestations against this exact frozen horizon.
It does not authorize A1b runtime or A2 implementation.

## Verification

Acceptance requires the focused Planning suite, policy-impact and coverage
verification, generated freshness, plan validation, all registered declarative
suites, every retained migration checker, and diff hygiene to pass without a
new Bash checker or an increased known-failure baseline.
