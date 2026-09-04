# C6 And Proposed C7 Design History Research

**Status:** Research evidence; not planning admission

**Reviewed boundary:** commit
`9794b92708aad42c4838f9ad5c6b78e3984d73b3`, tree
`0f7bc73dcaf6c7cacf348c6f8de50ff5f41928c5`

## Question

Why did candidate C6 select its current authority, closure, transition, and
snapshot design? Has the proposed C7 design been attempted or considered
before, and could it reintroduce a previously recorded defect?

This report does not accept C7, supersede C6, or admit implementation. It
records primary-source research needed before those decisions.

## Method

The research covered:

- all 1,183 commits reachable through `git log --all`;
- 210 dangling commit objects reported by `git fsck`, including the protected
  historical heads recorded by the
  [historical reachability recovery](../../historical-git-reachability-recovery/reports/final-acceptance.md);
- the accepted A1 ADR, milestone and repair reports, current implementation,
  and tests;
- the A1b authoring brief, proposed ADR, candidates C through C6, rejection
  ledger, schema, interface, and authority reports; and
- the current Architecture, Contracts, Cross-Platform, Security, Persistence,
  and Planning standards.

The repository contains no artifact named C7. “C7” below means the design
assembled after C6 review; it has no candidate commit, tree, schema, or
admission status.

## Historical Sequence

| Boundary | Decision or defect | Lasting lesson |
| --- | --- | --- |
| A1 foundation, `c7d23dfa` through `94b295b4` | Established the read-only facade, snapshot-bound operations, derived `NextOperation` guidance, one immutable functional `AnalysisState`, dormant decisions, and separation from A2. Snapshot identity deliberately included scope, exclusions, modes, symlinks, and nested repository state. | These were intentional architecture decisions, not accidental repair residue. |
| A1 repairs, `51dcd258` through `2359a987`; acceptance `933c9ab9` | Fixed live worktree reads, incomplete child inspection, incomplete generated contracts, wrong equality and pattern behavior, internal result leakage, private imports, and weak negative evidence. | Cold reconstruction, exact public algebra, external semantic oracles, and failure-path precision are proven recurring risks. |
| A1b trigger `3439aae9`; recovery base `c4408363` | Found that A1 handles lacked complete immutable authority closure and that Draft 2020-12 equality had been replaced by NFC identity equality. | A1b must separate wire validation, domain semantics, and identity while preserving exact replay authority. |
| Initial A1b `f41037bf` | Used three aggregate roots, NFC identity v1, and broad semantic/provider/version payloads. | Rejected aggregate cold-inspection authority, incomplete migration, and underspecified identity. |
| Candidate C `44de7dff` | Introduced representation-preserving identity v2 and direct storage for every inspectable object. | Direct stored-object inspection survived all later candidates; C was rejected for unrelated registry/import closure defects. |
| C-prime `ecdf5a55`, C2 `c2aea75c`, C3 `ebc75340` | Closed relationship registration, public package roots, entrypoints, attestation registration, and Router selections. | Explicit membership and machine-enforced import ownership cannot be replaced with path inference, prose inventories, or smoke tests. |
| C4 `b92ed782` | Added `SnapshotVersions`, `NavigationVersions`, and `AnalysisVersions` to repair ambient reconstruction. | Rejected after the authority-scope standards showed those records copied independently owned promises and caused broad invalidation. |
| C5 `4f69f994` | Replaced version bags with content snapshots, owner-local semantic objects, reference-only authority views, `AuthorityBoundValue`, and generated execution closure. Provider and authorization authority became transition-only. | This is the first precedent for much of proposed C7. It was not admitted because Git lineage, complete views, current-only closure, Authority/Contracts coupling, and ambient codec/role/operation membership remained. |
| C6 `9794b927` | Removed Git lineage and complete views, separated Authority from Contracts, froze codec and operation catalogs, added side/role roots, and attempted transition-complete analysis closure. | C6 is blocked proposed planning authority. None of these mechanisms has runtime acceptance evidence. |

Primary records are the
[A1 ADR](../../../../decisions/standards-engine-navigation-analysis.md),
[A1 final acceptance](../../standards-engine-navigation-analysis/reports/a1-final-acceptance.md),
[A1b brief](../../standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md),
and [A1b execution ledger](../execution-ledger.md).

## Why C6 Looks The Way It Does

### Transition-complete closure

