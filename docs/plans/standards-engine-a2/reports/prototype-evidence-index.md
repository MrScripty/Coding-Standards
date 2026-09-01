# A2 Milestone 0 Prototype Evidence Index

**Status:** `P1, P2R2, P3, and P4R pass; P2 and P4 revise; P2R rejected;
P5 execution admitted`

The canonical [design-validation protocol](design-validation-protocol.md)
predeclares every question, comparison, dimension, oracle, and threshold.
Prototype source is never merged to `main`. This index will record exact
branch commits and terminal worktree dispositions after each isolated run.

| ID | Exact path | Branch and worktree | Exact admitted base | Prototype commit | Verdict | Worktree disposition |
| --- | --- | --- | --- | --- | --- | --- |
| A2-P1 | `tools/standards_engine/prototypes/a2/authoring-state-model.prototype.html` | `prototype/a2-m0-state-model`; original `/tmp/coding-standards-a2-p1-state-model` now contains out-of-scope M6 work | `bbdfb485e914540e0e53092dab71c9b80f55102d` | `9b3e2111f6909d93e6c2d86f8c7dbb805dad07f8`, corrected by `a6a2e1060e07f5f16d2ee91f72720e31751ba27b` | `pass` | `archive-protected` exactly at `refs/archive/a2-prototypes/p1-state-model`; live worktree unavailable to A2 |
| A2-P2 | `tools/standards_engine/tests/prototypes/a2/projected-view.prototype.py` | `prototype/a2-m0-projected-view`; `/tmp/coding-standards-a2-p2-projected-view` | `a8c7b04504b58446fc0fd6c53b867ddeb7827185` after governed fast-forward and exact-path move from the uncommitted creation worktree | `3bab6e981d6e902e087f485c03fca78d0505a39e` | `revise` | `removed-archived` at `refs/archive/a2-prototypes/p2-projected-view` |
| A2-P2R | `tools/standards_engine/tests/prototypes/a2/projected-analysis-replay.prototype.py` | `prototype/a2-m0-projected-analysis-replay`; removed `/tmp/coding-standards-a2-p2r-projected-analysis-replay` | `c509d61ed0537907191ea615f4a613fc02dabcb2` | `a0478c5c363d851435f193ef5be7ec75255378af` | `reject-requires-product-reauthorization` | `removed-archived` at `refs/archive/a2-prototypes/p2r-projected-analysis-replay` |
| A2-P2R2 | `tools/standards_engine/tests/prototypes/a2/projected-material-identity.prototype.py` | removed `prototype/a2-m0-projected-material-identity`; removed `/tmp/coding-standards-a2-p2r2-projected-material-identity` | `a959ca3d6112ce4b3dc532805cbcb24b2e7fce2c` | `b76f443b5bc05b179d20193bf27ea4d3054db7f3` | `pass` | `removed-archived` at `refs/archive/a2-prototypes/p2r2-projected-material-identity` |
| A2-P3 | `tools/standards_engine/tests/prototypes/a2/publication-recovery.prototype.py` | `prototype/a2-m0-publication-recovery`; `/tmp/coding-standards-a2-p3-publication-recovery` | `a8c7b04504b58446fc0fd6c53b867ddeb7827185` after governed fast-forward and exact-path move from the uncommitted creation worktree | `53fd98f292400aee6929d0cc950cc6163944a5a5` | `pass` | `removed-archived` at `refs/archive/a2-prototypes/p3-publication-recovery` |
| A2-P4 | `tools/standards_engine/tests/prototypes/a2/facade-workflow.prototype.py` | `prototype/a2-m0-facade-workflow`; `/tmp/coding-standards-a2-p4-facade-workflow` | `a8c7b04504b58446fc0fd6c53b867ddeb7827185` after governed fast-forward and exact-path move from the uncommitted creation worktree | `47cfcd5340196b275b910a398d61b7ef68a8e071` | `revise` | `removed-archived` at `refs/archive/a2-prototypes/p4-facade-workflow` |
| A2-P4R | `tools/standards_engine/tests/prototypes/a2/facade-composition.prototype.py` | removed `prototype/a2-m0-facade-composition`; removed `/tmp/coding-standards-a2-p4r-facade-composition` | `fc7dbeabb5828b5b6f3840a1ff004209ae291385` | `9a0c34325e2849c437072b12b3188bede7f08d4e` | `pass` | `removed-archived` at `refs/archive/a2-prototypes/p4r-facade-composition` |
| A2-P5 | `tools/standards_engine/tests/prototypes/a2/efficiency-measurement.prototype.py` | `prototype/a2-m0-efficiency-measurement`; `/tmp/coding-standards-a2-p5-efficiency-measurement` not created | `b503dcb76fd27aca41df154f37e20f6635de44bf` | pending | pending | creation admitted; expected `removed-archived` |

