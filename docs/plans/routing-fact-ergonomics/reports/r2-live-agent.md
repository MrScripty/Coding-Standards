# R2 connected-agent qualification

**State (2026-09-28): completed after session restart.** The connected authoring-purpose Codex catalog and `runtime_info` both report interface **45**. The live instance is `7b218cb0-a70a-4325-934c-743b3f312e96`, catalog digest `sha256:8235cb21f7d1937be1a003eb2eef570345242194dac36d79463b16e26bb6d65d`, `installation_state: current`, `action: reuse`. The saved registration still selects the repository source, purpose `authoring`, and `--output-schemas on-demand`; it has no new routing flag. No store, handle or registration argument was changed.

## Initial stale connection (historical observation)

Before restart, the connected catalog still presented interface 44. `runtime_info` returned instance `acd7ec54-b009-41a3-a5ee-62b2110681a9`, catalog digest `sha256:feedb6e08686a2b2036548c41c05459a7e72c4fd9d2cd217ecc22bf18b6c3d17`, `installation_state: restart-required` and `action: restart-and-reconnect`.

Through that same connected tool, `routing_facts` returned a real snapshot handle and eight registered enum-set categories. For the representative review/qualification task, known facts were activities `verification, documentation`, boundaries `generated-contract, ipc`, topics `contracts, diagnostics, performance`, and details `topic.contracts.schemas, workflow.verification.oracles`. Other categories remained omitted and unknown. The baseline envelope request was 563 JSON bytes including the returned snapshot and `content.limit=2`. The old process returned the transport error `Engine invocation failed; inspect server stderr` for `route`, so it supplied no valid baseline route or continuation. This failure is not evidence about the interface-45 process. No application or standards mutation occurred.

The paired model comparison below is separate from the connected-session result.

## Actual connected interface-45 navigation and mistakes

`routing_facts` returned snapshot `snapshot:v1:00d9a08b-4d75-4266-a00c-e172d95df3c1` and eight enum-set definitions. The agent supplied known verification, documentation and commit activities, library application form, contracts/diagnostics/performance topics, and schema/oracle details directly. It left boundaries, frameworks, languages and workflow profile unanswered. The first compact route succeeded with 12 reading entries and four unresolved questions; no `describe_input` call was needed. The boundary question was then answered with `generated-contract` and `ipc` against the **same snapshot**. The refined route succeeded with 18 reading entries; frameworks, languages and workflow profile remained unanswered rather than becoming empty or absent.

The returned `content.next` request and the returned full `explanation` request were each passed directly to `route` without rebuilding their facts. Both succeeded, retained the same snapshot and compact fact values, and retained the three unanswered questions. The content page returned one exact item at offset one and a further continuation. A separate explicit-unknown enum-set assertion returned `{"state":"unknown"}` in the echo and kept that fact unanswered. A justified known-empty framework set returned `[]` and removed that question. These separate probes did not alter the main refinement's unknown facts.

| Live mistake | Result |
| --- | --- |
| String supplied for enum-set `routing.activities` | `ROUTE.INPUT_INVALID`, exact `/facts/routing.activities`, useful unique-string-set feedback. |
| Undeclared fact name | `ROUTE.INPUT_INVALID`, non-exact `/facts` pointer without echoing the caller's key. |
| Old `{type,state,value}` envelope | `INTERFACE.INVALID_ARGUMENTS`, bounded `/facts/*` `oneOf` feedback and `describe_input(route)` hint. |

All three were typed invalid outcomes (`isError: true`), not internal transport errors or successful routes. There were no route construction errors, repair calls or extra discovery calls in the successful connected workflow. The production registry has **no aliases, boolean facts or nullable facts**. Alias-collision, false, null and known-absence semantics therefore use the existing disposable-fixture tests in the supported 608/571-test CI, rather than inventing unsupported production facts or mutating standards. The live explicit-unknown and known-empty checks use actual enum-set definitions. No proposal, publication or production standards edit was made.

## Paired fresh-model comparison (separate from the connected-session result)

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
