# Nested proposal-material reuse — implementation and evidence

**Status:** implemented and locally verified; supported installed qualification and independent review are not claimed for this new increment.

**Branch:** `implementation/purpose-separated-standards-engine`
**Base:** `63338566110bf8de9d0a84fddf3322cc6bb6c0c9`
**Scope:** complete operation-local reuse through focused proposal creation, revision, analysis, and resolution. The user separately reported successful installed qualification and independent review of the preceding increment; that report is not new verification of this candidate.

## Objective and admission

The [performance design](standards-engine-performance-report/design.md) already admits passing verified immutable inputs through one operation. This increment closes the measured gap between focused workflow preflight, prospective revision validation, and native analysis. It preserves separate decision evaluations and current authority observations. Existing normative guidance, public schemas, persisted formats, dependency locks, Identity-v2, capture replay, and installed configuration remain unchanged.

The write set is the Engine's operation-material owner, authoring preparation boundary, focused workflow composition, corresponding tests, `PURPOSE-SEPARATION.md`, this report/evidence, and the generated verification-input manifest. Authoring's preparation dependency becomes invocation-owned rather than Engine-lifetime; its durable root coordination remains in the existing Authoring module. All in-repository callers are updated together. This is an internal Python composition change, not a new wire or persistence contract.

## Composed design and proof lifetime

The only added helper, `ProposalMaterials`, owns one verified base and the latest exact proposal projection. A focused invocation passes it explicitly. The Engine retains no scope field, and no global registry, context variable, cross-call cache, database or transport lifetime carries the scope across calls. One complete immutable projection replaces another when the revision changes. During a revision build the previous and current working values may coexist transiently; this is operation working memory, not an accumulating cache.

`AuthoringModule` receives its `ProposalPreparation` collaborator per create/revise invocation. That interface contains only prospective validation and exact base-repository path observation. The module still owns proposal identity, durable root creation, current-head checks, conditional advancement, and publication failure behavior. The Engine composes the concrete preparation and computation. Test-only fixture preparation preserves the prior low-level tests' synthetic-corpus boundary; real Engine tests exercise the production collaborator.

The snapshot content is fully verified once before its first use in an operation. Every reuse observes current snapshot lifecycle. Analysis loads and validates stored revisions at its existing boundaries, and the preflight and pre-/post-submission evaluations remain independent. Authorization and provider decisions are never retained in the helper. A new public invocation, including reentrant invocation on the same Engine, starts with its own helper and durable material checks.

Public authoring entrypoints admit purpose before entering private composed helpers. Internal helpers carry the already admitted scope; the purpose contract and generated public schemas are unchanged. Review, verification, application, and recovery receive their existing fresh material/authority observations rather than a borrowed focused scope. Capture performs the independent live and frozen compilations before any proposal-material reuse.

The helper clears its retained values on successful return, rejection, or an exception. There is one coherent owner for this proof lifetime. Removing it would distribute repeated derivation and its lifetime rules back across prospective validation, preflight, and analysis; it contains an actual measured responsibility rather than introducing a general cache framework.

## Behavioral acceptance

| Claim | Deciding evidence | State |
| --- | --- | --- |
| Reference and normative `propose` reuse one verified base and one projection through validation/analysis | Real disposable Git/SQLite workflow plus counted material operations | Passed locally |
| `revise` uses one base and independently builds the previous and new projections | Revision-content, stale-context and operation-count regressions | Passed locally |
| Focused resolution retains three evaluations while sharing input material | Preflight plus pre-/post-submission assertions | Passed locally |
| Current lifecycle, head and evidence decisions retain authority | Quarantine-during-authorization, competing-head and invalid-evidence regressions | Passed locally |
| Other invocations and purposes cannot borrow this scope | Separate invocation, public reentry, application-denial and cleanup regressions | Passed locally |
| Capture and publication/recovery remain correct | Existing real-boundary suites and explicit independent-capture regression | Passed locally |

