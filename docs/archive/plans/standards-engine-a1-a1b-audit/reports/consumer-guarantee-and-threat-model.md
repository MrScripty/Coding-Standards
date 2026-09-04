# Standards Engine Consumer Guarantee And Threat-Model Audit

**Status:** Historical and design evidence complete for `AUD-A4C`

**Audited boundaries:** accepted A1 v9 `2359a98740b6035a0414bfaf5427ceaa1301a1c8`,
accepted policy-impact-v2 A1 v10
`7bc8bd070f882eb9779dc678139777d05a6ce7c7`, admitted A1b plan base
`36dd75790b2f08a6e66624ccae4f8530bc111a92`, and accepted A1b
`84412f22fa9fe082f089eaa347c30c23f185ffee`.

**Purpose:** Determine which guarantees have real consumers or demonstrated
failure paths, which were selected by plans, standards, or review, and what
scoped risks they answer. This report supplies evidence and questions for A1c;
it does not select an A1c architecture or rescind A1/A1b acceptance.

## Method And Evidence Discipline

This audit uses repository-owned primary evidence: fixed Git objects, plans,
ADRs, ledgers, reports, source, manifests, schemas, generated artifacts, and
call-site searches. The three historical reports already produced by this
audit are used as navigation and corroboration:

- [A1 history and design](a1-history-and-design.md)
- [A1b history and design](a1b-history-and-design.md)
- [Standards evolution and causality](standards-evolution-and-causality.md)

A citation such as
`c7d23dfa:docs/archive/plans/standards-engine-navigation-analysis/plan.md` identifies
the file at that immutable commit. Search results are described with their
exact revision and scope so they can be reproduced with `git grep`.

The following labels are used consistently:

- **Fact** — directly present in a cited source, commit, or call-site search.
- **External-product demand** — required by a consumer with authority outside
  the repository's coordinated implementation and acceptance process.
- **External semantic constraint** — behavior constrained by an authority such
  as JSON Schema Draft 2020-12; this does not establish an external product
  consumer.
- **Repository-process demand** — required by this repository's planning,
  verification, migration, coverage, or release workflow.
- **Plan-selected** — made an acceptance criterion by an admitted A1 or A1b
  plan, whether or not an independent consumer requested it.
- **Standards-mandated** — required or strongly constrained by the applicable
  general standards snapshot.
- **Review-added** — entered or materially expanded after an independent
  candidate review finding.
- **Implementation choice** — one mechanism selected to satisfy a guarantee;
  the guarantee did not uniquely imply that mechanism.
- **Inference** — the audit's evidence-constrained interpretation.
- **Counterevidence** — evidence that narrows a stronger claim.
- **Unresolved** — the repository does not establish the answer.

Tests, fixtures, generated artifacts, plans, and review reports are evidence
producers or acceptance authorities. They are not counted as independent
product consumers merely because they instantiate a public type or call an
operation.

## Executive Findings

1. **Fact:** no independently deployed Standards Engine consumer was found at
   accepted A1 v9, accepted A1 v10, the A1b planning base, or accepted A1b.
   At all three runtime boundaries, the only non-test caller of the four
   public operations is the Engine-owned `AgentToolFacade`; A1 v9/v10 also
   redispatches some calls between snapshot-bound Engine instances. No
   non-test Python source outside `tools/standards_engine/` imports the
   `standards_engine` package. The accepted A1b consumer inventory independently
   records repository-local tests and examples as the public consumers and
   reports no deployed process, foreign-language binding, independently
   versioned tool-file consumer, or retained A1 state.
   (`2359a987:tools/standards_engine/standards_engine/tools.py`;
   `7bc8bd07:tools/standards_engine/standards_engine/tools.py`;
   `84412f22:tools/standards_engine/standards_engine/tools.py`;
   `84412f22:docs/archive/plans/standards-engine-a1b/reports/consumer-and-state-inventory.md`)

2. **Fact:** several guarantees nevertheless answer demonstrated defects or
   credible boundary failures. A1 actually returned live worktree bytes behind
   an immutable handle; cold child inspection actually depended on fresh or
   process-local authority; A1's two local schema implementations actually
   agreed with each other while disagreeing with the selected Draft on Unicode
   equality; A1 code crossed private package boundaries; and late A1b
   implementations actually allowed hostile inherited `GIT_*` variables to
   redirect Git operations. These are stronger evidence than test counts.
   (`933c9ab9:docs/archive/plans/standards-engine-navigation-analysis/issues.md`,
   SENA-021 and SENA-022;
   `c4408363:docs/archive/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`;
   `580d9c95:docs/archive/plans/standards-engine-a1b/execution-ledger.md`)

3. **Fact:** the four-operation read-only product, typed public algebra,
   immutable snapshots/results, successful-empty impact certification,
   authorization-aware resolution, and inspection were selected by A1's plan.
   Their origin is the repository's product brief and planning process, not a
   discovered external consumer contract. A1b preserved that product shape
   and selected materially stronger cold replay, direct child storage,
   transitive authority closure, durable SQLite publication and recovery,
   public-package enforcement, and exact migration/coverage reconciliation.
   (`c7d23dfa:docs/archive/plans/standards-engine-navigation-analysis/plan.md`;
   `36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`)

4. **Fact:** accepted A1 already passed bounded fresh-process reconstruction
   of context, requirement, observation, and certificate handles after its
   repairs. A1b's universal direct-object repository therefore converts a
   bounded behavior into a stronger structural guarantee; it is not merely the
   first repair of still-failing child inspection.
   (`c4408363:docs/archive/plans/standards-engine-standards-recovery/reports/historical-a1-repair-reproductions.md`)

5. **Fact:** A1b's durable recovery surface has no non-test operational caller
   in the accepted tree. `StandardsEngine.open_persisted` is called only by two
   Engine test files. `StoreRecovery.backup` and `restore` are implemented in
   production, but every call site is in Authority tests. This does not make
   the behavior false or useless; it establishes that the plan and review,
   rather than an operating consumer, demanded it.
   (`84412f22:tools/standards_engine/standards_engine/engine.py`;
   `84412f22:tools/standards_authority/standards_authority/recovery.py`;
   `84412f22:tools/standards_engine/tests/test_analysis.py`;
   `84412f22:tools/standards_engine/tests/test_c7_analysis.py`;
   `84412f22:tools/standards_authority/tests/test_sqlite_store.py`)