C5 bound authority used by the current projection. Its review described that
as insufficient for every advertised valid transition. C6 therefore attempted
to include static authority for current projection, dormant applicability, and
future successor work while still requiring fresh provider and authorization
authority to enter only a published successor.

This was a defensive response to the accepted
[immutable-authority closure rule](../../../../../topics/architecture.md), not an
attempt to make trust global. However, C6 never supplied an algorithm that
derives those future dependencies. Its “current execution path” traversal and
“every future transition” promise are inconsistent.

### Roots plus materialized dependencies

C5 introduced both fields. Roots preserve operation, side, role, kind, and
selected semantic identity. The materialized dependency list was intended as
evidence that traversal omitted or added nothing and as a cold-inspection
projection.

The proposed roots-only C7 record is therefore new. It can be correct only if
direct dependencies are immutable, Authority traversal is deterministic, and
tests independently prove that the derived closure is complete. Merely
deleting the stored list would discard C5/C6’s intended omission oracle.

### Snapshot scope, exclusions, modes, and nesting

C6 removed Git commit/tree identities, Adapter kind, tracking, inclusion
explanations, revisions, and worktree observations. It retained scope,
exclusions, modes, directories, symlinks, and nested content because accepted
A1 treated them as the selected filesystem value rather than capture
provenance.

The proposed leaf-only C7 snapshot is not a continuation of an accepted
decision. It is a new authority-scope claim based on the later finding that
Standards Engine semantics consume paths and bytes but not modes, directory
entries, or capture recipes.

### Coherence-rule identifiers

C5 left required-role and coherence behavior in ambient Engine construction.
Its review rejected the absence of an exact catalog. C6 introduced separately
stored operation contracts with role-kind requirements and coherence-rule IDs
to give those promises independent identities.

Removing the IDs is safe only if C7 does not return to ambient rules. The
replacement must be one fully specified, versioned structural algorithm plus
owner-local semantic validation. Exact operation contracts remain required;
the generated dependency matrix remains evidence rather than runtime
authority.

### Codec and Module ownership

C6 froze owner, kind, payload contract, identity domain, and allowed dependency
kinds because C5 relied on ambient registration. It kept domain construction
with domain Modules, composition with Engine/Analysis, and storage integrity
with Authority.

That closed membership is a response to repeated registry, private-import, and
owner-map failures. C7 must complete and mechanically verify it rather than
remove it.

## C7 Precedent Audit

| Proposed C7 decision | Historical precedent | Assessment |
| --- | --- | --- |
| Successor-only provider/authorization binding | Present in C5 and partly in C6; accepted A1 stores broad views in every state. | **Revise and retain.** It corrects C4’s broad trust, but C7 must state that `NextOperation` is structural guidance and that `advance(state, submission, execution_context)` binds fresh trust only in a successful child. |
| `NextOperation` is guidance, not authorization | Accepted since A1 `c7d23dfa`; exact target handles added by repair `51dcd258`. | **Retain.** C6’s future-authority interpretation overstates the accepted contract. |
| `advance(state, submission, execution_context)` | Accepted architecture at `94b295b4`; current implementation hides most context in `AnalysisKernel`. | **Retain internally.** Public `resolve(handle, submission)` may remain small if the facade supplies exact trusted context and the child binds it. |
| Roots-only execution closure | No prior selected design. C5/C6 store roots and transitive dependencies. | **Unproven.** Require a deletion test, cold reconstruction, independent closure-completeness mutation oracle, and proof that derived inspection loses no evidence. |
| Engine-owned closure identity plus Authority traversal | C5/C6 split semantic construction from storage, but they expose no Authority traversal Interface. | **New refinement.** It is justified only if deleting `transitive_closure(roots)` would duplicate generic DAG logic across Engine and Analysis. |
| Generic structural coherence without rule IDs | C5 used ambient structural coherence and was superseded for lacking exact catalogs. | **Do not repeat C5.** Remove IDs only with a complete algorithm owned by a versioned operation-contract codec and machine-verified exact role-kind contracts. |
| Leaf-only snapshot identity | No precedent in A1 or A1b candidates. | **New and high risk.** It needs explicit v11 replacement semantics and dispositions for every old snapshot inspection/test field. |
| Unicode-scalar path components | A1/C6 use repository-relative POSIX strings without a closed component grammar. | **New but bounded.** C7 defines strict UTF-8 components without normalization or case folding and admits only round-trippable Linux/ext4 names. |
| Omit mode, scope, exclusions, directories, and nesting boundaries | Never selected previously. | **New authority-scope decision.** Consumer mutation evidence, not absence of obvious reads, must prove each field immaterial. |
| Direct stored-object inspection | Introduced in Candidate C and retained through C6. | **Strong precedent.** Keep it. Inspection must not rerun current semantic operations or require source, caches, providers, or authorization services. |
| Exact operation dependency matrix | C5/C6 treat the matrix as generated evidence; C6 separately stores operation role contracts. | **Keep that distinction.** Correct route/read/related/analysis contracts, but do not make a handwritten matrix a second runtime authority. |

