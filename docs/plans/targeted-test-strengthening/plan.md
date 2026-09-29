# Targeted Test Strengthening

**Plan status:** `Verifying`

**Current phase:** T1 implemented and locally verified; candidate CI/review and preceding packaging acceptance remain separate.

**Next slice:** **T2 — Candidate qualification and acceptance**

**Acceptance status:** `partial`

**Composed-design review:** `not-applicable`; tests and isolated fault examples
change only. Existing product owners, public interfaces, state and dependency
contracts remain unchanged. The small AST helper is private to its existing test.

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

## Objective

Make the five previously deferred test weaknesses detect their named regressions,
without changing production behavior or treating an accepted earlier slice as
incomplete. This is priority 3 of the selected 2 → 4 → 3 sequence.

The user authorized implementation of the next step. Source is prepared in an
isolated branch against `91ceb0fedcd6bb23513cf414a60b1e506d7de893`, tree
`83b59dffdb8312867a65582d53c55edf2576604a`. Packaging's exact-source workflow
`36509340996` now reports success. Its current plan still records Verifying;
external review and acceptance-owner disposition remain separate. This delivery
neither edits that plan nor declares it Accepted. Integrate this prepared next
slice after the preceding packaging acceptance is resolved.

## Scope

T1's exact write set comprises the following existing tests, this plan directory,
a link-only update to `docs/plans/README.md`, and the producer-generated
`evaluation/standards-effectiveness/generated/suite-inputs.json`:

- `tools/standards_engine/tests/test_typed_routing_projection.py`
- `tools/standards_analysis/tests/test_routing_records.py`
- `tools/standards_engine/tests/test_fact_material_ownership.py`
- `tools/standards_engine/tests/test_immutable_work_reuse.py`
- `tools/standards_snapshots/tests/test_storage_lifecycle.py`

No production repair, dependency, CI configuration, new framework, schema,
interface version, persistent format, acceptance-history rewrite or provider
operation is included. A demonstrated product defect is recorded before admitting
any production repair. Hash/equality and float-zero advisories remain deferred.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T-A1 | The three routing negatives distinguish the specified projection failure, not merely AnalysisError. | contract-negative | existing real compiler fixture | automated | satisfied | [Verification](reports/verification.md) |
| T-A2 | The record-independence assertion uses a detached oracle and detects shared outer and nested containers. | focused + mutation | local Python | automated | satisfied | [Verification](reports/verification.md) |
| T-A3 | The material-owner import guard detects declared absolute, relative and aliased static navigation imports while accepting unrelated imports/text. | structural + negative | Python AST | automated | satisfied | [Verification](reports/verification.md) |
| T-A4 | A changed aggregate_id cannot hit exact-record decoding and cannot replace its previously admitted entry. | focused + mutation | real snapshot/authoring fixture | automated | satisfied | [Verification](reports/verification.md) |
| T-A5 | A real EXCLUSIVE writer blocks the no-work expiry probe with BUSY/unavailable, without maintenance writes or a stranded transaction. | persistence integration | Linux SQLite DELETE journal | automated | satisfied | [Verification](reports/verification.md) |
| T-A6 | Existing affected suites, generated freshness and structural checks pass; delivered changes preserve all production files. | integration | supported Python 3.12 locked CI | automated | pending | [Verification](reports/verification.md) |
| T-A7 | Independent review and owner disposition accept this bounded test slice without reopening previous work. | review | reviewer and acceptance owner | manual | pending | [Verification](reports/verification.md) |

## Binding Decisions

Use literal AnalysisFailure expectations tied to the existing applicability and
Analysis diagnostic owners. Parsing stays outside the projection exception scope;
changing an error class's fields in a controlled example must invalidate the test.
The unchanged real compiler remains the ordinary execution path.

Retain the ordinary canonical-record fixture and make its expected containers
independent before mutation. Verify freshness of the outer list, records, values
and aliases. Never patch production merely to pass a newly copied expectation.

The dependency guard parses static imports with Python's AST and resolves relative
module names with `importlib.util.resolve_name`. It guards only supporting's
navigation dependencies; it is not a dynamic import detector or a repository-wide
architecture framework. Fixture module strings are parsed, never imported.

Construct a valid second revision through Authoring, then substitute only that
revision's ID in the first aggregate record. Require the original stored-revision
identity diagnostic and canonical decoder invocation, followed by an intact old
cache entry. The test must distinguish identity-blind reuse from normal behavior.

For the SQLite case, use two admitted real connections and BEGIN EXCLUSIVE under
DELETE journal mode. Shorten only the test connection's busy timeout. Observe
actual probe SQL, the underlying SQLITE_BUSY cause, no maintenance transaction,
and unchanged counts/material after rollback. No sleeps, latency threshold,
fabricated SQLite error, or production timeout changes are part of acceptance.

## Evidence And Oracle Plan

The source-backed advisory population is the preserved typed-routing external
review (broad projection errors), fact-owner review (mutable expected containers
and incomplete imports), reuse review (aggregate identity), and storage review
(exclusive-read contention). Their prior acceptance dispositions remain intact.
Use the supplied review's exact framing: these were test gaps, not established
production failures.

Controlled in-memory substitutes prove detection of named faults only. Record
baseline-test survival versus strengthened-test rejection where comparable.
Required normal tests run without substitutes. Raw logs, exact mutation functions,
environment, candidate identities and results are retained in the delivery;
no mutated production file is distributed or committed. No mutation score or
complete fault-coverage claim is inferred from the sampled cases.

## Milestones

### T1 — Five stronger test boundaries

**Status:** `Implemented`

Work: inspect original diagnostics/fixtures; update only the exact test owners;
prove sampled regression detection; run complete affected suites and the normal
structural/generated checks; review the diff and package against the exact base.

Gate: T-A1–T-A5 have direct positive and negative evidence. Local test evidence
remains separate from the supported-runtime qualification required by T-A6.

### T2 — Candidate qualification and acceptance

**Status:** `Planned`

Write set: this plan's records and generated inputs; necessary T1 repairs only.
Obtain or reuse exact-material locked CI, independent test review and owner
acceptance. Bind to the reviewed candidate and preserve packaging's separate gate.
No retrospective PR or repeated full campaign is required without changed claims.

## Blockers

Handoff preparation had only Python 3.13.5/rpds-py 2026.5.1. Its task-owned Python
3.12 installation attempt failed on DNS; no lock or environment guarantee was changed.
The integrated candidate later passed the affected local selections on Python 3.12.3,
as recorded in the verification report. Required hosted candidate CI and independent
review cannot be claimed from these local runs.
These do not prevent isolated source/test work; keep acceptance Verifying when
those are the remaining claims. Packaging acceptance remains an integration gate,
not an assumed fact or a reason to modify already-correct product code.

## Re-Plan Triggers

Record/reassess a demonstrated product defect, a changed public failure contract,
a need for a general import/test framework, fixture failure before the intended
boundary, or unsupported required SQLite behavior. A narrow direct fixture repair
within these test owners does not expand the product scope.

## Final Acceptance

T-A1–T-A5 have local passing evidence. T-A6/T-A7 still require the named
supported candidate environment and independent review/owner disposition. Close
only this slice after all required claims are satisfied. Earlier accepted work and the separate packaging records are unchanged.
