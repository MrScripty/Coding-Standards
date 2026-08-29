# Standards Engine A1 History And Design

**Status:** Historical research complete for AUD-A1

**Scope:** A1 formation, design, implementation, repair history, accepted
boundary, later policy-impact-v2 amendment, effective standards snapshots, and
the fairest comparison boundaries for the A1/A1b audit.

## Citation And Interpretation Method

This report uses repository-owned primary sources only: Git commit objects,
contemporaneous plans, ADRs, reports, source, schemas, and tests. A citation of
the form `COMMIT:path` means the file exactly as stored in that immutable
commit. `COMMIT (commit object)` means the commit subject and body are the
source. Short commit IDs below are unique in this repository; exact boundary
hashes and trees are written in full.

The report labels conclusions as follows:

- **Fact** is directly established by a cited repository artifact or Git
  object.
- **Contemporaneous rationale** is the reason recorded at the time; it is not
  automatically an objective explanation of every consequence.
- **Inference** is this audit's interpretation of the recovered evidence.
- **Unresolved** means the repository evidence does not decide the question.

Raw line, export, version, package, and test counts are diagnostic evidence.
They do not by themselves establish good design, excessive complexity, or
redundant verification.

## Executive Findings

### Fact

A1 was conceived as a read-only, agent-facing Standards Engine that would let a
caller route, read, navigate, compare accepted and proposed standards
snapshots, and iteratively resolve impact work without supplying repository
paths. Controlled authoring, repository mutation, semantic acceptance, and
external-project baselines were deliberately excluded. The admitted design
used four public operations—`query`, `prepare`, `resolve`, and `inspect`—over
explicit snapshot and analysis handles. (`c7d23dfa:docs/plans/standards-engine-navigation-analysis/plan.md`,
Objective, Scope, and Constraints;
`c7d23dfa:docs/plans/standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md`,
sections 1–3 and 8)

