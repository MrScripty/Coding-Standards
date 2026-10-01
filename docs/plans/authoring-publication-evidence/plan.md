# Authoring Publication and Evidence Clarity

**Plan status:** `Active`

**Current phase:** A1 implementation is complete; final acceptance and main-targeted PR review are in progress.

**Next slice:** Complete A1's exact-candidate hosted checks and required independent review. Begin A2 only after A1 is accepted and merged to `main`.

**Acceptance status:** `pending`

**Composed-design review:** `applicable`; see [Simplicity and Ownership Review](#simplicity-and-ownership-review).

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

This is a new scope motivated by the supplied agent authoring report. It does not
reopen the accepted refactoring or routing-fact work, nor declare unrelated pending
packaging/test-strengthening acceptance complete. The source review and plan were
delivered as a planning-only archive; the current user request explicitly admits
implementation with operation `start` against this canonical plan path. The exact
starting revision is `149ba317e9397519bc181a048ecf76aef129a69c`, which matches
`origin/main`. A1 is owned by branch
`implementation/authoring-publication-evidence-a1` in task worktree
`/tmp/cs-authoring-publication-evidence-a1`. The original user worktree's staged,
unstaged, and untracked changes remain outside this branch.

## Objective

Enable an authorized standards author to understand exactly what was published,
which bytes each evidence reference supports, and which next action is safe. A
small authoring change should not reach nominal readiness with an already-detectable
destination-evidence mismatch, nor report publication without distinguishing the
canonical ref from the selected checkout/index. Preserve real authorization,
current-state checks, immutable revision binding, atomic co-edits, and portable
review receipts. Reuse existing mechanisms instead of adding another approval
system, mutable task session, generic evidence framework, or short-ID registry.

## Reviewed Source and Evidence

Review baseline: `149ba317e9397519bc181a048ecf76aef129a69c`, tree
`fdd40edc1eea85398e97b740a595a42631614d0b`, Engine interface **45**, request contract
**6**, result projection **7**. The exact Actions source artifact is `11036434347`
from run `36574954850`, archive SHA-256
`34d36acefcb3b9c4be1bf096797bbd3c111f893f2c8bb2ca8c0e2d00be802f0f`.
Its latest commit is an Engine-generated standards publication, not a runtime-code
change. Its old-looking deterministic Git timestamp is not evidence that it is an
old branch tip. The original agent session's private handles/transcript were not
supplied; the review reproduces mechanisms on this pinned code, not that exact run.

[Source review](reports/code-review.md) contains locations, actual results and
limitations. [Consumer inventory](reports/source-consumers.md) maps the public,
authorization, persistence, Git and presentation owners. Four actual-facade probes
reproduced the reported publication/index mismatch, late candidate-evidence failure,
generic exposure rejection and avoidable renewed Analysis work. In-memory reuse
and real Git two-tree trials establish bounded feasibility, not implementation.

The historical baseline CI run failed in two cases of the same supporting-workflow
scenario because its negative assertion depended on accepted Security exposure.
A1 replaced that assumption with a test-owned unexposed standard, without changing
Security exposure. The direct and warm-cache cases pass on the A1 candidate. No
hosted exact-candidate CI run is claimed. See issue B0.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A-C1 | Apply, recovery and later status distinguish durable publication identity from a fresh checkout/index observation, including unknown outcomes. | contract + integration | real Git and SQLite, replacement processes | automated | satisfied | A1 publication/recovery integration, including a new MCP process reading the retained applied result |
| A-C2 | Already-incompatible evidence is identified before readiness, with exact phase/reference/digest/source context; later changes still reject at the final boundary. | negative + lifecycle | real authority/evidence, both wire entrypoints | automated | pending | A1 covers repository-content@1; A2 must extend the matrix to bound references and both entrypoints |
| A-C3 | Explicit baseline, candidate and imported-local acquisitions retain exact bytes and provenance, never switch sources silently, and remain distinct from the decision's subject and authority. | contract + persistence | real Git, snapshot/projection and bounded local inputs | automated | pending | A2 capture/export oracles |
| A-C4 | Published bound evidence and coverage remain verifiable in a cold clone without the original worktree, capture store or external file; genuine legacy evidence retains its original meaning. | retained-history | old producer/new consumer and new exported candidate | automated | pending | A2 legacy/new receipt fixtures |
| A-C5 | Explicit reconciliation preserves unrelated staged, unstaged and untracked work; overlaps, stale observations and partial failures have owned outcomes without republishing. | lifecycle + concurrency | supported Linux/Git, real index/files and injected interleavings | automated | pending | A3 reconciliation matrix |
| A-C6 | Authorized previews identify blocking exposure/prerequisite material; application-purpose callers still receive only permitted information. | purpose boundary | real candidate and private dependencies | automated | pending | A4 redaction/diagnostic cases |
| A-C7 | Focused successor Analysis reuses only independently revalidated applicable decisions and explains invalidations; old decisions/readiness are never relabeled as new approvals. | semantic + differential | real Analysis, source/evidence drift and authorization | automated | pending | A4 reuse matrix |
| A-C8 | Generated contracts, supported callers, bounded compact responses and task examples are coordinated; required locked CI passes against the integrated material. | integration | current supported hash-locked CI | automated | pending | A5 exact-candidate evidence |
| A-C9 | An actual authorized agent completes a bounded authoring change, understands evidence and publication, and uses explicit reconciliation without unexplained repair loops or a new mandatory discovery ritual. | user workflow | real supported client against disposable repository | observed | pending | A5 matched authoring task |
| A-C10 | Independent material review and acceptance-owner disposition establish scope, retained identities and completion of only this new plan. | review + acceptance | independent reviewer and acceptance owner | manual | pending | Final decision record |

A fixture may use explicit test authorization but cannot establish editorial truth
or downstream quality. Observing a read-only review is not evidence that tests ran.
No production standards mutation is needed for qualification. Do not add mandatory
model runs to every intermediate patch; A-C9 is for the coherent final candidate.

## Scope

### In scope

Authoring publication reporting, a narrowly explicit checkout reconciliation action,
baseline/candidate/imported evidence acquisition and durable binding, early
publication-evidence preflight, scoped failure detail, candidate exposure explanation,
validated successor Analysis reuse, and the directly affected schemas, consumers,
examples, retained-state tests and records. Each milestone includes its own necessary
verification. Fix the demonstrated current fixture assumption as a qualification
prerequisite, not as a reason to weaken exposure checks.

### Out of scope

Remote pushes, history rewrites, changing the canonical branch policy, automatic
reset/stash/clean/rebase, unattended merging of user edits, repairing arbitrary
worktrees, new provider integrations or network evidence fetch, secret scanning,
global acceptance automation, an independent reviewer service, a new fact engine,
cache expansion, typed-edit conversion, eagerly embedding all schemas, replacing
exact handles with short request IDs, or broader downstream pilots. No existing
review/authorization requirement is dropped because a change is small or metadata.

## Binding Decisions

### D1 — Publication and checkout state are independent facts

Keep canonical publication's existing meaning: a verified candidate is imported,
the expected target ref is advanced, and its selected application outcome is recorded.
Do not secretly broaden apply into checkout mutation. Extend the existing native
apply/recovery results and focused workflow projection with one publication receipt:
application identity, exact candidate commit/tree, target ref, expected predecessor,
and durable publication state. These are already stored or derivable from the
selected ProposalApplication; they do not need another receipt registry.

Include an explicitly fresh checkout observation: selected worktree/HEAD binding,
index tree or exact index observation, whether publication paths still represent
the predecessor, safe mismatch counts, and observation status. Keep `not-observed`,
`unavailable`, `not-target-checkout`, `current`, `needs-reconciliation` and `conflicted`
distinct. Exact wire discriminants are generated under the existing schema owner;
there is no single boolean `clean` standing in for these meanings. A checkout error
after durable publication must not disguise the publication as failed or advertise
apply as the next action. Historical publication success and a later diverged target
are also separate observations.

`workflow_status` reconstructs the durable receipt after reconnecting and observes
current Git state again. It must not fabricate an original before-image for an old
application. New optional observation records are versioned separately if they must
persist; otherwise keep them ephemeral. Compact results include the commit/ref and
next action once; bounded detailed path lists belong in a selected detail page.
Never let a size limit hide a successful mutation or lose its application handle.

### D2 — Early evidence preflight, with one shared publication interpretation

Extract the evidence/destination assembly currently first exercised by
`_publish_coverage_into_candidate` into an owned, side-effect-free preparation
step shared by readiness/preflight and apply. It examines the exact logical
projection, coverage requirements and selected evidence. It does not publish a
Git ref, write readiness, grant apply authority, or pre-issue a publication approval.
Only after it succeeds may a new readiness claim be recorded.

For existing `repository-content` version 1 references, preserve the actual
contract: live local authorization plus destination-compatible bytes for portable
coverage. Identify a changed, removed or uncommitted destination reference before
issuing readiness. Baseline evidence that cannot fulfill that destination contract
must be rejected with an actionable explanation or explicitly bound through D3;
never change its digest or source silently. Old readiness is not rewritten; apply
performs the new safety preflight while retaining its original immutable binding.

Final apply still rechecks live capability/revocation, exact revision/head, evidence
where its contract requires a live observation, destination assembly, actual
candidate verification and expected-target publication. Preflight success is not
cached authority. Separate pure evidence preparation from final publication-grant
construction: a review request must not exercise `publish-coverage` merely to
obtain an early error. Candidate receipts depending on live authorization are
constructed and checked at their proper final boundary.

### D3 — Explicit bound evidence, reusing the current reference carrier

The selected first design is **Engine-bound, self-contained evidence artifacts**,
not a universal new provider ecosystem or an expanded EvidenceReference at every
existing use. Keep the four-field canonical EvidenceReference and request-local
evidence table. Add one bounded authoring acquisition operation, provisionally
`bind_evidence`, accepting a batch of explicit source selections and optional expected
source digests. Verify a supplied digest; otherwise return the digest of the exact
verified capture without requiring the caller to compute it first. It returns
reusable existing-format references plus provenance and an inspection handle. Use existing `inspect` for later observation rather than a
new family of evidence-list/query tools.

Supported acquisitions:

- **Baseline:** a named live snapshot and explicit path, or its exact recorded Git
  revision when an explicitly requested file is outside the captured compiler
  closure. Use the repository's verified object reader, not the checkout. Record
  both selected snapshot identity and actual source revision/path. An unavailable
  original object is unavailable, not permission to use current bytes.
- **Candidate:** an exact existing proposal-revision handle and path read from its
  verified logical projection. Preserve proposal/revision and projected-material
  identity. This is the source of evidence, not an assertion that it covers the
  final publication commit. Final-generated receipts cannot be evidence for their
  own identity; reject cycles/self-reference rather than invent a fixed point.
- **Imported local:** an explicitly selected bounded regular file under an
  operator-authorized root. Reuse an existing configured repository-local root for
  the initial deployment where adequate; supporting a separate root requires an
  explicit narrow composition setting and authorization, not arbitrary filesystem
  access. Record original locator as caller provenance, byte digest and capture
  identity. No URL fetching, shell execution, directory crawling or silent "working
  tree equals candidate" inference occurs.

An immutable bundle contains version, validated source descriptor, exact original
content bytes and digest, and any caller-reported external subject/producer metadata
marked as reported rather than verified. One canonical serialization owns the bundle;
its digest determines a reserved, collision-checked repository evidence path. Return
an ordinary `repository-content@1` reference to those **bundle bytes**, explicitly
labelled as such; retain the original content digest separately. Do not claim that
the bundle digest is the raw source digest. Source/provenance changes change the
bundle identity even when raw bytes happen to match.

Use one Engine-owned evidence-binding module and the existing snapshot aggregate/
content lifecycle for these bounded captures. No independent database or global
registry is needed. Preserve retention dependencies and failure cleanup; do not
expose a usable binding whose bytes were never admitted. Select and document named
per-item, batch and retained-material limits during the A2 vertical proof, using the
existing source/object limits where suitable; reject overflows without truncation
and test boundaries with small injected limits. Acquisition observes and binds material; it does not grant a decision, review or publication.

Adapt the local evidence resolver through explicit bound records supplied by its
composition owner. For a bound reference, it resolves the recorded immutable
bundle, checks its identity/content, and authorizes each actual subject/action
freshly. It must not consult a same-named worktree file or guess an alternative
provider. Legacy raw references remain on their existing resolver. Separate the
resolver from authorization policy; Engine must not import its facade to resolve
source, and the new module must not become a second semantic trust validator.

Include exactly the bound artifacts reachable from a proposal's purpose/edits,
Analysis decisions, coverage claims and review decisions in the generated candidate.
Collect through typed owned fields, not recursive scanning of arbitrary JSON.
Preview names, sizes and provenance before readiness, including imported material
that will become committed; publication authorization covers that inclusion. Do not
publish every capture in the store. Add the managed paths and exact bytes through
existing logical/final-candidate topology and regeneration owners before verification.
Reject collisions, missing captures and inconsistent bundles. Do not mutate accepted
policy text or leave untracked staging artifacts to satisfy the current resolver.

This deliberately preserves portable `repository-content@1` receipt semantics:
a cold reader finds the exact referenced bundle in the destination repository and
validates its digest using the existing receipt/trust path. Bundle provenance is
independently inspectable. No old receipt is reinterpreted as snapshot-bound, and no
blanket EvidenceReference or coverage-receipt migration is assumed. If a real
consumer requires raw content instead of the bundle carrier, or generic provider
admission cannot preserve its contract, stop at A2's small vertical proof and own a
versioned alternative; do not disguise raw bytes as bundle bytes.

**Origin is not subject or authority.** A baseline page may support before-state
reasoning; its capture does not prove after-state correctness. Existing obligation,
fingerprint, coverage and capability contracts decide whether the evidence is
admissible for a decision. External run claims remain claims unless a trusted
provider actually verifies them. No automatic baseline/candidate rebinding or
acceptance is inferred from matching bytes.

### D4 — Diagnostics travel from the failing owner through the authorized boundary

`ResolvedEvidence` currently raises a digest mismatch without details, and generic
Engine rejection discards available AnalysisFailure path/field/observed context.
Correct both ownership boundaries: produce exact structured mismatch data at
resolution/preflight, then project permitted bounded context through the existing
error machinery. Use reference ID, provider/version, validation phase, source kind
and material identity, expected/observed digest, and proposed next action. Absence
of readable bytes has no fabricated observed digest. A batch identifies the failing
member without reflecting arbitrary malicious keys or dumping evidence contents.

Authoring permission is required for private locators, subjects or provenance.
Application outputs keep their existing disclosure policy; do not globally expose
AnalysisFailure.observed or Git stderr. Distinguish invalid evidence, unavailable
source, unsupported provider, revoked authorization and stale subject. Preserve
machine-readable codes and add an explicit diagnostic extension only where needed.
Historical diagnostic payloads are not retroactively altered. `readiness-preflight`,
`decision-authorization`, `candidate-evidence`, `final-verification` and `recovery`
are phase values owned by the operation that supplies the context, not guesswork in
a generic hash validator.

### D5 — Reconciliation is a separate, explicitly authorized local operation

Add one authoring operation, provisionally `reconcile_application`, with observation
as its default and an explicit apply action. Input identifies the stored application
and one selected worktree; execution also supplies its exact preflight observation
binding. Do not use `recover_application` to conceal checkout writes: existing
recovery concerns canonical publication and durable outcomes only.

The first supported mutation is intentionally narrow: synchronize publication-owned
paths while carrying forward unrelated staged/unstaged/untracked work. Use a reviewed
Git two-tree operation through Repository Git, with expected predecessor and exact
published candidate; the feasibility trial used `read-tree -m -u old new`. This is
not a recipe to issue blindly. Derive the permitted path set, verify actual HEAD/ref,
index entries, modes and file states, and classify conflicts before effect. A
conflicting publication path or untracked obstacle refuses rather than merges or
overwrites. Do not silently stash, reset, clean, switch branches, write a commit,
advance the target again, or synchronize every linked checkout.

Protect private/common Git directories, linked-worktree identity, index locks and
no-follow filesystem boundaries at Repository Git. Preserve unrelated staged and
unstaged distinctions, not merely their combined bytes. Existing lockfiles belong
to their owner and are not deleted. Admit only explicitly supported regular-file
layouts initially; sparse/split indexes, unmerged entries, gitlinks, case collisions,
custom filters and other unsupported modes need explicit rejection or separately
proved support. Do not claim a platform matrix from Linux-only tests.

The Git index lock does not lock arbitrary editors or the branch ref. Establish
exclusive/cooperative ownership of the selected publication paths during mutation,
revalidate the ref/worktree/index observation at admission, and observe afterward.
Declare that local concurrent actors bypassing that ownership are outside the
supported write guarantee; hashing twice is not a replacement for ownership. A
changed or unavailable observation yields stale/unavailable, not permission to
retry with new assumptions. Do not add elapsed-time expiry to a valid user task.

There is no atomic transaction spanning SQLite, ref, index and filesystem. Before
mutation retain sufficient exact operation intent/preimages under the existing
owned lifecycle to explain a partial attempt. On failure inspect actual state and
return `reconciliation-required` or `unknown` as appropriate while preserving the
already-published receipt. Do not rollback over newer user bytes. A later explicit
observation/completion must reuse the admitted intent and remain idempotent. Any
journal/artifact added for interrupted reconciliation has a named owner, version,
byte bounds and retention; use no second generic task engine. If safe write ownership
or recoverable partial effects cannot be established, ship the truthful observation
and keep the write capability unsupported until that proof exists.

### D6 — Explain exposure and reuse decisions at their existing owners

Have application qualification return an internal structured blocker carrying the
actual blocking module, its exposure state and dependency edge/chain. The authoring
`preview_application` projection can show it and a supported inspect/read request.
The application-purpose adapter keeps its non-disclosure projection. Preserve valid
exposure rules; an approved detail does not automatically approve its Router or
other prerequisites. Bound dependency explanations and avoid partial private content.

Pass an explicitly available predecessor Analysis from focused `revise` to the
existing retained-decision evaluation path. The original records remain immutable.
Reuse fact observations, coverage attestations and dispositions only when the current
execution contract, subject, dependency fingerprints, evidence and authorization
still validate. Matching a fingerprint is necessary in the reproduced case, not a
universal authorization shortcut. Never swallow an unrelated corruption/authority
error as "not reusable". No hidden store-wide latest-Analysis search is introduced.
A bare revision without a selected Analysis stays explicit; do not invent prior work.

Expose bounded `reused`, `needs-decision`, `changed-dependencies` and `new-obligation`
information derived from the evaluator's actual comparisons. Include exact dependency
class/identity and old/new digests only to the authorized author. The source already
owns structured dependency fingerprints; there is no need for a second graph or a
heuristic "metadata is harmless" test.

Final `ProposalReadiness` decisions bind Analysis, revision and expected target.
They are not automatically copied onto a successor. Reusing lower-level decisions
can remove repeated submissions while a new final review still authorizes its new
subject. A broader cross-revision approval policy would be a different admitted
contract, not part of this plan.

### D7 — Make the successful path concise without another identity system

Use existing compact workflow summaries and explicit detail reads. Include new
publication/evidence/reuse information once in the result, with exact handles needed
for durable continuation. Full detail remains available. Human-friendly labels are
display-only; no short-ID resolver, server session or loss of cold continuation.

Provide contract-checked task examples for original evidence versus bound evidence,
changed candidate evidence, required read_many snapshot, resolve_many, review,
apply/observe and explicit reconciliation. Reuse discovered shared definitions;
do not restore large eager description-embedded schemas or require discovery before
every call. Measure the actual authoring trace and repair counts. Do not claim fewer
model tokens, latency or calls from JSON-size changes alone.

### D8 — Version actual boundaries, not all history

The inspected public interface is 45. New outputs/actions require the next unused
interface edition (46 if still unused at implementation). If milestones deploy
separately with later contract changes, version each actual release; do not force
unrelated integrated work back to a planned number. Update a1-interface, canonical
schema, generated models/catalogs/examples and direct clients atomically.

Keep existing proposal/revision, Analysis, readiness, application and coverage-receipt
encodings unless a specific new persisted representation changes their selected
meaning. Evidence captures and reconciliation intent have their own new discriminated
record kinds/versions and exact identity inputs. Their bytes may cause new candidate
commits, as expected; they do not retroactively alter old revision IDs. Retain real
old record readers where required by installed data, with exact version dispatch;
this is not revival of retired input-schema compatibility.

Cold old-producer/new-consumer checks must cover historical snapshots, proposals,
Analysis, readiness, admitted recovery and published v1 receipts. Do not fabricate
missing origin or checkout-before state for legacy references/applications. Missing
source data is unavailable, not a migration-by-guessing. No store deletion, mass
rewriting of accepted receipts, or automatic conversion of old evidence into bundles.

## Simplicity And Ownership Review

**Applicability:** `applicable`

- Independent concepts and dimensions: Git publication, checkout synchronization,
  evidence acquisition, evidence admissibility, authorization, exposure and rendering
  change for different reasons. Keep them at existing Git, Engine, Analysis and
  projection owners. The new evidence-binding module owns only capture/bundle lifecycle.
- State, identity, value, time, policy, and mechanism: immutable evidence bytes,
  revision and application facts remain exact values; live permissions, refs and
  working files are observations. A bundle is source material, not decision truth;
  a prior applied outcome is history, not a guarantee of present HEAD.
- Caller and composition-root knowledge: callers choose exact sources and actions,
  then reuse references/contexts. They should not reconstruct commits from opaque IDs,
  manually duplicate candidate bytes, infer why evidence changed phase, or script
  index repair. Composition supplies the correct resolver and worktree authority.
- Representative change paths and forced owners: another exposure blocker changes
  the qualification owner and authorized projection, not Git. An evidence-origin
  extension changes binding/admission and export tests, not rule evaluation. Another
  Git layout is admitted at Repository Git rather than through a facade workaround.
- Stable Interfaces versus hidden knowledge: canonical EvidenceReference and existing
  portable receipt semantics are reused with explicit bundles; collection never
  searches arbitrary JSON for evidence-shaped objects. Generic trust validators do
  not know Engine private handles or read filesystem paths themselves.
- Independent evolution, testing, failure, and replacement: receipt reporting can
  succeed while checkout observation is unavailable. Evidence capture/preflight and
  reconciliation have separate negative/fault tests. Production publication remains
  isolated from mutation of the selected checkout.
- Necessary complexity and containment: source provenance, late authority checks
  and partial Git effects are genuine obligations. Keep the first reconciliation
  conservative and bounded. Missing capability is explicit; no silent fallback to
  reset or live-path evidence and no universal artifact/approval registry.
- Deletion and cumulative machinery result: remove duplicated destination-evidence
  interpretation from phase-specific loops into one preparation owner; eliminate
  focused re-submission by reusing the existing evaluator; propagate blocker data
  rather than make authors rediscover it. At most two justified new focused actions
  (bind evidence and reconcile application) replace manual multi-step work. Any new
  abstraction must demonstrate reduced caller knowledge, not just smaller files.

## Milestones

### A1 — Explicit publication observations and early evidence failures

**Status:** `Verifying` — the repaired implementation and local A1 gate are complete; exact-head hosted checks, the required Passeur security/lifecycle review, and main integration remain pending.

**Goal:** make existing success/failure truthful before extending evidence capability.

**Write set:** the existing engine.py, agent_workflow.py, tools.py error projection,
Analysis trust/error and coverage_publication preparation boundary; Repository Git
read-only publication/worktree observation; canonical contracts/generated files and
direct tests/examples/guidance; this plan. Correct the affected supporting-workflow
fixture and its cache-enabled caller without changing accepted Security exposure.

**Work:** reproduce the recorded facade cases on the integrated candidate; add durable
receipt/fresh checkout observation; share side-effect-free evidence preflight before
readiness; expose bounded authoring phase/reference context; retain all final checks.
Create one planned coherent interface update, with exact old-consumer dispositions.

**Gate:** The local A1 gate passed on the repaired candidate `fab920f4`. Publication and recovery preserve
checkout/index state; durable receipts remain distinct from fresh checkout
observations, including unknown outcomes and a replacement MCP process. Evidence
preflight rejects incompatible destination bytes and paths that publication will
overwrite before readiness; final candidate validation remains in place. No global
source-binding migration or new reconciliation write is hidden in A1. Exact-head
hosted checks and the required Passeur security/lifecycle review remain outstanding.
Do not begin A2's dependent implementation until A1 is accepted and merged to
`main`. See the implementation result in the [execution ledger](execution-ledger.md).
A2 extends the evidence matrix to bound references.

### A2 — Explicit evidence bindings and portable artifacts

**Status:** `Planned`; follows A1.

**Goal:** safely use selected baseline/candidate/imported evidence across all phases.

**Write set:** one new Engine evidence-binding module and its composition adapter;
existing Snapshot aggregate use, trust resolver boundary, logical/final candidate
assembly and managed evidence-path integration; canonical action/result contracts,
inspect/evidence normalization consumers, tests and guidance. Analysis coverage
receipt code changes only if the vertical proof establishes a necessary contract
extension; preserve v1 semantics and declare it before implementation expansion.

**Work:** first prove one changed-page baseline acquisition through decision,
readiness, candidate inclusion and a cold receipt read. Then extend the same owner
to exact candidate and explicit local capture. Verify source digest, origin identity,
reachability, quotas, graph retention, no collision or self-reference, and disclosure
of exported evidence. Do not add source-independent authority or provider guessing.

**Gate:** A-C3/A-C4 plus A-C2 for old and bound references; no original store/root
needed for exported receipt validation; mutated original local source cannot mutate
a bound artifact, while its governing live authorization/revocation still changes.
A successful static reference parse alone does not admit the provider/material.

### A3 — Explicit, guarded checkout reconciliation

**Status:** `Planned`; follows A1, integrated after A2 in this sequence.

**Goal:** replace unsafe manual repair with one narrowly owned opt-in operation.

**Write set:** Repository Git reconciliation primitives and direct tests; Engine
application coordination and optional versioned intent storage; generated operation,
result and permission declarations; tests and authoring instructions. No general
worktree management platform or publication-policy change.

**Work:** turn the positive/conflict Git feasibility into a verified observation and
one explicit mutation, with supported-layout declaration and current-state guards.
Test uncertain outcomes and process interruption before advertising safe completion.
Keep no-effect repeated calls idempotent and late changes visible. Default is observe.

**Gate:** A-C5, verified preservation of unrelated index/worktree distinctions,
conflict refusal and recoverable partial effects. Arbitrary same-file merging is
unsupported. If the initial supported-layout proof fails, retain truthful observation
and block only the write capability rather than weakening its safety promise.

### A4 — Explain candidate blockers and reuse valid Analysis decisions

**Status:** `Planned`; follows A1–A3.

**Goal:** reduce rediscovery and renewed submissions without reusing approvals blindly.

**Write set:** context_projection/qualification internal blocker representation;
engine retained-decision reuse; focused workflow composition/presentation; generated
bounded diagnostic/summary types and examples; direct purpose/reuse tests and guide.

**Work:** preserve application redaction while exposing authoring cause chains; pass
selected predecessor Analysis into the existing evaluator; return precise validated
reuse/invalidation summaries; add concise real-task examples, including read_many's
required snapshot. Keep final review bound to the successor.

**Gate:** A-C6/A-C7, literal old/new dependency cases, no unauthorized disclosure,
fresh evidence/capability checks, same result as explicit fresh decisions, no added
mandatory discovery or status call, and bounded compact/full equivalence.

### A5 — Supported integration, author workflow and independent acceptance

**Status:** `Planned`; follows the coherent source candidate.

**Goal:** establish externally meaningful improvement and close only this plan.

**Write set:** qualification instruments, current guides, plan/evidence and generated
verification inputs. Repairs stay at the preceding owners unless a re-plan trigger
changes their meaning. No production policy edits to fabricate a qualification task.

**Work:** run the current unchanged locked Python 3.12 CI selections including repaired
baseline fixture tests, cold old/new records, a separate recipient's evidence read,
and an authorized fresh agent task in a disposable repository. Record runtime/catalog,
exact source/tree, source locator, all publication observations, required decisions,
repair/discovery counts, and unrelated Git state before/after. Compare like-for-like
steps; explain intentional diagnostic/contract changes. Review the coherent source
independently and verify only actual repairs afterward.

**Gate:** every A-C claim supported at its named fidelity, findings dispositioned by
the acceptance owner, exact candidate integration identified. Reuse valid earlier
evidence within scope; no full CI rerun merely to rewrite a passed result's prose.
No automatic acceptance by a tool or by this planning review.

## Required Verification Matrix

- **Publication:** current target checkout, detached/other branch, later target advance,
  unrelated staged+unstaged on one file, untracked files, overlapping changes,
  missing old objects, failed result persistence, target moved during publication,
  post-publication observation failure, restart and repeated observe/recover.
- **Evidence:** changed/deleted evidence path, unchanged context evidence, baseline vs
  exact candidate bytes, explicit imported file, false provider/source, bad digest,
  unsupported type, missing snapshot/aggregate/object, size limits, denied capability,
  revoked authorization, capture failure, portably exported artifact and tampering.
  The actual changed-page fixture must fail before readiness with legacy reference
  and succeed with a correctly authorized bound artifact, not a replacement digest.
- **Reconciliation:** clean old index, already current, unrelated index/worktree deltas,
  overlapping same file, untracked obstacles, additions/removals/mode changes,
  linked worktrees, stale observations, locks, unsupported index/layout, hostile
  filters/configuration, partial write/cleanup failure and replacement process.
  Test user-file preservation by exact bytes/modes/staging, not merely Git status.
- **Reuse/exposure:** unchanged dependency with unrelated edit; changed module,
  applicability, provider, execution authority or evidence; removed obligation and
  new obligation; explicit unknown facts; denied private Router; multiple blockers;
  bounded chains and safe application rejection; selected Analysis versus bare revision.
- **Regression:** existing publication/recovery, consumer registration, coverage and
  receipt, request evidence, proof reuse, snapshots, generated contracts and relevant
  Git tests; current full required CI and structural checkpoint. Mutations exercise
  the old failure where meaningful; normal acceptance tests use real owners.

## Blockers

There is no blocker to A1 source work after explicit admission. The precise original
agent run is unavailable, so do not claim a historical transcript replay. The pinned
baseline has a known test-fixture CI failure; its correction belongs to A1's narrow
qualification setup. The evidence-bundle carrier and recoverable reconciliation are
new capability proofs required in A2/A3, not assumed completed implementations.
The actual host/model and independent reviewer are not executed in this planning
task; A5 owns their authorized procedures. Source work must not imply those passed.

## Re-Plan Triggers

Re-plan if evidence requires an independent provider or stronger origin authentication,
if bundle carrier semantics cannot satisfy actual consumers, if self-reference or
portable-history support requires reinterpretation of old receipts, if safe Git
write ownership cannot be provided for the promised supported layout, if equivalent
prior Analysis decisions cannot pass existing fresh authorization, or if current
source changes alter the verified baseline assumptions. Declare actual new public,
persisted or security boundary changes before implementation; do not install a
fallback parser, speculative cache or broad framework to avoid the decision.
A discovered direct consumer of the selected contract extends that write set with
an issue disposition; it does not automatically reopen unrelated accepted projects.

## Final Acceptance

This is a reviewed **plan**, not a source implementation or new acceptance verdict.
Baseline observations, the 2000-dated deterministic publication, passing structural
checks and prior external reports do not qualify the future candidate. Keep original
failed probe drafts, CI failures, repaired fixtures and final candidate results at
their actual identities. Source/CI review is separate from authoring publication;
no production mutation, remote push or acceptance-status change occurred here.

After A1–A5 satisfy their claims, close this plan and retain non-blocking observations
as explicitly deferred new work. No next refactor is automatically admitted.

- Acceptance status: `pending`
- Final status: `Planned`
