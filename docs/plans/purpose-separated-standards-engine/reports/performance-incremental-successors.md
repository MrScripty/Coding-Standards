# Incremental successor construction

Status: implementation delivered; repository-level qualification remains blocked.

Base: `implementation/purpose-separated-standards-engine` at
`2e034f5dcc10bdd97e0d9b21e1edc6672f80c996`, tree
`09c605b62b0ed236fae0d90743131d28a738207e`.

## Outcome and scope

Construct an appended logical proposal revision from an eligible verified prefix
instead of reexecuting all earlier edits. Preserve the original accepted base,
complete final compilation and cumulative review/analysis inputs. This increment
changes neither public/persisted contracts nor review, application or recovery
replay authority. Schema-directed decoding and ordinary reads are outside scope.

The structural claim is one newly executed edit/change set and its required
manifest refresh for a simple one-edit append, independent of the number of
retained preceding change sets. The end-to-end claim is reduced native
`AgentToolFacade.revise_proposal` latency with a warm exact predecessor at
histories of 1, 4, 12 and 32 change sets. No numeric speedup or constant-time
request claim is made. Exact program matching, final compilation, complete
analysis, original-base verification and retention accounting still scale with
their relevant material.

The user's existing cold-reconstruction evidence motivates this scope; it is
not a baseline measurement of revision admission. This delivery does not present
that earlier measurement or focused-test duration as a measured successor speedup.

## Implementation

`projection_continuation.py` owns immutable computation input/material matching.
Its two small records carry original frozen base bytes, original snapshot identity,
complete original repository membership, canonical strings for every prefix
change set, installed compiler identity, projected bytes and projected membership.
Exact value equality, not a claimed revision hash alone, determines eligibility.
The strings snapshot authored data rather than retaining caller-owned nested edit
maps. Provenance has no disk format, public handle or independent retention owner.

`LogicalAuthoringCompiler.compile` accepts an optional predecessor. It verifies the
original base/borrowed compiled base as before, admits only a strictly shorter
exact prefix with matching material and recipe, and copies the predecessor file
table. Every value remains an immutable byte string. Each remaining change set
runs the existing edit, supporting-content, no-effect and manifest logic. Invalid
suffixes propagate their original failures and cannot mutate a sibling or prefix.

All suffix edit semantics and manifest membership arithmetic still use the
original base. The final candidate is always compiled. Final standard-successor
validation, semantic proposals, affected-policy selection and affected-module
selection all receive the complete logical program, original base and final
candidate. Provenance is returned only after those stages succeed. No earlier
proposal becomes an accepted standards baseline.

The compiler applies the same function/closure and exact-owner eligibility rule
previously enforced by the shared cache. Stateful/instance adapters stay on full
replay. This is the existing installed pure-compilation contract, not a claim
that Python function introspection can prove the absence of mutable global state.

`ProposalMaterials` offers its last projection during the current composed
operation. `CompiledSnapshotCache` can borrow the exact immediate predecessor of
the same proposal from its existing entries on an exact-successor cache miss.
It introduces no secondary cache, persistent checkpoint, search index or retained
history chain. The existing two-entry / 32 MiB limits charge the new provenance as
part of the same retained object graph. Budget pressure affects reuse, not meaning.

The engine's existing `reuse` boundary gates both strategies. Its independent
projection path ignores even an explicitly supplied predecessor. Stored revision
reads, authorization, snapshot lifecycle, proposal heads and conditional
publication remain outside this pure optimization and execute through their
existing owners. Failure to publish a prospective projection does not make its
handle accessible as a stored revision.

A new/cold native revision admission replays the full program. A cold focused
workflow can first reconstruct the predecessor during preflight and then continue
from that operation-local material; it still pays for the initial reconstruction.
After eviction, restart, changed input, changed compiler, absent provenance or
unmatched material, complete replay remains the supported computation.

## Deciding evidence and its limits

| Evidence | Result in this delivery | Claim actually covered |
| --- | --- | --- |
| `test_projection_continuation` | 12 tests passed | Exact prefix/input/material matching and immutable records |
| Isolated actual-owner control-flow harness | 11 checks passed | Real compiler/cache/material-owner/reuse-gate control flow with simulated domain collaborators |
| Python syntax compilation | Passed for changed source, tests and measurement runner | Syntax only; not full package import, typing or domain correctness |
| Focused real repository tests | Blocked before test-body execution | Missing source dependencies in the recovered checkout |
| Representative 1/4/12/32 successor latency | Unavailable; runner supplied, no observations recorded | No end-to-end performance claim accepted |
| Complete verifier and generated input refresh | Not run; full checkout required | Generated manifest freshness remains pending |

The isolated harness loads the actual compiler, cache, operation owner and private
engine reuse gate definitions from the edited source. It substitutes the absent
content-source, authority compiler, edit, manifest and durable-revision collaborators.
Its checks show suffix-only execution at 1/4/12/32, final compile/analysis invocation
with the original base and full program, byte-table equivalence under that simulated
model, invalid/no-effect suffix handling, copy isolation, changed-input fallback,
cache lookup/eviction/accounting, operation-local handoff and the independent replay
gate. It supplies no real policy-graph, database, authorization, publication,
physical-candidate or latency evidence. The harness is retained as delivery evidence,
not installed as an alternative production implementation or permanent suite oracle.

Real integration regressions were added to the existing owners' test modules:

