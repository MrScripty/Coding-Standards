# Standards Engine A1b History And Design Audit

**Audit status:** Complete historical research for `AUD-A2`

**Accepted implementation:** commit
`84412f22fa9fe082f089eaa347c30c23f185ffee`, tree
`8e0f96a61fcea2398418b17d16a061c20f7463f5`

**Acceptance record:** commit
`580d9c959b22f3fdeb0898e7fd4aafd168893580`

**Planning comparison base:** commit
`c4408363752b10060f631247f3e2f1fa26eae003`, tree
`84477150bd368a168dd04da3770de55c23bbb817`

## Scope And Method

This report reconstructs A1b from repository-owned primary sources. It covers
the defect and recovery brief that made A1b necessary, the standards-recovery
prerequisite, every recorded planning candidate through C7, implementation
milestones and rejected implementation boundaries, and final content-bound
acceptance. It analyzes the accepted design but does not compare A1 and A1b
quantitatively; that belongs to the audit's architecture comparison. It also
does not decide which individual tests are redundant; that belongs to the
verification-portfolio audit.

Historical claims use `commit:path` citations. Current links are navigation
aids; the named commit remains the authority when current wording differs.

Evidence labels have these meanings:

- **Fact:** directly observable in a commit, tree, source file, test, or
  accepted report.
- **Recorded rationale:** an explanation authored in the contemporaneous plan,
  ADR, report, ledger, or commit.
- **Inference:** this audit's interpretation of the primary evidence.
- **Counterevidence:** primary evidence that narrows or challenges a recorded
  rationale or inference.
- **Unresolved:** a question the surviving repository evidence cannot decide.

The design analysis uses Module, Interface, Seam, Adapter, Depth, Leverage, and
Locality consistently. Raw counts are diagnostic signals only. They do not by
themselves establish excessive complexity, redundancy, or design quality.

Primary navigation sources are the [A1b redesign
brief](../../standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md),
[accepted A1b plan](../../standards-engine-a1b/plan.md), [A1b execution
ledger](../../standards-engine-a1b/execution-ledger.md), [accepted
ADR](../../../decisions/standards-engine-a1b.md), [C6/C7 history
research](../../standards-engine-a1b/reports/c6-c7-design-history-research.md),
[C7 proposal](../../standards-engine-a1b/reports/c7-design-proposal.md), and
[final acceptance](../../standards-engine-a1b/reports/a1b-final-acceptance.md).

## Executive Findings

1. **Fact:** A1b began with one newly reproduced external-contract defect:
   accepted A1 treated NFC-equivalent but codepoint-distinct strings as equal
   for Draft 2020-12 `const`, `enum`, and `uniqueItems`. The trigger brief also
   treated incomplete semantic ownership and immutable-authority closure as
   systemic risks. Sources:
   `3439aae9540786d9734431e633ea5b62afb50592:docs/archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`
   and
   `c4408363752b10060f631247f3e2f1fa26eae003:docs/archive/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`.

2. **Counterevidence:** exact-tree standards-recovery reproduction found that
   accepted A1 already passed generated public-closure mutations, public result
   ownership, selected mutation-after-capture reads, and fresh-process
   inspection of context, requirement, observation, and certificate handles.
   The recovery report explicitly says those results did not prove exhaustive
   dialect semantics or every future authority Adapter. A1b therefore combined
   repair of a live equality defect with structural prevention against failure
   families that had already received local repairs. Source:
   `c4408363752b10060f631247f3e2f1fa26eae003:docs/archive/plans/standards-engine-standards-recovery/reports/historical-a1-repair-reproductions.md`.

3. **Fact:** A1b implementation was not admitted until a separate standards
   recovery added policy for evidence oracles, generated contracts, immutable
   authority closure, dependency selection, systemic replanning, and Router
   applicability, together with policy-graph and coverage projections. The
   recovery ran from the `3439aae9` brief through accepted candidate
   `a166e36f` and completion boundary `c4408363`. Sources:
   `3439aae9:docs/archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`,
   `238ff4e3:docs/archive/plans/standards-engine-standards-recovery/reports/standards-recovery-acceptance.md`,
   and
   `c4408363:docs/archive/plans/standards-engine-standards-recovery/plan.md`.

4. **Fact:** planning passed through an initial rejected design, Candidate C,
   C-prime, C2, C3, C4, C5, C6, and four C7 review boundaries before admission
   at `36dd7579`. The labels are not a clean C1-C7 sequence: no surviving
   contemporaneous artifact calls the initial design "C1"; the accepted ADR
   later says it supersedes C1 through C6. Commit identities, not inferred
   candidate numbers, are therefore the canonical historical keys. Sources:
   `36dd7579:docs/archive/plans/standards-engine-a1b/execution-ledger.md` and
   `580d9c95:docs/decisions/standards-engine-a1b.md`.

5. **Fact:** the accepted design preserves the four-operation read-only
   lifecycle but adds three foundation Modules, a closed immutable object
   repository, owner-local codecs, four operation-authority records,
   roots-only closures, direct consumed-trust objects, a generated 140-definition
   public algebra, manifest-owned package roots, and an AST-governed production
   import profile. Sources:
   `84412f22:docs/decisions/standards-engine-a1b.md`,
   `84412f22:tools/standards_engine/contracts/a1-interface.toml`, and
   `84412f22:tools/standards_engine/contracts/a1-contract.schema.json`.

6. **Fact:** six implementation boundaries were rejected after the first
   atomic cutover: `d6117216`, `3da674c1`, `ead04bc5`, `8b8a4b48`, `23706513`,
   and `88f93a33`. The later four review cycles concentrated increasingly on
   suite-input authority, Git-index authority, package-import acquisition, and
   the AST scanner's Python binding and control-flow model rather than the four
   Standards Engine operations. Source:
   `580d9c95:docs/archive/plans/standards-engine-a1b/execution-ledger.md`.

7. **Inference:** A1b's complexity has at least four different proven origins:
   real defect correction, explicitly selected product/operational guarantees,
   standards-mandated authority and evidence structure, and review-driven
   enforcement closure. Treating all of it as one indivisible product
   requirement would make later A1c simplification impossible and would
   misstate the historical evidence.

8. **Unresolved:** final acceptance proves conformance to the admitted A1b plan
   and standards. It does not prove that the plan selected the least machinery,
   that every internal Interface is deep, that every version has a real
   independently evolving consumer, or that every test/verifier supplies
   unique protection. No A1b artifact performs that marginal-necessity audit.

## Trigger: From Accepted A1 To A1b

### The recorded A1 boundary

**Fact:** the redesign brief preserved A1's historical acceptance at
implementation commit `2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`, with acceptance recorded at
`933c9ab93d18ede987d449a6fe7b9ebd313922fc`. It did not retroactively revoke
that result. Sources:
`3439aae9:docs/archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`
and
`933c9ab9:docs/archive/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`.

