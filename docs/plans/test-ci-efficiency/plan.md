# Plan: Faster CI with Explicit Test Fidelity and Isolated Fixtures

**Plan status:** `In Progress`

**Current phase:** M0 — Observable baseline and deterministic test oracles

**Next slice:** **M0 — Recover the recorded candidate, then obtain hosted timing artifacts and disposition the independent review**

**Acceptance status:** `pending`

**Composed-design review:** `applicable`; test fixture ownership and lifecycle are being consolidated. The complete probe appears below.

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Review and source evidence:** [reports/code-review.md](reports/code-review.md)

**Implementation authority:** The user selected this plan for implementation on 2026-09-29. M0 is admitted; see the execution ledger for the isolated candidate, source identities, and current implementation-worker binding.

## Objective

Reduce the elapsed time and repeated work of Coding-Standards' complete GitHub verification path while preserving its behavioral, security, publication, authorization, persistence, purpose-isolation, and cold-replay evidence. Make the remaining cost attributable to specific commands, tests, and fixture phases. Repair the audit's weak assertions and direct-invocation discovery defect as correctness work, not as a claimed speed improvement.

The user-observed problem is a 40-plus-minute CI run. This plan does not assume that the complete present suite previously ran in under three minutes, or promise that fixture reuse alone will achieve that duration. The reported five-module comparison is not the full workload.

## Reviewed Source and Integration Context

The reviewed branch head is `8260489e8e3ad6b7e170bbf7bd411bac90758abd`, on PR #2, `implementation/authoring-publication-evidence-a1`. The workflow actually checked out PR merge commit `fa7c4f9d5edee0a94baf6fff0ed29452ffaff7db`. Both have tree `c249e251efcf48ad13d4bfaf854cf496544bece7`; a local tree comparison found no difference. Accepted main at review time is `149ba317e9397519bc181a048ecf76aef129a69c`.

The successful run `36661745679` spent 45m35s in verification and 45m46s in the job. Main's earlier run `36574954850` spent 43m03s in verification but failed. That earlier run establishes a pre-existing long-running workload, not a passing performance baseline. Use the successful current workload for the comparison. Its decoded job log reports 613 Engine tests in 2,637.839s (43m57.839s), about 96.4% of the 2,735-second verification step. The other twelve package groups report 84.068s combined: Contracts is 63.943s, review-evidence 4.501s, and all Analysis tests 1.597s. All 1,254 discovered package tests report OK, followed by 73/73 structural suites passing. These group timings prioritize Engine work; individual Engine test/setup attribution remains missing. See [the hosted baseline](reports/hosted-baseline.json).

Recheck these identities, plan states, and intervening changes at implementation admission. The authoring-publication-evidence plan owns A1 acceptance and later A2/A3 work. This plan neither accepts that work nor changes its gates. Isolated preparation can proceed on the relevant source; integration must preserve A1's accepted semantics and resolve overlapping writes explicitly.

## Objective Acceptance

| ID | Observable criterion | Evidence kind | Required environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CI-A1 | Every current package-test invocation and the complete structural verifier has identifiable command, source identity, elapsed time, exit status, and retained diagnostic output. No discovered tests disappear silently. | supporting + harness integration | locked Python 3.12; hosted workflow for artifact retention | automated | pending | M0/M3 reports |
| CI-A2 | Every migrated fixture represents its declared input material, preserves source state, and isolates mutable repositories, indexes, refs, locks, stores, caches and lifecycle resources between consumers. | fixture contract + real Git/filesystem negative tests | Linux, real local Git, supported runtime | automated | pending | M1 report |
| CI-A3 | Coverage-summary checks always exercise their claimed transition; both digest outputs equal an independently computed changed-byte digest; direct compiler execution includes both operation-variant tests. | focused + negative/oracle + discovery | supported Python; controlled fixtures | automated | candidate evidence complete | M0 focused and negative-oracle checks, 2026-09-29 |
| CI-A4 | Retained integration tests prove real preview materialization, real final verification and publication, fresh evidence/authorization, warm purpose isolation, historical reads, and actual fresh-process recovery. Replaced work has an explicit claim-to-evidence mapping. | integration + contract + cold-process | real Git/SQLite and separate Python processes | automated | pending | M2 report |
| CI-A5 | Pure review-packet checks perform no Git setup; immutable routing scenarios reuse only their owned input scope. Remaining Git and source-mutation tests still reach their real boundaries. | focused + integration + scoped work counts | supported runtime and real Git where claimed | automated | pending | M2 report |
| CI-A6 | All 13 current package-test groups and the complete verifier pass for the delivered candidate; generated inputs are fresh; no new unaccounted skips, omissions, or weakened check outcomes occur. | repository integration + generated freshness | locked hosted Python 3.12 on ubuntu-24.04 | automated | pending | exact-candidate run |
| CI-A7 | The complete verification workload has a repeatable reduction beyond observed environment variability, with eliminated work identified and total resource cost reported. The comparison/budget recorded in M0 is met. | performance | same runner class, lock and comparable full workload | automated + owner disposition | pending | baseline/candidate report |
| CI-A8 | Independent review accepts test fidelity, fixture lifecycle and required-check preservation; the maintainer dispositions findings and accepts this objective separately from A1. | independent review | reviewer and acceptance owner | manual | pending | review/disposition |

