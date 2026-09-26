# Agent Workflow Simplification — Verification

Date: 2026-09-26. Status: implementation complete; local supported-runtime
qualification is complete, while configured-client restart and independent-review
qualification remain open. Base: `c4470f9e683da1e494eeeac3497e72e079221bac`.

## Implemented scope

The existing focused workflow facade now returns actionable pending work for
compact `propose`, `revise`, `analyze`, `resolve_workflow` and `resolve_many`.
The first page contains up to eight whole items and 64 KiB of page JSON, preferring
missing facts before required obligations. It is derived from the native result
already produced by the operation, with no extra Analysis evaluation or provider
execution. A large first record preserves success and returns an explicit full
read selection. Whole-record paging and observations share the existing owner.

Focused action continuations and compact summaries inherit the enclosing exact
context instead of copying it. Actual child work handles remain explicit.
`workflow_status` stays summary-only and retains its direct-count implementation;
full diagnostic outcomes remain supported. Review, authorization, atomic batch
admission, apply and recovery are unchanged and remain explicit.

Agent instructions now use actual compact fields, ready decision batches,
automatic proposal analysis, and grouped reads. Routing tool descriptions also
recommend `read_many` to ordinary application agents, without giving them the
authoring skill or catalog. Existing compatibility schema descriptions and MCP
structured/text representations are retained. Route-plus-content and request-local
evidence deduplication remain outside this bounded slice.

## Contract and retained state

Interface **38** replaces the focused result shape. The canonical schema generates
both public Python models and tool definitions; examples and direct consumers were
updated together. Request contract 6, result/state 7 and all handle/store versions
are unchanged. Restart the Engine and reconnect the client using the new catalog,
while preserving exact handles and the existing store.

A cold cross-version check created pending Analysis and readiness with the pinned
interface-37 implementation, then reopened the same store with interface 38. It
preserved both handles, read the new summary, accepted old work against its exact
old context, and returned two remaining inline obligations. No migration or store
deletion was performed. The fixture did not automatically review or apply anything
after cutover. This is retained-domain qualification, not a certification of the
user's installed host/client upgrade.

## Observed interaction cost

The same fixture creates four explicit impact obligations and resolves them in two
batches, stopping at complete Analysis before review/publication. Each call used a
fresh real MCP stdio server and verified structured/text result agreement.

| Metric | Interface 37 client | Interface 38 client |
| --- | ---: | ---: |
| Tool calls | 5 | 3 |
| Serialized argument bytes | 9,750 | 9,378 |
| Serialized result bytes | 18,499 | 16,091 |
| Arguments plus results | 28,249 | 25,469 |

This fixture needed **40% fewer tool calls**, **13.0% fewer result JSON bytes**,
and **9.8% fewer combined argument/result bytes**. Pending mutation responses are
larger than the old counts-only response; the reduction is across the complete
interaction because intermediate detail reads disappear. These are not tokenizer,
model reasoning, billing, general latency or application-wide performance claims.
MCP initialization, catalogs, envelopes and compatibility duplication are outside
the byte measure. The repeatable harness is
`tools/standards_engine/tests/workflow_interaction_trace.py`; run each client mode
against its corresponding source checkout.

The authoring catalog is a separate tradeoff: serialized `tools/list` JSON grew
from **663,883** to
**695,769 bytes** (about 4.8%), primarily because
the output schemas now describe inline work. There are still 20 focused tools;
input-schema bytes are unchanged at 120,974.
Descriptions grew by 436 bytes.
This measurement is wire/catalog JSON, not what a particular client injects into
the model. A short session that transfers the catalog can therefore exchange more
total wire bytes despite fewer calls. Actual model-visible cost requires the
configured-client qualification; the result-byte reduction is not a claim of net
token or billing savings. `catalog-wire-comparison.json` records both catalog parts.

## Verification results

| Check | Result |
| --- | --- |
| Full Engine suite, independently isolated module shards | 381 tests; 0 skipped; no failures |
| Focused workflow/paging/reuse/runtime suite | 50 tests passed |
| Final MCP/runtime/new-interaction checks | 26 tests passed |
| Contract/compiler suite | 54 tests; 1 environment qualification skipped |
| Analysis domain suite | 121 tests passed |
| Metadata suite | 43 tests passed |
| Policy-impact suite | 10 tests passed |
| Structural Verifier implementation suite | 168 tests passed |
| Registered complete checkpoint | 121 checks across 73 suites passed |
| Generated contract freshness | Compiler `--check` passed |
| Whitespace/error check | `git diff --check` passed |