**Recorded rationale:** the brief said A1's product architecture was worth
preserving: one read-only facade, neutral graph mechanics, standards-specific
analysis, explicit snapshot and analysis handles, immutable analysis state,
deterministic pending/complete projections, and exclusion of controlled
authoring. It attributed repeated repairs to two supporting seams: duplicated
contract semantics and incomplete immutable authority closure. Same source,
sections 2 and 4.

### The new external-contract disagreement

**Fact:** accepted A1 declared JSON Schema Draft 2020-12 but reused its
NFC-normalizing identity serialization for schema equality. Composed `"é"` and
decomposed `"e\u0301"` therefore agreed locally but contradicted the selected
Draft's codepoint string equality. Boolean/integer cases in the same
reproduction conformed. Sources:
`3439aae9:docs/archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`
and
`c4408363:docs/archive/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`.

**Recorded rationale:** this disagreement demonstrated that schema instance
equality, A1 domain equality, and identity canonicalization needed separate
owners. It also demonstrated that agreement between two locally maintained
implementations was consistency evidence, not an external conformance oracle.

### What remained broken versus what remained risky

| Finding at the accepted A1 tree | Evidence class | A1b consequence |
| --- | --- | --- |
| Unicode schema equality disagreed with Draft 2020-12. | Reproduced current defect. | Select one maintained Draft validator and separate equality domains. |
| Generated closure mutations, minimum/const/pattern/requiredness, result variants, and freshness passed. | Counterevidence to a claim that accepted A1 generation was simply still partial. | A1b strengthened closure ownership and removed independent keyword interpreters rather than merely adding missing fields. |
| Selected module reads and inspection stayed stable after source mutation. | Passing bounded behavior, not universal proof. | A1b made absence of live source structural for every advertised handle. |
| Fresh-process public inspection of context, requirement, observation, and certificate succeeded. | Passing bounded behavior, with a temporary fixture needed to reach fact handles. | A1b replaced owner lookup/session mechanisms with direct storage for every inspectable object. |
| All ten selected semantic version fields changed snapshot identity; two implementation versions did not. | Passing bounded identity projection. | A1b replaced the version bag with independently scoped payload, identity, handle, result, and operation versions. |

Every row is recorded in
`c4408363:docs/archive/plans/standards-engine-standards-recovery/reports/historical-a1-repair-reproductions.md`.

**Inference:** the historical case for A1b was stronger as a prevention and
ownership redesign than as a list of still-failing A1 acceptance behaviors.
The distinction matters: structural prevention may be valuable, but its
machinery should not automatically become a permanent external requirement.

## Standards Recovery As A Hard Dependency

**Fact:** commit `3439aae9` prescribed this sequence: standards audit,
standards-recovery plan, standards and semantic-graph implementation,
independent standards acceptance, A1b plan/ADR, A1b implementation, independent
A1b acceptance, then separate A2 review. A1b planning was unavailable until
recovery completed. Source:
`3439aae9:docs/archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`.

**Fact:** the accepted recovery added six policy families and their Router,
profile, prompt, template, fixture, suite, graph, and coverage projections:

- evidence-oracle, negative-fixture, and differential-evidence rules;
- generated-contract semantics, exact dialect/vocabulary, and separation of
  identity from instance equality;
- immutable authority closure;
- implementation-versus-dependency decisions;
- systemic-finding replanning; and
- Generated Contract Router/profile applicability.

Sources:
`a166e36f:docs/archive/plans/standards-engine-standards-recovery/reports/standards-recovery-candidate.md`
and
`a166e36f:docs/archive/plans/standards-engine-standards-recovery/reports/standards-recovery-consumer-dispositions.md`.

**Fact:** independent recovery acceptance reported zero Standards and
Specification findings, 585 focused package tests, 224 registered declarative
suites, 53 retained migration checkers, generated freshness, contract
validation, exact coverage identities, and a clean tree. It accepted candidate
`a166e36f`, tree `8e2c3421`; `c4408363` then completed the recovery lifecycle.
Source:
`238ff4e3:docs/archive/plans/standards-engine-standards-recovery/reports/standards-recovery-acceptance.md`.

**Diagnostic fact:** `git rev-list --count 3439aae9..c4408363` returns 100
commits. That interval includes the policy-impact-v2 prerequisite, coverage
reconciliation, review/lifecycle records, and semantic-oracle corrections, not
just normative prose. It demonstrates process cost, not that any individual
commit or check was unnecessary.

**Inference:** A1b inherited both useful corrective policies and a large
evidence-administration substrate before its own planning began. Policy graph,
coverage horizon, attestation, certificate, exact disposition, and
content-bound review obligations later became first-class A1b acceptance work,
even where they did not change caller-visible Engine behavior.

## Chronological Commit And Candidate Record

The table records every material A1b design or implementation boundary. Review
findings are cited from the commit that recorded them in the ledger when the
rejected subject itself could not contain its later review.