CI-A3 has candidate evidence complete; final objective acceptance remains pending. The review's earlier diagnostic observations do not satisfy implementation acceptance.

## Scope

### In Scope

The existing CI workflow; the Engine test fixture owners and their direct consumers; the specified publication, process-reuse, recovery and workflow-presentation tests; the two review-evidence test modules; Analysis routing tests; the compiler test entrypoint; this plan directory; a link-only plan index update; and producer-generated verification inputs affected by these edits.

### Out of Scope

Production verification bypasses; new runtime cache behavior; authorization/evidence reuse across mutable decisions; MCP/interface or persistence changes; general test frameworks, fixture registries or benchmark services; a pytest migration; shared writable Git worktrees as generic fixtures; cross-run caches of accepted results; removing required integration tests; scheduled-only substitutes for required PR checks; new timeout policies; and changes to unrelated plans' acceptance records.

Sharding is a conditional follow-up decision, not the first implementation. Removing unnecessary work precedes parallelizing it. A demonstrated production bottleneck may justify a separately admitted narrow change after M0/M2, not an automatic expansion into Engine redesign.

## Constraints and Assumptions

### Constraints

Preserve the native-only public interface, accepted-main capture, frozen material and replay closure checks, immutable snapshot identities, purpose-separated access, fresh lifecycle and authorization checks, exact review/readiness binding, guarded publication and recovery. A test stub models only its explicitly named boundary and is removed before real integration evidence is collected.

Preserve the current `engine` required-check identity, credential-free exact-source acquisition, immutable upload-action pin, source bundle, and hash-locked Python 3.12 installation. Performance changes do not weaken permissions, lockfiles or source provenance.

Use the smallest test-owned mechanism that removes demonstrated repeated work. A helper extraction alone is maintainability work until measured invocations or materialization actually decrease. A shared seed is immutable input, not shared mutable test state.

Use focused verification during edits. Reuse still-valid evidence for unchanged material and claims. Run the full acceptance path at the integration boundary, not after every helper edit or documentation update.

### Material Assumptions

| Assumption | Decision it affects | Validation and stopping condition | Owner |
| --- | --- | --- | --- |
| Engine remains the dominant cost at implementation admission | Which work receives optimization effort | Already confirmed at 96.4% for the reviewed run; obtain within-Engine test/setup attribution and refresh group timing only as source changes require | CI/integration owner |
| A prepared repository seed is cheaper than existing setup | Whether and where a seed survives as permanent test machinery | Compare preparation plus all forks and cleanup against equivalent direct construction in the actual repeated-use scope; decline reuse with no material net gain | Fixture owner |
| Selected callers observe unchanged source material throughout a sharing scope | Whether a seed or routing projection can be reused | Inventory mutations and add source-change/isolation negatives before sharing; callers with live-source semantics construct fresh input | Fixture/test owner |
| Preview checks are duplicated, not uniquely necessary | Which verifier calls may be substituted | Map exact candidate, receipt, publication, failure and cold-readback claims to retained tests; retain real verification where no equivalent evidence exists | Publication-test owner |
| Hosted timing differences exceed noise | Whether the performance objective is satisfied | Compare equivalent unprofiled full workloads, retain environment fingerprints and variability; repeat only when uncertainty can change the decision | Maintainer/CI owner |

These questions do not block independently useful assertion repairs, source inspection or timing instrumentation.

