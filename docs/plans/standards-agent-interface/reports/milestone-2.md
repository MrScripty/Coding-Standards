# Milestone 2: Fact Discovery And Routing Explanations

`routing_facts` now returns the snapshot-bound registered fact vocabulary without
Router content or editable rules. Focused `route` returns canonicalized supplied
facts, actual selected/unresolved rule expressions, existing graph/selection
causes, and questions carrying their exact fact definitions. Native `query`
retains its route-result shape.

The Engine projects explanation data from the existing evaluation pass. There
is no second evaluator and no interpretation of natural-language intent. Fact
projection is shared with the existing Router authoring read.

## Evidence

- All 32 focused navigation, generated-contract, and MCP tests pass on Python
  3.12 with the repository's locked dependencies.
- Vocabulary matches existing Router output. Native and focused selection and
  dependency closure agree for the reviewed Rust implementation scenario.
- Domain fixture tests cover Boolean, nullable string, enum-set, alias
  normalization/conflict, explicit negatives, invalid/unknown facts, and
  several simultaneous rule causes targeting the same standard.
- The official MCP SDK 1.29.1 stdio client discovers 23 tools and successfully
  retrieves vocabulary, routes known facts, inspects explanations, and retains
  unresolved questions. Compact-read and interleaved-snapshot checks still pass.
- Generated projection checks, focused lint, skill validation, and the Engine
  checkpoint pass (73 suites / 121 checks).

The added `RoutingQuestion` avoids presenting an enumeration-only answer list
as the universal answer shape. The fact definition plus the generated route
input schema describes the actual answer type and nullability.

A3 is satisfied. A7 has real-client navigation/routing evidence; its
proposal/application/recovery scenarios remain assigned to Milestone 3.
