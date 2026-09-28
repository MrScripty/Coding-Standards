## Source-review recommendation for R-A8

**Recommendation:** source portion of R-A8 can proceed to owner disposition with **no blocking source defect found** in inspected areas; **do not close R-A8** until locked-CI (R-A1/R-A2/R-A6) and live-agent (R-A7) evidence are observed. This is a source inspection only; I claim neither CI status nor live-agent behavior.

## Areas inspected

- `docs/plans/routing-fact-ergonomics/plan.md`, `issues.md`, `reports/verification.md`, `reports/source-consumers.md`, `tests/ROUTING-FACT-QUALIFICATION.md`
- `review-packet/routing-implementation.patch` (head hunks; full generated `_generated_contract.py` blobs truncated by size)
- `tools/standards_engine/standards_engine/routing_inputs.py:1-75`, `agent_navigation.py:21-118,204-272`, `context_projection.py:227-247,271-341`, `engine.py:2791-2897,3447-3479`, `input_feedback.py:14-39`
- `tools/standards_applicability/standards_applicability/core.py:216-236,534-567`
- `tools/standards_contracts/standards_contracts/validation_feedback.py:25-75`
- Contract: `RouteCall`, `RoutingFactAssertion(s)`, `CompactRouteResult.explanation:RouteCall`, `RoutedContentPage.next:RouteCall`, `ApplicationRoutedContentPage.next:RouteCall`
- Tests: `test_routing_fact_inputs.py`, `test_routing_fact_transport.py`, `test_compact_routing.py`, `test_route_content.py`, `test_agent_navigation.py` (focused portions), `codex_navigation_client.py` (head)

## Findings

1. **Advisory — caller `type` wins in unvalidated direct call** — `routing_inputs.py:31`, patch hunk `routing_inputs.py/bind_facts`
   - `{"type": definition.type, **value}` lets a `Mapping` value containing `type` overwrite the declared type, contrary to D2 "infer only declared type."
   - Affected: R-A2/R-A3 invariant. Reachable only by bypassing generated `RouteCall` validation (e.g. direct `bind_facts` with old `{type,state,value}` envelope); unreachable via facade because static schema forbids extra object props and old envelopes are rejected (`test_static_grammar_rejects_old_envelopes...`).
   - Even then `_bind_value` still rejects mismatched type, so no invalid success. **Not blocking.** Suggest `{**value, "type": definition.type}` for defense in depth.

2. **Advisory — `ContractError` from result construction is outside `_domain_errors`** — `agent_navigation.py:51-62`, `engine.py:3447-3458`
   - Inner `except (ApplicabilityError, ContractError)` covers only `bind_facts`; outer covers `_domain_errors()` which excludes `ContractError`. A `Compact/AgentRouteResult.from_value` failure would escape `navigate`.
   - Affected: R-A3/R-A4 "no uncaught ContractError/internal error." Reachable trigger: none found — `bind_facts:37` pre-validates `fact_assertions(bound)` with the same generated `RoutingFactAssertions` grammar before selection/construction, and tests cover the known RF-10 trigger. **Not blocking.** Owner may add an assertion or narrow catch as hardening.

3. **Satisfied — snapshot binding and qualification order** — `agent_navigation.py:52-58`, `context_projection.py:332-339`
   - Authoring loads/verifies selected snapshot via `_compiled_snapshot` then `bind_facts` on `compiled.router.fact_schema`; application calls `view._require("router")` before `bind_facts`, with full-closure qualification in `_route_bound`. `test_qualification_precedes_vocabulary_interpretation` patches `bind_facts` to prove no vocabulary read on unqualified content. Supports R-A4.

4. **Satisfied — type/state distinctions** — `core.py:534-567`, `routing_inputs.py:41-45`
   - Omitted (absent from `FactSet`), `false`, `[]`, nullable `null` (`exists=true`), `known-absent` (`exists=false`), `unknown` remain distinct; `"unknown"` string stays a known string. Literal `exists`/`Truth` oracles in `test_literal_state_and_exists_semantics`. Supports R-A2.