The A2 prototype owner owns each private worktree, its one authored source
path, and the branch-local generated suite-input projection required by that
new tracked path. Canonical `main` is the integration target and the A2
integration owner is its sole integrator. Prototype branches have no production
consumer and never merge. Each run uses scratch state only, then receives a
named recovery ref before its worktree is removed. A material result that
changes a registered question, oracle, state model, or threshold requires a new
canonical admission.

The generated projection diff is path-sensitive. P1 and every Python prototype
(P2, P2R, P2R2, P3, P4, P4R, and P5) must change only the repository-index
digest.
Python prototypes remain below the package's existing `tests` boundary; no
prototype becomes a production package input or requires production ownership.
P2, P3, and P4 had to move their unchanged authored file to the corrected exact
path and fast-forward
to path-correction commit `a8c7b04504b58446fc0fd6c53b867ddeb7827185`
before staging. That former P5 base grants no creation authority; P5 must use
the exact current base and isolation in its separately committed
[execution admission](p5-combined-efficiency-admission.md). P2R2
must be created only after its separately committed execution admission names
the current exact base. P4R must be created only from the exact base and path
registered by its separately committed
[execution admission](p4r-facade-composition-admission.md). No other
prototype-source rewrite, merge, or copying
is authorized by this correction. Exact review may update only a moved
artifact's embedded run path and minimum `__file__` parent depth under the
separately recorded relocation rule; the final evidence must record the
resulting source identity.

## A2-P1 Authoring State Model

### Question And Environment

The prototype asked whether one deep Authoring state model can preserve
immutable revisions and A1c analyses while one proposal head advances by
compare-and-swap and application distinguishes stale, unauthorized,
interrupted, applied, and recovery-required outcomes.

The self-contained HTML ran from its local file with no server, framework,
network, persistence, or external dependency. Node `v24.12.0` executed the
embedded logic under an in-memory DOM shim as a repeatable command-line check.
A human can reproduce the primary interaction by opening the exact worktree
file, clicking each guided-scenario button, and inspecting the complete domain
state, caller selections, last typed result, and transition trace.

### Results

| Scenario | Expected terminal evidence | Result |
| --- | --- | --- |
| Happy apply | verified candidate publishes and establishes `APPLICATION.APPLIED` | `pass` |
| Stale head CAS | wrong expected revision returns `PROPOSAL.STALE_HEAD` without mutation | `pass` |
| Mutation invalidates proof | prior immutable readiness returns `READINESS.STALE` after head movement | `pass` |
| Stale analysis | prior immutable analysis returns `ANALYSIS.STALE` for the new head | `pass` |
| Revoked authority | staging returns `AUTHORING.UNAUTHORIZED` | `pass` |
| Concurrent target change | publication returns `APPLICATION.STALE_TARGET` | `pass` |
| Interrupted before publication | recovery observes the base and returns `APPLICATION.RESUMABLE` | `pass` |
| Applied before response | recovery observes the candidate and returns `APPLICATION.APPLIED` | `pass` |
| Contradictory observation | recovery returns `APPLICATION.RECOVERY_REQUIRED` without guessing | `pass` |

The first run exposed a mutable `currentAnalysis`/`currentReadiness` selector in
domain state. That would risk recreating the mutable analysis-head design A1c
rejected. The corrective commit removed both selectors: commands now carry the
exact opaque analysis or readiness handle, immutable records remain addressed,
and only `proposal.head` is mutable.

### Four-Dimension Verdict

- **Effectiveness:** `pass`. All nine caller workflows reach a typed terminal
  state with explicit next operations and without repository paths, Git IDs,
  raw authority bytes, store paths, duplicated analysis facts, or authored
  completion flags.
- **Efficiency:** `pass` for this state-model question only. The selected model
  requires one mutable CAS head and exact opaque handles already returned to
  the caller. A mutable completion Boolean is strictly worse because it needs
  extra invalidation writes and cannot by itself identify the revision,
  analysis, authority, target, or verification proof. No latency, storage, or
  production resource claim is made; A2-P5 owns those measurements.
- **Correctness:** `pass` for pure transition logic. The exact negative cases
  passed after the A1c preservation correction. SQLite durability, Git
  atomicity, generated facade conformance, and real authorization providers
  remain outside this prototype's oracle.
- **Standards compliance:** `pass`. The prototype branch changed one authored
  HTML source plus only the mechanically derived branch repository-index
  digest. Generated freshness and all 265 declarative suites passed; staged
  whitespace, sensitive-value, and external-dependency review passed.

### Admitted And Rejected Decisions

Admit one deep Authoring Module candidate with private revision, approval,
readiness, attempt, and recovery seams. Only the proposal head is a mutable CAS
selection. Revisions, A1c `AnalysisHandle` references, approvals, and readiness
proofs are immutable and explicitly addressed. Caller-side last-handle
selection is convenience outside domain state. Success requires an established
published identity; contradictory or unavailable observation remains recovery
required.

