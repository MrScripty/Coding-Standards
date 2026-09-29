# Source consumers and version boundaries

All inspected references below use source `149ba317e9397519bc181a048ecf76aef129a69c`.
Rows are the admitted owner families, not permission for unrelated cleanup. At each
slice, enumerate actual symbol callers and tests before editing; extend this list
only for a demonstrated direct consumer. Shared contracts/generator inputs have one
serial integrator. Code review is [here](code-review.md).

| Owner | File | Current section | Planned disposition |
| --- | --- | --- | --- |
| Repository observation/publication | `tools/repository_git/repository_git/repository.py` | 631–692; existing index/command helpers | Observe exact target/worktree/index; new guarded local reconciliation primitive. Preserve isolated candidate and expected-target ref writes. |
| Git tests | `tools/repository_git/tests/test_repository.py` | publication/index, separate-layout cases | Keep existing preservation oracles; add two-tree/conflict/stale/partial-effect matrix without altering user Git config. |
| Engine application | `tools/standards_engine/standards_engine/engine.py` | 1252–1810 | Shared pure evidence preparation, rich publication view, explicit reconciliation coordination and final live checks. |
| Evidence resolution | `tools/standards_engine/standards_engine/tools.py` | 54–106; facade operation adapters | Separate resolver from permission policy; expose bounded new generated operations and references. No imports from Engine back into facade. |
| Trust values | `tools/standards_analysis/standards_analysis/trust.py` | EvidenceReference/ResolvedEvidence; authorization records | Keep exact digest/subject/capability validation; add safe context at owning resolution boundary, not global data echoes. |
| Error owner | `tools/standards_analysis/standards_analysis/errors.py` | AnalysisFailure | Extend only demonstrated diagnostic needs and preserve typed outcome/codes. |
| Portable coverage | `tools/standards_analysis/standards_analysis/coverage_publication.py` | 124–178,202–223,226+ | Keep current v1 destination semantics and cold read; share pure preflight and validate new exported bundles as existing repository artifacts. |
| Coverage parser | `tools/standards_analysis/standards_analysis/coverage.py` | 1068–1160 | Existing repository-content@1 rule constrains any extension; no broad provider relaxation. |
| Immutable authoring | `tools/standards_engine/standards_engine/authoring.py` | review_proposal/application/readiness records | Retain old identities. Introduce separate capture/reconciliation record kind only if necessary, not new meaning for old readiness. |
| Workflow composition | `tools/standards_engine/standards_engine/agent_workflow.py` | 105–178,219–326 | Publication facts visible on status; pass selected prior Analysis on revise; no final approval carryover. |
| Operation-local material | `tools/standards_engine/standards_engine/operation_materials.py` | ProposalMaterials | Reuse exact materials where legal without retaining current permissions or recovery authority. |
| Workflow display | `tools/standards_engine/standards_engine/workflow_presentation.py` | summarize/pending_work | Concise receipt/decision summary, precise safe continuations and bounded full detail. |
| Purpose qualification | `tools/standards_engine/standards_engine/context_projection.py` | 110–126,250–268 | Structured internal blockers; authorized candidate explanation versus application-safe rejection. |
| Logical/candidate assembly | `tools/standards_engine/standards_engine/logical_authoring.py` | projection topology and generated artifacts | Only explicitly selected captured evidence joins candidate files; exact topology/content and final manifest remain owned here/Engine. |
| Existing capture pattern | `tools/standards_engine/standards_engine/consumer_authoring.py` | bind_sources/captured_sources | Reference ownership precedent only; do not make consumer registration a generic evidence resolver. |
| New bound material owner | `tools/standards_engine/standards_engine/evidence_bindings.py` | new, A2 | Narrow acquisition, canonical bundle, lifecycle/export and origin inspection. No generic plugin registry. |
| Transport/canonical contracts | `tools/standards_engine/contracts/a1-contract.schema.json` | EvidenceReference, Apply/Recover/Workflow/Preview and proposed new calls | Keep current four-field evidence carrier; introduce bounded explicit public result/action variants at current schema owner. |
| Interface/generation | `tools/standards_engine/contracts/a1-interface.toml` | interface 45, request6/result7 | Allocate next actual release edition; regenerate _generated_contract.py and generated/agent-tools.json atomically. |
| Publication and evidence tests | `tools/standards_engine/tests/test_coverage_publication.py` | entire existing integration | Retain late evidence tampering and cold-clone verification; add changed-candidate evidence pre-readiness path. |
| Recovery tests | `tools/standards_engine/tests/test_publication_recovery.py` | entire existing fault fixture | Preserve never-republish-after-applied, selected application and current target checks. |
| Decision/purpose tests | `tools/standards_engine/tests/test_agent_workflow.py` | focused revision/status | Test intended source of prior Analysis and final-review separation. |
| New evidence/reconcile cases | `tools/standards_engine/tests/test_authoring_evidence_bindings.py` | new, A2 | Real capture/resolver/export/legacy/cold receipt and no-authority from evidence presence. |
| New reconciliation cases | `tools/standards_engine/tests/test_checkout_reconciliation.py` | new, A3 | Exact bytes/staging and interruption behavior in disposable Git/SQLite processes. |
| Existing baseline fixture | `tools/standards_engine/tests/test_supporting_workflow.py` | 78–86 and setup | Replace real topic.security assumption with test-owned exposure; direct wrapper in test_process_reuse.py stays coherent. |
| Authoring instructions | `.agents/skills/standards-engine/references/authoring.md` | publication/evidence task flow | Explain applied-versus-checkout, explicit binding/export, fresh final review, recovery versus reconciliation. |
| Entry guidance | `.agents/skills/standards-engine/SKILL.md` | result states and exact handles | Coordinate small current task examples; avoid repeating normative rules or restoring eager schemas. |
| Public docs | `tools/standards_engine/PURPOSE-SEPARATION.md` | authoring and retained contracts | Record authorized diagnostic split, actual version cutover and supported local mutation threat model. |
| Verification inputs | `evaluation/standards-effectiveness/generated/suite-inputs.json` | producer generated | Refresh only through the existing owner when implementation changes captured inputs. |