## Binding Decisions and Owners

| Decision | Owner | Evidence/rationale | Supersedes |
| --- | --- | --- | --- |
| The existing unittest commands remain the execution authority | CI owner | The workflow already owns 13 package groups; Python 3.12 provides native duration reporting | No new runner framework |
| Repository preparation has one Engine test-support owner | Engine fixture owner | `_clone_tracked_worktree` and `prepare_repository` encode different implicit source semantics | Duplicated materialization policy, after consumer migration |
| Seed reuse is explicit, scoped and measured | Fixture owner | Correctness depends on source identity, isolation and lifetime; local clone cost alone does not explain CI | Any implicit path-only/global cache proposal |
| Publication actions are ordinary helper operations, not calls into another TestCase | Publication-test owner | The warm-cache test manually runs another class's full scenario and lifecycle | Direct cross-TestCase execution at the changed boundary |
| Real final verification stays on the apply/recovery integration path | Engine owner; tests enforce it | Existing `_application_verifier` already supplies the narrow test seam | Redundant preview verification only where evidence is retained elsewhere |
| Packet pure checks and Git integration checks have separate setup | Review-evidence test owner | 49 tests currently inherit nine Git setup commands each, including pure checks | Unconditional Git setup for non-Git claims |
| Generated suite-input identities stay producer-owned | Standards verifier owner | Tests participate in registered verification inputs | Hand-edited digest expectations |
| Performance acceptance uses a measured complete-workload comparison | Maintainer | The successful baseline is 45m35s; the under-three-minute comparison is unestablished | Guessed numeric budgets or microbenchmark substitution |

No durable production architecture decision or new ADR is needed for the proposed test-only changes. Revisit that disposition only if a production boundary enters scope.

## Proposed Test-Support Design

### Repository Material and Isolation

Create a small private support module such as `tools/standards_engine/tests/repository_fixtures.py`. Make source selection explicit. Its material contract is the selected committed history plus the declared current tracked working-tree material where the caller needs development overlays. It excludes unrelated untracked files and leaves the source worktree, index and refs unchanged.

The current full-overlay helper is the reference for staged additions, staged removals/renames and modified tracked bytes. Preserve its existing regression at `test_fixture_worktree.py:12-40`. Extend contract evidence for a clean source, non-main source branch, repeated construction after source changes, executable modes and symlinks where supported. Decide and test absent tracked working-tree files explicitly; `ls-files` alone does not distinguish an unstaged deletion from a readable tracked file. Never substitute only HEAD or only mtime for a promise to capture current tracked bytes.

Audit all 35 actual preparation call sites recorded in the review inventory: 21 calls to the full-overlay helper and 14 calls to `prepare_repository`, including standalone Engine trace/MCP client helpers that are not named `test_*.py`. Also inspect the independent direct clone at `test_navigation.py:287`; leave it separate when cloning behavior is its actual subject. A use in `setUp` executes repeatedly, so source-line count is not runtime call count.

For clean CI material, avoid a redundant complete working-tree overlay only after a source-state check proves equivalence. For repeated constructions within one owned class/module scenario, evaluate preparing the coherent seed once and cloning it into independent repositories. Count seed preparation and disposal in the measurement. Do not introduce a global fixture pool simply to share across all test modules; most class-level helpers already run once, and a new seed may add rather than remove work.

An explicit seed owns its capture and temporary directory. A fork owns a complete Git repository, its own mutable refs/index/config/locks, and separate Engine stores and caches. Close consumers before disposing the seed. Register cleanup immediately, including partial-construction failures. Retain independent object copies for tests that may alter object files; preserve `--no-hardlinks` as the conservative default. Sharing Git alternates or common writable worktree metadata is not an admitted shortcut.

Migrate `prepare_repository` deliberately: it presently overlays just `a1-interface.toml`, `a1-contract.schema.json`, and `generated/agent-tools.json`, potentially making local accepted-tree material differ from installed contract bytes. Consumers that intentionally test that skew must construct it explicitly; ordinary workflow fixtures should use a coherent captured candidate. Keep temporary migration forwarding only while callers are being moved; remove it when the bounded migration is complete.

### Publication and Cache Scenarios

Put only genuinely shared setup/actions in a small ordinary fixture helper, such as `tools/standards_engine/tests/publication_fixtures.py`. It may prepare a repository, create fresh authoring/application facades, construct a test-owned proposal and drive named workflow actions. Tests retain their independent deciding assertions. Avoid a fixture hierarchy, one universal scenario configuration object, or a helper that silently asserts every product property.