Reject a mutable analysis head, mutable readiness head, authored completion or
application Boolean, implicit rollback, and recovery by guess. This preserves
A1C-U03, A1C-U06, A1C-U07, A1C-U15, A1C-U19, and A1C-U20. The public operation
shape, persistent representation, publication mechanism, and performance
selection remain unadmitted for A2-P2 through A2-P5.

### Archive And Superseded Worktree Contract

The accepted P1 evidence remains reachable exactly at
`refs/archive/a2-prototypes/p1-state-model` tip
`a6a2e1060e07f5f16d2ee91f72720e31751ba27b`. A later audit observed that the
original worktree and branch had advanced through unrelated M6 commits and
contained uncommitted M6 changes. A2 does not modify, clean, synchronize, or
remove that out-of-scope worktree.

The prior `retained-protected` live-worktree contract is therefore superseded
by `archive-protected`. Product-owner hands-on review requires a new separately
admitted clean worktree reconstructed from the exact archive ref. The prototype
still has no runtime, generated-contract, canonical Engine, or integration
consumer.

## A2-P2 Projected View

### Question And Environment

P2 asked whether exact non-Git replacement mutations can overlay a frozen A1c
snapshot, traverse the current compiler path, and remain semantically identical
to the same bytes captured independently through scratch Git without minting a
proposal snapshot or a second analyzer.

The accepted command was
`PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 /tmp/coding-standards-verifier/bin/python -P tools/standards_engine/tests/prototypes/a2/projected-view.prototype.py`
on Linux CPython 3.12.3. The verifier environment supplied the current project
dependency set. System CPython 3.11 and 3.12 invocations without that environment
were unavailable because `jsonschema` was absent; P2 therefore makes no 3.11
runtime claim.

### Results

| Evidence | Exact result |
| --- | --- |
| Semantic signature | overlay and scratch Git capture were equal |
| Requested corpus | identical 970 paths; digest `sha256:1ac080b26274ff3d54822eac12e9c6e32ded0524657a169ffc71dd8d4d74b05a` |
| Repeated comparison | three post-warm-up overlay and scratch runs remained equivalent |
| Exact negative cases | invalid path, traversal, missing target, duplicate mutation, and semantic-invalid diagnostics matched |
| A1c analyzer boundary | `PrepareCall` rejected `proposal-revision-handle` at `/request/proposed_snapshot/kind` with `CONTRACT.INVALID_INSTANCE` |
| A1c preservation | no snapshot-store mutation, proposal snapshot, second analyzer, or existing public-operation change |

The run observed a 7,100,838-byte requested base corpus, 800,550 bytes of
retained mutation path-and-content material including the required regenerated
suite-input projection, 62 changed byte positions, a 7,100,839-byte scratch
requested corpus, an 8,990,720-byte scratch snapshot store, and 13,239,201
tracked scratch-worktree bytes. Repeated compile observations ranged from about
1.67 to 1.70 seconds. These values are descriptive only; persistence and a
product latency budget were not tested.

### Four-Dimension Verdict

- **Effectiveness:** `revise`. The overlay supplies the exact requested corpus
  through the existing compiler, but the end-to-end analysis workflow is
  unavailable because the current public contract accepts only a
  `SnapshotHandle` as proposed material.
- **Efficiency:** `revise`. Replacement mutations avoid retaining the complete
  corpus in the candidate Adapter and are not dominated by the measured full
  scratch materialization, but durable delta representation, additions,
  deletions, and combined-workflow cost remain untested.
- **Correctness:** `pass` for compiler equivalence and exact negative cases;
  `unavailable` for projected analysis and cold replay. The tightened executable
  oracle returns `revise` only when every equivalence and exact diagnostic holds
  and the exact A1c contract boundary is observed.
- **Standards compliance:** `pass` for the isolated evidence commit. The final
  test-only source and branch-local index digest passed Ruff, formatting,
  generated freshness, all 265 declarative suites, staged diff, and
  sensitive-value review. Missing CPython 3.11 dependencies remain an explicit
  prototype limitation and block any production portability claim.

### Admitted, Rejected, And Revised Decisions

Admit only a private exact-mutation content Adapter candidate over a frozen A1c
base. Reject full-corpus-per-revision storage, proposal-as-snapshot, a second
analyzer, public A1c operation changes, and weaker negative-case matching.

Revise the end-to-end design before P5 or production planning. A2-P2R must
determine whether the existing analyzer can consume projected material while
retaining an exact immutable analysis identity and cold-replay input under the
accepted A1c `AnalysisState`, non-Git change-set, lifecycle, and handle choices.
If that is impossible, A2 must record the conflict and request explicit product
reauthorization rather than changing A1c by implication.

### Archived Worktree Contract