6. **Inference:** the evidence supports preserving boundary properties more
   strongly than preserving A1b's mechanisms. Decode arbitrary input at its
   entry Seam, keep issued results independent of later mutable source, use
   the selected external schema semantics, preserve explicit uncertainty,
   prevent ambient substitution during any promised replay lifetime, and do
   not report empty impact as complete without an adequate coverage claim.
   The evidence does not independently require one stored object per child,
   the seven-field generic envelope, every current version scope, SQLite for
   all uses, backup/restore in the product Module, or a 1,419-line Python
   capability analyzer.

7. **Unresolved:** no source identifies the real intended deployment and
   retention contract for A1c: in-process assistant tool, local command-line
   tool, long-running service, durable repository appliance, or reusable
   library. That choice materially changes the necessary handle lifetime,
   authorization model, persistence guarantees, package boundaries, and
   threat model. It must be made before internal machinery is treated as a
   permanent compatibility promise.

## Actual Consumers And Retained State

### Production call-site inventory

The following inventory deliberately excludes tests, fixtures, examples, and
documentation from the consumer count.

| Boundary | Production caller evidence | What is not present |
| --- | --- | --- |
| A1 v9 `2359a987` | `AgentToolFacade.query`, `prepare`, `resolve`, and `inspect` call the corresponding `StandardsEngine` methods. The Engine also redirects query/inspection to a snapshot-bound Engine source. | No non-test import of `standards_engine` outside its own package; no CLI, network listener, service, foreign binding, or independently released client. |
| A1 v10 `7bc8bd07` | Same Engine-owned facade and snapshot redispatch pattern after the policy-impact-v2 amendment. | No new independent consumer; the amendment changes internal policy-impact authority and public versioning. |
| A1b plan base `36dd7579` | Production still uses the A1 v10 facade; the A1b runtime is not yet implemented. | Planning artifacts are design authority, not runtime consumers. |
| A1b `84412f22` | `AgentToolFacade` remains the only non-test caller of the four methods. `open_repository` and `open_analysis` construct the facade and compile its contract. | No non-test caller of `open_persisted`; no operational caller of backup/restore; no non-test external package import. |
| Repository governance at `84412f22` | The Verifier's `PythonPackageContractCheck` calls `audit_python_packages` and `execute_python_package_contract`; the suite-input compiler and package verifier consume the sanitized Git-index Adapter. | These are real repository-process consumers, but they do not consume the four-operation Standards Engine product. |

Reproduction searches:

```text
git grep -n -E '\.(query|prepare|resolve|inspect)\(' <revision> -- '*.py' ':!**/tests/**'
git grep -n -E '(from|import)[[:space:]]+(tools\.)?standards_engine' <revision> -- '*.py' ':!**/tests/**'
git grep -n 'open_persisted' 84412f22 -- '*.py'
git grep -n -E 'backup\(|restore\(' 84412f22 -- '*.py'
```

**Counterevidence:** lower A1/A1b Modules do have production consumers. For
example, Metadata, Graph, Policy Impact, Analysis, and Verifier consume each
other through declared repository-local boundaries. The conclusion is not
that all packages are test-only. It is specifically that no independent
consumer establishes the necessity of the complete four-operation public
algebra, every inspectable child, or durable replay/recovery profile.

### Persisted-state inventory

**Fact:** A1 v9 and v10 expose `InMemoryAnalysisStateStore` and
`DirectoryAnalysisStateStore`. The latter stores immutable JSON states by
content identity, but the accepted A1b inventory found its use only in
temporary test directories and cold-process fixtures. It found no checked-in
state directory, snapshot bundle, navigation store, exported state fixture,
release artifact, or documented retention contract.
(`2359a987:tools/standards_engine/standards_engine/engine.py`;
`7bc8bd07:tools/standards_engine/standards_engine/engine.py`;
`84412f22:docs/archive/plans/standards-engine-a1b/reports/consumer-and-state-inventory.md`)

**Fact:** A1b intentionally adds a local SQLite store because non-derivable
analysis decisions would otherwise be lost and because A1B-A4 requires durable
cold replay, backup, and restore. The plan simultaneously excludes migration,
semantic export/import, checked-in databases, destructive restore, retention
management, deletion, enumeration, and garbage collection. The absence of
existing state justified an atomic breaking cutover with no compatibility
reader.
(`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`;
`36dd7579:docs/archive/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md`)

**Inference:** durable analysis decisions are a plausible future need, but the
accepted repository proves a capability rather than an observed retention
workflow. A1c should not infer retention duration, backup cadence, recovery
point objective, cleanup policy, or cross-machine portability from the mere
existence of A1b's store.

## Guarantee Provenance And Consumer Audit

The detailed evidence below is summarized here so consumer demand is not
blurred with standards, review, or mechanism choice.

| Guarantee | External-product demand | Repository-process demand | Plan-selected | Standards/review influence | Implementation choice or unresolved |
| --- | --- | --- | --- | --- | --- |
| Four operations | None found | Repository fixtures exercise them but are not independent consumers | A1 fixes all four; A1b preserves them | A1b treats accepted A1 as authority | Exact operation count and prepare/resolve split remain unresolved |
| Typed public algebra | None found; Draft 2020-12 is an external semantic constraint | Contract generation, examples, and acceptance consume it | A1 A8; A1b A1/A2/A5 | Generated-contract/evidence-oracle standards and repeated repair review | V11's 140 definitions and class layout are choices |
| Immutable snapshot/result | None found | Acceptance and analysis workflows depend on stability | A1 A2/A3 and single-state lifecycle; A1b A4 | A1 live-read review plus later Immutable Authority Closure | Capture and closure representation are choices |
| Cold reconstruction | None found | Cold-process fixtures and acceptance require it | Added during A1 repair; explicit A1b A4 | Immutable Authority Closure mandates no ambient replay once promised | Lifetime, portability, and store mechanism unresolved |
| Direct child inspection | None found | Inspection fixtures enumerate children | A1 advertises child inspection; A1b makes it universal | Aggregate roots rejected in A1b review | One stored object per child is review-selected, not uniquely required |
| Successful-empty coverage | None found | Core standards-change workflow requires consumer disposition | A1 A6; A1b A8 | Planning projection and systemic-replan standards | Exact horizon/attestation/certificate chain is a choice |
| Authorization/provider replay | None found | Repository coverage authorization is a real internal consumer | A1 capability/completion design; A1b A4/A4C | Immutable closure plus C7 contract reviews | Separate trust objects and later-revocation semantics unresolved |
| Identity/versioning | None found | Generated/persisted/coverage artifacts consume identities | A1/A1b plans version public and stored values | Equality defect plus `396144ad` authority/version rules | Exact version matrix and object granularity are choices |
| SQLite durability/recovery | None found; no non-test recovery caller | Required-real acceptance only | New A1b A4 guarantee | C7 review adds restore and exact interruption closure | SQLite is chosen; real retention need remains unresolved |
| Package-root enforcement | None found | Verifier is the direct consumer | A1b A6I | A1 private-import defect, Dependencies, and repeated review | Full AST capability model is review-selected |
| Git/index integrity | None found | Verifier, capture, and suite-input processes consume it | A1 A2; narrower A1b capture | Hostile-`GIT_*` review finding | Small sanitizer is chosen; exhaustive enforcement breadth is not fixed |
| Migration graph/attestations | None found | Primary demand is Planning, policy migration, and acceptance | A1 impact/coverage; A1b A8/A10/A11 | Policy Projection Completeness and Systemic Re-Planning | Registry/horizon/grant/certificate topology is a choice |

