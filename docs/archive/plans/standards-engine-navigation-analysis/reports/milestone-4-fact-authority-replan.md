# Milestone 4 Fact-Authority Replan

## Trigger

Consumer and impact dispositions carry decision fingerprints, but
`FactAnswerSubmission` does not. One applicability fact may unblock several
relationships, so binding its answer to any one relationship-specific
obligation would duplicate authority and invalidate a stable contextual fact
when unrelated topology changes.

Packet resolution and reuse are not implemented. The current clean boundary
therefore permits replacement without compatibility interpretation.

## Accepted Model

`standards_applicability` owns semantic `FactContract` values, typed values,
program compilation and evaluation, and reverse fact dependencies. A contract
binds stable ID, semantic revision, value domain, meaning, context kind,
answer/evidence contracts, and required authorization capability. Aliases and
display prompts remain lookup and rendering projections outside decision
identity.

`standards_analysis` derives a content-addressed `AnalysisContext` from the
changed policy identities and accepted/proposed semantic and structural state.
Relationship topology is excluded. A missing fact produces one
`FactRequirement` whose identity binds the canonical fact contract, analysis
context, and answer, evidence, and authorization contracts.

A typed `FactObservation` binds the requirement handle, validated value,
evidence, and authorization decision. Reuse is an exact lookup by requirement
identity. There is no separate prior-answer import algorithm and callers do not
echo dependency fingerprints.

### Immutable analysis state

Raw standards-change facts and caller-coordinated observation lists are not
public inputs. `AnalysisRequest` carries exact snapshots, changes, semantic
proposals, and at most one prior packet or completed-report handle. The engine
resolves that handle to one immutable, content-addressed `AnalysisState` and
imports only decisions whose narrower identities and current contracts remain
valid.

`AnalysisState` binds the exact snapshots and context, accepted observations,
consumer and impact dispositions, coverage certificates, current material
requirements, current reached obligations, reading plan, and contract
versions. Every packet and report binds its state handle. Different accepted
evidence or rationale therefore produces a different state and packet/report
identity even when the remaining work is identical.

A prior packet or report is only a deterministic reuse container. Requirement
identity remains the fact-reuse rule, and obligation identity plus its decision
fingerprint remains the disposition-reuse rule. There is no ambient
observation ledger and no second `prior_report` import path.

Trusted deterministic providers may receive a current requirement and exact
immutable inputs. They return a typed `ObservationClaim` or `NotAvailable`;
they never construct canonical observations. Analysis alone validates the
requirement, value, evidence contract, registered provider contract, and
current authorization before constructing `FactObservation`.

Unknown relationship evaluations remain pending impact references to their
requirements. They are not actionable obligations and do not independently
advertise fact-answer operations. Recording an observation reevaluates only
programs named by the applicability module's reverse dependency index.

## Contract Replacement

The superseding coordinated cutover advances:

- analysis contract 2 to 4;
- public interface 5 to 7;
- packet identity and schema 3 to 5;
- completed-report identity and schema 2 to 4;
- analysis-state identity and schema to 1; and
- applicability contract 2 to 3.

It adds `FactContract`, `AnalysisContext`, `FactRequirement`,
`FactObservation`, and typed evidence/authorization references. It removes
`ApplicabilityQuestion`, `FactAnswerSubmission`, actionable
`applicability-resolution` obligations, and fact-answer `DispositionRecord`
variants. Surviving obligation identity version 2 remains unchanged because
its representation does not change.

`AnalysisRequest.facts`, `AnalysisRequest.prior_report`, and individually
supplied observation or certificate reuse inputs are removed. One optional
`prior_analysis` packet/report handle replaces them. Router `RoutingFactSet`
inputs remain ephemeral query context and cannot enter standards-change
analysis.

Router fact authority must distinguish semantic meaning from display prompts,
so its projection schema advances and all seven facts receive reviewed
contract metadata. The empty policy-impact fact catalog adopts the accepted
serialized contract shape without inventing facts.

## Invariants

- A prompt-only or alias-only change does not change requirement identity.
- A fact semantic revision, value domain, meaning, context, answer contract,
  evidence contract, or authorization contract change does.
- An unrelated relationship change or another relationship using the same
  fact does not change requirement identity.
- A changed analysis subject or accepted/proposed semantic payload does.
- One requirement may name several dependent programs without those
  dependencies entering requirement identity.
- A fact observation from another requirement is never reused.
- A public analysis request cannot provide a raw fact value.
- One prior-analysis handle is the only caller-facing reuse input.
- One packet or report handle identifies exactly one complete analysis state.
- Different accepted evidence, authorization, or disposition rationale changes
  state and packet/report identity even when current work is unchanged.
- Only requirements material to the final fixed point block completion;
  superseded requirements remain state provenance but not current work.
- Reused observations and dispositions are revalidated against current
  evidence-provider and authorization contracts.
- A deterministic provider returns a claim; only analysis constructs an
  observation.
- A packet is stale after either bound snapshot changes, even when an
  observation remains reusable in a newly prepared packet.
- Invalid values, evidence, authorization, context kinds, duplicate
  observations, and conflicting observations reject deterministically.

## Verification

Fixtures must cover every identity stability and invalidation rule, one fact
blocking several relationships, exact reverse dependencies, observation reuse,
stale packets, schema/runtime agreement, Router parity, policy-impact behavior,
and rejection of every removed legacy shape. Broad graph, metadata,
applicability, analysis, engine, verifier, declarative, freshness, plan, link,
and complete-checkpoint verification remains required.

Coverage attestations must not be renewed until all fact-contract and other
horizon-affecting inputs are frozen. Any renewal requires fresh authorized
audit evidence over the exact resulting requirements.