## Measurements

Three complete serial sweeps per implementation used the same committed fixture
source at `63338566`. All 48 observations share the same captured content ID,
434 files and **3,733,667 source bytes**. The final candidate's production-source
hashes match the tested candidate. Baseline and candidate used the same Python,
dependency installation and host. No package-test processes ran concurrently
with the final timing comparison. The public facade and snapshot were already
constructed; fixture creation and capture are outside each operation timing.

| Operation | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Reference `propose` | 3.674 s | 1.595 s | 2.30x |
| Normative `propose` | 3.790 s | 1.620 s | 2.34x |
| Focused `revise` | 5.719 s | 2.878 s | 1.99x |
| Focused `resolve_workflow` | 3.324 s | 1.739 s | 1.91x |
| Focused `analyze` from a draft revision | 1.618 s | 1.650 s | 0.98x |
| Native `analyze_proposal` | 1.660 s | 1.525 s | 1.09x |
| `workflow_status` | 1.619 s | 1.590 s | 1.02x |
| `query_proposal` | 1.493 s | 1.568 s | 0.95x |

The first four rows address measured redundant derivation. The last four are
controls: their material-operation counts are unchanged, and these small samples
do not establish meaningful speedups or regressions for them. In particular,
focused `analyze` is valid from a draft revision context; it is not a request to
re-analyze a completed workflow context. Three samples establish medians and
ranges, not tail-latency service levels. No installed Codex/SDK or full-suite
speedup is inferred from these native-facade measurements.

| Operation | Durable content loads | Full compiler calls | Proposal projections | Decision evaluations |
| --- | --- | --- | --- | --- |
| Reference `propose` | 3 → 1 | 4 → 2 | 2 → 1 | 1 → 1 |
| Normative `propose` | 3 → 1 | 4 → 2 | 2 → 1 | 1 → 1 |
| Focused `revise` | 3 → 1 | 6 → 3 | 3 → 2 | 2 → 2 |
| Focused `resolve_workflow` | 2 → 1 | 4 → 2 | 2 → 1 | 3 → 3 |

Full compiler counts include the base and changed candidate compilation.
Resolution retains **three** separate evaluations: focused preflight and the
pre-/post-submission states. A revised proposal retains independent old/new
candidate compilations. Every new public call obtains fresh verified material;
no measured result depends on cross-call state. The implicit-capture regression
separately proves both independent record/replay compiler passes.

Instrumented spans are inclusive and are not added together. Actual wall times,
ranges, CPU observations and the fixed corpus binding are retained in:

- [Comparison CSV](performance-nested-increment/comparison.csv).
- [Baseline observations](performance-nested-increment/paired-baseline.jsonl) and
  [candidate observations](performance-nested-increment/paired-candidate.jsonl).
- [Environment and measured source hashes](performance-nested-increment/measurement-environment.json).
- [Reproduction driver](performance-nested-increment/measure_nested.py).

The helper's retained population is one base and the latest projection, verified
by ownership and cleanup regressions. Peak process RSS was not measured for this
increment; transient compiler working memory is not represented as a byte-budget
claim.

### Reproducing the paired comparison

Use separate baseline/candidate implementation checkouts and one common baseline
fixture checkout. Run each command serially with a new output filename:

```bash
python /path/to/measure_nested.py --source /path/to/baseline \
  --fixture-source /path/to/baseline --output /path/to/baseline.jsonl --repeats 3
python /path/to/measure_nested.py --source /path/to/candidate \
  --fixture-source /path/to/baseline --output /path/to/candidate.jsonl --repeats 3
```

The driver changes only disposable fixtures and the selected evidence file. It
checks the expected successful/pending outcome for each operation and counts the
same real implementation boundaries on both sides. The normative fixture is
synthetic test content, not a published standards change.

## Regression and structural evidence