### 1. Four operations: `query`, `prepare`, `resolve`, `inspect`

**Fact:** A1's objective required one agent-facing Engine for discovery,
retrieval, navigation, accepted/proposed comparison, and iterative resolution.
Its Scope then fixed four operations, while its A3, A7, and A9 criteria required
route/read, analysis, and real typed-agent workflows. The brief proposed the
same four calls and described `query` as carrying route/read/related variants.
(`c7d23dfa:docs/archive/plans/standards-engine-navigation-analysis/plan.md`;
`c7d23dfa:docs/archive/plans/standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md`,
sections 8, 9, 14, and 24)

**Fact:** A1b's Objective and Binding Decisions explicitly preserve those four
operations and the read-only immutable analysis kernel. A1B-A5 requires only
generated v11 values to cross them.
(`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`)

**Classification:** plan-selected product requirement; inherited by A1b.
There is no established external-product demand for exactly four operation
names or for the split between `prepare` and `resolve`. Typed agent use was a
repository-authored desired workflow.

**Counterevidence:** four operations form a comparatively deep external
Interface over routing, reading, relation traversal, impact analysis,
authorization, coverage, state transition, and inspection. A small operation
count is not proof of a simple implementation, but it is evidence that A1's
top-level product concept was coherent.

**A1c question:** Which caller journeys must remain stable? Preserve those
journeys before deciding whether they still require four calls, one analyze
operation with a continuation, or a smaller typed capability Interface.

### 2. Typed public algebra

**Fact:** A1 A8 selected one Draft 2020-12 schema to govern Python types, JSON
validation, agent-tool declarations, examples, identity-bearing
serialization, result variants, next operations, and rendering. Repeated A1
reviews then found missing generated semantics and internal Analysis result
types crossing the facade. Accepted Repair VI closed the then-admitted public
algebra, but the Unicode reproduction later proved both local equality
implementations wrong relative to the declared Draft.
(`c7d23dfa:docs/archive/plans/standards-engine-navigation-analysis/plan.md`, A8;
`933c9ab9:docs/archive/plans/standards-engine-navigation-analysis/issues.md`, SENA-022;
`c4408363:docs/archive/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`)

**Fact:** A1b A1B-A1, A1B-A2, and A1B-A5 select the maintained Draft validator,
complete reachable operation closure, generated models, and public facade
adaptation. The accepted facade validates arbitrary mapping input once,
decodes a generated call, invokes the native Engine, and requires the result
to belong to the operation's declared result algebra.
(`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`;
`84412f22:tools/standards_engine/standards_engine/tools.py`)

**Classification:** the structured boundary is plan-selected; complete
generated semantics and separation from internal types are defect- and
standards-driven; Draft equality is an external semantic constraint. The
particular 140-definition v11 schema and generated class arrangement are
implementation choices.

**Threat/failure answered:** unknown agent/tool input can supply missing,
extra, wrong-type, wrong-version, or contradictory fields. A public producer
can also omit a result variant or leak an internal object. The consequence is
misinterpreted work, invalid continuation, or silent contract drift.

**Simpler alternative:** validate and decode once at the arbitrary-input Seam,
then use a smaller hand-owned typed domain Interface internally. Generate only
wire/tool projections that have actual distinct consumers. This preserves the
boundary guarantee without treating every internal transfer as unknown input.

**Residual risk:** the schema can still describe the wrong product, and a
maintained validator does not prove the generated destination or owner
adaptation complete. Conversely, testing impossible wrong-type cases after a
generated value has already been constructed adds no new trust proof.

### 3. Immutable snapshots and immutable results

**Fact:** A1 A2 and A3 required deterministic immutable snapshot identities and
same-snapshot navigation. Its brief described packets/results as immutable and
excluded mutable authoring. The first accepted-looking A1 boundary actually
returned later live worktree bytes from a whole-module read; review withdrew
acceptance and required captured content. The single-state correction also
removed mutable supersession and hidden sessions.
(`c7d23dfa:docs/archive/plans/standards-engine-navigation-analysis/plan.md`, A2 and A3;
`933c9ab9:docs/archive/plans/standards-engine-navigation-analysis/issues.md`, SENA-019
through SENA-021)

**Fact:** v10 preserved those properties while changing policy-impact and
coverage identities. A1b narrows snapshot identity to exact logical paths and
bytes, discards Git/filesystem observations after capture, stores immutable
objects, and binds results to material execution closure rather than complete
input views.
(`7bc8bd07:docs/decisions/standards-engine-policy-impact-authority-v2.md`;
`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`;
`84412f22:tools/standards_authority/standards_authority/snapshot.py`)

**Classification:** plan-selected and supported by a demonstrated correctness
failure. The later general Immutable Authority Closure standard strengthened
the prohibition on live/process-local substitution. Content-addressed object
granularity and closure representation remain implementation choices.

**Minimum implication:** if a caller is given an immutable result or handle,
later mutation of repository files, process caches, authorization services, or
unrelated configuration must not silently change that result during its
promised lifetime. This is one of the strongest A1c guarantees in the record.

### 4. Cold handle reconstruction

**Fact:** A1's `inspect` contract advertised snapshot, navigation, analysis,
policy, report/state, and certificate-related inspection. The single-state
work added cold reconstruction, and successive repair reviews found child
inspection depending on hidden execution authority before Repair VI. Accepted
A1 then passed bounded fresh-process inspection regressions.
(`c7d23dfa:docs/archive/plans/standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md`,
sections 8, 18, and 25;
`933c9ab9:docs/archive/plans/standards-engine-navigation-analysis/issues.md`, SENA-022;
`c4408363:docs/archive/plans/standards-engine-standards-recovery/reports/historical-a1-repair-reproductions.md`)

