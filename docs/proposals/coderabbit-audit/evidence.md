# Evidence and intent for CodeRabbit standards proposals

The user authorized drafting standards change proposals through the Coding Standards MCP and exporting their exact proposed wording to Markdown. Approval and application are outside this request.

## Explicit user constraint

The user stated: "I do not want to end up enforcing that projects try sandboxing themselves as that is not nessisary".

The accepted drafting interpretation is ordinary fixture ownership and reliable setup: targeted Git environment handling, owned-server identity, explicit readiness, platform-capable fixtures, required build setup and bounded harness observation. These are optional recipe examples. This work must not impose containers, OS sandboxes, security namespaces, blanket environment clearing, or universal separation for every test. Shared fixtures remain valid under an adequate coordination and lifecycle contract.

## Observed source records

The source is CodeRabbit_Audit_MrScripty_2026-10-04.zip. Its SHA-256 is 97658b671252aef1e1890f03567185495cb7d227827bdb9cd92cd4ba6e68115a. The audit reports 138 formal findings, including one explicit withdrawal, plus 28 separate discussion observations. These are historical records, not independently reproduced current defects.

The ZIP reports bot activity on 139 of 150 PRs but completed code review on 45. Completion covers at least one revision or bounded range; it is not evidence that the latest complete PR head was reviewed. This supports a conditional review-scope clarification, not a requirement to adopt CodeRabbit or any paid review service.

The following summaries and links are copied from the source register:

- [CR-0099](https://github.com/MrScripty/Rheon/pull/1#discussion_r4176384448): Old success text can qualify changed source and produce a receipt containing new hashes without rerunning or binding the original run.
- [CR-0118](https://github.com/MrScripty/Rheon/pull/5#discussion_r4178807108): Verifier can stamp current binary SHA onto replay results produced by a different executable.
- [CR-0124](https://github.com/MrScripty/Rheon/pull/6#discussion_r4177522364): Changes to verify_browser.py print generation/options do not invalidate retained PDF receipt.
- [CR-0103](https://github.com/MrScripty/Rheon/pull/1#pullrequestreview-5404234097): A total count can be satisfied by extra generated declarations while missing expected names; explicit membership is the stronger completeness check.
- [CR-0127](https://github.com/MrScripty/Rheon/pull/7#discussion_r4178998726): Empty receipt or empty artifact hash map bypasses loop; require exactly three fixtures and both PNG/CSV keys.
- [CR-0136](https://github.com/MrScripty/Kenoma/pull/2#discussion_r4177970532): zip truncation can hide missing/extra vertices and coordinate dimensions.
- [CR-0068](https://github.com/MrScripty/Passeur/pull/1#discussion_r4140465157): Inherited Git directory, worktree, index, or object variables can redirect temporary fixture commands into the caller's repository.
- [CR-0133](https://github.com/MrScripty/Rheon/pull/9#discussion_r4179210717): Repository-local GIT_* variables override temporary seed checkout; add/commit and inventory checks can target real invoking repo.
- [CR-0089](https://github.com/MrScripty/Commonlight/pull/2#discussion_r4170945953): An unrelated server on fixed port3100 can satisfy readiness before the owned process fails, causing browser tests to upload/delete in another store.
- [CR-0002](https://github.com/MrScripty/Pumas-Library/pull/1#discussion_r4068869103): Paused clock and a yield could fire the connect timeout before backend admission instead of testing silent generation.
- [CR-0049](https://github.com/MrScripty/Pumas-Library/pull/29#discussion_r4172281136): A fixed two-second communicate timeout could kill cold/slow fixtures before they demonstrated custody; tests should synchronize on readiness first.
- [CR-0029](https://github.com/MrScripty/Pumas-Library/pull/5#discussion_r4136464588): env_clear removed transport settings, making managed Python provisioning fail behind required proxies or custom trust gateways.
- [CR-0100](https://github.com/MrScripty/Rheon/pull/1#pullrequestreview-5404234097): Python optimization strips assert-based source/pin checks, allowing silent success.
- [CR-0112](https://github.com/MrScripty/Rheon/pull/4#discussion_r4178611352): Python -O removes equality assert; completed case can be published despite different accepted times.
- [CR-0114](https://github.com/MrScripty/Rheon/pull/4#discussion_r4178611361): Source hash, benchmark, replay manifest and byte checks use assert and can silently disappear under -O.

## Engineering inference and proposed response

Retained results need a defensible connection to their actual material producing inputs before they can qualify another acceptance decision. Complete-population checks need expected membership and cardinality rather than incidental counts, empty iterations or truncated pairwise comparisons. These are proposed clarifications of existing claim fidelity and authoritative oracle principles.

The Python examples illustrate existing mode-independent invariant enforcement. The fixture examples illustrate existing ownership, precondition and terminal-observation contracts. They create no new generic test-isolation or sandboxing obligation.

The proposals should preserve Verification's existing cost admission, construction-proof alternatives and proportionality. No universal receipt format, signing scheme, new harness, negative-control quota, fixed fixture count, platform matrix, review provider or mandatory docstring threshold is supported by these records.

## Limits and review work

The exact accepted base is dcc56f26e884ade260770beceba2501d3746200d. Current uncommitted edits are not part of this authority and must be preserved. Original standards adoption and version at the time of each report have not been established. Effectiveness improvements remain hypotheses until observed on downstream tasks.

Draft creation does not constitute material review, consumer disposition, coverage attestation or publication readiness. Candidate validation and declared-consumer review must be completed only in a later authorized review/application workflow.
