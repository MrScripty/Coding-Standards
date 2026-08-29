# A1 And A1b Architecture And Complexity Comparison

**Status:** Milestone 2 architecture comparison complete for AUD-A4

**Scope:** Accepted A1 v9, accepted A1 v10, the A1b planning and standards
base, and accepted A1b v11. This report compares guarantees before structure,
then evaluates Modules, Interfaces, Seams, Adapters, Depth, Leverage,
Locality, representations, identities, versions, operational obligations, and
representative change propagation.

## Method And Evidence Discipline

The comparison uses four immutable observations for different questions:

| Observation | Commit | What it decides |
| --- | --- | --- |
| Original accepted A1 | `2359a98740b6035a0414bfaf5427ceaa1301a1c8` | The runtime, contract, and evidence the original A1 acceptance actually reviewed at public v9. |
| Accepted A1 amendment | `7bc8bd070f882eb9779dc678139777d05a6ce7c7` | The accepted v10 policy-impact correction made after A1 acceptance and before A1b. |
| A1b planning/standards base | `36dd75790b2f08a6e66624ccae4f8530bc111a92` | The admitted C7 plan and standards posture immediately before A1b runtime implementation. |
| Accepted A1b | `84412f22fa9fe082f089eaa347c30c23f185ffee` | The implementation tree later accepted as A1b at public v11. |

The v10 production packages are unchanged between `7bc8bd07` and
`36dd7579`; only two Engine test files differ in the audited package set.
Consequently, `7bc8bd07` is the accepted runtime amendment and `36dd7579` is
the fair immediate implementation base. (`git diff --name-status
7bc8bd07..36dd7579 -- tools/graph_engine tools/standards_*`;
`c6fc663b` commit object)

The reproducible inventory is documented in
[inventories/README.md](inventories/README.md) and implemented by
[`architecture_metrics.py`](inventories/architecture_metrics.py). It counts
physical Python files/lines, AST definitions, package-root `__all__` exports,
selected-package production imports, schema definitions, registered suites,
and retained Bash checkers. Its limitations are binding here:

- a line or export count is diagnostic, not a quality verdict;
- an import edge records direction, not cognitive cost;
- AST test functions omit dynamically generated cases and do not replace
  accepted executed-run totals;
- generated code is included in totals but reported separately; and
- the four observations do not promise identical behavior.

Historical statements use `COMMIT:path` citations. **Fact** means a repository
artifact establishes the claim. **Recorded rationale** means the repository
records that reason at the time. **Inference** is this audit's architectural
interpretation. **Unresolved** means the evidence does not decide the issue.

## Executive Conclusion

**Fact:** A1 and A1b expose the same four primary operations: `query`,
`prepare`, `resolve`, and `inspect`. Both expose a large generated request,
result, submission, handle, and inspection algebra through the Engine root.
A1 v9 exported 139 generated names plus six handwritten facade/storage
capabilities; A1b exports 142 generated names plus four handwritten
facade/composition capabilities. The earlier informal characterization of A1
as having only a tiny Engine root API was wrong. (`2359a987:tools/standards_engine/standards_engine/__init__.py`;
`2359a987:tools/standards_engine/standards_engine/model.py`;
`84412f22:tools/standards_engine/standards_engine/__init__.py`)

**Fact:** A1b corrects real A1 failures. It delegates Draft 2020-12 semantics
to the selected `jsonschema` implementation, removes A1's custom schema
validator and generic NFC identity serializer, removes all five semantic
`x-standards-engine-*` schema-extension families, makes owner semantics and
identity relations explicit, and proves cold persisted reconstruction without
legacy readers. (`84412f22:docs/plans/standards-engine-a1b/reports/schema-and-domain-contract-audit.md`;
`84412f22:docs/plans/standards-engine-a1b/reports/a1b-cutover-evidence.md`)

**Inference:** A1b improves semantic ownership while making the composed
system materially more elaborate. Relative to the A1b plan base, the selected
production ecosystem grows from 96 to 125 Python files and from 29,733 to
38,410 lines; internal package dependency directions grow from 22 to 36. Most
growth is not the generated public algebra: generated contract code shrinks
from 4,175 to 3,377 lines, while non-generated production grows from 25,558 to
35,033 lines. New Identity, Contracts, and Authority foundations plus Verifier
growth account for 7,487 of the 8,677 added production lines. These numbers do
not prove excess by themselves; they locate the new reasoning burden.

**Inference:** The central design trade is not “small A1 Interface versus huge
A1b Interface.” It is:

- A1: one externally deep facade over broad, sometimes conflated schema and
  authority semantics, with weak cross-representation Locality; versus
- A1b: better-separated semantic owners and several genuinely deep foundation
  Modules, composed through a 14-kind directly stored object graph, owner
  codecs, exact closure/trust records, SQLite operations, a broad version
  matrix, and stronger repository-governance machinery.

A1b acceptance establishes internal coherence against the selected guarantees.
It does not establish that every selected guarantee or every structural proof
mechanism is necessary for a future A1c. Conversely, the existence of more
machinery does not erase the demonstrated value of external Draft semantics,
correct identity separation, neutral graph ownership, explicit uncertainty,
or non-ambient replay.

## Normalize Guarantees Before Comparing Structure

Direct size comparison would be misleading because A1b accepts stronger
guarantees. The following matrix separates common product behavior from new or
strengthened obligations.