**Fact:** A1b A1B-A4 makes cold reconstruction explicit for every advertised
handle after source and process mutation. Architecture's post-A1 Immutable
Authority Closure standard requires every replayable/inspectable handle to
bind complete transitive authority and prohibits fresh providers,
authorization, live filesystem/service reads, caches, or originating-process
state.
(`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`;
`36dd7579:topics/architecture.md`, Immutable Authority Closure)

**Classification:** cold replay is plan-selected; exact transitive closure is
standards-mandated once the handle is declared cold-replayable; direct object
storage, codecs, envelope, DAG, and SQLite are implementation choices. No
actual consumer establishes how long handles must survive or whether they must
move between machines.

**Simpler alternatives:** explicitly process-local handles; one persisted
aggregate state/snapshot; an exported immutable bundle; or parent-handle plus
child selector. Each is valid only if the public lifetime and supported
inspection operations are stated honestly.

**A1c question:** Is cold reconstruction a user workflow or a test-derived
acceptance property? Name lifetime, process boundary, machine boundary,
required source independence, and retention before selecting storage.

### 5. Direct child inspection

**Fact:** A1's broad `InspectionResult` made child artifacts inspectable, and
A1 repairs made selected child reconstruction work. A1b's first design stored
three aggregate roots. Independent review rejected aggregate-only inspection;
Candidate C then directly stored every public inspectable object. A1b retained
that rule through one generic `inspect` method whose implementation dispatches
over content snapshots, views, execution closures, navigation, policies,
relationships, contexts, requirements, observations, coverage objects, and
analysis roots.
(`44de7dff:docs/archive/plans/standards-engine-a1b/execution-ledger.md`;
`84412f22:tools/standards_engine/standards_engine/engine.py`)

**Classification:** public inspectability was plan-selected; one direct stored
object per advertised child and one-resolution-rule universality were
review-added structural guarantees. The accepted A1 evidence is
counterevidence to treating direct object storage as the only way to achieve
cold child inspection.

**Threat/failure answered:** a child handle can outlive the parent process or
cache and become unresolvable, or resolution can scan a mutable aggregate and
return a different child. The consequence is a broken advertised handle and
non-reproducible explanation/evidence.

**Simpler alternative:** advertise only aggregate roots, embed material
children immutably, and return a parent handle plus stable typed child key.
That reduces object families but changes the Interface and should be evaluated
against actual inspection journeys, not test cardinality.

**Residual risk:** direct storage prevents a missing lookup path but does not
prove that every child deserves a public identity. It also expands codec,
version, persistence, inspection, and verification surfaces for every new
child family.

### 6. Successful-empty impact and coverage certification

**Fact:** A1's brief says an empty edge query does not prove no consumers and
defines authored audit declarations plus generated certificates over a bounded
horizon. A1 A6 requires deterministic certificates and forbids inferring a
successful empty result from absent edges. The requirement emerged after the
repository already had a Planning rule requiring policy-impact query and
consumer disposition for normative changes.
(`c7d23dfa:docs/archive/plans/standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md`,
section 17;
`c7d23dfa:docs/archive/plans/standards-engine-navigation-analysis/plan.md`, A6;
`36dd7579:workflows/planning.md`, Policy Projection Completeness)

**Fact:** A1's initial coverage design self-invalidated because attestations
changed the complete snapshot they answered and could omit unseen consumers.
The repair introduced an independent horizon, view, requirements,
attestations, and certificates. A1b A1B-A8 then requires exact equality among
selected consumers, dispositions, coverage subjects, and valid certificate
subjects; the A1b cutover renewed these after final registration and freeze.
(`933c9ab9:docs/archive/plans/standards-engine-navigation-analysis/issues.md`,
SENA-005, SENA-015, and SENA-017;
`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`, A1B-A8;
`84412f22:docs/archive/plans/standards-engine-a1b/reports/a1b-cutover-evidence.md`)

**Classification:** both repository-process demand and plan-selected product
behavior. The post-A1 systemic-replanning and policy-projection standards make
complete consumer disposition standards-mandated for governed standards
changes. The exact horizon/provider/attestation/certificate identity chain is
an implementation choice.

**Threat/failure answered:** a maintainer omits an edge, source registry entry,
or consumer, and the engine reports no impact. This is primarily an
authoring/governance correctness risk, not an external attacker. The
consequence is an unreviewed standards change and false completion.

**Simpler alternatives:** require an explicit human `reviewed-empty` decision
for the bounded owner; derive coverage from a smaller dependency-local source
inventory; or keep certification solely in the standards-change workflow
instead of every general analysis result.

**Residual risk:** exact equality proves closure relative to the authored
registry and horizon. It cannot prove that humans identified every semantic
consumer. A valid certificate can faithfully certify an incomplete model.

### 7. Authorization and provider replay

**Fact:** A1 separated read, analysis, consumer-review, impact-review, and
audit-review capabilities. Completion required valid authorization and
evidence. Fact-authority replanning then made observations depend on explicit
provider and authorization views rather than raw caller facts.
(`c7d23dfa:docs/archive/plans/standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md`,
sections 18 and 23;
`933c9ab9:docs/archive/plans/standards-engine-navigation-analysis/issues.md`, SENA-018
and SENA-019)

**Fact:** A1b A1B-A4/A4C requires existing results to replay without live
provider or authorization services and requires consumed provider/grant
objects to enter only successful successor states. C7 review expanded the
contract to exact issuer and revocation revisions, principal, capability,
action, typed subject, submitted evidence, authorization evidence, revocation
evidence, and `not-revoked` state. Accepted code validates an injected
Adapter's typed outcome against the exact current request, then persists the
grant and direct evidence references.
(`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`;
`84412f22:tools/standards_analysis/standards_analysis/trust.py`;
`84412f22:tools/standards_engine/standards_engine/engine.py`)

**Classification:** capability separation and authorization-aware completion
are plan-selected. Persisted direct trust objects are driven by the Immutable
Authority Closure standard and expanded by C7 review. The exact object algebra
and field set are implementation choices. No independently deployed
authorization service or adversarial principal is present in the repository
evidence.

**Threat/failure answered:** a caller submits a decision outside its granted
capability or for a different work subject; a provider supplies a fact over
different inputs; a replay silently asks a changed live provider or
authorization service and changes old meaning. Consequences include
unauthorized completion and non-reproducible decisions.

