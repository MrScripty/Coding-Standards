# CodeRabbit audit: draft standards change proposals

Prepared 2026-10-04 from `CodeRabbit_Audit_MrScripty_2026-10-04.zip` using
the Coding Standards MCP. Accepted base:
`dcc56f26e884ade260770beceba2501d3746200d`.

This is a review copy. Standards have not been applied or changed. Proposals
2 and 3 are saved MCP drafts; proposal 1's complete wording is provided but
its MCP submissions were rejected before draft creation.

| Proposal | Intended change | MCP status |
| --- | --- | --- |
| 1 | Retained evidence identity and complete inventories | Rejected: evidence digest mismatch; no saved handle |
| 2 | Optional test fixture and Python gate examples | Saved; needs action |
| 3 | Scope and completion of reviews selected as gates | Saved; needs action |

The fixture examples expressly impose no project sandboxing requirement.
They describe ordinary setup, readiness and resource coordination, permit
adequate shared fixtures, and preserve required proxy and TLS settings.

These are narrowly scoped opportunities from historical findings. Most findings
already map to existing standards; this draft does not duplicate every finding
as a new rule. The archive does not establish which standards version each
project had adopted, and these findings were not independently reproduced.
No fixed docstring threshold, universal harness, receipt system, signing scheme,
review provider or platform matrix is proposed.

The draft starts from accepted MCP authority. Existing uncommitted work in the
repository is outside that base and will need reconciliation before any future
application. [Evidence and user constraints](evidence.md) are recorded separately.
Full requests and MCP outcomes are retained alongside this Markdown copy.

---

# Proposal 1: Retained evidence identity and complete inventories

Status: wording drafted; MCP submission rejected before a proposal was created.
The returned code was `ANALYSIS.EVIDENCE_DIGEST_MISMATCH`: “Resolved evidence
bytes do not match the declared digest.” Both the original owner placement and
an alternate placement wholly within Verification received this rejection. No
proposal or revision handle was returned. The exact cause remains unconfirmed.

The purpose evidence file's declared digest matches its current bytes, and the
same evidence reference was accepted for proposals 2 and 3. This does not prove
that the Engine's other retained evidence bindings are valid. Repairing or
retiring existing certificates is outside this drafting request.

## Purpose and effect

Clarify two recurring applications of Verification's existing evidence rules.
A saved success result must identify the source and material producing context
it actually observed before it qualifies a current claim. A completeness check
must establish the expected population and compare its required members.

Examples from the audit include stamping the current executable hash onto an
older replay result, accepting the right total count with the wrong members,
and allowing an empty loop or truncated pairwise comparison to report success.
Protected repository-state checks must observe the particular state they claim
to protect, including their own output writes when relevant.

These conditions follow the selected claim. They do not require a universal
receipt system, hash inventory, fixed fixture count, permanent scanner or
project sandbox. Existing construction proofs and proportionate reruns remain
valid.

Evidence: CR-0099, CR-0118, CR-0124, CR-0103, CR-0127 and CR-0136;
see [the source record and limits](evidence.md).

## Proposed edits and placement

The intended original placement is retained below:

- Add `Retained Evidence Identity` under `Coverage And Durable Evidence Records`
  in `workflow.verification`.
- Add `Complete Inventory Evidence` as a section of
  `workflow.verification.oracles`, before `Negative Fixture Isolation`.
- Register `workflow.verification.retained-evidence-identity` and
  `workflow.verification.inventory-completeness` as separate policy scopes at
  semantic revision 1, with supporting provenance.
- Preserve the existing registered scopes and their semantic revisions.

The rejected requests are preserved in
[the original request](01-evidence-request.json) and
[the alternate request](01-evidence-revised-request.json). They are draft
requests, not applied edits.

## Exact proposed wording

The following text is from the submitted draft request. There is no saved MCP
candidate available to read back for this proposal.

### Retained Evidence Identity

When a retained result is used to satisfy a current acceptance claim, establish
which material source, inputs, producer, configuration, and environment produced
that result. Select those facts from what can change the claimed property;
unrelated environment details do not become required evidence.