| Guarantee family | Accepted A1 v9/v10 | Accepted A1b v11 | Comparison disposition |
| --- | --- | --- | --- |
| Product lifecycle | Four read-only operations over immutable snapshot/analysis handles; no authoring, application, or semantic approval. | Same four read-only operations and exclusions. | Common core; valid architectural comparison. |
| Canonical discovery/navigation | Neutral metadata, graph, applicability, policy-impact, and analysis owners; no caller paths after bootstrap. | Preserved and adapted to authority objects/views. | Common behavior with changed internal representation. |
| Unknown and rejection behavior | Three-valued applicability, typed rejected outcomes, exact completion. | Preserved with a closed generated result/rejection algebra. | Common behavior; A1b strengthens closure. |
| Public contract | One schema generated/checked Python and agent-tool shapes, but a custom validator and generated decoder implemented semantics locally. | One operation-reachable schema/interface pair; maintained Draft validator is semantic authority; generated models call the same compiled validator. | Demonstrated correction, not optional cosmetic growth. |
| Immutable replay | Issued handles were snapshot-bound; accepted v9 stored immutable `AnalysisState` and captured content sufficiently for its accepted cold tests. | Every advertised handle directly resolves a persisted immutable owner object with exact dependency closure and no fresh trust. | A1b deliberately strengthens a bounded behavior into a structural universal. |
| Identity/equality | Domain-separated hashes over a generic canonical serializer; schema equality, deduplication, and identity were insufficiently separated. | Codepoint-preserving identity v2; schema, applicability, domain equality, ordering, deduplication, and identity have separate owners. | Demonstrated defect justifies separation; exact number of records/scopes remains design choice. |
| Persistence | Memory and directory AnalysisState stores; file publication uses write, file `fsync`, and hard-link insertion. | Memory and SQLite object stores, schema/profile checks, transactional publication, backup, offline non-overwriting restore, cold reopen, and real interruption evidence. | Stronger operational guarantee; not a like-for-like implementation cost. |
| Public inspection | Snapshots, navigation, policy/relationship, coverage, fact, and analysis artifacts reconstruct through state-bound engine logic. | Fourteen public handle families directly name stored objects under a universal handle/envelope rule. | Same broad inspection aim, substantially stronger uniform representation. |
| Compatibility | Incompatible cutovers reject earlier states; no retained external state required migration. | Atomic v11 replacement; all v10 handles/state unsupported; no readers, converters, aliases, or fallback decoders. | Common simplifying policy. |
| Package/governance enforcement | Repairs caught one private package import; normal tests and repository verification checked packages. | Manifest roots, entrypoints, static exports, governed-source AST analysis, sanitized Git access, migration graph, and execution matrices. | New assurance obligation, adjacent to rather than intrinsic to four-operation semantics. |
| Platform/dependency support | Python `>=3.11`; audited package declarations had no external dependencies; custom schema tooling was standard-library-only. | CPython 3.11/3.12, Linux x86-64, glibc/wheel and ext4 profile, six locked dependency packages, licensing/security provenance. | New explicit operational and supply-chain surface caused partly by the correct dependency choice. |

Sources: `2359a987:docs/decisions/standards-engine-navigation-analysis.md`;
`2359a987:tools/standards_engine/standards_engine/engine.py`;
`84412f22:docs/decisions/standards-engine-a1b.md`;
`84412f22:docs/plans/standards-engine-a1b/plan.md`;
`84412f22:docs/plans/standards-engine-a1b/reports/identity-version-object-matrix.md`.

The later interpretations in this report apply only after this normalization.
For example, SQLite cost cannot be blamed on the four-operation Interface
without first asking whether durable direct-child replay is retained as an
A1c requirement.

## Reproducible Structural Inventory

### Whole selected ecosystem

| Observation | Production files | Production lines | Non-generated production lines | Test files | AST test functions | Test lines | Internal package edges | Suites | Bash checkers |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A1 v9 accepted | 96 | 29,445 | 25,199 | 42 | 581 | 16,465 | 22 | 218 | 53 |
| A1 v10 accepted | 96 | 29,733 | 25,558 | 42 | 585 | 16,790 | 22 | 224 | 53 |
| A1b plan base | 96 | 29,733 | 25,558 | 42 | 585 | 16,818 | 22 | 225 | 53 |
| A1b accepted | 125 | 38,410 | 35,033 | 60 | 677 | 19,019 | 36 | 226 | 53 |

The v10-to-plan-base difference is verification posture, not runtime growth.
From the immediate base to accepted A1b, production lines rise 29.2%,
production files 30.2%, AST test functions 15.7%, and test lines 13.1%.
Generated contract lines fall 19.1%. The non-generated increase is 37.1%.

**Inference:** A1b is not larger primarily because a generator emitted more
boilerplate. The main new burden is handwritten authority, contract,
composition, and verification machinery. This supports a design review of
those mechanisms but does not decide which are unnecessary.

### Principal package movement

| Package | A1b base production lines / tests | A1b accepted production lines / tests | Architectural observation |
| --- | ---: | ---: | --- |
| `standards_identity` | absent | 238 / 8 | Small bottom-level Module hiding byte framing and hashing. |
| `standards_contracts` | absent | 1,208 / 18 | Replaces two local Draft interpreters with one maintained implementation Adapter and build projection. |
| `standards_authority` | absent | 2,403 / 39 | Adds capture, envelope, repository, closure, SQLite, backup/restore, and recovery. |
| `standards_analysis` | 7,189 / 82 | 7,280 / 66 | Similar total size but materially replaced internals and gained Authority/Identity dependencies. |
| `standards_engine` | 7,454 / 46 | 7,176 / 36 | Package total shrinks 278 lines, while `engine.py` grows from 1,600 to 2,539 lines because generated code shrinks and composition concentrates. |
| `standards_verifier` | 10,273 / 380 | 13,911 / 433 | Adds 3,638 production lines and 53 AST tests, including the governed-source/package/Git enforcement family. |

