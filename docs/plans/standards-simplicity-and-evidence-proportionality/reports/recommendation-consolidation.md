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

Dependency-local invalidation is a sixth, conditional hypothesis. It remains a
prototype until its completeness properties are demonstrated.

## Consolidated Change Families

| Family | Recommendations | Normative result | Why this owner | Supporting evidence |
| --- | --- | --- | --- | --- |
| N1 Composed simplicity | S1, S2, C1-C4, C6-C8 | Revise Core; add Architecture composed-design admission; require a Planning applicability record and an artifact/change probe. | Core owns the universal meaning; Architecture owns material design admission; Planning owns the durable decision record. | A1b's locally coherent Modules composed into 22-to-36 dependency directions, a 2,539-line composition root, and a nine-surface kind-addition path. Commit `44de7dff` removed the applicable review without structural failure. Hickey H1-H6/H8-H9 distinguish simple from easy and decomposition from decomplection. |
| N2 Evidence necessity and scoped risk | S3, S5, S11, C5 | Add one Verification unit covering reachable failure, consequence, actor/failure source, proof boundary, oracle, marginal value, overlap, cost, retirement, and exact-byte purpose. Security retains adversarial semantics; Resilience and Diagnostics consume consequence, recovery, detection, and diagnosis facts. | Verification decides whether evidence proves and is needed for a claim; Security should not become a blanket model for ordinary internal errors, while Resilience and Diagnostics retain their established owners. | 218-226 suites, 53 retained Bash checkers, repeated proof families, 917 hashed suite-input files, and no current evidence-lifecycle owner. Counts locate cost; the claim audit supplies the removal criteria. |
| N3 Validation proof and failure behavior | S4, S10 | Register and revise Contracts' existing Validation Proof Lifetime and Invariant Contracts sections; extend their existing suite family. | Contracts owns construction, validity, proof lifetime, and failure semantics; Verification owns evidence of those rules. | Repeated A1b decode paths coexist with an existing rule against revalidating intact proof-bearing values. Current invariant wording does not distinguish contained programming defects from corruption or external emission. Reproduced JSON Schema and durable-boundary defects remain protected. |
| N4 Promise proportionality | S6, S7, S10 | Revise Immutable Authority Closure and Version Scope so closure and compatibility follow stated lifetime, reconstruction, overlap, deployment, persistence, and actual-consumer promises. | Architecture owns authority closure; Contracts owns compatibility and invalidation promises. | Closure fanout grew from 7 to 27 relationships; fourteen stored kinds acquired local obligations; v10/v11 were atomic cutovers with no retained A1 reader. Genuine cold replay and independently deployed/persisted contracts remain counterexamples to simplification. |
| N5 Bounded correction and established tooling | S8, S12, C4-C5 | Revise replanning/systemic rules with reachability stops, deletion/smaller-Interface remedies, proof substitution, composition recheck, and dependency preference when mature tooling owns the required semantics. | Planning owns repair scope; Dependencies owns implementation-versus-dependency; Verification supplies evidence adequacy. | Systemic reviews found real defects but also expanded inventories, AST logic, identities, and matrices. `jsonschema` and SQLite removed local semantic products; a custom analyzer created its own Interface, tests, and late repair loop. |
| P1 Dependency-local invalidation prototype | S9 | Prototype first; revise Projection Completeness only if the exact algebra detects changed/missing consumers and stale authority while leaving truly unrelated subjects stable. | Planning owns change-specific disposition; graph/verifier implementation remains separately owned. | The graph grew from 41/207 to 47/387 units/relationships and one guardrail renewed all 44 subjects. The audit explicitly rated the change below unconditional confidence. |

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

## Enforcement Portfolio

The smallest planned portfolio is:

- expand `core-simplicity` rather than add separate simple/easy, composition,
  deletion, and cumulative-admission suites;
- update the existing Planning consolidation/template suites and structural
  checker to make applicability durable;
- add one `evidence-necessity-and-risk` suite because no existing suite decides
  marginal necessity or retirement;
- extend `contract-invariants` with the existing Validation Proof Lifetime
  fixture rather than add a second Contracts suite;
- extend the existing authority, version, dependency, and systemic suites for
  their revised decisions;
- do not create or change generic verifier Python for normative wording that
  declarative checks can express.

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

## Evidence Limits

- A1/A1b show that the present rules admitted a globally complected result;
  they do not prove every A1b Module or check unnecessary.
- Commit history supports a missing admission/enforcement path; it cannot
  recover every human reason for a design choice.
- The local-invalidation concern is well supported, but the replacement
  algorithm is not. That is why P1 remains conditional.
- The planned relationship set is based on the graph at commit `351e7852` and
  must be re-queried before implementation.
