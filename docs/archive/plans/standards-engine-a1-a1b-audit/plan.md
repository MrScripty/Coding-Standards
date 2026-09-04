# Plan: Audit Standards Engine A1 And A1b

**Plan status:** `Accepted`

**Current phase:** Audit accepted

**Next slice:** None in this plan; normative standards changes and binding A1c
design require separate admission.

**Acceptance status:** `satisfied`

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Produce an inspectable, source-cited comparison of Standards Engine A1 and the
accepted A1b implementation, including the design and development history that
created each system and the source model behind the repository's complection
principle, so later standards revisions and A1c design decisions can distinguish
product requirements, missing standards, missed application, conflicting
guidance, standards-induced complexity, and merely nominal decomposition.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AUD-A1 | A1's formation, accepted boundary, later amendments, design, implementation, and verification are reconstructed from primary repository sources with exact commit citations. | `focused` | `not-applicable` | `automated` | `satisfied` | [A1 history and design](reports/a1-history-and-design.md) |
| AUD-A2 | A1b's problem statement, C1-C7 design evolution, rejected candidates, accepted implementation, and review corrections are reconstructed from primary sources. | `focused` | `not-applicable` | `automated` | `satisfied` | [A1b history and design](reports/a1b-history-and-design.md) |
| AUD-A3 | Standards revisions effective during A1 and A1b are pinned and their causal or permissive relationship to observed design decisions is classified without inferring causation from compliance alone. | `focused` | `not-applicable` | `automated` | `satisfied` | [Standards evolution and causality](reports/standards-evolution-and-causality.md) |
| AUD-A4 | A reproducible comparison measures Interfaces, Modules, dependencies, representations, versions, implementation size, change Locality, and operational obligations at fixed A1 and A1b revisions. | `focused` | `not-applicable` | `automated` | `satisfied` | [Architecture and complexity comparison](reports/architecture-and-complexity-comparison.md) |
| AUD-A4C | A consumer, guarantee, and threat-model audit distinguishes externally demanded behavior from standards-, plan-, review-, and implementation-selected prevention machinery. | `focused` | `not-applicable` | `automated` | `satisfied` | [Consumer guarantee and threat model](reports/consumer-guarantee-and-threat-model.md) |
| AUD-A5 | A claim-level verification audit classifies A1 and A1b tests, suites, checkers, validators, digests, and contracts by necessity, oracle, overlap, proof substitution, and lifecycle without declaring individual evidence redundant from counts alone. | `focused` | `not-applicable` | `automated` | `satisfied` | [Verification portfolio audit](reports/verification-portfolio-audit.md) |
| AUD-A6 | A synthesis records revised findings, confidence, counterevidence, proposed project-agnostic standards changes, and evidence-constrained A1c design principles. | `focused` | `not-applicable` | `automated` | `satisfied` | [Final synthesis](reports/final-synthesis.md) |
| AUD-A7 | Every material claim in the final synthesis traces to a commit, repository artifact, generated inventory, or explicitly labelled inference, and repository checks pass. | `integration` | `not-applicable` | `automated` | `satisfied` | [Final verification record](execution-ledger.md) |
| AUD-A8 | Hickey's original *Simple Made Easy* presentation is reconstructed from conference-owned audiovisual/session sources and a clearly labelled secondary transcript, then compared with the current normative text, planning projection, decision fixture, policy graph, and A1b admission history without reproducing the copyrighted transcript. | `focused` | `network-research` | `manual` | `satisfied` | [Primary-source research](reports/simple-made-easy-primary-source-research.md) and [complection conformance audit](reports/simple-made-easy-complection-conformance.md) |

## Scope

### In Scope

- A1 design and implementation history beginning with the navigation-analysis
  effort and ending at the exact A1 comparison boundary selected by the audit.
- A1b standards recovery, redesign planning, C1-C7 alternatives, implementation
  candidates, review findings, and accepted implementation commit
  `84412f22fa9fe082f089eaa347c30c23f185ffee`, tree
  `8e0f96a61fcea2398418b17d16a061c20f7463f5`.
- Standards snapshots and changes that materially affected architecture,
  contracts, verification, planning, security, diagnostics, and implementation.
- Static and historical measures used as diagnostic evidence, never automatic
  design verdicts.
- Verification necessity, test-surface placement, threat-model scope,
  validation proof lifetime, diagnostic sufficiency, and evidence overlap.
