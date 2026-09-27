# Agent Interaction Quality — Verification

**Status: Verifying.** Code is implemented in an isolated checkout. Supported-runtime
CI for this diff, the deployed client check and independent review remain separate
acceptance gates. Source baseline: `67266105cbd900d89572eb540b54b298653ed01c`.
The coordinated interface is **41**; Analysis request 6 / state projection 7,
workflow handles, readiness, recovery and SQLite formats are unchanged.

## Changes and ownership

The contracts runtime remains the single validator-facing owner. It obtains
structured errors from jsonschema and projects at most eight value-free issues,
with an 8 KiB serialized issue-array bound and bounded error traversal. Declared
field names, array indices, validation keywords and safe constraint explanations
are retained. Dynamic map keys are redacted, overlong locations are explicitly
non-exact, and omitted detail is flagged. A proven disjoint discriminator selects
useful diagnostic causes only; ambiguous unions are not guessed and validity
still comes from the independent validator. Successful input does no feedback work.
The original first error/cause tree remains available internally.

The Engine facade returns typed feedback and an operation-specific `describe_input`
request before invoking domain actions. Runtime-info and input-discovery observers
use the same feedback owner. Typed request-local evidence normalization retains
specific missing/unused-reference explanations without exposing alias values or
introducing a second evidence registry. Malformed handle versions are not echoed.
Input diagnostics do not infer evidence, approve decisions or create proposals.

`relationship_groups` uses the current snapshot's existing graph. Its page includes
registered IDs, purposes and traversal policies, with default eight / maximum 32
whole records and a 16 KiB page bound. Returned `next` requests retain snapshot and
selection. An omitted snapshot explicitly captures accepted authority; a nonzero
offset cannot select fresh ambient authority. Registered groups with no edges for
a target remain valid. The application projection supplies only its permitted graph
and requires qualified Router content for vocabulary discovery. Hidden targets
cannot be used to retrieve private groups. No secondary registry or alias guessing
is introduced.

Unknown focused relationship queries now include that same first vocabulary page;
authoring retains `GRAPH.UNKNOWN_GROUP`, while application returns the qualified
`APPLICATION.UNKNOWN_GROUP`. The first page is not a claim to contain all groups;
its counts and continuation remain explicit. Native authoring query and candidate
preview failure shapes are unchanged. Final snapshot lifecycle checks prevent a
page from being published after authoritative lifetime loss.

Focused authoring `route` now defaults to `compact-route-result`: all selected
reading entries and required dependencies, exact known facts, all unanswered fact
questions, a remaining unresolved reading-plan count, and a same-snapshot full
`explanation` request. It does not construct full rule expressions just to discard
them. `detail: "full"` returns the prior `agent-route-result`. Full detail and
content-page continuations preserve their selection. Native query/preview contracts
and application qualification remain unchanged. No omitted fact becomes an empty
set; the six questions in the measured case remain genuinely unanswered.

Catalog descriptions point to the existing input discovery and new vocabulary.
The read-only `tests/catalog_inventory.py` utility distinguishes description
characters/UTF-8 bytes, input schemas, output schemas and serialized catalog JSON,
and accepts actual saved tools/list responses. It does not reconfigure clients,
open a standards store, submit tools, or claim that host-generated declarations
have the same size. **Compatibility mode remains the default**. There is no new
mode, guessed client policy or implicit support retirement.

## Acceptance evidence

| Check | Observed result |
| --- | --- |
| Complete Engine selection, four file-disjoint shards | 488 passed; no skips, errors or failures |
| Final focused feedback/navigation/catalog rerun | 30 passed; included in package totals |
| New Engine and contracts regression methods | 25 + 8; included in package totals |
| Cold-process MCP stdio interaction checks | 3 passed; included in Engine total |
| Contracts/compiler package | 69 passed; 1 existing environment check skipped |
| Metadata / policy-impact / Analysis / verifier packages | 43 / 10 / 121 / 168 passed (342 total) |
| Graph package | 37 passed |
| Complete registered structural checkpoint | 121 checks across 73 suites passed |
| Generated-contract freshness and diff checks | Passed |
| Interface-40 to interface-41 retained fixture | Exact status, repeated review, readback and main preserved |

The complete Engine run used one frozen runtime/source checkpoint, after the early
fixture/import corrections. All four shards passed on that run (121, 94, 166 and
107 tests). The final focused rerun passed before this verification record and
plan status were finalized; only maintenance records and generated verification
inputs were then refreshed. The final structural/generation/patch checks validate
that delivered material. No earlier failed case is counted as a pass without its
successful rerun.

The new tests are included in package totals, not additional passes. Test logs,
shard selections, outcome reconciliation, exact measurements and reconstruction
hashes are included under `DELIVERY/evidence`.

