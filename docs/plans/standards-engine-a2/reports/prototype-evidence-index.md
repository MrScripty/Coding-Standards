# A2 Milestone 0 Prototype Evidence Index

**Status:** `P1 and P3 pass; P2 revision and P4/P5 review pending`

The canonical [design-validation protocol](design-validation-protocol.md)
predeclares every question, comparison, dimension, oracle, and threshold.
Prototype source is never merged to `main`. This index will record exact
branch commits and terminal worktree dispositions after each isolated run.

| ID | Exact path | Branch and worktree | Exact admitted base | Prototype commit | Verdict | Worktree disposition |
| --- | --- | --- | --- | --- | --- | --- |
| A2-P1 | `tools/standards_engine/prototypes/a2/authoring-state-model.prototype.html` | `prototype/a2-m0-state-model`; `/tmp/coding-standards-a2-p1-state-model` | `bbdfb485e914540e0e53092dab71c9b80f55102d` | `9b3e2111f6909d93e6c2d86f8c7dbb805dad07f8`, corrected by `a6a2e1060e07f5f16d2ee91f72720e31751ba27b` | `pass` | `retained-protected` at archived tip `refs/archive/a2-prototypes/p1-state-model` |
| A2-P2 | `tools/standards_engine/tests/prototypes/a2/projected-view.prototype.py` | `prototype/a2-m0-projected-view`; `/tmp/coding-standards-a2-p2-projected-view` | `a8c7b04504b58446fc0fd6c53b867ddeb7827185` after governed fast-forward and exact-path move from the uncommitted creation worktree | pending | pending | pending; expected `removed-archived` |
| A2-P3 | `tools/standards_engine/tests/prototypes/a2/publication-recovery.prototype.py` | `prototype/a2-m0-publication-recovery`; `/tmp/coding-standards-a2-p3-publication-recovery` | `a8c7b04504b58446fc0fd6c53b867ddeb7827185` after governed fast-forward and exact-path move from the uncommitted creation worktree | `53fd98f292400aee6929d0cc950cc6163944a5a5` | `pass` | `removed-archived` at `refs/archive/a2-prototypes/p3-publication-recovery` |
| A2-P4 | `tools/standards_engine/tests/prototypes/a2/facade-workflow.prototype.py` | `prototype/a2-m0-facade-workflow`; `/tmp/coding-standards-a2-p4-facade-workflow` | `a8c7b04504b58446fc0fd6c53b867ddeb7827185` after governed fast-forward and exact-path move from the uncommitted creation worktree | pending | pending | pending; expected `removed-archived` |
| A2-P5 | `tools/standards_engine/tests/prototypes/a2/efficiency-measurement.prototype.py` | `prototype/a2-m0-efficiency`; `/tmp/coding-standards-a2-p5-efficiency` | `a8c7b04504b58446fc0fd6c53b867ddeb7827185`; worktree not yet created | pending | pending | pending; expected `removed-archived` |

The A2 prototype owner owns each private worktree, its one authored source
path, and the branch-local generated suite-input projection required by that
new tracked path. Canonical `main` is the integration target and the A2
integration owner is its sole integrator. Prototype branches have no production
consumer and never merge. Each run uses scratch state only, then receives a
named recovery ref before its worktree is removed. A material result that
changes a registered question, oracle, state model, or threshold requires a new
canonical admission.

The generated projection diff is path-sensitive. P1 and the Python P2 through
P5 artifacts must change only the repository-index digest. Python prototypes
remain below the package's existing `tests` boundary; no prototype becomes a
production package input or requires production ownership. P2 through P4 must
move their unchanged authored file to the corrected exact path and fast-forward
to path-correction commit `a8c7b04504b58446fc0fd6c53b867ddeb7827185`
before staging. P5 must be created directly from that re-admitted base. No
other prototype-source rewrite, merge, or copying is authorized by this
correction.

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

### Retained Worktree Contract

- Purpose: allow the product owner to drive and inspect the human-facing state
  prototype before Milestone 0 design acceptance.
- Owner: A2 prototype owner.
- Head and reachability: clean tip
  `a6a2e1060e07f5f16d2ee91f72720e31751ba27b`, archived exactly by
  `refs/archive/a2-prototypes/p1-state-model`.
- Synchronization: frozen; no rebase, merge, or edit without a new registered
  prototype question or corrective evidence commit.
- Consumer: product-owner design review only; no runtime, generated contract,
  canonical Engine, or integration consumer.
- Retirement: after product-owner feedback is recorded, or before Milestone 0
  acceptance, whichever comes first; then verify the archive ref and remove
  only this clean task-owned worktree.

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