- General standards findings and A1c design constraints supported by the audit.
- Conference-owned presentation sources and a secondary transcript used to
  reconstruct the general source model for simple, easy, compose, and complect.

### Out Of Scope

- Normative standards edits, policy-graph mutations, or new executable suites.
- A1c implementation, a binding A1c architecture, or activation of A2.
- Rewriting or correcting historical A1 or A1b records.
- Removing tests, validators, digests, contracts, packages, or runtime code.
- Inferring redundancy, causation, or design quality from raw counts alone.
- Reproducing a full copyrighted transcript or treating reaction commentary as
  Hickey's source argument.

## Constraints And Assumptions

### Constraints

- Historical claims cite immutable commits and paths rather than current-file
  wording when that wording changed after the event.
- The audit distinguishes observed fact, repository-authored rationale,
  inference, and recommendation.
- A1 and A1b are not treated as feature-identical. Direct comparisons identify
  which guarantees are common, added, removed, or strengthened.
- Subagents write only their assigned reports. The integration owner alone
  changes this plan, ledger, issues, shared synthesis, and generated inventories.
- The accepted A1b implementation tree is evidence authority even though the
  final acceptance record was committed afterward at `580d9c95`.

### Assumptions

- `933c9ab93d18ede987d449a6fe7b9ebd313922fc` records A1 acceptance, but the
  audit must identify the exact implementation tree and later A1 amendments
  that form the fairest comparison base.
- Repository Git history, plans, ADRs, reports, source, tests, and policy graph
  are the primary sources for this audit.
- The current clean worktree permits non-overlapping report preparation.

## Binding Decisions

| Decision | Owner | Evidence | Supersedes |
| --- | --- | --- | --- |
| Pin A1b to implementation commit `84412f22` and tree `8e0f96a6`; treat `580d9c95` as acceptance evidence rather than implementation content. | Audit integration owner | [A1b final acceptance](../standards-engine-a1b/reports/a1b-final-acceptance.md) | Earlier candidate `3da674c1` as final comparison boundary |
| Observe A1 runtime at accepted v9 `2359a987` and accepted v10 amendment `7bc8bd07`; use `36dd7579` only for the accepted A1b planning/standards base; compare accepted A1b at `84412f22`. | Audit integration owner | A1 and policy-impact-v2 acceptance records, the four fixed trees, and the [inventory method](reports/inventories/README.md) | One-boundary comparison that attributes post-acceptance A1 amendments or planning-only standards changes to A1b runtime |
| Use Module, Interface, Seam, Adapter, Depth, Leverage, and Locality consistently in design evaluation. | Architecture analysis owner | Codebase-design framework | Raw file/package counts as design authority |
| Use report-per-question delegation with one serial synthesis owner. | Planning owner | Planning concurrent-work contract | Shared multi-agent editing |
| Treat the Strange Loop session and restored conference upload as the primary audiovisual source, InfoQ as conference-publisher corroboration, and the community transcript only as a timestamp/search aid with explicit limitations. | Source-research owner | [Primary-source research](reports/simple-made-easy-primary-source-research.md) | The supplied reaction video's mixed-speaker captions as Hickey authority |

## Evidence And Oracle Plan

| Claim | Domain | Deciding oracle | Independent authority | Unsupported domain | Intended negative failure |
| --- | --- | --- | --- | --- | --- |
| Historical event occurred | Git history | Exact commit object, diff, and contemporaneous artifact | Git object database | Lost or rewritten unreachable history | Current prose used as historical authority without commit pin |
| A design promised a guarantee | Specification/design | Contemporaneous plan, ADR, report, schema, or Interface | Accepted record at the selected revision | Undocumented intent | Later interpretation substituted for recorded promise |
| Implementation supplied a guarantee | Behavior/structure | Source plus relevant accepted evidence at the fixed revision | Consumer path or independent review where available | Unexecuted historical environments | Documentation-only claim treated as implementation proof |
| Complexity changed | Architecture | Reproducible inventories plus qualitative Interface and Locality analysis | Representative change history | Subjective cognitive experience not recoverable from artifacts | Raw count used as automatic verdict |
| Evidence is necessary | Verification | Reachable failure, material consequence, adequate oracle, and non-subsumed protection | Contract, threat model, prior defect, or mutation/change history | Hypothetical unobserved failures | Test count alone used to declare redundancy |
| Standards influenced design | Causality | Standards effective before decision plus cited or mechanically enforced dependency | Decision history and counterevidence | Unrecorded human reasoning | Compliance alone treated as causation |