Initial navigation tests identified two test-isolation errors: one assumed a policy
identity field that this authoring view does not expose; another intercepted rule
serialization during snapshot compilation rather than isolating the presentation
under test. Both were corrected and their focused reruns passed. Initial structural
verification identified three private cross-package imports; these were corrected
to public roots and a public diagnostic-bound export before the complete checkpoint
was rerun successfully. The earlier failures are retained, not relabeled as passes.

## Measured interaction and catalog effects

Measurements use default Python JSON serialization of exact tool/domain values,
not model tokens, latency, billing, context-window use or model reliability.

For two explicit known routing facts (implementation activity and an explicitly
empty application-profile set), full routing returned **30,136 JSON bytes** and
compact routing **6,041 bytes**, a **79.95% reduction**. Both contained the same
three selected reading entries, all six unanswered fact questions and the same
known facts; 43 unresolved reading-plan entries moved to the explicit explanation.
Those entries were not deemed inapplicable. The optional full explanation requires
one additional read only when its details are actually needed.

The invalid `{"change_set": {}}` proposal now identifies `/change_set/purpose` and
`/change_set/edits`, rather than only a generic contract error. An unknown `related`
group returns canonical choices and can be repaired without an intervening full
policy read. The integration tests perform these calls through actual cold stdio
processes, not a mock MCP transport or model-generated input.

| Focused catalog | Baseline descriptions (characters) | Updated descriptions | Baseline complete JSON (bytes) | Updated complete JSON |
| --- | ---: | ---: | ---: | ---: |
| Authoring / compatibility | 60,070 | 60,750 | 728,810 | 807,727 |
| Authoring / native | 9,744 | 10,424 | 623,157 | 702,074 |
| Application / either mode | 2,572 | 3,096 | 44,388 | 76,052 |

The updated catalogs contain 22 focused authoring tools and nine focused application
tools. Descriptions grew by 680 and 524 characters respectively. Most complete
catalog growth comes from declaring typed output feedback and group pages, which
appear in each standalone tool output schema: authoring output-schema JSON grew
from 526,236 to 603,441 bytes; application from 34,489 to 64,598 bytes. Input-schema
JSON grew by 903 bytes in each catalog. This is a real tradeoff, not a claimed
catalog-size reduction. Native authoring descriptions still omit the 50,326-character
embedded-schema fallback; that change already existed at the baseline.

The operator's approximate 71,000-character observation was not reproduced from
this source-only description measure. Use the inventory command on the actual
saved catalog to distinguish runtime/catalog drift from the host's presentation
or counting convention. Do not infer token savings from these raw byte counts.

## Retained authority and unchanged state

A baseline interface-40 process created a real disposable reference proposal,
Analysis and readiness. With the same store and accepted main, a fresh interface-41
process obtained identical status, repeated-review readiness and exact proposal
content readback. No migration, deletion or publication occurred. This is retained
state evidence for the synthetic fixture, not a claim about the user's private
production store.

Of 316 prior schema definitions, **312 remain exactly unchanged**. Changes are
limited to `RouteCall` and the three rejection models that gain optional feedback;
six definitions were added. Native authoring mutation types and all persisted
representations are unchanged. The baseline Core, Router and 71 workflow/topic/
profile/reference files are byte-identical. No dependency pins, normative content,
approvals, provenance or coverage attestations were changed.

## Environment, qualification and cutover

Local evidence was executed on Linux with CPython 3.13.5, jsonschema 4.26.0,
referencing 0.37.0 and rpds-py 2026.5.1. The repository's supported environment is
locked CPython 3.11/3.12, including rpds-py 2026.6.3. A bounded attempt to provision
3.12 failed because DNS was unavailable. The lock remains unchanged, and the
interpreter-dependent environment test is explicitly skipped rather than counted
as passing. Run supported CI for this exact diff before acceptance.

No authenticated Codex or other real model turn was run here. The updated existing
configured-client harness includes group discovery, but passing scripted stdio
checks is not deployed-model qualification. The reported previous native session
and pending preserved-trace reconciliation remain separate evidence; no verdict
was fabricated or silently changed. Compatibility retirement requires explicit
qualification or support retirement for the actual supported deployment set, plus
integration review; hypothetical unspecified clients are not a permanent gate.

Apply all changed source, tests, generated projections and the generated input
manifest together. Refresh the client catalog after restarting the MCP server.
Clients that asserted `agent-route-result` for every focused route must accept the
new default compact result or explicitly request full detail. Preserve installed
stores and exact workflow handles. The default compatibility flag and native
opt-in remain as before. Remote repositories and the user's unrelated ZIP changes
were not accessed for mutation.
