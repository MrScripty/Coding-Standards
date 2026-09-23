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

The available interpreter is Python 3.13.5, outside the declared supported
3.11/3.12 range. Installed jsonschema 4.26.0, referencing 0.37.0, attrs 26.1.0
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

Executed test records are summarized below. Final packaging reconciles their
results and any focused repairs. Structural checks do not execute the package
tests or certify prose quality.

| Observation | Result |
| --- | --- |
| Metadata suite, including new support parsing and staleness cases | 31 passed |
| Existing policy-impact suite | 10 passed |
| Contracts suite after variant capability check | 23 run; successful with one existing interpreter-dependent skip |
| Analysis domain suite, including explicit semantic preservation | 100 passed |
| Logical authoring suite | 23 passed |
| Existing low-level authoring suite | 13 passed |
| Engine analysis/publication workflow suite | 14 passed |
| Generated-contract/facade suite after explicit-purpose fixture repair | 15 passed |
| MCP transport unit suite | 12 passed |
| Purpose projection suite | 14 passed |
| Real CLI/stdin-stdout transport and cold SQLite reads | 4 passed |
| Existing focused agent navigation | 11 passed |
| Existing native navigation | 7 passed |
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

## Remaining acceptance

The official MCP SDK and configured Codex client are unavailable here. Their
existing harnesses have been updated for explicit purpose and the supporting
workflow, but execution in the supported locked environment remains required.
No independently delegated material review or inspection of the user's installed
store/pending recovery obligations was performed.

Candidate `a0a425ce93579ff6b0cabb05cc8a6f9b0ffe5f36` passed the corrected
generated-contract suite and the complete structural checkpoint. A final
formatting-only adjustment to seven test callers preserved their parsed ASTs.

The plan's C8 installed qualification and C10 independent final review therefore
remain outstanding. Required evidence is not replaced with the local interpreter,
a passing structural checkpoint, or the synthetic provenance review decisions.
The content guide remains gated on code acceptance.

## Handoff

The runtime operation and version map, empty-corpus bootstrap, replay limits and
safe cutover are documented in
[the Engine implementation contract](../../../../tools/standards_engine/PURPOSE-SEPARATION.md).
The separate [content guide](../../../guides/positive-guidance-and-provenance.md)
remains an authoring-only proposal. Start its work only after the remaining code
acceptance evidence is supplied.