The exact accepted A1 implementation is commit
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`. The later acceptance commit
`933c9ab93d18ede987d449a6fe7b9ebd313922fc` records review authority but is not
the implementation content. (`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`)

A1 was accepted only after two withdrawn acceptances and five rejected repair
candidates. Those reviews found live-worktree reads behind immutable handles,
incomplete generated contract semantics, cold reconstruction dependent on
fresh execution authority, public/domain result leakage, JSON Schema semantic
mistakes, internal package imports, and incomplete test oracles. The final
review reported zero Standards and specification findings for Repair VI.
(`933c9ab9:docs/plans/standards-engine-navigation-analysis/execution-ledger.md`,
entries “A1 Acceptance Reopened” through “Plan A1 Accepted”;
`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-vi-candidate.md`)

The accepted v9 implementation still contained a known-later defect: its local
validator and generated decoder used NFC-normalized identity serialization as
the equality oracle for JSON Schema `const`, `enum`, and `uniqueItems`. The two
local paths agreed, but their Unicode decisions disagreed with the declared
Draft 2020-12 instance-equality contract. This was identified immediately
after A1 acceptance and later reproduced from the exact accepted tree.
(`3439aae9:docs/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`,
sections 3 and 4.3;
`c4408363:docs/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`)

Policy-impact authority v2 then amended A1 prospectively. Its accepted source
candidate is commit `7bc8bd070f882eb9779dc678139777d05a6ce7c7`, tree
`35a22f824f7ed5f50347032b956b2108fc073f77`; independent acceptance is recorded
at `bf9f3d86`, and the plan lifecycle transition at `dd571976`. It advanced the
public contract from v9 to v10, consolidated catalog, relationship,
compatibility, graph, coverage, and inspection ownership in
`standards_policy_impact`, and explicitly retained the rest of A1 and its
historical v9 acceptance. (`dd571976:docs/plans/standards-engine-policy-impact-authority-v2/plan.md`;
`bf9f3d86:docs/plans/standards-engine-policy-impact-authority-v2/reports/prerequisite-acceptance.md`;
`7bc8bd07:docs/decisions/standards-engine-policy-impact-authority-v2.md`)

### Inference

A1's strongest design decision was its external product shape: one read-only
Module with a four-operation Interface, explicit uncertainty, explicit handles,
and no mutation authority. Its single immutable `AnalysisState` also removed
three competing lifecycle identities and hidden mutable supersession. Those
decisions gave substantial external Depth and should not be conflated with the
supporting machinery that later failed. Evidence for this distinction appears
in both the accepted A1 ADR and the later A1b brief, which explicitly said the
central product architecture was worth preserving.
(`2359a987:docs/decisions/standards-engine-navigation-analysis.md`, Public
Interface and State, Authorization, and Completion;
`3439aae9:docs/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`,
section 2)

A1's weakest design decision was treating one declaration authority as if it
were one executable semantic authority. The schema, custom validator,
generator, generated decoder, identity serializer, internal domain models,
public adapters, renderer, examples, and tests had to remain synchronized. The
repair sequence is direct change-history evidence that this arrangement had
poor Locality even though it had a single named schema owner. The later
standards-recovery brief reached the same root-cause conclusion
contemporaneously after A1. (`3439aae9:docs/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`,
sections 2 and 4.1–4.6)

The policy-unit coverage and immutable-analysis machinery solved real stated
requirements—unknown applicability, successful empty impact, replay,
authorization, exact completion, and cold inspection—but the history does not
show that each requirement came from an independent external consumer. It
shows that the plan required them. Their necessity for A1c therefore remains a
product-requirement question, not a fact established by A1's successful tests.

## Fair Comparison Boundaries

No single A1 commit answers every comparison question. The audit should use
the following explicit boundaries.

| Use | Commit and tree | Why it is fair | What it must not be used to claim |
| --- | --- | --- | --- |
| Primary historical A1 implementation | `2359a98740b6035a0414bfaf5427ceaa1301a1c8`; tree `97c850ab718287007c1e1daac538f40869f71a1d` | This is the implementation that A1's final independent review accepted, after all recorded A1 repairs. It preserves the actual v9 design and test portfolio. | It is not the last A1-derived runtime before A1b, and it does not contain the later standards recovery or policy-impact v2. |
| Acceptance authority | `933c9ab93d18ede987d449a6fe7b9ebd313922fc`; implementation tree remains `97c850ab…` | This commit closes objectives and records independent review. | Its documentation-only tree `bffc59d2…` is not the A1 implementation tree. |
| Accepted post-A1 runtime amendment | `7bc8bd070f882eb9779dc678139777d05a6ce7c7`; tree `35a22f824f7ed5f50347032b956b2108fc073f77` | This is the exact accepted policy-impact-v2 source candidate. It represents A1 v10 after the later authority correction. | It must not replace v9 when asking what the original A1 plan produced under its original standards snapshot. |
| Final accepted recovery repository before A1b planning | `c4408363752b10060f631247f3e2f1fa26eae003`; tree `84477150bd368a168dd04da3770de55c23bbb817` | This is the accepted standards-recovery transition immediately before the A1b plan. Relative to `7bc8bd07`, A1 production source is unchanged and only two engine test files add exact semantic-cause assertions. | It is a repository/standards/test posture, not a separately reviewed A1 runtime implementation. |
| Formation and design evolution base | `c7d23dfa55a9558b929e6b838d7ea0563981a1ef`; tree `5e9c4eb211ee0a67039b0ec11142db9b106243ae` | This commit admitted the original architecture, schema, brief, plan, and implementation base before runtime work. | It is not a completed implementation. |

Sources: `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`;
`bf9f3d86:docs/plans/standards-engine-policy-impact-authority-v2/reports/prerequisite-acceptance.md`;
`c4408363:docs/plans/standards-engine-standards-recovery/reports/standards-recovery-acceptance.md`;
the named Git commit objects.

### Boundary recommendation

**Inference:** Architecture and behavior comparisons should report both
`2359a987` and `7bc8bd07`: the former answers “what did accepted A1 design and
build?”, while the latter answers “what A1-derived runtime existed after its
accepted pre-A1b amendment?”. Verification-history comparisons may additionally
use `c4408363`, provided the report identifies the two added test files rather
than calling that tree another A1 implementation.

`396144ad`, previously used informally as an A1 baseline, is unsuitable as the
sole historical A1 boundary. It contains the v10 runtime, later standards
recovery, A1b C1–C3 planning, and one post-v2 engine-test correction. It is
useful as a “state immediately before A1b implementation planning progressed”
snapshot, but it mixes authorities not present when A1 was designed or
accepted. Git shows that the only A1 package changes from `7bc8bd07` through
`396144ad` are `tools/standards_engine/tests/test_analysis.py` and
`test_navigation.py` at `c6fc663b`; no A1 production file changed.
(`c6fc663b` commit object; `git diff 7bc8bd07..396144ad -- tools/standards_*`)

## Origin And Problem Statement

### Historical precursor

**Fact:** The navigation-analysis work emerged from a verification-engine
design audit. That audit found that canonical module discovery lived in
`standards_verifier`, graph coverage depended on verification-suite
registration, fourteen of forty-four canonical modules were absent from the
queryable graph at the revalidated revision, and the repository lacked a
neutral metadata owner suitable for verification, graph queries, and future
agent navigation. It recommended completing routing and graph visibility,
restoring small policy-independent engine Interfaces, and separating generic
mechanics from policy and migration lifecycle.
(`c7d23dfa:docs/plans/standards-verification-engine/reports/python-engine-standards-design-audit.md`,
Historical Executive Conclusion, SW-01, SW-02, and Audit Guardrails)

The same audit explicitly deferred verification-oracle fitness. Its later
M6-I71 example showed a text assertion rejecting Markdown line wrapping even
when the rendered sentence was unchanged. A1 therefore began with an already
known but out-of-scope warning that passing checks did not necessarily prove
the semantic claim attributed to them. (`c7d23dfa:docs/plans/standards-verification-engine/reports/python-engine-standards-design-audit.md`,
Subsequent Scope Limitation: Verification Oracles)

The A1 brief framed Coding Standards as a selectively read knowledge system:
agents should describe work through typed facts, discover standards without
repository paths, retrieve canonical authority, navigate declared relations,
expose uncertainty, and receive a bounded change-analysis work queue. It did
not propose automated judgment of arbitrary prose meaning.
(`c7d23dfa:docs/plans/standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md`,
sections 1 and 2)

### Admission precondition

A1 planning waited for the verification-engine M6-I72 recovery boundary at
commit `13a9f48b95ed7532f480e4604d9dfa23443e8f43`, tree
`c27a1e2bbf52244c5b30eb1d21381be6e5c86d68`. That recovery preserved the
M6-I71 oracle defect as future work rather than silently treating it as solved.
The A1 formation commit `c7d23dfa` is the direct child of that recovery.
(`c7d23dfa:docs/plans/standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md`,
section 4; `c7d23dfa` commit object)

### Product split

**Contemporaneous rationale:** A1 separated navigation/read-only analysis from
controlled authoring because mutation, acceptance, application, authorization,
rollback, and recovery required a stronger lifecycle. The ADR also rejected a
custom command-string language: typed Python and structured agent-tool
messages would be authoritative, with text only a derived human projection.
(`2359a987:docs/decisions/standards-engine-navigation-analysis.md`, Public
Interface and Considered Options)

**Inference:** This split decreased machinery inside the initial product by
preventing session heads, compare-and-swap authoring state, write recovery, and
application authority from entering A1. It also made the later single-state
correction possible: mutable head semantics could remain an A2 concern rather
than being preserved for compatibility.
(`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-packet-supersession-replan.md`)

## Chronological A1 Commit Record

The table covers every material commit from formation through final A1
acceptance. Documentation publication commits are retained where they mark a
review candidate or lifecycle decision.

| Date | Commit | Recorded event | Historical significance and source |
| --- | --- | --- | --- |
| 2026-08-22 | `c7d23dfa` | Admit navigation-analysis contracts | Added the brief, active plan, ADR, canonical schema v1, examples, identity fixtures, and custom validator before runtime implementation. `c7d23dfa` commit object and `c7d23dfa:docs/plans/standards-engine-navigation-analysis/reports/milestone-0-architecture-contract-review.md`. |
| 2026-08-22 | `3383ec68` | Admit metadata cutover | Recorded `c7d23dfa` as the implementation base and froze the neutral metadata consumer inventory. `3383ec68` commit object. |
| 2026-08-22 | `3e8aae87` | Centralize canonical metadata | Introduced `standards_metadata`, switched inventoried production consumers, and removed the verifier-owned loader without fallback. `3e8aae87` commit object; `3e8aae87:docs/plans/standards-engine-navigation-analysis/reports/milestone-1-neutral-metadata-cutover.md`. |
| 2026-08-22 | `8edbc46e` | Add snapshot and policy identity | Added clean-Git, dirty-Git, and non-Git snapshot identities plus stable policy-unit declarations, locators, and distinct representation/structural/semantic identities. `8edbc46e` commit object; `8edbc46e:docs/plans/standards-engine-navigation-analysis/reports/milestone-2-snapshot-policy-unit-foundation.md`. |
| 2026-08-22 | `3fe09812` | Centralize standards graph projection | Created the neutral `standards_graph` Adapter shared by analysis and verification; removed verifier ownership of canonical metadata edges. `3fe09812` commit object; `3fe09812:docs/plans/standards-engine-navigation-analysis/reports/milestone-2-standards-graph-ownership-replan.md`. |
| 2026-08-22 | `bbbab878` | Add typed navigation façade | Implemented snapshot-bound read, related, and inspect behavior over module and policy identities without caller paths. `bbbab878` commit object; `bbbab878:docs/plans/standards-engine-navigation-analysis/reports/milestone-2-read-related-inspect.md`. |
| 2026-08-23 | `5849ffd4` | Add typed Router projection | Added a reviewed executable Router projection and three-valued applicability rather than parsing Router prose or hardcoding policy in Python. `5849ffd4` commit object; `5849ffd4:docs/plans/standards-engine-navigation-analysis/reports/milestone-2-router-projection-replan.md`. |
| 2026-08-23 | `60afb3e4` | Reconcile rewritten lineage | Recorded a repository-owner-authorized reword-only rewrite. Original commits `8b632df4` through `ca3dda6f` map to `c7d23dfa` through `5849ffd4`; every tree stayed identical. `60afb3e4:docs/plans/standards-engine-navigation-analysis/execution-ledger.md`, Commit Message History Reconciliation. |
| 2026-08-23 | `4d4e4d05` | Classify and traverse policy impact | Implemented modification/addition/removal classification and accepted/proposed graph-union selection, but stopped before obligations because relationship semantics lacked typed authority. `4d4e4d05` commit object; `4d4e4d05:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-change-classification.md`. |
| 2026-08-23 | `8203576a` | Admit compiled policy impact | Replaced the proposed edge-keyed sidecar with a compiled source-owned policy-impact authority, added fact-free `always`, and planned migration of 39 relationships. `8203576a` commit object; `8203576a:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-policy-impact-applicability-replan.md`. |
| 2026-08-23 | `7df157aa` | Establish corrective green base | Reconciled current producers with the versioned policy-impact/applicability contract before the compiler cutover. `7df157aa` commit object. |
| 2026-08-23 | `f9496cb3` | Compile policy-impact authority | Added `standards_applicability`; compiled source declarations into graph topology and typed semantics; removed former manifest/parser authorities. `f9496cb3` commit object; `f9496cb3:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-applicability-policy-impact-cutover.md`. |
| 2026-08-23 | `c6f9b44b` | Replan policy-unit sources | Replaced module-source relationships and report-dependent coverage with heading-scoped policy units and reusable certificates; reviewed 39 mappings and 28 policy-unit baselines. `c6f9b44b` commit object; `c6f9b44b:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-policy-unit-source-replan.md`. |
| 2026-08-23 | `3873a404` | Cut impact sources to policy units | Moved policy-unit loading to metadata, graph projection to `standards_graph`, remapped declarations, and removed the analysis-owned loader. `3873a404` commit object; `3873a404:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-policy-unit-source-cutover.md`. |
| 2026-08-23 | `ee940a91` | Add reusable consumer coverage | Split complete analysis snapshots from narrower coverage views, added an independent horizon, requirements, attestations, and certificates, and removed legacy audit flags. `ee940a91` commit object; `ee940a91:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-coverage-identity-cutover.md`. |
| 2026-08-23 | `049bfce5` | Require unmapped normative review | Added mandatory whole-artifact obligations for changed normative content outside exact policy-unit scopes. `049bfce5` commit object; `049bfce5:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-unmapped-normative-obligations.md`. |
| 2026-08-23 | `b7d1e243` | Preserve unknown impact | Kept three-valued unknown outcomes and introduced fact requirements rather than coercing missing facts to false. `b7d1e243` commit object; `b7d1e243:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-unknown-applicability.md`. |
| 2026-08-23 | `211df1dc` | Require certified empty impact | Made missing coverage an obligation even when no consumer relationship was selected. `211df1dc` commit object; `211df1dc:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-empty-impact-coverage.md`. |
| 2026-08-23 | `97df0903` | Complete lifecycle selection | Added move, split, merge, reciprocal tombstone, and accepted/proposed context behavior; initially accepted Milestone 3. `97df0903` commit object; `97df0903:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-lifecycle-impact-selection.md`. |
| 2026-08-23 | `c9197165` | Add immutable packet foundation | Added pending packets, typed submissions, deterministic work, and next-operation projection. `c9197165` commit object; `c9197165:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-packet-foundation.md`. |
| 2026-08-23 | `50043a5b` | Recover missing consumer obligations | Reopened incomplete Milestone 3 because definite impact candidates never became consumer-review obligations; introduced plural reasons and coordinated identity/version changes. `50043a5b` commit object; `50043a5b:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-consumer-obligation-recovery.md`. |
| 2026-08-23 | `4baa6311` | Compile plural reading plans | Preserved multiple Router, dependency, and consumer causes; narrowed the coverage projection and renewed 28 coverage attestations. `4baa6311` commit object; `4baa6311:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-reading-plan-recovery.md`. |
| 2026-08-24 | `94b295b4` | Adopt single-state lifecycle | Replaced packet, report, hidden-session, and global-supersession authority with one immutable `AnalysisState`/`AnalysisHandle`; added state stores and cold reconstruction. `94b295b4` commit object; acceptance report added at `e61e9567:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-single-state-acceptance.md`. |
| 2026-08-24 | `e61e9567` | First A1 acceptance | Accepted `94b295b4`, tree `ff032da5…`; later withdrawn after audit. `e61e9567` commit object and the later withdrawal in `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-single-state-acceptance.md`. |
| 2026-08-24 | `51dcd258` | Repair snapshot and public contract | Captured immutable content, advanced the Interface to v9, added schema generation/freshness, bound continuations, expanded inspection, and reopened acceptance. `51dcd258` commit object. |
| 2026-08-24 | `b8f52240` | Second A1 acceptance | Accepted `51dcd258`, tree `f8d028e8…`; later withdrawn when SENA-022 reproduced further defects. `b8f52240` commit object; `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-acceptance.md`. |
| 2026-08-24 | `714ba23f` / `b3c80285` | Repair II implementation/candidate | Fixed whole-module inspection, cold child reconstruction, schema traversal, facade decoding, and plan parsing. Review rejected omitted numeric/result semantics and fresh-authority-dependent reconstruction. `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-ii-candidate.md`. |
| 2026-08-24 | `8ed8ba0b` / `70166d32` | Repair III implementation/candidate | Generated the complete input/result closure and state-bound reprojection. Review rejected Python equality, wrong regex semantics, domain results crossing the public Interface, and invalid negative fixtures. `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-iii-candidate.md`. |
| 2026-08-24 | `3d389dd7` / `21147efe` | Repair IV implementation/candidate | Corrected type-sensitive const/enum behavior, regex search semantics, public result adaptation, and intended plan diagnostics. Review rejected duplicate canonical comparison, `uniqueItems` equality, and substring-only evidence. `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-iv-candidate.md`. |
| 2026-08-24 | `e7e0e1e2` / `c3d3bda8` | Repair V implementation/candidate | Unified local equality through the metadata canonical serializer and made plan diagnostics exact. Review found an internal package import and incomplete const/enum differential matrix; runtime behavior was otherwise recorded as correct. `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-v-candidate.md`. |
| 2026-08-24 | `2359a987` / `85485404` | Repair VI implementation/candidate | Switched generated code to the public metadata entry point and completed Boolean/integer plus Unicode differential cases. `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-vi-candidate.md`. |
| 2026-08-24 | `933c9ab9` | Final A1 acceptance | Independent review accepted `2359a987`, tree `97c850ab…`, with zero Standards and specification findings and closed A1/A2 sequencing. `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`. |

### Complete acceptance and repair-boundary inventory

This inventory prevents a documentation commit from being mistaken for the
implementation it reviewed and preserves every withdrawn or rejected tree.

| Boundary | Implementation commit | Exact implementation tree | Final historical disposition | Principal later finding |
| --- | --- | --- | --- | --- |
| Initial single-state acceptance | `94b295b40bc1cef9a6281355d68115f3a98ed112` | `ff032da51fcaff45533c07daa8de464065b8e55c` | Accepted by `e61e9567`, then withdrawn | Snapshot-bound module reads could reach live bytes; generated/public/inspection and acceptance projections were incomplete. |
| Boundary Repair I | `51dcd258942b0774c73ae8b620227c7ce34d1129` | `f8d028e887f4061a1d03ad6e75b9776a5fc3966b` | Accepted by `b8f52240`, then withdrawn | Whole-module inspection still leaked live state; cold child artifacts and schema-owned types/results were incomplete. |
| Boundary Repair II | `714ba23fb5186b549ab44865d36c77509dbf654a` | `d5fa6ceed1aa35ec83fe1073f0c0a8818658cc1b` | Rejected | Numeric constraints and concrete generated results were omitted; cold projection used fresh execution authority; plan/ADR evidence was inconsistent. |
| Boundary Repair III | `8ed8ba0beba5dd16c0a2da50655952842ab61c85` | `eaeac78739468fc2c79241f6a7830e54986d2f95` | Rejected | Python const/enum equality, full-match regex, domain result classes, and invalid negative fixtures diverged from the claimed Interface. |
| Boundary Repair IV | `3d389dd7f73f48c21d80570331c8058737f941db` | `6fcbfed114dcfd768186f8610c0792e220657b32` | Rejected | Equality remained independently implemented; `uniqueItems` and Unicode/Boolean cases disagreed; the diagnostic oracle matched fragments. |
| Boundary Repair V | `e7e0e1e20762f994e644f2e3c88d017d1625266c` | `22c263b4f30c706b94ce3125c8f0537e5d210fe6` | Rejected | Generated code crossed an internal metadata seam and const/enum evidence omitted Boolean/integer cases. |
| Boundary Repair VI | `2359a98740b6035a0414bfaf5427ceaa1301a1c8` | `97c850ab718287007c1e1daac538f40869f71a1d` | Accepted by `933c9ab9` | Independent review reported no remaining Standards or specification finding; later standards recovery separately found the Draft equality nonconformance. |

Sources: the candidate and acceptance reports at
`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/`, plus
`933c9ab9:docs/plans/standards-engine-navigation-analysis/execution-ledger.md`.

## Post-Acceptance Discovery And A1 Amendment

| Date | Commit | Event | Significance and source |
| --- | --- | --- | --- |
| 2026-08-24 | `3439aae9` | Record A1b redesign brief | Preserved the accepted A1 record but identified declared-dialect equality nonconformance, incomplete semantic ownership, ambient authority risks, porous public results, incomplete oracles, and missing routed standards. `3439aae9:docs/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`. |
| 2026-08-24 | `7a571ed2` | Implement normative standards recovery | Changed Router, Architecture, Contracts, Dependencies, Planning, Verification, and added the Generated Contract profile and stable policy units. `7a571ed2` commit object and changed paths. |
| 2026-08-25 | `0a7fb2da` | Compile recovery projections | Added executable fixtures, suites, prompts/template projections, and policy-impact declarations for the recovered standards. `0a7fb2da` commit object. |
| 2026-08-25 | `cbc53cfb` through `95cb97ba` | Plan and repeatedly admit policy-impact v2 | Replaced a Router-local repair with a systemic policy-impact authority plan; its exact governance chain and supersessions are retained in the plan header and ledger. `dd571976:docs/plans/standards-engine-policy-impact-authority-v2/plan.md` and `execution-ledger.md`. |
| 2026-08-25 | `9bbc1e05` | Implement policy-impact-v2 cutover | Consolidated internal authoring, artifact kinds, compatibility, graph, semantics, public v10 closure, and unsupported-v9 behavior. This was Milestone 0, not final acceptance. `9bbc1e05` commit object; `9bbc1e05:docs/plans/standards-engine-policy-impact-authority-v2/reports/authority-cutover-candidate.md`. |
| 2026-08-25 | `101001bd` | First certified v2 candidate | Certification and tests passed, but independent review later rejected ineffective per-kind evidence booleans, raw verifier failure leakage, malformed optional handling, and incomplete sampled compatibility evidence. `dd571976:docs/plans/standards-engine-policy-impact-authority-v2/execution-ledger.md`, Exact-Candidate Acceptance Rejection. |
| 2026-08-25 | `7bc8bd07` | Corrected v2 source candidate | Replaced nine ineffective booleans with one effective registered-suite rule, tightened decoding/translation, derived the compatibility matrix, and renewed coverage after the corrected freeze. `7bc8bd07:docs/plans/standards-engine-policy-impact-authority-v2/reports/prerequisite-recovery-candidate.md`. |
| 2026-08-25 | `bf9f3d86` / `dd571976` | Independent acceptance and transition | Accepted `7bc8bd07`, tree `35a22f82…`, with zero findings; plan became Accepted. `bf9f3d86:docs/plans/standards-engine-policy-impact-authority-v2/reports/prerequisite-acceptance.md`; `dd571976` commit object. |
| 2026-08-25 | `c6fc663b` | Strengthen semantic-cause evidence | Added exact compiler/graph-derived semantic-cause assertions to two engine test files without production changes. `c6fc663b` commit object. |
| 2026-08-26 | `c4408363` | Complete standards recovery | Accepted the recovery repository state; A1b planning became eligible, while no A1 production source changed after `7bc8bd07`. `c4408363:docs/plans/standards-engine-standards-recovery/reports/standards-recovery-acceptance.md`; `c4408363` commit object. |

## Effective Standards Snapshots

### Original A1

**Fact:** The formation commit `c7d23dfa` is based directly on
`13a9f48b`. No normative standards document changed between that parent and
accepted implementation `2359a987` or final acceptance record `933c9ab9`.
The A1 plan itself routed Core/Router, Planning, Implementation, Verification,
Documentation, Tooling, Commit, Architecture, Contracts, Diagnostics,
Security, Cross-Platform, and Persistence. It explicitly declined Performance
because it made no performance claim. (`c7d23dfa:docs/plans/standards-engine-navigation-analysis/plan.md`,
Routed Standards; Git path comparison `13a9f48b..933c9ab9`)

The later A1b brief found that this route omitted Build despite generators,
Library despite reusable packages, and Dependencies despite choosing a local
JSON Schema subset instead of an established implementation; it also found
IPC applicability unclear for independently consumed tool messages.
(`3439aae9:docs/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`,
section 4.7)

**Inference:** The original A1 comparison must therefore evaluate both design
quality under the standards actually selected and routing/application failure.
It would be historically incorrect to judge the original design as though the
later Generated Contract, Immutable Authority Closure, evidence-oracle,
implementation-versus-dependency, and systemic-replan rules already existed.

### Post-A1 amendment

**Fact:** `7a571ed2` changed the applicable normative corpus before
policy-impact-v2 planning. It added the Generated Contract profile and changed
Architecture, Contracts, Dependencies, Planning, Verification, and Router.
`0a7fb2da` added their executable policy projections and fixtures. No later
normative standards file changed through accepted v2 candidate `7bc8bd07` or
final standards-recovery transition `c4408363`. (`7a571ed2` and `0a7fb2da`
commit objects; Git path comparison `0a7fb2da..c4408363`)

Policy-impact v2 was explicitly reviewed against those recovered owners,
including Generated Contract, Dependencies, Architecture, and Verification.
(`bf9f3d86:docs/plans/standards-engine-policy-impact-authority-v2/reports/prerequisite-acceptance.md`,
Standards Review)

**Inference:** v10 is not merely “more A1 under the same rules.” It is an A1
amendment developed under standards created in response to v9's failure. That
is why v9 and v10 must remain separate observations in standards-causality
analysis.

## Accepted Requirements And Guarantees

The final A1 plan had nine objective criteria. The acceptance report groups
their satisfied evidence as follows. (`933c9ab9:docs/plans/standards-engine-navigation-analysis/plan.md`,
Objective Acceptance; `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`,
Objective Closure)

| Guarantee family | Accepted A1 v9 behavior |
| --- | --- |
| Canonical discovery | One neutral metadata path loads corpus membership, module identity, aliases, document paths, `Requires`, `Specializes`, and policy-unit declarations; inventoried production consumers do not retain a parallel loader. |
| Snapshot identity | Clean Git, dirty/non-Git, mode, symlink, submodule, exclusion, semantic-contract, and integrity inputs produce immutable deterministic snapshot identities; implementation-only versions remain provenance. |
| Navigation | Typed callers route, read, follow relations, and inspect handles without repository paths; follow-ups remain bound to the same snapshot or analysis. |
| Policy lifecycle | Stable policy-unit identity, semantic overlays, moves, splits, merges, retirement, successors, aliases, and unmapped normative change are explicit; structural change is not semantic proof. |
| Impact selection | Modification, addition, removal, move, split, and merge select deterministic seeds and traverse accepted/proposed relation unions through the generic graph while preserving unknown applicability. |
| Consumer coverage | Derived coverage requirements plus authorized attestations create reusable certificates; missing or stale coverage cannot make empty impact succeed. |
| Resolution | `prepare` and `resolve` produce `CompleteResult` only when exact current obligations, facts, observations, authorization, evidence, and coverage conditions are satisfied. |
| Generated contract | One JSON Schema declaration governs the selected Python, JSON, agent-tool, example, identity, result, next-operation, and rendering projections; stale generation fails. |
| User workflows | Representative route/read plus modification, addition, removal, move, split, and merge paths pass through the real typed Adapter and broad repository verification. |

The accepted scope did **not** grant semantic approval, relationship
authorization, mutation, application, rollback/recovery, project-baseline,
arbitrary-prose-interpretation, or performance guarantees. A `CompleteResult`
proved only that the declared read-only analysis work reached its fixed point.
(`2359a987:docs/decisions/standards-engine-navigation-analysis.md`, Public
Interface, State/Completion, and Consequences;
`933c9ab9:docs/plans/standards-engine-navigation-analysis/plan.md`, Out of
Scope)

### v10 amendment

Policy-impact v2 preserved the four operations and remaining A1 semantics but
changed the policy-impact portions: one internal v2 contract owns supplemental
artifact kinds, relation kinds, compatibility, nodes/groups/edges, semantics,
provenance, and coverage fingerprints; public v10 exposes only
operation-reachable definitions and operation-shaped relationship inspection;
v9 handles/states are unsupported. (`7bc8bd07:docs/decisions/standards-engine-policy-impact-authority-v2.md`,
Decision)

## Module And Interface Structure

At accepted v9, the intended dependency direction was:

```text
StandardsEngine
  -> standards_metadata
  -> standards_applicability
  -> standards_policy_impact
  -> standards_graph
  -> standards_analysis