## Version/persistence facts

EvidenceReference currently has exactly id/digest/provider_contract/provider_contract_version.
Local facade resolution is working-tree repository-content@1; coverage publication
and published receipt replay independently demand destination bytes. Proposal
readiness schema1 and application schema1 are retained records, not display DTOs.
Authoring contract2 and request contract6 are retained. Result projection7 remains
the request side of the current protocol; this release adds result projection8.
Public interface46 is the reviewed candidate edition; installed interface45 clients
must reconnect and reload the interface46 schema after deployment. There is no
interface45 output compatibility mode. In-repository generated contracts, examples,
tests, and configured harnesses are updated together. The running MCP instance
remains on interface45 because it is bound to the separately dirty main checkout;
it was not restarted or served A1 source. Application/readiness persistence schemas
are unchanged and the cold status read remains covered.

Bound bundles deliberately add independent material rather than change old reference
meaning. New aggregate kinds must explicitly declare identity, retention, root
dependencies and failure cleanup. Reconciliation observations are transient unless
a durable intent is required for partial-effect recovery; that intent does not
become a second publication record. Existing coverage v1 loader support remains.

## Delivery consumers

Reconcile installed authoring registrations and existing native/agent test harnesses
with each actual new interface edition. No provider networking or registration
change is part of this planning task. Keep application-purpose catalogs restricted.
A new action may require a specifically authorized capability; availability does
not imply the user authorized a checkout mutation or exporting imported evidence.

Generated examples in contracts/examples/a1-examples.json, contract/schema tests,
request-evidence normalization, mcp_catalog descriptions, operation inventory, CLI
reference invocation and configured Codex qualification harnesses are direct
consumers of public additions. Do not broaden all of them unless the selected
slice actually changes their inputs or outputs. Historic traces retain their original
source/catalog and verdict; no backdated migration is performed.
