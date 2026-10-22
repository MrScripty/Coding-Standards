# Independent Rust correction and application-exposure review

Reviewed on 2026-10-04 by the separate review agent `exposure_material_review`.
The reviewer did not author the candidate, record Engine review decisions, edit
standards, or publish exposure. The earlier
[independent review](independent-review.md) remains frozen at SHA-256
`a1d55ca293cced29591c41866bec5c5f1f898413cae51ee1634b500075f92603`.

## Exact reviewed subject and decision

- Proposal: `proposal:v1:800744d7-33d1-4b31-9a8e-bd66d2c9d3db`.
- Immutable candidate revision:
  `proposal-revision:sha256:9f0a8a377542d5372bf2c3db613a5c511693ca271e70c5b784e8290af5e14aa6`.
- Accepted source underlying the original material:
  `dcc56f26e884ade260770beceba2501d3746200d`.
- New policy scope: `profile.language.rust.baseline`, semantic revision 1,
  heading chain `Baseline Rust Change` in `profile.language.rust`.
- New direct consumer: `profile.language.rust.tooling`.
- New justification: `provenance.rust-baseline.evidence-sufficiency-2026-10-04`.
- Authorization supplied to the reviewer: the user has approved the exact
  sufficient-evidence correction and qualification of the four Rust exposures.

**Accept the material in this exact candidate for all 32 proposed application
exposures.** The authorized correction resolves the earlier Rust blocker without
weakening evidence sufficiency or adding a new generic principle. The remaining
31 module texts are unchanged. The four Rust targets now have a coherent required
reading path. No further specialist text changes are needed for this correction.

This is independent material acceptance, not a verification pass, application
preview result, Engine readiness decision, coverage certificate, or publication.
Those workflow results remain the publication owner's responsibility.

## Independent exact-candidate checks

The reviewer used the standards-engine authoring MCP, retaining exact snapshot
and proposal handles. All ten specialist profiles were read in full from
accepted snapshot `snapshot:v1:d8c60c31-5617-4eb1-bc7f-3954b793c33b`, then reread
at the candidate revision above. No specialist content, required dependency,
or specialization list changed.

All 32 proposed targets were independently reread at that revision. Thirty-one
matched the captured accepted text exactly. For the Rust base, the reviewer
constructed the expected text by replacing only the approved step 2 in the
captured accepted text; the candidate matched that expected text exactly.
All 32 preserved their required dependencies and specialization lists and
reported candidate exposure `current`.

The six additional required owners were also independently reread: `core`,
`workflow.verification`, `workflow.implementation`, `workflow.tooling`,
`topic.concurrency`, and `topic.security`. Each remained textually unchanged,
preserved its relationships, and reported current candidate qualification.
Their dependencies close within that set and the selected targets.

The reviewer read the actual candidate baseline unit, its impact relationships,
its decision-provenance relationship, and the provenance record through the MCP:

- The policy read resolves to exactly `Baseline Rust Change`, including the six
  baseline steps and the existing feature-configuration guidance.
- Its `policy-impact` read reports exactly one declared consumer edge, to Rust
  Tooling. No ten-profile blanket semantic relationship was added.
- Its decision-provenance read reports exactly the new justification record.
- The provenance record reports `current`, is bound to this policy subject,
  labels its origin `current-justification`, and states that historical original
  motives are unknown.
- Coverage reports subject `profile.language.rust.baseline`, requirement
  `sha256:4ce10ebc3bd0c5978b93fb7ce06d4afaa977588521cb50d76c8b8152756d4db4`,
  status `review-required`. Material acceptance does not misreport that pending
  status as an issued certificate.

The request and candidate agree on registration at semantic revision 1: there
was no earlier registered identity for this scope. Only the affected baseline
is newly registered. Unchanged Rust invariants and routing are not newly
represented as audited policy units.

## Normative correction assessment

The exact corrected instruction is:

> Establish the changed claim with adequate existing evidence or a construction
> guarantee, or add a focused Rust regression test when needed.

Core and Verification already make the deciding obligation adequate evidence
for the changed property. They permit an existing test or a construction proof
when it establishes that property. The former Rust instruction demanded a new
focused test irrespective of sufficiency, even though the profile says it owns
Rust mechanisms while generic owners retain cross-language policy.

The correction restores that authority boundary. Reuse or construction is valid
only when it establishes the changed claim; it is not permission to accept an
unexamined behavior or omit an independently required boundary observation.
A focused Rust regression test is still required when needed to establish the
claim. Existing Rust execution and scope instructions, configured Clippy checks,
feature contracts, and selected specialist claims remain in force. No blanket
verification bypass, new test harness, sandbox, isolation mechanism, or copied
identity/inventory rule is introduced.

