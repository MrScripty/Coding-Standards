# Purpose-separated Engine implementation evidence

Status: source implementation delivered for verification; the plan is not
accepted for standards-content migration.

## Source and execution boundary

The work starts from the existing branch
`implementation/purpose-separated-standards-engine` at
`41598c4ce3527fe539ae2f30d6f2cd4246faec11`. Its parent/main baseline is
`366c1d90a24bbfb50973f62b155a5f3396c0f107`. The pre-existing branch change is the
read-only Actions qualification workflow.

A GitHub Actions source bundle reproduced that exact history through Git CLI.
The source ZIP SHA-256 is
`2b61b32e73ee4d7f48ea265c48ec268fa5d31610296a0e16a9ef6ca198e7faf3`.
All implementation commits use Git CLI. Direct remote Git transport is
unavailable in the execution environment; the user authorized a changed-files
ZIP instead. No remote implementation push or PR is claimed.

At implementation delivery, the available interpreter was Python 3.13.5,
outside the declared supported 3.11/3.12 range. Installed jsonschema 4.26.0,
referencing 0.37.0, attrs 26.1.0
and jsonschema-specifications 2025.9.1 match their locked versions; local
rpds-py 2026.5.1 differs from pinned 2026.6.3. The dependency lock and supported
range remain unchanged. Results below are supporting source observations, not
substitutes for the locked installed-client acceptance claim.

## Implemented boundary

The host selects immutable application or authoring purpose. Engine public
operations and facade/transport dispatch enforce purpose before authoring work.
Application wire variants are declared in the canonical contract, and explicit
application result models are built from qualified domain data. The same view
covers native/focused reads, inspection, relationship traversal, routing facts,
continuations, catalogs, schemas, CLI examples and transport encodings.

Whole-module exposure binds reviewed content, metadata and applicable routing
inputs. Policy scopes inherit the containing module's review. Registered
prompts/templates bind their actual content and declared owner facts. A filtered
graph precedes traversal, including relationships owned by a module's policy
units; hidden intermediary nodes create no application path.

Provenance records, operational-aid revisions, explicit exposure and supporting
review obligations compose through the existing proposal/analysis/review/local
publication/recovery machinery. The subject association has one declaration;
its graph edge is derived and descriptive. Captures include all new authorities.
New automatic snapshots read accepted main, not an unpublished checkout branch.

The real standards, reference bodies, prompts/templates and normative relationship
and policy-unit declarations are preserved. Both new real manifests are empty.
No wording migration or real application qualification was performed.

## Material implementation decisions

The existing contract compiler now admits named operation variants. This is a
small extension to its existing representation owner, not an additional schema
validator. The compiler's exact public root closure includes those variants and
preserves submission-capability coverage. This adds
`tools/standards_contracts` to the plan's concretely affected owner set.

Whole-module positive rewrites require explicit preservation across structural
changes. Previously, preservation required the structural digest to remain
identical, and changed semantics were represented as a separate proposed overlay.
The implemented contract instead analyzes explicit same-revision preservation or
next-revision change against the actual candidate's semantic revision. This
keeps candidate text, metadata, supporting bindings and review subject coherent.
It is a deliberate Analysis interpretation change: request 6, result/state and
Analysis handles 7. Engine interface is 31 and implementation version is 0.2.0.
Unchanged generic identity, Snapshot and store contracts keep their versions.

The generic graph engine, SQLite store and publication lifecycle were retained.
No automatic prose rewriter, model scorer, additional database, context cache,
remote permission system or compatibility adapter was added.

## Supporting tests

Executed test records are summarized below. Final selected runs passed after the focused repairs described below.
Structural checks do not execute the package tests or certify prose quality.
These selected runs did not include the complete Engine suite in the supported
pinned environment at delivery time. Post-delivery qualification is recorded
below.

| Observation | Result |
| --- | --- |
| Metadata suite, including new support parsing and staleness cases | 31 passed |
| Existing policy-impact suite | 10 passed |
| Contracts suite after variant capability check | 23 run; successful with one existing interpreter-dependent skip |
| Analysis domain suite, including explicit semantic preservation | 100 passed |
| Logical authoring suite | 23 passed |
| Existing low-level authoring suite | 13 passed |
| Engine analysis/publication workflow suite | 14 passed |
| Existing coverage-publication suite | 1 passed |
| Generated-contract/facade suite after explicit-purpose fixture repair | 15 passed |
| MCP transport unit suite | 12 passed |
| Purpose projection suite | 14 passed |
| Real CLI/stdin-stdout transport and cold SQLite reads | 4 passed |
| Existing focused agent navigation | 11 passed |
| Existing focused agent authoring workflow | 6 passed |
| Existing native navigation | 7 passed |
| Navigation-index suite, including verified index publication | 14 passed |
| Renderer suite after purpose/publication distinction | 10 passed |
| Coordinated publication followed by provenance-only publication | 1 passed using real Git, SQLite and the complete publication checkpoint |
| Full structural checkpoint | 73 suites passed; zero failed or blocked |
| Canonical contract projection freshness | Passed |
| Real normative-body and declaration preservation against branch base | Passed |

The publication test ran in an isolated candidate repository, using actual
review submissions for synthetic content. It published a rule, reference,
registered prompt/template, provenance and exposure; read the application and
authoring views; then published a rationale-only update while preserving the
rule and historical snapshot content. These fixture decisions do not certify
real standards or replace independent implementation review.

