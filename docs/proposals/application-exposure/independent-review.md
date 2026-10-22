# Independent application-exposure material review

Reviewed on 2026-10-04 by the separate review agent `exposure_material_review`.
This agent did not author the qualification proposal and has not recorded Engine
review decisions, changed standards, or published application exposure.

## Exact subjects and decision

- Proposal: `proposal:v1:800744d7-33d1-4b31-9a8e-bd66d2c9d3db`.
- Original 32-module revision: `proposal-revision:sha256:15c67a010c50cb271e16abe4dabe2889df266ec9c201d949043af24ff06f4a45`.
- Reviewed 28-module successor: `proposal-revision:sha256:2aa97a0bc3df7967c2d596df8b8b848787641e3a448c076e1dbf4ef109426150`.
- Accepted source: `dcc56f26e884ade260770beceba2501d3746200d`.
- Captured accepted snapshot: `snapshot:v1:5fbd6b92-a9f2-4d5e-bbcb-894f843a6a85`.
- Scope: the 32 unchanged modules listed in the review packet, their required
  guidance, and relevant declared normative consumers. CodeRabbit change drafts
  are excluded. `workflow.standards-authoring` remains authoring-only.

**The 28-module successor is acceptable for application exposure unchanged.**
The reviewer independently confirmed that it qualifies exactly the 28 accepted
targets in the table below while leaving all four Rust targets unreviewed.
All 32 source texts, required dependencies, and specialization lists remain
unchanged. The five required modules outside that 28-target set are unchanged
and report current candidate qualification. No normative correction was included.

The original complete 32-module qualification was not acceptable as submitted.
The Rust base profile needs a narrow evidence-policy correction; the three other
Rust modules remain unqualified until that required base has a coherent reviewed
disposition. This is one substantive blocker with four affected exposure targets,
not four separate normative defects. The successor addresses that exposure
blocker by withholding those targets, rather than waiving or editing their rules.

An acceptable material disposition is not an Engine approval, application preview
result, verification pass, or claim that the module improves downstream behavior.
The accepted successor targets still require the publication workflow's exact
candidate application checks and verification.

## Review evidence and method

The reviewer read each whole proposed module, including applicability, exceptions,
metadata, headings, links, and dependencies, using the captured MCP content in
[accepted-material.json](accepted-material.json) and
[review-packet.md](review-packet.md). Required guidance was compared with Core,
Verification, Implementation, Tooling, Concurrency, and Security. The authoring
workflow supplied the maintenance review standard rather than application policy.

Independent `query_proposal` reads of all 32 targets at the original revision returned
exact text equality with the captured accepted reads. All 32 also preserved their
`requires` and `specializes` lists. Each read reported candidate exposure
`current`; that is the proposed qualification state, not this review's acceptance
or evidence of publication.

The reviewer repeated all 32 exact reads at the successor revision. The 28
accepted targets report `current`; Rust base, Async, API, and Security report
`unreviewed`. Text, `requires`, and `specializes` equality held for all 32.
Separate successor reads confirmed unchanged current qualification for the five
additional required owners: `core`, `workflow.verification`, `workflow.tooling`,
`workflow.implementation`, and `topic.concurrency`. Their dependencies close
within that same set and the accepted targets. Standards Authoring reports
`unreviewed` and remains intentionally excluded.

Nontransitive `policy-impact` queries were inspected for all 32 targets. They
returned 231 declared direct edges, with registered policy-unit mappings for 10
targets and no policy-unit mappings for 22. Nineteen distinct declared normative
consumers were identified. Every such normative consumer was read, including the
five outside the captured material: IPC, Language Bindings, Library, Planning,
and Concurrent Plan Integration. The group forbids transitive traversal, so these
results are explicitly a direct declared inventory, not a claimed exhaustive
transitive semantic closure. Empty results for unregistered modules do not prove
that those modules have no consumers.

The proposal changes qualification rather than source semantics. This review
checked normative coherence; it does not certify the unchanged implementation,
fixture, enforcement-suite, or historical-document projections named by the
impact graph. A subsequent normative correction requires its own owner and
consumer analysis rather than inheriting this exposure-only review.

