# Engine routing and review workflow verification

**Status:** source implementation complete; installed acceptance remains pending.
**Reference source:** `c947f5456d37c9fffbaefdf0bb0d4004eee699cf`.
**Implementation commits:** `b4fb45db` and fact-value correction `a39d1739` in the
private disposable implementation branch. No external refs were updated.
**Interface edition:** 36. Independent Analysis, Snapshot, readiness, application
and SQLite formats are unchanged.

## Source and standards boundary

The complete GitHub Actions source bundle reproduced the exact reference history.
Its archive SHA-256 was
`bbc83e496ab76894e57da830de94cf216956f9e1e9083007de6be29fe3e83738`.
The user-reported accepted local migration `72963ad5` could not be fetched from
GitHub or the retrieved files. This work therefore uses the accessible routed
standards plus the explicitly agreed positive-guidance practices. It does not
claim to have inspected the final local wording or the user's live store.

The implementation plan was written before production edits. Its owners,
acceptance claims and composed-design review governed the work. The small
fact-value fix and corrected paging-evidence interpretation are recorded in the
ledger. No separate graph, workflow database, review lifecycle, automatic
reviewer, hot-reload mechanism or compatibility implementation was added.

## Implemented behavior

A single Router selection parser supplies compilation, readable routing
inspection and logical routing edits. It reads the documented pipe-table/module
link representation rather than historical headings. Tests rename and remove
the S1 heading, preserve ordinary targets, exercise simultaneous retargeting,
and assert exact preservation outside changed selection rows. Fenced examples,
prose and optional references do not become normative selections. The helper
is deliberately a narrow Router format owner, not a general Markdown engine.

`resolve_many` accepts explicitly authored decisions against one original
Analysis, validates each through the ordinary submission/evidence/authorization
owner, and stores only the final Analysis under the existing proposal-head
guard. Rejected batches leave no intermediate Analysis publication. External
provider and authorization observations are not a global transaction. Batching
supplies no coverage assertion, review approval, readiness or Git publication.

Focused workflows default to compact summaries. `workflow_details` retrieves
bounded sections with exact work handles, including coverage requirements.
Continuations bind the original Analysis, section and selected observations.
Historical detail remains historical; its observation token is neither live
publication authority nor a persisted workflow state. `detail: full` remains an
explicit diagnostic choice.

`runtime_info` identifies the running instance, purpose, interface, schema,
catalog and implementation material. It observes installation drift without
opening the standards store or Git. Initialization, tool listing and normal
responses carry the same identity. An expected catalog digest distinguishes a
client's actual retained catalog from the running one. Restart/reconnect or
refresh is an explicit operator/client action, not promised hot reload.

The fact test found a shared-validator defect: a schema-owned fact map was
assumed to supply an object method. The validator now serializes through its
containing generated submission. Single and batched fact decisions produce the
same final Analysis identity.

## Executed evidence

| Check | Actual result |
| --- | --- |
| Baseline heading-regression cases | Both failed before the parser replacement, reproducing the reported coupling. |
| New parser and existing routing cases | 18 passed. |
| Integrated Router loader/read/edit cases | 3 passed; included again in the composed owner run. |
| Corrected batch, paging, fact, authorization and head-race cases | 10 passed. |
| Runtime identity cases | 4 passed, including real CLI/MCP without Git/store; included again in the composed owner run. |
| Metadata package | 43 passed. |
| Policy-impact package | 10 passed. |
| Contracts package | 54 run successfully, with one pre-existing interpreter-dependent skip. |
| Analysis package | 121 passed. |
| Verifier package | 168 passed. |
| Earlier affected workflow/supporting/generated/material/purpose tests | 50 passed. |
| Composed Engine owner run | 105 executed: 104 passed; one old full-envelope equality assertion needed the new process-identity distinction. The corrected exact cold-MCP case passed. |
| Real cold MCP batch/review/preflight/publication/readback and recovery | Both workflows passed (2 tests). |
| Final complete structural checkpoint | 73 suites, 121 checks passed. |
| Generated contract freshness, syntax and staged whitespace | Passed. |
| Protected source comparison | All 70 canonical modules and 120 total protected content/registration files unchanged. |
| Package reproduction | Base-bound patch and resulting file hashes verified; ZIP CRC verified. |

The new MCP test reuses the existing real publication walkthrough through a
raw JSON-RPC stdio client, with synthetic standards, real Git/SQLite and actual
review submissions. It verifies mixed coverage/consumer/impact decisions,
application preview/readback, explicit review and verification, and failed
publication followed by cold explicit recovery. A separate real-domain test
exercises fact answers and proves serial/batch authority equivalence. These are
not the user's 84 live decisions or real content audit.