The final source identity is
`sha256:120cbaf126a390808473faf8d18f6f29d4b35448243359f029459e11f0916284`.
The clean task-owned worktree was removed after archive ref
`refs/archive/a2-prototypes/p2-projected-view` was verified at exact tip
`3bab6e981d6e902e087f485c03fca78d0505a39e`. The prototype and branch-local
projection remain recoverable and did not enter canonical `main`.

## A2-P2R Projected-Analysis Identity And Replay

### Question And Environment

P2R asked whether any private seam can give two byte-distinct projected
proposal revisions to the existing analyzer while retaining an injective,
immutable, cold-replayable identity through the unchanged A1c `AnalysisState`.
It compared exactly the five predeclared locations where revision-specific
information could reside: ambient current-head lookup, invocation-only
material injection, the proposed-snapshot field, existing A1c identity fields,
or a separate durable analysis authority.

The accepted command was
`PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 /tmp/coding-standards-verifier/bin/python -P tools/standards_engine/tests/prototypes/a2/projected-analysis-replay.prototype.py`
on Linux CPython 3.12.3 in the dependency-complete verifier environment. Cold
replay used fresh child processes over serialized fixture bytes. CPython 3.11
passed syntax parsing, but its system environment lacked `jsonschema`; this
prototype makes no CPython 3.11 runtime or platform-completeness claim.

### Results

| Candidate or oracle | Exact result |
| --- | --- |
| Unchanged A1c state | both revisions encoded to the same 876 bytes and `analysis:sha256:bc1fa2a16bb6697dc9abab5ba139bf67d74ce033c1c14b7682049c0eccc1f6b0` |
| Ambient current head | revision A replay resolved revision B after head movement; identity was non-injective |
| Ephemeral injection | both cold replays returned `A2P2R.EPHEMERAL_INPUT_MISSING`; no replay authority survived |
| Synthetic proposed snapshot | distinct identities and exact replay succeeded, but only by representing proposal material as an A1c snapshot, prohibited by A1C-U06 and P2 |
| Changed A1c identity | adding `projected_revision` to the change produced distinct 931-byte states with 55 retained identity bytes and exact replay; generated `PrepareCall` rejected it at `/request/changes/0`, the current analyzer erased it to the original declared change, and a top-level state field returned `ANALYSIS.INVALID_STATE` |
| Separate authoring-analysis state | distinct 184-byte outer states replayed exactly through two authorities; the current A1c codec rejected the outer state |
| Analyzer material guard | current `evaluate_analysis` returned `ANALYSIS.SNAPSHOT_MISMATCH` when material did not match the state's proposed snapshot root |
| Candidate-space check | composite proposal/analysis handles and aggregate-child indexes reduce to a second authority; duplicate-root surrogates reduce to proposal-as-snapshot; existing-field and semantic-proposal salts reduce to changed A1c identity semantics |
| Terminal threshold | all five candidates were inadmissible, all registered cold-process observations were exact, the codec and contract oracle was available, and the admissible candidate count was zero |

An independent read-only audit of the current state codec, generated contracts,
prepare/resolve flow, aggregate store, and A1c ADR reproduced equal state bytes
and equal analysis IDs for the collision case. It found no sixth preserving
location: a composite handle, aggregate child, authorization record, duplicate
root, prior analysis, or semantic salt reduces to one of the five tested
representation classes.

### Four-Dimension Verdict

- **Effectiveness:** `reject`. Neither unchanged-state candidate can identify
  and cold-replay the exact proposal revision. Every candidate that can do so
  changes a protected product or architecture boundary.
- **Efficiency:** `unavailable` for design admission. The executable records
  876-byte unchanged states, 931-byte identity-overloaded states, and 184-byte
  outer second-authority states, but no candidate is correctness-equivalent and
  admissible. These representation observations establish no latency, durable
  storage, or full-corpus budget.
- **Correctness:** `pass` for the terminal rejection. The current A1c codec,
  generated prepare contract, analyzer material guard, fresh-process replay,
  exact negative results, and independent implementation audit agree. SQLite
  restart, full-corpus compilation, migration, and public behavior remain
  outside this claim.
- **Standards compliance:** `pass` for the isolated rejection evidence. The
  test-only source and branch-local repository digest passed Ruff, formatting,
  generated freshness, all 265 declarative suites, exact staged diff, and
  sensitive-value review. The commit has a conventional subject and a body
  recording rationale, scope, and contract effect.

### Admitted And Rejected Decisions

Admit the negative design fact only: no private projected-analysis seam exists
under the complete protected constraint set. P2's private exact-mutation
content Adapter remains valid for compilation equivalence but is not an
analysis identity or replay design. Admit no new operation, public field,
state format, proposal snapshot, facade root, durable mapping, analysis owner,
or production source.

Reject mutable current-head lookup and invocation-only material injection
outright. Do not select among the three replayable conflicts. Product-owner
reauthorization would have to reopen A1c analysis identity/codec semantics,
permit proposal material to become snapshot authority, or permit a separate
authoring-analysis identity and authority. Reducing A2 so projected proposal
analysis is no longer required is the non-reauthorization alternative. Each
choice materially changes product scope or a protected A1c decision and
requires an explicit user decision plus a re-plan; A2 cannot choose it.