## Integration checkpoint

After applying the delivery patch to the working tree, the exact locked Python
3.12.3 environment passed generated-contract freshness, all 54 contract tests,
and `verify_repository` (121 checks across 73 suites). A disposable committed
candidate passed the complete Engine suite: 381 tests, 0 failures. The focused
runtime, review, consumer and workflow-interaction smoke checks passed 29 tests.
The cold trace reproduced the intended presentation change: five calls with
explicit detail pages and three calls with inline work, both ending in
`complete`.

The first full-suite attempt against the uncommitted worktree produced one
`SUITE_INPUT.STALE_FILE` failure because its clone-based fixture starts from
`HEAD`; the same test passed in 2.3 seconds after the exact candidate was
committed in a disposable clone. This was an integration-fixture condition, not
a source or generated-manifest defect.

The freshly launched local CLI reports Interface 38. The host-managed connected
authoring MCP still reports Interface 37 with `installation_state:
restart-required`; reconnecting that client remains an operator gate.

The complete Engine suite was partitioned by test module into independent disposable
clones, accepting the implementation checkpoint `cc101135` as local main. The
fourth shard initially caught a test-client error: a resumed `workflow_status`
correctly omitted inline work, but the updated test helper required it. The helper
now reads the initial page only for lightweight status and consumes inline work
when present. That entire shard was rerun at `1c465c3c`, which also includes the
routing-description/agent-doc clarification; production domain behavior was
unchanged. Both the initial failure and completed rerun logs are retained.
The shard manifest records exact selections, commands and the follow-up revision.
Counts do not multiply these tests by also adding focused reruns. Final MCP,
runtime and new-interaction checks cover the routing-description clarification.
The initial sequential exploratory run was replaced by these isolated complete
shards; its interrupted log is not acceptance evidence.

The new regressions cover direct multi-turn work without first-page fetches,
missing-fact progression, exact page equivalence, whole-record byte pressure,
explicit oversized retrieval, cold continuations, strict result shapes,
stale/foreign work rejection, lightweight status and absence of domain effects
from presentation. Existing cold MCP cases exercise consumer/coverage decisions,
explicit review, real local publication and interrupted-publication recovery.
An initial new test demonstrably failed against the original duplicate-context
response before the implementation.

## Failure found and resolved during qualification

The inherited cold-publication scenario resumes a proposal through lightweight
`workflow_status`. Its compact batch test consumer had assumed every pending
workflow result included `work`, causing `KeyError: work`. The correction is in
the test consumer, not in the Engine: status continues to be lightweight; a
caller resuming from status obtains its initial page explicitly. Mutation results
continue to remove that read. The full affected shard, including publication and
recovery, was rerun rather than suppressing or skipping the failing scenario.

## Standards and remaining qualification

The implementation uses the existing workflow and pure projection owners rather
than introducing session state, a new identity layer or automatic decision-making.
The generated-contract and IPC boundary change is explicitly versioned, documented,
and exercised by real process consumers. The existing evidence and publication
owners retain authority; structural verification is not represented as semantic
review. No normative policy, exposure approval, attestation or user state was edited.

Local execution used **Python 3.13.5** with **rpds-py 2026.5.1**, rather than the
repository's supported locked Python 3.11/3.12 and rpds-py 2026.6.3. The dependency
lock was preserved; its exact-environment test was skipped explicitly. These local
runs are diagnostic correctness evidence, not supported-environment qualification.
The configured Codex client and independent external reviewer were not available
in this run. Run the prescribed locked-environment/client checks and independent
review before marking the change Accepted or merging it. No remote push or merge
was performed.

## Delivery

The ZIP contains complete changed/new files at repository-relative paths, this
report and the slice's plan/ledger/issues. `DELIVERY/` contains a unified patch,
base/new file hashes, integration instructions and the recorded verification logs.
Apply the patch only after a clean `git apply --check`; preserve independently
edited files and reconcile differences against the pinned base. Keep all existing
workflow stores and restart/reconnect rather than clearing them.
