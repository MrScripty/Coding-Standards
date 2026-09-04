# Milestone 7 Row 19 Tooling Decomposition

## Proposed Owner Contract

`workflows/tooling.md` will own generic selection, configuration, automation,
orchestration, scheduling, cost control, debt tracking, and result reporting for
development tools.

It applies when a repository must choose or coordinate tools that support
implementation and evidence production. It does not own what evidence proves,
change procedure, commit-history safety, dependency provisioning or versions,
documentation obligations, product runtime behavior, language-specific tool
semantics, or copyable recipes.

The owner will require `core`, `workflow.implementation`,
`workflow.verification`, and `workflow.commit`. Existing owners retain
precedence for their concerns; Tooling transports or schedules their selected
checks without redefining them. Contradictory tool, authority, scope, or
orchestration facts are `invalid`; unavailable required capability or access is
`unavailable`; unsupported repository, platform, or toolchain capability is
`unsupported`.

Tooling must not fall back to conventional tools, hook stages, editor settings,
warning policies, formatter/linter pairs, CI providers, gate lists, fail-fast
modes, tiers, caches, timeouts, path filters, installation commands, or passing
automation as acceptance.

## Ordered Children

The 18 overlay rows are exact, canonical-owner-homogeneous semantic outcomes. Child
`19.1` creates a useful owner and focused decision fixture before any later
Tooling population. Shared legacy-source edits, plan state, dispositions,
generated artifacts, router changes, metadata, and reference indexes remain
serial integration-owner work.

Each child must preserve exact dispositions, remove competing legacy authority,
add focused positive and negative evidence, run its declared checkpoint, and
advance the cursor atomically. Reference children create or populate
`reference/recipes/tooling.md` as non-normative material; routed children amend
only the canonical owner when the legacy rule contains a missing generic
contract, otherwise they convert the source section to an index.

Child `19.8` is a reviewed split package because each source identifier mixes
durable TypeScript semantics with volatile product syntax. The TypeScript
profile remains the only canonical owner and receives the normative contract.
`reference/recipes/tooling.md` receives only non-normative ESLint, Prettier,
`tsconfig`, glob, preset, and custom-rule examples. Each source identifier still
receives exactly one `split` disposition to its canonical TypeScript owner; the
reference extraction is supporting material, not a second authority or a
duplicate disposition.

Child `19.9` applies the same boundary to formatting. Tooling remains the sole
canonical owner for formatting responsibility, editor automation selection,
scheduling, and formatter/linter separation. `STD-0682` and `STD-0686` use one
`split` disposition each while VS Code settings, format-on-save configuration,
Prettier/ESLint pairing, and installation syntax move only to non-normative
Tooling recipes. `STD-0681` and `STD-0683` remain direct Tooling refinements.
Child `19.10` remains independently responsible for standalone formatter
command and output examples.

Child `19.12` applies the split boundary to CI orchestration. Tooling remains
the sole canonical owner for provider-neutral dependency graphs, failure
aggregation, scheduling, cancellation, and reporting. `STD-0687` is a direct
refinement; `STD-0689` and `STD-0690` receive one `split` disposition each while
GitHub matrix, `fail-fast`, `if: always()`, `continue-on-error`, `needs`,
`success()`, fixed-tier, launcher, and package-command examples move only to
non-normative Tooling recipes. Child `19.14` remains independently responsible
for the full CI workflow YAML.

Child `19.13` applies the same boundary to debt and automation cost. Tooling
remains the sole canonical owner for debt-boundary selection, measured cost,
cache suitability, cancellation, filtering, timeout, retention, and diagnostic
strategy. `STD-0691` is a direct refinement and `STD-0692` receives one `split`
disposition while GitHub permissions, concurrency, setup, cache, package-command,
summary, and artifact syntax move only to non-normative Tooling recipes. Child
`19.14` remains independently responsible for the full CI workflow YAML.

Child `19.15` reconciles replacement lineage rather than restoring obsolete
headings. `STD-0696` records the former Directory Validation parent as an index
lineage disposition. `STD-0697` receives one `split` disposition with
Documentation as sole canonical owner for impact selection, stable boundary
association, explicit diff inputs, and typed diagnostics. Maps, commands, hook
YAML, and provider syntax move only to non-normative reference. The remaining
children are renumbered without changing their ownership or dependency order.

Child `19.16` keeps Implementation as sole canonical owner for selecting change
description evidence from risk, affected contracts, decisions, review needs,
and Verification claims. `STD-0698` receives one `split` disposition while
GitHub template placement, installation commands, headings, and checklist
syntax move only to a non-normative Implementation recipe.

## Implementation Sequence

1. Create the bounded Tooling owner with hook orchestration (`19.1`).
2. Route commit safety and separate hook recipes (`19.2`-`19.3`).
3. Govern editor configuration and move examples (`19.4`-`19.5`).
4. Govern generic linting, move taxonomy, and split TypeScript policy from
   product recipes (`19.6`-`19.8`).
5. Split formatting policy from product recipes, then move standalone command
   examples (`19.9`-`19.10`).
6. Separate Verification gate meaning from provider-neutral CI orchestration
   and product recipes (`19.11`-`19.12`).
7. Govern debt/cost and move CI recipes (`19.13`-`19.14`).
8. Reconcile traceability lineage, then route PR, dependency, and setup concerns
   (`19.15`-`19.18`).

## Re-plan Triggers

Stop if implementation requires Tooling to redefine another owner's contract,
creates a dependency cycle, makes reference material normative, preserves a
legacy default, or cannot produce a useful owner in child `19.1`.
