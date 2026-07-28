# Standards Effectiveness Evaluation

This directory contains the reproducible baseline and neutral evaluation
fixtures for the standards-library effectiveness restructure.

## Baseline

The baseline is frozen at commit
`6b4df85f042898374e9d23d265f4ecd25b0a7ba7`, immediately after the
restructure plan was added and before normative standards changed.

`corpus.tsv` classifies every Markdown artifact by its current kind,
normative role, preliminary target role, preliminary disposition, and frozen
source.
`generate-baseline.sh` reads each artifact from the frozen commit and writes:

- `generated/file-metrics.tsv`: lines, headings, and strong imperative
  occurrences by file;
- `generated/section-inventory.tsv`: a stable identifier for every heading in
  normative or operationally derived guidance; and
- `generated/summary.tsv`: corpus totals used by the baseline report.

Run:

```bash
./evaluation/standards-effectiveness/generate-baseline.sh \
  /path/to/Coding-Standards
```

Generated metrics are factual inventory. `findings.md` owns semantic findings
such as duplication, conflicts, broad obligations, and ownership gaps.

The working tree contains ignored prompt files. Their contents are frozen under
`snapshots/prompts/` for baseline reproducibility only, with trailing whitespace
normalized. The snapshots are not canonical guidance; Milestone 1 must decide
whether prompts are versioned distribution artifacts or remain explicitly
local.

## Fixtures

`fixtures/scenarios.md` defines seven product-neutral tasks. Each scenario
declares expected routing, acceptance, exclusions, prohibited errors, and plan
artifacts. `baseline-scores.md` applies the fixed rubric to current guidance.

The same fixtures and rubric must be used after restructuring. A changed
fixture requires a recorded reason and before/after rescoring.

## Architecture Contract

- `information-architecture.md` owns roles, paths, routing, precedence, and
  migration decisions.
- `metadata-schema.md` defines canonical module metadata.
- `owner-map.tsv` and `owner-overrides.tsv` map the baseline corpus to proposed
  canonical owners.
- `generate-owner-map.sh` writes the complete 916-section owner proposal.
- `check-metadata.sh` and `verify-metadata-fixtures.sh` validate the metadata
  contract and its negative cases.

## Routed Vertical Slice

`verify-s1-routing.sh` checks the first complete routed path:

- S1 small local bug fix;
- Rust language profile;
- library application profile;
- Core, Router, implementation, and verification workflows; and
- explicit exclusion of unrelated standards.

The selected context is compared with the frozen baseline line count.

## Plan Lifecycle Fixtures

`check-plan-structure.sh` and `verify-plan-fixtures.sh` enforce deterministic
active-plan structure:

- current lifecycle state, phase, and exactly one next slice;
- plan-level acceptance status;
- separate ledger and issue artifacts;
- valid milestone states;
- no embedded execution diary; and
- no `Accepted` state while acceptance remains pending, partial, or blocked.

Human review still owns whether the named evidence semantically proves the
objective.

## Acceptance Claim Fixtures

`verify-acceptance-claims.sh` checks the seven fixed scenarios and focused
regressions against the canonical claim model:

- evidence kind, environment qualification, and execution mode are separate;
- every required claim must have matching observed evidence;
- simulated hardware evidence cannot satisfy required-real acceptance;
- startup smoke cannot substitute for a user workflow; and
- manual execution is not a higher evidence kind.

`verify-verification-ownership.sh` checks that Verification remains the single
acceptance owner while Testing, Tooling, Launcher, and Release retain only their
test-design, scheduling, command, and shipping responsibilities. It rejects the
legacy universal timing/CI taxonomy and smoke-as-feature substitution.

## Contract Decision Fixtures

`verify-contract-decisions.sh` checks coordinated replacement, persisted
migration, public versioning, independently deployed negotiation, generated
artifacts, derived-state rebuild, valid degradation, and typed unavailable,
invalid, or unsupported outcomes. It rejects replacement across independent or
authoritative-state boundaries and degradation without an authoritative,
semantically equivalent source.

`verify-contract-ownership.sh` checks that legacy architecture, coding,
interop, release, and binding guidance links to the canonical topic and does not
restore universal append-only evolution, mandatory coexistence, destructive
recovery, untyped cache/default fallback, blanket additive compatibility, or
catch-all executor delegation.

## Documentation Decision Fixtures

`verify-documentation-decisions.sh` checks that durable documentation is
selected from changed responsibilities, invariants, contracts, decisions, and
operational procedures rather than directory or file changes. It distinguishes
no-documentation, boundary README, contract README, ADR, and runbook profiles
and rejects the removed universal per-directory rule.

`verify-decision-traceability.sh` runs the distributed checker in isolated Git
repositories. It proves staged mode reads the index, range mode reads the
explicit base/head commits, mapped decision-bearing changes require their exact
artifact, unstaged work is excluded from staged mode, and an unrelated ADR
cannot satisfy another boundary. Prior/current map union cases ensure removing
a row cannot hide a deleted or relocated trigger.

## Commit Authority Fixtures

`verify-commit-authority.sh` separates per-commit staged review from full
branch-history review and history-maintenance authority. It permits rewriting
only for an explicitly authorized, unshared, recoverable range, distinguishes
linear and merge topology, and rejects the removed mandatory cleanup policy.

## Scoring

Each rubric dimension is scored:

- `0`: missing, contradictory, or requires an incorrect outcome;
- `1`: partially covered, ambiguous, duplicated, or disproportionate;
- `2`: clear, sufficient, proportionate, and owned.

Reducing document size cannot compensate for a lower correctness score.
