# Verification: Proposal Consumer Registration And Candidate Application Preview

**Status:** Source implementation complete; local verification recorded below. Supported-deployment and user-proposal qualification remain external.

**Source baseline:** `9091bc72ac146b47d613b1836fbd8a89bd46f9ba` on `implementation/purpose-separated-standards-engine`.

**Current contract:** Engine interface **34**. Analysis request/result, Snapshot, proposal, readiness and SQLite contract versions retain their existing meaning. No store reset, conversion or compatibility adapter was added.

## Scope and source recovery

The source was recovered as the exact complete Git bundle from the repository's existing Actions artifact `engine-source-9091bc72ac146b47d613b1836fbd8a89bd46f9ba` (run 36082647857, artifact 10843096021). The artifact SHA-256 matched `3bec00071ddef6113c4b91d6185662afb6f57fc2bd9bfdc38c33c351178a458e`. All source and functional tests used the complete repository, rather than the partial source recovery available for earlier fixes.

The implementation used a separate local branch and disposable Git/SQLite repositories. The user's installed MCP, original store, pending proposal and reviewed content were not accessed. No remote push or publication to the user's repository occurred; synthetic publication stayed isolated.

## Implemented outcome

`register-consumer` is a typed logical edit in the existing `StandardsChangeSet`. It admits an explicit canonical identity, original tracked repository path, supported artifact kind and evidence/projection authority. The Engine reads the selected file at the proposal's exact original revision and privately retains its bytes in the content-addressed logical revision. Public requests supply intent, not captured bytes. The compiler can therefore resolve new consumers and draft-only policy units in one candidate, including policies introduced in an earlier draft. Cold replay uses retained original material, not a current working-tree file.

Registration updates the existing node-catalog owner. Relationships remain explicit, and coverage and review remain independent obligations. Publication compares against the original retained consumer material: registering a fixture does not rewrite its source. Existing aliases, identities, scope validation and atomic publication mechanisms remain in place.

Registered Markdown documentation, including `.agents/...` skill references, now participates in the existing operational-guidance read/revise/review path. Fixture and implementation consumers do not acquire arbitrary source-code write authority. Documentation remains outside application delivery until explicitly qualified.

`preview_application` is an authoring-only read operation for an exact proposal revision. Its read, route and related variants use the same `ApplicationView` as published application reading. Candidate envelopes and continuations retain proposal identity and contain no fabricated published snapshot handles. Exposure and prerequisite checks remain effective; a preview supplies no approval, readiness, certification or publication.

MCP discovery reports interface 34 and the configured purpose. The normal application catalog remains published-only. This is explicit process-version visibility, not hot reload. General workflow-response pagination/compaction is not part of this patch.

## Deciding evidence

The new regression suite exercises actual metadata, graph and logical-compiler implementations. It covers draft-only scopes, same-candidate registration, registration after a previous draft introduced the policy, two actual tracked fixture paths, a hidden-directory Markdown document, duplicate identities and paths, captured-source binding, failure without mutation, full/incremental equality, unreviewed documentation, and absence of automatic coverage certification.

Application-view tests compare candidate and published semantic fields, routing questions, required reading paths and relationship results. They assert candidate-only continuations, no snapshot-child handles, exclusion of provenance/fixture data, and rejection of unreviewed or stale required material.

The real-process publication test uses JSON-RPC over actual MCP stdio subprocesses, Git and SQLite. Every call starts a fresh server process. The procedure initializes the catalog, creates a coordinated proposal, registers consumers and policy links, reads revised authoring documentation, previews the candidate, rejects the same operation through the application interface, records explicit synthetic review decisions, runs preflight, applies atomically in a disposable repository, and reads the published result back. It also exercises failed duplicate registration and working-tree drift both before source capture and after capture. Fixture bytes remain unchanged; only explicitly revised documentation changes. The old preview remains bound to its original revision after publication.

The protocol client is a small standard-library test using the repository's declared wire shape. It invokes the actual server rather than mocking the transport. It does not claim official-SDK, Codex-installed-client or user-store qualification.

## Test results