**Inference:** The Engine package's total size slightly falls, which is
counterevidence to a claim that A1b merely bloated the public product Module.
The stronger concern is composition concentration (`engine.py` grows 58.7%)
and ecosystem growth around Authority and Verifier. A1c should measure the
reasoning required to change the system, not just the size of one directory.

## Interface Comparison

### The root Interface correction

| Observation | Schema definitions | Generated exports | Engine-root exports | Handwritten root additions | `engine.py` lines |
| --- | ---: | ---: | ---: | ---: | ---: |
| A1 v9 accepted | 143 | 139 | 145 | 6 | 1,586 |
| A1 v10 accepted / A1b base | 141 | 138 | 144 | 6 | 1,600 |
| A1b accepted | 140 | 142 | 146 | 4 | 2,539 |

A1 v9's handwritten additions are `AgentToolFacade`, the state-store Protocol,
memory and directory state-store Adapters, `StandardsEngine`, and
`render_text`. Its root also installs all generated exports through `model`.
A1b's additions are `AgentToolFacade`, `ENGINE_CODECS`, `StandardsEngine`, and
`render_text`; it directly re-exports all generated names. A1b generated output
contains 140 definition types plus `DEFINITION_METADATA` and
`decode_contract`. (`2359a987:tools/standards_engine/standards_engine/__init__.py`;
`2359a987:tools/standards_engine/standards_engine/model.py`;
`84412f22:tools/standards_engine/standards_engine/_generated_contract.py`)

**Inference:** Both root Interfaces are broad in names and narrow in primary
verbs. The four operations provide high Leverage, but a caller that directly
constructs typed values, opens repositories, interprets handles, or handles
failures must learn much more than four method names. A1b also adds
`open_persisted` beside `open_repository` and `open_analysis`, making durable
construction an explicit part of the class Interface.
(`2359a987:tools/standards_engine/standards_engine/engine.py`;
`84412f22:tools/standards_engine/standards_engine/engine.py`)

### Lower Interfaces

At accepted A1, `standards_analysis` exports 118 names. At accepted A1b it
exports 137. A1b Authority exports 48, Contracts 17, and Identity 7. These are
not automatically supported end-user APIs; the A1b package policy nevertheless
requires production imports through declared public roots, making those roots
real repository-wide Interfaces. (`84412f22:tools/standards_verifier/standards_verifier/python_packages.py`;
the package `__init__.py` files at the selected commits)

**Inference:** Internal maintainers receive less Depth than external facade
callers. Owner Modules expose models, codecs, dependency extraction, identity
records, failures, and construction helpers so Engine and Verifier can compose
them. Static public-root governance turns “internal in principle” into
“explicitly exported in practice.” A1c should decide which lower Interfaces
are supported seams and make the rest private rather than using public export
breadth as an enforcement convenience.

### The schema boundary

A1's schema was named the sole machine authority for Python types, JSON
validation, agent tools, examples, identity-bearing serialization, result
variants, next operations, and rendering. Its five extension families also
described contract/state-machine, identity, invariants, projection, and
authority concerns. Several local executables still supplied the actual
semantics. (`2359a987:tools/standards_engine/contracts/a1-contract.schema.json`;
`2359a987:tools/standards_engine/contracts/README.md`)

A1b's v11 schema is larger—3,890 lines versus 2,257 at the v10/base
observation—but removes every extension family. JSON Schema owns wire shapes;
`a1-interface.toml` owns operation roots and wire versions; Contracts owns
Draft validation/projection; domain Modules own invariants and identities;
Analysis owns transitions; Engine owns composition/authorization adaptation.
(`84412f22:docs/plans/standards-engine-a1b/reports/schema-and-domain-contract-audit.md`)

**Inference:** A schema crossing package boundaries is not by itself a design
flaw when it is the public transport Adapter for values supplied by those
packages. The A1 flaw was that the declaration claimed semantic ownership
across boundaries it could not execute consistently. A1b corrects that error.
The remaining A1b concern is upstream: placing many independently inspectable
domain objects in the public Interface obliges the wire schema to project all
of them. A deeper aggregate Interface would shrink schema coordination by
removing public concepts, not by hiding their schema definitions elsewhere.

## Module And Dependency Direction

The inventory uses consumer-to-supplier arrows. No selected-package import
cycle appears in either observation.

### Accepted A1

```text
standards_engine
  -> graph_engine, standards_analysis, standards_applicability,
     standards_graph, standards_metadata, standards_policy_impact

standards_analysis
  -> graph_engine, standards_applicability, standards_metadata,
     standards_policy_impact

standards_graph
  -> graph_engine, standards_metadata, standards_policy_impact

standards_policy_impact
  -> graph_engine, standards_applicability, standards_metadata

standards_verifier
  -> all six neutral/domain suppliers above
```

This gives the neutral graph, applicability, metadata, policy-impact, and
analysis concerns real Leverage across Engine and Verifier. Deleting those
owners would put loaders, traversal, or policy meaning back into several
callers. (`2359a987:docs/decisions/standards-engine-navigation-analysis.md`)

### Accepted A1b

```text
standards_identity                         # bottom-level
standards_authority -> standards_identity
standards_contracts                       # external Draft Adapter; no selected internal supplier

standards_metadata -> standards_authority, standards_identity
standards_graph -> graph_engine, standards_authority,
                   standards_identity, standards_metadata
standards_policy_impact -> graph_engine, standards_applicability,
                           standards_authority, standards_identity,
                           standards_metadata
standards_analysis -> graph_engine, standards_applicability,
                      standards_authority, standards_identity,
                      standards_metadata, standards_policy_impact

standards_engine -> foundations plus all domain suppliers
standards_verifier -> Contracts, Authority, and domain suppliers
```