The explicit purpose contract required updating in-repository test callers.
A remaining purpose-less fake Engine in the generated-contract test was found
by the broader run and corrected; the exact case and the complete 15-test suite then passed. Earlier
findings included graph-source attribution, private imports bypassing public
module interfaces, stale contract examples, and MCP error classification.
Those were repaired rather than suppressed or accepted as baseline debt.

Candidate `03523e09c10a470f77f4d2f82f4365f34a827ab3` supplied the real publication
observation. Candidate `fe6c88e032ed28715c2ed9aa5240aadea2895873` supplied the broader
package and transport observations. Later focused repairs preserve these
subjects where unaffected and are checked at their changed boundary. These are
private test-candidate commits, not user-repository main updates.

Candidate `a0a425ce93579ff6b0cabb05cc8a6f9b0ffe5f36` passed the corrected
generated-contract suite and the complete structural checkpoint. A final
formatting-only adjustment to seven test callers preserved their parsed ASTs.

## Post-delivery client qualification — September 23, 2026

Python 3.12.3 installed the six Engine dependencies from
`tools/standards_contracts/requirements.lock` with `--require-hashes` and
`--only-binary=:all:` into a disposable environment. A separate disposable
client environment installed the official MCP Python SDK 1.30.0. Both
environments passed `pip check`.

The official SDK pending-workflow harness passed: it refused review before a
required disposition and accepted explicit resolution. The full SDK walkthrough
also passed against a disposable repository whose local `main` was the candidate:
authoring and application catalogs were purpose-separated; interrupted
publication required cold-process recovery; retry did not republish; stale
revision review was refused; explicit resume and normal publication succeeded;
application readback exposed approved content without authoring-only provenance.

Codex CLI 0.156.1 ran `tests/codex_navigation_client.py` through its actual
app-server client using a temporary `standards-authoring` registration pointing
at the candidate and the hash-locked Engine Python. It discovered 15 focused
tools, checked all 20 inline edit variants and the nested evidence schemas,
then completed route-to-read with the exact snapshot. This did not start a
model turn or modify the installed Codex configuration.

The CI-defined package run covered 477 Python tests and 73 structural checks.
One platform-harness fixture initially used request contract version 5 despite
the branch's version 6 contract; correcting that fixture and rerunning its three
tests passed. The package run used locally cached pinned dependency versions;
the separate client qualification used a fresh hash-verified Engine install.

## Remaining acceptance

The user's installed `standards-engine` registration now includes
`--purpose authoring`. The live Codex client discovers its 15 focused tools and
validates their schemas, but route returns `SUPPORT.UNSUPPORTED_CAPTURE` because
the accepted local `main` predates the new content contract. The candidate
passed route/read in a temporary registration whose local `main` was the exact
candidate. The real accepted ref was not retargeted to make the test pass.
The installed store was copied using SQLite's online backup API and retained
offline with a verified per-revision inventory at
`/home/jeremy/.local/share/standards-engine/archive/old-store-2026-09-23/`.
It contains ten proposal roots and ten revisions. Five revisions have an
application selection, application record, and `applied` outcome; five have no
readiness, selection, or application record. No admitted application has an
unresolved outcome. The five deferred drafts are retained for historical review
and excluded from active cutover. Any useful intent requires a new proposal
against then-current accepted standards; no stored proposal status was changed.
The inventory preserves root/revision IDs, relevant Git revisions, and the
owning accepted Engine revision and dependency lock identity.
All five applied candidate commits exist as Git objects but are not ancestors
of current accepted `main`. The inventory records that reachability, and fresh
snapshots will use current accepted `main` as their source.

Independent Standards and Spec reviews of `git diff main...HEAD` plus the
working changes found no substantive source-scope mismatch or blocking code
standard violation. The Standards review identified full exception logging at
the application boundary as a diagnostic privacy risk. Application paths now
emit bounded exception class names without exception text or traceback; focused
tests assert that a private exception message is absent from both the public
response and diagnostics. The generated suite-input manifest was refreshed.

The plan's C8 installed cutover and C10 independent final review remain
outstanding. Synthetic provenance review decisions do not certify the real
standards content. The content guide remains gated on code acceptance.

## Delivery validation

The implementation commit is `ea4f643fbed938281e2a03e31963c995f0bcdcbb`, created
on the existing dedicated branch with Git CLI. The changed-files ZIP provides
complete replacement files, a full-index patch, an incremental Git bundle,
base/result hashes and application instructions. In separate disposable clones,
patch application reproduced the intended index and bundle import fast-forwarded
to the exact clean commit. Archive CRC and replacement-file hashes also passed.

The explicit Git CLI push to the existing GitHub branch failed with
`Could not resolve host: github.com`. The fallback archive is the delivery;
no remote push or pull request is reported.

## Handoff

The runtime operation and version map, empty-corpus bootstrap, replay limits and
safe cutover are documented in
[the Engine implementation contract](../../../../tools/standards_engine/PURPOSE-SEPARATION.md).
The separate [content guide](../../../guides/positive-guidance-and-provenance.md)
remains an authoring-only proposal. Start its work only after the remaining code
acceptance evidence is supplied.
