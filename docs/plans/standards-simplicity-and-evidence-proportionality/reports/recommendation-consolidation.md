# Recommendation Consolidation And Normative Design

**Status:** planning evidence for the Standards Simplicity And Evidence
Proportionality plan.

## Decision

The accepted A1/A1b audit produced twelve standards proposals (S1-S12), while
the *Simple Made Easy* conformance analysis produced eight refinements
(C1-C8). They are not twenty independent policy requirements. Most are
different observations of five related failures:

1. local ownership review did not decide whether the composed artifact was
   simple;
2. correctness machinery could be admitted without proving its marginal need
   or lifecycle;
3. validation policy did not distinguish proof boundaries and failure
   consequences;
4. authority/version machinery could grow beyond actual lifetime and consumer
   promises; and
5. systemic repair and custom proof tooling lacked proportional stopping and
   substitution rules.

Dependency-local invalidation is an implementation-design finding, not a sixth
normative family in this plan. Milestone 0 demonstrated a bounded candidate for
named deciding dependencies, but retained the current standard because the
known concrete consumer—repository-specific Python tooling—is excluded.

The accepted A1c Linux implementation supplies fresh evidence for the three
unimplemented families. It can confirm, refine, or falsify the audit's
assumptions, but it cannot become the project-agnostic wording or be edited by
this standards plan. Only Milestone 1 was normative while A1c was developed, so
A1c can test the usefulness of that accepted change; it cannot establish a
causal success or failure for the still-unimplemented Milestones 2 and 3.

A final depth-and-Locality review found that the first remaining-milestone
design still layered policy over rules already present in Acceptance Claims,
Validation Proof Lifetime, claim-directed diagnosis, dependency comparison,
and actual-consumer versioning. The refined design deepens those existing
owners, retains sufficient prose, and removes broad downstream rewrites.

## Consolidated Change Families

| Family | Recommendations | Normative result | Why this owner | Supporting evidence |
| --- | --- | --- | --- | --- |
| N1 Composed simplicity | S1, S2, C1-C4, C6-C8 | Revise Core; add Architecture composed-design admission; require a Planning applicability record and an artifact/change probe. | Core owns the universal meaning; Architecture owns material design admission; Planning owns the durable decision record. | A1b's locally coherent Modules composed into 22-to-36 dependency directions, a 2,539-line composition root, and a nine-surface kind-addition path. Commit `44de7dff` removed the applicable review without structural failure. Hickey H1-H6/H8-H9 distinguish simple from easy and decomposition from decomplection. |
| N2 Evidence necessity and scoped risk | S3, S5, S11, C5 | Revise the existing Acceptance Claims owner with permanent-evidence marginal value, overlap, lifecycle cost, retention/removal, and exact-byte-purpose admission. Do not add a parallel Verification owner or repeat the procedure downstream. | Acceptance Claims already owns the smallest complete claim set; Quality Gates, Oracle Boundaries, Coverage, and Claim-Directed Diagnosis already own risk, cost, adequate oracles, and trace-led investigation. The missing semantics deepen that Interface. | A1/A1b accumulated 218-226 suites, 53 retained Bash checkers, repeated proof families, and 917 hashed suite-input files. A1c is smaller but still contains layered checks whose marginal independence must be demonstrated. Counts locate cost; the claim audit supplies removal criteria. |
| N3 Validation proof and failure behavior | S4, S10 | Register Validation Proof Lifetime unchanged; revise only Invariant Contracts' over-broad failure-mechanism prohibition to distinguish contained defects from arbitrary input, escaping invalid state, and authoritative-state corruption. | Contracts already owns complete proof lifetime. Repeating it would not make agents apply it; the remaining normative gap is failure consequence. Verification owns evidence admission, not validity procedure. | Existing prose already requires direct consumption of the same intact proof-bearing representation and new proof after representation loss, mutation, contract change, or a new authority boundary. A1c's facade/decode repetition is therefore an application question. Current invariant wording still fails to distinguish contained programming defects from corruption or external emission. |
| N4 Promise proportionality | S6, S7, S10 | Revise Immutable Authority Closure and Version Scope so semantic closure and compatibility follow stated lifetime, reconstruction, overlap, deployment, persistence, and actual-consumer promises, without prescribing separate identity/codec/handle/version/lifecycle objects. | Architecture owns authority closure; Contracts owns compatibility and invalidation promises. | A1/A1b closure fanout grew from 7 to 27 relationships and v10/v11 were atomic cutovers with no retained A1 reader. A1c shows that a complete closure may be an aggregate and that format discriminators, identity revisions, compatibility versions, migration versions, and allocation ordinals have different roles. Its several version fields do not prove historical readers or cross-engine migration promises. |
| N5 Bounded correction and established tooling | S8, S12, C4-C5 | Revise replanning/systemic rules with owner-and-reachability stops, deletion/smaller-Interface remedies, proof substitution, composition recheck, and an established-dependency comparison when standardized semantics would otherwise be reimplemented. Thin adapters and domain-specific products remain valid when they own distinct local semantics. | Planning owns repair scope; Dependencies owns implementation-versus-dependency; Verification supplies evidence adequacy. | A1c removed much A1b machinery through aggregate ownership and a smaller Interface, showing that deletion can be a systemic repair. A1/A1b systemic reviews found real defects but also expanded inventories, AST logic, identities, and matrices; `jsonschema` and SQLite removed local semantic products while a custom analyzer created its own Interface, tests, and repair loop. |
| P1 Dependency-local invalidation | S9 | No normative change in this plan. Retain Projection Completeness; preserve the bounded prototype for a separately scoped Coding Standards Python coverage-design audit. | Planning already owns change-specific dispositions. The current global-horizon behavior belongs to repository-specific coverage implementation and its complete owner/consumer boundary. | The graph grew from 41/207 to 47/387 units/relationships and one guardrail renewed all 44 subjects. The [prototype](dependency-local-invalidation-prototype.md) demonstrates exact local, global-protocol, missing-disposition, and unrelated-consumer behavior, but implementation feasibility does not prove a generally applicable normative deficiency. |

