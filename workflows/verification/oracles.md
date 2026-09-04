# Independent Test Oracles

**Standards metadata**

- ID: `workflow.verification.oracles`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change creates a validator, negative fixture, property test, differential test, or other independent oracle.
- Does not apply when: Ordinary existing assertions suffice and no validation oracle, negative fixture, property, or differential mechanism changes.
- Requires: `workflow.verification`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `workflows/verification/oracles.md`

## Evidence Oracle Boundaries

For each acceptance claim, identify the observation mechanism and the exact
property it can decide. The expected property must come from authority
independent of the subject under test. Two projections that share one semantic
implementation can prove agreement with each other, but not conformance to an
external contract.

Keep these evidence boundaries explicit:

- deterministic generation proves freshness from the selected source, not
  semantic completeness;
- an exact literal proves literal identity only when literal identity is the
  contract;
- coordinated edits to a subject and a copied expectation do not provide an
  independent oracle; and
- mutation evidence proves detection of the sampled mutations, not complete
  detection outside the sampled domain.

When the required claim has no independent or otherwise authoritative oracle,
return `unavailable`. When the mechanism cannot decide the claimed property,
the evidence is `invalid`. Do not upgrade local agreement, freshness, parsing,
snapshot equality, or a passing harness into a stronger conformance claim.
## Negative Fixture Isolation

A negative fixture proves its intended failure only when every unrelated
precondition is valid and the observed result identifies the expected
diagnostic or failure point. Record the expected typed diagnostic and the
relevant complete message or structured fields when those details distinguish
the target failure from earlier validation failures.

Construct the fixture from a valid case by changing only the condition under
test where practical. A nonzero exit, thrown exception, generic rejection, or
substring match is insufficient when several validators can reject the same
input. If the fixture cannot reach the intended boundary, classify the
evidence as `invalid`; do not count incidental failure as acceptance.
## Property And Differential Evidence

Property, generative, mutation, and differential evidence must name:

- the property being tested;
- the generated or sampled input domain;
- the independent or authoritative oracle;
- the compared implementations or projections;
- reproducibility and shrinking behavior where applicable; and
- the unsupported or unexamined domain.

Comparison between local implementations proves consistency only unless an
independent authority establishes expected semantics. External conformance
claims require the selected specification, reference implementation, official
corpus, or another authority that is independent of the implementations being
compared. A sampled counterexample can disprove a universal claim; absence of
one does not prove completeness beyond the declared domain.

Return `unsupported` when the selected oracle or corpus does not cover a
well-formed required domain and `unavailable` when required authority or
reproducibility inputs cannot be obtained. Do not silently narrow the claim to
the cases a generator or local comparator happens to support.