On 2026-09-01 the user subsequently selected the A1c identity/codec evolution
for prototype-first validation. That authority does not change P2R's rejection
verdict or admit its source. The exact selected scope is recorded in the
[projected-material reauthorization](a1c-projected-material-reauthorization.md),
and P2R2 now owns the new deciding prototype.

P4R, P5, the public contract, persisted authoring design, facade, and production
implementation remain unavailable until P2R2 accepts the selected boundary.

### Archived Worktree Contract

The final source identity is
`sha256:ee36875535c9befb6c1f183fd71436699cd1f15bd7e0a64b138625158cba5097`.
The clean task-owned worktree was removed after archive ref
`refs/archive/a2-prototypes/p2r-projected-analysis-replay` was verified at
exact tip `a0478c5c363d851435f193ef5be7ec75255378af`. The source and its
branch-local generated projection remain recoverable and did not enter
canonical `main`.

## A2-P2R2 Projected-Material Identity And Replay

### Question And Environment

P2R2 asked whether the explicitly reauthorized closed projected-revision
material reference can give one evolved Analysis-owned state injective identity
and exact cold replay through the current compiler, Analysis kernel, Snapshot
Module, and SQLite owner without changing snapshot-backed A1c behavior. It
compared the selected bounded reference with the omitted-reference collision
and a correctness-equivalent persisted full-material control while retaining
ambient-head, proposal-as-snapshot, identity-salt, and second-analysis-authority
cases as prohibited controls.

The exact prototype command ran with dependency-complete Linux CPython 3.11.14
and SQLite 3.50.4, then CPython 3.12.3 and SQLite 3.45.1. Each run used an
independent real scratch Git repository, scratch SQLite store, actual repository
head movement, store close/reopen, and fresh child processes. Both environments
returned `pass` for all 42 registered verdict gates.

### Results

| Evidence | Exact result |
| --- | --- |
| Representative caller | one `analyze_revision(revision_handle)` call; exact `self, revision_handle` signature; no caller changes, material, repository/store facts, resolver, or current head |
| Injective identity | two equal-descriptor revisions produced distinct canonical revision bytes, distinct 1,046-byte state encodings, and distinct analysis handles |
| Cold replay | both handles resolved their exact original revision and evaluation in fresh processes after the scratch repository head advanced |
| Snapshot preservation | semantic projection and state replay remained exact; the generated contract still rejected a revision handle; all eight current operation roots were unchanged |
| Dependency and lifecycle | real SQLite rows bound each selected revision and analysis to its base; quarantine and undelete were exact; purge removed every base-dependent record atomically while the independent alternate root, dependency, and load remained exact |
| Typed boundaries | missing, wrong-base, wrong-dependency, malformed, tampered, retained-input, retained-semantic, unsupported-contract, quarantined, expired, unknown-root, and purged cases reached their exact registered outcomes |
| Prohibited controls | ambient current-head lookup, proposal-as-snapshot, identity salt, and a duplicate Analysis authority were absent and verdict-gated |

The two immutable revision identities were
`proposal-revision:sha256:f843f7fbc07f62aceb6344dcb4bf367f4e9b0bc700c79a3e5d05df2c09d30f7f`
and
`proposal-revision:sha256:6f2ee7040c08cf3d1ff423a9bb86abd62f33b6191e8cd57a94d1095d3cb0c204`.
Their analysis identities were
`analysis:sha256:8780425f2a174631fa7107e2ff03bbabc3f0893d11dca6f7a2f9faee8f836228`
and
`analysis:sha256:5acc65501667a6cc00a299d5f3ddd17d7c804ce285b72787090d07e860ae69d3`.

### Efficiency Evidence

The selected canonical material reference was 202 bytes, the Analysis state
1,046 bytes, and the immutable revision payload 1,636,286 bytes. Including
record identities and dependency rows, selected durable material was 1,637,766
bytes. The correctness-equivalent persisted full-material control was
14,626,773 durable bytes over a 7,265,159-byte base corpus and therefore about
8.9 times larger. The scratch SQLite allocation was 41,275,392 bytes and is a
descriptive allocation observation, not retained product state or a budget.

After one warm-up, all three CPython 3.11 selected compilation observations
ranged from 7.61 to 7.66 seconds and the full-material observations from 3.34
to 3.36 seconds. CPython 3.12 observations ranged from 7.92 to 7.93 seconds and
3.41 to 3.43 seconds respectively. The selected resolver is slower in this
prototype, but the full-material control does not strictly dominate it because
it retains substantially more durable material. No production latency promise
or guessed threshold is admitted; P5 owns the combined-workflow comparison.

### Four-Dimension Verdict

