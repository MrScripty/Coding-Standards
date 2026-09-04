# Authority-Scope Standards And Impact Review

**Status:** `Reviewed`

**Review date:** 2026-08-26

**Auditor authority:** `standards.review.audit` supplied by the user-authorized
contract-authority-scope standards change.

## Finding

The standards did not direct authors to build an umbrella schema or increment
one version for unrelated changes. Architecture already required separation
when concerns change for different reasons, and Contracts already warned in
the language-binding case that one release input or version identifier does not
create one compatibility promise.

The admission system nevertheless had three general gaps:

1. Concern separation was review guidance, but there was no explicit admission
   record before a module or artifact became canonical for several concerns.
2. Contracts distinguished declaration and executable owners for generated
   keywords, but did not state generally that containing or annotating domain
   semantics does not transfer their authority to the declaration.
3. The strongest version-scope rule was nested under Cross-Language Contract
   Selection. Same-language schemas, manifests, registries, persisted handles,
   and other contract artifacts did not receive the same explicit rule, and no
   general rule tied identity invalidation to a material change in reproduced
   meaning.

This was an admission design flaw in the standards system: the correct design
principle existed in fragments, but the routed policy, planning projection,
decision evidence, and semantic-impact graph did not make it a concrete gate.
It made the problematic design admissible; it did not make that design
inevitable or excuse the local ownership decision.

## General Correction

| Authority | Disposition | General effect |
| --- | --- | --- |
| Architecture Concern Boundaries | retained | Still owns the basic separate-or-keep-together decision. |
| Architecture Authority Scope Admission | added | Requires owned versus referenced concerns, owners, lifecycles, and change reasons before multi-concern canonical authority is admitted. |
| Contracts Artifact Necessity And Authority Placement | retained | Still rejects purposeless mirrors and misplaced authority. |
| Contracts Declaration And Semantic Authority | added | Separates declaration representation from executable and domain-semantic ownership without forbidding a coherent single owner. |
| Contracts Version Scope And Invalidation | added | Scopes versions to compatibility promises and identity invalidation to material meaning. |
| Generated Contract Semantic Conformance | retained | Continues to own complete generated semantics and independent conformance evidence. |
| Generated Contract Semantic Closure | modified, semantic revision 2 | Projects the new owned/reference and version/invalidation decisions at generated boundaries. |
| Contracts Cross-Language Contract Selection | retained | Its artifact classification, generation, publication, and binding-cohort specialization remains useful; the new rule generalizes rather than contradicts it. |
| Contracts Identity And Instance Equality | retained | It owns equality domains, not version-scope admission. |

No normative rule was removed. The audit found no obsolete or contradictory
authority: deleting any row marked retained would remove a distinct decision
or boundary specialization. Adding a universal schema count, maximum version,
file-size limit, or mandatory decomposition pattern was rejected because none
of those measures responsibility coherence.

## Consumer Dispositions

| Surface | Disposition | Reason |
| --- | --- | --- |
| `CORE-STANDARDS.md` | no change, no new direct edge | Core already owns general simplicity and single-authority principles; the concrete admission belongs to Architecture and Contracts. |
| `STANDARDS-ROUTER.md` and routing fixtures | no change, no new direct edge | Architecture, Contracts, and Generated Contract applicability did not change. |
| `topics/architecture.md` | canonical policy change | Owns responsibility and authority placement. |
| `topics/contracts.md` | canonical policy change | Owns declaration semantics, compatibility, version, and invalidation behavior. |
| Generated Contract profile | text, semantic-revision, fixture, and graph update | Direct specialization of both new decisions. |
| Library profile | graph-only direct consumer | Already separates coherent reusable behavior and routes public/generated/persisted versioning. |
| Language Binding profile | graph-only direct consumer | Already keeps adapter representation separate from domain behavior and rejects version-string cohort inference. |
| IPC profile | graph-only direct consumer | Its schemas, decoders, dispatch, and version markers consume declaration and compatibility decisions. |
| Persistence profile | graph-only direct consumer | Already delegates supported-version and evolution semantics to Contracts. |
| Build workflow | graph-only direct consumer | Already owns derivation actions rather than generated content authority. |
| Release workflow | graph-only direct consumer | Already derives release units and version choices from compatibility promises. |
| Planning and implementation prompts | text and graph update | They now require authority, change-axis, version, and invalidation decisions before work proceeds. |
| Plan template | text and graph update | Its optional simplicity review now records canonical/reference authority and version/invalidation scopes. |
| Authored A1 interface schema | graph-only implementation impact | It is a current multi-concern declaration and version source; the relationship records review impact without putting A1 policy into the standard. |
| Contract generator, validator, generated model, and public facade | graph-only implementation impact | They project or execute the declaration and therefore consume semantic-owner or version scope. |
| Analysis snapshot and resolution implementations | graph-only implementation impact | They include or enforce interface versions in provenance and identity-sensitive state. |
| Security, resilience, concurrency, dependencies, diagnostics, and unrelated application profiles | no new direct edge | Their policy may compose with an affected change, but none directly projects the new authority or version decision. Existing Generated Contract dependency edges remain intact. |

