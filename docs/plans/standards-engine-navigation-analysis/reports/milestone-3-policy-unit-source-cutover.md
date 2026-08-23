# Milestone 3 Policy-Unit Source Cutover

## Accepted Authority

Policy-unit sidecars own identity, module-relative locators, lifecycle, and
semantic revisions. `standards_metadata` loads and validates those sidecars
with canonical module metadata as one immutable snapshot-bound corpus. It does
not own the authored facts.

Module-owned policy-impact files remain relationship authority, but each
relationship now originates from one exact active policy unit owned by that
module. The reviewed 39-row migration inventory produced 126 relationships
from 28 accepted Planning and Commit policy units. One-to-many mappings preserve
coherent source meaning rather than preserving the legacy edge count.

## Dependency Evidence

- `standards_policy_impact` consumes the metadata-owned corpus and compiles one
  graph contribution plus one typed semantics index.
- `standards_graph` projects policy-unit nodes and composes relationship
  providers; `standards_metadata` has no graph dependency.
- `standards_analysis` imports policy-unit models from metadata and retains only
  comparison, classification, seed selection, and impact behavior.
- The Standards Engine and verifier composition roots reuse one corpus for
  compilation and graph composition.
- `standards_analysis.policy_units` and its graph source were removed without a
  compatibility re-export or fallback parser.

## Navigation And Validation

Exact policy-unit queries traverse only that unit's relationships. Module-level
Standards Engine navigation derives a grouped view from contained units while
retaining every policy-unit source in returned relationship summaries. A module
with no mapped policy units reports an incomplete mapping rather than a
successful empty policy-impact conclusion.

The compiler rejects module sources, aliases used as canonical sources,
retired units, cross-owner units, and unknown units. Metadata loading separately
requires active locators to resolve exactly once and validates identity,
ownership, alias, predecessor, successor, and tombstone invariants.

## Verification Evidence

- Contract validation: 27 examples, 7 identity fixtures, 4 operation
  envelopes, and 100 definitions.
- Python tests: graph engine, applicability, metadata, policy impact, standards
  graph, analysis, Standards Engine, and verifier suites.
- Declarative verification: all 218 registered suites, including focused
  policy-semantic-impact fixtures.
- Complete mixed repository checkpoint, generated freshness, plan and Markdown
  link checks, and `git diff --check` at the accepted write set.