| Date | Boundary | Material decision or correction | Disposition and primary source |
| --- | --- | --- | --- |
| 2026-08-24 | `3439aae9` redesign brief | Recorded the Unicode equality disagreement, systemic ownership risks, mandatory standards recovery, recommended contract compiler and immutable repository, and A2 prohibition. | Non-authorizing prerequisite brief; `3439aae9:docs/archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`. |
| 2026-08-26 | `c4408363` recovery base | Completed independently accepted standards recovery and made A1b planning eligible. | Accepted prerequisite; `c4408363:docs/archive/plans/standards-engine-standards-recovery/plan.md`. |
| 2026-08-26 | `f41037bf` initial plan, retrospectively the earliest C-series design | Selected NFC identity v1, three typed aggregate roots, Contracts-to-Identity and Authority-to-Contracts dependencies, a directory Adapter, and a staged schema cutover. | Rejected for incomplete ancestry/admission mechanics, premature production schema changes, missing semantic-consumer migration, incomplete dependency provenance, underspecified identity/annotations, and aggregate-only child inspection; findings recorded in `44de7dff:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-26 | `44de7dff` Candidate C | Replaced identity v1 with codepoint-preserving v2, directly stored every inspectable object, closed schema/interface proposals, and added identity, authority, consumer, and policy-impact inventories. | Rejected because new relationship sources were absent from the closed registry and successful imports did not prove public-root use; `ecdf5a55:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-26 | `ecdf5a55` C-prime | Added explicit relationship registration plus manifest public roots and AST import rules. | Rejected because root-form imports could still load private children and the migration omitted affected roots, entrypoints, and private-import consumers; `c2aea75c:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-26 | `c2aea75c` C2 | Added static `__all__`, exact entrypoints, production source ownership, and systemic import migration. | Specification passed; Standards rejected alternate-root entrypoints, an undeclared Authority/Contracts dependency, missing attestation registry, and omitted Commit routing; `ebc75340:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-26 | `ebc75340` C3 | Closed entrypoint isolation, Authority shape validation, coverage registry, and Router dependencies. | Rejected for horizon-freeze ordering, public inspections depending on absent version fields, and contract evidence limited to historical regressions; `b92ed782:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-26 | `b92ed782` C4 | Added object-specific `SnapshotVersions`, `NavigationVersions`, and `AnalysisVersions`, and widened feature/mutation evidence. | Rejected after authority/version-scope review found copied umbrella promises, mixed capture/interpretation, repository domain ownership, and overbroad trust; `4f69f994:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-26 | `396144ad` standards intervention | Added authority-scope admission, declaration-versus-semantic authority, contract-artifact necessity, and independent version-scope rules during active A1b planning. | Normative input explicitly cited as confirming C4's systemic defect; `396144ad:topics/architecture.md`, `396144ad:topics/contracts.md`, and `4f69f994:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-26 | `4f69f994` C5 | Introduced content-only snapshots, reference-only views, owner-produced `AuthorityBoundValue`, structural execution closure, and transition-only trust. | Rejected for residual Git lineage, complete-view state identity, current-only rather than promised transition closure, Authority/Contracts coupling, and ambient codec/role membership; `9794b927:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-26 | `9794b927` C6 | Removed Git lineage and complete views, separated Authority from Contracts, froze codec/operation catalogs, added qualified roots, retained directory/hard-link storage, and attempted transition-future-complete closure. | Rejected for incomplete operation/trust contracts, structural snapshot breadth, speculative platform/migration scope, duplicated SQL/object kind, and hypothetical future closure; `748d30f7:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-27 | `d06c819b` / `1d18b70d` process correction | Removed the C6-R-T-S direct-child/exact-HEAD/state-only commit protocol and added a general Planning rule that plans do not own Git topology. | Accepted standards/process correction; `1d18b70d:workflows/planning.md` and `1d18b70d:docs/archive/plans/standards-engine-a1b/reports/serial-plan-commit-boundary-guardrail.md`. |
| 2026-08-27 | `748d30f7` C7 | Selected SQLite plus memory stores, path/raw-byte snapshots, roots-only closures, executable per-operation contracts, owner-local codecs, and direct consumed trust. | Architecture retained, but candidate rejected for incomplete envelope, restore, operation-role, authorization, interruption, rejection, and version contracts; `ac362dc5:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-27 | `ac362dc5` corrected C7 | Closed the then-six-field envelope bytes, SQLite restore/interruption, operation roles/cardinalities, typed authorization outcomes, rejection algebra, and removed the analysis umbrella versions. | Rejected for underclosed envelope/identifier dispatch, typed grant/evidence shape, confused operation selectors, and incomplete `strace` provenance; `ee7f2a47:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-27 | `ee7f2a47` typed C7 | Replaced the six-field envelope with seven structural fields, froze authorization/evidence records, distinguished record identity from operation selectors, and pinned test-oracle provenance. | Rejected because Authority still parsed a generic semantic-ID grammar and encoded operation selectors/version summaries still duplicated typed compatibility; `36dd7579:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-27 | `36dd7579` admitted C7 | Made semantic IDs opaque to Authority, replaced encoded selectors with typed `(operation, compatibility_revision)`, assigned edge policy to owner codecs plus one Engine coherence algorithm, and corrected summary ownership. | Independently admitted with zero findings; the admission record was committed with the first implementation slice at `ecc2a321:docs/archive/plans/standards-engine-a1b/reports/a1b-plan-admission.md`. |
| 2026-08-27 | `ecc2a321` Milestone 0 | Added `standards_identity`, exact six-package lock/provenance, Python 3.11/3.12 support, and isolated foundation tests. | Implemented checkpoint; `ecc2a321:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-27 | `a3f5312d` Milestone 1 | Added `standards_contracts` around `jsonschema`/`referencing`, compiled 140 reachable definitions, generated immutable staging projections, and added feature/mutation tests. | Implemented checkpoint; `a3f5312d:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-28 | `eee83026` prerequisite fix | Replaced `str(int)` in identity encoding so integers beyond CPython's ambient 4300-digit conversion limit satisfy the admitted unbounded integer grammar. | Implemented owner-local correction; `eee83026:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-28 | `45163746` Milestone 2 | Added envelope/repository/closure/capture Modules, memory and SQLite Adapters, backup/restore, exact Git/native capture, and required-real syscall interruption evidence. | Implemented isolated authority checkpoint; `45163746:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-28 | `d6117216` first atomic cutover | Replaced A1 production paths, generated v11 algebra, coverage identities, imports, stores, serializers, and migration/coverage artifacts. | Rejected: Authority named downstream kinds; domains did not produce bound values; root cardinality could collapse; provider qualifications were lost; Verifier depended on Engine; old generator/suites/import paths remained; clean entrypoints and genuine public cold reconstruction were unproved. `3da674c1:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-28 | `3da674c1` first corrected implementation | Injected owner codec sets, required domain-produced bound values, moved generation to Contracts, removed Verifier-to-Engine, rejected dynamic aliases, and added fresh-interpreter inspection. | Rejected at Milestone 4 for trust selection, analysis qualification, source-independent reconstruction, no-overwrite recovery, alternate imports, real entrypoint operations, migration closure, and executable operation/codec evidence; `ead04bc5:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-28 | `c07ca3f` candidate record | Bound `3da674c1`, tree `63d55780`, as a review subject. | Later superseded; `c07ca3f:docs/archive/plans/standards-engine-a1b/reports/a1b-implementation-candidate.md`. |
| 2026-08-28 | `ead04bc5` second corrected implementation | Added exact trust contracts/input roles, transition-qualified authority, persisted composition, atomic restore, typed entrypoint operations, alternate-import checks, migration closure, operation/codec evidence, and a typed suite-input projection. | Rejected because the projection duplicated check semantics and omitted transitive/index/package/entrypoint authority; imports still bypassed through `sys.modules`; fixtures used ambient files; operation evidence was incomplete. `8b8a4b48:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-28 | `8b8a4b48` consolidated C7 cutover | Gave each check an input-closure Interface, moved suite-input manifest authority to Analysis, introduced a governed-source AST profile, centralized sanitized Git-index access, and renewed provider-v5 coverage. | Rejected for Store/Delete binding-lifetime errors and remaining direct Git calls that hostile `GIT_*` state could redirect; `23706513:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-29 | `23706513` binding/Git correction | Added execution-ordered bind/unbind events and one public sanitized Git command Adapter across Verifier paths. | Rejected because the public Git-reachability entrypoint still ran Git directly; conditional bindings, simple `sys` aliases, and assignment target order still bypassed or misclassified capability use; `88f93a33:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-29 | `88f93a33` reachability correction | Routed reachability through the typed Adapter and added branch context, `sys` provenance, and left-to-right target ordering. | Rejected because conditional deletion, nested-scope conditional provenance, and augmented-assignment evaluation remained wrong; `e955c39e:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| 2026-08-29 | `e955c39e` branch-state replan | Recorded conservative branch-exit joins, enclosing-scope provenance, and augmented-assignment load/store order as the bounded replacement. | Replan evidence only; `e955c39e:docs/archive/plans/standards-engine-a1b/plan.md`. |
| 2026-08-29 | `84412f22` accepted implementation | Implemented one abstract branch-state join across supported visitors, retained possible `sys` provenance, and corrected augmented assignment; complete evidence passed. | Accepted implementation subject, tree `8e0f96a6`; identified retrospectively by `580d9c95:docs/archive/plans/standards-engine-a1b/reports/a1b-implementation-candidate.md` and accepted by the final report in that commit. |
| 2026-08-29 | `580d9c95` final record | Recorded zero-finding independent Standards and Specification acceptance and changed plan/ADR lifecycle to Accepted. | Final acceptance evidence; `580d9c95:docs/archive/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`. |

**Diagnostic fact:** from the initial plan through final acceptance, the A1b
lineage contains 29 commits: 15 through the admitted-C7 content and 14 after
admission. It contains eleven recorded planning rejection/supersession rounds
before admission and six exact implementation rejections before `84412f22`.
The counts describe iteration cost; they do not establish that every correction
was avoidable.

## Design Evolution: What Each Candidate Added Or Removed

### Initial design through C4

**Fact:** `f41037bf` initially proposed three aggregate authority roots,
directory-backed storage, continued NFC identity v1, and a dependency chain in
which Contracts depended on Identity and Authority depended on Contracts.
Direct child inspection, complete consumer migration, and exact dependency
provenance were incomplete. Source:
`f41037bf:docs/decisions/standards-engine-a1b.md`.

**Fact:** Candidate C (`44de7dff`) made the first enduring large change:
codepoint-preserving identity v2 and direct storage of every public inspectable
object. C-prime through C3 then expanded relationship-source registration,
public-root/export/entrypoint authority, package migration, Router selections,
coverage-source registration, and generated semantic evidence. Sources:
`44de7dff:docs/decisions/standards-engine-a1b.md` and
`b92ed782:docs/archive/plans/standards-engine-a1b/execution-ledger.md`.

**Recorded rationale:** these additions prevented historical A1 failure classes
in which private imports, implicit registries, incomplete generated closure, or
ambient authority passed local smoke checks.

**Inference:** C-prime through C3 primarily deepened governance and proof around
the design rather than changing the caller-facing four-operation lifecycle.

### C4 to C6: authority decomposition under new standards

**Fact:** C4 attempted to make cold reconstruction explicit with separate
snapshot, navigation, and analysis version records. Commit `396144ad` then
added general authority-scope and version-scope standards while A1b was active.
The next replan explicitly cited those standards and rejected C4's records as
copied umbrella authority. Sources:
`396144ad:topics/architecture.md`, `396144ad:topics/contracts.md`, and
`4f69f994:docs/archive/plans/standards-engine-a1b/execution-ledger.md`.

**Fact:** C5 replaced copied version bags with content snapshots, reference-only
views, owner-local semantic objects, `AuthorityBoundValue`, and structural
closure. C6 then removed residual Git lineage and complete views, separated
Authority and Contracts, froze owner/kind/payload/identity/dependency
membership, qualified roots by side/role, and attempted to bind all authority
for every possible future transition. Source:
`748d30f7:docs/archive/plans/standards-engine-a1b/reports/c6-c7-design-history-research.md`.

**Recorded rationale:** independent version and authority scopes would avoid
invalidating unrelated consumers, while transition-complete closure would make
every advertised continuation replayable.

**Counterevidence:** the C6/C7 history found no algorithm for C6's future
transition closure and emphasized that `NextOperation` had always been
structural guidance, not authorization. C6's direct-file store also created
application-owned publication, locking, cleanup, and durability machinery.
Same source and
`748d30f7:docs/archive/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md`.

### C7: a simplification relative to C6

**Fact:** C7 deliberately removed several C6 mechanisms:

- persisted transitive dependency lists became roots-only closure with derived
  transitive identity;
- hypothetical future transition authority became authority actually consumed
  by a successful child;
- structural snapshots became exact logical-path/raw-byte mappings;
- a native hard-link object-file protocol became one SQLite table;
- ambient/aggregate operation and trust authority became four executable
  operation records plus direct consumed trust; and
- generic semantic-ID parsing became opaque owner-local identifiers.

Source:
`36dd7579:docs/archive/plans/standards-engine-a1b/reports/c7-design-proposal.md`.

**Recorded rationale:** SQLite supplied writer serialization, crash recovery,
backup, and transactional publication behind a smaller storage Adapter; exact
leaf content and roots-only closure removed non-material capture and repeated
dependency authority. Source:
`36dd7579:docs/archive/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md`.

**Counterevidence:** C7 was a simplification only relative to the already large
C6 authority design. It retained direct storage for every inspectable object,
owner codecs, a seven-field envelope, per-operation records, a broad trust
algebra, exact package governance, and extensive evidence obligations. The
deletion of C6 machinery does not establish that the remaining C7 machinery was
minimal relative to the accepted A1 behavior.

## Accepted Requirements And Guarantees

The accepted objective in
`84412f22:docs/archive/plans/standards-engine-a1b/plan.md` requires all of the following:

| Guarantee | Accepted implementation mechanism | Historical origin |
| --- | --- | --- |
| Preserve query, prepare, resolve, and inspect with immutable analysis state. | `StandardsEngine` facade and generated request/result algebra. | Preserved A1 product architecture. |
| Correct Draft equality and avoid local keyword duplication. | `jsonschema.Draft202012Validator` behind `standards_contracts`; generated values delegate runtime validation. | Reproduced Unicode defect plus generated-contract recovery policy. |
| Cover every operation-reachable request/result definition. | Closed interface TOML, 140-definition schema closure, generated Python and agent-tool projections. | Historical partial-generation failures and recovery policy. |
| Separate schema equality, applicability equality, identity, ordering, and deduplication. | Identity v2 plus owner-local typed records and keys. | Reproduced equality conflation and `396144ad` authority-scope standards. |
| Reconstruct every advertised handle without ambient mutable state. | Direct immutable objects, exact references, owner codecs, SQLite, and public cold composition. | Redesign brief plus immutable-authority-closure standard. |
| Bind only material operation authority. | Reference-only views, four operation records, qualified roots, roots-only derived closure. | C4-C7 version/authority-scope reviews. |
| Replay existing results without live trust. | Direct provider and authorization objects stored only for successful child states. | Immutable-authority rule and C5-C7 review. |
| Replace A1 atomically with no compatibility layer. | V11/v3/v4 coordinated cutover and deletion of old paths. | Inventory found no external consumer or retained state. |
| Prove local durable publication and recovery. | SQLite schema v1, exact transaction profile, real syscall interruption, verified backup and non-overwriting restore. | C7 persistence selection plus review findings. |
| Enforce package ownership and public imports. | Manifest roots/entrypoints, static `__all__`, AST governed-source profile, safe-path clean-environment execution. | Historical private-import repair, generated-contract policy, and repeated review findings. |
| Reconcile every changed policy consumer and coverage subject. | Policy-impact registry, migration table, suite-input horizon, authorization, attestations, certificates, exact set equality. | Standards recovery and coverage system. |

**Fact:** the consumer inventory found no independently deployed consumer and
no retained A1 persisted state; it therefore selected a coordinated breaking
replacement and prohibited dual readers, converters, aliases, and fallback
decoders. Source:
`84412f22:docs/archive/plans/standards-engine-a1b/reports/consumer-and-state-inventory.md`.

**Inference:** compatibility machinery was correctly excluded on the recorded
facts. That decision does not itself justify the size of the new persistence
and reconstruction machinery; it only shows that old/new coexistence was not
required.

## Recorded Alternatives And Their Fate

| Alternative | Recorded disposition | What the evidence establishes |
| --- | --- | --- |
| Continue A1's local Draft subset and generated decoder | Rejected after the reproduced equality disagreement and duplicated semantics audit. | Strong evidence supports rejection: the selected external contract and local behavior actually disagreed. `84412f22:docs/archive/plans/standards-engine-a1b/reports/dependency-and-dialect-decision.md`. |
| Use a code-first model library | Rejected because model semantics plus schema projection would retain two authorities. | Recorded design rationale; no implementation comparison was performed. Same source. |
| Scatter direct `jsonschema` calls | Rejected because reference, profile, and diagnostic policy would be duplicated. | The deep Contracts Module has a clear deletion-test case. Same source. |
| Three aggregate stored roots or bounded snapshot bundles | Preferred by the initial independent design review, then rejected when exact child cold inspection and identity closure were found incomplete. | This was a real simpler alternative, not merely hypothetical. It was not revisited after direct-object inspection became binding. `44de7dff:docs/archive/plans/standards-engine-a1b/execution-ledger.md`. |
| C6 native ext4 directory/hard-link object store | Rejected for application-owned staging, locking, synchronization, cleanup, and recovery. | SQLite is demonstrably simpler than C6 for the same selected durability guarantee. `36dd7579:docs/archive/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md`. |
| Persist the flattened transitive closure | Rejected because it duplicates immutable direct references and the same traversal. | Roots-only closure removes a non-independent representation while retaining the derived identity. `36dd7579:docs/archive/plans/standards-engine-a1b/reports/c7-design-proposal.md`. |
| Aggregate provider and authorization views | Rejected because unrelated trust changes invalidate results and replay can become ambient. | Direct consumed trust has stronger materiality, although the required trust-model detail remains open. `84412f22:docs/decisions/standards-engine-a1b.md`. |
| Retain A1 compatibility readers or migrate old state | Rejected because inventory found no external consumer or retained state. | Strong evidence supports a breaking replacement on the recorded repository facts. `84412f22:docs/archive/plans/standards-engine-a1b/reports/consumer-and-state-inventory.md`. |
| Put SQLite or semantic exports in Git; store authored declarations as SQL | Rejected because authored standards need reviewable text and machine state is local/generated. | Strong ownership rationale; no A1c reason to reverse it is recorded. `84412f22:docs/decisions/standards-engine-a1b.md`. |
| Support arbitrary raw-byte paths, macOS, Windows, other filesystems, migrations, GC, or remote storage immediately | Rejected or deferred because no admitted consumer required them and evidence was absent. | This is appropriate scope restraint, though it leaves a deliberately narrow operational profile. Same source and the accepted plan. |

**Inference:** candidate history compared many representations within the
immutable direct-object premise, but after Candidate C no later design returned
to a radically smaller aggregate Module Interface. C7 compared itself mainly
with the larger C6 design. A1c may therefore revisit a bounded aggregate design
without claiming that A1b already disproved every such design; it must still
preserve whatever child inspection and replay guarantees the integrated audit
selects as externally meaningful.

## Accepted Module, Interface, Seam, And Adapter Design

### External Engine seam

**Fact:** the accepted lifecycle has four operations, but the full public
Interface is larger than four method names. It also includes three construction
paths (`open_repository`, `open_analysis`, `open_persisted`), configuration and
failure obligations, opaque handle rules, operation ordering, and the complete
generated request/result algebra. At `84412f22`, the generated Module exports
142 names and the Engine root adds four owned exports. Sources:
`84412f22:tools/standards_engine/standards_engine/engine.py`,
`84412f22:tools/standards_engine/standards_engine/_generated_contract.py`, and
`84412f22:tools/standards_engine/standards_engine/__init__.py`.

**Inference:** the four-operation facade has high behavioral Leverage, but
describing it as a four-item Interface understates the caller knowledge carried
by the 140-definition public algebra, construction modes, failure taxonomy, and
continuation handles. A1c should measure the Interface that callers must learn,
not only count operation methods.

### Foundation Modules

| Module | Accepted Interface role | Seam/Adapter evidence | Depth observation |
| --- | --- | --- | --- |
| `standards_identity` | Typed encoding and domain-separated hashing only. | Pure in-process; no Adapter is needed. | Seven exports hide byte framing and very-large-integer encoding; comparatively deep. |
| `standards_contracts` | Compile schema/interface, decode values, project artifacts, stable failures. | One maintained Draft implementation is adapted; projection is build-time. | Seventeen exports hide reference resolution, reachability, profile admission, validation, and generation; comparatively deep, though projections remain broad. |
| `standards_authority` | Envelopes, repositories, capture, closure, SQLite recovery, Git-index commands, typed failures. | `MemoryObjectStore` and `SQLiteObjectStore` are two real storage Adapters; `GitCaptureSource` and `NativeCaptureSource` are two real capture Adapters. | Forty-eight exports expose much of the persistence/capture machinery; the Module supplies substantial behavior but its Interface is not small. |
| Domain Modules | Own semantic models, typed identity records, codecs, dependency extraction, ordering, and transitions. | Codec sets are owner-local internal composition seams, not independently deployed Adapters. | Analysis exported 137 names at the accepted tree, making the owner vocabulary broad. |
| `standards_engine` | Compose Modules, select operation roots, adapt internal outcomes to generated results. | External seam is the caller facade; lower seams remain internal in principle. | High capability, but a 2,539-line composition implementation and large generated Interface concentrate coordination. |
| `standards_verifier` | Enforce package, import, entrypoint, suite-input, graph, and migration contracts. | Uses public owner Adapters but also implements the governed-source AST model. | Six root exports hide a large implementation; the Module is deep for callers but costly to maintain. |

Export counts are reproducible from
`84412f22:tools/standards_identity/standards_identity/__init__.py`,
`84412f22:tools/standards_contracts/standards_contracts/__init__.py`,
`84412f22:tools/standards_authority/standards_authority/__init__.py`, and
`84412f22:tools/standards_analysis/standards_analysis/__init__.py`; the
Engine/generated counts use
`84412f22:tools/standards_engine/standards_engine/_generated_contract.py`.
They are navigation and Interface diagnostics, not automatic rejection rules.

### Locality and the deletion test

**Fact:** one persisted semantic kind generally requires an owner model,
payload contract, identity record, codec, dependency extractor, envelope,
handle/public projection, operation-role admission where applicable, migration
disposition, policy relationship, and focused/integration evidence. The closed
kind/contract/identity/dependency table is recorded at
`84412f22:docs/archive/plans/standards-engine-a1b/reports/c7-design-proposal.md`; actual
owner codecs are composed from public roots at
`84412f22:tools/standards_engine/standards_engine/authority.py`.

**Inference:** owner-local codecs improve semantic ownership, but changes that
cross public inspection, persistence, or operation closure have low Locality:
the owner, Authority, Engine composition, generated contract, migration graph,
coverage, and tests may all need coordinated changes. A1b proves that these
edits can be made consistently; it does not prove that the edit path is the
least sufficient one.

**Deletion-test assessment:** deleting Identity or Contracts would spread byte
encoding or schema semantics back across callers, so those Modules clearly earn
their seams. Deleting the generic repository would spread persistence and
resolution across many owners, so it also hides real complexity. The weaker
case is not the repository itself but the number of separately represented and
publicly inspectable objects placed behind it. The evidence does not show
whether all of those objects need independent public identity rather than a
smaller aggregate Interface.

## Representations And Versions

**Fact:** A1b atomically selected interface/schema 11, request 3, result 3,
public handle 4, identity encoding 2, authority envelope 1, SQLite schema 1,
owner payload contracts, owner identity domains, and four typed operation
compatibility keys `(route, 2)`, `(read, 2)`, `(related, 2)`, and `(analysis,
2)`. The former analysis umbrella versions were removed. Source:
`84412f22:docs/archive/plans/standards-engine-a1b/reports/identity-version-object-matrix.md`.

**Recorded rationale:** representation, semantic identity, public handle,
result projection, operation compatibility, and storage schema can change for
different reasons and therefore must not share an umbrella version. The
accepted `396144ad` Contracts standard required independently changing promises
to have independent scopes and allowed shared coordination without a shared
version. Source: `396144ad:topics/contracts.md`.

**Fact:** the v11 public schema is 3,890 lines with 140 definitions at the
accepted implementation, and generated Python exports 140 definition types plus
`DEFINITION_METADATA` and `decode_contract`. Sources:
`84412f22:tools/standards_engine/contracts/a1-contract.schema.json` and
`84412f22:tools/standards_engine/standards_engine/_generated_contract.py`.

**Inference:** A1b fixed umbrella invalidation but expanded the compatibility
matrix. This may be correct ownership and still be expensive. The standards
supplied strong tests against under-separation; surviving artifacts do not show
an equivalent whole-system test against many individually justified version
scopes whose consumers still replace atomically.

## Durable Authority And Operational Profile

**Fact:** every advertised handle directly resolves an immutable seven-field
envelope. Authority verifies canonical bytes, exact handle/envelope/reference
agreement, owner-recomputed identity, direct dependencies, and cycles; owner
codecs validate semantic payloads. SQLite stores only `(handle, envelope)` and
exposes immutable `get`/`put_if_absent`, backup, offline non-overwriting
restore, integrity checks, and cold reopen. Sources:
`84412f22:docs/decisions/standards-engine-a1b.md`,
`84412f22:tools/standards_authority/standards_authority/repository.py`, and
`84412f22:tools/standards_authority/standards_authority/store.py`.

**Fact:** the durable/native profile is CPython 3.11/3.12, Linux x86-64, glibc
2.17 or newer for selected wheels, local case-sensitive non-casefold ext4, an
admitted SQLite capability profile, and a capability-checked host `strace`
oracle for real `fsync`/`fdatasync` interruption. Other platforms,
filesystems, architectures, non-UTF-8 names, streaming capture, migrations,
semantic export/import, deletion, enumeration, remote storage, and garbage
collection are outside scope. Sources:
`84412f22:docs/archive/plans/standards-engine-a1b/plan.md`,
`84412f22:docs/archive/plans/standards-engine-a1b/reports/a1b-dependency-provenance.md`,
and
`84412f22:docs/archive/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md`.

**Recorded rationale:** narrow required-real support was preferable to inferred
portability, and SQLite removed more application-owned durability machinery
than it introduced relative to C6's direct-file design.

**Inference:** this is a coherent explicit tradeoff, not an accidental false
portability claim. It nevertheless makes A1b operationally narrower and gives
a repository-local standards engine substantial database, filesystem,
dependency-provenance, backup/restore, and fault-injection obligations.

**Unresolved:** the repository inventory established no external consumer and
no retained state. It did not identify a real consumer that independently
required SQLite durability, offline backup/restore, deterministic
during-commit killing, or direct cold inspection of every child kind rather
than the already passing A1 reconstruction paths. The redesign brief and
accepted immutable-authority standard supplied those guarantees as design
requirements.

## Import, Source, And Verification Governance

### How package enforcement expanded

**Fact:** the redesign brief required generated/facade imports to use documented
package entry points. Candidate reviews expanded that into manifest-owned
public roots and entrypoints, statically resolvable `__all__`, AST-derived
production ownership, rejection of private/alternate/star/dynamic imports,
safe-path clean-environment execution, and eventually a bounded
execution-aware model for Python bindings and possible import-capability
provenance. Sources:
`3439aae9:docs/archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`,
`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`, and
`84412f22:tools/standards_verifier/standards_verifier/python_packages.py`.

**Fact:** the last four rejected implementation boundaries were dominated by
this enforcement Module: `sys.modules` acquisition, working-tree versus index
authority, class/comprehension lookup, assignment binding lifetime, hostile
Git environment, conditional binding/deletion, nested `sys` provenance, and
augmented-assignment order. The accepted scanner implementation is 1,419 lines;
its accepted correction matrix has 45 tests on each supported Python version.
Sources:
`580d9c95:docs/archive/plans/standards-engine-a1b/execution-ledger.md`,
`84412f22:tools/standards_verifier/standards_verifier/python_packages.py`, and
`580d9c95:docs/archive/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`.

**Recorded rationale:** public-root enforcement would make historical private
import leakage difficult, and conservative capability tracking would reject
alternate runtime-import machinery without pretending to interpret arbitrary
adversarial Python.

**Inference:** this is the clearest case where assurance machinery became a
major implementation in its own right. It protects repository dependency
policy, not the semantic behavior of query/prepare/resolve/inspect. Its bugs
repeatedly blocked A1b acceptance even after the C7 runtime architecture was
retained. That does not prove the enforcement is useless; it does prove that
standards conformance and review closure materially increased A1b's delivery
cost outside the core Engine behavior.

### Accepted evidence portfolio

**Fact:** final review recorded 679 package tests, separate required-real
evidence, 226 registered declarative suites, 53 retained Bash migration
checkers, generated freshness, Ruff, plan validation, and diff hygiene.
Standards Analysis contributed 66 tests, Engine 36, and Verifier 433. Source:
`580d9c95:docs/archive/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`.

**Fact:** three A1b declarative suites combine behavioral check types with text
and path-state assertions:

- `84412f22:evaluation/standards-effectiveness/suites/a1b-contract-conformance.toml`;
- `84412f22:evaluation/standards-effectiveness/suites/a1b-authority-reconstruction.toml`;
- `84412f22:evaluation/standards-effectiveness/suites/a1b-public-cutover.toml`.

Their path-state assertions serve migration/presence/deletion claims; they do
not independently prove runtime semantics. Runtime behavior is supplied by
package and integration tests. The 53 retained Bash checkers were not extended
for A1b, but their inventories and graphs changed when new executable inbound
references appeared. Sources:
`8b8a4b48:docs/archive/plans/standards-engine-a1b/execution-ledger.md` and
`84412f22:evaluation/standards-effectiveness/suites/a1b-public-cutover.toml`.

**Counterevidence to a blanket redundancy claim:** many checks have distinct
oracles: external validator selection, generated freshness, owner-codec
identity, SQLite required-real interruption, fresh-interpreter reconstruction,
public facade results, and migration deletion do not prove the same property.
The final acceptance also expressly avoided mutable catalog-count and hardcoded
generated-identity assertions.

**Unresolved:** no A1b report maps every check to a reachable failure,
material consequence, independent oracle, proof substitution, overlap, and
removal condition. Passing every layer proves the accepted claims; it does not
establish the marginal value of every layer. The audit's separate verification
portfolio report must decide this check by check rather than from totals.

## Complexity Provenance Classification

This classification describes what the history proves about origin. It does
not decide whether an item should remain in A1c.

| Machinery or obligation | Proven origin | Classification and confidence | Evidence |
| --- | --- | --- | --- |
| Maintained Draft validator | Directly fixes the reproduced Unicode equality defect and removes two local interpreters. | **Explicitly required; high confidence.** | `3439aae9` brief; `c4408363` equality reproduction; `84412f22:tools/standards_contracts/`. |
| Complete generated public closure | Responds to historical partial generation and public-result leakage; required by recovery policy. | **Defect- and standards-driven; high confidence.** | `3439aae9` brief; `a3f5312d` compiler checkpoint. |
| Codepoint-preserving identity v2 | Separates representation identity from schema/domain equality. | **Defect-driven core, review-expanded details; high confidence.** Exact huge-integer grammar and custom chunk conversion came from the admitted contract rather than a known product input. | `eee83026` ledger entry; identity matrix at `84412f22`. |
| Direct object storage for every inspectable kind | Introduced after aggregate-root review; makes one cold lookup rule structural. | **Review- and standards-driven; medium confidence.** Accepted A1 already passed bounded cold child inspection, so the need for universal direct storage is preventive. | `44de7dff` ADR; `c4408363` A1 reproductions. |
| Seven-field envelope and owner-local codecs | Separates storage integrity from domain semantics under authority-scope rules. | **Standards- and review-driven; high confidence.** | `396144ad` standards; `ac362dc5` through `36dd7579` ledger. |
| Many scoped payload/identity/handle/result/operation versions | Replaced copied umbrella versions under the new version-scope rule. | **Standards-driven; high confidence.** Necessity of every independent scope to an actual consumer remains unresolved. | `396144ad:topics/contracts.md`; identity matrix at `84412f22`. |
| Roots-only closure | Simplifies C6 repeated dependency lists and binds material authority. | **Architecture-driven simplification; high confidence.** | C7 proposal at `36dd7579`. |
| Direct provider/authorization objects and closed evidence algebra | Prevents replay through ambient live trust and avoids broad aggregate invalidation. | **Immutable-authority standard plus review-driven contract closure; high confidence.** Threat-model proportionality remains unresolved. | `ac362dc5`/`ee7f2a47` ledger; accepted ADR at `84412f22`. |
| SQLite, backup/restore, and `strace` interruption | Replaced more complex C6 direct-file publication and proves required-real durability. | **Review-selected operational mechanism; high confidence.** Whether the product needed this durability level remains unresolved. | C7 SQLite audit at `36dd7579`; authority checkpoint `45163746`. |
| Exact wheel/source/license/hash/OSV provenance | Required by Dependencies, Licensing, Release, Security, and plan review. | **Standards- and review-driven; high confidence.** | dependency decision/provenance at `84412f22`. |
| Policy-impact migration, suite-input horizon, grants, attestations, certificates | Required to update and prove standards-consumer coverage after changing governed artifacts. | **Standards-infrastructure-driven; high confidence.** | recovery consumer dispositions `a166e36f`; A1b issues A1B-009/021/022/027 at `84412f22`. |
| Manifest/import/entrypoint AST verifier | Began with a real A1 private-import defect and expanded through repeated review. | **Defect-triggered but predominantly review-driven in final scope; high confidence.** | A1b brief `3439aae9`; ledger `d6117216` through `84412f22`. |
| C6-R-T-S exact Git topology protocol | A plan-local attempt to make review ancestry mechanical. | **Incidental process complexity; high confidence.** It was removed and a general standards correction prohibited it. | `d06c819b` plan; `1d18b70d:workflows/planning.md`. |
| C1-C6 planning artifacts and rejected machine schemas | Necessary historical evidence after rejection, not accepted runtime authority. | **Development/process residue; high confidence.** | accepted plan planning boundary at `580d9c95`. |
| Full test/verifier portfolio | Mixes unique semantic, operational, migration, and governance claims. | **Mixed and unresolved.** Counts cannot decide necessity. | final acceptance `580d9c95`; three A1b suite definitions at `84412f22`. |

## Process And Replanning Cost

**Fact:** `git diff --numstat c4408363 84412f22` reports 71,478 added and
18,328 deleted lines across 258 changed paths. At `84412f22`, A1b reports
contain 8,645 lines; the plan, ledger, issues, and ADR contain another 2,857.
These figures include generated contracts, policy/coverage projections,
fixtures, reports, and replacement of prior code. They are reproducible
diagnostics, not an architectural verdict.

**Fact:** major accepted-tree implementation concentrations include:

- `tools/standards_engine/standards_engine/engine.py`: 2,539 lines;
- `tools/standards_engine/standards_engine/authority.py`: 868 lines;
- `tools/standards_analysis/standards_analysis/authority.py`: 1,342 lines;
- `tools/standards_verifier/standards_verifier/python_packages.py`: 1,419 lines;
- public schema: 3,890 lines and 140 definitions.

All measurements are from commit `84412f22` at the named paths. They indicate
where review and change effort may concentrate; they do not measure Depth as a
line-count ratio.

**Fact:** the first atomic cutover (`d6117216`) changed 140 files with 20,845
additions and 17,784 deletions. Later correction commits repeatedly regenerated
or renewed large migration/coverage artifacts: `ead04bc5` changed 54 files and
`8b8a4b48` changed 78. Sources are the corresponding commit diffs.

**Inference:** A1b's atomic no-compatibility cutover avoided permanent parallel
runtime paths, but it made review corrections expensive because code,
generated projections, policy relationships, suite inputs, coverage authority,
and evidence had to move together. The process achieved consistency at the
cost of low incremental Locality.

## Counterevidence Against A One-Sided "A1b Is Excess" Conclusion

- **Fact:** A1b removed the known nonconforming local Draft equality behavior
  and did not replace it with another local validator.
- **Fact:** C7 removed substantial C6 machinery: native hard-link publication,
  persisted transitive lists, structural snapshot metadata, hypothetical
  future authority, aggregate trust views, and semantic-ID parsing.
- **Fact:** memory/SQLite storage and Git/native capture are real two-Adapter
  seams, not test-only hypothetical seams.
- **Fact:** the coordinated cutover deleted the old validator, generic NFC
  serializer, split/directory stores, version bags, old generated model path,
  and compatibility fallbacks rather than layering replacements indefinitely.
- **Fact:** independent final review found zero findings against the admitted
  plan and reproduced the last defect family on both supported runtimes.

Sources:
`580d9c95:docs/archive/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`,
`84412f22:docs/archive/plans/standards-engine-a1b/reports/a1b-cutover-evidence.md`, and
`84412f22:docs/decisions/standards-engine-a1b.md`.

These facts establish correctness relative to the selected guarantees and show
that some complexity replaced worse or duplicated machinery. They do not
establish proportionality.

## Evidence-Constrained Implications For Standards And A1c

These are audit hypotheses for later synthesis, not normative changes or a
binding A1c architecture.

1. **Preserve observable guarantees, not A1b's internal shape.** The four
   operations, corrected schema equality, complete public behavior, immutable
   issued results, and declared failure behavior have strong historical
   evidence. Individual codecs, records, package seams, and verification
   mechanisms do not automatically have the same status.

2. **Separate current defect evidence from preventive structure.** The Unicode
   equality defect was current and externally grounded. Universal direct-child
   storage, SQLite durability, exact trust records, and the governed-source
   abstract interpreter were largely preventive or governance mechanisms.
   A1c should require each to restate the reachable failure and consequence it
   uniquely prevents.

3. **Re-run the deletion test above the individual owner.** A1b's standards
   reviewed each authority and version for coherent ownership. A1c should also
   test whether deleting or merging several adjacent representations makes
   complexity disappear or merely moves essential work to callers.

4. **Measure representative change Locality before design admission.** Add one
   public field, add one inspectable kind, change one identity rule, change one
   operation role, and change one internal import. Record every Module,
   version, generated artifact, relationship, coverage record, and test that
   must change.

5. **Keep internal seams internal.** Store and capture have demonstrated
   multiple Adapters. Owner codec and verification seams should not be exposed
   beyond the smallest Module Interface merely because internal tests need
   them.

6. **Make the Interface the primary test surface.** Preserve a small
   characterization suite for meaningful A1b behavior, then retain internal
   tests only where they protect a distinct risky invariant that cannot be
   observed adequately through a deeper Module Interface.

7. **Threat-model trust and validation by seam.** User/arbitrary input,
   persisted bytes, Git/native capture, dependency artifacts, and
   authorization are real validation seams. Already constructed immutable
   owner values inside one process should not be treated as untrusted at every
   hop without a named mutation or corruption path.

8. **Distinguish policy-governance tooling from product runtime.** Package
   import enforcement and coverage certification may remain valuable repository
   tooling, but their defects should not automatically redefine whether the
   four-operation Engine design is complete.

## Unresolved Questions For The Integrated Audit

1. Which exact commit should represent A1 in the fair architecture comparison:
   accepted implementation `2359a987`, final acceptance record `933c9ab9`, a
   later repair/amendment, or the standards-recovery base?
2. Which A1b guarantees were demanded by an actual Engine consumer, and which
   became requirements only through the redesign brief or standards recovery?
3. Does every one of the closed inspectable object kinds require independent
   public identity and cold inspection, or could a deeper aggregate Module
   preserve the actual caller workflows?
4. Which independently scoped versions have consumers that can genuinely
   evolve independently rather than only theoretical change reasons?
5. Does the authorization/provider algebra correspond to an actual adversarial
   or independently deployed trust seam, or primarily to repository-internal
   correctness policy?
6. Is durable SQLite state retained in real operation, and if so, what are its
   lifecycle, size, cleanup, and recovery consumers? A1b deliberately has no
   enumeration, deletion, migration, or garbage collection.
7. Which package-import scanner failures could have produced a real hidden
   dependency in accepted code, and which only violate a maximal static
   enforcement profile already covered by ordinary runtime/import failure?
8. Which of the 679 package tests, 226 suites, 53 Bash checkers, digests, and
   freshness gates have unique failure coverage after proof substitution?
9. Would a smaller typed public algebra preserve all real callers, or are all
   140 generated definitions directly consumed?
10. The accepted ADR retrospectively says C1-C6, while the contemporaneous
    ledger uses initial candidate, C, C-prime, C2-C7. Should the integrated
    audit retain only commit identities to avoid inventing a false ordinal
    history? This report recommends yes.

## Conclusion

**Fact:** A1b is an accepted, internally coherent correction of A1's contract
equality and semantic-authority design under the standards in force. It
preserves the read-only lifecycle, removes parallel legacy implementations,
and supplies stronger replay, durability, package, migration, and evidence
guarantees than A1.

**Inference:** the same history shows why concern about excess machinery is
well founded. Several A1 failure families were already behaviorally repaired
at the accepted A1 tree; A1b converted them into stronger structural
guarantees. New authority/version standards pushed the design from copied
umbrellas toward many owner-scoped representations. Repeated content review
then expanded package, Git, suite-input, and coverage enforcement until those
systems dominated the last implementation corrections. A1b's acceptance proves
the selected machinery works together, not that all of it is necessary.

The defensible next step is therefore not to discard A1b's guarantees or to
preserve its structure wholesale. The integrated audit should identify the
smallest externally meaningful guarantee set, classify each internal mechanism
by unique reachable risk and consumer, and use A1c to test whether greater
Depth and Locality can preserve those guarantees with fewer representations,
versions, validation paths, and evidence layers.