Captured artifact digests at review:

| Artifact | SHA-256 |
| --- | --- |
| `accepted-material.json` | `7194e856fdec0132e1b445ceca4b5b7b4867d326f05ff666db8875b5b294560b` |
| `review-packet.md` | `6b2b8b51c520ef3380e9972d332ad3c34aefcf0ae8c8ba8d1b82f80d05d5057f` |
| `proposal-result.json` | `e1c40aeb49dafa2ddbfb99e0cfdb2cf4def87c11cdd091c13971c9c805c1acf9` |
| `rust-baseline-correction.md` | `08db5233b372b365ddcff35bf909da4ddcec826bb085f6e4ddefe5b04ec572e9` |

## Blocking finding E1: the Rust baseline overrides evidence sufficiency

**Owner:** `profile.language.rust`, “Baseline Rust Change.”

For a local library bug fix the profile unconditionally instructs the agent:

> Add a focused Rust regression test.

Core's Verification guidance requires a new focused regression test only when
existing evidence does not already prove the property, and explicitly permits an
adequate construction proof or existing test. Verification's “Acceptance Is A Set
Of Claims” likewise permits an existing test or construction guarantee to close
the claim and requires material deciding value before adding permanent evidence
machinery.

The Rust profile says it owns Rust mechanisms while cross-language policy remains
with generic owners. Requiring a new test despite adequate existing evidence is
an additional evidence-policy obligation, not a Rust expression of that existing
policy. The baseline has no `SHOULD`, illustrative-reference status, or explicit
adequate-evidence exception. It can therefore cause an application agent to add
redundant evidence solely because the change is in Rust.

This is a concrete coherence and generality defect in the material selected for
exposure. The finding does not depend on reproducing a CodeRabbit defect or on
disliking language-specific guidance.

**Narrowest acceptable correction:** retain Rust-specific execution and scope
guidance, but make the test step preserve the generic evidence decision. For
example:

> Establish evidence for the changed behavior. Reuse an adequate existing test or
> construction proof; add a focused Rust regression test when existing evidence
> does not already prove the property.

That wording is a suggested correction, not an approved successor revision.
It would change the normative obligation and must pass the Engine's appropriate
owner, coverage, consumer, independent-review, and publication work. The base
profile currently has no registered policy units; exposure approval must not be
used to bypass uncovered-owner authoring requirements.

The instruction to run Clippy is not the same demonstrated conflict. Selecting a
Rust lint adapter with repository-configured warnings is legitimate
language-specific baseline guidance. Core does not explicitly forbid that
supporting gate. Whether it should be a qualified default is a separate
proportionality improvement; this review does not require removing it to resolve
E1.

**Required-dependent dispositions:** `profile.language.rust.async`,
`profile.language.rust.api`, and `profile.language.rust.security` all require the
Rust base. Their own mechanism guidance is acceptable, but their complete reading
path cannot receive an unconditional material acceptance while the base is
withheld. Keep all four outside application exposure until the base correction is
reviewed, or revise this qualification to expose only the other 28 modules.

### Separate review of the proposed correction wording

The reviewer read [rust-baseline-correction.md](rust-baseline-correction.md),
whose proposed replacement is:

> Establish the changed claim with adequate existing evidence or a construction
> guarantee, or add a focused Rust regression test when needed.

This wording correctly restores the generic evidence-sufficiency decision while
retaining the Rust adapter: the evidence or construction guarantee must establish
the changed claim, and a focused test is added when needed for that claim. It
does not weaken acceptance, invent a new principle, require sandboxing, or select
new evidence machinery. Its surrounding proposal preserves the other baseline
steps and does not grant a lint or verification bypass.

This is an independent assessment of proposed text only. It is not an Engine
candidate-read result, semantic revision approval, or application authorization.
The immediate successor leaves the original Rust text intact and unqualified.
Any later normative proposal requires exact candidate review, required owner and
consumer dispositions, and authorization for that source change.

## Per-target material dispositions

“Accept” means acceptable unchanged for the proposed application purpose, subject
to exact application-view and publication checks. “Defer” means withhold the
proposed qualification for this revision.

