# Standards Engine A1/A1b Audit: Final Synthesis

**Status:** Accepted for `AUD-A6` and verified under `AUD-A7`.

**Fixed observations:** original accepted A1 v9 at `2359a98740b6035a0414bfaf5427ceaa1301a1c8`,
accepted A1-derived v10 amendment at `7bc8bd070f882eb9779dc678139777d05a6ce7c7`,
A1b plan/standards base at `36dd75790b2f08a6e66624ccae4f8530bc111a92`,
and accepted A1b at `84412f22fa9fe082f089eaa347c30c23f185ffee`.

This report integrates the commit-pinned [A1 history](a1-history-and-design.md),
[A1b history](a1b-history-and-design.md), [standards causal history](standards-evolution-and-causality.md),
[architecture comparison](architecture-and-complexity-comparison.md),
[consumer and threat-model audit](consumer-guarantee-and-threat-model.md), and
[verification audit](verification-portfolio-audit.md). Historical facts remain
owned by those reports and their immutable sources. This report owns the
cross-report conclusions and recommendations.

## Executive Verdict

The concern that A1b became larger and more complex than its product behavior
alone requires is supported. The important qualification is that A1b is not
merely A1 with gratuitous structure. It corrects a reproduced external JSON
Schema conformance defect, separates identity from equality, removes several
conflated semantic authorities, makes dependency closure explicit, and
supplies stronger persistence and replay guarantees. Those are real merits.

The excess-risk finding is cumulative: locally coherent Modules, records,
versions, codecs, validators, stores, closures, policy relationships, and
verification mechanisms compose into a system whose total reasoning and
change cost was never subjected to an equally strong whole-design admission
test. From the immediate A1b base to accepted A1b, the selected production
ecosystem grew from 96 to 125 Python files, 29,733 to 38,410 lines, and 22 to
36 internal package dependency directions. Generated contract code became
smaller, so the growth is predominantly handwritten authority, contract,
composition, and verifier machinery. These counts locate the growth; the
change-history, deletion tests, and Interface analysis establish its design
significance. See the [architecture comparison](architecture-and-complexity-comparison.md).

The standards share responsibility, but “the coding standards caused A1b” is
too broad. Some later design choices were directly standards-influenced:
authority/version rules explicitly rejected an earlier umbrella design, and
the C6 history calls its transition-complete closure a defensive response to
Immutable Authority Closure. Other choices—SQLite, the exact number of stored
objects, owner-codec shape, and the governed-source AST implementation—were
selected implementations, not prescribed structures. A1b's initial design and
the recovery rules also share one defect analysis, so early compliance is
common-cause evidence rather than independent causation. The detailed causal
classification is in the [standards report](standards-evolution-and-causality.md).

The central standards failure was not an absence of all simplicity or
verification guidance. Pre-A1 standards already required least sufficient
structure, conditional security, objective-aligned evidence, proof-bearing
types, and no redundant decoding of an intact validated value. The failure was
that planning and review could admit every local addition without requiring
the composed result, the marginal value of permanent evidence, or the relevant
failure/threat model to be reconsidered. Some guidance was also ambiguous:
Contracts' proof-lifetime rule rejects redundant internal decoding, while its
Invariant Contracts wording can be read to demand supported runtime machinery
for every internal violation.

A1c should therefore not return to A1. It should preserve the corrected Draft
Adapter, small deep Identity and Contracts Modules, four-operation product
Interface, explicit uncertainty, domain-owned semantics, and non-ambient
behavior for whatever replay lifetime is actually promised. It should test
whether universal durable child-object replay, fourteen independently public
stored kinds, broad internal root Interfaces, the cumulative version matrix,
and custom governance interpreters can be removed or aggregated. That is a
smaller design target without discarding the evidence that made A1b better.

No independent external Engine consumer was found at any fixed observation,
and no retained A1 state was found. In accepted A1b, `open_persisted` has only
test callers and backup/restore has no operational caller. That makes A1b an
assurance-maximal implementation of plan-selected guarantees rather than a
shape forced by observed deployment. Plan authority is still legitimate; the
finding means A1c must state its intended caller, handle lifetime, retained
state, and loss consequences instead of treating A1b's capabilities as
consumer facts. See the [consumer and threat-model audit](consumer-guarantee-and-threat-model.md).

## How The Audit Revises The Earlier Understanding