The detailed supporting-workflow test retains its full coordinated content, exposure, provenance, semantic-revision and historical-readback evidence. The warm-cache test owns a smaller real publication scenario with before/after reads, explicit warming of authoring and application caches, observed reuse, new-publication visibility, preserved historical snapshot results, and purpose redaction. Keep an additional provenance-only transition in the warm test only where the claim mapping shows a unique cache-invalidation requirement; otherwise that transition remains in the detailed scenario.

Do not call another test method or replace another TestCase's class attributes. Extract only the needed setup behind an ordinary context-managed fixture. Apply the same bounded ownership check to `SnapshotDetailTests`, which currently borrows `AnalysisWorkflowTest`'s class lifecycle. Production resources and test input identities remain explicit.

### Review-Packet and Routing Inputs

Keep review-evidence fixtures package-local; their small two-commit data contract is not the same as an Engine standards-corpus fixture. Pure namespace, request-shape, ZIP-validation and descriptor-lifecycle checks need only their declared values and temporary filesystem resources. Actual Git history, dirty source preservation, worktree/common-Git-directory protection, attributes, binary diffs, replace refs and promisor behavior remain real Git integration tests.

Mixed tests should be split at their claim boundary, not mechanically moved wholesale. For example, the duplicate-key portion of `test_request_rejects_duplicate_keys_and_unsafe_paths` is pure parsing, but its missing-source case still depends on repository content. Use the real request parser for parsing claims; keep end-to-end CLI coverage separately.

Within `RouterProjectionTest`, share read-only module/projection inputs for the unchanged canonical routing scenarios. Construct fresh fact bindings and result sets per scenario. Keep fresh input construction for target-drift, changed-source and recording/frozen-replay tests. This is test-scope reuse, not a production routing cache.

## Evidence and Oracle Plan

| Claim | Deciding oracle | Required fidelity and intended negative |
| --- | --- | --- |
| Coverage summary | A test-owned coverage requirement plus literal expected work/count/decision values before and after its transition | Assert that the required operation exists before resolving it. A no-op, omitted work item or wrong count fails; equality between two production summarizers alone is insufficient |
| Changed evidence digest | `"sha256:" + hashlib.sha256(changed_destination[evidence_id]).hexdigest()` computed in the test | Both domain failure and public diagnostic equal those bytes' digest; a different valid-looking SHA-256 must fail; retain expected digest, phase, source, material and no-authorization assertions |
| Compiler entrypoint | Actual standalone and discovery executions include both `OperationVariantTest` methods | Move the main guard after every class; compare method identities, not just aggregate pass status |
| Fixture material | Independent inspection of source/destination tracked paths, blob bytes/modes, status/index/ref state | Missing current edits, retained obsolete files, leaked untracked material or source modification fails |
| Fixture isolation | Two independently mutable forks and an unchanged seed/source | Mutating refs, files, index or stores in one does not alter the other; construction failure releases owned resources |
| Preview | Existing public preview creates the expected private candidate and leaves canonical publication state unchanged | A scoped verifier substitute can prove orchestration, never real verification; at least one retained real coverage-aware preview checks its produced receipt/candidate |
| Apply/recovery | Existing real final verifier, committed candidate, bound evidence and fresh authorization; separate-process consumer | Preview success never authorizes bypassing apply verification; changed evidence and revoked authorization still reject |
| Warm reuse | Observed cache reuse with exact current/historical results and application redaction | Stale result after publication, cross-purpose exposure or bypassed fresh authority fails |
| Workload completeness | Per-package discovered test-ID inventory plus claim-level mapping for intentional replacements | Missing modules, dropped methods, unexpected skips or a successful empty selection fail acceptance |

Use controlled test-local faulty outputs where needed to prove the strengthened assertions reject the named bug. Do not commit mutated production code or create a generalized mutation-testing project. Reopening a facade in the same interpreter is not fresh-process evidence; retain actual subprocess tests for that claim.

## Systemic Finding Audit

**Invariant family:** A check owns its preconditions and evidence fidelity; reusable immutable inputs do not confer shared mutable authority or replace an observable boundary.

