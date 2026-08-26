# Standards Recovery Final Coverage Evidence

**Status:** `Frozen prior evidence; renewal pending admitted test correction`

**Milestone 2 execution boundary:** commit
`f037ab11c6bdcda8b61a64c5aa1932e86570096b`, tree
`212206c6aeb60830c3bed5df392358ff953590a2`

This report records deterministic coverage compilation for standards recovery.
It is evidence for a later candidate review; it is not an authored attestation,
generated certificate authority, or acceptance report.

## Frozen Authority

| Authority | Exact identity |
| --- | --- |
| Coverage horizon | `sha256:538c9ef051b79129beb5d471394d9c399c7e3c2882567c6aad4c16c1b4d62f43` |
| Compiled declarations | `sha256:dde852daaa6bb60d1987f44f46140e9de80cc3bd0c9d6277ec2f7fa037c8a0dd` |
| Supplemental artifact catalog | `sha256:aff67842c9b61404bc32b0755539b20ada91931912e597354d2b9d426815f620` |
| Policy-impact authoring contract | `sha256:79e3da8c9b146588bff81a1da695a852680425edd68439d57dcea402e9948a4b` |
| Policy-impact provider contract | `sha256:e4124f6088b1c21c5e8a7d707cee7f57bb649fb0e6f129b9acaee5f2695899ed` |
| Applicability fact schema | `sha256:694b87b31797467a94d0aaacb5a30c40c3ed259fc66e3811172d1c5e4e243884` |
| Relationship-kind contract | version 2 |
| Horizon provider | `standards-analysis:policy-impact-consumer-horizon`, version 3 |
| Coverage and attestation contracts | version 2 |

Policy, graph, horizon, suite, runtime, generated-contract, and package-test
inputs were frozen before compilation. The horizon digest is identical to the
independently accepted policy-impact v2 horizon. The Milestone 1 comparison and
protected-consumer audit found no unexplained semantic drift or omitted
consumer requiring authority mutation.

## Mechanical Equality

Coverage was compiled through `load_canonical_standards_corpus`,
`compile_policy_impact`, and `compile_coverage`. Canonical set and map
projections produced:

| Projection | Canonical digest | Result |
| --- | --- | --- |
| Active policy-unit subject set | `sha256:890708c49a7dca500f195effd30d8eeb7cdc5608d98251d441de0ed898702f29` | Equal to requirement, attestation, and certificate subject sets. |
| Subject to requirement | `sha256:58338737be13849c8bd8753a1fc85f00e26b3d8a04fb137980f791fbc5ad9cd4` | Every active subject has one current requirement. |
| Subject to attestation | `sha256:1a2217ae8b9d6d24fda38dbe705c9bed7d7d4cc722849ef77ab67c2c9039ecdb` | Every requirement reuses one exact dependency-valid attestation. |
| Subject to generated certificate | `sha256:02b30dcaac84cbf16ebb377b9e8a9da5c827c2aa708c4c3edbd7e5857e746829` | Every attested subject generates one current certificate. |

No attestation was renewed: every authored requirement handle, evidence
reference, conclusion, exclusion set, and auditor provenance remains valid.
Compilation rejects stale, duplicate, extra, or missing attestations; none was
observed. Every attestation is complete, carries repository evidence, and has
an empty explicit-exclusion set.

## Exact Subject Bindings

