# Milestone 7 Row 45 Language Index Closure

## Owner Review

`STD-0704` and `STD-0705` are the frozen title/introduction and language
catalog of `languages/README.md`. Both route language-profile selection to
`STANDARDS-ROUTER.md`; neither owns an independent language mechanism.

The current source is not yet a valid non-normative index. It repeats Router
policy through "do not replace" and "should not live inline" statements and
retains the legacy Rust index as an entrypoint. Closure must replace those
statements with concise navigation to the Router's Language Profiles section
and the canonical Rust profile. The legacy Rust index is not a fallback route.

## Exact Outcomes

- `STD-0704` receives one `index` disposition to `STANDARDS-ROUTER.md`; the
  source becomes an explicitly non-normative language-profile entrypoint.
- `STD-0705` receives one `index` disposition to `STANDARDS-ROUTER.md`; its
  manual catalog becomes concise canonical-profile navigation without copied
  applicability policy or a legacy-index route.

The Router remains the sole applicability and dependency authority. The Rust
profile remains the canonical Rust navigation owner.

## Consumer Audit Impact

The required `verify-language-index-closure.sh` will directly inspect
`languages/README.md`, so it is a new non-root README consumer. Implementation
must add exactly that verifier to the shared README-consumer manifest, add one
precise `language-index-closure` classification to the audit schema, and update
the row-35 checker from 32 to 33 classified consumers. It must not broaden any
existing consumer classification or add a positive root-README route.

This shared checker change remains serial integration-owner work and requires
the complete fail-fast suite after focused P37 evidence passes.

## Ordered Child

Child `45.1` rewrites the language index, records both exact dispositions, adds
the language-index closure verifier, applies the bounded consumer-audit update,
closes row 45 and P37, and advances to immutable row 46. Planning acceptance
does not dispose either identifier or change the source.

## Bounded Write Set

Planning may touch only this decomposition, its owner-validation fixture and
checker, the active plan, and the execution ledger. Implementation may touch
only `languages/README.md`, the exact disposition table, the new language-index
verifier, the row-45 checker, the README-consumer manifest and audit checker,
the row-35 checker count, plan, and ledger.

The Router, canonical Rust profile, legacy Rust index, other consumers,
generated inventories, immutable train, package manifest, templates,
configuration, lockfiles, and downstream repositories remain read-only.

## Verification Gates

Planning requires exact row and P37 identity, two undisposed source IDs, owner
metadata, current source-policy and legacy-route detection, prospective verifier
uniqueness, the frozen 32-consumer baseline, Router and language-profile routing
evidence, execution-train integrity, plan structure, shell syntax, and diff
integrity.

Implementation additionally requires two unique exact dispositions, concise
source headings and canonical links, absence of copied policy and legacy
fallback routing, exactly 33 classified README consumers, unchanged root README
authority, row-45 and P37 closure, row-46 activation, and the complete
fail-fast suite.

## Typed Outcomes And No Fallback

Unknown language applicability remains a Router diagnostic. Do not select a
profile from README presence, preserve inline root-policy ownership, route
through the legacy Rust index, read every language profile, infer applicability
from the catalog, copy Router policy into the index, omit the new consumer from
the audit, or retain an undisposed identifier.

## Re-plan Triggers

Stop if either identifier contains unique normative policy, the Router is not
the canonical owner, source cleanup requires a third semantic outcome, the new
consumer cannot be represented exactly in the shared audit, implementation
requires files outside the bounded write set, or focused evidence cannot prove
closure without weakening a canonical contract.