| Evidence | Observed result |
| --- | --- |
| Pre-change baseline registration/purpose checks | 22 passed |
| New pre-change regression observations | Unsupported consumer registration and missing candidate-preview capability reproduced |
| New registration/preview and MCP transport tests, final targeted run | 28 passed |
| Final cold-process MCP publication walkthrough | 1 passed; 168.030 seconds |
| Metadata package | 43 passed |
| Policy-impact package | 10 passed |
| Contract package | 52 run; successful with one existing interpreter-dependent skip |
| Analysis package | 114 passed |
| Verifier package after regenerating affected inputs | 168 passed |
| Broad Engine package and final affected reruns | See final execution reconciliation below |
| Complete structural checkpoint | 73 suites and 121 checks passed |
| Canonical contract projection freshness | Passed |
| Python syntax and exact diff whitespace | Passed |
| Actual baseline capture reconstructed by the new compiler | Passed; 440 original captured files |
| Unchanged real content inventory | 113 files unchanged, including all 70 canonical modules |
| Patch round trip, file checksums and archive CRC | Recorded in package verification metadata |

### Execution reconciliation

A broad package run overlapped late test/documentation and verification-input changes. Its initial verifier checkpoint and two Engine publication cases observed a stale generated verification-input manifest. Regenerating through the owning Engine operation restored the verifier package and the two real publication checks. The run also found one mock projection in `test_analysis.py` missing the new `captured_consumer_files` field; the fixture was updated to represent the actual typed projection. Production code did not receive a mock-specific fallback.

The complete run, its failures and the final affected reruns are retained separately. A repaired case is not relabeled as having passed in the earlier run. Final execution counts and any remaining failures are recorded below before delivery.

The broad Engine run completed **307 tests in 1060.417 seconds**, with two stale-input failures and the one mock error described above. No other failure was reported. The final exact rerun of all three affected cases passed **3 tests in 138.536 seconds**. Four additional candidate-view/registration cases added during review are included in the final 28-test focused run. These observations are not described as a single clean final full-suite run.

A frozen capture created with the actual baseline interface-33 compiler contains **440 files**. The interface-34 compiler successfully reconstructed that original capture without adding source inputs or mutating a store. This checks baseline capture readability, not the contents or readiness of the user's private proposal.

## Environment and limits

### Complete-checkout qualification

The delivered patch applied cleanly to the local implementation branch and was committed as `3a86d078`. A Python 3.12.3 environment with the repository's locked contract dependencies passed the 28 new registration/preview/MCP tests, the cold-process publication test (one test in 69.447 seconds), metadata (43), policy impact (10), contracts (52), analysis (114), and verifier (168) suites. The complete Engine suite passed all **311 tests in 501.610 seconds** against the committed candidate. Canonical contract projection freshness passed. Regenerating verification inputs through a temporary Engine store produced the packaged manifest and passed 73 suites and 121 structural checks.

The user's actual installed server and preserved proposal were not accessed. Supported local code qualification therefore does not establish the separate installed-user-proposal claim.

### Original package environment

Local runtime was Python **3.13.5**, outside the repository's declared Python 3.11/3.12 qualification. Installed jsonschema 4.26.0, referencing 0.37.0, attrs 26.1.0, jsonschema-specifications 2025.9.1 and typing-extensions 4.16.0 match the named lock versions. Local rpds-py is **2026.5.1** rather than locked **2026.6.3**. Test outcomes establish their local observed behavior; they do not substitute for the supported pinned-environment check.

The baseline read path, metadata, graph, schema, actual compiler, full/incremental replay, real MCP, SQLite and Git publication mechanisms were exercised. The report does not claim an independent external model review, a CI run of this patch, or a successful resume/publication of the user's actual preserved proposal.

A design self-review removed a proposed additional consumer-file freshness check after confirming that the existing readiness and compare-and-swap contract already binds publication to the exact original accepted revision. The patch reuses that authority rather than adding a redundant guard.

## Preservation and outstanding findings

The original normative and reference bodies, policy declarations, prompt/template bodies, skill reference bodies, node catalog, application-exposure manifest and reasoning-provenance manifest remain unchanged. The only content-guide change is the authoring H0 operation map needed to use the new capabilities. The real fixture and documentation registrations belong to the resumed standards proposal, not to this code patch.

The user's preserved proposal `503f233b-5c9f-442f-a04f-99f330142bae` remains external. Earlier review evidence remains historical evidence; new registrations may produce additional review/coverage obligations. Use current supported status/resume and revision handles. A change to accepted authority may require normal stale-state reconciliation; do not patch the store or transfer old readiness blindly.

Known separately scoped issues are automatic catalog replacement and large repeated workflow responses. Replace the actual server process and reconnect the client for interface 34. Use focused candidate read/route/related previews for view validation; this patch does not claim to solve arbitrary workflow output truncation.

## Handoff

See `APPLY.md` in the delivery package for base checks, integration, generators, MCP restart and example logical registrations. The local supported-environment checks are recorded above. The plan remains `Verifying` while external deployment/user-proposal claims are pending.