A1b deliberately prevents Authority from importing Contracts or domain
semantics. Authority treats semantic IDs and payload contracts as opaque;
owner codecs validate domain values. This is a strong dependency-direction
merit. (`84412f22:docs/plans/standards-engine-a1b/reports/identity-version-object-matrix.md`;
`84412f22:tools/standards_authority/standards_authority/repository.py`)

**Inference:** The new foundation direction is coherent, but Authority and
Identity become crosscutting suppliers for most semantic owners. A change that
remains inside one domain can have good Locality; a change that makes a value
persisted or publicly inspectable crosses owner, codec, envelope/reference,
Engine composition, public schema, migration, and verification seams. The
architecture eliminates semantic dependency cycles while retaining substantial
coordination coupling.

## Representations, Identities, And Compatibility Scopes

### A1 representation cluster

Accepted A1 coordinated at least:

1. repository Markdown/TOML/TSV authority;
2. the public Draft schema plus five custom annotation families;
3. a custom schema validator;
4. a custom generator and generated Python/agent tools;
5. handwritten domain models and transitions;
6. facade Adapters from domain values to generated values;
7. a generic canonical identity serializer and domain hashes;
8. memory/directory persisted AnalysisState; and
9. examples, identity fixtures, renderer, and inspection projections.

This cluster had one named declaration owner but several executable semantic
owners. Repair history shows equality, regex, reachability, conversion,
inspection, and identity changes crossing the cluster. (`2359a987:tools/standards_engine/contracts/README.md`;
`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-boundary-repair-vi-candidate.md`)

### A1b representation cluster

A1b removes the local Draft interpreter and generic semantic serializer, but
adds or formalizes:

- separate public schema and operation-interface declarations;
- a Contracts compiler/Adapter and generated public artifacts;
- owner-local semantic models, typed identity records, codecs, dependency
  extraction, equality, ordering, and deduplication keys;
- one identity-v2 byte encoding and domain-separated hash frame;
- a seven-field immutable authority envelope;
- memory and SQLite envelope stores;
- standards views and roots-only execution closures;
- direct provider and authorization records; and
- fourteen directly stored public object kinds.

The 14-kind public object matrix covers content snapshot, standards view,
execution closure, navigation, analysis root, policy, relationship,
certificate, coverage view/requirement/attestation, analysis context, fact
requirement, and fact observation. Each has a payload contract, semantic ID,
codec, dependencies, handle projection, and inspection path.
(`84412f22:docs/plans/standards-engine-a1b/reports/identity-version-object-matrix.md`)

**Inference:** A1b trades conflation for explicit composition. That is a
semantic improvement, but explicitness is not free: the number of independently
represented public concepts sets a lower bound on codecs, registrations,
versions, migration dispositions, and evidence. The architectural question for
A1c is not whether each object is internally coherent. It is whether callers
need each object as an independent Interface concept.

### Identity and version scope

A1 v9 used separately named snapshot, navigation, obligation, analysis,
analysis-context, fact, coverage, and certificate domains, but one generic
canonical serializer also influenced schema equality and deduplication. V10
advanced several umbrella contract/handle/analysis/coverage families together.
(`2359a987:docs/decisions/standards-engine-navigation-analysis.md`;
`7bc8bd07:docs/decisions/standards-engine-policy-impact-authority-v2.md`)

A1b correctly separates wire, semantic, operation, storage, and identity
promises:

- interface/schema 11;
- request contract 3;
- result projection 3;
- public handle schema 4;
- identity encoding 2;
- authority envelope 1;
- SQLite schema 1;
- owner payload/semantic identity versions; and
- operation compatibility keys `(route, 2)`, `(read, 2)`, `(related, 2)`, and
  `(analysis, 2)`.

The former analysis contract/schema umbrella `6/3` has no A1b successor.
Analysis payload, semantic identity, handle representation, result
representation, and operation compatibility now have independent owners.
(`84412f22:docs/plans/standards-engine-a1b/reports/identity-version-object-matrix.md`)

**Inference:** This fixes real over-invalidation, yet the cumulative
compatibility Interface is larger. The repository has evidence that the
promises *can* change for different reasons; it does not establish that each
has an independently evolving consumer. A1c should retain scope correctness
and add a cumulative test: does independent versioning reduce real migration
cost, or only encode theoretical change reasons inside an atomic product?

## Why `interface_schema_version` Is 11

The field is `interface_schema_version` (not “infrance”). Its value is an
allocation counter for incompatible public schema shapes, not evidence of
eleven accepted product releases.