## Systemic Finding Audit

- Invariant family: architectural and verification proportionality across A1,
  A1b, future A1c, and the general standards library.
- Sibling producers and consumers: Core, Architecture, Contracts, Security,
  Resilience, Diagnostics, Verification, Planning, Implementation, Router,
  prompts, templates, fixtures, suites, policy graph, and Standards Engine.
- Authority and projection inventory: owned by the standards-evolution report
  and final synthesis; no normative consumer will change in this audit.
- Consumer dispositions: proposed only, with confidence and required evidence;
  implementation belongs to a later standards-change plan.
- Scope or sequencing replacement: finish evidence before selecting normative
  changes or binding A1c structure.

## Simplicity And Ownership Review

- Independent concepts: historical reconstruction, architecture comparison,
  verification audit, standards causality, and design synthesis.
- Intentional coupling: every synthesis claim must cite one or more independent
  reports or primary repository sources.
- Accidental coupling risk: using A1b's internal contracts or tests as the
  definition of required A1c behavior.
- Canonical authority scope and referenced authorities: this plan owns audit
  scope and status; reports own detailed evidence; Git and accepted historical
  artifacts remain primary authorities.
- Version and identity-invalidation scopes: reports identify commits and trees;
  no runtime or standards version changes.
- Policy/state/lifecycle owners: Planning owns the audit lifecycle;
  Documentation owns report quality; Verification owns claim sufficiency.
- Future changes that should remain independent: standards revisions and A1c
  architecture selection remain separate later efforts.

## Milestones

### Milestone 0: Pin Boundaries And Method

**Goal:** Establish the audit plan, immutable comparison candidates, report
contracts, and evidence method.

**Allowed write set:**

- `docs/archive/plans/standards-engine-a1-a1b-audit/plan.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/execution-ledger.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/issues.md`

**Tasks:**

- [x] Pin accepted A1b implementation and acceptance evidence.
- [x] Identify the initial A1 lineage and recorded acceptance commit.
- [x] Reconcile the exact A1 comparison implementation and standards snapshot.
- [x] Define evidence categories and non-overlapping report ownership.

**Acceptance gate:** Plan structure is complete and the worktree contains no
overlapping pre-existing changes.

**Status:** `Accepted`

### Milestone 1: Historical Research

**Goal:** Produce independent A1, A1b, and standards-evolution histories.

**Allowed write set:**

- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/a1-history-and-design.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/a1b-history-and-design.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/standards-evolution-and-causality.md`
- Integration-owner updates to plan, ledger, and issues.

**Tasks:**

- [x] Reconstruct A1 history and design.
- [x] Reconstruct A1b history and design.
- [x] Reconstruct standards changes and causal candidates.
- [x] Reconcile contradictions and missing history serially.

**Acceptance gate:** AUD-A1 through AUD-A3 have commit-pinned reports with facts,
inferences, counterevidence, and unresolved questions separated.

**Status:** `Accepted`

### Milestone 2: Architecture And Verification Comparison

**Goal:** Build reproducible structural inventories and a claim-level evidence
portfolio comparison.

**Allowed write set:**

- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/architecture-and-complexity-comparison.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/consumer-guarantee-and-threat-model.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/verification-portfolio-audit.md`
- Audit-owned generated inventories under
  `docs/plans/standards-engine-a1-a1b-audit/reports/inventories/` if needed.
- Integration-owner updates to plan, ledger, and issues.

**Tasks:**

- [x] Select fair fixed A1 and A1b implementation trees.
- [x] Inventory Modules, Interfaces, dependencies, representations, versions,
  implementation and test surfaces, and operational obligations.
- [x] Analyze representative change propagation from Git history.
- [x] Trace actual consumers, required guarantees, corruption/adversary paths,
  and consequences separately from selected preventive mechanisms.
- [x] Classify evidence by claim, failure reachability, oracle, overlap,
  proof substitution, threat model, cost, and lifecycle.

**Acceptance gate:** AUD-A4, AUD-A4C, and AUD-A5 are reproducible and avoid
count-only verdicts or unproved test-removal claims.

**Status:** `Accepted`

### Milestone 3: Synthesis

**Goal:** Produce revised, evidence-weighted conclusions for standards changes
and A1c.

**Allowed write set:**

- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/final-synthesis.md`
- Integration-owner updates to plan, ledger, and issues.

**Tasks:**

- [x] Classify each standards finding as missing, missed application,
  conflicting/ambiguous, standards-induced, product-required, or unresolved.
- [x] Record confidence, counterevidence, and the change needed to validate each
  recommendation.
- [x] Separate preserved A1/A1b merits from A1c implementation hypotheses.
- [x] Identify which earlier proposed standards changes are confirmed, revised,
  rejected, or still unproved.

**Acceptance gate:** AUD-A6 is complete and every material recommendation is
traceable to primary evidence.

**Status:** `Accepted`

### Milestone 4: Verification And Handoff

**Goal:** Verify the audit artifacts and hand off bounded later efforts.

**Allowed write set:**

- All audit-plan artifacts.

**Tasks:**

- [x] Verify links, commit identities, report cross-references, plan structure,
  diff hygiene, and absence of normative/runtime changes.
- [x] Record final unresolved questions and later-owner triggers.
- [x] Mark the audit accepted only when AUD-A1 through AUD-A7 are satisfied.

**Acceptance gate:** AUD-A7 passes and the final report names the exact inputs
for a later standards-change plan and A1c design effort.

**Status:** `Accepted`

### Milestone 5: Complection Source Addendum

**Goal:** Test the repository's complection principle and its enforcement path
against the source model in Rich Hickey's *Simple Made Easy* without changing
normative standards or selecting A1c architecture.

**Allowed write set:**

- `docs/archive/plans/standards-engine-a1-a1b-audit/plan.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/execution-ledger.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/issues.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/simple-made-easy-primary-source-research.md`
- `docs/archive/plans/standards-engine-a1-a1b-audit/reports/simple-made-easy-complection-conformance.md`

**Tasks:**

- [x] Distinguish the supplied reaction video from the original conference talk.
- [x] Build a copyright-safe timestamped proposition map from primary and
  explicitly qualified secondary sources.
- [x] Compare the source model with Core, Planning, fixtures, graph routing, and
  A1b's actual plan-admission history.
- [x] Separate general standards consequences from A1c and Standards Engine
  Python design questions.

**Acceptance gate:** AUD-A8 is satisfied, source limitations are explicit, the
conformance verdict traces to current and historical repository evidence, and
no normative or runtime artifact changes.

**Status:** `Accepted`

## Blockers

- `none`

## Re-Plan Triggers

- The exact A1 implementation boundary cannot be reconstructed from reachable
  primary history.
- A1 and A1b have materially different product guarantees that invalidate a
  direct comparison category.
- Historical artifacts contradict accepted commit content without a resolvable
  supersession record.
- A report finds a systemic standards consumer family outside the current audit
  scope that is necessary to support a material conclusion.
- Evidence cannot distinguish a standards effect from a product requirement or
  implementation decision; the conclusion must remain unresolved rather than
  be forced.
- Concurrent work overlaps an assigned report or shared planning artifact.

## Concurrent Work

| Owner | Primary write set | Adjacent write set | Forbidden/shared | Output/report | Integration order |
| --- | --- | --- | --- | --- | --- |
| A1 research agent | `reports/a1-history-and-design.md` | none | plan, ledger, issues, other reports, normative files, runtime code | Commit-pinned A1 history and design report | 1 |
| A1b research agent | `reports/a1b-history-and-design.md` | none | plan, ledger, issues, other reports, normative files, runtime code | Commit-pinned A1b history and design report | 1 |
| Standards research agent | `reports/standards-evolution-and-causality.md` | none | plan, ledger, issues, other reports, normative files, runtime code | Standards snapshot and causal analysis report | 1 |
| Consumer/threat-model agent | `reports/consumer-guarantee-and-threat-model.md` | none | plan, ledger, issues, other reports, normative files, runtime code | Consumer evidence, guarantee provenance, and scoped threat model | 2 |
| Source-research agent | `reports/simple-made-easy-primary-source-research.md` | none | plan, ledger, issues, other reports, normative files, runtime code | Primary-source hierarchy, transcript limitations, and timestamped proposition map | post-acceptance addendum |
| Audit integration owner | Plan, ledger, issues, comparison, verification, synthesis, inventories | all audit-owned paths after delegated reports complete | normative files and runtime code | Integrated audit | serial after each wave |

Concurrent Plan Integration does not apply: subagents have disjoint report
paths, do not modify shared authority, and one integration owner reads current
state after their work completes.

## Final Acceptance

- Acceptance status: `satisfied`
- Deferred follow-ups: normative standards implementation and binding A1c
  design remain separate later plans.
- Final status: `Accepted`