- **Effectiveness:** `pass`. One opaque caller handle reaches exact analysis
  and replay for both immutable revisions without caller-owned internal facts,
  ambient selection, or another analysis authority.
- **Efficiency:** `pass` for the registered P2R2 comparison. The selected state
  retains bounded identity plus change-proportional revision material instead
  of a full projected corpus per analysis, and the faster full-material control
  does not strictly dominate across the registered resource dimensions.
- **Correctness:** `pass`. Identity, compiler and kernel reuse, exact fresh-
  process replay, current snapshot regression, typed failures, real SQLite
  dependency closure, quarantine, undelete, atomic purge, and independent-root
  survival are executable verdict gates on both supported runtimes.
- **Standards compliance:** `pass`. Independent specification and standards
  audits reported no remaining source-level blocker. Ruff, formatting, plan
  lifecycle, generated freshness at 7 retained Bash verifiers, the 9-node and
  33-edge dependency graph, all 269 declarative suites, the complete checkpoint,
  staged-scope, sensitive-value, and conventional-commit review passed.

### Admitted Decision And Limits

Admit for later canonical design one closed Analysis-owned proposed-material
value with snapshot and projected-revision variants, an immutable Authoring-
owned proposal revision, private exact material resolution into the current
compiler, retained normalized analysis inputs checked against that revision,
and typed snapshot dependencies inside the one SQLite aggregate owner. Analysis
remains the sole analysis authority. Reject mutable-head replay, invocation-only
material, proposal snapshots, identity salts, composite external handles, full
projected-material-per-analysis storage, and a second analysis state.

This is design evidence, not canonical source or contract authority. The
prototype-local operation name, codecs, handles, compatibility value, state and
store versions, migration decision, and generated request/result shapes remain
unselected. Only exact replacement mutations were exercised. P4R must select a
preservation-safe facade composition, and P5 must measure the combined design,
before ADR or production planning can proceed.

### Archive And Worktree Contract

Evidence commit `b76f443b5bc05b179d20193bf27ea4d3054db7f3` has source identity
`sha256:255ff74886a4e34b5d30717c25d72997851404d9d81097680bf3bb8eb2837376`
and remains reachable at
`refs/archive/a2-prototypes/p2r2-projected-material-identity`. The exact clean
task-owned worktree and temporary branch were removed after archive verification.
The prototype and its branch-local repository-index digest did not enter
canonical `main`.

## A2-P3 Publication And Recovery

### Question And Environment

The prototype asked whether one Authoring Module can keep a candidate outside
authoritative visibility, verify it, publish through an expected-old-OID ref
transition, and recover a truthful typed outcome after interruption from
durable attempt facts and current Git observation.

It used real temporary Git repositories and SQLite databases that were removed
after each process. The accepted command was
`PYTHONDONTWRITEBYTECODE=1 python3.11 -P tools/standards_engine/tests/prototypes/a2/publication-recovery.prototype.py`,
repeated with `python3.12`. Evidence covered CPython 3.11.14 with SQLite 3.50.4,
CPython 3.12.3 with SQLite 3.45.1, and Git 2.43.0.

### Results

| Evidence group | Exact result |
| --- | --- |
| Safe and recovery scenarios | 13 of 13 passed |
| Repeated safe-path observations | 5 of 5 passed on each supported Python runtime |
| Expected-ref conflict | stale publication rejected; competing target preserved |
| Verification failure | target remained unchanged; cold recovery returned `verification-failed` |
| Authorization rejection | no staging Git call or candidate identity was created |
| Applied before response | cold reopen observed candidate identity and returned `applied` |
| Unavailable observation | returned `unavailable` without persisting a guessed outcome |
| Contradictory observation | unverified authoritative candidate returned `invalid` |
| Unsafe controls | unchecked update overwrote concurrent work; publish-before-verify exposed invalid content |

The five repeated safe-path observations each used 12 Git/process calls, a
12,288-byte SQLite file allocation, and 39,658 to 39,659 scratch bytes. These
are descriptive local observations, not production budgets.

### Four-Dimension Verdict

- **Effectiveness:** `pass`. Stage, verify, expected-target publish, and cold
  recover form one complete workflow, and recovery distinguishes unchanged,
  applied, stale, verification-failed, unauthorized, invalid, and unavailable
  observations without caller-coordinated Git.
- **Efficiency:** `pass` for the registered comparison only. The safe path adds
  one compare-and-swap ref transition and durable attempt facts; the unsafe
  alternatives are correctness-dominated. Timing and byte observations do not
  admit a production resource budget; P5 owns combined-design comparison.
- **Correctness:** `pass`. Real Git proves expected-old-OID lost-update
  prevention, real SQLite cold reopen proves durable observation, and the two
  unsafe controls prove why update-without-CAS and publish-before-verify are
  rejected.
- **Standards compliance:** `pass`. The final test-only branch changed one
  authored source plus only the derived repository-index digest. Ruff,
  formatting, generated freshness, both supported Python runtimes, staged diff
  review, sensitive-value review, and all 265 declarative suites passed.

