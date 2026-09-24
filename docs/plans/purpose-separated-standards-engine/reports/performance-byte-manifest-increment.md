# Compact bytes and source-based manifests — implementation and evidence

**Status:** implemented and locally qualified; supported installed qualification and independent review are separate.

**Branch:** `implementation/purpose-separated-standards-engine`  
**Base:** `2aef993edc8a47ce474468c641cc2e542e3ec8da`  
**Tested implementation commit:** `de85f5adfda221fe88fbf0dba12b34aa2e410cf6`  
**Evidence date:** September 23, 2026 (America/Vancouver).

## Objective and bounded admission

Implement the next measured opportunities from the bounded investigation: cheaper
exact-byte identity computation, suite-input manifest construction without an
intermediate filesystem/Git repository, and explicit snapshot reuse within one
publication test's unchanged-revision intervals. The [admission](performance-byte-manifest-increment/admission.md)
records responsibilities, write scope, preserved guarantees and the deciding evidence.

Applicable guidance was Core, the selected Performance, Verification and oracle
rules, Development Proportionality, Architecture and immutable replay, Contracts,
Implementation, Commit and Documentation. This is code and implementation evidence;
normative standards, operational prompts/templates, public Engine wire schemas,
persisted formats, dependency locks and the installed configuration are unchanged.
The existing plan is not relabeled as globally accepted by this report.

## Implemented design

### Identity-owned compact storage and exact encoding

`standards_identity.IdentityArray` retains exact immutable `bytes` directly.
Other iterables retain validated tuple construction. The public `values`
observation, sequence equality, hash and representation remain tuple-based;
observing the tuple explicitly may allocate it. Compact storage changes an internal dataclass layout; serialization continues through the canonical Identity encoder, not dataclass introspection. Byte subclasses and mutable
iterables still use the generic validation/copying path. Raw bytes do not become
a new top-level IdentityValue variant.

The encoder emits the same decimal integer-array preimage, using the existing
256 decimal tokens in 64 KiB input chunks. This bounds per-byte join scratch,
not total output memory: the public encoder still returns complete encoded bytes.
Path ordering, Unicode, escaping, arbitrary-size integers, domain/prefix/length
framing and complete SHA-256 verification are preserved. The implementation
removes millions of unnecessary generic validation/dispatch calls rather than
trusting a stored digest or retaining a cache across operations.

### One manifest compiler with explicit input adapters

The Verifier now distinguishes declaration input (`CheckInputContext`) from
physical check execution (`CheckContext`). `SuiteInputSource` provides the small
input surface actually required by declaration discovery: exact bytes, explicit
membership, repository-index observation and local link resolution.

`DirectoryInputs` retains real-file containment, symlink handling and candidate
membership observations. `FrozenInputs` consumes the existing FrozenContentSource
and an explicit normalized regular-file inventory. It separates an indexed file
from captured bytes: unused uncaptured files are valid membership, while every
consumed file needs actual bytes. Missing bytes produce `INPUT.UNAVAILABLE`;
conflicting file/directory membership is invalid. An empty file is present only
when real empty bytes were supplied and receives the actual empty-content digest.

Both adapters feed the same check-owned declarations and manifest compiler.
Config, tables, package manifests and policy-impact declarations use that input
surface for discovery. Markdown retains universal-newline parsing while file
digests continue to bind original bytes. Declaration-only dependency validation
uses symbolic graph IDs with explicit empty artifact membership, eliminating
ambient host-file alias discovery. The generic graph engine is unchanged.

The exported `suite_input_projection_bytes_from_content` lets Engine logical
authoring pass its already-known content and computed candidate inventory to
that compiler. The removed bridge previously touched every proposed path,
wrote captured material, initialized/staged a temporary Git repository and
removed it afterward. None of those temporary steps is required now.

Actual check execution, package subprocess validation, physical candidate
verification, Git publication and recovery still operate on real checkouts.
Filesystem and frozen interfaces are both current consumers of one compiler;
there is no second serializer, compatibility branch, selective verification,
new database, cross-call cache or transport-lifetime change.

### Narrow test-workload correction

