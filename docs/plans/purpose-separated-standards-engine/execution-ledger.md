# Execution Ledger

## September 23, 2026 — Planning package prepared

Prepared the code-first implementation plan and separate standards-authoring guide against published baseline `366c1d90a24bbfb50973f62b155a5f3396c0f107`.

The user selected generic operational guidance, supplementary examples, authoring-only reasoning provenance, purpose-aware use of existing graph/Engine infrastructure, and freedom to replace older contracts without compatibility maintenance. The plan applies those prospective practices as a task-local design contract while preserving published normative content during code implementation.

Source inspection identified application exposure through full reads and relationship inspection, mixed navigation/authoring catalogs, reference-CLI schema/example paths, and the need to include registered prompts/templates in the later Engine-mediated migration.

No repository edits, code implementation, package test execution, real-client qualification, or content migration were performed as part of preparing these documents. All implementation acceptance claims remain pending. M0/S0 is the next implementation slice.

Document preparation checks confirmed the current plan checker's required headings, fields, acceptance-row states, and design-probe labels, plus local Markdown links and archive integrity. These are document checks, not an execution of the repository's Engine or complete verification checkpoint.


## September 23, 2026 — Code implementation and supporting verification

Reused the dedicated branch at `41598c4c` through its exact-history Git bundle.
The bounded source/consumer map was reconciled and implementation proceeded
independently of the unavailable pinned-client and remote Git transport. The
user selected a changed-files ZIP when remote delivery is unavailable.

Implemented the purpose boundary, qualified content, provenance association,
coherent authoring, replay, contract projections and local transports. All real
normative bodies and declarations remain unchanged; the two infrastructure
manifests start empty. The separate guide has not been executed.

The [implementation evidence](reports/implementation-evidence.md) records actual
tests, material repairs and remaining acceptance. It includes actual synthetic
Git/SQLite publication and separate-process CLI/MCP observations. Tests on the
available Python 3.13 are supporting observations, not pinned-platform acceptance.

The whole-module rewrite path required explicit same-revision preservation and
actual next-revision candidate metadata. This is represented by Analysis 7, with
updated fixtures rather than an old-format compatibility branch. Named wire
variants remain owned by the existing contract compiler.

The next accepted action is installed qualification and independent review.
Local implementation and artifact packaging do not authorize the standards
content migration while those requirements remain pending.

## September 23, 2026 — Final source verification and ZIP validation

Local Git CLI commit `ea4f643fbed938281e2a03e31963c995f0bcdcbb` contains the
implementation. The final navigation-index suite passed 14 tests, the existing
coverage-publication suite passed one test, and the focused authoring workflow
passed six tests. Final selected test processes completed normally.

The delivery patch recreated the intended index in a clean base checkout; the
incremental bundle fast-forwarded a separate disposable branch to the exact
clean implementation commit. ZIP CRC and all replacement hashes passed. The
artifact includes the exact base, patch, full files, bundle and apply procedure.
GitHub push remains DNS-blocked, so no PR was created. This evidence update does
not change source behavior, normative content or the pending acceptance boundary.

## September 23, 2026 — Post-delivery client qualification

Installed the Engine's hash-locked dependencies in Python 3.12 and the official
MCP Python SDK 1.30.0 in a separate disposable client environment. The SDK's
pending-workflow and full publication/recovery walkthroughs passed, including
application-purpose readback and provenance isolation. Codex CLI 0.156.1 passed
its configured app-server navigation harness against a temporary authoring
registration. The complete package run covered 477 Python tests and 73
structural checks after correcting one stale platform-harness contract version.

The installed Codex registration now declares authoring purpose. Its live client
loads the tool catalog, but automatic route rejects the old accepted `main` as
an unsupported capture. The real accepted ref and store were preserved; an
isolated store copy yielded ten proposal heads, five with applied outcomes and
five without recorded application.
Candidate-client qualification and this installed boundary are recorded in the
[implementation evidence](reports/implementation-evidence.md). Code integration,
old-store disposition, and independent review remain pending.

## September 23, 2026 — Old-store audit and disposition

Used the SQLite online backup API to make a consistent copy of the installed
store, then verified its integrity and SHA-256 after placing it in a private
offline archive at
`/home/jeremy/.local/share/standards-engine/archive/old-store-2026-09-23/`.
The adjacent `inventory.json` records the owning accepted Engine revision and
dependency-lock identity, proposal root and revision identities, relevant Git
revisions, readiness, application selection, application, and outcome links.

The inventory contains ten roots and ten revisions. Five have completed applied
outcomes. Five have no readiness, application selection, or application record;
they are deferred drafts, not interrupted publications. No admitted application
has an unresolved outcome. The deferred revisions are retained for historical
review and excluded from active cutover. Relevant intent must enter the new
Engine as new proposals against then-current accepted standards. The old store
and its proposal records were not edited.
All five applied candidate commits still exist as Git objects, but none is an
ancestor of current accepted `main`. The archive inventory records this exact
reachability; the fresh Engine will capture current accepted `main`.

Independent Standards and Spec reviews found no blocking source or spec issue.
The Standards review identified an application diagnostic path that could emit
private exception text to host logs or stderr. That path now reports only the
exception class, with focused tests for both Engine and MCP boundaries. The
suite-input projection was regenerated to match the changed source.

## September 23, 2026 — Accepted-main integration and fresh-store activation

Committed the reviewed repair and audit as `42d67355`, then fast-forwarded
local accepted `main` to that commit and returned the checkout to the
implementation branch. The original old SQLite file was moved into the private
archive alongside the independently verified SQLite backup and inventory.
Both database files pass integrity checks; the inventory records both hashes.

The new default store contains zero proposal roots and records and a snapshot
sourced from exact accepted `main` at `42d67355`. The installed Codex
`standards-engine` registration passed catalog, schema, route, and read checks
against that fresh store. Application CLI route returned the intended
`APPLICATION.CONTENT_UNAVAILABLE` result while the production exposure manifest
remains empty. The code release is accepted; real content qualification remains
the separate guide's work.

The earlier complete package run passed 477 tests. The post-fix rerun passed
the first five package groups and advanced through most Engine tests without a
failure, but was interrupted in a slow case; five focused post-fix regression
tests passed. The final generated-input and 73-check structural checkpoints
passed. This qualification limit is recorded rather than treating the
interrupted run as a complete post-fix pass.