### Admitted And Rejected Decisions

Admit isolated staging, verification before publication, expected-old-OID Git
ref publication, durable attempt identities, and cold observation-based
recovery as the publication mechanism candidate. Establishing the expected
candidate identity is required before reporting success. Reject unchecked ref
updates, publication before verification, inferred rollback, and success from
unavailable or contradictory observation.

This result does not yet select the product's canonical publication outcome,
which remains a product-owner decision. It also does not admit a cross-store
transaction, provider authorization mechanism, concurrent-process scheduler,
canonical store schema, public facade, or production performance claim.

### Archived Worktree Contract

The clean task-owned worktree was removed after archive ref
`refs/archive/a2-prototypes/p3-publication-recovery` was verified at exact tip
`53fd98f292400aee6929d0cc950cc6163944a5a5`. The source and branch-local
projection remain recoverable from that ref; neither entered canonical `main`.

## A2-P4 Facade Workflow

### Question And Environment

P4 compared eight explicit additive Authoring operations with a single tagged
dispatch and with overloading the accepted A1c `query` and `inspect` roots. It
also exercised a representative create, discover, revise, query, analyze,
approve, apply, and recover workflow plus wrong-handle, stale-head,
unauthorized, unsupported-contract, and invalid-selector cases.

The accepted command was
`PYTHONDONTWRITEBYTECODE=1 python3.11 -P tools/standards_engine/tests/prototypes/a2/facade-workflow.prototype.py`,
repeated on CPython 3.12. Both runtimes loaded the current A1c operation roots
from the manifest and produced the exact expected `revise` verdict.

### Results

| Candidate or invariant | Exact result |
| --- | --- |
| Current A1c roots | all eight manifest roots preserved and unmodified |
| Explicit additive surface | eight calls, 16 caller field occurrences, no next-operation ambiguity in the modeled flow |
| Tagged dispatch | eight calls, 24 field occurrences, all steps share one ambiguous root |
| A1c overload | eight calls, 28 field occurrences, four duplicated Module-owned facts, four current definitions changed |
| Local negative cases | exact rejections with no mutation; all 11 original invariants passed |
| Cross-prototype preservation | twelfth invariant detected all three prohibited stand-ins |

The prohibited stand-ins were a projected `SnapshotHandle` for proposal
material, mutable current analysis/decision selectors, and a caller-supplied
target containing `ref` and `expected_oid`. The first conflicts with A1C-U06
and P2, the second with P1's immutable explicitly addressed evidence, and the
third with A1C-U04 and P3's caller-hidden Git coordination.

### Four-Dimension Verdict

- **Effectiveness:** `revise`. The in-memory workflow completed, but only by
  using three prohibited stand-ins. It cannot establish an admissible
  end-to-end Authoring workflow.
- **Efficiency:** `pass` only for the surface comparison. Explicit roots avoid
  eight tagged selectors and avoid the overload candidate's duplicated facts
  and coordinated A1c changes. No contract, persistence, or combined-workflow
  efficiency claim is admitted.
- **Correctness:** `pass` for manifest-root preservation, local handle/CAS and
  authorization rejections, and exact conflict detection; `unavailable` for a
  preservation-safe query/analyze/apply composition.
- **Standards compliance:** `pass` for revise evidence. Both supported Python
  runtimes, Ruff, formatting, generated freshness, all 265 declarative suites,
  exact staged diff, and sensitive-value review passed. The audit refuses to
  select the candidate rather than changing prior decisions by implication.

### Admitted, Rejected, And Revised Decisions

Admit only the comparative finding that explicit additive operations are the
non-dominated surface candidate among the three tested shapes. Reject tagged
dispatch and A1c `query`/`inspect` overload. Do not admit the eight candidate
roots, candidate contract version, request fields, internal seams, or modeled
workflow.

P4R must follow an accepted P2R2. It must remove proposal-as-snapshot, keep
analysis, approval, and readiness immutable and explicitly addressed, and
obtain target authority from trusted deployment context while preserving P3's
expected-ref publication internally. If it cannot do so, the facade remains
rejected.

### Archived Worktree Contract

The final source identity is
`sha256:6965a383b673b38b70a9b7cfece083465f84d229148e24ec0603adb4ac7b2013`.
The clean task-owned worktree was removed after archive ref
`refs/archive/a2-prototypes/p4-facade-workflow` was verified at exact tip
`47cfcd5340196b275b910a398d61b7ef68a8e071`. The artifacts remain recoverable
and were not merged to canonical `main`.

## A2-P4R Facade Composition

### Question And Environment

P4R tested whether a common-caller typed-continuation facade could preserve
eight distinct Authoring intents without P4's proposal-as-snapshot, mutable
evidence selector, caller Git facts, tagged dispatch, or A1c overload. It
compared the selected portfolio with a minimal three-root goal Interface, a
flexible revision-addressed portfolio, P4's invalid explicit surface, tagged
dispatch, and A1c overload.