The wording is general enough to allow the appropriate decision while retaining
the principle that acceptance follows adequate evidence. It resolves the exact
earlier blocker rather than using qualification to waive an unchanged defect.

## Complete bounded consumer inventory

The review horizon is the affected baseline's normative projections into the
ten canonical Rust specialist profiles dispatched by the base profile. The
reviewer inspected every whole specialist module and distinguished an actual
projection of this baseline from a prerequisite, specialization label, shared
generic principle, or projection of another Rust invariant.

**Within that bounded specialist population the inventory is complete:** Rust
Tooling is the single direct semantic consumer of the baseline scope. All ten
have explicit dispositions below. There are no undispositioned profiles in
that population. Existing `Requires` and `Specializes` relationships remain
appropriate and are not converted mechanically into semantic impact edges.

This is not a claim that a lexical search, an empty previous graph, or the new
single edge proves whole-repository semantic completeness. New evidence of an
additional actual baseline projection must expand the inventory and obtain its
disposition. The broader Library evidence-policy follow-up is identified below.

| Specialist | Baseline consumer disposition | Material reasoning and required action |
| --- | --- | --- |
| `profile.language.rust.tooling` | Direct consumer; accept unchanged | `Practical Starting Point` translates ordinary Rust changes into owning-crate/workspace formatting, checking, focused test selection, and repository Clippy execution. `Cargo Baseline Command Mechanisms` expresses accepted formatting/lint/build/test claims with only required packages, targets, features, and environments. `Mechanism Authority` leaves evidence sufficiency with generic owners. Those mechanisms project the baseline's execution and scope obligations without demanding a new test. The corrected exception is already coherent with this body; no text change is needed. |
| `profile.language.rust.api` | No direct baseline projection found; preserve prerequisites | This profile expresses accepted API, validated-type, conversion, feature, and Rustdoc contracts. Its evidence claims and construction mechanisms follow Contracts, Documentation, and Verification. It does not restate or implement the local-bug baseline's test-addition or command sequence. No correction is needed. |
| `profile.language.rust.async` | No direct baseline projection found; preserve prerequisites | Its execution, task, cancellation, shutdown, guard, and cleanup requirements specialize Concurrency and async lifecycle contracts. Its verification list covers those selected lifecycle properties, rather than copying a universal local-bug evidence recipe. The exception cannot waive those claims. No correction is needed. |
| `profile.language.rust.security` | No direct baseline projection found; preserve prerequisites | Filesystem authority, recoverable outcomes, sizing, queue, and listener mechanisms specialize Security and other selected owners. Verification covers applicable boundary properties; already-proven validated state has its own applicability exception. It does not impose a new-test policy independent of those claims. No correction is needed. |
| `profile.language.rust.cross-platform` | No direct baseline projection found; preserve prerequisites | Targets, capabilities, feature/consumer configurations, and evidence fidelity come from Cross-Platform, Dependencies, Contracts, and Verification. Compilation, linking, packaging, integration, and real-target observations remain distinct. Similar feature language does not transfer authority from those owners to the local-bug baseline. No correction is needed. |
| `profile.language.rust.dependencies` | No direct baseline projection found; preserve prerequisites | Cargo declarations, feature expressions, graph views, audits, and build-cost mechanisms project generic dependency and measurement contracts. Its evidence obligations are claim-matched and do not implement the baseline's formatting/test sequence. No correction is needed. |
| `profile.language.rust.release` | No direct baseline projection found; preserve prerequisites | Toolchain, publication, package metadata, release adapters, and release evidence follow accepted Release and Verification claims. It explicitly denies a fixed command set before every release. The local-bug correction does not waive artifact evidence or create release authority. No correction is needed. |
| `profile.language.rust.unsafe` | No direct baseline projection found; preserve prerequisites | It specializes the separate unsafe invariant: denial by default, justified relaxation, operation proof, caller contracts, and mechanism-selected evidence. Those are not projections of the registered baseline scope. Real unsafe-path and required-environment claims remain required; the correction does not substitute an unrelated safe-path test. No correction is needed. |
| `profile.language.rust.interop` | No direct baseline projection found; preserve prerequisites | Foreign dimensions, raw memory, provider lifetime, and callback proof specialize Interop and unsafe authority. Its applicable boundary cases and mechanism-appropriate diagnostics are distinct from adding a new local regression test by default. No correction is needed. |
| `profile.language.rust.language-bindings` | No direct baseline projection found; preserve prerequisites | Core/adapter ownership, conversion, serialization, callbacks, runtime adaptation, and native/host evidence follow binding contracts. Package placement and feature wording preserve architecture and consumer authority. Native-only evidence cannot replace required host proof; the correction does not authorize that substitution. No correction is needed. |

