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