**Bounded population:** the two repository helpers and their recorded direct callers; the manual publication and Analysis TestCase lifecycle reuse; the two packet test classes; `RouterProjectionTest`; the two weak-oracle sites; the compiler's early guard; and the existing workflow commands. The direct guard scan found no other test module declaring a later class after a main guard.

**Consumer dispositions:** migrate ordinary Engine fixture callers to one coherent material contract; retain explicit source-skew or clone-semantic scenarios; give pure packet checks lightweight setup; preserve real-Git packet cases; scope routing reuse to immutable scenarios; map duplicated preview/warm assertions before replacement. Inspect the adjacent `test_every_section_full_retry_preserves_exact_item` conditional: either populate every section it claims or name its limited populated-section scope accurately.

**Alternatives:** delete duplicate test execution; consolidate preparation; use an existing verifier seam; preserve a cheaper boundary-specific oracle; or decline an optimization when its net contribution is small. A new pool, production cache, adapter API or test framework is not the default.

**Stopping condition:** every member of this bounded population has a disposition, required claims have retained direct evidence, and the complete-workload comparison is decisive. Expand only when measurement identifies another material contributor or a new semantic/lifecycle owner. Do not continue redesign merely because more small allocations or calls exist.

**Repaired composition:** one Engine repository-material owner, separate package-local packet setup, ordinary publication actions, explicit per-test mutable resources, native unittest execution and existing production verification seams. Compared with the current composition, it removes duplicated setup policy and hidden TestCase lifecycles without adding production authority.

## Simplicity and Ownership Review

**Applicability:** `applicable`

**Independent concepts and dimensions:** Repository material answers what bytes/history are supplied; fixture ownership answers who allocates, when it is valid and where it is disposed; scenario actions answer how a workflow is driven; each test answers why a result establishes its named claim; CI controls execution and evidence retention.

**State, identity, value, time, policy and mechanism:** Only seed inputs and read-only routing projections may be shared under the declared scope. Git/SQLite state, authorization and clock-sensitive lifecycle observations remain owned by each test or explicitly stateful scenario. Canonical production authorities are referenced, not replaced. No interface/schema versions or compatibility matrix are added. Material changes create new captured inputs; root-path identity does not establish byte identity.

**Caller and composition-root knowledge:** Tests specify source material, destination and the actual scenario inputs. The fixture owner hides copying, branch preparation and cleanup. The existing workflow remains the runner composition root; there is no new discovery protocol or registry.

**Representative changes and forced owners:** A tracked-file materialization repair changes the repository fixture and its contract tests. A new publication assertion changes its test and only the shared action it genuinely needs. A packet filename rule changes packet tests, not Engine fixtures. A new test module follows unittest discovery; it does not require hand-maintaining a shard list under the initial design.

**Stable interfaces versus hidden knowledge:** The support boundary passes paths, immutable input captures, and explicitly owned fresh resources. It does not require callers to manipulate another TestCase's class state, Git internals, serialized Engine readiness records or global mock cleanup. Existing private verifier substitution remains inside Engine tests.

**Independent evolution, testing, failure and replacement:** Repository preparation has focused fixture tests and cleanup failures. Packet parsing is testable without Git. Publication correctness is independently checked with real verification. Timing reporting can be removed without changing test semantics. A seed can be replaced by direct construction without changing the material contract.

**Necessary complexity and containment:** Real Git history, authorization, recovery and cold processes are intrinsic to the promised evidence. Keep them in selected integration tests. Immutable input preparation, isolation and cleanup belong in small test support; profiling data belongs in reports, not product APIs.

**Deletion and cumulative machinery result:** The repository helper replaces two implicit policies and repeated preparation where measured. A publication helper replaces direct TestCase execution. Lightweight packet setup removes unused Git prerequisites. A seed survives only when measured savings exceed its lifecycle cost. No general fixture service, persistent test cache, runner framework, plugin layer or schema is retained.

## Milestones

### M0 — Observable baseline and deterministic oracles

**Status:** `In Progress`

**Goal:** Make time and test coverage attributable while repairing the three definite correctness defects.

**Allowed write set:** `.github/workflows/purpose-separated-engine.yml`; `tools/standards_engine/tests/test_workflow_presentation.py`; `tools/standards_engine/tests/test_coverage_publication.py`; `tools/standards_contracts/tests/test_compiler.py`; this plan directory; a link-only `docs/plans/README.md` entry; producer-generated `evaluation/standards-effectiveness/generated/suite-inputs.json` where affected.