## Critical Findings For The Proposed C7

### Stronger than C6

The following corrections are supported by current implementation evidence and
do not revive a rejected design:

- route directly consumes metadata, routing, and graph;
- read and related directly consume metadata and graph;
- analysis consumes metadata, graph, policy impact, and coverage, but not
  routing;
- inspection should directly resolve stored typed objects;
- provider and authorization authority should affect only decisions and
  successors that consume it;
- result projection must not invoke live providers, authorization, source
  repositories, owner maps, scans, or caches; and
- object-specific semantic identity remains with owning Modules rather than the
  generic repository or public schema.

### Requires revision rather than immediate acceptance

1. **Closure evidence:** roots-only storage is simpler but historically
   untested. C7 must prove deterministic traversal and omission detection before
   deleting the materialized dependency evidence.
2. **Coherence ownership:** opaque IDs are incomplete, but deleting them without
   a complete executable structural contract returns to C5’s ambient behavior.
3. **Snapshot identity:** leaf-only path/byte identity is new. It changes
   accepted A1 inspection behavior and reduces native worktree support. It must
   be an explicit v11 replacement with complete consumer dispositions.
4. **Capture integrity:** C7 must resolve one tree from one commit, use a second
   complete manifest for mutable capture, and use descriptor-relative
   no-follow reads. Current A1 and C6 prose do not close create/delete,
   rename, symlink, or ABA races.
5. **Nested repositories:** flatten only when exact nested objects resolve.
   Missing objects are `unavailable`; Git locator identity must not substitute
   for selected content.
6. **Capture provenance:** removing provenance from semantic identity is
   correct. Whether to discard it entirely or emit a non-authoritative capture
   receipt remains an explicit decision because accepted A1 exposed commit and
   source facts for audit.
7. **Trust records:** provider and authorization kinds require exact payload,
   identity, validation, dependency, and outcome contracts before cold
   reconstruction can be claimed.
8. **Machine closure:** codec membership and operation contracts cannot exist
   only in Markdown while runtime injection owns a different set.

## Historical Regression Guard

C7 must retain these defenses that arose from actual failures:

- the selected external Draft 2020-12 validator and complete generated public
  algebra;
- separate schema equality, domain equality, and identity encoding;
- direct immutable storage for every advertised handle;
- explicit relationship, policy-unit, attestation-source, suite, package, and
  public-import membership;
- AST-backed private-import enforcement and safe-path entrypoint execution;
- exact negative diagnostics that reach their intended failure;
- coverage authority freeze before attestations and certificates;
- atomic source, policy, schema, facade, test, and migration cutover;
- exact codec membership with missing, extra, and wrong-owner negatives; and
- content-bound review and lifecycle evidence recorded with coherent outcomes.

Removing any of these would repeat a documented A1 or A1b repair class.

## Recommendation

The research does not justify accepting C6, and it does not yet justify
accepting the assembled C7 design unchanged.

It supports creating a distinct blocked C7 planning candidate that:

1. records C6 as rejected and superseded by identified C7 material content;
2. preserves direct storage, exact machine membership, operation-specific
   authority, atomic migration, and cold inspection;
3. adopts the corrected operation dependencies and successor-only trust
   semantics;
4. resolves roots-only closure evidence, executable coherence ownership,
   snapshot field dispositions, capture races, nested-object resolution,
   provenance, platform scope, and exact trust records before admission; and
5. obtains one content-bound review of the complete C7 material design without
   prescribing Git topology or standalone lifecycle commits.

The correct current decision is therefore:

- **go** for research-backed C7 planning;
- **no-go** for accepting the current conceptual C7 as final design; and
- **no-go** for runtime implementation.