The coordinated publication/provenance test now supplies the returned snapshot
for reference, prompt/template and repeated content reads intended to observe the
same accepted revision. The provenance-only proposal explicitly uses that same
base. Fresh capture is retained before publication and after each publication,
as are assertions that the later snapshots differ. Historical provenance,
unchanged normative bytes/revisions and application exclusion assertions remain.
Independent implicit-capture, main-advancement, replay and recovery tests remain.
This changes the test workload, not the runtime meaning of an omitted snapshot.

## Same-corpus performance

Three serial baseline and candidate sweeps used the same executable, dependency
set, host and fixed fixture source at `2aef993e`. All observations used
435 captured files, 3,738,522 source bytes,
and the same content identity. Facade creation, initial capture and fixture setup
were outside these operation timings. Final comparisons ran after all package
qualification; no package test process ran concurrently.

| Operation | Baseline median | Candidate median | Speedup |
| --- | ---: | ---: | ---: |
| content_identity | 0.612 s | 0.148 s | 4.14x |
| read | 0.852 s | 0.362 s | 2.35x |
| propose | 1.810 s | 0.850 s | 2.13x |
| manifest_refresh | 0.653 s | 0.159 s | 4.11x |

`manifest_refresh` is an inclusive subspan of `propose`; these rows must not be
added. Three samples establish medians/ranges, not p95/p99 or deployment SLAs.
The [comparison CSV](performance-byte-manifest-increment/comparison.csv) and raw
[baseline](performance-byte-manifest-increment/final-baseline.json)/[candidate](performance-byte-manifest-increment/final-candidate.json)
records retain CPU, spans and exact input bindings.

### Identity and memory evidence

Both implementations emitted 13,137,463 encoded preimage bytes:

- Preimage SHA-256: `b2669faaace40e7b8a3003a1d13527a2f1c410a78caee7723eef1db46cb2ba5d`.
- Content ID: `snapshot-content:sha256:2a1b789a3d20e26d4d2dd96ecf11476e3f1b968a104655c701633ed2f7496378`.

A separate complete-identity tracemalloc probe measured peak traced allocation
of **77,203,351 bytes before** and **26,729,514 bytes after**,
a **65.4% reduction**. This is Python
traced allocation during that operation, not process RSS or all native memory.
Its instrumented duration is not used in the latency comparison. Whole encoded
output and final frame allocation remain proportional to the input representation.

### Publication workflow: runtime versus test-only changes

One serial run per combination used the same committed fixture source. Runtime
imports and test-file selection were independently selected. Physical publication
checkpoints exercised that same fixture candidate; complete final-candidate
qualification below separately covers the changed repository source.

| Combination | Test body | Snapshot publications | Complete checkpoints |
| --- | ---: | ---: | ---: |
| Baseline runtime / original test | 100.516 s | 10 | 2 |
| Candidate runtime / original test | 62.507 s | 10 | 2 |
| Candidate runtime / explicit-snapshot test | 51.251 s | 4 | 2 |

The first comparison isolates runtime changes while preserving the original
test and assertions. The third also includes the reviewed snapshot-reuse change.
Both actual publications and their complete checkpoints remain in every run.
These are single-workflow observations, not a suite-wide speedup estimate or a
prediction for the user's seven-minute development-machine run.

## Correctness and standards-consistency evidence

Five new Identity tests cover all 256 byte values, empty content, chunk boundaries,
large arrays, immutable observation, mutable/subclass input behavior, Unicode
path ordering, arbitrary integers and exact independent preimage/digest oracles.
Construction and encoding counters verify that byte payloads bypass generic
per-element work without bypassing validation of surrounding values.

Twelve new Verifier tests compare filesystem/frozen manifests and diagnostics,
including actual registered check populations, empty/missing data, malformed
configuration, UTF-8 and newline semantics, escaping links, directory inputs,
contradictory declarations, index errors and real symlink containment. One new
Engine regression runs logical projection while temporary staging and subprocess
creation are forbidden. Existing mutation, purpose, integrity, head, authorization,
publication and cold-recovery assertions are retained.

A separate full-corpus comparison reproduced the baseline manifest's exact
406,921 bytes with SHA-256
`2b7979b930bac05dabc5eab2547f81d3e618d3fae49962cbfa093f2440c7ad63`.
It consumed 417 declared content inputs against 1,165 repository paths, while
filesystem content reads, ambient existence queries, subprocess runs and
TemporaryDirectory creation were blocked during frozen compilation. See
[manifest equivalence](performance-byte-manifest-increment/final-manifest-equivalence.json).