**Simpler alternative:** validate authorization once at the transition Seam
and store one immutable decision record containing the exact accepted subject,
evidence, and authority fingerprint inside the aggregate analysis state. This
can preserve replay without requiring every trust concept to be a separately
inspectable repository object.

**Residual risk:** the system trusts the injected Adapter and repository-owned
authorization files; exact binding does not establish that the issuer is
legitimate. Replay intentionally does not consult fresh revocation state, so
whether a later revocation should invalidate an already-issued result remains
a product-policy question.

### 8. Identity and versioning

**Fact:** A1 required deterministic domain-separated identities and accumulated
separate snapshot, navigation, analysis, result, applicability,
relationship-kind, coverage, provider, and schema/interface versions. A1 v10
advanced several coordinated public and coverage versions during the
policy-impact amendment. The Unicode defect proved that a stable identity
normalization must not silently become schema-instance equality.
(`2359a987:docs/decisions/standards-engine-navigation-analysis.md`;
`7bc8bd07:docs/decisions/standards-engine-policy-impact-authority-v2.md`;
`c4408363:docs/archive/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`)

**Fact:** during A1b, Candidate C4's copied snapshot/navigation/analysis
version bags were rejected after commit `396144ad` added general authority-
scope and version-scope standards. Accepted A1b separates interface v11,
request v3, result v3, handle v4, envelope v1, identity encoding v2,
per-operation compatibility revisions, and owner-local payload/identity
versions. Semantic identity excludes storage and representation versions when
they do not change meaning.
(`396144ad:topics/architecture.md`;
`396144ad:topics/contracts.md`;
`4f69f994:docs/archive/plans/standards-engine-a1b/execution-ledger.md`;
`84412f22:docs/archive/plans/standards-engine-a1b/reports/identity-version-object-matrix.md`)

**Classification:** stable and correctly scoped identity is a product
correctness requirement. Equality separation fixes a demonstrated defect.
Rejection of umbrella invalidation is standards-mandated. The exact number of
identities, codecs, and version counters is an implementation choice, and no
independent consumer validates each claimed independent evolution path.

**Threat/failure answered:** unequal semantic states alias, equivalent states
split unnecessarily, representation changes invalidate meaning, or unrelated
consumers migrate in lockstep. These are internal/persistence correctness
risks, not primarily hostile-input threats.

**Simpler alternative:** define identity from the smallest immutable material
domain record, version only representations or semantics that have supported
overlap, and use atomic replacement for repository-coordinated internal types.

**Residual risk:** more precise local version ownership can still create a
large global compatibility matrix. Individually valid versions do not prove
that the composed Interface has good Depth or change Locality.

### 9. SQLite durability, backup, restore, and interruption

**Fact:** durable recovery was outside A1's original product scope, although
A1 implemented a directory state Adapter for cold fixtures. A1b A1B-A4 newly
requires SQLite durability, deterministic kill during the real commit sync
syscall, verified backup, offline non-overwriting restore, rollback selection,
and cold reopen on Linux ext4. C7 selected SQLite after C6's direct-file,
hard-link, lock, staging, cleanup, and synchronization design was judged more
complex.
(`c7d23dfa:docs/archive/plans/standards-engine-navigation-analysis/plan.md`, Out of
Scope;
`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`, A1B-A4;
`36dd7579:docs/archive/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md`)

**Fact:** the store threat model trusts application configuration, requires a
private same-principal directory and local case-sensitive ext4, excludes a
malicious same-principal process, and does not exclude another principal
racing a writable parent. The Adapter uses immutable rows, explicit
transactions, SQLite rollback-journal recovery, integrity verification,
bounded canonical envelopes, a non-overwriting backup/restore lifecycle, and
typed invalid/unavailable/unsupported outcomes.
(same SQLite audit;
`84412f22:tools/standards_authority/standards_authority/store.py`;
`84412f22:tools/standards_authority/standards_authority/recovery.py`)

**Classification:** plan-selected operational guarantee; SQLite is a selected
implementation and a simplification relative to C6, not a consequence uniquely
required by immutable handles. Restore details and exact interruption evidence
were review-added. No retained state or non-test recovery caller establishes
operational necessity.

**Simpler alternatives:** no durable store when the actual lifetime is one
process; persist only completed/non-derivable analysis aggregates; use atomic
file replacement for a single object; or delegate backup/restore to the
operator while verifying reopen. The appropriate alternative depends on a
real retention and loss-consequence contract.

**Residual risk:** acceptance exercised process interruption, not arbitrary
power loss, kernel, controller, drive, or filesystem failure. SQLite and the
admitted VFS contract carry much of that proof. Same-principal malicious
mutation remains explicitly out of scope, and A1b has no cleanup or migration
lifecycle if state accumulates.

### 10. Package-root and entrypoint enforcement

**Fact:** A1 review found internal package imports crossing the documented
public boundary. The A1b redesign brief required public package entry points.
Successive planning reviews expanded that into manifest-owned public roots and
entrypoints, static `__all__`, exact direct dependencies, Git-index-derived
production ownership, rejection of private/root-private/star/dynamic imports,
and safe-path execution. Later implementation reviews further expanded a
lexical binding/capability analyzer for `sys.modules`, `eval`, `exec`, import
machinery, conditionals, loops, exception aliases, assignments, functions,
classes, and comprehensions.
(`3439aae9:docs/archive/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`;
`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`, A1B-A6I;
`580d9c95:docs/archive/plans/standards-engine-a1b/execution-ledger.md`;
`84412f22:tools/standards_verifier/standards_verifier/python_packages.py`)

**Fact:** Dependencies' Requirement And Ownership rule rejects incidental
transitive availability, global installs, ambient search paths, and another
package's declaration as satisfaction evidence. It does not prescribe a Python
abstract interpreter. The A1b packages are source-tree Modules deployed
atomically, not independently published distributions.
(`36dd7579:topics/dependencies.md`;
`84412f22:docs/archive/plans/standards-engine-a1b/reports/policy-impact-migration-plan.md`)

**Classification:** the public-root defect is demonstrated; direct requirement
ownership is standards-mandated; exact static enforcement breadth is
review-added and an implementation choice. Its actual consumer is the
repository Verifier, not an Engine caller.

**Threat/failure answered:** code imports a private child, succeeds only because
of repository layout or ambient `sys.path`, or acquires a hidden import
capability. A later package refactor or isolated execution then fails or
bypasses declared dependency ownership.

**Simpler alternatives:** one application package with private internal
Modules; an existing import-linter rule over direct syntax; isolated public
root smoke execution; or a much smaller AST check that rejects explicit
cross-Module private imports without modeling arbitrary capability
provenance.