standards_graph / standards_policy_impact / standards_analysis
  -> graph_engine

standards_verifier consumes neutral owners; it does not own them.
```

This is the structure recorded by the accepted ADR and reflected in package
imports. (`2359a987:docs/decisions/standards-engine-navigation-analysis.md`,
Module Boundaries; `2359a987:tools/standards_engine/README.md`;
`2359a987:tools/standards_analysis/README.md`;
`2359a987:tools/standards_policy_impact/README.md`)

| Module | Owned behavior at accepted v9 | Principal Interface or seam |
| --- | --- | --- |
| `graph_engine` | Domain-neutral nodes, edges, named groups, and traversal. | Generic graph construction/query; policy meaning remains outside. |
| `standards_metadata` | Corpus membership, canonical modules, aliases, paths, policy-unit declarations/locators/lifecycle, source bytes, canonical serialization. | Immutable corpus and identity resolution used by navigation, graph, analysis, verifier, and generated validation. |
| `standards_applicability` | Fact schemas, immutable programs/fact sets, operators, type checks, three-valued truth, unresolved facts, dependency digests. | `compile_fact_schema`; schema compiles programs; programs evaluate bound fact sets. |
| `standards_policy_impact` | Source-owned policy-impact declarations, relationship-kind semantics, graph contribution, applicability programs, provenance. | One compiled set consumed by graph, analysis, verifier, and engine inspection. |
| `standards_graph` | Neutral projection of canonical modules/policy units and registered relation providers. | Registry/graph Adapter between metadata/policy-impact and generic graph. |
| `standards_analysis` | Snapshots, classification, impact selection, obligations, coverage, facts, reading plans, immutable state transitions and projection. | Domain functions and types, with `AnalysisKernel`/`AnalysisState` as lifecycle implementation. |
| `standards_engine` | Composition, repository opening, trusted capability injection, public conversion, state storage, four public operations, rendering and agent tools. | `StandardsEngine`, `AgentToolFacade`, generated public models, and state-store seam. |
| `standards_verifier` | Repository verification and diagnostics using the neutral owners. | Downstream consumer; not part of the four-operation product Interface. |

Sources: `2359a987:docs/decisions/standards-engine-navigation-analysis.md`;
`2359a987:tools/standards_engine/standards_engine/engine.py`;
`2359a987:tools/standards_analysis/standards_analysis/resolution.py`.

### External Depth and internal surface

**Fact:** The product Interface is four operations. State storage has at least
two real Adapters—`InMemoryAnalysisStateStore` and
`DirectoryAnalysisStateStore`—behind `AnalysisStateStore`. The agent Adapter
uses the same structured calls rather than a prose command language.
(`2359a987:tools/standards_engine/standards_engine/engine.py`, classes at lines
119–274 and operation methods; `2359a987:tools/standards_engine/standards_engine/tools.py`)

**Diagnostic facts:** `standards_analysis.__init__` exported 118 names at the
accepted tree; generated engine models exported 139 names. `engine.py` was
1,586 lines and `standards_analysis/resolution.py` 1,643 lines. The custom
generator and validator were 751 and 510 lines. These counts do not prove that
the Modules were shallow, but they establish that a caller using lower Python
Interfaces or maintaining composition had much more to learn than the
four-operation product Interface suggests. (`2359a987:tools/standards_analysis/standards_analysis/__init__.py`;
`2359a987:tools/standards_engine/standards_engine/_generated_contract.py` and
the named source files)

**Inference:** The external `StandardsEngine` Module had good Depth; the
cluster behind it did not consistently preserve that Depth for internal Python
callers or maintainers. Repair commits repeatedly crossed the schema,
generator, generated output, engine conversion, analysis domain, tool Adapter,
renderer, tests, and documentation. That propagation is stronger evidence of
limited Locality than the raw export or line counts.

## Representations And Versions

### Representation inventory at v9

A1 used at least these distinct representations:

1. Repository-authored Markdown/TOML/TSV authority: canonical metadata,
   policy units, Router projection, facts, policy-impact declarations, graph
   catalog, horizons, and coverage attestations.
2. One JSON Schema Draft 2020-12 document with
   `x-standards-engine-*` annotations for transport shape, identity,
   authorization, projection, and state-machine metadata.
3. A custom standard-library schema validator.
4. A custom generator producing `_generated_contract.py` and agent-tool JSON.
5. Handwritten analysis-domain Python values and transformations.
6. Adapters converting analysis values to generated public results.
7. Canonical identity serialization and multiple domain-separated hashes.
8. Persisted `AnalysisState` contract values in memory or the directory store.
9. Examples, identity fixtures, deterministic text rendering, and
   inspection-result projections.

Sources: `2359a987:tools/standards_engine/contracts/README.md`;
`2359a987:tools/standards_engine/contracts/a1-contract.schema.json`;
`2359a987:tools/standards_engine/contracts/generate_contract.py`;
`2359a987:tools/standards_engine/contracts/validate_contracts.py`;
`2359a987:tools/standards_engine/standards_engine/engine.py`;
`2359a987:tools/standards_analysis/standards_analysis/resolution.py`.

### Version evolution

The formation schema was public contract/schema/applicability v1. Successive
coordinated cutovers advanced policy-impact, obligation, reading-plan, fact,
state, and public Interface identities. Recorded milestones include public v4
for plural obligations, v5 for reading plans, v7 for fact authority, v8 for
single-state lifecycle, and v9 for the post-acceptance integrity repair.
Policy-impact v2 later advanced the public Interface to v10.
(`c7d23dfa:tools/standards_engine/contracts/a1-contract.schema.json`;
`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-consumer-obligation-replan.md`;
`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-reading-plan-replan.md`;
`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-fact-authority-replan.md`;
`94b295b4:tools/standards_engine/contracts/a1-contract.schema.json`;
`2359a987:tools/standards_engine/contracts/a1-contract.schema.json`;
`7bc8bd07:tools/standards_engine/contracts/a1-contract.schema.json`)

At accepted v9 the ADR separately named snapshot/handle v2, navigation v2,
analysis identity/schema v2, result schema v1, analysis contract v5,
applicability v3, relationship-kind v1, horizon-provider v2, and numerous v1
identity domains for context, requirements, observations, coverage view,
attestation, and certificate. Historical packet v4 and report v3 domains were
retired. (`2359a987:docs/decisions/standards-engine-navigation-analysis.md`,
Public Interface and Serialization/Identity)

At v10, Interface/schema became 10, result projection 2,
snapshot/navigation/analysis handle schema and identity 3, analysis
contract/schema 6/3, coverage families 2, internal policy-impact authoring and
provider contracts 2, and horizon-provider 3. Edge identity remained v1.
(`7bc8bd07:docs/decisions/standards-engine-policy-impact-authority-v2.md`,
Public Contract)

**Inference:** The versions generally represented real incompatible cutovers,
and the design consistently rejected silent compatibility fallback. That is a
merit. The cumulative compatibility vocabulary was nevertheless large, and
many version changes moved together because the schema, identity, state, and
projection meanings were tightly coupled. A1c should treat the observed
coupling as evidence to measure, not assume that every A1/A1b version is an
independent consumer requirement.

## Verification And Acceptance Approach

### Accepted portfolio

The final v9 acceptance recorded:

- 82 `standards_analysis` tests;
- 45 `standards_engine` tests;
- 18 `standards_metadata` tests;
- 12 `standards_applicability` tests;
- 7 `standards_policy_impact` tests;
- 35 `graph_engine` tests;
- 2 `standards_graph` tests;
- 380 `standards_verifier` tests;
- 33 contract examples, 8 identity fixtures, 4 operation envelopes, and 143
  validated schema definitions;
- generated freshness and current-plan checking;
- 218 declarative suites and 53 retained Bash checkers; and
- scoped Ruff and Git diff integrity.

Source: `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`,
Verification Boundary.

The contract validator was explicitly standard-library-only. It rejected
unsupported keywords in its maintained subset, resolved local references,
validated examples, checked discriminated unions and identity annotations,
and checked generated freshness and operation/state-machine references. It was
described as conformance tooling rather than runtime or another schema
authority. (`2359a987:tools/standards_engine/contracts/README.md`, Validation)

Verification also included targeted negative fixtures, identity mutation,
post-capture source mutation, cold-process reconstruction, exact diagnostics,
schema semantic mutations, differential local equality checks, and independent
review of each final repair candidate. (`933c9ab9:docs/plans/standards-engine-navigation-analysis/execution-ledger.md`,
repair entries)

### What the portfolio proved and did not prove

The later standards-recovery reproduction reran the accepted tree and found
that the accepted repair families were reproducible: generated closure for the
sampled mutations, public result adaptation, immutable selected reads, cold
child inspection, selected version identity, and exact negative diagnostics.
It also explicitly bounded those claims: freshness was not semantic
correctness; two local implementations were not an external oracle; identity
canonicalization was not JSON Schema equality; selected cold tests did not
prove every future Adapter; and field mutation did not prove every contract
belonged in identity. (`c4408363:docs/plans/standards-engine-standards-recovery/reports/historical-a1-repair-reproductions.md`)

**Inference:** The test count is not evidence that the portfolio was
unnecessary. The stronger finding is that several accepted or candidate gates
had low marginal or misclassified evidentiary value:

- generated freshness proved agreement with the generator, not generator
  completeness;
- local validator/generated agreement proved consistency, not external
  dialect conformance;
- candidate fixtures sometimes failed before reaching their claimed defect;
- substring matching proved less than a complete diagnostic;
- broad passing totals coexisted with a live-worktree leak and incomplete
  native models.

These are direct historical examples of evidence needing a named reachable
failure, an adequate oracle, and a clear unsupported domain. They do not justify
removing any specific remaining test without a claim-level audit.

## Defects And How They Were Discovered

| Defect family | Discovery path | Correction or disposition | Evidence |
| --- | --- | --- | --- |
| Missing consumer-review obligations | The plan marked Milestone 3 accepted, then implementation review noticed definite impact candidates never became obligations. | Reopened Milestone 3; added canonical aggregation and plural provenance at `50043a5b`. | `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-consumer-obligation-replan.md`. |
| Coverage self-invalidation | Attestations changed the complete snapshot they answered; declaration-only horizon could omit unseen consumers. | Split complete snapshot from `CoverageAuthorityView`; introduced independent horizon, requirements, attestations, certificates. | `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-3-coverage-identity-replan.md`. |
| Reading metadata invalidated every coverage subject | Horizon v1 fingerprinted one opaque manifest; adding reading-only metadata changed all 28 requirements. | Provider v2 excluded only typed reading authority and renewed coverage once. | `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-horizon-projection-replan.md` and `milestone-4-horizon-v2-audit.md`. |
| Fact answers had wrong identity scope | One fact could affect several relationships; relationship-bound answers duplicated authority. | Added semantic fact contracts, topology-independent context, requirements, observations, provider/authorization views. | `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-fact-authority-replan.md`. |
| Content identity conflicted with mutable packet supersession | Re-preparing identical state returned the same packet ID, but global history made it stale. | Replaced packets/reports/hidden sessions with one immutable state and branching/idempotent transitions. | `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-packet-supersession-replan.md`. |
| Immutable handle read live bytes | Post-implementation audit mutated source after snapshot issuance and observed whole-module reads from current worktree. | Captured exact Git-tree or verified-manifest content and bound reads to it; first acceptance withdrawn. | `933c9ab9:docs/plans/standards-engine-navigation-analysis/execution-ledger.md`, A1 Acceptance Reopened; SENA-021 in `issues.md`. |
| “Repaired” inspection still leaked live state and caches | Follow-up audit exercised whole-module inspection and cold child handles. | Reconstructed from persisted immutable state and stored authority views; second acceptance withdrawn. | Same ledger, “A1 Boundary Repair Acceptance Reopened Again”; SENA-022. |
| Generator preserved names but omitted meaning | Independent reviews mutated integer minimums, result shapes, nested variants, and native results. | Expanded traversal and generated result closure over Repairs II–IV. | Repair II–IV candidate reports at `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/`. |
| Equality and regex semantics diverged | Review tested Boolean/integer constants, Unicode, `uniqueItems`, and regex behavior across validator/generated entrypoints. | Repairs IV–VI unified local behavior and evidence. | Repair III–VI candidate reports. |
| Local agreement contradicted selected external dialect | Post-A1 root-cause audit compared the local equality oracle with Draft 2020-12 and reproduced Unicode cases from exact v9 tree. | Retained as known A1 nonconformance; standards recovery and A1b became prerequisites. | `c4408363:docs/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`. |
| Policy-impact invariant split across four owners | A Router projection verifier failure led to a systemic audit of compiler, catalog, verifier path inference, coverage parsing, and public schema. | Policy-impact v2 consolidated internal authority and moved public contract to operation-shaped v10. | `7bc8bd07:docs/decisions/standards-engine-policy-impact-authority-v2.md`, Context and Decision. |
| First policy-impact-v2 acceptance evidence still incomplete | Independent exact-tree review found ineffective serialized booleans, raw failures, malformed optional handling, and sampled rather than derived compatibility evidence. | Corrected at `7bc8bd07`; coverage renewed; independently accepted. | `dd571976:docs/plans/standards-engine-policy-impact-authority-v2/execution-ledger.md`, Exact-Candidate Acceptance Rejection and Recovered Candidate. |

## Decisions That Added Or Removed Machinery

| Decision | Contemporaneous reason | Machinery effect | Audit interpretation |
| --- | --- | --- | --- |
| Separate A1 from A2 authoring | Mutation and recovery needed a stronger lifecycle. | Removed write sessions, proposal heads, apply/recovery, and rollback from A1. | Clear reduction and preserved product coherence. |
| One JSON Schema declaration plus custom extensions | Avoid parallel Python/JSON contracts and a custom IDL; avoid an unjustified dependency. | Added a large schema, custom validator, generator, generated Python/tool JSON, annotations, freshness and semantic tests. | One declaration owner did not provide one semantic owner; poor Locality was exposed by repairs. |
| Neutral metadata and standards graph Modules | Prevent verifier ownership and duplicate consumers. | Added packages and cutovers, while deleting old loaders/adapters without fallback. | Added structure but improved authority and reuse; deletion test suggests the concern would otherwise reappear in several callers. |
| Standard-library applicability Module | Avoid dependency cycles and duplicate evaluators. | Added a typed expression compiler/evaluator and contracts. | A defensible deep Module with several real consumers: Router, policy impact, analysis, verifier. |
| Compiled source-owned policy impact | Avoid topology/semantic sidecars and policy-aware generic graph code. | Added declarations, compiler, semantics index, identity mappings, and verification. | Coherent concern, but v1 left catalog/compatibility/coverage pieces outside until v2. |
| Independent coverage horizon/view/requirement/attestation/certificate chain | Prove complete consumer discovery, including successful empty impact, without self-invalidating attestations. | Added multiple identities, stores, audit artifacts, renewal workflow, and exact subject checks. | Solved a stated guarantee; external necessity and least-sufficient form remain unresolved. |
| Immutable packets, then fact authority, then single-state lifecycle | Bind evidence and decisions, support reuse/replay, eliminate hidden sessions and supersession conflict. | First added packet/report identities, then removed them in favor of one state; retained contexts, requirements, observations, authorization/provider views, and storage. | Single-state cutover materially reduced competing lifecycle concepts, though underlying authority representation stayed large. |
| No compatibility runtime at each cutover | No supported external state required migration; silent interpretation was unsafe. | Avoided dual readers, aliases, fallback parsers, and converters. | Consistent complexity reduction, but produced rapid public version churn. |
| Repeated independent acceptance reviews | Separate implementation evidence from acceptance authority and catch sibling defects. | Added candidate reports, lifecycle transitions, fixtures, and broad reruns. | Expensive, but it found defects the implementation-owned suites missed; the weakness was often oracle selection, not review independence. |

Sources: accepted A1 ADR Considered Options and Consequences at
`2359a987:docs/decisions/standards-engine-navigation-analysis.md`; the cited
replan reports; policy-impact-v2 ADR and ledger.

## Rejected Alternatives And What They Reveal

| Alternative rejected at the time | Recorded reason | Later relevance |
| --- | --- | --- |
| Keep metadata in `standards_verifier` or inject a verifier-built graph | Would invert dependency direction or leave verifier as hidden A1 owner. | The neutral cutover appears well supported by several actual consumers. |
| Put graph projection in metadata | Would make the loader own a downstream graph representation. | Preserved a focused metadata Interface, although it introduced `standards_graph`. |
| Parse Router prose or hardcode Router decisions in Python | English was not deterministic; hardcoding would create policy authority. | The reviewed projection was a reasonable Adapter, but its semantic consumers later required stronger recovery rules. |
| Make Python classes the contract owner | JSON/tool consumers would need another contract. | Correctly identified multi-consumer pressure, but the chosen schema still had multiple semantic interpreters. |
| Create a custom interface language | Added parser and maintenance surface. | Avoided an even larger bespoke language. |
| Adopt a third-party schema implementation | The admitted subset was thought implementable with the standard library and no dependency was yet justified. | Later exact-tree evidence found a declared-dialect nonconformance; this is strong evidence that implementation-versus-dependency review was inadequate. |
| Edge-ID policy semantics sidecar | Topology and semantics would be two synchronized authorities. | Compiler ownership was reasonable; v2 showed the same invariant was still split elsewhere. |
| Put policy fields in generic graph metadata | Would weaken graph neutrality. | Preserved generic graph leverage and avoided policy-specific traversal. |
| Build an incremental policy compiler | Full rebuild was simpler at repository scale. | A clear least-machinery decision. |
| Populate policy units for every module just to enable read/inspect | Would invent semantic identities and audit work unrelated to navigation. | A clear rejection of unnecessary machinery. |
| Preserve mutable packet supersession with session IDs or hidden heads | Would break deterministic identity or reintroduce ambient state. | Single immutable state was the more coherent A1 design. |
| Perform all A1b redesign during policy-impact v2 | Equality, general contract compilation, and immutable storage were independent changes. | Preserved auditability and provides the secondary v10 comparison boundary. |

Sources: `2359a987:docs/decisions/standards-engine-navigation-analysis.md`,
Considered Options; milestone 2 and 3 replan reports at `933c9ab9`;
`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-packet-supersession-replan.md`;
`7bc8bd07:docs/decisions/standards-engine-policy-impact-authority-v2.md`,
Considered Options.

## What A1 Did Well

The following are audit inferences grounded in the cited facts, not claims that
every implementation choice should survive A1c.

1. **The external Module had a coherent, deep Interface.** Four operations
   covered route/read/related, prepare, iterative resolution, and inspection,
   while callers supplied no paths and text remained non-authoritative.
   (`2359a987:docs/decisions/standards-engine-navigation-analysis.md`, Public
   Interface)

2. **The product scope was disciplined.** A1 did not absorb authoring,
   semantic approval, application, rollback, external projects, arbitrary
   prose inference, or unmeasured performance claims.
   (`933c9ab9:docs/plans/standards-engine-navigation-analysis/plan.md`, Scope)

3. **Generic graph mechanics stayed policy-neutral.** Policy impact selected
   named graph groups and compiled policy semantics outside `graph_engine`.
   (`2359a987:docs/decisions/standards-engine-navigation-analysis.md`, Graph
   Composition)

4. **Unknown and invalid were not silently collapsed.** Three-valued
   applicability, unresolved facts, unsupported versions, missing authority,
   and typed rejections preserved uncertainty.
   (`2359a987:docs/decisions/standards-engine-navigation-analysis.md`,
   Applicability and Audit Coverage)

5. **The single-state correction simplified a genuinely conflicting model.**
   It removed packet/report/state triple identity, hidden sessions, and global
   supersession rather than layering another compatibility head.
   (`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-packet-supersession-replan.md`)

6. **Cutovers usually removed superseded runtime authorities.** Metadata,
   graph projection, applicability, policy-unit loading, and later public v10
   did not retain production fallback loaders merely for compatibility.
   (Milestone 1–4 cutover reports; policy-impact-v2 ADR)

7. **The repository preserved rejected evidence.** Withdrawn acceptances,
   rejected trees, review findings, and rewrite mappings remained inspectable
   rather than being rewritten as success. That preservation is what makes the
   current standards audit possible.
   (`933c9ab9:docs/plans/standards-engine-navigation-analysis/execution-ledger.md`;
   `60afb3e4` commit diff)

## What A1 Did Poorly

1. **It conflated declaration authority with semantic authority.** One JSON
   Schema document was named the sole machine authority, but several local
   implementations independently supplied equality, regex, traversal,
   conversion, and validation behavior. The repair sequence and later Draft
   reproduction directly demonstrate the resulting disagreement.

2. **Change Locality was weak across the contract seam.** A public semantic
   correction routinely touched schema, generator, generated source, agent
   tools, domain models, engine conversion, renderer, package exports,
   fixtures, plan checks, and documentation. The repeated repair commits show
   this propagation; counts merely reinforce it.

3. **The internal Interfaces exposed extensive machinery.** The product
   Interface was small, but lower package Interfaces exposed authority views,
   kernels, contracts, facts, observations, requirements, decisions,
   coverage objects, traces, and serialization operations. Tests and engine
   composition crossed those seams directly. This reduced the Depth available
   to maintainers even if end callers used only four operations.

4. **Several requirements produced multi-stage authority chains before their
   necessity was independently evidenced.** Coverage in particular required a
   horizon, view, requirement, attestation, certificate, identities, renewal,
   inspection, and exact-set evidence. The repository proves that chain met the
   plan's guarantee; it does not prove that an actual A1 consumer required the
   full guarantee or that a smaller aggregate could not satisfy it.

5. **Verification often accumulated around representations.** A1 checked
   schema, generator freshness, generated decoder, examples, identity
   fixtures, internal domain behavior, public adaptation, declarative suites,
   and retained Bash. Some overlap was valuable, but candidate history shows
   that agreement and totals were sometimes mistaken for an independent
   oracle.

6. **The design churned public versions rapidly before acceptance.** v1 became
   v9 during the implementation, then v10 during the pre-A1b amendment. The
   no-fallback policy kept runtime simpler, but the version sequence is evidence
   that the admitted public shape was not stable enough at formation.

7. **Routing missed applicable standards.** Build, Library, and Dependencies
   were not selected for generator/package/local-standardized-semantics work;
   later recovery identified and corrected those gaps. This is evidence of
   missed standards application as well as missing/ambiguous standards, not
   proof that the original selected standards caused every design choice.

Sources for findings 1–7: the Repair II–VI reports; `3439aae9` A1b brief
sections 2–4.8; accepted v9 schema and package entry points; standards-recovery
reproductions; original plan Routed Standards.

## Evidence For Later Standards Decisions

This report does not authorize normative changes, but A1 supplies the following
causal candidates for the standards-evolution and synthesis reports:

| Candidate classification | A1 evidence |
| --- | --- |
| Missing or unclear standard | No then-effective rule clearly separated declaration ownership from executable semantic ownership or required an independent dialect oracle. |
| Routing/application failure | The plan omitted Build, Library, and Dependencies even though the work generated artifacts, created reusable packages, and chose local standardized semantics. |
| Enforcement/oracle failure | Passing freshness, local differential checks, and broad suite totals did not catch the declared-dialect mismatch or early ambient-authority leaks. |
| Systemic-replan failure | Successive repairs addressed the latest equality/projection example; sibling defects emerged at the next review until the later recovery required an invariant-family audit. |
| Product-required complexity | Explicit unknown applicability, exact completion, and cold reconstruction were stated A1 guarantees and cannot be dismissed merely because their implementation was large. |
| Possibly over-specified product requirement | Full consumer-coverage certification and transitive inspectable authority were plan requirements, but repository history does not identify an independent external consumer that demanded their most elaborate form. |
| Standards-induced complexity, unresolved | Original standards emphasized one owner, typed contracts, evidence, and immutable identity, but the evidence does not prove those rules caused the exact schema/coverage design. Compliance alone is not causation. |

## Unresolved Questions For The Comparative Audit

1. Which A1 guarantees were exercised by a real independent caller rather than
   only repository-owned tests and the agent Adapter?
2. Which coverage, identity, validation, and verifier checks detect distinct
   reachable failures, and which are subsumed by another proof? Counts cannot
   decide this; AUD-A5 must classify them claim by claim.
3. Were the lower-package Interfaces intended as supported external Python
   Interfaces or only internal seams? Their broad exports exist, but consumer
   commitments need call-site and documentation analysis.
4. Could exact cold reconstruction have been represented as one persisted
   immutable aggregate rather than several inspectable authority values, or
   did a stated consumer require independent child handles?
5. Was successful empty impact a necessary A1 product promise, or a governance
   requirement imported from standards-maintenance process? The plan treats it
   as required, but origin evidence does not identify an independent consumer.
6. Should the v10 policy-impact correction count as A1 merit, A1 repair debt,
   or a separate standards-recovery prerequisite in each comparison category?
   This report recommends showing both v9 and v10 rather than forcing one
   label.
7. How much of A1b's later machinery preserves externally observable A1
   guarantees, and how much preserves A1's internal representations and test
   topology? That is the central A1/A1b/A1c question and cannot be decided from
   A1 alone.

## Conclusion

The fairest historical account is not that A1 was simply “small and flawed” or
that its acceptance was meaningless. A1 established a valuable read-only
product Interface, neutralized several real ownership inversions, handled
uncertainty conservatively, and converged on a coherent immutable state model.
Its independent review process found and preserved serious defects.

The equally important account is that A1's supporting contract and authority
machinery lacked Depth and Locality. A single schema declaration accumulated
transport, generation, identity, state-machine, authorization, and projection
roles while several executables still supplied the actual semantics. Coverage
and replay guarantees expanded into multi-representation authority chains, and
verification often proved local agreement more readily than independent
correctness. Policy-impact v2 improved one systemic seam, but did so under a
different standards snapshot and should be analyzed as an amendment, not
silently folded into the original accepted A1.

Those distinctions give the later audit a stable evidence base: compare A1b
against accepted v9 for historical causality, against accepted v10 for the
latest pre-A1b runtime behavior, and against `c4408363` only when the recovered
standards and verification posture are themselves the subject.
