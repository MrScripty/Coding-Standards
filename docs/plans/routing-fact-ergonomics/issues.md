# Routing-Fact Ergonomics — Findings and Dispositions

These are this new plan's observations. Earlier accepted review findings and
verdicts are not edited, reclassified or converted into prerequisites here.

| ID | Severity / evidence | Owner and boundary | Disposition | Verification / revisit trigger |
| --- | --- | --- | --- | --- |
| RF-01 | Design-critical: omitting a repeated type makes type-dependent validity snapshot-dependent. The prototype's 126 cases include 41 static-stage differences with identical final validity. | Engine focused input projection; applicability semantic binder; purpose error mapping | Fix in R1: bind using the selected schema before construction/evaluation, keep safe invalid feedback and avoid uncaught canonical decoding errors. | Wrong scalar/set/null values through actual facade and cold MCP; no internal error or invalid success. |
| RF-02 | Design-critical: `explanation` and both routed-content `next` objects use `RouteCall`; copying the old typed facts produces an invalid new continuation. | Focused result/continuation producer | Fix in R1 as one bidirectional projection from the canonical bound fact set. | Every returned continuation validates and executes under the new schema in a replacement process; same authority, selected content and questions. |
| RF-03 | Design-critical: canonical `FactSet` is also used by native query/preview and Analysis. A global replacement would widen scope or mutate stored meaning. | Applicability / native Engine / persistence | Preserve canonical definitions and native contracts; change focused RouteCall and focused fact echoes only. | Old producers/new consumers, exact canonical schemas, paired native/focused cases and retained-state tests. |
| RF-04 | Integration assumption: actual downstream consumers of saved focused requests may require a separate rollout. Only repository consumers and the known native/on-demand deployment were inspected. | Integration owner | Confirm actual supported consumers before cutover; do not invent hypothetical indefinite support or silently overwrite saved requests. | Re-plan for a real independently deployed overlap requirement; refresh changed catalog bindings while retaining snapshot/workflow data. |
| RF-05 | Environment: no actual client/model has observed the proposed union; local Python 3.13.5 probe is not locked 3.12 candidate CI. | Host/verification owner | Required R-A6/R-A7 evidence, not a passed claim. Keep unrelated canonical design work bounded. | First real schema/discovery observation can change the wire design; candidate qualification must use the actual deployed surface. |
| RF-06 | Scope: three state buckets or a raw-only shorthand would add duplicate-state conflict machinery or lose explicit absence/unknown semantics. | Public contract owner | Declined alternatives; select one facts map with a disjoint marker form. | Revisit only if real consumers show the selected shape cannot express their current fact domain. |
| RF-07 | Future-type assumption: supported fact types currently have no arbitrary object or numeric value. | Applicability + focused contract owner | No new types admitted. Marker-object disjointness is explicit, not an open-ended guarantee. | Re-plan grammar on an actual new fact type. |
| RF-08 | Sequencing: prior external review packets lacked some CI/delivery/baseline evidence, but the six-slice sequence is Accepted. | Future packet-generator owner, not routing implementation | Defer to user's priority 4. Preserve existing source/CI/review/owner separation; no external transmission or automatic verdict here. | Admit after routing ergonomics' normal completion, using its real evidence needs. |
| RF-09 | Test debt from earlier review is accepted as non-blocking and belongs to priority 3. | Future test-strengthening owner | Defer broad unrelated repairs. Add only tests needed by the routing change now. | Separate evidence-based admission after review-packet work. |

No demonstrated production defect is claimed by this planning artifact. RF-01–03
are foreseeable failure classes in a proposed contract change, not evidence that
the accepted baseline mishandles the existing contract.

## RF-10 — Normalization-induced assertion collision

A real counterexample uses a string-set containing `e\u0301` and `é`: raw uniqueItems
passes, but the unchanged canonical binder normalizes both entries to `é`. A focused
result or continuation cannot serialize that duplicate array under its declared
uniqueItems contract. This would otherwise escape during result validation. The
canonical binder/native query semantics are deliberately unchanged. R1 checks the
reverse-projected assertions with the existing generated validator before selection
and returns bounded field feedback at that focused boundary. This is an additional
validation of the owned wire projection, not a new semantic binder or registry.
Tests cover the generated static acceptance, canonical native observation, focused
invalid result, normalization repair and actual cold stdio in both purposes.


## Implementation disposition

RF-01–RF-03 are implemented and locally verified; RF-10 is covered by typed feedback,
literal canonical observations, repair cases and actual cold stdio. RF-04/RF-05 remain
explicit integration/host requirements, not reasons to retain an old focused parser.
RF-06/RF-07 remain the admitted grammar boundaries. RF-08/RF-09 remain deferred to
the user's later priorities. R1 admits no additional product or general test slice.
RF-11: the full selection found two directly affected current-version assertions
in test_schema_presentation and test_capture_handoff_transport that still expected
44. Their fixed expectations preserve the existing store-free identity and capture
proof assertions. Both are included in the final affected rerun. No runtime code
was changed to satisfy these tests.
The supported locked environment and actual live model have not been run here;
independent review and acceptance remain with their identified owners.