All **177 Engine tests passed** exactly once in the final campaign. They ran in
18 isolated per-module Python processes, with at most three modules concurrent;
each test module owned independent fixture repositories and stores. This is full
discovered test-population coverage, not a claim of one serial ordered suite run.
The qualification repository was a private Git CLI candidate
`20f05cd5800a5a27feb69bd2df2f1bc5db9b5879` with its own accepted `main`.
Its changed Python sources are byte-identical to the delivered implementation.

The eleven supporting package suites ran **421 tests: 420 passed and one existing
interpreter-dependent skip**. These covered Graph, Repository Git, Analysis,
Applicability, Contracts, Standards Graph, Identity, Metadata, Policy Impact,
Snapshots and the Verifier. Existing assertions and test populations were
preserved. Low-level Authoring fixtures now supply the invocation-owned
preparation interface; their synthetic validation scope is not claimed as real
Engine preparation coverage.

The new eleven regressions cover coherent creation/revision, exact operation
counts, invalid evidence, snapshot quarantine during authorization, a competing
proposal head after preflight, fresh subsequent reads, independent public
reentry, cleanup after exceptions, independent capture passes, and denial of
application-purpose authoring. Existing real Git/SQLite publication, cold
recovery, coordinated supporting-content publication, native/CLI/MCP transport,
and purpose-projection tests all passed in the final campaign.

[The verification inventory](performance-nested-increment/verification.json)
retains per-module/package outcomes. [Per-test timings](performance-nested-increment/test-timings.csv)
include setup/body/teardown but were measured under concurrent test execution;
they are diagnostic, not paired performance evidence.
[The source binding](performance-nested-increment/source-binding.json) records
exact tested hashes and a separate Python 3.11 grammar check. Grammar acceptance
is not execution on Python 3.11.

The final structural checkpoint is recorded separately in
[structural evidence](performance-nested-increment/structural.json). Its checks
validate declared structure and generated freshness, not prose quality or the
functional test results. Raw test-process logs are included in the delivery
archive's `evidence/qualification/` directory.

## Qualification boundary

The local runtime is Python 3.13.5, Git 2.47.3 and SQLite 3.46.1. The repository supports Python 3.11/3.12. Local `rpds-py` is 2026.5.1 rather than locked 2026.6.3. The lock and support declarations remain unchanged. This candidate needs its own supported locked run and independent review before claiming installed acceptance; the user's qualification of `63338566` does not transfer automatically. The official MCP SDK and configured Codex installation are not present here.

The source reconstruction preserves local accepted `main` at `366c1d9`. Disposable test clones place their own local `main` at a candidate. The user's working tree, installed database, archived proposals and Codex configuration are outside the write set.

Cross-call compilation retention, selective compilation, SQLite changes and transport-lifetime changes remain outside this increment. Native calls that already derive their material once are expected controls, not promised speedups.

## Review and integration disposition

The implementation retains the existing public schema, persisted state,
identity framing, accepted-main capture and two-pass replay, purpose projection,
and per-call Engine/store lifetime. Source comparison confirms normative
standards, registered prompts/templates, public contracts, dependency locks,
and the previous Identity/Git performance implementation are unchanged.

The internal `AuthoringModule` preparation collaborator is now supplied per
create/revise invocation. All in-repository callers were updated together; old
constructor callback parameters and their unused Engine adapters were removed.
This is a coordinated internal Python interface replacement, not a runtime
compatibility layer. The previous accepted plan is not reopened or relabeled.

This increment closes nested focused proposal/analysis material reuse at the
implemented boundaries. Review, verification, application and recovery retain
fresh existing observations; cross-call compilation and transport-lifetime
changes remain separate conditional work. The complete broader design is not
claimed to be implemented.

The final Git CLI commit and exact tree are identified by the delivery manifest.
The supplied incremental bundle preserves that commit; the patch independently
reproduces its tree. Remote integration and installed acceptance are separate
from the local evidence above.
