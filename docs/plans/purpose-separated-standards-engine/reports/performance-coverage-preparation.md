# Coverage preparation — implementation and evidence

Status: source implementation complete; focused source-subset evidence passed.
Full-checkout integration, supported-runtime measurements and independent review
remain pending.

Base: `implementation/purpose-separated-standards-engine` at
`5a9dcb08effda50a485e6ae08d9fe4c349c74eda`.

## Outcome and scope

Prepare each suite dependency projection once per validated, loaded manifest and
group policy relationships once per complete coverage compilation. Preserve every
suite fingerprint, coverage view, requirement identity, canonical manifest byte,
rejection and independent replay boundary. The production write set is confined
to Metadata's `suite_inputs.py` and Analysis's `coverage.py`. Four new test modules,
this report and a complete-checkout measurement runner accompany them.

This is shared preparation inside existing owners, not incremental manifest
construction or a second compilation cache. Public and persisted wire formats,
generated contracts, dependency locks, normative standards, authorization,
publication, accepted-base interpretation and Engine replay selection are unchanged.
The user's previous 121-test/64.8-second run and 8.2 seconds of verifier work are
context, not a measured baseline/candidate comparison for this increment.

## Implementation and ownership

### Manifest-owned dependency projections

`load_suite_input_manifest` retains its existing canonical-form, registry,
suite-definition, dependency graph, file digest, absence, use and index validation.
Its final all-suite derivation now uses one definition lookup and keeps the
resulting projections in a private read-only mapping. That mapping is attached
only after every derivation succeeds, before returning the validated manifest.
There is no partially published index or lazy mutation during later reads.

`SuiteInputManifest.dependency()` returns the prepared result for a loaded
manifest. Its original derivation body remains the computation for a directly
constructed manifest. Direct construction does not acquire authority from a
previous object. The private field is excluded from constructor arguments,
equality, hashing and representation; `as_projection()` and canonical serialization
retain their exact declared fields. `dataclasses.replace()` starts with no prepared
index, including when the replacement changes prerequisites or file material.
Unknown suite IDs retain `KeyError`. Each fresh load still reads and verifies its
supplied source; a previously retained object cannot authorize a corrupt reload.

The index has the same lifetime as its manifest. Existing compilation-cache
accounting traverses its slot, mapping and immutable result records before
retention. Lookup never expands the retained object graph. Existing cache limits
and overflow/eviction behavior remain unchanged.

### Compilation-local relationship grouping

`compile_coverage_definitions` initializes one edge-ID group per selected policy,
visits the semantics mapping once, and derives every policy view from that policy's
group. Unrelated sources are excluded, policies without edges still receive views,
and an empty policy corpus avoids the scan. This grouping is local scratch data,
not another retained index or a cross-compilation graph cache.

The public `derive_coverage_view` signature is unchanged. A standalone call still
selects from the supplied graph. Both standalone and bulk construction invoke one
private derivation helper, retaining sorted relationship processing, complete local
horizon membership, evidence-owner checks, semantic overrides and requirement
identity calculations. Authorization and repository coverage decision functions
are unchanged. No caller-provided filtered graph becomes a new public trust input.

## Verification performed

| Evidence | Observed result | Proof boundary |
| --- | --- | --- |
| New manifest regression module | 12 tests passed | Real source adapters, manifest validation, identity encoding and preparation in the recovered source subset |
| New coverage regression module | 12 tests passed | Actual coverage definitions/functions with synthetic already-compiled corpus/graph records and isolated imports |
| New accounting regression module | 2 tests passed | Actual existing `_retained_size` function applied to prepared manifests; not the full LRU workflow |
| Independent original-source comparison | 100 cases matched | Complete coverage material or complete structured rejection, using original and candidate function bodies on deterministic synthetic inputs |
| Removal-of-optimization probes | Both detected by assertion failures | Regression counters fail when original repeated scanning or uncached dependency lookup is restored |
| Python compilation and 3.11 grammar parsing | Passed | Syntax, not execution on CPython 3.11/3.12 |
| Two new full-checkout integration tests | Not run | Import fails on unavailable `tools.standards_applicability` before test bodies |
| Complete Engine compilation benchmark | Not run | Import fails on unavailable `tools.graph_engine` |

The 28 authored regression tests comprise 26 executed focused checks and two
pending integration checks. The independent comparisons are additional bounded
evidence, not 100 claims about the entire Engine. Their generator uses seed 73109,
0–12 policies, 0–7 edges per policy, shuffled relationship ordering, changed input
bytes and sampled missing-consumer/invalid-owner/missing-suite failures. Separate
focused tests cover diamond prerequisites, shared file uses, absence, repository
index changes, immutable lookup, parallel reads, replacement, corruption and
canonical serialization. Removing only the optimization makes the structural
regressions fail; these are not wall-clock assertions.

The integration tests use the existing real CoverageTest fixture. They cover the
loader-to-horizon-to-view path and persisted coverage claims across unrelated,
corrupt and coherently changed relevant inputs. They require execution in the
complete repository alongside the existing coverage, manifest, Engine/replay and
cache tests.

## Isolated performance observations

Seven alternating baseline/candidate pairs per workload follow one excluded
warm-up pair. Both sides use the same source bytes and synthetic compiled records.
The timed operation performs actual manifest loading/validation, coverage-horizon
construction and all coverage definitions. Fixture creation, result comparisons,
structural counters and memory observations are outside the timer.