| Version | First material repository boundary | What changed | Implementation/acceptance status |
| ---: | --- | --- | --- |
| 1 | `c7d23dfa` admission; `bbbab878` typed facade | Initial navigation, requests/results, snapshots, inspection, and pre-runtime schema corrections. | Committed and used by early A1 milestones; not a final A1 release. |
| 2 | `f9496cb3` | Compiled policy-impact declarations and fact-free applicability. | Committed milestone cutover. |
| 3 | `ee940a91` | Reusable consumer-coverage view/requirement/attestation/certificate model. | Committed milestone cutover. |
| 4 | `50043a5b` | Recovered missing consumer obligations and plural provenance. | Committed corrective milestone. |
| 5 | `4baa6311` | Plural reading plans and related coordinated identities. | Committed milestone recovery. |
| 6 | No canonical schema commit | An intermediate number was consumed or bypassed during fact/immutable-state replanning. The surviving report explicitly advances public Interface 5 to 7 but does not preserve a standalone v6 schema or assign v6 a complete final meaning. | Planning allocation only; exact standalone shape unresolved. |
| 7 | `94b295b4:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-fact-authority-replan.md` | Planned fact contracts, topology-independent context, requirements/observations, and immutable analysis state. | Explicit planned target; never committed as the canonical schema. |
| 8 | `94b295b4` | Superseding single `AnalysisState`/`AnalysisHandle`; removed packet/report/hidden-session/global-supersession model. | Committed and provisionally accepted by `e61e9567`; that acceptance was later withdrawn. |
| 9 | `51dcd258`; final `2359a987` | Boundary-integrity repair: immutable selected content, generated closure, continuation binding, inspection/public model correction. | Several v9 repair candidates; final A1 v9 accepted at `2359a987` by `933c9ab9`. |
| 10 | `9bbc1e05`; corrected `7bc8bd07` | Policy-impact authority v2, operation-shaped relationship inspection, coordinated handle/result/analysis changes. | Implemented, corrected, and independently accepted at `7bc8bd07` by `bf9f3d86`. |
| 11 | Planned by admitted C7 `36dd7579`; first cutover `d6117216`; final `84412f22` | A1b external-validator contract, authority-object replacement, handle v4, request/result v3, and removal of old schema semantic extensions. | Planned before runtime, then implemented through several rejected v11 candidates; accepted at `84412f22` by `580d9c95`. |

The canonical schema's Git history jumps from v5 at `4baa6311` to v8 at
`94b295b4`; there is no committed canonical v6 or v7 schema. The fact-authority
report's explicit “public interface 5 to 7” proves v7 was allocated before the
single-state supersession; it proves an intervening allocation existed or was
bypassed, but it does not justify inventing a standalone v6 contract after the
fact. (`94b295b4:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-fact-authority-replan.md`;
`94b295b4:docs/plans/standards-engine-navigation-analysis/reports/milestone-4-packet-supersession-replan.md`)

**Conclusion:** “11” means eleven monotonic incompatibility allocations during
rapid design and repair, including planning-only, withdrawn, and superseded
states. The stable independently accepted product boundaries relevant to this
audit are v9, v10, and v11. The number is evidence of pre-acceptance design
churn and coupled cutovers; it is not evidence of eleven supported formats,
eleven migrations, or eleven externally deployed generations. Both A1 and A1b
explicitly reject old versions and retained no compatibility readers.

## Operational Obligations

| Obligation | A1 v9/v10 | A1b v11 | Design consequence |
| --- | --- | --- | --- |
| Runtime dependencies | Audited packages declare Python `>=3.11` and no dependencies; custom Draft tooling is local. | Exact CPython 3.11/3.12 and six-package lock; `jsonschema` and `referencing` are direct Contracts dependencies with transitive provenance. | Correct external semantics adds supply-chain, wheel, license, vulnerability, and platform proof. |
| Persistent unit | Complete `AnalysisState` JSON behind memory/directory state-store Seam. | Generic immutable envelope per directly inspectable semantic object behind memory/SQLite store Seam. | Smaller aggregate storage becomes a typed object repository. |
| Publication | Temporary file, file `fsync`, hard-link no-overwrite publication. | SQLite transaction/profile, capability checks, real `fsync`/`fdatasync` interruption, backup, integrity, offline non-overwriting restore. | Stronger durability and recovery obligations. |
| Capture | Git/dirty/non-Git snapshot construction inside the Engine/analysis cluster. | Git and native capture Adapters publish exact logical-path/raw-byte snapshots. | Two real Adapters justify the capture Seam, but widen platform/path contracts. |
| Supported environment | No narrow filesystem/architecture support contract was admitted beyond Python. | Linux x86-64, glibc threshold, case-sensitive non-casefold ext4, selected SQLite capability profile; many other systems explicitly unsupported. | More honest and testable, but operationally narrower. |
| Lifecycle operations | State put/get/values; no separately admitted backup/restore contract. | Put/get plus backup/restore and cold reopen; intentionally no enumeration, deletion, GC, migration, remote store, or semantic export/import. | Coherent bounded profile; retained-data cleanup and evolution remain unresolved. |

Sources: package `pyproject.toml` files at `2359a987` and `84412f22`;
`2359a987:tools/standards_engine/standards_engine/engine.py`;
`84412f22:docs/plans/standards-engine-a1b/reports/a1b-dependency-provenance.md`;
`84412f22:docs/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md`.

**Inference:** A1b's operational design is explicit rather than accidentally
portable. That is a merit. It is also a major expansion for a repository-local
read-only standards tool whose consumer inventory found no independent
deployment and no retained A1 state. A1c must decide its actual persistence
lifetime before selecting storage machinery; it should not inherit SQLite or
aggregate-only storage merely because either predecessor used it.

## Representative Change Propagation And Locality

Commit statistics are diagnostics. The stronger evidence is which independent
owners had to move for one semantic correction.

