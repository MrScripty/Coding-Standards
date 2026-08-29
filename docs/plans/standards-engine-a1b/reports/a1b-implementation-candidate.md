# Standards Engine A1b Implementation Candidate

**Status:** `Accepted by final content-bound review`

**Implementation commit:** `84412f22fa9fe082f089eaa347c30c23f185ffee`

**Implementation tree:** `8e0f96a61fcea2398418b17d16a061c20f7463f5`

**Recorded:** `2026-08-29`

**Review subject:** The material A1b implementation content identified by the
commit and tree above. Candidate and acceptance reports added afterward are
evidence about that content and do not invalidate the reviewed subject. Only a
material change to the identified implementation content requires a new review.

This candidate supersedes rejected implementation commit
`88f93a33e490373fd32106d163795d21d0bd3eb7`, tree
`69b7cc8f2222cc766b1885ac70187cc0e77fea73`. The replacement preserves the C7
architecture while correcting the conditional branch-exit, nested-scope
capability-provenance, and augmented-assignment-order defects found by that
review. The rejected boundary remains historical evidence and is not used for
A1B-A11.

## Candidate Scope

The candidate completes the C7 replacement of A1 with:

- the exact locked `jsonschema==4.26.0` and `referencing==0.37.0` dependency
  closure recorded in [dependency provenance](a1b-dependency-provenance.md);
- codepoint-preserving identity encoding v2 and owner-local semantic identity
  contracts;
- one generated v11 request/result algebra owned by Standards Contracts;
- exact path/raw-byte content snapshots and a bounded authority-envelope v1;
- one immutable SQLite schema-v1 authority repository with owner-local codecs;
- reference-only standards authority views and roots-only execution closure v2;
- independently identified route, read, related, and analysis operation
  authority contracts;
- direct provider and authorization authority consumed only by successful
  analysis transitions; and
- one immutable, branchable analysis state with cold-process inspection of
  every advertised public object family.

The exact contract, object-kind, compatibility, role/cardinality,
direct-dependency, authority-view, execution-closure, and trust selections are
enumerated in the [C7 design](c7-design-proposal.md), [schema and domain
audit](schema-and-domain-contract-audit.md), [authority composition and
execution closure](authority-composition-and-execution-closure.md), and
[cutover evidence](a1b-cutover-evidence.md). Those records are incorporated as
candidate evidence rather than copied into another authority catalog.

## Corrected Review Findings

The completed boundary incorporates every prior correction and additionally:

1. exposes one typed, sanitized `git_command` result through the public
   Standards Authority root;
2. maps Git process unavailability and nonzero status into public
   Git-reachability diagnostics without a second subprocess owner;
3. joins every already-supported branching visitor through one abstract state
   operation that distinguishes definite binding from possible `sys`
   provenance;
4. preserves possible unbinding across one- and two-armed conditionals, loops,
   and `try` paths;
5. carries possible `sys` capability provenance into nested-scope lookup;
6. evaluates ordinary and augmented assignment in target/value load then store
   order while preserving left-to-right chained targets;
7. verifies hostile inherited Git state and unavailable Git through the direct
   public reachability entrypoint; and
8. registers the retained Git-reachability implementation as an exact node and
   source-owned dependency-policy consumer with a mechanically derived
   migration disposition.

The package scanner treats class namespaces according to Python name-resolution
semantics: direct class-body statements observe ordered class bindings, while
nested methods and comprehensions do not close over class locals. Focused
regressions cover both accepted and rejected cases.

## Migration And Coverage

- Accepted and proposed policy-impact source registries compile through the
  same production path.
- Selected consumer subjects exactly equal recorded disposition subjects.
- Required coverage subjects exactly equal valid certificate subjects.
- All 47 current coverage attestations in the ten registered owner files bind
  provider version 5 and horizon version 5; no provider-v4 or horizon-v4
  record remains current.
- Repository claim sources contain stable semantic selectors rather than
  generated handles or digests; Analysis derives current requirements,
  grants, attestations, and certificates.
- Generated Python contract output is fresh against the canonical v11 schema
  and interface contract.
- Every public package manifest declares its direct dependencies, public root,
  static exports, Python range, and repository entrypoints.
- Superseded validator, serializer, generator, storage, coverage, and
  compatibility paths are unreachable or deleted as required by the plan.
- No mutable catalog or relationship-count oracle is used as acceptance
  evidence.

## Verification

The clean implementation tree passed:

| Evidence | Result |
| --- | --- |
| Standards Authority | 39 tests passed; one capability-selected skip |
| Standards Analysis | 66 tests passed |
| Standards Engine | 36 tests passed |
| Standards Contracts | 18 tests passed |
| Standards Verifier | 433 tests passed |
| CPython 3.11 and 3.12 correction matrix | 45 governed-source and Git-reachability tests passed in each exact locked environment |
| A1b public cutover | Generated-contract semantic conformance, immutable-authority closure, and public-cutover suites passed under hostile inherited `GIT_DIR` and `GIT_INDEX_FILE` on both supported Python versions; direct public reachability regressions also passed |
| Generated projections | Fresh against their authoritative inputs |
| Declarative verification | 226 of 226 registered suites passed |
| Migration verification | All 53 retained Bash migration checkers passed without extension |
| Repository hygiene | Plan structure and staged diff checks passed |

The worktree was clean when the implementation commit and tree were recorded.

## Review Disposition

Independent content-bound review found no Standards or Specification defect in
the exact commit and tree above. The boundary is accepted by the
[final acceptance record](a1b-final-acceptance.md). `A1B-028` and the stale
`A1B-004` lifecycle projection are `resolved`; Milestones 0 through 4,
A1B-A11, the plan, and the ADR are `Accepted`. A2 remains inactive pending its
own review and admission.