The frozen source identity was
`sha256:d3e9d80f3561eb83d818969cdf586d423baba594a8a435a547e2c5dc034c036f`.
The exact prototype ran with `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.`, and
safe-path `-P` in the dependency-complete
`/tmp/coding-standards-a1c-py311` and
`/tmp/coding-standards-a1c-py312` environments. The real current A1c platform
harness created, queried, prepared, resolved, and inspected scratch state in
each run, then removed it.

### Results

| Candidate or invariant | Exact result |
| --- | --- |
| Selected public shape | exactly `create_proposal`, `find_proposals`, `revise_proposal`, `query_proposal`, `analyze_proposal`, `review_proposal`, `apply_proposal`, and `recover_application`; 16 defined caller fields |
| Representative work | 11 A2 calls plus unchanged A1c `resolve`; all proposal, revision, analysis, readiness, and application handles had observable downstream use |
| Query composition | current generated `QueryCall` decoded canonical route, read, and related requests; historical read survived head movement; prototype-local projected answers explicitly made no canonical A1c `QueryResult` claim |
| Caller knowledge | 49 independently named required atomic facts and exactly 49 supplied; no forbidden repository, ref, OID, store, resolver, capability, or completion fact |
| Failure coverage | 28 negative cases covered every one of 17 registered failure contracts with exact bounded results, complete Adapter traces, and nonmutation |
| Publication and recovery | success required verified candidate identity, expected-target CAS, and exact post-observation; unavailable or contradictory observation never inferred success |
| Candidate comparison | no correctness-equivalent candidate strictly dominated the selected portfolio on calls, caller facts, fields, ambiguity, and coordinated owners |
| A1c preservation | exact eight roots and capabilities unchanged; additive roots still rejected; generated snapshot, analysis, query, and resolve DTOs composed without another Analysis authority |

Both CPython 3.11.14 and 3.12.3 returned `pass` for all 34 verdict gates,
reported the 49/49 workload, advanced a real A1c resolve handle, and removed
their temporary state. Independent specification and standards audits passed
on the exact frozen hash after rejecting and correcting earlier overclaims in
mutation scope, query variants, A1c failure meanings, and unavailable-target
classification. Ruff, formatting, generated freshness, plan structure, all
269 declarative checks, all seven retained Bash verifiers, staged-scope,
sensitive-value, and commit review passed.

### Four-Dimension Verdict

- **Effectiveness:** `pass`. A caller completed create, cold handoff and
  rediscovery, revise, historical and current query, projected analysis through
  unchanged A1c `resolve`, review, direct application, and recovery using only
  authored facts and returned opaque handles.
- **Efficiency:** `pass` for the registered Interface question. The selected
  candidate supplied exactly the independently named workload facts and was
  not strictly dominated by a correctness-equivalent alternative. Timing,
  durable-byte, and combined-workflow claims remain owned by P5.
- **Correctness:** `pass` for facade shape and composition. Exact bindings,
  authorization ordering, immutable history, query-union handling, current
  resolve meanings, publication observation, recovery, failures, traces, and
  nonmutation were executable gates. P2R2 and P3 remain authoritative for real
  material persistence and Git semantics.
- **Standards compliance:** `pass`. Both independent frozen-source audits and
  every required runtime, repository, diff, sensitive-value, and commit gate
  passed before archival.

### Admitted And Deferred Decisions

Admit the typed-continuation portfolio as the A2 facade design for later
contract and implementation planning. Its public intents and caller fields are
the eight shapes listed above; the Authoring Module privately derives proposal
binding, projected material, head checks, target authority, verification, Git
facts, and recovery observations. Only exact replacement mutations were in
scope. Existing A1c `resolve` remains the continuation for pending Analysis.

Reject the minimal merged-goal Interface, redundant flexible handles, P4's
caller stand-ins, tagged dispatch, and A1c root overload. Do not yet select
exact request/result schemas, a public Interface version, handle wire formats,
store representation, migration, an ADR, production write sets, or Engine
code. Generated `QueryCall` compatibility proves the current request union can
be carried; prototype-local projected answers are not canonical A1c result
semantics.

P5 must be re-registered against the accepted P2R2 material model and this P4R
facade before it can execute. The former P5 base and unexecuted isolation entry
predate both accepted decisions and are not creation authority.

### Archived Worktree Contract

Evidence commit `9a0c34325e2849c437072b12b3188bede7f08d4e`
was created from exact admitted base
`fc7dbeabb5828b5b6f3840a1ff004209ae291385`. The archive ref
`refs/archive/a2-prototypes/p4r-facade-composition` was verified at that exact
tip before the clean worktree and temporary branch were removed. The prototype
source and branch-local repository-index projection remain recoverable only
from the archive and did not enter canonical `main`.