| Earlier working belief | Revised finding | Basis and confidence |
| --- | --- | --- |
| `interface_schema_version = 11` means there were eleven released or accepted schemas. | It is a monotonic allocation/design-iteration ordinal. The canonical schema moved through pre-acceptance milestones, a planned v7 with no committed v6/v7 schema, withdrawn v8/v9 candidates, and later accepted v9, v10, and v11 boundaries. There were not eleven supported migrations or deployed generations. | [Architecture version reconstruction](architecture-and-complexity-comparison.md#why-interface_schema_version-is-11), high. |
| The schema crossing many package boundaries is itself the design flaw. | A wire schema may legitimately project values owned by several Modules. A1's flaw was claiming representation, validation, identity-related serialization, state-machine, projection, and domain semantics through one declaration whose executables disagreed. A1b correctly narrows schema authority, although its many public object concepts still make schema coordination broad. | A1 repair history and A1b schema/domain audit, high. |
| A1 had a tiny public Interface and A1b greatly enlarged it. | Both Engine roots are broad generated algebras around four primary verbs. A1 v9 had 139 generated plus six handwritten root exports; A1b has 142 plus four. A1b's main regression is composition and governance burden behind the facade, not root export count. | Reproducible AST inventory, high. |
| A1b mainly bloated `standards_engine`. | The Engine package total actually shrank by 278 lines from the base, although `engine.py` grew from 1,600 to 2,539. Most net growth moved into Authority, Contracts, Identity, and Verifier; Verifier alone added 3,638 production lines. | Reproducible inventory, high. |
| All A1b machinery follows from fixing A1. | A1b combines a demonstrated external semantic repair, retained A1 product behavior, newly selected durability/replay/platform guarantees, standards-driven ownership/evidence obligations, and review-driven enforcement. The fix does not determine one unique implementation. | A1b history and guarantee normalization, high. |
| The standards lacked simplicity guidance. | Strong general simplicity guidance existed before A1. What was missing was an enforceable cumulative admission test for Depth, Interface burden, Locality, and marginal machinery; some relevant guidance was missed, unrouted, or ambiguous. | Standards chronology, high. |
| Large test/checker counts prove redundancy. | Counts prove accumulation and cost, not redundancy. Removal needs a claim-level analysis of reachable failure, consequence, oracle, overlap, static/construction proof, diagnostic value, and lifecycle. Several evidence families have demonstrated consolidation paths; the 53 inherited Bash checkers remain unresolved individually. | [Verification portfolio audit](verification-portfolio-audit.md), high for the rule and named overlapping families. |
| File hashes are generally unnecessary. | A digest is justified when it is a content identity, supply-chain selection, publication/restore integrity, or freshness boundary required by a real lifetime. It is weak when it freezes incidental bytes whose meaningful change is already detected by a nearer semantic, capability, or integration check. Purpose and threat model—not the primitive—decide. | [Hash purpose audit](verification-portfolio-audit.md#hash-and-digest-purpose-audit), high. |

The most consequential correction is the distinction between a deep external
Interface and a simple implementation. Both A1 and A1b provide high Leverage
through four verbs, but both expose a broad value algebra and coordinate many
internal owners. External Depth is a merit; it is not evidence that internal
reasoning is proportionate.

### Verification-specific corrections

- Accepted A1 had 581 named package tests, 218 suites, and 53 Bash checkers.
  Accepted A1b reported 679 broad tests, while its named package rows sum to
  677; it had 226 suites and the same 53 checkers. Only three added suites are
  A1b-specific; five came from general standards recovery. The unexplained
  two-test discrepancy is retained rather than normalized.
- A1's two local schema implementations passed together while sharing the
  wrong Unicode equality rule. More checks did not compensate for a
  non-independent oracle.
- A1b selects the correct Draft implementation but applies it repeatedly:
  facade prevalidation, generated decode, nested model normalization, result
  conversion, and facade output validation. The safe simplification is one
  validation per real proof boundary and immutable proof-bearing values—not
  trust in unenforced Python annotations.
- The generated suite-input authority is approximately 788 KiB/25,938 lines
  and binds 917 files across 3,672 uses. It proves input-byte invalidation, not
  that each suite remains a semantically adequate oracle.
- The package-governance family includes a 1,419-line Python analyzer, a
  262-line declarative Adapter, a 713-line unit-test file, 32 unit tests, 17
  overlapping declarative cases, and a 45-test matrix on two Python versions.
  Its failures matter for architecture discipline and clean execution, but its
  admitted profile is non-adversarial and does not justify treating the custom
  analyzer as a security barrier.

These facts support portfolio consolidation and A1c design deletion. They do
not prove the 53 inherited checkers or every individual internal test
unnecessary. The full matrix is in the [verification audit](verification-portfolio-audit.md).

## What A1 And A1b Each Demonstrate

### Merits to preserve from A1

- A read-only product can expose `query`, `prepare`, `resolve`, and `inspect`
  while hiding path discovery, graph traversal, applicability, policy impact,
  analysis fixed points, and rendering. This is genuine Interface Depth and
  high Leverage.
- The product boundary remained disciplined: no authoring, application,
  semantic approval, rollback, or arbitrary prose interpretation.
- Three-valued applicability, typed rejected outcomes, immutable results, and
  explicit handles avoid plausible-looking guesses.
- The single immutable `AnalysisState` deleted packet/report/session and global
  supersession machinery. It is historical evidence that simplification can
  improve correctness.
- Memory and directory state stores were two real Adapters behind a small
  persistence Seam, and the standard-library-only operational profile made
  fewer promises.

### A1 defects not to restore

- One schema declaration was treated as authority for several independently
  changing semantic families. Local validation and generated decoding agreed
  with each other while disagreeing with Draft 2020-12 for codepoint-distinct
  Unicode values. Local agreement was not an external oracle.
- The generic canonical identity serializer influenced instance equality,
  deduplication, and identity without keeping their domains sufficiently
  separate.
- A1's generated and handwritten Interfaces were already broad, and important
  changes propagated through schema, identity, analysis, Engine, fixtures,
  coverage, and verifier surfaces.
- Acceptance followed two withdrawn acceptances and five rejected repair
  candidates. The process caught defects, but also shows that passing local
  portfolios did not establish external semantic conformance or whole-design
  simplicity.

### Merits to preserve from A1b

- Contracts is a deep external-standard Adapter: it hides Draft selection,
  reference resolution, profile admission, validation, projection, and typed
  failures behind a smaller Interface. Deleting it while retaining the public
  JSON Schema contract would scatter those concerns.
- Identity is a small deep Module: it owns byte framing and hashing while
  leaving domain equality, ordering, and deduplication with domain owners.
- Authority does not import Contracts or domain semantics. Opaque persistence
  plus owner codecs preserves correct dependency direction.
- The schema's five custom semantic-extension families and the local Draft
  interpreter were removed rather than layered with another fallback.
- Memory/SQLite stores and Git/native capture are real Adapter pairs. C7 also
  removed substantial C6 machinery while keeping its admitted replay and
  durability guarantees.
- No compatibility reader was retained because no external consumer or stored
  predecessor state required one.

### A1b mechanisms to challenge in A1c

- A universal rule makes fourteen public handle kinds independently stored,
  identified, encoded, dependency-tracked, decoded, inspected, versioned, and
  migrated. Coherence is proven; independent consumer need is not.
- Durable SQLite publication, capability probing, backup/restore, interruption
  tests, platform/wheel constraints, and dependency provenance are real costs.
  They are proportionate only if the corresponding lifetime and recovery
  promises serve an actual consumer.
- `engine.py` is a composition concentration point for codecs, authorities,
  closures, trust, stores, operation roots, projection, and inspection.
- Internal package-root Interfaces are broad partly because repository policy
  requires all cross-module imports through exported roots. That turns
  implementation composition into formal Interface surface.
- A public inspectable-kind change structurally crosses owner model, identity,
  codec, dependencies, storage admission, schema, Engine composition,
  migration, coverage, and verification. Owner-local semantic changes can have
  good Locality; cross-Interface changes are intentionally expensive.
- The final rejected implementation boundaries were dominated by custom AST
  package/Git/source enforcement rather than the four product operations.

The deletion test separates justified foundations from promising
simplifications. Deleting Identity, Contracts, or neutral graph/metadata
owners while retaining their responsibilities would move complexity into
callers. Reducing the durability promise or aggregating child authority can
make Authority, codec, version, storage, and evidence machinery disappear.
Those are stronger A1c experiments than merely merging files or renaming
packages.

## Standards Findings And Proposed Changes

These are project-agnostic changes supported by the audit. They are proposals
for a later normative plan, not edits made here. Each proposal preserves the
current ban on choosing designs from raw line, file, type, dependency, or test
counts.

### S1. Admit composed design Depth, Interface burden, and Locality

**Change:** Amend Core's Simplicity and Ownership and Architecture's Concern
Boundaries/Authority Scope Admission so an architecture is evaluated both
locally and as a composition. A material design should identify its supported
Interfaces, caller knowledge, composition-root knowledge, representative
change paths, and deletion result. A Module is deep when its Interface hides
substantially more reasoning than it exposes. A Seam needs one hypothetical
Adapter to test its shape and normally two real Adapters to justify permanent
generality.

**Reason:** Current rules decide whether each concern has a coherent owner, but
do not decide whether the collection of owners produces useful overall Depth
or acceptable Locality. A1b can satisfy every local ownership decision while
requiring a new public kind to cross nine coordinated surfaces.

**Evidence:** Stable four-verb product Interface; `engine.py` growth; 22-to-36
dependency-direction growth; fourteen-kind propagation path; v10 and v11
multi-owner cutovers; policy-graph fanout. **Counterevidence:** Identity,
Contracts, neutral graph owners, and real store/capture Adapters pass the
deletion test. The rule must not collapse coherent owners into a shallow
monolith. **Confidence:** high.

### S2. Require least-sufficient-machinery and cumulative admission

**Change:** Strengthen planning and architecture admission for every material
new Module, representation, version, registry, validator, store, cache,
protocol, or custom verifier. Record the unique reasoning, risk, or consumer
obligation it removes; a simpler considered alternative; what would fail if it
were absent; and the condition under which it can be removed. Re-run the
cumulative review after systemic replanning or when several locally justified
mechanisms compose into a new operational obligation.

**Reason:** Core already says “least code and structure,” but no fixture,
planning gate, or review protocol forces the claim to be demonstrated. A1b's
C1-C7 process repeatedly proved local correctness without a final comparison
against a bounded aggregate architecture.

**Evidence:** C1-C7 growth and simplification; Authority/version fixtures that
decide coherent ownership one scope at a time; fourteen independently coherent
stored objects; accepted operational matrix. **Counterevidence:** Some
one-call-site boundaries are still justified; this is a reasoning gate, not a
construct-count threshold. **Confidence:** high.

### S3. Add evidence necessity, marginal value, and lifecycle

**Change:** Add a Verification policy unit that distinguishes “this check can
prove a claim” from “this claim needs this permanent check.” For each material
check or evidence family, record:

1. the reachable failure or change it detects;
2. material consequence and affected trust/correctness boundary;
3. the deciding independent or authoritative oracle;
4. why types, construction, static analysis, a deeper Interface check, another
   check, normal failure, or trace-led debugging do not already cover it;
5. overlap and intentional defense in depth;
6. execution, maintenance, and diagnosis cost; and
7. retention/removal trigger.

Prefer the smallest portfolio that covers the named claims. A regression test
for a defect is not automatically permanent when the defect class becomes
unrepresentable or is subsumed by a stronger, cheaper proof.

**Reason:** Existing Verification is strong about claim selection, oracle
quality, negative-fixture isolation, and evidence fidelity, but does not test
marginal necessity or lifecycle. Core and Implementation can therefore cause
one focused test to accumulate per defect without a later subsumption review.

**Evidence:** 218-226 suites, 53 retained Bash checkers, growing package-test
surfaces, repeated proof mechanisms, duplicated generated freshness/example
checks, overlapping unit/declarative package matrices, and migration evidence
with no retirement event; no current policy unit owns evidence lifecycle.
**Counterevidence:** Repeated independent reviews found real defects, so
count-only deletion is invalid and some overlapping checks may be justified
defense in depth. **Confidence:** high for the standards gap and named
overlapping families; unresolved for the individual 53 inherited checkers.

### S4. Classify failure before selecting validation machinery

**Change:** Amend Contracts' Invariant Contracts and Validation Proof Lifetime
to classify at least:

- unknown or arbitrary external input;
- adversarial input or mutation;
- expected recoverable operational failure;
- internal programming error that fails immediately and is contained;
- internal defect that can silently cross a boundary, corrupt durable state,
  violate authorization, or emit externally trusted output.

Typed decoding and negative-path evidence are required at applicable public,
trust, process, persistence, plugin, queue, independent deployment, or mutable
data boundaries. Intact proof-bearing internal values are consumed directly.
For a contained internal programming defect, an assertion, propagated error,
or diagnostic trace may be sufficient unless the consequence/risk model shows
why supported runtime recovery or permanent validation is needed.

**Reason:** The current proof-lifetime section explicitly rejects decoding the
same unchanged validated value again. The current Invariant Contracts ending
rejects debug-only enforcement, panic, recovery, or graceful abort without
distinguishing contained internal programming errors from corrupting boundary
failures. That ambiguity admits duplicate validators and negative tests even
where invalid values are unrepresentable.

**Evidence:** A1/A1b repeated decoding paths; pre-A1 proof-lifetime wording;
A1b's generated smart constructors; user-observed distinction between
debugging and boundary protection. **Counterevidence:** JSON, SQLite, Git,
process, persistence, plugin, and public values genuinely cross new proof
boundaries. Static types are not proof when unchecked mutation, deserialization,
or independently authored data remains possible. **Confidence:** high. The
verification audit traced the duplicate public path while separately retaining
durable decode, corruption, and interruption evidence.

### S5. Require scoped threat and correctness-risk models

**Change:** Generalize Security's conditional threat-model discipline without
classifying all internal code as hostile. Before admitting validation,
integrity, redundancy, or adversarial evidence, state the actor or failure
source, input authority, mutation capability, boundary and proof lifetime,
failure consequence, detection/recovery requirement, and residual risk.
Permit different models for different Modules and operations.

**Reason:** Arbitrary/user input and externally influenced security surfaces
need strong validation. Pure internal construction often does not. Durable
corruption, concurrency, authorization, and silent external emission may still
justify machinery without an adversary. One scoped format avoids both blanket
trust and blanket suspicion.

**Evidence:** Security's filesystem rules and A1b's SQLite threat model are
positive examples; A1b also accumulated broad hostile-environment matrices
without one common risk-admission rule. **Counterevidence:** A formal security
threat model would be overkill for every internal helper; the proposal includes
correctness risk and is applied only when machinery is material. **Confidence:**
high.

### S6. Make immutable authority closure proportional to promised lifetime

**Change:** Retain the prohibition on ambient substitution, but amend
Immutable Authority Closure so the required closure follows an explicit
consumer promise: supported operations, handle lifetime, process/repository/
deployment lifetime, persistence and reconstruction need, allowed environment
dependencies, authorization lifetime, and failure behavior. Full transitive
content-addressed cold reconstruction is required only when that promise
requires it. An opaque in-process handle or reconstructible cache need not own
the same repository machinery.

**Reason:** The standard's invariant is valuable, but its broad reading helped
turn replay into a structural universal. Closure requirements should follow
the Interface promise, not the existence of any opaque handle.

**Evidence:** Real A1/A1b cold-replay claims; C6's recorded defensive response;
Immutable Authority Closure's relationship fanout from 7 at recovery to 27 at
accepted A1b; fourteen direct stored kinds. **Counterevidence:** If a handle is
advertised as durable and inspectable in a cold process, complete non-ambient
closure is necessary. **Confidence:** high.

### S7. Add cumulative compatibility/version review

**Change:** Retain independently scoped versions when promises really change
independently. Also require each version to name actual consumers, supported
overlap/lifetime, independent deployment or persistence facts, and the
cumulative migration/test matrix it adds. Several scopes may intentionally
move atomically; independent change reasons alone do not require permanent
independent public versions.

**Reason:** The authority/version correction rightly rejected A1's umbrella
invalidation. A1b then acquired many locally valid scopes without proving they
serve independently evolving consumers. The product still performed an atomic
v11 replacement and retained no old readers.

**Evidence:** `interface_schema_version` allocation history; v10/v11 cutovers;
A1b identity/version/object matrix; no retained external A1 state or consumers.
**Counterevidence:** Wire, storage, identity encoding, and domain payloads can
have genuinely different compatibility lifetimes. The rule must not recreate
one global version. **Confidence:** high.

### S8. Give systemic replanning bounded stop and simplification paths

**Change:** Keep sibling-invariant review after a systemic defect, but add
explicit stopping rules: bound the affected semantic family from authority
and reachability; stop when every reachable material consumer is disposed;
accept removal or a smaller Interface as a repair; allow normal failure and
diagnostics for low-consequence contained defects; and do not add a new check
when an existing stronger claim subsumes it. A replan must compare the revised
composition with the pre-finding objective before admitting more machinery.

**Reason:** Systemic replanning prevented A1's example-by-example repair loop,
yet in A1b it repeatedly expanded inventories, catalogs, AST logic, Git
authority, suite-input identities, and evidence matrices. Completeness needs a
definition of the relevant system, not an unbounded search for another
possible representation.

**Evidence:** Five rejected A1 repair candidates; systemic recovery rules;
A1b's repeated C and implementation reviews; final governed-source correction.
**Counterevidence:** The broader reviews found real private-import, capability,
and source-acquisition defects. Stopping rules must be claim- and consequence-
based, not schedule-based. **Confidence:** high.

### S9. Make policy-impact and evidence invalidation dependency-local

**Change:** Retain explicit change-specific consumer disposition and reject an
unaudited empty impact. Amend Projection Completeness/coverage policy so a
bounded semantic change invalidates the changed policy, changed relationships,
affected consumers, and evidence whose deciding authority changed. A provider-
wide horizon or regenerated digest must not automatically renew unrelated
semantic subjects without a stated shared compatibility promise.

**Reason:** Exact graph coverage prevents silent missing consumers, but global
horizon renewal can make evidence identity churn without new semantic proof.

**Evidence:** policy graph growth from 41 policy units/207 direct relationships
at recovery to 47/387 at A1b; one guardrail renewed all 44 subjects; large
relationship and suite-input rewrites accompanying bounded corrections.
**Counterevidence:** Successful empty-impact proof and stale-authority detection
are real governance guarantees. Local invalidation must still detect a changed
edge or missing consumer. **Confidence:** medium-high; a later standards plan
should prototype the invalidation algebra before changing it.

### S10. Retain demonstrated recovery rules

**Change:** Do not remove Generated Contract routing, external semantic
oracles, schema dialect/vocabulary admission, identity-versus-instance
equality, validation proof lifetime, conditional Security, claim-directed
Verification, or non-ambient reconstruction for a genuinely durable replay
contract. Refine their applicability and admission; do not weaken their
semantic outcomes.

**Reason:** These rules address reproduced A1 defects or clear boundary risks.
A1c should trim implementation excess without restoring local Draft
interpretation, umbrella semantic ownership, or ambient fallback.

**Evidence:** Unicode/equality reproduction, routing omissions, snapshot/cold
inspection repairs, and accepted A1b conformance. **Confidence:** high.

### S11. Admit hashes by the identity property they protect

**Change:** Make exact-byte hashes permanent only when literal bytes
participate in content identity, supply-chain selection, persisted
reconstruction, publication/restore integrity, or a recorded legal/release
artifact. Otherwise prefer the deciding semantic, structural, capability,
version, or execution check. Do not copy one authoritative lock or expected
byte list into a second permanent hash table without a different threat.

**Reason:** A digest decides byte identity, not whether byte identity matters.
Treating every hash as either mandatory or wasteful loses the distinction the
user's concern requires.

**Evidence:** Public handle frames, snapshot/Git objects, backup/restore, and
dependency lock hashes protect material identity. A duplicated dependency
`EXPECTED` table, a hash of a script already embedded in a committed report,
and exact host `strace`/license bytes have weaker or incidental claims.
**Counterevidence:** replacing an exact content identity with a version string
or capability probe is weaker when replay or supply-chain integrity genuinely
depends on the bytes. **Confidence:** high.

### S12. Prefer dependency guarantees and established proof tooling

**Change:** Test the project's Adapter, selected capability, and known
regressions rather than reimplementing or exhaustively retesting a mature
dependency's semantics. A custom language interpreter, static analyzer,
validator, persistence protocol, or test oracle needs evidence that established
tools are insufficient for a reachable material failure and a lifecycle owner
for the new semantic product.

**Reason:** Custom proof machinery creates another Module whose own semantics,
Interface, versions, tests, and failures require review. It can consume more
design effort than the application property it protects.

**Evidence:** adopting `jsonschema` removed A1's false local Draft owner; C7
SQLite removed C6's larger application-owned durability protocol; the custom
Python binding/provenance analyzer then caused several late A1b rejection and
repair rounds. **Counterevidence:** established tools do not automatically fit
the exact contract. Adapter-specific behavior, known regressions, clean
execution, and capability qualification still need evidence. **Confidence:**
high.

### Required policy-graph work for a later normative change

The later standards-change plan must query and disposition existing
`policy-impact` relationships before editing owners, create or revise policy
units, and connect only applicable consumers. The likely graph shape is:

| Proposal | Likely policy authority | Direct projections to investigate |
| --- | --- | --- |
| S1-S2 | New `topic.architecture` unit for composed design proportionality, plus Core semantic revision | Planning/implementation prompts, plan template's simplicity review, architecture fixture and suite, Library and Generated Contract profiles where Interface admission applies. |
| S3 | New `workflow.verification.evidence-necessity-and-lifecycle` unit | Planning/implementation prompts, plan template acceptance claims, Verification fixtures/suite, test/coverage documentation; implementation projections only where a checker actually enforces the rule. |
| S4 | New Contracts unit or semantic revisions to Proof Lifetime and Invariant Contracts | Generated Contract, IPC, Language Binding, Persistence, Verification, contract fixtures/suite, prompts/templates, affected runtime boundary implementations. |
| S5 | Scoped risk unit owned by Contracts or Verification with conditional Security relationship | Security/Resilience/Diagnostics, planning and implementation prompts, validation/evidence fixtures, only threat-bearing implementation surfaces. |
| S6 | Semantic revision of `topic.architecture.immutable-authority-closure` | Persistence, Engine/Authority, cold-replay fixtures/suite, and every current implementation projection; remove unconditional projections whose consumer promise no longer applies. |
| S7 | Semantic revision of `topic.contracts.version-scope-and-invalidation` | Public/generated/persisted/binding profiles, Release, prompts/template, schema/interface/generator/runtime projections, cumulative-version fixture. |
| S8 | Semantic revision of `workflow.planning.systemic-finding-replan` | Planning/implementation prompts, plan template, issue record, systemic fixtures and suite. |
| S9 | Semantic revision of `workflow.planning.projection-completeness` and applicable coverage policy | Policy graph compiler, coverage authority, migration/attestation reports, prompts/template, policy-impact fixtures and suites. |
| S11 | New Verification hash-admission unit or a section of evidence necessity | Dependencies, Generated Contract, Persistence, Release/legal evidence, prompts/template, hash-purpose fixture; connect exact implementation artifacts only where bytes are semantic authority. |
| S12 | Core Implementation/Dependencies and Verification semantic revisions | Dependencies and Generated Contract profiles, implementation prompt, dependency/tooling fixtures, selected Adapter and clean-environment suites. |

This is an impact hypothesis, not an authoritative relationship list. The
neutral graph query and owner-by-owner disposition are mandatory because the
existing graph contains hundreds of exact relationships and lexical links do
not establish semantic consumption.

## Evidence-Constrained A1c Direction

### Preserve as behavioral constraints

- Four read-only operations with typed request/result/rejection behavior.
- Explicit uncertainty and no valid-looking fallback for unavailable facts.
- Correct maintained Draft 2020-12 semantics behind a deep Contracts Adapter.
- Domain equality, ordering, deduplication, and identity kept distinct.
- One canonical owner for domain semantics; wire declarations project rather
  than acquire that authority.
- Immutable results and no ambient substitution within the handle lifetime
  A1c explicitly promises.
- Neutral metadata/graph/applicability/policy owners where current multiple
  real consumers still justify them.
- No compatibility shims when consumer, deployment, and retained-state facts
  still show an atomic replacement.

### Treat as hypotheses, not inherited requirements

- Every public child concept needs its own cold-resolvable stored object.
- Durable SQLite authority, backup/restore, and interruption behavior are
  product requirements rather than an optional operational profile.
- Every independently meaningful semantic version needs an independently
  coordinated public version in this atomically deployed product.
- Cross-package imports require a custom governed-source abstract interpreter.
- All generated domain types must be the internal representation rather than
  boundary DTOs.
- Policy coverage identity must renew through one global horizon.
- A failed internal assertion is unacceptable even when it is contained,
  immediately visible, non-corrupting, and well diagnosed.

### Minimum design experiments before A1c admission

1. **Aggregate-state prototype.** Represent navigation and analysis with one
   persisted aggregate each and opaque child references. Exercise every real
   `inspect` workflow and determine which of the fourteen A1b child kinds truly
   needs independent cold lookup.
2. **Lifetime profiles.** Compare in-process, process-restart,
   repository-reconstructible, and durable-archival handles. Price Authority,
   persistence, authorization, backup, and recovery separately for each.
3. **Boundary-only contract model.** Keep JSON Schema and generated DTOs at the
   public Adapter, use domain constructors internally, and validate each value
   once per real proof boundary. Demonstrate exact failure classification when
   proof is lost or data crosses JSON/persistence/process boundaries.
4. **Representative Locality probes.** Before selecting a design, perform an
   added public field, internal field, inspectable kind, identity-rule change,
   and operation compatibility change. Record every Module and Interface that
   must change and why.
5. **Governance alternative.** Compare custom AST/Git analysis with ordinary
   packaging, import-linter/type-checker capabilities, runtime package tests,
   and review. Preserve only protections tied to reachable material failures.
6. **Verification portfolio.** Start from the four-operation Interface and
   named external/persistence/security claims. Add internal checks only for a
   distinct risky invariant that the deeper Interface cannot diagnose or prove
   adequately. Record subsumption and removal conditions from the start.
7. **Version matrix.** Give every proposed version an actual consumer and
   lifetime. Compare separate scopes with one explicit coordinated version
   record that preserves semantic sub-identities without promising independent
   compatibility.
8. **Coverage invalidation prototype.** Show that dependency-local renewal
   catches changed and missing relationships while leaving unrelated accepted
   subjects intact.

### A1c success criteria

A1c is not successful merely because it has fewer lines, types, or tests. It
must satisfy the preserved caller-visible and external-semantic claims with:

- greater Depth at supported Interfaces;
- fewer independently supported concepts for callers and maintainers;
- better Locality on the representative changes;
- no duplicated semantic authority or validation of intact proof-bearing
  values;
- operational obligations matched to explicit consumers and lifetimes;
- a smaller, claim-complete evidence portfolio with stated marginal value; and
- deletion tests showing removed machinery disappeared instead of moving into
  callers.

## Decisions This Audit Does Not Authorize

- No existing test, verifier, hash, contract, version, package, or persistence
  mechanism is declared removable from counts alone.
- No normative standards or policy-graph changes are made by this audit.
- No A1c architecture is selected. The recommendations define preserved
  behavior, admission tests, and experiments for a later design effort.
- A1b's acceptance is not reopened. Acceptance proves that its named claims
  passed at the accepted boundary; it does not prove that every internal
  mechanism is the least costly way to keep those claims true.

## Confidence And Remaining Unknowns

### High-confidence conclusions

- A1b corrects real A1 semantic and authority defects while adding materially
  more handwritten composition, persistence, and governance machinery.
- A1 and A1b both have deep four-operation facades and broad public value
  algebras; the main A1b regression is not root export count.
- `interface_schema_version = 11` records design allocations and incompatible
  cutovers, not eleven accepted/deployed versions.
- Current standards already contain important simplicity, conditional-risk,
  proof-lifetime, and oracle rules. The general shortcomings are cumulative
  admission, failure/risk classification, evidence marginal value/lifecycle,
  and bounded systemic review.
- External Draft semantics, equality/identity separation, non-ambient behavior
  for a promised replay lifetime, and trust-seam/durable-seam validation must
  survive simplification.
- Repeated validation of one intact proof-bearing value, duplicated exact
  freshness matrices, and incidental byte hashes have evidence-supported
  consolidation paths.
- A1c should challenge universal child-object durability, the custom package
  interpreter, byte-complete global suite-input closure, and independently
  versioned internal concepts before challenging the small deep Identity and
  Contracts Modules.

### Medium-confidence or conditional conclusions

- Standards directly influenced authority closure and version decomposition,
  but the proportion attributable to standards versus plan/review/implementation
  choice cannot be quantified.
- Dependency-local policy-evidence invalidation appears feasible, but it needs
  a prototype proving changed/missing edges remain detectable.
- SQLite and its corruption/interruption evidence are proportionate under the
  accepted A1b durability promise. Whether that promise is proportionate for
  A1c depends on deployment and retained-state facts.
- A smaller aggregate can probably preserve useful cold inspection, but the
  fourteen child workflows have not yet been tested against one.

### Unresolved inputs for later work

1. The first real A1c caller and deployment form: in-process agent tool, CLI,
   service, durable appliance, or reusable library.
2. Required handle lifetime and portability across process, repository,
   machine, upgrade, and authorization changes.
3. Which state is non-derivable, how long it is retained, the consequence of
   loss, and who owns backup, cleanup, migration, and deletion.
4. Which child artifacts have independently valuable inspection workflows.
5. Which version scopes have actual overlapping or independently deployed
   consumers.
6. Whether exact historical replay of coverage proof is a product capability
   or repository-governance evidence.
7. Which of the 53 inherited Bash checkers still owns a distinct live claim;
   this requires a separate checker-lifecycle audit.
8. Whether both CPython versions and the current Linux/ext4 profile remain
   A1c product targets.

Those unknowns are not blockers to the standards proposals. They are deliberate
admission questions that prevent standards from selecting an A1c mechanism
before consumer and risk facts exist.