| Target | Disposition | Material assessment |
| --- | --- | --- |
| `workflow.verification.oracles` | Accept | Independent authority, negative-fixture reachability, and sampled-domain limits are claim-based requirements. It does not select a test library, permanent harness, or sandbox. The documentation consumer preserves the distinction between a changed artifact and adequate proof. |
| `topic.contracts` | Accept | Invariant ownership, boundary decoding, proof lifetime, destination meaning, and evolution are selected from actual authority and consumer facts. Intact in-boundary proof and contained-defect outcomes have explicit exceptions; adapters may specialize diagnostics. The reviewed consumers preserve these authorities. |
| `topic.cross-platform` | Accept | Supported targets and filesystem identity are project facts. Mechanisms and layouts remain contextual; path containment is conditional on untrusted authority. Required real evidence follows the selected support claim. |
| `reference.recipes.tooling` | Accept as optional reference | Metadata and opening text explicitly deny normative authority. Historical tools, products, versions, commands, matrices, and settings illustrate previously selected decisions. Qualification must preserve contextual authority and optional retrieval. |
| `profile.boundary.generated-contract` | Accept | Applicability requires a program-consumed generated contract. Source freshness, semantics, and consuming behavior remain separate claims; Build, Contracts, Dependencies, and Verification retain ownership. It does not infer IPC, persistence, or binding scope from serialization alone. |
| `workflow.verification.platforms` | Accept | Evidence follows each promised target and permits optional/best-effort targets only when the support contract does. Runner, command, matrix, and scheduling mechanisms remain contextual. |
| `topic.resilience` | Accept | Criticality, state authority, degradation, retry safety, and recovery are operation-specific. Unknown mutation outcomes remain distinct from confirmed failure, and disposable reconstruction requires authority. Concrete timing/retry guidance has relevant technical conditions; no universal dependency criticality or retry count is imposed. |
| `topic.diagnostics` | Accept | Diagnostic selection follows an accepted audience and information claim. Diagnostic reporting cannot substitute for owned outcomes, recovery, or lifecycle. Causal identity and products are conditional, and bounded disclosure is preserved. |
| `workflow.documentation` | Accept | Documentation is triggered by durable knowledge that implementation and tests do not sufficiently own. Profiles and placement preserve canonical ownership and permit a no-documentation outcome. Traceability checks retain exact mapped scope and prior-state obligations without a universal `src/` trigger. |
| `workflow.build` | Accept | Build actions identify material inputs, outputs, side effects, invalidation, and access. Determinism is claim-selected. It does not require sandboxing, universal clean builds, or blanket environment clearing. |
| `workflow.commit` | Accept | Staged scope, preservation, authority, integration, and cleanup are explicit. Branches and worktrees are conditional; preservation of commit reachability is tied to cleanup that could remove it. Existing project promises and Core precedence still govern. See optional convention refinement below. |
| `workflow.release` | Accept | Publication, compatibility, artifact identity, versioning, reproducibility, and acceptance are selected from actual consumers and channels. Internal coordinated changes, SemVer adoption, metadata, and ecosystem artifact conventions are distinguished. No universal release provider, matrix, or integrity product is required. |
| `workflow.release.operations` | Accept | Support, channels, presentation, withdrawal, and recovery are contract-owned. Draft states, maintenance branches, support windows, and registry operations are not universal. Immutable published bytes and actual retained consumers remain protected. |
| `topic.performance` | Accept | Optimization and measurements are tied to an owned workload, representative environment, comparison, and tradeoff. No universal profiler, budget, sample count, pooling, or benchmark framework is selected. |
| `topic.contracts.schemas` | Accept | Semantic authority, version roles, invalidation, supported dialect, and reachable generated closure are explicit. External conformance is distinct from local agreement. Its reviewed consumers preserve independent semantic owners rather than granting schema metadata umbrella authority. |
| `topic.contracts.protocols` | Accept | Outcome meaning precedes protocol projection. Producer and consumer proof cover the selected status/body/disclosure contract without universal HTTP mappings, wrappers, or decoder order. |
| `topic.contracts.evolution` | Accept | Compatibility follows actual deployment, persistence, and consumer obligations. Coordinated replacement, supported persisted states, generated derivation, and independently deployed overlap remain distinct. It does not require speculative compatibility. |
| `topic.architecture` | Accept | Ownership and independent change select boundaries and composition. The material-design admission can retain a coherent module or decline machinery. Counts, framework patterns, and repository layout do not decide architecture. Reviewed consumers retain generic authority. |
| `topic.architecture.replay` | Accept | Complete immutable authority is required only by an actual immutable/replay promise. Process-local lifetime, durable cold replay, caches, and current access permission are distinguished. One aggregate can suffice; per-field registries and versions are not mandated. |
| `topic.code-design` | Accept | Coherence, caller knowledge, independent change, current consumers, and domain meaning govern structure. It permits one-call-site boundaries and deliberate non-consolidation. Its architecture and verification consumers preserve those distinctions. |
| `topic.dependencies` | Accept | Selection, ownership, reproducibility, provisioning authority, update, and removal follow actual requirements. Candidate counts and popularity do not decide suitability; existing accepted local implementations have explicit review triggers. Provisioning is owned and independently verifies satisfaction without universal installation commands. |
| `topic.licensing` | Accept | Exact terms and actual use/distribution determine obligations. Legal interpretation is routed to its owner when needed. No guessed license matrix, copied attribution template, or tool product supplies authority. This is a material-policy review, not a legal compatibility opinion. |
| `topic.accessibility` | Accept | Supported users, tasks, modalities, platform capabilities, and selected external obligations define outcomes. Native/custom mechanisms and evidence are selected from that contract. It does not impose a web-only framework, universal modality checklist, or accessibility tool. |
| `profile.boundary.persistence` | Accept | Durable guarantees, source/destination authority, interruption, store capabilities, and supported migration states select mechanisms. It expressly rejects a mandatory phase sequence, universal database, startup migration, or rollback default. |
| `profile.application.frontend` | Accept | UI projection, state, synchronization, lifecycle, interactions, and real-browser claims retain their respective owners. Framework, resource holder, selectors, and evidence fidelity remain contextual. Conditional Contracts specialization is explicit. |
| `profile.language.rust` | Defer: E1 | The unconditional new-test step contradicts generic adequate-evidence sufficiency. Other language mechanisms do not resolve that conflict. Correct and review the base before exposure. |
| `profile.language.rust.async` | Defer: required base | Own guidance is coherent: suspension, runtime composition, task completion, cancellation, bounded blocking isolation, guards, and durable effects preserve generic contracts without selecting a universal runtime. Requires the base withheld by E1. |
| `profile.language.rust.api` | Defer: required base | Own guidance correctly expresses accepted generic contracts through types, conversions, traits, parameters, features, visibility, outcomes, and Rustdoc. It avoids universal derives and wrapper shapes. Requires the base withheld by E1. |
| `profile.language.rust.security` | Defer: required base | Own guidance preserves filesystem authority through use, recoverable outcomes, checked numeric domains, limits, queue ownership, and listener lifecycle. Equivalent supported mechanisms remain possible. Requires the base withheld by E1. |
| `profile.language.typescript` | Accept | Public type expression follows consumer contracts; static types do not prove runtime validity. Generation, domain distinctions, and lint scope retain generic owners. `strict` is explicitly SHOULD guidance with staged adoption and justified overrides. |
| `profile.language.typescript.async` | Accept | Current-invocation authority and all terminal outcomes are required only where operations overlap or own lifecycle obligations. Several scoped mechanisms are permitted; an uncancellable operation can remain observed without applying stale results. |
| `workflow.verification.gui` | Accept | Startup qualification uses only material environment facts. CI display, sandbox flags, graphics workarounds, wrappers, and limits are conditional on the selected environment; normal interactive behavior must not be weakened. See optional ambiguity refinement below. |