Bind the result to those facts when it is produced, or establish the connection
from authoritative retained records. Compare that producing context with the
current claim before reusing the result. Hashes computed from the current
checkout, executable, renderer, or input do not establish what produced an
earlier result. Reconcile reported measurements and aggregates with their
authoritative observations when the claim depends on them.

Keep historical qualification scoped to its original source and procedure.
Rerun the affected evidence when material producing facts changed or cannot be
established. Missing required identity or observations leaves the current claim
`unavailable`; contradictory identity or an unsupported inference is `invalid`.

Use existing records, an adequate construction guarantee, or a proportionate
rerun when they establish the connection. This rule does not require a new
receipt system, universal hash inventory, byte identity, signing, or a fixed
record format. Apply the existing evidence-machinery admission criteria before
introducing a permanent mechanism.

## Complete Inventory Evidence

When a validator claims that a population is complete, that protected state is
unchanged, or that every corresponding value was compared, establish the
expected members, cardinality, identity rules, and observation boundary from
the claim's independent or authoritative contract. Deriving the expected
population from only the observed output cannot establish completeness.

Compare every required member and relation. Reject missing or unexpected
members, forbidden duplicates, mismatched cardinality, and empty populations
when the contract requires members. Counts, empty iterations, and comparisons
that truncate to the shorter input cannot establish exact membership or a
complete pairwise comparison. An empty population is valid when the owning
contract permits it.

For a protected filesystem or repository-state claim, observe every relevant
state selected by that claim. Tracked worktree content, staged content, untracked
content, and ignored content are distinct possible inputs; a tracked diff does
not prove that all are unchanged. Include only the paths and state the claim
actually protects, rather than expanding to a repository-wide inventory by
default.

Account for relevant effects of the observation and result-publication procedure.
A result claiming protected state remains unchanged must still be true after
that procedure's own writes. Select a safe output location or establish the
postcondition according to the owned mutation contract.

Use an adequate construction guarantee or the smallest complete observation
that establishes the property. Missing expected-population or observation facts
is `unavailable`; incomplete comparison or contradictory membership is
`invalid`. This rule selects no fixed fixture count, inventory format, permanent
scanner, or requirement to sandbox a project.

## Review considerations

Review the existing Verification consumers against these new scopes and
establish their actual operational impact. Exercise representative stale-result,
missing-member, permitted-empty, and protected-state cases if this proposal
proceeds. The historical findings were not reproduced in this drafting work.

---

# Proposal 2: Optional test fixture and Python gate recipes

Status: saved through the Coding Standards MCP; `needs-action`, unreviewed and
unapplied.

## Purpose and effect

Provide optional examples for Git fixture setup, owned server readiness,
explicit test synchronization, watchdogs, platform-capable fixtures, build and
async prerequisites, and Python checks whose supported execution includes
optimization. The examples illustrate existing obligations rather than creating
new acceptance gates.

Fixture ownership means knowing which resource a test observes and coordinating
its lifecycle. The text explicitly excludes requirements for project sandboxing,
containers, security namespaces, blanket environment clearing, or a separate
resource for every test. Shared fixtures remain suitable when their setup,
coordination and cleanup satisfy the selected claim.

Evidence: CR-0002, CR-0049, CR-0068, CR-0089, CR-0133 and CR-0029;
Python examples: CR-0100, CR-0112 and CR-0114.
See [the source record and limits](evidence.md).

## Proposed edits

Create `reference.recipes.verification` at reference authority, requiring the
existing Verification, Concurrency, Contracts and Cross-Platform owners. Add
supporting provenance. The recipes select no framework, isolation policy,
platform matrix, optimization-support requirement or universal assertion ban.

## MCP candidate content

The following complete new module was read back from the immutable proposal
revision through `query_proposal`. Relative links are adjusted for this review
copy's location; the proposed wording is unchanged.

# Test Fixture And Gate Recipes

**Standards metadata**

- ID: `reference.recipes.verification`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A project has selected a verification claim and fixture or gate procedure and wants optional examples for ownership, readiness, platform setup or supported Python execution modes.
- Does not apply when: The project is selecting acceptance, threat boundaries, mandatory test isolation, supported targets, enforcement policy or a test framework.
- Requires: `topic.concurrency`, `topic.contracts`, `topic.cross-platform`, `workflow.verification`
- Specializes: `none`
- Verification: Reference authority, owner links and example correctness checks; examples supply no acceptance or security certification.
- Canonical owner: `reference/recipes/verification.md`