5. **Satisfied — aliases and normalization** — `core.py:219-236`, `routing_inputs.py:28-38`
   - Supplied names preserved through `require` + `bind`; alias+canonical duplicate errors even when values agree; NFC + sorted sets owned by binder; RF-10 reverse-projection `decode_contract` returns typed invalid without changing native duplicate-tuple semantics (`test_normalized_set_collisions...`, `test_unicode_collision...`). Supports R-A2/R-A3/R-A5.

6. **Satisfied — invalid feedback and privacy** — `routing_inputs.py:48-75`, `input_feedback.py:22-39`
   - Single bounded `InputIssue`, exactness only for unique registered name, `~`/`/` escaping, `MAX_POINTER_CHARS` fallback to `/facts`, fixed constraint prose, `describe_input:{route}`, `ROUTE.INPUT_INVALID` vs `APPLICATION.INPUT_INVALID` adaptation. Unknown keys/values not echoed; multi-error ordering (resolution before value pass) explicitly tested. Supports R-A3. Both purposes covered via facade and cold stdio.

7. **Satisfied — continuations and full explanation roundtrip** — `agent_navigation.py:88-118,232-239`, `with_route_content:215,232-239`
   - One `fact_assertions` projection feeds authoring echo, `explanation.facts` (compact), and both purposes' `content.next.facts` with canonical IDs, normalized values, same snapshot/detail/limit/offset; `next`/`explanation` are `RouteCall` refs so validate under the new contract. Cold-process equality, `Detail` preservation, no-extra-capture/compile, and final-lifecycle discard covered. Supports R-A4.

8. **Satisfied — no new authority, migration, or redundant binder** — `core.py:219-224`, `engine.py:2801-2808`
   - `FactSchema.require` only factors existing lookup/error; single `schema.bind` per focused call (asserted `call_count==1`); shared `_bound_routing_selection` keeps rule/dependency/ordering/digest guard; native `RouteRequest`/`FactSet`/`FactValue`, previews, Analysis, handles, request-6/result-7 unchanged. Supports R-A5, plan D5.

9. **Satisfied — contract/guidance coordination (inspected subset)** — schema `RouteCall.facts`, `Compact/AgentRouteResult.facts` → `RoutingFactAssertions`; interface 45; `describe_input` closure contains only new shape and `FactValue`/`FactSet` absent (`test_input_discovery...`); `PURPOSE-SEPARATION.md`, `README.md`, qualification guide updated.
   - I did not inspect `mcp_catalog.py` route prose or `.agents/skills/standards-engine/*` content in this pass — see gaps. Supports R-A1/R-A6 subject to CI freshness checks.

10. **Satisfied — test independence (inspected tests)** — differential compares final validity plus canonical `as_contract()` equality, with independent literal `exists`/truth/unknown, exact codes/fields, distinct durable-snapshot vocabularies (not ambient files), negatives (old envelopes, numbers, arbitrary objects, wrong scalar/set, unknown IDs, duplicates, empty-string-in-set, extra marker fields), and cold-stdio both-purposes checks. The `successes==33` count and differential's parallel typed completion are brittle if read alone, but literal/boundary tests break the circularity. Supports R-A2/R-A3.

## Evidence gaps

- Full patch tail beyond the read window; full `_generated_contract.py` diff (size-truncated); `ContractError`/`ContractFailure.instance_pointer` definition (relied on via passing RF-10 tests, not direct read).
- `mcp.py` transport mapping for hypothetically escaped errors; `mcp_catalog.py` and skill-guidance wording; DELIVERY/evidence artifacts and any CI logs.
- Locked-runtime CI and actual host/model comparison were explicitly out of source inspection; verification report correctly leaves R-A1/R-A2/R-A6 (CI) and R-A7/R-A8 (host/owner) pending.

## R-A disposition from source review

- R-A3/R-A4/R-A5: source behavior inspected supports the claimed satisfied status, subject to owner confirmation; no source blocker found.
- R-A1/R-A2/R-A6: source shape supports the claims but require locked-CI proof; not granted by inspection.
- R-A7: requires live-agent evidence; not granted.
- R-A8: recommend owner accept the source portion with the two advisories above, and hold final R-A8 until R2 integration evidence arrives.