**Residual risk:** the accepted analyzer intentionally is not a general Python
interpreter and can only conservatively model its selected syntax profile.
Dynamic behavior can always exceed a static subset. Conversely, many modeled
paths would already fail loudly during import or execution; the record does
not map each rejection to a distinct material product consequence.

### 11. Git capture and Git-index sanitization

**Fact:** A1 snapshots included clean Git, dirty/non-Git, modes, symlinks,
submodules, exclusions, and integrity inputs. A1b intentionally narrows the
semantic snapshot to requested logical paths and bytes. Its Git capture
resolves one commit, reads commit/tree/blob objects, verifies each object type,
length, and Git hash, and reads neither the worktree nor index. Native capture
uses descriptor-relative no-follow traversal and endpoint revalidation.
(`c7d23dfa:docs/archive/plans/standards-engine-navigation-analysis/plan.md`, A2;
`36dd7579:docs/archive/plans/standards-engine-a1b/plan.md`, Milestone 2;
`84412f22:tools/standards_authority/standards_authority/capture.py`)

**Fact:** late A1b reviews found direct Verifier Git calls could be redirected
by inherited `GIT_DIR` and `GIT_INDEX_FILE`. Accepted A1b centralizes Git
execution in a small Adapter that removes all `GIT_*` environment variables;
the package, suite-input, and reachability consumers use it. Final evidence
ran under hostile overrides on both supported Python versions.
(`580d9c95:docs/archive/plans/standards-engine-a1b/execution-ledger.md`;
`84412f22:tools/standards_authority/standards_authority/git_index.py`;
`84412f22:docs/archive/plans/standards-engine-a1b/reports/a1b-cutover-evidence.md`)

**Classification:** immutable source capture is plan-selected and supported by
the actual A1 live-source defect. Git-object verification is an implementation
choice aligned with content identity. Environment sanitization is review-added
and answers a demonstrated hostile-environment path. The large systemic scan
proving all Git consumers use the Adapter is review/verification machinery,
not part of the Engine product Interface.

**Simpler alternative:** keep the small explicit Git wrapper and prohibit
direct subprocess calls through ordinary static search/lint plus one hostile-
environment integration test. For an A1c that accepts only a commit/tree
snapshot, omit native worktree capture and its concurrency contract.

**Residual risk:** removing `GIT_*` does not authenticate the `git` executable
selected by `PATH`; that belongs to the dependency/supply-chain model.
Same-principal mutation of the repository and executable is not prevented.

### 12. Migration graph, dispositions, attestations, and certificates

**Fact:** Planning's Policy Projection Completeness rule predates A1 and
requires a normative change to query the `policy-impact` graph and disposition
every returned consumer. A1 made impact analysis and successful-empty coverage
part of the product. The post-A1 Systemic-Finding Re-Planning rule requires an
invariant-family inventory and non-blocked disposition for every selected
consumer.
(`36dd7579:workflows/planning.md`, Policy Projection Completeness and
Systemic-Finding Re-Planning)

**Fact:** A1b created/retired governed implementation artifacts, so its plan
required exact catalog and relationship migration, admitted-source
registration, selected-consumer/disposition equality, final horizon freeze,
authorized attestation renewal, and certificate equality. These artifacts
were part of implementation admission and final acceptance even where the
changed relationship did not affect query/prepare/resolve/inspect behavior.
(`36dd7579:docs/archive/plans/standards-engine-a1b/reports/policy-impact-migration-plan.md`;
`84412f22:docs/archive/plans/standards-engine-a1b/reports/a1b-consumer-dispositions.md`;
`580d9c95:docs/archive/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`)

**Classification:** repository-process demand and standards-mandated
governance. The exact graph schema, supplemental catalog, horizon identity,
attestation-source registry, grant objects, and certificate pipeline are
implementation choices. They should not be described as externally demanded
Engine features.

**Threat/failure answered:** a standards change silently misses one
distribution/enforcement consumer, a new relationship source exists but is
not registered, a removed implementation remains reachable, or stale
attestations make incomplete migration appear accepted.

**Simpler alternatives:** change-specific impact records with explicit
reviewed-empty disposition; dependency-local invalidation; one authoritative
consumer manifest compiled into review output; and removal of runtime coverage
objects when coverage is only a repository planning concern.

**Residual risk:** graph and attestation closure can prove agreement among
declared authorities, not semantic completeness of those declarations. Broad
horizon invalidation also creates renewal work that can obscure the few
consumer decisions that actually changed.

## Scoped Threat And Failure Models

The word *threat* below includes accidental corruption and programmer error as
well as adversarial action. The actor and Seam determine the necessary
response; local process internals are not treated as hostile merely because a
malformed state can be imagined.

