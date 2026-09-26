# Input Contract Discovery Verification

**Status: Verifying.** The implementation and local checks are complete. Actual
client/model qualification, supported-runtime CI for the new diff, and independent
review remain open. Base: `190491fb36314624aec74946f58fd0f61f852a60`.
Resulting Engine interface: **40**.

## Implemented behavior and ownership

One flat read-only `describe_input` operation exposes exact input contracts for
operations in the running purpose/catalog. It uses the active compiled interface
and the existing catalog digest. A selected definition is visible only through
that operation's input-reference closure. It does not open the standards store,
capture a snapshot, read Git, authorize a decision or alter a workflow.

Each response carries exact schema documents as `schema_json` strings, definition
names, root/selection, dialect, interface/catalog identity, counts and any next
request. Schema documents are result data, not a new string-based mutation API.
The canonical validator still owns instance semantics. The contracts package's
structural iterator owns reference discovery and leaves literal/default/enum data
unchanged. The service owns only selection, deterministic breadth-first ordering
and whole-record pagination.

Pages default to eight records and permit at most sixteen; the complete domain
result JSON is bounded at 16 KiB. Byte pressure returns fewer whole records, and an
oversized record returns an explicit unsupported outcome rather than partial text.
Every selected/nonzero-offset request requires the original catalog digest. A
changed catalog rejects the request; an input-only closure cannot expose another
purpose's private operations or output definitions.

Guidance is generated for every published tool, not a special list of authoring
operations. Both purposes and schema modes retain their scope. CLI/direct-facade
observers describe their full operation surface; MCP describes its actual focused
or advanced catalog. Identities are intentionally scope-specific. All old mutation
input/output declarations are unchanged. Compatibility remains the default.

## Automated evidence

| Check | Result |
| --- | --- |
| Current Engine test-method coverage | 437 distinct current IDs observed passing |
| Complete initial Engine selection | 435 tests, four file-disjoint shards; three stale catalog assertions identified |
| Final integrated discovery/consumer rerun | 72 passed; included in the 437 IDs |
| New discovery / real workflow / qualification-checker tests | 22 methods; included above |
| Contracts/compiler package | 61 passed; one environment check skipped |
| Metadata / policy-impact / Analysis / verifier packages | 43 / 10 / 121 / 168 passed (342 total) |
| Complete registered structural checkpoint | 121 checks across 73 suites passed |
| Generated-contract freshness and diff checks | Passed |
| Interface-39 to interface-40 cold observation/review | Exact Analysis/readiness, review and main preserved |

The initial Engine run exposed three test consumers that explicitly enumerated
the old application tool set. Those assertions now include only the new read-only
operation in addition to the prior set; private-authoring exclusions and actual
denial tests remain. The affected consumers passed their reruns. Two extra checker
regressions were then added. This is complete-selection coverage plus final reruns,
not a claimed single uninterrupted all-green 437-test execution.

The first auxiliary-package invocation omitted their package-local test-helper
search paths. It was corrected and both affected packages rerun successfully; no
production code was changed to work around those invocation errors. One early
standalone workflow invocation was interrupted by the execution tool's call limit;
the same test completed in the full Engine selection and the final integrated
rerun. Raw initial logs and successful results are retained in delivery evidence.

Discovery tests reconstruct every published input closure in both purposes and
modes and compare it directly with the canonical definitions. The independent
Draft 2020-12 validator accepts valid examples and rejects malformed inputs. Tests
cover nested evidence/decision variants, recursive expressions, literal `$ref`
data, exact byte boundaries, numeric representations, terminal pages, stale
catalogs, off-purpose/unpublished operations, selectors outside input scope, cold
continuations and no-store/no-filesystem observation after construction. A key-order
regression proves equivalent catalogs produce identical pages.

A real disposable workflow obtains its schemas through MCP discovery, proposes and
revises a candidate, resolves one decision and a multiple-decision batch, and
reviews to readiness in both modes. Shared and inline evidence produce identical
Analysis/readiness results. Main remains unchanged. This deterministic test uses
fixture-authored inputs; it is not substituted for model-visible qualification.

## Actual-model qualification support and limits

`tools/standards_engine/tests/codex_discovery_client.py` is an opt-in actual-model
harness. It requires `--allow-model-turn`, an explicit model/surface and a new private
evidence directory. It creates a disposable repository, a run-owned MCP registration
and an empty client working directory. Other MCP servers must be disabled before a
model turn starts. Source configuration and production stores are not changed.

The model receives semantic task intent and real fixture evidence, not prefilled
calls or schema/example files. It must discover and use all five authoring
operations, preserve the isolated write set, batch ready decisions, reuse evidence
and stop at readiness. The checker evaluates observed tool events, validates exact
retrieved records and arguments, requires every used named definition to have been
retrieved before its call, rejects repairs/outside tools, checks exact content and
revision readback, and verifies that main was not published. Unused union alternatives
need not be read. Branch selection uses the independent validator; the checker does
not implement a replacement production validator.