| Change | Commit observation | Propagation | Locality interpretation |
| --- | --- | --- | --- |
| Plural consumer obligations, v4 | `50043a5b`: 19 files, 1,343 additions, 124 deletions | Plan/reports, Analysis packets/obligations/tests, schema, examples, identities, validator. | One missing work concept crossed domain, wire, identity, evidence, and governance. |
| Reading plan, v5 | `4baa6311`: 27 files, 1,462 additions, 330 deletions | Analysis compiler/tests, schema/examples/fixtures, Router/catalog authority, coverage projection/attestations, verifier evidence. | Adding derived reading causes invalidated a global coverage horizon as well as product code. |
| Single-state lifecycle, v8 | `94b295b4`: 36 files, 7,758 additions, 1,317 deletions | ADR/plan, Analysis models/state/transitions, Applicability, Engine, schema/examples/validator, rendering/tools/tests. | A genuine simplification deleted packet machinery, but the replacement still required a broad atomic cutover. |
| Boundary integrity/generation, v9 | `51dcd258`: 34 files, 6,545 additions, 387 deletions | Analysis snapshots/results/coverage, new generator/generated artifacts, schema/examples/identity, Engine/model/renderer/tool Adapter, Metadata serializer, tests, plan checker. | Immutable-read and contract-closure repairs crossed nearly every representation; generated `agent-tools.json` accounts for much of the raw addition. |
| Policy-impact authority, v10 | `9bbc1e05`: 61 files, 1,745 additions, 1,304 deletions | Policy compiler/contract, schema/public projection, graph/catalog, coverage/attestations, verifier, plans/reports. | Consolidating one systemic invariant improved ownership but forced broad policy and evidence renewal. |
| Initial A1b v11 cutover | `d6117216`: 140 files, 20,845 additions, 17,784 deletions | Foundations, all domain owners, Engine/schema/generated output, package manifests/import verifier, policy graph/migration, coverage, suites, tests, docs. | Atomic replacement avoided permanent dual paths but created very low incremental Locality. |
| Final governed-source correction | `84412f22`: 8 files, 245 additions, 50 deletions | Primarily Verifier AST state, package fixtures, generated suite-input identity, and acceptance records. | A bounded repository-governance defect—not core Engine semantics—still blocked product acceptance. |

Sources are the named Git commit objects and their diffs. The candidate reports
at `933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/` and the
A1b ledger at `580d9c95:docs/plans/standards-engine-a1b/execution-ledger.md`
record the corresponding review findings.

### Representative semantic-kind change in A1b

The accepted C7 matrix makes propagation structural. Adding one new public
inspectable kind normally requires:

1. an owner model and payload contract;
2. a typed identity record and domain;
3. owner codec and dependency extraction;
4. envelope/repository kind admission;
5. handle and inspection schema definitions;
6. Engine codec composition, projection, and operation-role admission;
7. migration and policy-relationship dispositions;
8. coverage identity/attestation renewal where the governed inputs change;
9. focused, integration, generated-freshness, import, and migration evidence.

The A1b history report identifies the same closed path in the C7 design.
(`84412f22:docs/plans/standards-engine-a1b/reports/c7-design-proposal.md`;
`84412f22:tools/standards_engine/standards_engine/authority.py`)

**Inference:** Owner-local codecs make semantic changes *within* an existing
kind more local than A1's schema-as-semantic-owner approach. Making a concept
newly persistent or public remains costly because public inspection is the
Interface and persistence is structural. This is the most important A1b
Locality distinction: local owner changes can be good, cross-Interface changes
are intentionally expensive.

## Depth, Leverage, And Design Merits

### Merits shared or preserved

1. **Four-operation product Depth.** The facade hides repository paths,
   graph traversal, policy compilation, analysis fixed points, and rendering
   behind a small verb set with high Leverage.

2. **Disciplined read-only scope.** Neither design absorbs authoring,
   application, semantic approval, rollback, external projects, or arbitrary
   prose interpretation.

3. **Neutral graph and metadata ownership.** These Modules have several real
   consumers. Their deletion would recreate verifier ownership or duplicate
   graph/loading mechanics.

4. **Explicit uncertainty.** Unknown applicability, unavailable authority,
   unsupported versions, and typed rejection are preserved rather than coerced
   into success.

5. **No compatibility layering without consumers.** Both designs replace
   incompatible pre-acceptance forms atomically and remove old readers.

### A1-specific merits

- One immutable `AnalysisState` deleted packet/report/session/supersession
  machinery instead of adding another mutable head.
- The directory and memory state-store Adapters supplied two real
  implementations behind a small Seam.
- The implementation remained standard-library-only and made fewer explicit
  operational promises.

### A1b-specific merits

- Contracts is a deep Module: 17 exports hide reference resolution,
  dialect/profile admission, compiled validation, closure, failures, and
  projection. Deleting it would scatter direct Draft calls and diagnostic
  policy.
- Identity is a deep Module: seven exports hide exact scalar framing,
  canonical encoding, and hashing without deciding domain equality.
- Authority preserves correct dependency direction: semantic owners issue and
  validate values; storage never becomes domain authority.
- Store and capture are justified Adapters: memory/SQLite and Git/native are
  two real implementations, not speculative abstractions.
- C7 removed C6's hard-link object protocol, persisted transitive lists,
  hypothetical future authority, aggregate trust views, and structural capture
  metadata.
- The v11 schema removes semantic extension families and the local Draft
  interpreter rather than layering another interpretation path.

Sources: accepted ADRs at `2359a987` and `84412f22`; C7 proposal and SQLite
audit at `36dd7579`; package roots at `84412f22`.

## Design Regressions And Excess-Risk Evidence

The following findings are not count-only verdicts. Each links observed
structure to caller knowledge, change propagation, or operational work.

1. **Composition-root concentration.** `engine.py` grows from 1,600 to 2,539
   lines while coordinating public adaptation, owner codecs, views, closures,
   providers, authorization, operation roots, persistence, projection, and
   inspection. The facade stays behaviorally deep for callers, but maintainers
   must reason across more owners at one composition point.

2. **Direct-object universality.** Fourteen public kinds receive independent
   identity, storage, codec, dependency, handle, and inspection treatment.
   The history proves coherence, not that callers need each child independently
   addressable.

