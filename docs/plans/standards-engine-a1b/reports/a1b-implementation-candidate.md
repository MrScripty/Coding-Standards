# Standards Engine A1b Implementation Candidate

**Status:** `Rejected by final content-bound review`

**Implementation commit:** `8b8a4b481d4e330e118f879a862d2a3630c85f84`

**Implementation tree:** `3435dd4e7cd5784913389f53fb90d6fbb06b73d7`

**Recorded:** `2026-08-28`

**Review subject:** The material A1b implementation content identified by the
commit and tree above. Candidate and acceptance reports added afterward are
evidence about that content and do not invalidate the reviewed subject. Only a
material change to the identified implementation content requires a new review.

This candidate superseded rejected implementation commit
`3da674c1227a8ff6544e846a252a21a255854f49`, tree
`63d55780f77c7f1af64762b6363b8ba776e7fd51`, and the subsequent staged
correction candidates. It is the first complete Milestone 3 implementation
boundary submitted for Milestone 4 content-bound acceptance. Independent review
rejected it because the governed-source scanner used textual position instead
of Python binding lifetime and three Verifier Git call sites bypassed the
sanitized authority Adapter. It must not be used as A1B-A11 evidence.

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

1. centralizes Git-index access and sanitizes inherited `GIT_*` state;
2. places suite-input manifests and coverage-horizon composition under
   Standards Analysis ownership;
3. binds checks to typed authority inputs instead of package-wide ambient
   repository state;
4. binds Numeric Lifecycle evidence to the canonical inventory and exact
   checker source bytes;
5. materializes and compares the staged index through the shared authority
   adapter;
6. rejects dynamic-import capability through a lexical package AST analysis
   that preserves Python module, function, class, and comprehension scope;
7. derives codec-closure evidence from production composition rather than a
   parallel catalog; and
8. renews coverage only after the provider-v5 and horizon-v5 authority inputs
   are frozen.

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
| Standards Verifier | 414 tests passed |
| A1b public cutover | Generated-contract semantic conformance, immutable-authority closure, and public-cutover suites passed |
| Generated projections | Fresh against their authoritative inputs |
| Declarative verification | 226 of 226 registered suites passed |
| Migration verification | All 53 retained Bash migration checkers passed without extension |
| Repository hygiene | Plan structure and staged diff checks passed |

The worktree was clean when the implementation commit and tree were recorded.

## Review Disposition

The review reproduced the reported broad gates but found missing regressions for
assignment RHS ordering, deletion lifetime, exception aliases, and ambient Git
overrides. `A1B-028` is reopened; Milestone 3 is `Active`; the ADR remains
`Proposed`; and Milestone 4, A1B-A11, and A2 remain unavailable.