## Optional improvements and retained concerns

These do not independently block the 28 accepted targets and are not authorization
to change source in the qualification proposal.

1. **Inherited fixture serialization restriction.** Concurrency permits explicit
   coordination but requires the reason independent ownership cannot be
   established before allowing serialization. That narrows otherwise adequate
   coordination choices and deserves the previously recommended generality
   review. Concurrency is unchanged required guidance rather than one of the 32
   newly qualified owners. This review does not certify that restriction as an
   optimal principle or require project sandboxing to satisfy it.
2. **Rust and library evidence-policy family.** The unqualified Library consumer
   says local deterministic behavior requires focused regression tests. A future
   correction should bound consumers that actually project evidence sufficiency,
   so fixing only the Rust wording does not create competing policy. Library is
   outside this exposure proposal and remains unreviewed; this finding does not
   silently qualify it or claim its whole required closure has passed.
3. **Commit format default.** The unconditional conventional-commit language
   would be clearer as a project-selected format or a justified default when no
   format is established. Core already gives governing project contracts
   precedence. There is no demonstrated active consumer conflict in this
   exposure-only candidate; avoid treating the style refinement as a new safety
   obligation or as permission to rewrite history.
4. **GUI environment wording.** “Do not silently ... inherit an operator desktop
   session” is properly read as prohibiting undeclared ambient dependence, in
   light of the surrounding material-facts qualification. An explicitly selected
   representative or required-real desktop session can be appropriate. Make that
   condition clearer in a future wording pass so agents do not infer mandatory
   private desktop sessions, containers, or operating-system sandboxes.