| Seam | Plausible actor or corruption path | Material consequence | Existing mitigation at `84412f22` | Simpler admissible alternative | Residual risk or unresolved fact |
| --- | --- | --- | --- | --- | --- |
| Arbitrary agent/tool input | Caller supplies malformed shape, wrong version, forged handle, mismatched evidence, or unauthorized submission. | Wrong operation, invalid continuation, unauthorized decision, crash, or ambiguous failure. | Schema validation and generated decoding in `AgentToolFacade`; exact result algebra; typed rejection; authorization binds action, subject, capability, and evidence. | Validate once at the facade and pass proof-bearing typed values directly; keep internal impossible states fail-fast. | No network listener or hostile multi-tenant deployment is established. Resource-exhaustion limits and native-Python bypass policy are not fully specified. |
| Repository-authored content | Maintainer writes invalid TOML/schema/Markdown, omits a semantic edge/source, or makes a false attestation. | Wrong routing/impact, false empty result, stale or incomplete policy projection. | Closed registries, owner parsers, policy graph, horizon, exact dispositions, authorization, attestations, certificates, and broad verification. | Compiler validation plus change-specific consumer review and explicit reviewed-empty decision. | Machinery cannot infer missing semantic meaning from prose. A coherent but incomplete authored model can pass. |
| Persisted bytes | Disk decay, partial write, other-principal path race, unsupported old/new schema, or operator copies a corrupt store. | Handle contradiction, lost decisions, wrong replay, unavailable recovery. | Private ext4 root checks, SQLite transaction and schema profile, immutable rows, canonical bounded envelope, owner identity recomputation, dependency verification, integrity check, verified backup/restore. | Persist one aggregate with atomic replacement and checksum, or make handles process-local when no retention promise exists. | Same-principal malicious mutation is excluded; physical power-loss behavior relies on SQLite/VFS contract; retention, cleanup, and migration needs are unknown. |
| Local process internals | Programmer passes the wrong owner type, omits a closure root, mishandles a variant, or violates an invariant after construction. | Immediate exception, wrong identity/result, or durable corruption if the error reaches persistence. | Immutable dataclasses, constructors/codecs, generated types, assertions, runtime owner checks, focused tests, and closure verification before publication. | Static types, smart constructors, assertions, propagated exceptions, traces, and Interface-level tests; add runtime validation only before durable or externally visible harm. | The standards do not consistently distinguish contained fail-stop defects from corruption-capable internal defects. Marginal need for many internal negative tests is unresolved. |
| Git environment and repository selection | Inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, or related variables redirect a command; index/worktree changes during observation. | Verification or capture applies to the wrong repository/content and falsely passes. | One Git Adapter removes `GIT_*`; Git capture resolves and hash-verifies objects; index output is NUL/UTF-8 checked; native capture revalidates endpoints. | Small wrapper plus prohibition/search for direct Git subprocess and one hostile-environment test; accept commit-only input where possible. | `PATH`/executable provenance is separate; same-principal mutation remains possible; native endpoint checking does not claim detection of every mutate-away-and-back event. |
| Supply chain and test oracle | Compromised or drifting `jsonschema`, `referencing`, transitive wheel, Python/SQLite runtime, or host `strace`; wrong test oracle. | Schema misvalidation, compromised execution, false durability evidence, or non-reproducible builds. | Exact hash lock, source/wheel/license/notice/provenance review, isolated installs on CPython 3.11/3.12, capability checks, security audit, independent Draft semantics owner, recorded `strace` provenance. | Retain the maintained validator and its exact lock; avoid making test-only oracles runtime dependencies; reduce supported targets if product facts permit. | A hash identifies selected bytes but does not establish upstream trust. Registry/maintainer compromise and host toolchain trust remain. |
| Authorization and provider trust | Caller forges work context; provider claims over different inputs; issuer/Adapter is compromised; revocation changes after decision. | Unauthorized or irreproducible analysis completion. | Injected typed Adapters; exact input roles; evidence digest verification; exact action/subject/capability binding; stored provider/grant objects only on success; cold replay without live services. | Validate at transition and store the accepted decision/evidence/authority fingerprint inside analysis state. | Root issuer legitimacy is composition policy, not proven by the record. Treatment of later revocation of historical results is unresolved. |
| Concurrent source mutation | File, directory, mount, or repository content changes during snapshot capture; two writers publish one identity. | Torn snapshot, aliasing, or contradictory immutable object. | Held descriptor reads, no-follow traversal, binding and endpoint rewalk, Git immutable object reads, SQLite `BEGIN IMMEDIATE`, idempotent identical put, collision rejection. | Require clean Git commit snapshots for authoritative analysis; serialize one aggregate-state writer. | A1b deliberately excludes mutation detection stronger than endpoint revalidation and admits only local ext4. |
| Crash and durability | Process dies before/during/after commit, lock contention, failed restore, unavailable filesystem synchronization. | Lost or partial decision, corrupt store, destructive recovery, false success. | SQLite rollback journal, `synchronous=EXTRA`, real sync-syscall kill evidence, cold reopen, no application retry, non-overwriting offline restore, source preservation. | Do not promise durable recovery absent a retained-state consumer; otherwise persist only material analysis aggregates and use operator-owned backup. | Tests do not simulate all hardware/firmware failures. Operational backup schedule, monitoring, retention, and disaster owner are absent. |
| Package/source-tree boundary | Developer imports private child, relies on ambient path/global install, or acquires dynamic import capability. | Hidden dependency and failure after isolation/refactor; declaration drift. | Manifest/root/entrypoint contracts, AST audit, static exports, Git-index ownership, safe-path execution, correction matrix. | One package; import-linter/static direct-import rule; isolated public-root smoke; ordinary fail-fast import error for low-consequence paths. | No independently deployed local packages are present. The accepted analyzer's full breadth has no per-case consequence map. |
| Policy migration and coverage | Maintainer omits changed consumer, source registration, deletion disposition, attestation, or renewal after horizon change. | Standards enforcement surfaces diverge while plan reports completion. | Source-owned graph, exact natural-key migration, selected/disposition equality, final freeze, authorized attestations, certificate equality. | Dependency-local change report and explicit reviewed-empty decision. | Completeness remains relative to authored sources; broad renewal can add process noise without adding semantic evidence. |

## Cross-Guarantee Observations

### Guarantees that have direct defect evidence

The strongest evidence supports:

- declaration semantics must agree with the selected external schema contract;
- arbitrary tool input is decoded and validated at its trust Seam;
- generated/public results do not leak internal domain types;
- an issued immutable result does not read later live source;
- a promised replay does not silently substitute a current provider,
  authorization decision, cache, or worktree;
- schema equality, domain equality, and content identity remain separate;
- direct Git commands cannot be redirected by ambient `GIT_*` variables when
  repository identity matters; and
- a policy-impact workflow cannot call an empty edge set complete without an
  adequate bounded coverage decision.

These properties are supported by actual A1/A1b findings or an external
semantic authority, not merely by standards preference.

### Guarantees supported primarily by accepted plan/review authority

The repository proves implementation of, but not independent demand for:

- cold reconstruction of every advertised handle family;
- direct storage of every inspectable child;
- one generic envelope and object repository for all owners;
- four separately persisted operation-authority records and the complete
  current version matrix;
- durable SQLite publication for normal use;
- product-owned backup and non-overwriting restore;
- deterministic `strace` interruption as permanent acceptance evidence;
- direct provider and grant objects rather than an aggregate decision record;
- exhaustive Python binding/capability analysis for package-root enforcement;
  and
- the exact horizon/attestation/certificate pipeline and its invalidation
  breadth.

This is not a finding that those guarantees are wrong. It is a finding about
their evidence class and therefore about what A1c must independently justify.

### Counterevidence against removing all machinery

- A1's local schema subset produced a real standards disagreement; replacing
  the maintained validator with another small local interpreter would discard
  strong evidence.
- A1's live-read and fresh-authority defects show that immutable labels without
  owned capture/replay mechanics are insufficient.
- A1b's repeated private-import and hostile-Git findings show that ordinary
  happy-path execution did miss real boundary violations.
- Coverage self-invalidation and missing consumer obligations were real design
  failures, not merely verifier aesthetics.
- SQLite removed substantially more application-owned durability machinery
  than C6's direct-file protocol for the *same selected durability claim*.