This reference contains optional examples for a test procedure whose claim,
fixture lifecycle, supported environment, and tool authority have already been
selected. [Verification](../../../workflows/verification.md) owns the claim and
observation. [Concurrency](../../../topics/concurrency.md) owns work and shared
resource coordination. [Contracts](../../../topics/contracts.md) owns invariant
enforcement, and [Cross-Platform](../../../topics/cross-platform.md) owns target
capability. The examples add no obligations and select no test framework.

Here, fixture ownership means that a test targets the resource it intends to
observe and owns or coordinates its lifecycle. It does not mean that the project
must sandbox itself. Containers, operating-system sandboxes, security namespaces,
blanket environment clearing, and a separate resource for every test are not
requirements of these recipes. A shared fixture is suitable when its initial
state, coordination, and cleanup satisfy the selected claim.

## Git Fixture Setup

For a test that creates a temporary Git repository, select the subprocess
environment so repository-local settings cannot redirect commands into the
invoking repository. A Git implementation that supports listing its local
environment variables can identify those settings through
`git rev-parse --local-env-vars`. Construct a child environment, omit the selected
repository-local overrides, and explicitly target the fixture directory.

Potential overrides include `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, and object
directory settings. The list is illustrative, not an exhaustive hard-coded
contract. Establish fixture repository identity before mutation. When needed,
exercise the helper with an inherited override and observe that the fixture is
changed while the invoking repository remains unchanged.

Retain declared transport capability such as proxy and TLS trust settings when
the fixture needs it. Selecting relevant variables avoids erasing necessary
capability through blanket environment clearing. The example creates no security
sandbox or protection claim against hostile test code.

## Owned Server Readiness

For a test that starts a server, allocate an endpoint according to the server
and harness contract and retain the started process's completion capability.
When another process can answer at that endpoint, distinguish the owned instance
through an instance-specific readiness response, startup channel, or another
observation the real server supports. A responding fixed port alone may belong
to another service.

Begin browser or client actions after the owned instance is ready. Observe
startup failure and reap owned child work at the selected teardown boundary.
Select one mechanism that proves the needed identity and lifecycle; the example
does not require adding a token protocol to every server or killing unrelated
processes occupying a port.

## Explicit Readiness And Harness Bounds

A cancellation test can wait for an admission event, worker marker, or another
owned state transition before pausing a controllable clock or requesting
cancellation. Select the signal that establishes the state under test. A sleep
or scheduler yield does not alone prove admission, active work, or custody.

Keep a watchdog that diagnoses a stalled test separate from the signal that
releases a test-controlled worker and from production deadlines. Select its bound
from the harness and execution environment. On expiry, retain the failure and
perform owned cleanup; do not turn expiry into the successful worker release or
silently change the production transfer contract.

## Platform Fixtures And Execution Prerequisites

Construct executable fixtures for the actual target. A shell script renamed
`python.exe` does not provide a Windows executable. Observe selected capabilities
such as symlink creation before relying on their fixtures. If a required target
claim cannot be observed, retain it as unavailable even when a runner permits
skipping an unsupported fixture.

Establish required built artifacts before tests launch them. A no-emit type check
does not create a CLI executable. Await asynchronous actions and lookups through
the result the test intends to assert, and preserve each required command's
failure when orchestrating multiple checks. These examples select neither a
universal build command nor a platform matrix.

## Python Gate Checks Under Optimization

For a Python gate that owns a mandatory source-identity check, an explicit
failure path can preserve the check under supported optimized execution:

```python
def check_source_identity(expected_source, observed_source):
    if observed_source != expected_source:
        raise ValueError("source identity mismatch")
