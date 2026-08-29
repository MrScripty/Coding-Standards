# Standards Evolution And Causal Relationship To A1 And A1b

**Status:** Historical research evidence; not a normative standards change or
A1c design decision

**Audit objective:** `AUD-A3`

**Accepted A1 implementation:** commit
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`

**A1 acceptance record:** commit
`933c9ab93d18ede987d449a6fe7b9ebd313922fc`

**Accepted A1b implementation:** commit
`84412f22fa9fe082f089eaa347c30c23f185ffee`, tree
`8e0f96a61fcea2398418b17d16a061c20f7463f5`

**A1b acceptance record:** commit
`580d9c959b22f3fdeb0898e7fd4aafd168893580`

## Executive Finding

The history supports four conclusions.

1. A1 was not built in the absence of simplicity, ownership, contract-artifact,
   proof-lifetime, test-selection, Security-applicability, Resilience, or
   diagnostic-selection guidance. Much of that guidance was already strong at
   A1's implementation base. A1 nevertheless admitted an umbrella schema,
   incomplete semantic projection, ambient reconstruction authority, routing
   omissions, and evidence that proved local agreement rather than the declared
   external contract. The strongest classification is therefore **standard
   present but unrouted, unenforced, ambiguously applied, or misapplied**, with
   narrower missing rules around generated-contract semantics, independent
   evidence oracles, and transitive replay closure.

2. The standards recovery did not arise independently of A1b. The A1b redesign
   brief first described the A1 defects and proposed generated-contract,
   evidence-oracle, immutable-authority, dependency-selection, and systemic-
   replanning rules. Commit `7a571ed2` then made almost those same proposals
   normative, and A1b planning began only after their graph, fixtures, suites,
   prompts, and coverage were accepted. Compliance between A1b and those rules
   is therefore partly **common-cause evidence**, not proof that the standards
   independently caused the design.

3. There is nonetheless direct evidence that standards changed A1b's design.
   The C6 history calls its transition-complete closure a “defensive response”
   to Immutable Authority Closure. The A1b ledger says the authority- and
   version-scope standards at `396144ad` caused C4's copied version records and
   umbrella authority to be rejected as a systemic defect. The policy-impact
   graph grew from 7 direct consumers of Immutable Authority Closure at the
   standards-recovery boundary to 27 at accepted A1b, including 22
   implementation projections. These facts support **standard plausibly
   induced machinery**, especially for exact authority closure, independently
   scoped identities and versions, codec ownership, and evidence closure. They
   do not establish that every resulting class, codec, test, or store mechanism
   was required by the rule.

4. Neither the A1-era standards nor the recovery rules contain an effective
   whole-design proportionality gate. They ask what a Module, contract,
   invariant, version, test, or graph relationship owns and proves, but they do
   not require its *marginal* value, proof substitution, composition cost,
   Interface Depth, representative change Locality, or later removal condition.
   The executable simplicity fixture favors separation from declared concern
   facts but never measures what callers must coordinate after separation. The
   verification workflow asks for the “smallest complete claim set” and rejects
   assertions at every internal hop, yet it has no admission test for a check
   whose failure is unreachable, statically impossible, already subsumed, or
   adequately diagnosed by fail-fast behavior. This is the best-supported
   project-agnostic shortcoming exposed by both A1 and A1b.

These findings do not rescind either acceptance. A1 and A1b were accepted
against their recorded objectives and standards snapshots. This report asks
what those snapshots made likely, permitted, detected, or failed to detect.

## Method And Causal Discipline

The sources are repository-owned Git objects, standards, plans, ADRs, reports,
fixtures, suites, source manifests, and policy-impact declarations. No
chronological coincidence is treated as causation by itself.

Each outcome is classified using one or more of these labels:

- **standard absent** — no applicable rule or routed projection addressed the
  decision at the time;
- **standard present but unrouted/unenforced/misapplied** — applicable guidance
  existed but routing, planning, review, implementation, fixtures, or acceptance
  did not make it effective;
- **conflicting or ambiguous guidance** — applicable rules supported materially
  different interpretations;
- **standard plausibly induced machinery** — a contemporaneous source explicitly
  cites the standard as a reason, the standard mechanically required the work,
  or the standard constrained the chosen solution strongly enough to support a
  causal inference;
- **product requirement** — the accepted plan or Interface promised the
  behavior independently of the standards;
- **implementation choice** — the requirement did not uniquely imply the
  selected mechanism;
- **unresolved** — the record cannot distinguish the causes or necessity.

Confidence means confidence in the classification, not a design-quality score.
Counts are diagnostic evidence only. They do not prove that a particular
Module, version, relationship, or test is unnecessary.

## Pinned Standards Snapshots

| Period | Effective standards boundary | Material facts |
| --- | --- | --- |
| A1 formation and original implementation | parent `13a9f48b95ed7532f480e4604d9dfa23443e8f43`; A1 starts at `c7d23dfa` | Core simplicity, Architecture concern ownership, Contracts proof lifetime and invariant rules, typed Verification claims, conditional Security, Resilience, Diagnostics, Planning, Implementation, Router, prompts, and plan template were already present. Generated Contract, explicit evidence-oracle boundaries, systemic-finding replanning, and Immutable Authority Closure were absent. |
| A1 repair sequence and acceptance | standards prose remains materially the `13a9f48b` snapshot through implementation `2359a987` and acceptance `933c9ab9` | A1 changed runtime, fixtures, graph metadata, and plan evidence, but no applicable normative Core/Architecture/Contracts/Verification/Planning/Security/Resilience/Diagnostics/Router rule changed during the A1 implementation and repair interval. |
| A1b redesign trigger | `3439aae9540786d9734431e633ea5b62afb50592` | The redesign brief records defects, identifies routing omissions, and proposes standards recovery before A1b. It is a report, not yet normative authority. |
| Standards recovery policy | normative batch `7a571ed26a132056368ef465d6041910c5a6ed48`; executable projections `0a7fb2da`; policy-impact v2 `9bbc1e05` | Adds Generated Contract routing/profile, generated semantic conformance, schema dialect/vocabulary, equality-domain separation, Immutable Authority Closure, implementation-versus-dependency, evidence-oracle boundaries, negative-fixture isolation, differential evidence, and systemic-finding replanning. |
| Accepted standards-recovery base | candidate `a166e36f6f0c8d4d0620c98666027462e62a7b80`; completion `c4408363752b10060f631247f3e2f1fa26eae003` | A1b planning explicitly uses this boundary. It contains 41 policy units and 207 direct policy-impact relationships by a direct TOML inventory; the acceptance report records 224 suites, 53 retained checkers, and 585 focused package tests. |
| A1b initial through C4 planning | `c4408363`, followed by A1b plan `f41037bf`, C through C4 at `44de7dff`, `ecdf5a55`, `c2aea75c`, `ebc75340`, and `b92ed782` | Recovery rules are fully effective. No A1b runtime implementation is admitted; repeated independent planning reviews expand contract, membership, authority, persistence, platform, and evidence obligations. |
| Authority/version-scope correction | `396144ad9a75c948484d1e564fab73c857bd6f4d` | Adds Architecture Authority Scope Admission and Contracts Declaration And Semantic Authority and Version Scope And Invalidation, with prompts, plan-template projection, fixtures, a suite, 44 graph relationships, and full coverage renewal. |
| C5/C6 and process correction | C5 `4f69f994`, C6 `9794b927`, topology replan `d06c819b`, standards correction `1d18b70d` | The new authority rules directly supersede C4 version bags. Immutable closure drives C5/C6 authority work. A1b's commit-topology protocol is then recognized as process machinery inconsistent with existing ownership; Planning is strengthened to reject it generally. |
| C7 and accepted A1b | C7 `748d30f7`, simplified C7 `36dd7579`, implementation `84412f22`, acceptance `580d9c95` | No later Core, Security, Resilience, Diagnostics, or Implementation policy change occurs. A1b implementation expands direct policy-impact relationships to 387 and adds three existing-heading policy-unit projections for Cross-Platform, Security, and Dependencies without changing their normative prose. |

The stage-by-stage A1b boundary is exact:

| A1b stage | Plan commit | Effective general standards snapshot |
| --- | --- | --- |
| initial admitted plan | `f41037bf71deddba36056b27d418fe767a7cfb62` | accepted recovery `c4408363752b10060f631247f3e2f1fa26eae003` |
| C | `44de7dff9c83f08b24225c82ad1b6a974f6655a9` | `c4408363752b10060f631247f3e2f1fa26eae003` |
| C-prime | `ecdf5a55588d18d068a513d910959ccbd9c65f71` | `c4408363752b10060f631247f3e2f1fa26eae003` |
| C2 | `c2aea75c85800aec6ac00fcc3b2690f8629845ab` | `c4408363752b10060f631247f3e2f1fa26eae003` |
| C3 | `ebc75340781bf032164d93817edca7c5a04ba892` | `c4408363752b10060f631247f3e2f1fa26eae003` |
| C4 | `b92ed7828982723d0118294ea1a09f30001ad25e` | `c4408363752b10060f631247f3e2f1fa26eae003` |
| C5 | `4f69f9940b806ca602f44dab7aa00c1df4db8abd` | authority/version correction `396144ad9a75c948484d1e564fab73c857bd6f4d` |
| C6 | `9794b92708aad42c4838f9ad5c6b78e3984d73b3` | `396144ad9a75c948484d1e564fab73c857bd6f4d` |
| topology replan | `d06c819bca5f29583c425dd49cd869842ad7d75f` | `396144ad9a75c948484d1e564fab73c857bd6f4d`; this A1b replan precedes the general correction |
| C7 | `748d30f778ba04ddbf33e3b82fb8031cf947c815` | topology-corrected standards `1d18b70d99db48317de2cc9243fc06b133d7329a` |
| C7 contract closures | `ac362dc5f6ca2ac51c9b593cecde3639f4a883fb`, `ee7f2a47b5497112f3c8ce81c1ed45de3921bab9` | `1d18b70d99db48317de2cc9243fc06b133d7329a` |
| simplified C7 | `36dd75790b2f08a6e66624ccae4f8530bc111a92` | `1d18b70d99db48317de2cc9243fc06b133d7329a` |
| implementation and acceptance | `84412f22fa9fe082f089eaa347c30c23f185ffee`, `580d9c959b22f3fdeb0898e7fd4aafd168893580` | no later normative prose change; A1b adds policy-unit and graph projections of existing Cross-Platform, Security, and Dependencies headings |

A1's implementation sequence from `3383ec6827f4d84adbbcc972dc17387c4daab6bd`
through initial product acceptance `e61e9567382b15e467da8d77a8a73671a2ea3e93`,
then its six repair implementations from
`51dcd258942b0774c73ae8b620227c7ce34d1129` through
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, all retained the pre-A1 general
standards snapshot. The repair candidate and acceptance documentation changed;
the routed general standards did not.

The exact accepted A1 and A1b identities come from their final acceptance
reports: [A1 final acceptance](../../standards-engine-navigation-analysis/reports/a1-final-acceptance.md)
at commit `933c9ab9`, and
[A1b final acceptance](../../standards-engine-a1b/reports/a1b-final-acceptance.md)
at commit `580d9c95`.

## Standards Lineage Before A1

### Generalization and simplicity

The standards were imported and generalized from a project-specific repository
at `433b1d3d4159ecdc921c3f88ed9a84089034ed31` on 2026-02-05. The first explicit
simplicity revision at `f98272c5e98257ffe47265b1932981b3663daf00` on
2026-05-28 defined simplicity as reduced conceptual entanglement and required
abstractions to remove caller reasoning load. Commit
`38a01a004c94ac7e8a93f087cf290ef01c778f0a` moved this into canonical
[Core](../../../../CORE-STANDARDS.md) on 2026-07-30 and added the executable
`core-simplicity` decision table.

At A1's base, Core already required:

- separation by independent change reasons, but retention of coherent behavior;
- the least code and structure needed for owned behavior;
- additional structure only for independent decisions, enforceable invariants,
  reduced repeated reasoning, or demonstrated variants;
- abstractions only when callers can safely ignore an owned concern; and
- deletion of adapters and paths without a current supported contract.

The same snapshot also said “More named components can be simpler.” This is not
contradictory in isolation, but it creates a material interpretation risk when
reviewers can satisfy ownership questions by naming more concepts without
showing that the composed Interface is deeper.

The fixture at
`evaluation/standards-effectiveness/fixtures/core/simplicity-decisions.tsv`
was unchanged in every material respect from `38a01a00` through accepted A1b.
Its inputs are `coherence`, `ownership`, `change_axes`, `invariants`,
`lifecycle`, `failure`, a prohibited metric, and fallback. Its executable suite
defaults to `separate` and chooses `keep-together` only for `coherence=one` and
`change_axes=one`. It contains no dimension for:

- caller knowledge or exposed Interface concepts;
- representation and transformation count;
- composition-root burden;
- number of coordinated versions;
- ordinary change propagation;
- duplicate validation or evidence;
- operational prerequisites; or
- machinery removed versus introduced.

The fixture proves that visible counts and smallest-diff defaults do not decide
decomposition. It does not prove that a collection of individually owned
Modules has good Depth, Leverage, or Locality. This is a **standard present but
weakly enforced** finding with high confidence. The possibility that its
default-to-separate structure encouraged fragmentation is **unresolved** with
medium-low confidence because no A1b decision cites the fixture as its reason.

### Contracts, validation, invariants, and typed diagnostics

Before A1, Contracts had already accumulated several strong rules:

- `286dc75a1a017258d4124225accd537fb462dcd1` established Validation Proof
  Lifetime: intact proof-bearing values are consumed directly, not decoded
  again; new proof is required only after proof loss, unchecked mutation,
  contract change, or a new trust/process/persistence/plugin/queue/independent-
  deployment seam.
- `8b7ff7e61ce552a1611d257cef050949b0caa391` established Invariant Contracts,
  including static proof as a valid evidence mechanism and a warning not to
  require one test per sentence.
- Contract Artifact Necessity already rejected DTOs, schemas, Interfaces, and
  generated artifacts that merely mirror another representation without a
  distinct ownership, validation, representation, evolution, or transport
  obligation.

There was also tension. Invariant Contracts ended with a universal prohibition
against “debug-only enforcement, release logging, panic, recovery, graceful
abort” as a fallback for an invariant. Architecture and many contract sections
required typed `invalid`, `unsupported`, and `unavailable` outcomes. That text
does not distinguish an external or durable contract violation from a contained
internal programming defect that fails immediately with adequate stack and
trace information. It can therefore be read as requiring supported validation
and typed failure machinery for impossible internal states.

This is **conflicting or ambiguous guidance** with medium-high confidence.
Proof Lifetime says not to revalidate intact internal values, but Invariant
Contracts can be read to require runtime enforcement and typed outcomes for all
material invariants. The record does not prove which A1b checks were added
because of that ambiguity, so individual necessity remains **unresolved**.

### Verification and Implementation

Verification was already substantially claim-directed before A1:

- `b41ea98133c157fd7a0f4479e79279d5707b979d` modeled acceptance as typed
  claims;
- `344c6311c73a0823bb5b2bacd7ea4194855ec015` separated test and release
  evidence ownership;
- `b53c3ff0e4f6bab877e9d4556273722f38233d26` governed focused test design;
- `c419dfe8fc6a7f9ea3a845c3d4d1710a707565a5` made coverage diagnostic rather
  than acceptance by itself; and
- `e66dd66a457d5e9545ad03a00c19cf324df47679` governed supporting and diagnostic
  gates.

At A1's base, [Verification](../../../../workflows/verification.md) required the
“smallest complete claim set,” prohibited unrelated high-cost claims, said not
to assert every internal hop, derived edge cases from actual domains rather
than universal empty/null/failure lists, limited coverage to named risks, and
recognized compilers, traces, logs, and focused probes as diagnostic tools.

At the same time, Core still said “Add the smallest test that fails for the
defect or missing behavior,” and
[Implementation](../../../../workflows/implementation.md) required every slice
to include focused regression or acceptance evidence and to update source and
focused tests or fixtures together. Neither Verification nor Implementation
asked whether:

- the prohibited failure was reachable;
- a type, constructor, compiler, or existing validator already made it
  impossible;
- another accepted check already detected it at adequate fidelity;
- fail-fast behavior and ordinary debugging were sufficient for a contained
  internal defect;
- a check was temporary scaffolding; or
- a later Interface-level claim subsumed an earlier internal check.

The absence of an evidence-necessity, substitution, and lifecycle rule is a
**standard absent** finding with high confidence. It explains how an extensive
portfolio could remain standards-compliant, but it does not prove any specific
A1 or A1b test redundant.

### Security, Resilience, Diagnostics, and threat models

Security was not an unconditional validation mandate. At A1's base,
[Security](../../../../topics/security.md) applied only when untrusted input
could authorize an operation, resource access, side effect, or security-
relevant decision, or when a network listener admitted work. It explicitly did
not apply when no untrusted value influenced authority or security behavior.
Filesystem Containment asked whether an attacker could mutate components
concurrently and allowed revalidation when the recorded threat model excluded
such mutation.

[Diagnostics](../../../../topics/diagnostics.md), established at
`6ed47adc97aa544ee5a67ac89477842354344bde`, selected diagnostics only for an
accepted operator, support, consumer, or verification claim and rejected
duplicate failure logging at every layer. [Resilience](../../../../topics/resilience.md),
including its failure-boundary revision at
`759eb7349e9f3c2d461eef049a88a32b5488e9f6`, required translation at the
narrowest owner and likewise rejected catch/log/wrap/rethrow at every layer.

A1b did record a scoped storage threat model in
[the C7 SQLite audit](../../standards-engine-a1b/reports/c7-sqlite-storage-audit.md):
the store path is trusted configuration; same-principal malicious mutation is
excluded; another principal racing a writable parent is not. This is important
counterevidence to a claim that A1b wholly ignored threat models.

The general gap is narrower: no routed workflow requires each validation,
negative test, integrity check, or internal failure projection to identify
whether it answers an adversarial threat, unknown-input seam, independently
evolving representation, persistence risk, concurrency risk, or ordinary
programmer defect. Security owns adversarial threats, but Verification and
Contracts do not require an equivalent scoped correctness-risk record before
machinery is admitted. This is a **standard absent** finding with high
confidence; whether a large fraction of A1b's internal checks would disappear
under such a model remains **unresolved**.

## A1 Formation Under The Standards

A1 starts at `c7d23dfa55a9558b929e6b838d7ea0563981a1ef`, whose parent is the
accepted verification-engine boundary `13a9f48b`. Its authoring brief and plan
made several choices that later became important causal evidence.

### One schema as several authorities

The A1 plan's A8 criterion and Binding Decisions made one Draft 2020-12 schema
the sole machine authority for Python types, JSON validation, agent-tool
definitions, examples, identity-bearing serialization, result variants,
derived next operations, and text rendering. Its constraints declared
“Canonical schema authority is singular.”

This outcome had two standards causes:

- Core required one canonical owner and prohibited second sources of truth;
  Contracts allowed an owned schema or generator input as canonical authority.
- Core and Architecture also required separation of concerns that change for
  different reasons and required abstractions to hide unrelated reasoning.

The standards did not say how to resolve these directions when one declaration
could *contain* many semantic families. The A1 plan interpreted singular source
authority as broad semantic authority. The later authority-scope review at
`396144ad` concluded that the principle existed “in fragments” but the routed
admission system had no concrete gate.

Classification: **conflicting or ambiguous guidance** and **standard present
but unenforced/misapplied**, high confidence. It is not credible to classify
the problem as a total absence of concern-separation guidance.

### Routing omissions

A1 explicitly routed Planning, Implementation, Verification, Documentation,
Tooling, Commit, Architecture, Contracts, Diagnostics, Security,
Cross-Platform, and Persistence. It did not route:

- Build, despite changing generators and generated outputs;
- Library, despite creating reusable Python packages; or
- Dependencies, despite choosing to implement a JSON Schema subset locally.

The A1b redesign brief at `3439aae9`, section 4.7, records these exact
omissions. Build, Library, and Dependencies already existed in the Router at
the A1 snapshot. The Generated Contract profile did not, and Language Binding's
wording did not cleanly apply to ordinary schema-to-Python generation.

Classification: Build, Library, and Dependencies are **standard present but
unrouted**, high confidence. Generic Generated Contract applicability is
**standard absent**, high confidence. IPC applicability was and remains
fact-dependent; no external or independently deployed A1 consumer was found,
so its omission is not established as a defect.

### Contract interpretation and evidence

A1's successive repair candidates corrected incomplete generated reachability,
Boolean/integer behavior, Unicode equality, pattern behavior, public result
types, private imports, cold inspection, and negative fixture diagnostics.
Accepted implementation `2359a987` passed two locally maintained equality
implementations. After acceptance, the A1b brief compared both with the
declared Draft 2020-12 data model and showed that both were wrong for
codepoint-distinct Unicode strings.

The A1-era Verification workflow already said evidence proves only the claim it
can observe and required a usable oracle for property testing. It did not yet
state that expected semantics must be independent of the subject under test or
that agreement between local projections proves consistency rather than
external conformance. The repair process also repeatedly fixed the latest
example without an explicit systemic-family replan rule.

Classification: explicit independent-oracle and systemic-family rules were
**standard absent**, high confidence; general evidence-sufficiency guidance was
**present but insufficiently enforced**, medium-high confidence. The local
validator and generated decoder were **implementation choices**, high
confidence.

### Immutable handles and ambient authority

A1's product contract independently promised immutable, snapshot-bound handles,
same-snapshot navigation, and cold inspection. The initial implementation still
allowed whole-module reads from the live worktree and cold child inspection
through instance-local or fresh authority. The A1 repairs corrected those
defects before acceptance.

Architecture already rejected ambient global infrastructure and duplicate state
authority. Persistence, Contracts, and the A1 plan itself supplied substantial
direction. What was absent was an explicit rule that an inspectable/replayable
handle bind the *complete transitive authority closure* and never depend on a
fresh provider, originating process, or cache.

Classification: the replay promise is a **product requirement**; the failures
were **implementation choices** and **standard present but incompletely
enforced**; transitive closure wording was **standard absent**. Confidence is
high for all three. The conclusion does not imply that a generic object
repository, per-owner codec, SQLite, or all later A1b machinery was required to
meet the promise.

### A1 acceptance did not validate whole-design simplicity

The final A1 acceptance report records zero independent Standards findings and
zero specification findings, 145 focused package tests across Analysis,
Engine, and Metadata, 380 Verifier tests, 218 declarative suites, and 53 retained
Bash checkers. The accepted plan contained a Simplicity And Ownership Review,
but neither that review nor the `core-simplicity` suite tested caller knowledge,
schema semantic span, representation count, change Locality, or evidence
overlap.

Classification: **standard present but unenforced at whole-design level**, high
confidence. Counts establish the size of the evidence portfolio, not its
redundancy.

## Standards Recovery After A1

### The recovery rules share a source with A1b

The A1b redesign brief at `3439aae9` was written 44 minutes after A1 acceptance.
It preserved the four-operation facade and analysis kernel but identified two
supporting seams: duplicated contract semantics and incomplete immutable
authority. It proposed:

- evidence-oracle boundaries;
- Generated Contract semantic conformance and routing;
- schema dialect/vocabulary and equality-domain separation;
- Immutable Authority Closure;
- implementation-versus-dependency decisions; and
- systemic-finding replanning.

Commit `7a571ed2`, seven hours later, added those rules in
[Architecture](../../../../topics/architecture.md),
[Contracts](../../../../topics/contracts.md), Dependencies, Planning,
Verification, the Router, and a new Generated Contract profile. Commit
`0a7fb2da` then added prompts, template fields, six suites, decision fixtures,
and 57 direct graph relationships for the selected policy units. Policy-impact
v2 at `9bbc1e05` made source-owned relationships and independent coverage
executable.

This chronology prevents a simplistic causal claim. The A1 defect analysis
produced both the standards and the proposed A1b shape. **Common cause** is the
primary explanation for their initial agreement. Later A1b replans provide
stronger causal evidence because they explicitly cite the now-effective rules.

### What the recovery genuinely improved

The recovery addressed demonstrated A1 defects rather than abstract style:

- Generated Contract policy distinguishes declaration freshness, reachable
  shape, semantic behavior, and public producer/consumer behavior.
- Evidence Oracle Boundaries rejects local agreement as an external oracle.
- Negative Fixture Isolation requires a fixture to reach its intended failure.
- Identity And Instance Equality separates schema, domain, and identity
  relations.
- Implementation Versus Dependency made the implementation-versus-dependency
  choice explicit and A1b selected `jsonschema` rather than another local Draft
  interpreter. The redesign brief had already proposed that direction, so the
  selection is also common-cause evidence rather than a standards-only effect.
- Systemic-Finding Re-Planning requires an invariant family and sibling
  consumer inventory rather than the next local patch.

Accepted A1b's contract foundation is therefore not evidence of unnecessary
machinery by itself. It replaces two faulty semantic implementations with one
selected dependency and a project Adapter. These changes have direct defect and
external-contract evidence and classify primarily as **product requirement**
and **corrected implementation choice**.

### What the recovery did not constrain

The new decision fixtures decide whether a source has an independent oracle,
whether a schema feature is supported, whether authority is ambient, and
whether a finding is systemic. They do not decide whether the complete selected
guarantee is worth its operational and maintenance cost or whether a simpler
Interface can supply it.

In particular, the `immutable-authority-decisions.tsv` fixture admits exact
captured storage and rejects ambient/process-local reconstruction, but it does
not compare a persisted aggregate, a content-addressed object graph, a bounded
snapshot, or an intentionally process-local handle. The systemic-replanning
fixture requires complete sibling inventories but has no stop rule based on
marginal risk, caller-visible consequence, proof substitution, or implementation
cost.

Classification: the recovery is **correct but incomplete standards guidance**,
high confidence.

## A1b Planning And Direct Standards Influence

### Initial route and plan

A1b planning began from accepted recovery boundary `c4408363`. Its ledger says
the Router selected Planning, Implementation, Verification, Documentation,
Build, Tooling, Architecture, Contracts, Dependencies, Licensing, Security,
Diagnostics, Library, Persistence, and Generated Contract. IPC and Language
Binding were explicitly excluded from the observed in-process, no-independent-
consumer facts. Later review added Concurrency, Resilience, Release, and
Cross-Platform for durable publication, interruption/retry, dependency
distribution, and filesystem identity.

This is evidence that the recovery fixed A1's routing omissions. It also made
many more canonical owners applicable to every A1b design review. That increased
coordination is partly the real cost of A1b's durable and generated-contract
requirements and partly the cost of the standards' projection model.

### Immutable Authority Closure

The normative rule added at `7a571ed2` says an immutable, replayable, or
inspectable handle binds every authority, contract, provider input, and
authorization view that can affect advertised results through exact immutable
identities. It prohibits ambient mutable state, instance caches, originating
process dependence, undeclared providers, fresh authorization, and unbound live
reads. It assigns reopening to Persistence and exact typed failures to
Contracts.

The [C6/C7 design history](../../standards-engine-a1b/reports/c6-c7-design-history-research.md)
states that C6's transition-complete closure was “a defensive response” to this
rule. C5/C6 added or refined:

- content snapshots and authority views;
- `AuthorityBoundValue`;
- role- and side-qualified execution roots;
- materialized or derived dependency closure;
- exact owner codec membership;
- per-operation authority contracts;
- provider and authorization objects; and
- cold direct storage for every advertised inspectable family.

C7 later removed complete views, copied dependency lists, hypothetical-future
trust, capture metadata, and other overreach while retaining roots-only
transitive closure and direct stored-object inspection.

The policy graph gives independent mechanical evidence of influence. At
accepted recovery boundary `c4408363`,
`topic.architecture.immutable-authority-closure` had 7 direct relationships:
Persistence, four A1 implementations, one fixture, and one suite. At accepted
A1b implementation `84412f22`, it has 27: one normative consumer, 22
implementation projections, three fixtures, and one suite. The current
declaration is
`evaluation/standards-effectiveness/policy-impact/topic.architecture.toml`.

Classification:

- exact cold replay for every advertised handle — **product requirement**, high
  confidence, because A1b A1B-A4 states it independently;
- exact transitive closure and prohibition on ambient/fresh authority —
  **standard plausibly induced machinery**, high confidence;
- generic envelope, closed codec sets, roots-only DAG, SQLite layout, backup,
  restore, syscall interruption, and every object family — **implementation
  choice**, high confidence;
- whether those mechanisms are proportionate to actual consumers —
  **unresolved**, high confidence.

The rule's phrase “immutable, replayable, or inspectable handle” is broad. It
does not first require an actual consumer promise for cold reconstruction,
lifetime, portability, or failure behavior. A project-agnostic standard could
retain the no-ambient-authority principle while making full transitive cold
replay conditional on a declared consumer contract.

### Authority and version scope

The authority-scope standards at `396144ad` were added during A1b planning,
after C4. Their own impact review says the previous standards had the right
principle in fragments but no routed admission record. The new rules require:

- one authority only for coherent responsibility with aligned owners,
  lifecycles, invariants, and change reasons;
- declarations to reference rather than acquire independently owned semantics;
  and
- versions and identity invalidation to follow one compatibility promise rather
  than file, schema, build, release, or cutover co-location.

The A1b ledger explicitly says these accepted standards “confirm” C4's version
bags and umbrella authority as a systemic defect. C5 removes
`SnapshotVersions`, `NavigationVersions`, `AnalysisVersions`, generic
`VersionMap`, snapshot-as-query authority, and broad provider/authorization
authority. It replaces them with domain-owned identity records, owner codecs,
reference-only views, and structurally composed closure. This is direct causal
evidence, not chronology alone.

At accepted A1b, the graph records 10 direct relationships for Authority Scope
Admission, 16 for Declaration And Semantic Authority, and 17 for Version Scope
And Invalidation. The accepted plan lists interface v11, request v3, result v3,
handle v4, envelope v1, identity encoding v2, and independently scoped owner,
payload, operation, and result versions.

Classification:

- rejection of umbrella authority and unrelated invalidation — **standard
  plausibly induced**, high confidence;
- separate semantic owners — both **product correctness requirement** and
  **standard plausibly induced**, high confidence;
- the particular number and placement of codecs, records, and versions —
  **implementation choice**, high confidence;
- whether the total compatibility matrix is excessive — **unresolved**, because
  neither the standard nor fixture measures cumulative coordination cost.

The authority-scope fixture admits or rejects each scope independently. It has
no case where several individually valid authorities create an unreasonably
shallow composed Interface. The version fixture similarly tests each promise
but not the global version matrix. That is a project-agnostic standards gap.

### Systemic-finding replanning and expanding review scope

The systemic rule was intended to stop A1's example-by-example repairs. In A1b
it repeatedly expanded reviews to complete families: relationship registration,
public roots and `__all__`, entrypoint execution, codec membership, operation
roles, coverage sources, Git-index ownership, typed suite inputs, and governed
source analysis. Many were responses to actual review findings; later reviews
continued to find sibling defects.

This record supports two conclusions at once:

- systemic review found real inconsistencies that local smoke tests missed;
- the rule offered no proportionality or termination criterion other than
  complete inventory and non-blocked disposition.

The accepted A1b ledger records review matrices growing from 24 to 41 to 45
direct package-import and Git-reachability regressions, plus repeated complete
checkpoints. That is evidence of verification growth, not evidence that any
test was unnecessary.

Classification: **standard plausibly induced machinery**, medium-high
confidence for the inventories and class-level evidence; **implementation
choice**, high confidence for the AST evaluator, Git Adapter, and exact test
matrix; necessity of individual checks **unresolved**.

### Planning's Git-topology overreach and correction

A1b's C6-R-T-S protocol prescribed a direct-child review/admit/start chain,
exact-HEAD review, standalone lifecycle commits, and intervening-commit
invalidation. The 2026-08-27 ledger identifies this as a self-reinforcing
administrative loop and says it contradicted existing Planning,
Implementation, and Commit ownership.

Commit `d06c819b` removed the A1b-specific protocol. Commit `1d18b70d` then
changed general Planning, its prompt, template, fixture, suite, policy graph,
and all 44 coverage attestations so plans cannot own commit count, parentage,
ancestry, exact-HEAD admission, or state-only lifecycle commits.

Classification: the original protocol was **standard present but misapplied**
and **implementation/process choice**, high confidence. The general correction
is evidence that the standards can learn from A1b without becoming repo-
specific. It also exposes the administrative cost of the coverage model: one
small Planning semantic revision changed the global horizon and required all 44
subject attestations to be renewed even though only a bounded subset of
consumer meaning changed.

### Policy-impact graph and coverage fanout

Planning's Policy Projection Completeness rule predates A1 and requires every
normative change to query and disposition affected policy consumers. A1 then
made exact impact and successful-empty coverage a product feature. Standards
recovery made source-owned relationships and independent coverage executable.

Direct TOML inventories at fixed worktrees show:

| Boundary | Policy units | Direct policy-impact relationships |
| --- | ---: | ---: |
| accepted standards recovery `c4408363` | 41 | 207 |
| authority-scope acceptance `396144ad` | 44 reported by its review | 251 reported by its review |
| Planning topology correction `1d18b70d` | 44 | 253 reported by its guardrail |
| accepted A1b implementation `84412f22` | 47 | 387 |

The three later units are projections of unchanged existing Cross-Platform,
Security, and Dependencies headings added so A1b implementation relationships
could be registered; they are not new normative meanings.

Selected source fanout changed as follows:

| Policy unit | Recovery direct relationships | Accepted A1b direct relationships |
| --- | ---: | ---: |
| Generated Contract Semantic Conformance | 12 | 22 |
| Identity And Instance Equality | 7 | 17 |
| Immutable Authority Closure | 7 | 27 |
| Evidence Oracle Boundary | 6 | 6 |
| Systemic-Finding Replan | 6 | 6 |

The graph accurately records real implementation consumption. Its cost is not
automatically a defect. The proportionality concern is the coverage horizon:
several reports show that changes to registered suite content or graph inputs
can stale every coverage requirement, even where a policy unit's semantic
meaning and direct consumers are unchanged. That broad invalidation helped
drive A1b's repeated freeze, renew, and revalidate cycles.

Classification:

- policy-impact analysis and successful-empty coverage — **product requirement**
  for A1 and A1b, high confidence;
- mandatory consumer disposition for standards changes — **standard plausibly
  induced process machinery**, high confidence;
- provider-wide horizon invalidation and exact attestation/certificate model —
  **implementation choice**, high confidence;
- whether a narrower dependency-invalidating coverage model can preserve the
  guarantee — **unresolved**.

## Verification Causality Across A1 And A1b

### Rules that prevented false confidence

The recovery Verification rules have clear value:

- generated freshness no longer stands in for semantic completeness;
- two local implementations no longer establish external conformance;
- negative fixtures must reach their intended diagnostic;
- exact literals prove only literal identity when that is the contract; and
- property and differential evidence declares its input and unsupported
  domains.

These rules directly address accepted A1 failures. They should not be removed
merely because the evidence portfolio is large.

### Rules that fail to decide necessity

The standards still admit a check once it can name a coherent claim and an
adequate oracle. They do not require proof that the claim needs a permanent
check. Examples raised by the audit remain unaddressed:

- a runtime wrong-type case that cannot enter through the typed construction
  path;
- an internal value already covered by an intact proof-bearing representation;
- a file digest where exact bytes are not identity, security, persistence, or
  publication authority;
- a negative fixture for an impossible state that would fail immediately and
  safely if a programmer somehow created it;
- an internal test completely subsumed by the public Module Interface; or
- a verifier that proves only that another check or declaration exists.

Contracts already says not to revalidate intact proof-bearing values, and
Verification already says not to assert every internal hop. If A1 or A1b does
so, it is at least partly **standard present but misapplied**. However, no rule
requires explicit evidence-subsumption review, and no fixture tests these cases;
that part is **standard absent**.

The accepted A1b report records 226 declarative suites, 53 retained Bash
checkers, and large package suites. Those counts trigger this audit; they do not
decide redundancy. A claim-level verification report must inspect reachability,
consequence, oracle, overlap, static proof, diagnostic sufficiency, cost, and
removal condition before recommending deletion.

### Digests and exact identities

A1 and A1b use hashes for several different purposes: content-addressed
handles, exact snapshots, locked dependencies, generated freshness, policy
coverage, and some recorded artifact identities. Content-addressed identity,
dependency integrity, and exact replay are real contracts. A hash is not
redundant simply because Git also tracks the file.

The standards lack a general decision rule that limits exact-byte assertions to
contracts where byte identity, supply-chain integrity, mutation detection,
persisted reconstruction, or publication identity is material. Evidence Oracle
Boundaries says an exact literal proves only literal identity, which prevents a
false semantic claim but does not decide whether literal identity is worth
checking.

Classification: **standard absent**, high confidence; individual A1b hash
necessity **unresolved**.

### Errors, assertions, traces, and debugging

Diagnostics and Verification already recognize exceptions, compiler output,
traces, logs, state inspection, and focused probes as legitimate diagnosis.
They correctly say diagnostics do not change an operation outcome and should
not be emitted at every layer.

Invariant Contracts, in contrast, rejects panic, graceful abort, and debug-only
enforcement without classifying the failure first. No canonical rule clearly
distinguishes:

1. unknown or adversarial boundary input;
2. expected recoverable operational failure;
3. internal programming defect with immediate contained fail-stop behavior; and
4. rare internal corruption capable of silent, durable, security, or
   irreversible harm.

Without that classification, typed validation and negative tests can spread
from real trust seams into ordinary internal workings. This is **conflicting or
ambiguous guidance**, high confidence. The appropriate later correction should
not authorize silent corruption or replace tests for known regressions. It
should permit assertions, propagated exceptions, and ordinary traces when a
scoped risk model shows that permanent validation machinery has no distinct
protective value.

## Consolidated Causal Classification

| Observed outcome | Classification | Evidence | Counterevidence / limit | Confidence |
| --- | --- | --- | --- | --- |
| A1 schema owns representation, validation, identity-related serialization, results, tools, and rendering | conflicting/ambiguous guidance; present but misapplied | A1 A8 and plan Binding Decisions; Core one-owner plus concern-separation rules; `396144ad` gap report | One declaration can legitimately generate several representations when they share one promise | high |
| A1 local schema interpreters disagree with Draft 2020-12 while agreeing with each other | standard absent for explicit independent oracle and generated semantic profile; implementation choice | A1b brief section 3/4; recovery equality reproduction; rules added at `7a571ed2` | A1-era Verification already required objective-aligned oracles generally | high |
| A1 omitted Build, Library, Dependencies | present but unrouted | A1b brief section 4.7; Router at `13a9f48b` | Generated Contract profile genuinely absent and Language Binding ambiguous | high |
| A1 snapshot/cold inspection used live or process-local authority before repair | product requirement; implementation choice; closure rule absent | A1 plan A2/A3/A8; SENA-021/022; later closure rule | Architecture already prohibited ambient state generally | high |
| A1 repair candidates fixed sibling defects sequentially | systemic replan absent; implementation/review choice | SENA-021/022 and repair reports; systemic rule added after | Some sibling defects were discovered only after stronger evidence existed | medium-high |
| A1b adopts `jsonschema` and removes local Draft interpreter | product requirement and corrected implementation | A1 external disagreement; Dependencies recovery rule; A1B-A1 | Dependency adds supply-chain and platform work | high |
| A1b creates full immutable authority repository and exact closure | product requirement plus standard plausibly induced machinery | A1B-A4/A4C; C6 report calls response defensive; graph grows 7 to 27 consumers | Full cold replay is expressly accepted; selected storage mechanics are not prescribed | high for influence; unresolved for proportionality |
| A1b separates versions, identities, domain objects, and codecs | standard plausibly induced plus implementation choice | `396144ad`; C4 rejection explicitly cites it; accepted version/object matrix | Separation corrected real umbrella invalidation; exact count is not prescribed | high |
| A1b AST import/governed-source analysis and exact membership matrices | implementation choice; systemic rule plausibly induced audit breadth | repeated C/C-prime/C2 and post-cutover review findings | Private import leaks and dynamic capability paths were actual defects | medium-high |
| A1b SQLite fsync/fdatasync interruption, backup, and restore evidence | product requirement plus implementation choice | A1B-A4 required-real; C7 SQLite audit | Immutable closure does not itself mandate SQLite or syscall injection | high |
| A1b repeated complete coverage renewal | product requirement plus standard-induced process and coverage implementation choice | Planning projection completeness; `1d18b70d` guardrail; coverage reports | Exact coverage prevents silent missing consumers | high |
| A1/A1b extensive test and verifier portfolio | standard absent for marginal necessity/lifecycle; some present guidance misapplied; redundancy unresolved | Verification text, Core/Implementation test rule, accepted reports | Repeated reviews found real defects; counts alone prove nothing | high for standards gap; unresolved for individual checks |
| Internal typed failures and validation machinery | conflicting/ambiguous invariant guidance; implementation choice | Contracts Proof Lifetime versus Invariant Contracts final prohibition | Many values cross JSON, SQLite, Git, process, plugin, or public seams and need validation | medium |
| A1b threat-model awareness | present in Security and storage design; broader correctness-risk admission absent | Security applicability; C7 store threat model | Not every internal Interface needs a security threat model | high |
| C6 Git commit-topology protocol | present but misapplied; implementation/process choice | A1b ledger and `1d18b70d` correction | Content-bound review still requires stable identity | high |

## Candidate Project-Agnostic Standards Shortcomings

These are evidence-supported candidates for later standards design. They are
not settled normative wording.

### 1. Whole-design Depth and composition are not admitted

Core and Architecture evaluate concern ownership but not whether the resulting
Module Interfaces hide more reasoning than they expose when composed. A later
standard should consider caller knowledge, deletion tests, real versus
hypothetical Adapters, composition-root burden, and representative change
Locality. It should preserve the current rejection of raw file/type/test count
thresholds.

Evidence: `core-simplicity` fixture limits; A1 umbrella schema; accepted A1b's
broad internal ownership and version matrix; current graph fanout.

### 2. “Least sufficient machinery” lacks an admission mechanism

Core says “least code and structure,” but planning, review, and fixtures do not
require each new Module, representation, version, registry, validator, store,
or verifier to name the material reasoning or risk it uniquely removes. A
later rule could require a simpler considered alternative for materially
complex designs and a cumulative review when machinery grows.

Evidence: A1b C1-C7 replans; authority/version fixtures decide ownership but not
aggregate cost; repeated accepted local corrections.

### 3. Evidence needs marginal-necessity and lifecycle review

Verification should distinguish “this check can prove a true claim” from “this
claim needs this permanent check.” Candidate dimensions are reachable failure,
material consequence, adequate independent oracle, static or construction
proof, overlap/subsumption, diagnostic value, cost, and removal condition.

Evidence: Verification already asks for smallest claims but has no such fixture;
Core/Implementation encourages a focused regression per defect/slice; A1/A1b
portfolios accumulate; no individual redundancy is yet proved.

### 4. Failure classification should precede validation machinery

Contracts should distinguish unknown external input, expected recoverable
failure, internal fail-stop programming defects, and internal defects with
silent/durable/security consequences. Typed validation and negative tests are
appropriate at applicable trust, process, persistence, plugin, independent-
deployment, or public seams. Assertions, propagated errors, and trace-led
debugging may be sufficient for contained internal defects.

Evidence: Proof Lifetime and Diagnostics already support internal trust and
diagnosis; Invariant Contracts' blanket no-panic/no-debug wording creates the
ambiguity.

### 5. Threat and correctness-risk models need scoped application

Security already models adversarial filesystem capability correctly, but there
is no general route from each validation/evidence decision to the relevant
actor, input authority, mutation capability, persistence/concurrency mechanism,
failure consequence, proof lifetime, and residual risk. The general rule should
not label all internal code untrusted.

Evidence: Security applicability and C7 store threat model are positive
examples; A1b's broad internal validation and hostile-environment matrices lack
one common risk-admission format.

### 6. Full immutable closure should be conditional on the promised lifetime

The prohibition on ambient substitution is well supported. Full transitive,
content-addressed, cold-process reconstruction should follow an explicit
consumer promise naming lifetime, supported operations, persistence, allowed
environment dependencies, and failure behavior. The standard should not imply
the same repository machinery for every opaque or inspectable in-process
handle.

Evidence: A1/A1b real cold-replay requirement; direct C6 causal statement;
27-consumer accepted graph; selected mechanics remain implementation choices.

### 7. Version-scope rules need a cumulative compatibility review

The `396144ad` correction should be retained: file co-location is not a
compatibility promise. A complementary check should ask whether independently
valid versions have actual independent consumers and whether their combined
compatibility matrix costs more than it protects.

Evidence: C4 umbrella invalidation was real; accepted A1b now coordinates many
scoped versions; the fixture tests them only one at a time.

### 8. Systemic replanning needs proportional stop and simplification paths

Systemic review should continue to inspect sibling implementations after a
class defect. It should also state when an inventory is sufficient, when a
failure is too low consequence to mechanize, when removal or a smaller
Interface is preferable to adding another registry/check, and when existing
evidence subsumes the new class claim.

Evidence: systemic review caught real A1b defects but repeatedly expanded
catalog, AST, Git, suite-input, and evidence matrices.

### 9. Policy-impact and coverage invalidation need proportionality review

The standards should retain change-specific consumer dispositions and reject
unaudited empty impact. The exact horizon and attestation mechanism should be
reviewed for dependency-local invalidation so a bounded semantic change does
not automatically renew unrelated subjects merely because one global horizon
changed.

Evidence: `1d18b70d` required renewal of all 44 subjects; total relationships
grew 207 to 387; coverage reports distinguish unchanged semantic dispositions
from regenerated identities.

### 10. Retain the recovery rules that have demonstrated unique value

No evidence supports removing Generated Contract routing, external semantic
oracles, equality-domain separation, proof lifetime, conditional Security,
claim-directed Verification, or the prohibition on ambient substitution for a
promised replay contract. Later refinements should add proportionality and
necessity rather than return to A1's weak semantics.

## Implications For A1c Evidence, Not Yet Its Architecture

This history supports process constraints for A1c but does not select its
implementation:

- Preserve A1b's accepted caller-visible and replay guarantees only after each
  guarantee is separated from its current implementation machinery.
- Treat A1b's public four-operation Interface and accepted behavior as the
  primary characterization surface; do not automatically preserve every
  internal codec, record, version, test, or graph node.
- Freeze representative change exercises before design so Locality evidence
  cannot be tailored after the result is known.
- Record which A1b mechanisms are required by an actual consumer, which exist
  to satisfy standards process, which provide diagnosis only, and which are
  artifacts of rejected candidates or current implementation structure.
- Compare a deliberately smaller design against the same cold-replay,
  generated-contract, equality, authorization, and policy-impact claims rather
  than assuming smaller source is simpler.
- Keep the standards change and A1c architecture as separate acceptance
  efforts. Otherwise A1c may merely encode the desired result into the rules
  used to evaluate it, repeating the common-cause problem seen before A1b.

## Unresolved Questions For The Remaining Audit

1. Which exact A1 post-acceptance runtime amendments between `933c9ab9` and
   recovery boundary `c4408363` should be included in the fair A1 architecture
   comparison? Policy-impact v2 changes A1 implementation without reopening its
   accepted product boundary.
2. Which A1b tests have a distinct reachable failure and oracle, and which are
   subsumed by types, construction, public Interface evidence, or another
   verifier? Counts cannot answer this.
3. Which A1b object and version families have actual independent consumers?
   The consumer/state inventory found no external A1 consumer or retained A1
   state, but internal A1b owners may still have legitimate independent change
   promises.
4. What is the smallest implementation that can satisfy A1B-A4/A4C? The
   standards establish the guarantee, not the minimum storage and codec shape.
5. Can coverage requirements invalidate only from changed policy, relationships,
   and consumer authority rather than one provider-wide horizon while retaining
   proof of successful empty impact?
6. Which internal failures can corrupt durable or authorization state before
   detection, and which fail immediately with adequate diagnostic context? This
   is required before proposing validation or test deletion.
7. Did repeated independent review optimize for finding any unproved internal
   state rather than for the smallest complete public claim set? Review reports
   establish findings, not reviewer intent, so this remains unresolved.

## Source Register

The principal immutable sources used by this report are:

- `13a9f48b95ed7532f480e4604d9dfa23443e8f43`: the pre-A1 standards snapshot,
  principally `CORE-STANDARDS.md`, `STANDARDS-ROUTER.md`,
  `topics/{architecture,contracts,security,diagnostics,resilience}.md`,
  `workflows/{planning,implementation,verification}.md`, and
  `evaluation/standards-effectiveness/fixtures/core/simplicity-decisions.tsv`;
- `c7d23dfa55a9558b929e6b838d7ea0563981a1ef`: A1 admission in
  `docs/plans/standards-engine-navigation-analysis/{plan.md,execution-ledger.md}`
  and
  `docs/plans/standards-verification-engine/reports/standards-engine-navigation-analysis-authoring-brief.md`;
- `2359a98740b6035a0414bfaf5427ceaa1301a1c8` and
  `933c9ab93d18ede987d449a6fe7b9ebd313922fc`: accepted A1 implementation and
  `docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`;
- `3439aae9540786d9734431e633ea5b62afb50592`:
  `docs/plans/standards-verification-engine/reports/standards-engine-a1b-redesign-authoring-brief.md`;
- `7a571ed26a132056368ef465d6041910c5a6ed48`: recovery normative rules in
  `STANDARDS-ROUTER.md`, `profiles/boundaries/generated-contract.md`,
  `topics/{architecture,contracts,dependencies}.md`, and
  `workflows/{planning,verification}.md`;
- `0a7fb2dad8160c15051bf9b64e4c25a14091f5c8`: recovery fixtures under
  `evaluation/standards-effectiveness/fixtures/`, the six corresponding
  `evaluation/standards-effectiveness/suites/*.toml` files, prompts, plan
  template, and `evaluation/standards-effectiveness/policy-impact/*.toml`
  projections;
- `9bbc1e050a865131a41559b7b3a7ce96a9fb4f23`: policy-impact authority v2 in
  `tools/standards_policy_impact/`, `tools/standards_analysis/`, and
  `evaluation/standards-effectiveness/{policy-impact,policy-coverage}/`;
- `c4408363752b10060f631247f3e2f1fa26eae003`: recovery completion in
  `docs/plans/standards-engine-standards-recovery/` and A1b planning base;
- `f41037bf71deddba36056b27d418fe767a7cfb62` through
  `36dd75790b2f08a6e66624ccae4f8530bc111a92`: A1b C through corrected-C7
  planning history in `docs/plans/standards-engine-a1b/`, particularly
  [the A1b ledger](../../standards-engine-a1b/execution-ledger.md) and
  [C6/C7 research](../../standards-engine-a1b/reports/c6-c7-design-history-research.md);
- `396144ad9a75c948484d1e564fab73c857bd6f4d`: authority/declaration/version-
  scope rules in `topics/{architecture,contracts}.md`, their fixtures and
  suite, and
  [the impact review](../../contract-authority-scope/reports/authority-scope-impact-review.md);
- `1d18b70d99db48317de2cc9243fc06b133d7329a`: plan-versus-Git-topology
  correction in `workflows/planning.md`, its prompt, template, fixture, suite,
  graph, coverage attestations, and
  [guardrail evidence](../../standards-engine-a1b/reports/serial-plan-commit-boundary-guardrail.md);
- `84412f22fa9fe082f089eaa347c30c23f185ffee` and
  `580d9c959b22f3fdeb0898e7fd4aafd168893580`: accepted A1b implementation and
  `docs/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`.

Every historical standards statement in this report was inspected with
`git show <commit>:<path>` at its effective boundary. Current links aid
navigation but do not replace the cited commit as historical authority.
