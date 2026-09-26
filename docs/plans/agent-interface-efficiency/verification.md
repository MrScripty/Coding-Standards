# Agent Interface Efficiency Verification

Status: **Verifying**. The three implementation goals are complete with local
behavior evidence. Supported-environment, configured-client and independent-review
acceptance gates remain open. Baseline:
`34c2dcbaf9aa7ade5589ae5c88383719dda81200`; resulting interface: **39**.

## Scope and authority

Host-selected schema presentation, bounded exact route content, and typed
request-local evidence expansion compose the existing Engine owners. Native
application/authoring separation, evidence verification, immutable contexts,
explicit review, publication and recovery remain unchanged. No dependency,
normative-policy, approval, provenance, persisted-state or remote-publication
change is included.

The executable Router selected applicable implementation, verification, planning,
documentation, library, generated-contract, IPC, contracts, architecture, security,
diagnostics and performance guidance with no unresolved task facts. Source,
generated projections, affected consumers and fixtures were reviewed as one
coordinated change. See plan.md and ledger.md for admission and findings.

## Local verification results

| Evidence | Result |
| --- | --- |
| Engine test-method coverage, full selection plus corrected reruns | 406 observed passing methods |
| Final focused tests (included in Engine coverage) | 38 passed |
| Final generated-contract/main-advance consumers (included above) | 16 passed |
| Final single and batched publication/recovery scenarios (included above) | 4 passed |
| Contract/compiler package | 53 passed; 1 environment check skipped |
| Metadata, policy-impact, Analysis and verifier packages | 342 passed |
| Registered structural checkpoint | 121 checks across 73 suites passed |
| Generated-contract freshness and diff checks | Passed |
| Interface-38 records reopened under interface 39 | Exact Analysis/readiness preserved |

The complete original 405-test Engine selection ran in four file-disjoint shards.
It exposed six failing test methods (ten failure entries including subtests): four
publication scenarios expected interface 38, one consumer assumed the facade
always selected native rather than agent input roots, and one fixture committed a
fresh manifest without the corresponding new interface files. The Engine correctly
rejected that inconsistent tree. These test consumers were corrected without
weakening the production checks. All affected methods passed their final reruns.
One additional numeric-boundary test brings the current total to 406. This is
full-selection coverage plus targeted reruns, not a claimed single all-green full
suite execution. `DELIVERY/evidence/engine-test-coverage.json` lists every current
test ID and its observed pass; the initial logs are retained alongside reruns.

Review also found valid JSON Schema integers encoded as `1.0` were not usable
directly as Python slice indices. The route now normalizes validated whole counts
to integers. The final regression covers both purposes, offsets zero/one and
fractional rejection, matching the established workflow-detail convention.

## Measured interaction changes

Real cold MCP stdio calls, without a model turn, compared the same snapshot and
native Analysis/readiness identities. Every request used a replacement process;
no persistent connection cache or alias registry supplied the gains. Both schema
modes and purposes returned exactly the same policy reads as ordinary route plus
read_many. The two-policy scenario retained all eight unresolved routing questions.

| Measured workflow | Before | After | Result |
| --- | --- | --- | --- |
| Route and read two policies | 2 | 1 | Same exact content, reading plan and unresolved questions |
| Application route/read result JSON | 26,548 bytes | 26,078 bytes | 470 fewer bytes |
| Authoring route/read result JSON | 58,452 bytes | 57,972 bytes | 480 fewer bytes |
| Four explicit decisions plus three-owner review, request JSON | 8,582 bytes | 7,814 bytes | 768 fewer bytes; 8.95% reduction |
| Three-owner review alone, request JSON | 1,334 bytes | 1,038 bytes | 22.19% reduction |

Evidence-request measurements above use compatibility mode. Native mode gave the
same 768-byte reduction; synthetic topic labels differ across modes, so compare
within a mode rather than attributing that label difference to schema presentation.
The evidence scenario retains two explicit calls, identical Analysis/readiness and
2,085 result bytes. Review remains explicit and the trace stops before publication.
Each request binds its own table; reusing a previous request's alias is rejected.

Catalogs were measured as complete focused `tools/list` tool-array JSON using the
same serializer against the pinned baseline and final implementation:

| Catalog | Baseline bytes | Final bytes | Change |
| --- | --- | --- | --- |
| Authoring, compatibility (default) | 695,769 | 721,935 | +3.76% |
| Authoring, native (opt-in) | 695,769 | 616,282 | -11.42% |
| Application, either mode | 34,551 | 39,274 | +4,723 bytes / +13.67% |

The new compatibility catalog grows because it still carries the supported-client
workaround and must describe the added capabilities. Native authoring saves 79,487
bytes against the baseline, or 105,653 bytes against new compatibility. Application
schemas grow to describe exact routed content; choosing the smaller complete input
projection avoids artificial reference overhead. Identical application catalogs
correctly share their catalog digest across modes.

These are serialized JSON byte and deterministic tool-call measurements, **not**
model-token, billing, latency, memory or model-reliability guarantees. MCP
structuredContent and its matching JSON TextContent remain intact; the 2025-11-25
MCP tools specification recommends the text form for backward compatibility. The
trace asserts equality. Whether both copies reach a model depends on its actual
client and was not inferred here.

## Boundary and retained-state evidence

An actual interface-38 process created immutable Analysis and readiness records.
The interface-39 process reopened those exact records in the same disposable store,
then produced identical readiness using request-local evidence. No migration,
store deletion or publication occurred. Of 286 previous schema definitions, only
RouteCall and the two focused route-result definitions changed; the other 283,
including native authoring and retained-state definitions, are unchanged.

Tests cover independent Draft 2020-12 validation, recursion, closed fields, actual
catalog identity and purpose filtering; all pages and exact byte boundaries;
unavailable dependencies, source/lifecycle loss and cold continuations; missing,
unused and cross-request aliases, native uniqueness, foreign work, stale bytes,
unsupported providers, denied decisions, expanded batch limits and literal authored
content containing reference-like text. A separate omitted-snapshot reproduction
establishes one capture and one compiled-snapshot query in each purpose.

The explicit publication/recovery workflows passed final reruns for both single
and batched decisions, including interrupted publication observation, authorized
completion, normal publication and cold readback. These tests do not grant user
authorization or cause publication in the user's repository.

## Environment and acceptance gates

Local execution: CPython 3.13.5, Linux x86-64, jsonschema 4.26.0 and rpds-py
2026.5.1. The repository supports locked CPython 3.11/3.12 and pins rpds-py
2026.6.3. Local evidence does not replace that environment qualification. The lock
and existing CI workflow were preserved; the supported-environment check remains
explicitly skipped rather than reported as passing.

Run the locked CI checks and obtain independent review before acceptance.
Compatibility schema mode remains the default. Configured Codex and optional MCP
SDK clients are unavailable locally; the updated configured-client harness must
be run on the actual host before selecting native presentation for that deployment.
Its transport/schema checks alone do not certify model-visible rendering or model
behavior. The direct stdio evidence does not claim to execute either absent client.

Restart/reconnect for interface 39 and preserve stores and exact handles. Native
mode is explicitly selected with `--schema-mode native`; it is never inferred from
a client name. `DELIVERY/manifest.json` binds the changed files and base, and the
packaging check records reconstruction in `DELIVERY/reconstruction.json`. No changes
were pushed or merged remotely by this implementation.