5. **Scope lists as conditional dimensions.** Long normative lists in Contracts,
   Architecture, Accessibility, and the language profiles describe applicable
   facts or allowed mechanisms, generally with explicit conditions. Preserve
   those conditions if later editing or projection shortens the material. Their
   length alone is not evidence that a rule is unnecessary or an example has
   acquired authority.

## Authority, consumer, and isolation conclusions

The 28 accepted modules provide technical conditions, preserved properties,
failure/lifecycle meaning, and acceptance criteria with sufficient context for
an application agent to select mechanisms. Conditional refinements and language
adapters do not become universal requirements merely through exposure.

The optional Tooling recipe retains reference/contextual authority. Historical
GitHub Actions, Prettier, ESLint, EditorConfig, Node, and Lefthook examples are
adapted after canonical decisions; they do not replace those decisions or need
to enter routine normative reads. Application preview must confirm this
separation and preserve qualified required dependencies.

There is no general requirement for a project to sandbox itself. Verification
fixture isolation is an ownership and coordination property. Build controls
material inputs and access for its claim. GUI sandbox settings are recorded only
when applicable. Security's untrusted-execution detail is selected for
less-trusted or delegated authority or an actual isolation promise; trusted
subprocess use alone does not select it, and the detail disclaims a required
sandbox product or permanent harness.

The extra normative consumers read through the graph do not expand this
proposal's qualification scope. IPC, Language Bindings, Library, and Concurrent
Plan Integration report unreviewed candidate exposure and must remain outside
readiness claims. Planning reports current exposure. A conditional link to one
of those modules is not an unconditional prerequisite and does not imply its
qualification was reviewed here.

## Publication and review limits

- Do not approve the original 32-module revision from this record. Its material
  blocker remains documented. The exact 28-module successor named above has
  independently verified scope and unchanged material; this record supports
  its 28 exposure dispositions when bound through the Engine's review workflow.
  It does not support qualifying the four excluded Rust modules.
- A normative Rust correction is separate material work, with explicit semantic
  and consumer dispositions and a fresh independent exact-revision review.
- Keep the authoring workflow authoring-only. Its applicability explicitly
  excludes projects merely applying the library.
- Source text is accepted snapshot content, not the dirty live worktree.
  Existing unpublished user work and exposure edits remain outside this record's
  mutation authority.
- Application read/route/relationship filtering, complete required qualification,
  repository verification, Engine review readiness, application, and accepted
  readback remain publication-owner work. Candidate authoring reads cannot stand
  in for those results.
- No live CodeRabbit defect was reproduced. No effectiveness experiment,
  platform runtime check, legal interpretation, or downstream deployment was
  performed. The evidence establishes material review and exact candidate text
  preservation within the stated scope.