```

The caller obtains the expected identity from its authoritative contract and
the observed identity from the subject. The names, exception, and identity
representation are illustrative. Use the owning gate's actual failure contract.

Python `assert` statements may be removed under `-O` or `PYTHONOPTIMIZE`; they do
not enforce a mandatory gate whose supported execution includes that mode.
For such a gate, a focused negative case can present a mismatched identity under
normal and optimized execution and observe the intended failure in each.
Successful execution of an unrelated command is not that observation.

Ordinary test assertions remain suitable when their runner's execution contract
preserves them. This example adds neither a universal assertion ban nor a
requirement to support optimized execution for every Python tool.

## MCP record and outstanding work

- Proposal: `proposal:v1:b969a125-e30d-4e68-8393-d598b975c9b5`.
- Revision: `proposal-revision:sha256:7bc099b4433ee5e68fbb43d83f5e3f22d0757362553d8b14732ab6341bc5c3f5`.
- Analysis: `analysis:sha256:b1b7d79edfcd28f64f2d03bb7610095af4ea5243c69be993add403c61f551bb5`.
- Current analysis reports 1 pending provenance impact review.
- Application exposure: `unreviewed`.

These handles identify the saved draft. No review decision or publication
authorization is supplied by this document. Before publication, review the
example correctness, discoverability and material effect on adopting tasks;
complete the Engine's required checks and review workflow.

[Submitted request](02-fixture-recipes-request.json) ·
[MCP result](02-fixture-recipes-result.json).

---

# Proposal 3: Scope and completion of reviews used as gates

Status: saved through the Coding Standards MCP; `needs-action`, unreviewed and
unapplied.

## Purpose and effect

When a project chooses a review as a gate, distinguish completed review of an
identified source and scope from bot activity, command acknowledgements,
skipped review or an empty finding list. Preserve source mapping when carrying
a review into acceptance of a later revision.

The archive records bot activity on 139 of 150 PRs and completed code review on
45. A completed review may cover only one historical revision or bounded
range. These records support conditional scope guidance, not a requirement to
adopt CodeRabbit, a paid service or review on every edit.

Use the existing review artifact when it supplies the necessary facts. No
separate receipt format or universal full-file review requirement is introduced.

Evidence: [the ZIP coverage summary and source record](evidence.md).

## Proposed edits and placement

Add `Review Evidence Scope` to `workflow.tooling`, immediately before
`Tool-Debt Governance`. Register `workflow.tooling.review-evidence-scope` at
semantic revision 1 and add supporting provenance. Preserve the existing
Tool-Debt Governance policy and its semantic revision.

## Exact proposed wording

The following new section was read back from the immutable MCP candidate.
The submitted request includes the complete unchanged surrounding module.

## Review Evidence Scope

When a project relies on a human or automated review to satisfy a named gate,
establish the review's completion, exact source revision or range, examined
scope, and material exclusions. Use the existing review artifact when it supplies
those facts; a separate receipt is not required.

Before carrying that review into acceptance of another source revision, establish
how the reviewed source maps to the accepted source and which material changes
remain unreviewed. Review-only slices may contribute coverage when their source
mapping and examined scope establish the selected claim. Derive required
coverage and exclusions from that claim and the project's review authority.

Bot presence, summaries, command acknowledgements, skip notices, and an empty
finding list do not independently prove completed review of the required scope.
Thread resolution records discussion state; remediation acceptance requires the
evidence selected for the affected behavior.

Missing required completion or scope facts leaves the review claim `unavailable`;
contradictory scope or a false completion claim is `invalid`. Continue independent
checks while retaining any unsatisfied required review claim.

This rule applies only to a review the project has selected as a gate. It does
not require a provider, paid service, review on every edit, full-file coverage,
or treating every exclusion as a defect.

## MCP record and outstanding work

- Proposal: `proposal:v1:21e52eda-e849-4843-b2d5-f5d2a384e889`.
- Revision: `proposal-revision:sha256:2b0e0698fc06f3f73f1b0ddbe1ecb823fa4a519060a8a232c0847dd8aaccba27`.
- Analysis: `analysis:sha256:d71f07942517e0a99268717f52a9717ee103659a1d445e722eb6bdd8ffd4bdac`.
- Current analysis reports 5 pending obligations: consumer review for Rust
  tooling, TypeScript and the tooling recipes; coverage review for the new
  policy scope; and provenance impact review.
- Application exposure: `needs-review`.

These handles identify the saved draft. Complete the Engine's consumer,
coverage and material review before any later authorized application.
Historical review coverage was not revalidated against live PRs in this work.

[Submitted request](03-review-scope-request.json) ·
[MCP result](03-review-scope-result.json).
