# R2 connected-agent qualification

**State (2026-09-28): incomplete.** The connected authoring-purpose Codex tool catalog still presents interface 44. A direct `runtime_info` call returned instance `acd7ec54-b009-41a3-a5ee-62b2110681a9`, interface `44`, catalog digest `sha256:feedb6e08686a2b2036548c41c05459a7e72c4fd9d2cd217ecc22bf18b6c3d17`, `installation_state: restart-required` and `action: restart-and-reconnect`. The saved registration selects the repository source, purpose `authoring`, and `--output-schemas on-demand`; it has no new routing flag. No store, handle or registration argument was changed.

Through that same connected tool, `routing_facts` returned a real snapshot handle and eight registered enum-set categories. For the representative review/qualification task, known facts were activities `verification, documentation`, boundaries `generated-contract, ipc`, topics `contracts, diagnostics, performance`, and details `topic.contracts.schemas, workflow.verification.oracles`. Other categories remained omitted and unknown. The baseline envelope request was 563 JSON bytes including the returned snapshot and `content.limit=2`. The old process returned the transport error `Engine invocation failed; inspect server stderr` for `route`, so it supplied no valid baseline route or continuation. This failure is not evidence about the interface-45 process. No application or standards mutation occurred.

The candidate connection has not yet been refreshed in this agent session. Interface-45 construction, refinement, continuations and mistake feedback through this connected tool remain unobserved, so R-A7 is still open. The separate paired model comparison below does not replace that connected-agent check. Keep the plan `Verifying` until the actual catalog reports 45 and the live workflow is observed. Existing automated disposable-fixture coverage of boolean, nullable and alias cases remains separate from the production vocabulary, which has none of those definitions.

## Paired fresh-model comparison (separate from the connected-session gate)

Two disposable clean checkouts used the same `gpt-6-sol` prompt and authoring/on-demand registration: baseline `ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76` (interface 44) and candidate `39d44f007c36684e1ebc546f31a19e20e2e660e5` (interface 45). The model routed a new internal library feature for implementation, verification and documentation, explicitly no application forms, with representation boundaries initially unresolved. It then learned the IPC and generated-contract boundaries, refined against the original snapshot, and followed one returned content page and the full explanation. All four route calls per side succeeded without input repair. The initial candidate explicitly supplied `routing.boundaries: {"state":"unknown"}`; the baseline omitted that still-unknown category. Both preserved other unanswered categories. The candidate's later calls used the returned compact facts directly.

| Observation | Baseline 44 | Candidate 45 |
| --- | ---: | ---: |
| Construction errors from MCP calls | 0 | 0 |
| Route repair calls | 0 | 0 |
| `routing_facts` vocabulary calls | 1 | 1 |
| `describe_input` calls | 2 | 0 |
| Initial route request JSON bytes | 331 | 284 |
| Refined route request JSON bytes | 425 | 293 |
| Returned content-page request JSON bytes | 436 | 304 |
| Returned full-explanation request JSON bytes | 419 | 287 |
| First content page reads | 2 | 2 |
| Additional content page reads | 1 | 1 |

The two first-page reads reflect the initial and then refined routes, not an accidental identical retry. Request lengths use compact UTF-8 JSON serialization of the model's tool arguments; they are not model-token or billing measurements. Both agents retained five unanswered questions after refinement. One baseline follow-up was denied by the nested client's default approval setting before any Engine invocation; one candidate follow-up started without its disposable MCP registration. Those harness setup failures were corrected with explicit registration and automatic review, and are excluded from construction-error and repair-call counts. They do not replace the required check through this session's real connected tool catalog.