The candidate's single relationship is therefore appropriate:

- source: `profile.language.rust.baseline`;
- consumer: `profile.language.rust.tooling`, whole-artifact consumer scope;
- relation: `normative-consumer`;
- evidence owner: `review:consumer`;
- meaning: Rust Tooling projects claim-scoped Rust baseline verification and
  execution into Cargo adapters, preserving sufficient-evidence reuse or
  construction and selected scope, without creating a mandatory new-test or
  universal command obligation.

The submitted `always` applicability means that this declared consumer preserves
the source policy whenever consumed; it does not make every Rust Tooling feature
applicable to every source change. The candidate related read displays
applicability as unknown rather than evaluating a routing scenario, so this
review does not treat that display as an independent applicability decision.

## Provenance assessment

The current-justification record accurately distinguishes this review finding,
user-approved correction, and unknown historical origin. Its exact evidence
references identify the captured source material and proposed correction. Its
assumption leaves generic sufficiency with Core and Verification. Its limits
exclude downstream effectiveness claims and new audit authority over other Rust
sections. Alternatives and reconsideration conditions are relevant to the
decision and do not become application requirements.

The record is correctly associated with the policy unit rather than exposed as
additional normative steps. Qualification must preserve the separation between
normative guidance, optional references, and maintenance decision provenance.

## Application material dispositions

| Newly restored target | Disposition at this revision |
| --- | --- |
| `profile.language.rust` | Accept the whole corrected module for application exposure. The only source change is the authorized adequate-evidence exception. |
| `profile.language.rust.async` | Accept unchanged. Its required Rust base now has a coherent reviewed disposition, and its distinct lifecycle claims remain intact. |
| `profile.language.rust.api` | Accept unchanged. Its required Rust base now preserves generic evidence authority, and its existing contract-expression guidance remains intact. |
| `profile.language.rust.security` | Accept unchanged. Its required Rust base now preserves sufficiency without weakening boundary, sizing, resource, or shutdown obligations. |

For the other 28 targets, the per-target material reasoning in the frozen
[independent review](independent-review.md) is reaffirmed for the exact new
revision on the basis of fresh identical-text, relationship, and exposure
readback. That includes keeping `reference.recipes.tooling` optional/contextual,
not a normative prerequisite. Together, those 28 and the four rows above supply
an explicit material acceptance for the full 32-target qualification.

The seven other Rust specialist modules read for consumer review remain
unreviewed for application exposure. Reviewing their semantic coherence for this
baseline change does not qualify their whole application reading paths.
`workflow.standards-authoring` remains intentionally authoring-only.

## Retained follow-up and limits

- The Library profile's existing “local deterministic behavior requires focused
  regression tests” wording remains an out-of-scope evidence-policy follow-up.
  It projects generic library evidence policy rather than this Rust baseline;
  registering a Rust baseline-to-Library edge would misstate authority. This
  correction neither changes nor qualifies that module. Review the actual
  generic evidence-policy family if that follow-up is pursued.
- The earlier optional generality concerns, including Concurrency's fixture
  serialization restriction and GUI ambient-environment wording, are unchanged.
  No project-sandboxing requirement is added.
- The consumer completeness claim is bounded to the ten reviewed Rust
  specialists and the changed baseline projection. It does not certify every
  corpus section, historical artifact, agent prompt, or unregistered consumer.
- The new baseline unit's coverage requirement remains review-required at the
  observed candidate read. The Engine must resolve and publish the appropriate
  evidence-backed coverage decision; this record supplies review evidence, not
  a substitute certificate.
- No live CodeRabbit defect reproduction, downstream effectiveness experiment,
  runtime/platform execution, or entire-repository code audit was performed.
- Exact candidate application reads/routes/graph filtering, the complete
  checkpoint, review readiness, authorized application, and accepted authoring
  and application readback remain necessary before reporting publication.
- Existing unpublished work remains outside this review's mutation authority.
  The reviewer has written only this new record; the earlier report is frozen.

## Evidence artifacts

| Artifact | SHA-256 |
| --- | --- |
| `independent-review.md` | `a1d55ca293cced29591c41866bec5c5f1f898413cae51ee1634b500075f92603` |
| `accepted-material.json` | `7194e856fdec0132e1b445ceca4b5b7b4867d326f05ff666db8875b5b294560b` |
| `rust-baseline-correction.md` | `08db5233b372b365ddcff35bf909da4ddcec826bb085f6e4ddefe5b04ec572e9` |
| `rust-qualified-request-final.json` | `275184011302acd81804df25b9ed40975b6225457c4147796b57ca715d39b449` |
| `rust-qualified-result-final.json` | `a410be3d6f8754ff68745af24924388251122941cfd15d869ada487c9b7c610c` |