3. **Internal Interface breadth.** Analysis exports 137 names and Authority
   48. Repository governance makes public roots mandatory, so internal
   composition concerns become broad formal Interfaces.

4. **Cumulative compatibility burden.** Individually scoped versions correct
   A1's umbrella invalidation, but there is no evidence that all scopes evolve
   independently in a product that still replaces its public surface
   atomically.

5. **Operational expansion.** A read-only repository tool now owns database
   capability probing, backup/restore, real syscall interruption evidence,
   platform/wheel support, and dependency security/licensing provenance.
   These are appropriate if durable cold replay is a real consumer promise;
   that consumer remains unidentified.

6. **Governance machinery competes with product delivery.** The final four
   rejected implementation boundaries were dominated by governed-source and
   Git-capability analysis. Correcting this tool delayed acceptance after the
   C7 runtime architecture was retained.

7. **Low cross-Interface Locality.** The atomic v11 cutover and later migration
   renewals show that schema, owner objects, Engine composition, package
   contracts, policy relationships, coverage, and evidence move together when
   a public concept changes.

8. **No admitted simplification test for the whole composition.** A1b
   repeatedly tested each authority and version for coherent ownership, but
   did not re-compare the accepted C7 composition with a bounded aggregate once
   direct-child storage became binding.

Sources: `580d9c95:docs/plans/standards-engine-a1b/execution-ledger.md`;
`84412f22:docs/plans/standards-engine-a1b/reports/identity-version-object-matrix.md`;
`84412f22:docs/plans/standards-engine-a1b/reports/c6-c7-design-history-research.md`.

## Standards, Requirements, And Implementation Choices

| Machinery | Best-supported origin | Architectural judgment |
| --- | --- | --- |
| External Draft validator | Demonstrated A1 Unicode/equality nonconformance plus Dependencies/Generated Contract recovery. | Preserve the semantic outcome and deep Contracts Adapter. |
| Four-operation facade, typed uncertainty, immutable issued results | Original A1 product requirements preserved by A1b. | Preserve unless A1c explicitly changes product scope. |
| Full transitive authority closure | A1/A1b replay promise plus Immutable Authority Closure standard; C6 report calls its broad form a defensive response to that rule. | Preserve no ambient substitution; make cold lifetime and transitive breadth conditional on a declared consumer. |
| Identity/domain-equality separation | Demonstrated defect plus recovered Contracts rules. | Preserve. Exact records/domains remain design choices. |
| Owner codecs and opaque storage | Authority/version-scope standards directly rejected C4 umbrella bags. | Coherent if an object repository remains; number of kinds is not standards-mandated. |
| SQLite/backup/restore/interruption | C7 implementation choice for the plan's durable publication guarantee. | Proportionate only if A1c retains that operational promise. |
| Many scoped versions | Directly influenced by `396144ad` authority/version-scope standards. | Scope rule is correct; cumulative matrix needs independent-consumer review. |
| Policy graph, migration, coverage renewal | Existing projection-completeness and A1 successful-empty-coverage guarantees. | Real governance value; high fanout and global invalidation need proportionality review. |
| Package/Git AST verifier | Triggered by a real A1 private-import defect; expanded through systemic-review findings. | Useful policy tooling, but its final breadth is an implementation choice separate from Engine semantics. |
| No compatibility runtime | Consumer/state inventory found no external deployment or retained state. | Strongly supported simplification. |

The standards recovery and A1b proposal share the A1 defect analysis as a
common cause. Early agreement between standards and design is therefore not
proof that the standards caused every mechanism. Later C4-C7 replans that
explicitly cite `396144ad` are stronger direct causal evidence.
(`396144ad:topics/architecture.md`; `396144ad:topics/contracts.md`;
`4f69f994:docs/plans/standards-engine-a1b/execution-ledger.md`)

## Deletion Test

The deletion test asks whether removing a Module or concept makes complexity
disappear or merely pushes essential reasoning into callers.

| Candidate deletion or merge | Where complexity would go | Assessment |
| --- | --- | --- |
| Delete `standards_identity` while retaining content-addressed domain identities | Exact encoding/framing/hashing would be reimplemented in every owner. | Fails deletion test; retain a small deep Module. |
| Delete `standards_contracts` while retaining the public Draft contract | Draft selection, reference/profile rules, diagnostics, closure, and projection would scatter through generator and runtime callers. | Fails deletion test; retain the deep Adapter. |
| Delete neutral metadata/graph/applicability Modules | Engine, Analysis, Policy Impact, and Verifier would duplicate loading, traversal, or truth semantics. | Fails deletion test on current consumers. |
| Delete generic Authority while retaining 14-kind durable direct replay | Persistence, envelope verification, cycle/dependency checks, and lookup would move into every owner or Engine. | Fails deletion test under the A1b guarantee. |
| Delete durable direct replay as a product guarantee | Authority, SQLite, backup/restore, envelope, many codecs/records, and required-real evidence could disappear rather than move. | Promising only if consumer/lifetime audit shows process-local or aggregate replay is sufficient. |
| Merge several child authority objects into one persisted analysis/navigation aggregate | Some independent child identity/inspection disappears; aggregate codec and projection remain. | Strong A1c experiment. The repository has not shown that all 14 child handles require independent cold lookup. |
| Remove public lower-level exports but keep internal modules | Calls move to private imports unless composition is narrowed. | Beneficial only with a smaller explicit owner Interface, not a naming-only change. |
| Delete owner codecs while retaining generic storage | Domain validation/identity would move into Authority and recreate semantic conflation. | Fails deletion test; reduce kinds before reducing codecs. |
| Delete the full governed-source abstract interpreter | Public-import policy would rely on simpler static import checks, runtime packaging, or review; some dynamic bypass protection disappears. | Candidate simplification, but AUD-A5 must identify which accepted failures remain reachable and material. |
| Delete SQLite backup/restore/interruption claims while retaining ephemeral or reconstructible state | Machinery disappears; recovery falls back to rebuilding from canonical repository inputs. | Candidate if state is truly cache-like and no retained consumer requires recovery. |
| Delete old-version readers | Complexity disappears because no retained consumer/state exists. | Already done correctly in both A1 and A1b. |