| Subject | Requirement | Attestation | Certificate |
| --- | --- | --- | --- |
| `profile.boundary.generated-contract.applicability` | `coverage-requirement:sha256:3b80d635c1f83d054ee96101b4b41ec304a487b409d51f3d7ba141eb0ad02985` | `coverage-attestation:sha256:e1255ded868c4d42286de8c33996fcd40c88c17840d56d055b5418ae9cda37c9` | `certificate:sha256:09995b5bd27a47f84a25de616da4a84450bc074e47f2e6d20890334368acf200` |
| `profile.boundary.generated-contract.semantic-closure` | `coverage-requirement:sha256:aa0d7552c58cdfe8d4f122f57b35fde59397f7d2799c04eb92ccc40c408a0638` | `coverage-attestation:sha256:1916014b6fb556a78901c8f6a9f44757d3b64d04f9e1a3621f03effb8278252c` | `certificate:sha256:cf0aac10153799653d77232b11223cf2d851a70eeb7a7269ec0136914445bcee` |
| `router.generated-contract-profile-applicability` | `coverage-requirement:sha256:73513902fc2bd9c11c196649534d445306ae42713ea42c7d77ee72297b12976b` | `coverage-attestation:sha256:16481e915f9de7f0e13c136815fa088bcde803439950fc32f406d63206e3edd1` | `certificate:sha256:fc22e748841ba814bf6979aec7f31aa999cc0a990a0687005f18ce1ee08e584f` |
| `topic.architecture.immutable-authority-closure` | `coverage-requirement:sha256:e471201acb12403dd38da4b3a32cbd53298a282e8e6d4a8ab73685ea593900c5` | `coverage-attestation:sha256:c1c273cc343b8ec629ee6bd70353b09d89477f7b8be9384cc0782ddedf29a894` | `certificate:sha256:014451c6abfc723ed208e65fffa23b5c25847f66831d2d7c982f105e24306cc1` |
| `topic.contracts.generated-semantic-conformance` | `coverage-requirement:sha256:a9867f79341e229bc600913bbec5a7e748638419cb1a7a340b9492e9f8146fa9` | `coverage-attestation:sha256:bbd639dc73ff7fe0515e81cb3cccc6fcbb6419c2b28d307043915b7b792507a0` | `certificate:sha256:b1f80d99c9d504a437830b59c18d34b16e03ad35d56b50f56f778691ba47939a` |
| `topic.contracts.identity-versus-instance-equality` | `coverage-requirement:sha256:ceb4a77c5a7ddbfc697ae2639d1ecd07eeadbb5c621aab0886c048e20ad46762` | `coverage-attestation:sha256:52bd1c6ad3028226927c8cb3885d11114c8fc3c74f389f27db4f3543b5e2eb4a` | `certificate:sha256:3371bf0233d45391265687f2dad689c9047f0568f3650ed2d5f7fd56a0255517` |
| `topic.contracts.schema-dialect-and-vocabulary` | `coverage-requirement:sha256:c8f6c0082c61f7d89c693d3937d9d306cdc2e58e46335eab73012fc9b8420722` | `coverage-attestation:sha256:1edd2c64b722ccb951a09738fc59523b63d96d853b407ad535b3c6703ada0107` | `certificate:sha256:e4abc0102ee80a3bdc731735101d366ff037369d88db27c72ab5ea7f37949da4` |
| `topic.dependencies.implementation-versus-dependency` | `coverage-requirement:sha256:c01424cae2b9ea5db691db525398caf43cc1f48a518037c7eab119ec86f0097f` | `coverage-attestation:sha256:78fb77e40b47255788b87b508cc061b5cdfd8ac7beba7179df37b8d6606b482d` | `certificate:sha256:56b559576af7714569f49b866429015d57a0c5317d541291836b7f083c9a699d` |
| `workflow.commit.branch-context` | `coverage-requirement:sha256:8f865cfe60bd1a1655530b8f8cf2a75a93544e6f696d413bdd4168bd7fc550c2` | `coverage-attestation:sha256:d7a7c89517a13c00d5cd5b9ec383ff145a29f1e09a2a2d66c65e427e83f172fb` | `certificate:sha256:e92d4e026dd113338b171dd56c5a47e1bfdd5852544f45a822eb48bbd834bc34` |
| `workflow.commit.branch-history-review` | `coverage-requirement:sha256:4da57432645c5e65757d815eeaf81867b89d202530aa0e3cc8a361129b0ccded` | `coverage-attestation:sha256:65b548daee7f9fea98c7e176c073ed634a10c3c3db415e0616147bb4d8c49e61` | `certificate:sha256:c96499df616851aabed1e196257f935d8f91459c61c659e7f864dadff296cee2` |
| `workflow.commit.cherry-pick-lineage` | `coverage-requirement:sha256:de5ed6d1e13d372153d9f00563e84d1a64a931f4bc530b05d74985107fae3c82` | `coverage-attestation:sha256:47bc10b92da9ef871b438f4f1237344a31b2b2051ca3273838b46e826995cc2e` | `certificate:sha256:59b9f8de13b61207bb2c268b4ac1ab438b0685b47c2ed942ba9594cd8638bfe4` |
| `workflow.commit.commit-message` | `coverage-requirement:sha256:9415d644357434faf5bd4ed39a00d4c0210c784dc7190cf73764e2b046d3da87` | `coverage-attestation:sha256:a615ea0325a4224cf64e502fb936693c4528282717826215acb03ec39b757ab4` | `certificate:sha256:ee6981057f3698943b73e2547e47d995aafd53bc4d13647f84909cf8cf2a5a94` |
| `workflow.commit.hook-bypass-authority` | `coverage-requirement:sha256:200b8357092f53fa788cdcde92866bdb722807c1831ae73dd23ab6e49b11ceed` | `coverage-attestation:sha256:ee5678682a2a1f3843592cd1cdde18f271bae18aff920d4744e380e80f3e63e3` | `certificate:sha256:7618208243be0c5264744a095ea32985eca000b9acfc7c65c62601ebd608d6b7` |
| `workflow.commit.integration-mechanisms` | `coverage-requirement:sha256:74afaef0578a69c3e22249b0482ec8e67ddb435d7095d36035df9c938e96a632` | `coverage-attestation:sha256:f2958e57ee523b52c194ebd22362ad57f87c9439868bd1eedb48ce4e4c6504d1` | `certificate:sha256:66b0346baad42da73191630fda56500f386ad588457799f80459ab7d7ba4f652` |
| `workflow.commit.invalid-outcomes` | `coverage-requirement:sha256:07102fb5e17a07d2fab3e98b78ad40e545794d6c6fa07009d70e34b9390540bc` | `coverage-attestation:sha256:cfd4b263a5fb9fdf3389575a208848f6540587402b25e2d57848989e5ca21cb2` | `certificate:sha256:b98e3a62fb49f5155a3e2272a4f41287aac72d0204048d10a447e479eed92e0c` |
| `workflow.commit.isolation-applicability` | `coverage-requirement:sha256:a582dc828966b5d1525aa90d50c5faa666a251c06bbf9893224092d0de8b7139` | `coverage-attestation:sha256:8f453218d77721e520589bdd12ba892af8862fcfe9554a8ca6bccebb8bd6a111` | `certificate:sha256:a8478ee6f8fd4ac4ee72533212a05d99580a94e0872d0d68557db0739b856f2b` |
| `workflow.commit.per-commit-boundary` | `coverage-requirement:sha256:cda203fd9b04479bc0cbcbf14f4537e58efd10a2aa8fa2bb8ca9d6b6fa198005` | `coverage-attestation:sha256:a6bc46083aa0d1cab75d4dfda4e1d28b05a6b7b5c96e3d6b839b47119d0f89f7` | `certificate:sha256:21009af47bd32ea8597253c14bfbd36666482d7956a2214b13e2c87e6d072139` |
| `workflow.commit.rewrite-authority` | `coverage-requirement:sha256:b2996059640679c700f5342a846c66ced801b8d3a22ed7b3ff88e8f6e640b12f` | `coverage-attestation:sha256:88011e71892c00f14fadec037c34472e4fe0207b27ef4f77bced652d538fc537` | `certificate:sha256:57a7e00b527a38553efb0fa848d5f17347d16608ab782ff8cc11c835ee39b94a` |
| `workflow.commit.terminal-branch-lifecycle` | `coverage-requirement:sha256:11c699bc52751b7111a04e8f251f587c0600ebd426018dc58acefc9ce83afed0` | `coverage-attestation:sha256:7d2178f0195472c66471f0c4d210b83276573a17ae19e748b12a048a3c0a367f` | `certificate:sha256:f0c7287bed3c1e8cffee99f0d7697d213de980409b584861e5f4c604171766f8` |
| `workflow.commit.topology` | `coverage-requirement:sha256:4f2ce7f65d1400a7add49937adf1d359ad13692798e8b1ddd70fcf9133e758fd` | `coverage-attestation:sha256:bd5ccd53e04ce4aba399242fda66e7ef2fbbebd8adc3ae4f2fd87f27d083325b` | `certificate:sha256:df93e610fa746706dc49c1e0d2134925b03a8bba25a68f8e99aa2c7dcac9468d` |
| `workflow.commit.worktree-lifecycle` | `coverage-requirement:sha256:12f0e5fdc4b9b160efe05fb9251f31a25b6a911b92dc4e29f94258b8d3bcec08` | `coverage-attestation:sha256:434f56459280227b7304779de11fcf01466cc2ecbb82a74e7a902ba545e7dc6c` | `certificate:sha256:01109a94332b3ab5d0ef5e58c4bdfbf6208b0fbc7709cd01bd12ad54b07577fe` |
| `workflow.planning.acceptance-claims` | `coverage-requirement:sha256:7672a1578a80339960c163bdb6dce0b674e969b6d48b6a5b92db70781696af80` | `coverage-attestation:sha256:20623378bd8310eccd45f5f8f1d162b4631d9a371258d62bec7220ebcd039ca7` | `certificate:sha256:7fb724f5dc2c9810bee5a5b257bfb00d8b660a4f302e976c19625599e29b163e` |
| `workflow.planning.active-plan-fields` | `coverage-requirement:sha256:19b5034dcb60e95c86213102449c0e5df96fa5a03ca036cb9bd58a5bbe463c9c` | `coverage-attestation:sha256:9f04385bd8ba0416b749244391beb6d5e66ac79ff3228764bd3b08e82c8e3a98` | `certificate:sha256:c07fd37ca4efe0eaea597bdd7f9cecd02255eb630556dad1066bb8733d0808b3` |
| `workflow.planning.artifact-model` | `coverage-requirement:sha256:540fd5792d6784bf61185f926c79b266d40fc08229d3839c444af1fd50c64e20` | `coverage-attestation:sha256:34e930100f3f028f8475f2641f42c6aa4ddf34c6e9fdea64569d23f097057ac6` | `certificate:sha256:aee09d8df20c0f48e8b368343a087df3646ce86b79aa09945472a7194384cc86` |
| `workflow.planning.completion` | `coverage-requirement:sha256:736ed52f9862426f784b08f708c0f3c2878b017480a2bc1dc2434689832ce005` | `coverage-attestation:sha256:69e1e3f1fd00b654b32c4add04daa641d015454235e45bb7b99cf0e8f28c6bb1` | `certificate:sha256:62d0d7ea26618d9f6b5d881aadadeadbd21867e7f25ad1d4bd19b403d1b51793` |
| `workflow.planning.concurrent-integration-routing` | `coverage-requirement:sha256:e39cf684de6e6075e0792237e0edb0129eb91c674f16df394b2f6b3af6796716` | `coverage-attestation:sha256:378823315a3696f42f573b2054303564b9d0ebbdb141939b6b31377338892859` | `certificate:sha256:73cd9d3aafa657e8085b5e6f5c5c3aa854e97615d0ff13c368afe096bb85b648` |
| `workflow.planning.concurrent-work` | `coverage-requirement:sha256:08fb9f62a563ea047812eb5a635f774c00ca593d4933e2a52b12a697989deccd` | `coverage-attestation:sha256:4b8b83d23dd2c1e6f8d9028c2751acabd140493161da823bf2f1ae658847438b` | `certificate:sha256:884d9757c7fa8cfd19b4db5c9bea36c28a1fc5d922cdf8219b8ef874e2bc0bc8` |
| `workflow.planning.current-state` | `coverage-requirement:sha256:4e4e415920e2bf43189424950107a8eb287c1921d4260bcdd627bbd0165f5f41` | `coverage-attestation:sha256:1b94f27387a0ae2198d1d9e29f1db6c80a77bf623b88aef078524312eae776cf` | `certificate:sha256:2a1aa5bb8653035504f41b162644f446d43115fd9ba0406aec056a29ae6ddd22` |
| `workflow.planning.findings` | `coverage-requirement:sha256:52aa2d15d9e65d72ad357d099c88e5b798ee949178144d8db9ab1c81afeb456b` | `coverage-attestation:sha256:5c478c31a5186a5dbb043aa4fc77775419de6e7d78766083f2d1bf52e8bda48e` | `certificate:sha256:fe2c3455cc393c37b99c22bd1ca014b1a72053dc062b3c4ede2feaa7099ee152` |
| `workflow.planning.lifecycle` | `coverage-requirement:sha256:c5ed3424fc3db4ea9514666169e2fccbef2f3a5d55899be5c6eca9be18ee52b5` | `coverage-attestation:sha256:90108aa56f40e085234ca6fcdc4e0fbc817f55e062f7db16ba781bd87d06bb1a` | `certificate:sha256:754d85fe93083df94695cfe9b512c6a9eeef2cc57fb55c8e12b3a1774790f025` |
| `workflow.planning.milestones-and-slices` | `coverage-requirement:sha256:e38e0a0e40066b56522d57b2878ead8c7c32b6cb80bd45dd1688b44da82dd400` | `coverage-attestation:sha256:557def1a8bc14c4a5c94097cd2127b620d29a4185fdf51351ed7dbe577dd58da` | `certificate:sha256:3677f1a1e61635be9c877ed634a0115f1d90bd5c8f6ab2bb571e63babc38574f` |
| `workflow.planning.plan-admission` | `coverage-requirement:sha256:49a6fd0f98527aa492e96407bc35e951e2a0a09ec5c5aa4776392f00cb041b99` | `coverage-attestation:sha256:c6c161cff6c0e62f2534e270666d96ebb47c709854af4550703a3788e6460591` | `certificate:sha256:643ef48d6727bf853f1bb6380e17250e1bd13eed4457cc146da7715eba44f571` |
| `workflow.planning.projection-completeness` | `coverage-requirement:sha256:2bba3dbe129b609ca28f66f9a216bbefbe8cee55f82f7ff5f7247d32d10fa28b` | `coverage-attestation:sha256:ff0236e8c168cc0a06284100dc442bf7f6b9753b8c9058c67ecdcff137f877c2` | `certificate:sha256:704c8bc89050bbe0109a4f6b07bb3992ea452541a4c8532eb44c8831ce1fa2ef` |
| `workflow.planning.replanning` | `coverage-requirement:sha256:606f14b44dbf9df67a206350122208be532ef6cd603248c6a534a37891643b3a` | `coverage-attestation:sha256:804a905dc4d213496937dc9da6fe0ac132ac9108469e22a3a580191270256a3f` | `certificate:sha256:d7873571bea5fbd674a9664dbc508b8797e0d6004e3fd90d1ebd67aa14304435` |
| `workflow.planning.repository-isolation` | `coverage-requirement:sha256:307b6ef26f70d9a985ba0363ad61d01c6786d989bcb1a404687af494a9ea3994` | `coverage-attestation:sha256:3b04f4d684b934f570db45b59608019b523a143314444f30008f1ac09b7b78f5` | `certificate:sha256:c7e8aa5efb24e0adb955ad2468b5545a985ba28a6e4442130e78a959a9f90160` |
| `workflow.planning.systemic-finding-replan` | `coverage-requirement:sha256:0a0b4acd80d7fd84be94913d3fdb253fb8e93e6d227c1519906cd4d29faaf70b` | `coverage-attestation:sha256:636ddbdb85e2eb41fc31f9afc23ee10207de56d598db57302588fbf183b83ad3` | `certificate:sha256:9d5635d1fc062ad8bba0d14905c5264c8446f321ec1dfd8d55c9e23bb31c66b7` |
| `workflow.planning.written-plan-applicability` | `coverage-requirement:sha256:9b589e307eca2f7e2bcaddd9931dbf872017fb16ac8bd04e1843be13bc7c6ba7` | `coverage-attestation:sha256:e176fdeeb671872ccfb6bf4f96ff14fdf404d232c23cddee5f35e7bc0946f97d` | `certificate:sha256:566d872034835254993ca70ba23fa70c1a9dabde421ad8e415d92120f4a63eb7` |
| `workflow.verification.acceptance-claims` | `coverage-requirement:sha256:a1a8e579df5b91ab84750e9cc222de70a37fd3cbb11236cf89c858704e576aa7` | `coverage-attestation:sha256:9a33dc83eeccfa3a8fcd5a0304b5885e05737c15ef994466503443051b02c41f` | `certificate:sha256:dd22ef168fa6b78e4d9491420bb76fe7fd66a68619c88dcc219919f65a25a417` |
| `workflow.verification.differential-evidence` | `coverage-requirement:sha256:5ca30a8aba98f4c31525f2df1b99467d93981ff1dca5251feca59d0b70e69eec` | `coverage-attestation:sha256:8a3e406de8a9e9b31a8bc1950172cab8323f402c5a1f2688cfe51f8cbfc0f030` | `certificate:sha256:2c9243ac3135f11a5c22af6dd3dc766ab5d302e12f9d1089d6d2b8acd179e487` |
| `workflow.verification.evidence-oracle-boundary` | `coverage-requirement:sha256:05e1a248dba4a77381f8fc4a4c696b263f128e81ece5790c194e9513a3af6ea9` | `coverage-attestation:sha256:2c71901b9f9cbf3259936d4fe55efc5e3c9934fa6baafa8c2b0dc6b0851957db` | `certificate:sha256:902e27c5dab9a4f97180c40db96c977a3e43b835a445a61f23d45a34dea99cca` |
| `workflow.verification.negative-fixture-isolation` | `coverage-requirement:sha256:52fef9943d995829caba5b72d653a3dae9038a055d0e78356fced08714f77b78` | `coverage-attestation:sha256:612e0872f0a7f3f4456d9d7f2a72a637c732662a70a3fc2716adef34e02cd470` | `certificate:sha256:8bc59760048abd0ea0e4fe3cb9d88041f62bc1717d1aa4a8efcac8ac0cb6baa3` |

## Consumer And Horizon Result

The Milestone 1 protected closure and disposition report remains the authority
for selected-consumer decisions. Its exact `W union R` projection has one
non-blocked disposition per mapped consumer. Coverage compilation independently
binds the provider-v3 horizon and every member fingerprint; the unchanged
horizon plus the accepted independent audit exposes no missing consumer class.
No graph edge or empty impact result is used as proof of completeness.

The equality above remains exact for candidate
`7a54d5fe7778f481278e4f21a12863d2f261b280` but does not accept the standards
recovery. The admitted semantic-oracle repair will change two registered
horizon inputs, so final coverage must be recompiled after those inputs freeze
and before replacement-candidate verification.
