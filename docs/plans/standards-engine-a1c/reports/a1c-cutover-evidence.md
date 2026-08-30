# A1c Milestone 5 Cutover Evidence

**Recorded:** 2026-08-30

## Boundary

This record belongs to the atomic Milestone 5 A1b-to-A1c replacement based on
`59b2107a13d165986c64654217121ee9d18db6f4`. The coherent implementation commit
is assigned only after final generated freshness and verification pass; this
report does not create a separate lifecycle boundary.

## Implemented Cutover

- `repository_git` owns sanitized Git command execution and exact object reads.
- `standards_snapshots` owns unique snapshot roots, immutable deduplicated
  content, aggregate analysis storage, quarantine, undelete, expiry, and purge.
- Metadata and downstream semantic compilers consume one immutable
  `ContentSource`; they do not know Git, SQLite, or snapshot lifecycle.
- One immutable `AnalysisState` stores exact inputs and dependency-valid
  decisions. Requirements, obligations, reading plans, certificates,
  completion, and child inspection are deterministic projections.
- The generated v12 facade exposes exactly create, find, delete, undelete,
  query, prepare, resolve, and inspect with handle representation v5.
- The A1b generic Authority package, domain wrappers, v11 facade, independent
  child persistence, and A1b declarative artifacts are absent without fallback
  or compatibility loading.

## Relationship And Consumer Dispositions

The baseline-to-current migration fixture contains one disposition for every
relationship in the union of both graphs: 258 retained, 86 corrected, 63
added, and 43 retired. The final graph has 407 relationships. Corrections,
additions, and retirements affect exactly these coverage subjects:

| Subject | Added | Corrected | Retired |
| --- | ---: | ---: | ---: |
| `core.simplicity-and-complection` | 4 | 0 | 0 |
| `topic.architecture.composed-design-admission` | 13 | 0 | 0 |
| `topic.architecture.immutable-authority-closure` | 12 | 11 | 16 |
| `topic.contracts.declaration-and-semantic-authority` | 1 | 1 | 1 |
| `topic.contracts.generated-semantic-conformance` | 1 | 1 | 1 |
| `topic.contracts.identity-versus-instance-equality` | 1 | 0 | 1 |
| `topic.contracts.version-scope-and-invalidation` | 1 | 0 | 1 |
| `topic.cross-platform.filesystem-paths` | 7 | 0 | 7 |
| `topic.dependencies.requirement-and-ownership` | 12 | 65 | 8 |
| `topic.security.filesystem-containment` | 8 | 0 | 8 |
| `workflow.planning.active-plan-fields` | 2 | 5 | 0 |
| `workflow.planning.replanning` | 1 | 3 | 0 |

Every changed row names its source policy unit, relationship kind, consumer,
declaration source, fingerprint, and disposition. Added relationships register
the A1c packages, runtime paths, generated contract, and registered Python
verification. Corrected relationships replace A1b identities or fingerprints
with their A1c owners. Retired relationships select only deleted A1b authority,
wrapper, facade, suite, and fixture consumers. No selected consumer is blocked
or implicit.

The twelve affected authored claims cite this evidence. The other 37 policy
subjects retain identical typed coverage dependencies and unchanged claims.
Analysis derives current requirement and certificate identities from the
frozen views; authored claims retain stable subject and semantic selectors and
contain no generated digest.

## Verification

- Repository Git: 5 tests passed.
- Snapshots: 13 tests passed.
- Identity: 9 tests passed.
- Contracts: 19 tests passed.
- Applicability: 12 tests passed.
- Metadata: 20 tests passed.
- Policy Impact: 9 tests passed.
- Standards Graph: 2 tests passed.
- Analysis: 73 tests passed.
- Standards Engine: 22 tests passed, including cold reconstruction and all
  eight public workflows.
- Standards Verifier: 433 tests passed.
- All 227 registered declarative suites passed.
- All 53 retained migration checkers passed without extension.
- Required coverage subjects equal valid repository coverage subjects: 49 of
  49, with no missing or extra subject.
- Generated checker dependency changes are limited to the admitted A1b-to-A1c
  migration-fixture reference replacement; node and unrelated projections are
  unchanged.

Final generation freshness, changed-source lint, plan validation, staged-scope
review, and diff hygiene are rerun after this evidence and its exact attestation
references are staged.