**Inference:** Identity, Contracts, and neutral domain owners have strong
deletion-test cases. The highest-value A1c deletion opportunities are above
those owners: reduce promised durable replay, reduce independently public
object kinds, aggregate authority at the product Interface, and separate
repository-governance tooling from product completion. Deleting low-level
Modules while retaining all A1b promises would only relocate machinery.

## Evidence-Constrained A1c Design Directions

These are experiments and admission constraints, not a binding A1c design.

1. Preserve the four-operation behavior and corrected external schema
   semantics, but derive a minimal public algebra from real caller workflows.

2. Choose handle lifetime first: in-process, process-restart, repository-state,
   or durable archival. Select aggregate or object-graph persistence only after
   that promise is explicit.

3. Prototype one persisted aggregate for analysis and one for navigation.
   Test whether all real `inspect` workflows work without independent storage
   for coverage, fact, context, and closure children.

4. Keep schema authority at the wire Interface only. Domain owners should
   construct valid internal values; schema validation belongs at public,
   persistence, process, plugin, or otherwise independently mutable seams.

5. Retain Identity and Contracts as small deep Modules. Retain Authority only
   to the depth required by the selected persistence promise.

6. Make the product Interface the primary test surface. Admit internal tests
   only for distinct risky invariants or failure modes that the deeper
   Interface cannot observe adequately.

7. Run representative Locality probes before design acceptance: add one public
   field, one internal field, one inspectable kind, one identity rule, and one
   operation compatibility change. Count affected owners only after explaining
   why each must change.

8. Require every new version to name an actual compatibility consumer. Allow
   separate scopes, but review their cumulative migration and coordination
   burden.

9. Keep store and capture Adapters only when there are at least two real
   implementations or one real implementation plus a credible near-term
   alternative. A1b meets this for memory/SQLite and Git/native.

10. Treat package/coverage governance as repository infrastructure with its
    own risk and acceptance model. Its failure should block Engine acceptance
    only when it can invalidate an Engine or standards-governance claim.

## Counterevidence And Limits

- Root export counts do not show an A1-to-A1b explosion; they are nearly equal.
- A1b's Engine package is smaller in total than the base, and generated code is
  shorter. Complexity growth is concentrated elsewhere.
- Repeated independent review found real A1 and A1b defects. The process cost
  cannot be dismissed as ceremony merely because it was high.
- The external Draft dependency, Identity separation, public result closure,
  and cold non-ambient reconstruction each answer demonstrated or explicit
  failures.
- C7 is substantially simpler than C6 for the same admitted durability and
  replay guarantees.
- A1's smaller operational surface also hid incorrect Draft semantics and
  weaker assurance. “Return to A1” is not a sufficient A1c design.
- Static inventories cannot measure how often callers use an export, how hard
  code is to understand, or which tests have unique marginal value.
- No report proves a particular remaining test, hash, validator, or codec
  redundant. That decision belongs to the claim-level verification audit.

## Unresolved Questions

1. Which of the 140 public definitions are used by a caller independent of the
   implementation and its tests?
2. Which child handles must survive a process restart independently, rather
   than being inspected through one aggregate analysis/navigation handle?
3. Is SQLite state retained in actual use? If so, who owns deletion, growth,
   migration, backup, and restore despite A1b intentionally omitting
   enumeration, GC, and migrations?
4. Are lower package roots supported external Interfaces or merely an internal
   import-governance mechanism?
5. Which version scopes have independently evolving consumers rather than only
   independently imaginable change reasons?
6. Can repository canonical inputs reconstruct all needed state cheaply enough
   to treat persistence as a cache rather than durable authority?
7. Which governed-source failures can produce a hidden dependency that normal
   packaging, static import checks, runtime failure, or review would not expose?
8. Does successful empty-impact certification belong inside the product
   lifecycle or in separate standards-governance tooling?
9. What is the smallest aggregate that preserves real cold-inspection and
   replay workflows without reintroducing ambient state?
10. Which validation and evidence layers remain necessary after the Interface
    becomes the primary test surface? AUD-A5 must answer claim by claim.

## Final Architectural Finding

A1 and A1b each contain design worth preserving. A1 provides the clearer proof
that a read-only four-operation Module can have substantial external Depth.
A1b provides the clearer proof that declaration ownership, semantic ownership,
identity, persistence, and external standardized behavior must not be
conflated.

A1's principal architecture defect was broad semantic ownership behind one
schema declaration and the resulting poor change Locality. A1b's principal
architecture risk is the opposite failure at composition scale: many locally
coherent owners, objects, versions, proofs, and governance relationships form
a system whose cumulative Interface and change cost were never subjected to an
equally strong whole-design simplification gate.

That makes the concern about “too much machinery” well supported, but more
specific than a line-count complaint. The evidence supports preserving corrected
semantics and deep foundation Modules while challenging the durability promise,
the number of public inspectable objects, the cumulative version matrix, the
composition-root burden, and the scope of governance verification. Those are
the most promising A1c design variables and the strongest general standards
evidence produced by the architecture comparison.