Membership alone now yields a typed unavailable result when consumed bytes are
missing, rather than inheriting the removed bridge's touched empty file. This is
an explicit validity improvement, not a claim that invented empty content and
unavailable content have identical outcomes. On complete equivalent material,
manifest bytes, membership, declarations and content digests agree.

The design localizes each decision: Identity owns representation; the Verifier
owns declaration discovery and manifest compilation; each source adapter owns
its input guarantees; Engine composition supplies exact candidate material;
physical verification retains its own authority. Removing the new input seam
would put filesystem materialization back into logical authoring. It contains
an independently meaningful existing responsibility rather than speculative
reusability. Review refined symbolic graph isolation and newline parity before
the final run; interrupted intermediate runs are not counted as qualification. A completed first pass found a test-only handle-field error; the test now uses the existing provenance result `authority` field. The final full pass below includes that correction.

## Local qualification

The committed implementation `de85f5ad` ran **178 Engine
tests in one serial unittest process**, with return code zero. The eleven
supporting package suites ran **438 tests**, with
**1 existing interpreter-dependent skip**.
Combined: **616 tests run, 615 passed, 1 skipped**.
Test outcomes and commands are in [verification](performance-byte-manifest-increment/verification.json).
Full process elapsed time includes imports; unittest-reported duration is
recorded independently. No full-suite baseline/candidate speedup is claimed.

The structural checkpoint ran separately and passed **73 suites / 121 checks**.
Generated manifest publication uses the existing Engine owner. The final delivery
also runs this checkpoint after the evidence-only commit. These checks validate
structure/freshness, not prose quality or independent implementation review.

The source checkout preserves its existing accepted `main`. Disposable test
clones give the exact candidate their own local accepted `main`, as required
by PURPOSE-SEPARATION.md. [Source binding](performance-byte-manifest-increment/source-binding.json)
identifies tested implementation hashes; the later evidence commit changes
reporting and derived index evidence rather than production Python. Changed
Python also parses with the 3.11 grammar; grammar acceptance is not execution.

## Qualification limits and handoff

The isolated local runtime is Python 3.13.5, outside the declared 3.11/3.12
range. It uses the same executable binary and core dependencies for both sides;
rpds-py 2026.5.1 differs from locked 2026.6.3. Optional rich-environment packages
were not imported. The dependency lock and supported range remain unchanged.
See [environment](performance-byte-manifest-increment/environment.json).

The official SDK/configured Codex client and an independent reviewer were not
available for this increment. Local native/CLI/MCP, real Git/SQLite publication
and recovery tests are evidence of their actual claims, not substituted installed
qualification. Run the supported locked qualification and relevant client checks
before installed acceptance. No user store, archived proposal, Codex configuration,
remote branch or real accepted-main ref was changed.

Use one delivery method in APPLY.md. The incremental bundle preserves actual
Git CLI commits; the patch reproduces the same final tree. The delivery manifest
records exact base/result commits, modes, file hashes and any removals.

## Reproduction

Use separate implementation checkouts at the base and candidate plus one fixed
fixture checkout of `2aef993e`, with its own local main at that base. Execute the
same Python/dependencies serially:

```bash
python measure_increment.py --source /path/to/base --fixture-source /path/to/fixture --output baseline.json --repeats 3
python measure_increment.py --source /path/to/candidate --fixture-source /path/to/fixture --output candidate.json --repeats 3
python measure_publication.py --source /path/to/base --fixture-source /path/to/fixture --test-source /path/to/base --output publication-base.json
python measure_publication.py --source /path/to/candidate --fixture-source /path/to/fixture --test-source /path/to/base --output publication-runtime.json
python measure_publication.py --source /path/to/candidate --fixture-source /path/to/fixture --test-source /path/to/candidate --output publication-reused.json
```

The [operation driver](performance-byte-manifest-increment/measure_increment.py)
and [workflow driver](performance-byte-manifest-increment/measure_publication.py)
write only disposable fixtures and selected evidence files. Required publication
checks remain active. Use the recorded commands in verification.json for full
package populations; retain the separate structural result.
