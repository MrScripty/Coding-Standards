# Standards Verification Guide

Verification should help agents find applicable coding guidance and use the
Engine correctly. Evidence must state the behavior actually observed.

## Current checkpoint

Use the Engine `verify_repository` operation, documented in the
[Verifier README](../../tools/standards_verifier/README.md). It checks declared
metadata, routes, navigation links, plan records, consumer graph structure,
generated contracts, and package boundaries. A passing checkpoint does not imply
that every relevant consumer was declared or that downstream code conforms.

The retained suites describe these limited observations. Do not interpret their
historical names as broader acceptance claims. Functional Engine tests must be
run separately before claiming behavior such as successful editing, receipt
publication, immutable replay, or rejection of mismatched evidence.

## Graph coverage and reviews

Source-owned relationships identify consumers to inspect. `review:consumer`
binds a review to that consumer's content and relationship; `suite:<id>` also
includes the named suite's declared inputs. Neither ownership label creates a
certificate. Engine audit publication requires actual review evidence and
bound authorization. Stale certificates must not be treated as current.

The September 2026 cleanup removed the stale claims rather than renewing them
without review. Registered coverage remains review-required. Receipt code and
its functional tests are registered consumers so relevant changes affect their
review requirements. The registered graph is an explicit review scope, not proof
that no undeclared consumer exists.

## Historical evaluation

The baseline at `6b4df85f042898374e9d23d265f4ecd25b0a7ba7`, archived reports,
and frozen snapshots record earlier observations. They do not establish current
Engine behavior. Retired policy simulations and migration fixtures can be read
from Git history; they are no longer checkpoint obligations.

## Scoring

For a substantive review, score each rubric dimension:

- `0`: missing, contradictory, or requires an incorrect outcome;
- `1`: partially covered, ambiguous, duplicated, or disproportionate;
- `2`: clear, sufficient, proportionate, and owned.

Reducing document size cannot compensate for a lower correctness score. Review
whether the guidance helps an agent make a real design or development decision,
including relevant exceptions and tradeoffs. Do not replace that judgment with
exact phrasing, arbitrary line counts, or a model that merely restates the rule.