- Logical compiler: exact output and one-refresh continuation at growing histories;
  cumulative original-base semantic revision and relationship/module selection;
  mixed edits, multiple suffix sets, removals, invalid final successors; no-effect
  and invalid suffix rejection; changed program, snapshot, recipe and output material.
- Proposal/cache workflow: native warm admission, new-cache and eviction replay,
  fresh original-base/stored-revision reads, invalid suffix/stale head rejection,
  unchanged older revisions, and cumulative review obligations compared with a
  fresh cache-free engine after continuation.
- Nested material owner: suffix-only in-operation construction with no process
  cache, and the existing reentrant observer forwards the new internal argument.

Existing corruption, lifecycle, authorization, failed-publication, review, capture,
application-purpose and restart tests remain required alongside these regressions.
None of the real integration checks above is reported as passing here.

## Source and environment limitation

The GitHub connector confirmed the pinned branch and supplied inspected source.
Direct repository cloning was unavailable. Prior user-owned delivery archives
provided exact replacement sources; their result tree matches the pinned branch.
Every changed existing-file base was checked against that delivery's recorded
SHA-256 or, for the logical compiler test file, the current GitHub blob SHA.
This establishes the update's existing-file bases, not a complete local checkout.

The recovered subset lacks, among others,
`tools.repository_git.repository_git.errors` and the `tools.standards_analysis`
package. The baseline logical-authoring test import failed on the former. The
candidate focused test imports failed on those same missing dependencies, before
real test-body execution. Logs accompany the delivery. The local Python runtime
is 3.13; no qualification against the repository's complete locked environment
was possible. No upstream commit, branch or authoritative store was modified.

The canonical generated `suite-inputs.json` was deliberately left unchanged:
regenerating it against this incomplete source/index would produce an invalid
substitute. After applying and staging the source/test changes in the full
repository, use the owning Engine refresh command before integration verification.
The delivery is not merge-accepted while that gate and the real tests are pending.

## Reproduction in a complete checkout

Use the repository's locked Python environment. Review and stage the intended
source, tests and documentation. Refresh the owned generated manifest:

```bash
printf '%s\n' '{"kind":"verify-repository","refresh_verification_inputs":true}' |
  PYTHONPATH=. python3 -P .agents/skills/standards-engine/scripts/invoke.py verify_repository
```

Inspect `verification.passed` and all diagnostics, then review/stage the generated
manifest. Run the focused regressions:

```bash
PYTHONPATH=. python3 -m unittest \
  tools.standards_engine.tests.test_projection_continuation \
  tools.standards_engine.tests.test_logical_authoring \
  tools.standards_engine.tests.test_proposal_reuse \
  tools.standards_engine.tests.test_nested_materials
```

Run the existing full engine/verifier suites to cover independent review,
publication, recovery, lifecycle and capture boundaries, and repeat the verifier
without refresh to establish freshness. The structural counters and equivalence
assertions are required; a passing wall-clock threshold is not substituted for them.

### Successor-admission measurements

The [measurement runner](performance-incremental-successors/measure_successors.py)
prepares one disposable full repository fixture with exact current heads at 1, 4,
12 and 32 change sets. Every timed sample uses a private SQLite backup of its
unchanged seed. It warms the exact predecessor, then times only the native
`revise_proposal` request through validation and conditional admission. Preparation,
warm-up reads and independent final-material comparison are outside that timer.

The runner records wall and CPU time, executed edits, manifest refreshes, authority
compiles, original-base loads, cache accounting, request/result/material digests,
Python/platform/package information, installed source hashes and source status.
It requires exact one-edit/one-refresh continuation (or history-plus-one for full
replay) on this simple workload and independently compares final material through
the existing full-replay boundary. It rejects divergent outputs rather than
reporting an optimized but different result. Iteration zero is explicitly warm-up;
all subsequent observations are retained, including slow samples.

Use a clean complete source revision for preparation. Keep that accepted-base
fixture fixed when comparing baseline and candidate installed implementations.
For a same-candidate comparison, `--strategy full-replay` disables only the internal
continuation match, preserving exact-read caching and final compilation. For the
unmodified pinned baseline, pass its checkout with `--source` and the same prepared
fixture; the runner also supports that source without the continuation module.

```bash
SCRIPT=/absolute/candidate/docs/plans/purpose-separated-standards-engine/reports/performance-incremental-successors/measure_successors.py
python3 "$SCRIPT" --source /absolute/baseline --fixture /tmp/successor-fixture \
  --prepare --output /tmp/successor-prepared.json
python3 "$SCRIPT" --source /absolute/baseline --fixture /tmp/successor-fixture \
  --strategy full-replay --output /tmp/successor-baseline.json
python3 "$SCRIPT" --source /absolute/candidate --fixture /tmp/successor-fixture \
  --strategy continuation --output /tmp/successor-candidate.json
```

Compare only matching `workload_sha256`, per-history `request_sha256`,
`result_sha256` and `projection_sha256` values. Retain the host CPU/resource limits
and storage facts with the evidence; platform strings alone do not qualify hardware.
Alternate run order when repeating comparisons. Report per-history distributions,
median and range for non-warm-up samples, rather than promising a speedup from a
single sample. Increase repetition when variability obscures a decision. This
native-admission measurement does not measure an entire interactive editing session.

## Remaining acceptance

Close qualification only after canonical manifest regeneration, real differential
and workflow tests, independent replay boundary coverage, representative paired
latency evidence, and the repository's independent review step. Until then the
source implementation is available for review, but its complete domain behavior
and claimed user-visible performance benefit remain unqualified.