**Tasks:**

1. Preserve all existing commands and the single `engine` job identity. Separate the small package groups, Engine suite and structural verifier into named timing boundaries. Add native `unittest -v --durations 0` reporting on the Python 3.12 CI path. Retain process wall time around every package command; class/module setup and process startup are not fully explained by per-test timings.
2. Retain logs and source/runtime/lock identity outside the source worktree. Upload bounded reports on both success and failure using the already pinned artifact action. Preserve the actual test exit code when piping through `tee`; keep `set -euo pipefail`. Upload failure must not convert a failed check to success. Avoid dumping environment variables or credentials.
3. Retain the decoded successful run as the current package-level baseline. Obtain unchanged-test, instrumented per-test/setup evidence before optimizing workload; reuse equivalent exact-material evidence when already available. Record actual `git rev-parse HEAD`, tree, PR head/base, Python and dependency versions, runner image/resources, command, test IDs/outcomes, fixture warm state and duration. Do not label `github.event.pull_request.head.sha` as the checked-out candidate when the workflow uses `github.sha`.
4. Rank test bodies and setup costs. Where class/module setup is material, use scoped profiling or temporary measurements of those phases. Profile selected expensive tests; do not infer hosted throughput from profiled wall time.
5. Make the coverage requirement explicit and always exercised; independently assert the expected summary. Check exact changed-byte SHA-256 at both diagnostic layers. Move `unittest.main()` to the end of `test_compiler.py`.
6. Record the performance comparison, material contributor list, expected removable work and variability policy in the baseline report before choosing broader optimizations. Use a repeatable complete-workload reduction as the initial claim. The maintainer may add an absolute turnaround budget supported by that evidence; no guessed three-minute target becomes a gate.

**Gate:** CI-A1 and CI-A3 have direct evidence; the baseline explains enough of the dominant cost to select M1/M2 work. Assertion repair remains independently useful when a hosted run is unavailable. Timing changes that do not alter source-test material can precede oracle changes for a clean comparison; do not require separate lifecycle commits merely to do so.

### M1 — Consolidated repository material and safe reuse

**Status:** `Planned`

**Goal:** Give Engine tests one coherent fixture material contract and remove measured repeated setup while preserving isolation.

**Allowed write set:** new `tools/standards_engine/tests/repository_fixtures.py`; `test_analysis.py`, `test_agent_workflow.py`, `test_fixture_worktree.py`, and the direct consumers enumerated in `reports/fixture-call-sites.json`; corresponding fixture contract tests; this plan's records; affected producer-generated suite inputs. The independent clone in `test_navigation.py` is initially read-only investigation; add it to the exact write set only if its semantics match the consolidation.

**Tasks:**

1. Classify each caller by live tracked material versus explicit captured input, mutation pattern, setup frequency and required Git history.
2. Extract and test the materialization owner. Preserve source state and existing deletion/rename behavior; make any intentional contract skew explicit.
3. Avoid redundant clean-source overlays after proving equivalence. Benchmark a seed only in scopes with repeated construction, including all setup/fork/disposal work.
4. Retain independent repos and stores. Add sibling-isolation, changed-input, failure-cleanup and source-preservation tests. Keep corruption cases off shared object files.
5. Migrate callers and remove obsolete wrappers and repeated branch/setup logic. Audit generated input closure for newly introduced support modules.

**Gate:** CI-A2 passes; measured setup work decreases in admitted scopes without changed material or lost tests. Decline a seed that provides negligible benefit. Extraction and coherence improvements may be accepted as correctness/maintenance work without claiming they materially resolve 45-minute CI.

### M2 — Claim-directed scenario reduction

**Status:** `Planned`

**Goal:** Remove redundant heavy verification and inappropriate fixture work, retaining every distinct required claim.

**Allowed write set:** `tools/standards_engine/tests/test_analysis.py`, `test_coverage_publication.py`, `test_process_reuse.py`, `test_supporting_workflow.py`, `test_publication_recovery.py`, `test_workflow_presentation.py`; new small `publication_fixtures.py` only if needed; `tools/review_evidence/tests/test_cli.py`, `test_repair_boundaries.py` and a package-local support file only if justified; `tools/standards_analysis/tests/test_routing.py`; corresponding direct fixture tests; plan records and affected producer-generated suite inputs. `test_consumer_publication.py` is initially retained as real-boundary evidence; include necessary assertion additions through an explicit write-set update.