## What Is Retained

The change is a refinement, not a rejection of the standards recovery:

- generated-contract routing and external semantic oracles;
- schema dialect and vocabulary admission;
- identity versus instance equality;
- direct use of intact proof-bearing values;
- conditional Security for real trust/adversarial surfaces;
- claim-directed Verification and negative-fixture isolation;
- non-ambient reconstruction when a durable replay contract promises it;
- independently scoped versions when actual consumers or lifetimes differ;
- fine-grained policy units and explicit consumer dispositions.

These controls have reproduced defects or clear consumer consequences. Their
applicability is narrowed; their semantic outcomes are not weakened.

## Repository Conformance Evidence Portfolio

These artifacts let this repository demonstrate that its own standards change
is coherent. They are not an enforcement system imposed on adopters. An
adopter may choose manual review, an established tool, custom tooling, or no
automation according to its accepted claims and risks.

The smallest planned repository portfolio is:

- expand `core-simplicity` rather than add separate simple/easy, composition,
  deletion, and cumulative-admission suites;
- update the existing Planning consolidation/template suites and structural
  checker to make applicability durable;
- extend `acceptance-claims` with one focused evidence-necessity fixture; do not
  create `evidence-necessity-and-risk` as a parallel policy or suite;
- extend `contract-invariants` with the existing Validation Proof Lifetime
  fixture rather than add a second Contracts suite;
- extend `contract-authority-scope` with immutable closure as well as its
  existing authority/version decisions; do not register
  `architecture-owner-contract` as another closure suite;
- extend the existing dependency and systemic suites for their revised
  decisions;
- do not create or change generic verifier Python for normative wording that
  declarative checks can express.

The graph relation name `enforcement-suite-projection` is an existing
repository artifact classification. It means that the named suite is evidence
for the source policy unit inside this repository; it does not mean the written
standard enforces itself or that users must run that suite.

## Project-Agnostic Drafting Tests

Every normative sentence must pass all of these tests:

1. It can be applied without knowing A1, A1b, A1c, Python, JSON Schema, SQLite,
   Git, or this repository's package layout.
2. It selects from observable ownership, consumer, lifetime, risk, failure,
   and change facts rather than construct or test counts.
3. It permits both keeping a coherent deep Module and introducing a useful
   Seam; separation itself is not a simplicity verdict.
4. It permits immediate failure and trace-led debugging for contained internal
   defects while retaining validation where arbitrary input or escaping
   consequence makes invalid state reachable.
5. It can remove, aggregate, or decline machinery instead of only making an
   admitted mechanism more exhaustive.
6. It states when the rule is not applicable and never converts Hickey's
   technology examples into mandates.
7. It states the required decision or outcome without requiring this
   repository's checker, suite, prompt, or graph machinery as the adopter's
   enforcement mechanism.

## Evidence Limits

- A1/A1b show that the earlier rules admitted a globally complected result;
  they do not prove every A1b Module or check unnecessary. A1c supplies current
  counterexamples and consumers, but only Milestone 1 can be evaluated as a
  standard that was actually in force during A1c development.
- Commit history supports a missing admission/application path; it cannot
  recover every human reason for a design choice.
- The local-invalidation prototype proves completeness only relative to named
  deciding dependencies. It cannot discover a real semantic consumer never
  declared by humans, and it does not prove that a repository-specific coverage
  algorithm belongs in general standards. Explicit review and reviewed-empty
  authority remain; any implementation change requires its own complete audit.
- The planned relationship set began from commit `351e7852`, was revalidated at
  Milestone 0 base `ac418826`, and is now stale relative to the accepted A1c
  49-unit/407-relationship graph. Every unimplemented owner and evidence-owner
  rationale must be freshly queried and dispositioned before a normative edit.
- A current graph declaration is not proof that its evidence owner actually
  decides the cited claim. In particular, the generic immutable-authority
  fixture is presently attributed to the A1c-specific snapshot suite even
  though that suite does not consume it. `contract-authority-scope` is the
  planned generic owner because it already decides Architecture authority and
  Contracts version scope; Milestone 3 must verify and implement that ownership
  before acceptance.