The A1c question is which claim remains, not whether A1b's replacement was
simpler than every rejected A1b candidate.

## Evidence-Constrained Minimum Guarantee Set For A1c Evaluation

This is a characterization baseline for comparing A1c proposals, not a
binding design or a promise that every guarantee must remain public.

### Strong baseline guarantees

1. **Read-only scope:** navigation and analysis do not mutate or accept
   canonical standards. Any future authoring authority remains separate.
2. **Trust-seam decoding:** arbitrary structured input is completely decoded
   and validated once against the supported public contract. Proven internal
   values are consumed directly until their proof lifetime ends.
3. **External semantic conformance:** Draft 2020-12 behavior uses the selected
   maintained semantics owner; generated freshness is distinct from semantic
   agreement and public behavior.
4. **Snapshot-bound meaning:** every issued result identifies the exact
   material source/authority it used, and later repository mutation cannot
   change that result.
5. **Explicit uncertainty and failure:** unknown applicability remains unknown;
   invalid, unsupported, unavailable, and unauthorized conditions remain
   distinguishable where callers can act differently.
6. **No ambient substitution:** within the declared handle lifetime,
   resolution never replaces missing material source, provider input,
   authorization, or compatibility authority with current ambient state.
7. **Equality and identity separation:** schema-instance equality, domain
   equality/order/deduplication, and content identity use their owning
   contracts rather than one generic comparator.
8. **Exact completion:** a completed analysis cannot omit, duplicate, or accept
   unauthorized current obligations/decisions.
9. **Covered empty impact:** an empty impact result states the bounded coverage
   authority that makes it meaningful, or remains explicitly unaudited.
10. **Repository selection integrity:** any Git operation whose result affects
    authority or acceptance uses an explicit repository and a sanitized
    environment; content identity is independently checked where replay or
    supply-chain integrity depends on exact bytes.

### Conditional guarantees requiring an explicit consumer contract

1. **Cold replay:** require cross-process reconstruction only after naming the
   consumer, lifetime, machine boundary, retained operations, source
   independence, and failure behavior.
2. **Child handles:** advertise independent child identity only for child
   workflows that cannot be served adequately by an immutable aggregate and a
   typed selector.
3. **Durability:** require SQLite-class crash, backup, and restore behavior only
   for state whose loss consequence and retention lifecycle justify it.
4. **Authorization replay:** persist enough accepted authority/evidence to
   reproduce a material decision; separately stored trust objects are optional
   unless independently inspected or evolved.
5. **Independent versions:** create a version only for one supported
   compatibility promise with an actual consumer or retained representation.
   Repository-coordinated internal replacements may be atomic.
6. **Package boundaries:** enforce public roots to the depth required by actual
   distribution/refactor isolation. A source-tree Module does not become an
   independently deployed package merely because it has a manifest.
7. **Policy coverage machinery:** keep consumer disposition and rejection of
   unaudited empty impact, while allowing a smaller dependency-local evidence
   mechanism if it proves the same bounded claim.

### Machinery that is not part of the minimum by itself

The evidence does not make the following independently mandatory: a generic
content-addressed DAG, one envelope format across every domain, direct storage
of all children, SQLite schema v1, a backup/restore API, a sync-syscall
injection harness, owner codec sets as public Interfaces, the current number of
versions, an AST binding/capability interpreter, global suite-input digests,
or provider-wide coverage renewal. An A1c design may still select any of them
after a concrete consumer/risk/deletion test.

## Questions A1c Must Answer Before Design Admission

1. Who is the first real caller: an in-process agent tool, local CLI,
   long-running service, or independently installed library?
2. Which exact workflows require `query`, `prepare`, `resolve`, and `inspect`,
   and which operation boundaries are merely inherited names?
3. What is the supported lifetime and portability of each handle family?
4. Which child artifacts are independently inspected by a caller rather than
   only asserted by tests?
5. What state is not derivable from Git, how long is it retained, what is the
   consequence of loss, and who owns backup, restore, cleanup, and migration?
6. Which authorization actors are genuinely distinct principals, and should a
   later revocation invalidate old analysis or only future transitions?
7. Which provider inputs come from independently changing services or plugins,
   as opposed to deterministic repository compilation?
8. Which version scopes have supported overlapping consumers, persisted data,
   or independently deployed producers? Which can be atomic internal changes?
9. Can coverage certification remain a repository planning concern rather
   than part of every Engine state and public inspection family?
10. Can a representative route/read and full analysis journey be implemented
    with one immutable aggregate authority and materially fewer conversions?
11. For each retained validator, verifier, digest, or negative test, what
    reachable failure, consequence, independent oracle, and non-subsumed value
    does it have?
12. For each new Module or Adapter, what caller reasoning disappears, what
    real second implementation exists, and what happens under the deletion
    test?
13. How many Modules, versions, generated artifacts, graph relationships,
    coverage records, and tests change when adding one result field, one
    inspectable kind, one identity rule, one operation dependency, and one
    internal import?
14. Which low-consequence internal defects can safely fail fast and be debugged
    through exceptions/traces rather than gaining permanent typed validation
    and negative-fixture machinery?

## Final Classification

**Fact:** A1 and A1b were both accepted against their admitted plans and
standards snapshots. A1b preserves the read-only product while materially
strengthening semantic conformance, replay, durability, authority closure,
package governance, Git isolation, and migration evidence.

**Fact:** the accepted repository has no external product consumer and no
retained A1 state. The accepted A1b tree has no non-test caller of persisted
Engine reopening or backup/restore. Repository process tooling, rather than an
external Engine client, is a direct production consumer of package-root,
Git-index, migration, and coverage enforcement machinery.

**Inference:** A1b's design is best understood as an assurance-maximal
implementation of plan-selected guarantees under strengthened standards, not
as the minimum shape demanded by observed callers. Its strongest lessons are
boundary properties—external semantic conformance, immutable meaning,
trust-seam validation, explicit uncertainty, no ambient replay substitution,
and honest coverage—not its complete internal object and verifier topology.

**Counterevidence:** several of those properties were added only after real
defects escaped earlier reviews, so A1c cannot justify simplification by
assuming types, Git, or ordinary debugging make every boundary safe. The
burden is to show a simpler owner and proof, not merely fewer files or tests.

**Unresolved:** whether cold durability, independent child handles, detailed
trust replay, package isolation, and full governance closure are valuable in
the eventual product depends on deployment and consumer facts that do not yet
exist in the repository record. A1c design should make those facts explicit
before reusing or deleting the corresponding A1b machinery.