### Failures investigated and corrected

Early tests exposed stale authored example metadata still naming interface 35;
the example authority now agrees with interface 36. Intermediate runs also
encountered stale generated input digests while source was changing. The final
checkpoint used freshly generated inputs. An integration fixture initially
passed `(path, bytes)` pairs where a set of paths was required; that fixture was
corrected before the integrated Router tests passed.

The composed owner run caught a historical-read test comparing entire MCP
responses across fresh servers. Different server instance IDs are now intentional.
The corrected assertion requires different process IDs and identical historical
content/result fields, preserving the original replay claim rather than suppressing
it. Its exact cold-process rerun passed. The Router regression fixtures were also made independent of the continued
presence of the historical S1 title; the final ten heading/parser/consumer tests
passed.

The first combined focused run had 22 successful cases plus the shared fact-map
error and an incorrect expectation that historical Analysis pages revalidate
live evidence files. The fact owner was fixed. The page test now establishes
actual context/section binding and stable historical reads; live evidence
validation stays with decisions and publication. The corrected ten-case suite
passed in full.

An exploratory whole-Engine sweep started before the final fact correction and
was stopped as superseded. It is not counted as a completed full Engine suite.
The completed owner runs, package suites and real MCP walkthrough provide the
named evidence. Interrupted invocations are not passes. No external independent
reviewer was available; the code review recorded here is a self-review, separate
from the user's earlier independent standards-material review.

## Response-size observation

A four-decision fixture compared the same original proposal and reached the
same final Analysis identity through serial and batched submissions:

| Domain JSON payload | Bytes |
| --- | ---: |
| Pending full response | 12,005 |
| Pending compact response | 1,867 |
| Complete full response | 11,519 |
| Complete compact response | 1,681 |
| Four serial full decision responses, combined | 44,054 |
| One batch compact decision response | 1,681 |

The decision-response component was approximately 96% smaller. This excludes
submission input, discovery, detail-page reads, protocol framing and duplicated
MCP text/structured encodings. It is not a general end-to-end latency, model-cost
or correctness improvement claim. Every decision retains its own evidence and
authorization; computation needed for those checks remains.

## Runtime environment and remaining gate

### Complete-checkout integration on supported Python

The package was applied to the current `main` checkout at `b5f3b275`, with all
42 supplied source/result hashes and the patch check matching. The suite-input
manifest was regenerated from this checkout instead of copied from the package.
Integration used Python 3.12.3 and locked contract dependencies, including
rpds-py 2026.6.3. The contract projection and complete structural checkpoint
passed (73 suites, 121 checks).

Contracts (54), Analysis (121), verifier (168), metadata (43), and policy-impact
(10) tests passed. The focused routing, workflow, runtime, and review cases
passed except for one synthetic consumer path already registered in this
checkout's policy-impact catalog. The fixture was moved to existing unregistered
files; its 15 tests and both real cold MCP publication/recovery tests then passed.
An affected Engine run passed 78 tests and found one baseline assumption that
`core` lacked application exposure. This checkout approves `core`; the test now
uses an existing unapproved standard, and its focused rerun passed. These were
fixture corrections for current content, not changes to publication authority.

The code and generated contract are qualified in this checkout. An installed
server/client and any preserved live proposal or store remain outside this local
test and require separate operator verification.

### Package-source environment

Local execution used Python 3.13.5, jsonschema 4.26.0, referencing 0.37.0,
attrs 26.1.0, jsonschema-specifications 2025.9.1 and rpds-py 2026.5.1.
The repository supports Python 3.11/3.12 and locks rpds-py 2026.6.3. The official
MCP SDK was unavailable in this environment; real stdio protocol tests were
executed instead. These limits are explicit U7 installed-qualification work,
not successful supported-platform evidence.

Integrate on the actual migrated checkout, regenerate verification inputs from
that combined tree, run the supported locked-host checks and review against its
current applicable standards. Restart the actual server process and reconnect
its client; verify runtime_info and current catalog. No database reset or
rewriting of published content is needed. Existing evidence that explicitly
names changed code/documentation remains subject to its normal currentness
checks; the patch does not automatically renew receipts.

The delivery intentionally excludes a baseline-derived suite-input manifest so
it cannot overwrite bindings for the user's migrated corpus. The package's
APPLY.md gives regeneration and qualification steps. Source implementation is
complete; exact local corpus compliance, installed-client qualification and
whole-library effectiveness are not represented as established here.