**Tasks:**

1. Produce a claim map for repository verification, preview, apply, recovery, warm reuse and cold consumers. Distinguish structural checks from semantic publication evidence.
2. In `test_coverage_publication.py`, preserve the unreviewed-preview rejection and a coverage-aware real-preview test. Remove the full repository-verification-as-setup pass only where its necessary generated material is established by the existing producer and its verification claim is already covered. For a redundant preview within a larger real-apply scenario, substitute only `_application_verifier` during that one call; assert the candidate passed to the substitute is the expected material and publication state is unchanged. Restore the real verifier before apply. Keep the evidence-change-after-review rejection and cold readback.
3. Review the duplicate real preview in `test_analysis.py:476` using the same claim map. Change it only if the remaining preview integration proves its unique candidate property. Never replace every preview with a stub because apply also verifies.
4. Replace the warm-cache test's manual full TestCase replay with a smaller scenario using ordinary fixture actions. Retain purpose isolation, cache reuse, exact current/historical results and publication invalidation. Keep unique provenance-cache evidence if required.
5. Keep recovery setup independent. It already substitutes `_application_verifier`; reduce surrounding construction only where measured. Prefer immutable initial material and fresh real proposal/readiness state. Do not transplant path-bound admitted databases, serialized readiness or authorization between fixture roots. If modifying its patch lifecycle, own and stop its individual patcher rather than stopping unrelated patches globally.
6. As bounded secondary cleanup, move pure packet checks to lightweight setup and split mixed assertions by their real boundary. The entire hosted package took 4.501s; keep effort proportionate to this contribution. Keep all Git/security/CLI integration cases and their precise diagnostics. Assert no Git setup is invoked by the pure fixture.
7. As bounded secondary cleanup, reuse unchanged routing corpus/projection inputs within their owned scenario scope, with fresh per-call fact/result containers. Preserve fresh-load, drift and frozen-source evidence.
8. Compare the after inventory and claim map, profile remaining dominant tests when necessary, and dispose of redundant helpers rather than accumulating two testing paths.

**Gate:** CI-A4/CI-A5 pass. Scoped operation counts or timing show the intended repeated work actually disappeared. Any loss of unique evidence is repaired before broad performance acceptance.

### M3 — Complete-workload qualification and acceptance

**Status:** `Planned`

**Goal:** Establish the actual hosted outcome, retained fidelity and maintainable final composition.

**Allowed write set:** this plan's records, link-only plan index, affected generated input projection, and bounded repairs in already admitted owners. Any added production owner or materially different CI execution topology requires replanning first.

**Tasks:**

Run the complete existing 13-package workflow and complete verifier under the hash-locked Python 3.12 hosted environment. Record all group outcomes, IDs/counts, permitted skip reasons, source/tree, generated freshness and total verification time. Compare the optimized unprofiled workload with the successful baseline, accounting for source and runner changes. Retain setup and process totals as well as individual timings; do not present parallel critical-path reduction as eliminated CPU work.

Repeat equivalent measurements only when observed variability could change the acceptance decision; reuse valid exact-material results rather than demanding an arbitrary fixed run count. Record samples and their range and the selected comparison method. Keep CI-A7 pending when a difference is indistinguishable from noise or the authoritative workload/environment is missing.

Obtain independent read-only review of fixture isolation, evidence equivalence, mock scope, generated input ownership and failure propagation. Fix findings in their owners, reuse the reviewer for narrow verification, and obtain maintainer disposition. `Implemented` is not `Accepted`.

If the accepted turnaround objective remains unmet, use the measured residual: a newly identified production hotspot needs its own bounded owner decision; balanced class/module-level CI sharding may be considered only after proving independent resources and exact test coverage. Any sharding design must preserve same-class warm scenarios, the union of discovered IDs, per-shard failures, source/environment identity, and a stable required aggregate gate. Do not add it merely to mask unmeasured duplication.

**Gate:** CI-A6–CI-A8 and all preceding claims are satisfied. Otherwise retain the exact pending/blocked claim and the next evidence procedure.

## Verification Commands and Evidence Reuse

Use the interpreter installed from `tools/standards_contracts/requirements.lock` on Python 3.12. The existing workflow supplies the authoritative package list and import contexts. Focused examples:

```bash
PYTHONPATH=. "$python" -m unittest discover -s tools/standards_engine/tests -p 'test_fixture_worktree.py' -v --durations 0
PYTHONPATH=. "$python" -m unittest discover -s tools/standards_engine/tests -p 'test_workflow_presentation.py' -v --durations 0
PYTHONPATH=. "$python" -m unittest discover -s tools/standards_engine/tests -p 'test_coverage_publication.py' -v --durations 0
PYTHONPATH=. "$python" -m unittest discover -s tools/review_evidence/tests -v --durations 0
PYTHONPATH=. "$python" -m unittest discover -s tools/standards_analysis/tests -p 'test_routing.py' -v --durations 0
PYTHONPATH=. "$python" tools/standards_contracts/tests/test_compiler.py -v
PYTHONPATH=. "$python" -m unittest discover -s tools/standards_contracts/tests -p 'test_compiler.py' -v
PYTHONPATH=.:tools/standards_verifier "$python" tools/standards_verifier/verify.py --complete
git diff --check
```

Refresh suite-input material through its existing producer/authorized Engine `verify_repository` operation with `refresh_verification_inputs: true`; then verify the non-refresh path and inspect the generated diff. Generated freshness is supporting evidence, not semantic acceptance. Include new fixture support paths in the actual registered input closure where the existing producer requires them; do not hand-edit digest records or invent a new input manifest owner.

The complete campaign remains all 13 groups in the workflow, not the example focused selection above. Preserve real subprocess publication/recovery cases and changed-authority/cache regressions. A source-only edit does not justify repeating unchanged external acceptance simply to update prose.

## Blockers

No blocker prevents plan admission, oracle repair or timing instrumentation. Hosted performance acceptance requires executable access to the supported runner and locked environment. The review container has Python 3.13.5 and rpds-py 2026.5.1 and cannot qualify that claim. The earlier failed main run is not a substitute.

A1 has separate outstanding review/integration authority. Resolve overlapping source at integration; do not rewrite A1's status or start its later milestones through this performance plan.

## Re-Plan Triggers

Replan when measurement identifies a material bottleneck outside the admitted test/CI owners; a proposed reuse changes identity, authorization, persistence, fixture-source semantics or failure behavior; unique real-boundary evidence cannot be retained after reduction; a global pool/framework or cross-run cache becomes necessary; sharding changes required-check topology; or a final timing claim needs a different workload/environment/budget.

Ordinary repairs, an additional direct consumer in the bounded helper migration, or a test file needed for the same invariant require an explicit write-set update, not a new architecture campaign.

## Concurrent Work

Use disjoint writes only when useful. The integration owner owns the workflow, plan status, generated-input refresh and final acceptance. A fixture worker owns the repository support and migrated callers; a scenario worker owns publication/process-reuse tests after the fixture interface is stable; a lightweight-test worker may own review-evidence and Analysis routing tests independently. The integrator allocates overlapping Engine files to one writer at a time. Reviewers remain read-only.

Serial plan-state integration does not require a concurrent-plan revision protocol merely because several agents contribute. Apply that profile only if outstanding proposals can race on shared plan authority. Return concise handoffs with exact writes, commands, evidence fidelity, failures and residual concerns.

## Repository Isolation and Rollback

Because an open A1 PR touches the same tests, perform implementation in a dedicated, task-owned branch/worktree or equivalent isolated candidate. The implementation agent records its actual branch/path and current base at admission; target is `main`, integration owner is the maintainer, and the branch is temporary and review-visible. Integrate only after resolving the current A1 semantics and acceptance ordering. No existing user worktree is removed by this plan.

All initial changes are test/CI-only and reversible by reverting their coherent source changes; production interfaces and persistence need no migration. Retain original evidence in the report when replacing a test. Remove plan-created worktrees only with the exact head-reachability and commit-disposition evidence required by the Commit workflow; otherwise document their retained purpose and next disposition.

## Final Acceptance

**Acceptance status:** `pending`

**Current final status:** `In Progress`

**Deferred mechanisms:** production optimization and CI sharding, revisited only through measured residual cost and a changed design decision. General test frameworks and persistent caches are excluded.

The maintainer accepts this objective only after every CI-A claim has its required evidence. A faster local subset, reduced test count, generated-freshness pass, or green workflow without a decisive performance comparison does not by itself close the objective.