Checker tests are synthetic event tests only. Their passing results are not a model
run. The raw configured-client harness also exercises discovery but deliberately
remains a no-model catalog/navigation check. **Neither actual Codex harness was run
here: the executable/authenticated user client is unavailable.** The source-level
protocol adapter was checked against the published rust-v0.157.1 app-server types;
that is not execution qualification of any installed client/version.

Read `tests/INPUT-DISCOVERY-QUALIFICATION.md` for commands and acceptance requirements.
A successful fixture run is behavioral evidence for that particular client/model
and exposure surface; it does not claim all rendered TypeScript fields stop showing
unknown. Compatibility retirement still needs accepted direct/discovery access for
every supported deployment and integration review.

## Measured costs

Measurements use the same JSON serializer on the exact baseline and current
catalogs. They describe serialized JSON, not model tokens, billing or latency.

| Focused catalog | Baseline bytes | Updated bytes | Change |
| --- | --- | --- | --- |
| Authoring / compatibility | 721,935 | 728,810 | +6,875 (+0.95%) |
| Authoring / native | 616,282 | 623,157 | +6,875 (+1.12%) |
| Application / either mode | 39,274 | 44,388 | +5,114 (+13.02%) |

The catalog now contains 21 focused authoring tools and eight focused application
tools. The discovery input is **787 JSON bytes**, with only string/integer fields
and no nested union. Actual model-visible rendering of this input remains a host
qualification item rather than an inferred guarantee from its size.

| Discovery selection | Default-page calls | Result JSON bytes | Definitions |
| --- | --- | --- | --- |
| First propose overview only | 1 | 4,083 | First 8 of 66 |
| RevisePolicyUnitEdit selected closure | 1 | 1,908 | 6 |
| AgentImpactDispositionSubmission selected closure | 2 | 4,797 | 13 |
| AgentReviewCall complete closure | 2 | 4,853 | 16 |

The first overview intentionally reports remaining definitions. Selected closures
avoid unrelated edit alternatives, but other fields needed by a request may require
additional selections. `limit: 16` can obtain the measured 13- and 16-definition
closures in one call when byte pressure permits. Exact discovery results may be
reused while the catalog matches and the agent retains them in context. Discovery
is not prescribed before every production mutation.

## Retained state and compatibility

A comparison of canonical sources finds **312 unchanged previous definitions**, four
new discovery definitions, and one added operation. No prior operation declaration
changed. Analysis request 6 / state projection 7 and all handle, readiness, recovery
and SQLite representations remain unchanged.

An actual baseline interface-39 process created Analysis/readiness in a disposable
store. A new interface-40 process reopened the exact same records and repeated
review with the same evidence. Status values, readiness and main matched without
migration or store deletion. Discovery selections are catalog-bound observations,
not persisted workflow identities.

Local environment: CPython 3.13.5, jsonschema 4.26.0, rpds-py 2026.5.1 on Linux. The
repository supports locked CPython 3.11/3.12 with rpds-py 2026.6.3. The lock was not
changed. Baseline CI run 36268374875 succeeded under the supported environment, but
that does not qualify this new diff. Run its locked CI and independent review before
acceptance. No remote pushes, merges or production publication were performed.

## Delivery

The archive contains complete changed files, a base-pinned patch, file hashes/modes
and the verification logs. `DELIVERY/reconstruction.json` records fresh-base patch
reconstruction and byte/mode equality. Follow `DELIVERY/README.md`; apply the whole
coordinated patch, including new files and generated inputs, then restart/reconnect
for interface 40. Preserve all existing stores and workflow handles.

## Local integration qualification — 2026-09-26

Applied the archive patch to its exact base and verified all 35 delivered file
hashes and Git modes before adding the integration notes. CPython 3.12.3 with all
dependencies at the requirements.lock versions passed 62 contracts tests without
skips, 43 metadata tests, 10 policy-impact tests, 121 Analysis tests and 168 verifier
tests. Generated-contract freshness and all 73 registered structural suites passed.
Engine suite results are recorded in the execution ledger.

Qualification used a disposable clone of the exact base with the complete patch
staged. This preserves the user's pre-existing deleted tracked ZIP while allowing
publication fixtures to copy the full tracked tree. The delivery ZIP and unrelated
deletion remain outside the integration commit.

An independent comparison confirmed all 312 previous schema definitions and every
existing operation declaration are unchanged. A fresh stdio process launched with
the user's configured native-mode command reported interface 40, a current
installation and 21 tools. Discovery of propose returned the expected AgentProposeCall
root, eight complete records and a catalog-bound continuation over 66 definitions.
The native-mode host configuration was preserved.

These local supported-runtime checks do not claim a CI run or actual-model
discovery qualification. The opt-in model harness was not run during integration;
the configured session must reconnect before using interface 40. Independent review
and compatibility-retirement acceptance remain separate gates.