All cases use five suites and four manifest file records, including a diamond
prerequisite graph, overlapping uses, an absent path and repository-index use.
Corpus and graph parser execution, complete authority compilation, persisted
proposal admission, MCP transport and the user's test selection are outside this
measurement. These are synthetic mechanism observations, not representative
Engine-latency or test-suite-speedup claims.

| Policies / relationships | Baseline median (range), ms | Candidate median (range), ms |
| --- | ---: | ---: |
| 1 / 3 | 1.279 (1.162–1.357) | 0.800 (0.757–0.988) |
| 32 / 256 | 14.765 (14.122–15.959) | 3.461 (3.185–5.066) |
| 128 / 1,536 | 75.952 (72.398–82.270) | 10.675 (10.016–11.946) |

Every paired complete coverage projection was exactly equal, including manifests,
all view fields, horizon members, dependency-derived requirements and requirement
IDs. For 128 policies, suite fingerprint computations fell from 1,034 to 5;
relationship passes from 128 to 1; and relationship visits from 196,608 to 1,536.
The deciding result is reduced repeated work without reduced coverage scope.

The private index adds storage to a standalone loaded manifest. Sharing the same
fingerprint strings can also reduce duplication in the final coverage output.
Existing conservative accounting measured the 128-policy result at 560,420 bytes
before and 532,940 bytes after; the one-policy result increased from 10,983 to
11,951 bytes. These are fixture-specific reachable-object counts, not process RSS
or a universal memory saving. Separate tracemalloc observations and all raw timing
samples are retained in the delivery evidence.

## Source and environment limits

Direct clone/archive acquisition was unavailable. Complete replacement files were
recovered from the GitHub connector and verified against the exact upstream Git
blob identities: Metadata `7db6e020de046502a7cbc159832ccc6312e75a5e` and Analysis
`1363572e6056184d020139f3316f191bf28fa500`. Supporting source modules were likewise
checked, and the unchanged portions of both edited modules were compared as ASTs.
This establishes the patch bases, not a complete local repository.

Execution used CPython 3.13.5 on Linux, outside the repository's declared 3.11/3.12
qualification. Metadata tests execute actual source/identity modules. For coverage,
the delivery-only loader excludes imports from unavailable parser/graph/trust
packages while executing unchanged production definitions and function bodies;
fixtures explicitly supply the already-compiled structural inputs. The accounting
checks execute the existing accounting function extracted from its module. The
loader is retained as evidence and is not installed into the repository. It does
not provide parser, authorization, package-initializer, snapshot-store, publication
or full-cache integration evidence. The first manifest test run exposed a fixture
expectation difference in Python 3.13's exception class for replacing an `init=False`
field; the assertion now accepts the supported exception families while requiring
rejection. Both logs are retained.

The owning generated `suite-inputs.json` is intentionally unchanged in this ZIP.
Refresh it through the Engine after applying/staging the eight intended repository
files in a full checkout. Generating it against the partial source/index here
would not establish canonical freshness. No remote branch, accepted main, user
store or installed configuration was changed.

## Complete-checkout acceptance and reproduction

Use the supported locked environment, review the patch and stage its intended
write set. Refresh the generated input manifest through its owner, inspect the
reported outcome/diagnostics, and review/stage that generated change:

```bash
printf '%s\n' '{"kind":"verify-repository","refresh_verification_inputs":true}' |
  PYTHONPATH=. python3 -P .agents/skills/standards-engine/scripts/invoke.py verify_repository
```

Run the new focused and integration tests:

```bash
PYTHONPATH=. python3 -m unittest \
  tools.standards_metadata.tests.test_prepared_suite_dependencies \
  tools.standards_analysis.tests.test_coverage_preparation \
  tools.standards_analysis.tests.test_coverage_preparation_integration \
  tools.standards_engine.tests.test_coverage_preparation_accounting
```

Run the affected existing Metadata, Analysis and Engine tests, including manifest
corruption, coverage receipt/revocation, independent replay and retention/eviction
coverage. Repeat the repository verifier without refresh to establish freshness.
Keep the same selection and environment when comparing the previously reported
121-test turnaround; no corresponding reduction is promised here.

The [complete-compilation runner](performance-coverage-preparation/measure_coverage.py)
reads one explicit complete corpus into an exact frozen source and measures full
`StandardsEngine._compile()` calls. Use the same stable corpus for both installed
implementations, alternate process order across repeated comparisons, and retain
all observations. The script also records source/package identities, workload
size, dependency-fingerprint counts and current cache accounting. Compare timings
only when `input_sha256` and `coverage_output_sha256` match. It checks full semantic
signature stability within each run and complete coverage material across runs;
it does not time revision admission or transport.

```bash
python /absolute/candidate/docs/plans/purpose-separated-standards-engine/reports/performance-coverage-preparation/measure_coverage.py \
  --source /absolute/baseline --corpus /absolute/fixed-corpus --output /tmp/coverage-baseline.json
python /absolute/candidate/docs/plans/purpose-separated-standards-engine/reports/performance-coverage-preparation/measure_coverage.py \
  --source /absolute/candidate --corpus /absolute/fixed-corpus --output /tmp/coverage-candidate.json
```

Complete acceptance remains contingent on these real-checkout tests, representative
operation measurements and independent review. The implementation and isolated
reduced-work/equivalence evidence are available now; stronger claims are not
inferred from them.
