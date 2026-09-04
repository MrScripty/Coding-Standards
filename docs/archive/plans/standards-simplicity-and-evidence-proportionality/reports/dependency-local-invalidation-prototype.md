# Dependency-Local Invalidation Prototype

## Decision

**Retain the current standard; preserve the bounded algebra as implementation-
design evidence.** The prototype demonstrates that this repository could
invalidate a prior policy-coverage decision from its deciding policy unit,
declared relationship membership or semantics, registered consumer, evidence
closure, and shared interpretation protocol. It also demonstrates that an
unrelated global-horizon member need not invalidate every subject.

That result does not establish a missing project-agnostic standard. The known
concrete consumer is the Coding Standards repository's Python coverage
implementation, which this plan deliberately excludes. Turning its prospective
algorithm into general normative Planning text while leaving that consumer
unchanged would confuse standards recommendations with recommendations for the
standards tooling and leave a known projection incomplete.

The prototype boundary is equally important: dependency-local invalidation
cannot discover a semantic consumer that was never declared in any authority.
Explicit consumer review, exact dispositions for declared consumers, and an
explicit reviewed-empty decision remain necessary. A local digest is not proof
that humans modeled every real consumer.

## Fresh Admission Baseline

- Repository revision: `ac418826eb98c7facd2a29ef7463dcb384df731b`.
- The worktree was clean before Milestone 0 started.
- The current policy-impact compiler reports 47 policy units, 387 direct
  relationships, and 175 supplemental consumer nodes.
- The planned inventory and visualization still match that live topology.
- Checker migration packages through `M6-I72` are `accepted`; no later package
  is admitted. Milestone 0 therefore has no active write-set collision.
- The current suite registry contains 226 suites and 246 suite-closure
  memberships.
- The generated suite-input manifest's repository-index digest is stale after
  the planning package added tracked files. Milestone 0 deliberately reads the
  captured manifest and does not rewrite shared generated authority. The first
  later slice admitted to touch generated inputs must regenerate it serially.

## Question

Can a policy/evidence decision be invalidated from its actual dependencies so
that changed or missing authority becomes stale while unrelated subjects stay
stable?

The current coverage view includes one digest over the complete horizon in
every subject. The prototype confirmed that changing one horizon member makes
all 47 current subject views different. That is safe but broader than the
decision being proved.

## Candidate Algebra

For subject `s`, define:

```text
LocalAuthority(s) = H(
  algebra-version,
  interpretation-protocol,
  policy-unit(s),
  sort(Dependency(edge) for every declared outgoing edge of s),
)

Dependency(edge) = H(
  edge natural identity and semantic fingerprint,
  registered consumer identity and content,
  registered evidence-suite dependency closure,
)
```

The components have these meanings:

- `algebra-version` changes when the meaning of the local calculation changes.
- `interpretation-protocol` contains only shared rules required to interpret
  every subject: the policy-impact authoring contract, relationship-kind
  contract version, applicability language version and fact schema, and suite-
  input contract.
- `policy-unit(s)` binds identity, owner, heading, semantic revision,
  representation digest, and structural digest for the selected subject.
- the sorted dependency set is membership authority. Adding or removing a
  declared relationship changes the owning subject even if every retained edge
  is byte-identical.
- each edge binds its typed semantics, its actual consumer, and the transitive
  suite closure that supplies its evidence. An unrelated catalog node, suite,
  or input is absent from the calculation.

A prior decision for `s` is stale exactly when `LocalAuthority(s)` differs, the
subject was added or removed, or a required dependency cannot be resolved. A
shared interpretation-protocol revision intentionally invalidates all
subjects. An ordinary dependency change invalidates every subject that names
that dependency and no others.

## Executed Cases

The executable probe is
[dependency-local-invalidation-prototype.py](dependency-local-invalidation-prototype.py).
Run it from the repository root:

```bash
python3 docs/archive/plans/standards-simplicity-and-evidence-proportionality/reports/dependency-local-invalidation-prototype.py
```

It compiles the live canonical corpus and policy-impact authority, validates
the suite definitions and captured input manifest, derives every subject's
local authority, applies mutations in memory, and exits nonzero if observed
invalidation differs from the expected exact set.

| Case | Expected result | Observed result | Outcome |
| --- | --- | --- | --- |
| Changed relationship semantics | Invalidate only `topic.dependencies.requirement-and-ownership` | 1 invalidated, 46 stable | pass |
| Removed consumer relationship | Invalidate only the relationship owner | 1 invalidated, 46 stable | pass |
| Unrelated registered-consumer content change | Invalidate exactly the sources that declare that consumer and keep the representative source current | exact dependent set invalidated; representative source stable | pass |
| Provider/interpretation revision | Invalidate every subject | 47 invalidated, 0 stable | pass |
| Current authoritative edge missing from reviewed dispositions | Block its owner's acceptance without inventing a dependency change | exact missing edge and blocked owner reported; 0 invalidated, 47 stable | pass |
| Registered consumer content change | Invalidate every source that declares that consumer | exact one-source set invalidated, 46 stable | pass |
| Evidence-suite closure change | Invalidate every source whose edge names that suite | exact one-source set invalidated, 46 stable | pass |

The representative source is selected deterministically from the live subject
with the greatest direct relationship fanout. At this baseline it is
`topic.dependencies.requirement-and-ownership`; the selected edge targets the
`a1b-public-cutover` consumer and evidence suite. The decision does not depend
on that repository-specific subject.

## Counterexamples And Limits

### Counterexample: global-horizon membership

If every subject binds one complete horizon digest, changing an unrelated suite,
artifact, plan file, or graph member changes every subject. The prototype
selected the actual `suite:acceptance-claims` member because it is outside every
current policy edge's transitive evidence closure, recomputed the changed
horizon members projection and digest, and asserted 47 of 47 current subject views
changed. The same member has zero dependency-local subjects, so all 47 renewals
are unrelated to a deciding dependency.
The renewed identities prove byte-level change, but all 47 renewals add
no subject-specific consumer decision.

### Counterexample: local relationships without their evidence closure

Hashing only the subject and edge list would leave a decision current after its
consumer contract or deciding suite changed. The candidate algebra therefore
binds registered consumer content and the evidence suite's transitive input
closure.

### Limit: never-declared semantic consumers

Neither global nor local hashing can prove the existence of a consumer absent
from the authored model. The graph compiler can reject an unknown endpoint,
relationship membership changes invalidate the owning subject, and the change
workflow can block an authoritative edge without a disposition without
pretending the graph itself changed. Semantic completeness still requires
review. The standards must not turn
dependency-local invalidation into a claim that graph closure proves real-world
completeness.

## Standards Disposition And Code Follow-Up

Retain `workflow.planning.projection-completeness` at semantic revision 1 and
retain its current `policy-semantic-impact` relationship as reviewed-no-change.
The current rule already requires authoritative consumer queries, explicit
dispositions, missing-declaration repair, and reviewed-empty authority. The N2
evidence-proportionality family separately addresses the general need to
justify the cost and marginal value of permanent evidence machinery.

A separately scoped Coding Standards Python design audit should inspect the
global horizon in `tools/standards_analysis/standards_analysis/coverage.py`, its
coverage authority, reports, attestations, and migration ownership. That work
may adopt or revise this candidate algebra if its full implementation boundary
and compatibility consequences justify the change. It must not infer that the
prototype discovers undeclared semantic consumers or encode this repository's
Python types and file formats as general standards.

The prototype therefore proves feasibility and identifies a concrete machinery
cost. It does not prove a general normative deficiency, and it authorizes no
standards or verifier change in this plan.