A graph relationship records semantic impact; it is not a claim that a current
implementation already conforms. In particular, the local A1 consumers remain
eligible for their separately planned redesign without creating a
repository-specific exception in these standards.

## Decision Evidence

The registered `contract-authority-scope` suite owns three independent decision
tables:

- authority scope admits coherent deep modules and explicit references while
  requiring separate authority for independently changing umbrella concerns;
- declaration authority admits coherent single ownership and explicit external
  semantic owners while rejecting annotation-based ownership transfer; and
- version scope admits one coherent promise or separate versions while
  rejecting file/build/release coupling and unrelated identity invalidation.

Each table includes missing or contradictory authority outcomes. The suite also
checks the canonical policy, Generated Contract profile, both prompts, and plan
template, so a prose-only correction cannot satisfy acceptance.

## Policy-Impact Graph Review

The pre-change compiled graph contained 57 nodes and 207 relationships. The
reviewed graph contains 61 nodes and 251 relationships: four evidence nodes and
44 direct semantic relationships were added.

| Policy unit | Direct relationships after change |
| --- | ---: |
| `topic.architecture.authority-scope-admission` | 10 |
| `topic.contracts.declaration-and-semantic-authority` | 14 |
| `topic.contracts.version-scope-and-invalidation` | 17 |
| `profile.boundary.generated-contract.semantic-closure` | 13 total, including 3 new relationships |

The four catalog additions are the three decision fixtures and their registered
enforcement suite. Every new relationship names that registered suite as its
evidence owner. The compiler resolves every source to a current policy unit,
every target to canonical metadata or a supplemental catalog node, and every
relation to the version-2 authoring contract. No Router edge was added because
the routing facts and selected module closure are unchanged.

## Exact Coverage Review

The final authority contains 44 active policy units under eight owner-local
attestation sources. The provider-v3 horizon expands because canonical policy,
suite registration and content, fixture inputs, supplemental graph nodes, and
relationship declarations changed. Consequently every prior requirement is
stale even where its policy unit and direct relationships are unchanged.

For renewal:

1. Resolve all active policy units and their current semantic revisions,
   representation digests, structural digests, and owner-local attestation
   sources.
2. Compile the 61-node, 251-relationship graph and inspect the exact direct
   consumer sets above.
3. Reuse the prior complete consumer dispositions only where policy text,
   relationships, and target semantics are unchanged; bind them to the new
   independently derived horizon rather than copying old handles.
4. Apply this report's consumer dispositions to the three new units and the
   revised Generated Contract semantic-closure unit.
5. Derive one current requirement per active subject, issue one complete
   owner-local attestation with no exclusions, and compare policy-unit,
   requirement, attestation, and generated-certificate subject sets exactly.

The prior full-horizon review remains available in
`docs/archive/plans/standards-engine-policy-impact-authority-v2/reports/certify-recovered-coverage.md`.
It is supporting evidence for unchanged dispositions; this review owns the
new and revised policy and topology.
