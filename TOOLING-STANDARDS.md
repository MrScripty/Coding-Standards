# Tooling Standards

Legacy tooling guidance pending exact migration. Canonical generic automation
authority is [Tooling](workflows/tooling.md).

> **Acceptance authority:** [workflows/verification.md](workflows/verification.md)
> defines acceptance claims and what evidence proves. This file owns automation,
> scheduling, and reporting mechanisms. Moving a check between local hooks, CI,
> dedicated runners, release jobs, or manual procedures does not change its
> claim.

## Pre-Commit Hooks

Canonical hook selection and orchestration are defined by
[Tooling](workflows/tooling.md). The remaining subsections are migration input,
not competing generic authority.

### Why Pre-Commit Hooks

The former rationale is retained only as a non-normative
[Tooling recipe](reference/recipes/tooling.md#hook-feedback).

### Hook Runner Example

The former Lefthook selection and installation example is retained only in the
non-normative [Tooling recipe](reference/recipes/tooling.md#lefthook-example).

### Basic Configuration

Canonical configuration selection is defined by [Tooling](workflows/tooling.md).
The former configuration is retained only as a non-normative
[Tooling recipe](reference/recipes/tooling.md#lefthook-example).

### Hook Categories

Canonical scheduling is defined by [Tooling](workflows/tooling.md). The table
below remains migration input and does not define default stages.

| Hook | When | Typical Checks |
|------|------|-------------|
| pre-commit | Before each commit | Affected fast checks with useful local feedback |
| pre-push | Before pushing | Broader or more expensive checks selected by the project |
| commit-msg | After writing message | Validate commit message format |

These are scheduling defaults, not acceptance categories. A required claim may
run at either hook, in CI, on a dedicated environment, or through a recorded
manual procedure.

### Branch-History Review Reminder

Canonical history-review reminders and rewrite authority are defined by the
[Commit Workflow](workflows/commit.md#branch-history-review).

### Performance Tips

Canonical scheduling and cost decisions are defined by
[Tooling](workflows/tooling.md). The list below remains migration input.

1. **Run in parallel** - Independent checks should run concurrently
2. **Check only staged files** - Use `{staged_files}` placeholder
3. **Schedule by measured cost** - Keep interactive hooks useful and place
   expensive claims at an owned later gate
4. **Use file globs** - Only run checks on relevant file types

### Persisted Artifact Validation Hooks

Canonical persisted-artifact check orchestration is defined by
[Tooling](workflows/tooling.md). The recommendations below remain migration
input and are not defaults.

If the repo commits JSON, YAML, manifests, templates, saved workflows, or other
schema-backed artifacts, add fast staged-file validation where feasible.

Recommended approach:
- Run lightweight schema or shape validation in `pre-commit` for changed files
- Restrict checks to staged artifact paths for speed
- Regenerate derived artifacts in tooling when regeneration is deterministic
- Run broader validation or acceptance checks in `pre-push` when full-context
  verification is too slow for `pre-commit`

The goal is to stop checked-in examples and fixtures from drifting away from the
current producer contract.

---

## EditorConfig

Canonical editor-neutral configuration selection is defined by
[Tooling](workflows/tooling.md#editor-and-file-configuration). The remaining
rationale and examples are migration input, not EditorConfig authority.

### Purpose

The former EditorConfig rationale is retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#editorconfig-example).

### Standard Configuration

The former template and file-family settings are retained only in the
non-normative [Tooling recipe](reference/recipes/tooling.md#editorconfig-example).

### Key Settings

Select settings through the canonical
[Tooling workflow](workflows/tooling.md#editor-and-file-configuration). The
former universal settings table is retired and defines no defaults.

---

## Linting Strategy

Canonical lint policy and orchestration are defined by
[Tooling](workflows/tooling.md#lint-policy-and-orchestration).

### Language-Agnostic Principles

Select purpose, scope, severity, automation, and schedule through the canonical
Tooling workflow. Warning failure, autofix, changed-file scope, tiers, and CI
placement are not defaults.

### Common Linter Categories

The former category taxonomy and product list are retained only in the
non-normative [Tooling recipe](reference/recipes/tooling.md#linter-category-examples).

### TypeScript/JavaScript: ESLint 9+ (Flat Config) + Prettier

Canonical TypeScript static-analysis policy is defined by the
[TypeScript profile](profiles/languages/typescript.md#static-analysis-and-compiler-configuration).
Product syntax is retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#typescript-tooling-examples).

#### Common Flat Config Pitfalls

The former product-specific pitfalls are retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#typescript-tooling-examples).

Frontend-specific lint details (including React runtime-specific rule guidance)
are defined in [FRONTEND-STANDARDS.md](FRONTEND-STANDARDS.md).

### TypeScript Strict Mode

Select compiler checks through the canonical TypeScript profile. The former
flag list is retained only in the non-normative Tooling recipe.

### Custom Rules for Architecture

Derive architecture checks from canonical architecture authority. The former
custom-rule implementation is retained only in the non-normative Tooling recipe.

---

## Formatting

Canonical formatting authority and orchestration are defined by
[Tooling](workflows/tooling.md#formatting-policy-and-orchestration).

### Principle: Format on Save

Select editor automation and mutation authority through canonical Tooling.
The former VS Code example is retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#formatting-automation-examples).

### Principle: Check in CI

Select formatting checks and their schedule through canonical Tooling. The
former command and output example is retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#formatting-automation-examples).

### Format vs. Lint

Select formatter and linter responsibilities through canonical Tooling. The
former Prettier/ESLint pairing and installation example is retained only in the
non-normative [Tooling recipe](reference/recipes/tooling.md#formatting-automation-examples).

---

## CI Integration

Canonical CI orchestration, dependency-graph, failure-reporting, and scheduling
authority are defined by
[Tooling](workflows/tooling.md#ci-orchestration-and-scheduling).

### Quality Gates Are Mandatory

Canonical gate acceptance and blocking authority are defined by
[Verification](workflows/verification.md#quality-gates-and-execution-location).
The former universal gate catalog is retired and defines no mandatory checks.

### Prefer Failure Aggregation Over Fail-Fast

Select failure aggregation and reporting through canonical Tooling. The former
GitHub matrix, fail-fast, summary-job, and error-continuation examples are
retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#ci-orchestration-examples).

### Tiered CI Execution

Select the dependency graph, schedule, cancellation, and reporting behavior
through canonical Tooling. The former fixed tiers, GitHub dependency syntax,
and launcher and package commands are retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#ci-orchestration-examples).

### Lint Debt Ratchet (When Full Lint Is Temporarily Non-Blocking)

Select tool-debt boundaries, evidence, change rules, and retirement conditions
through canonical [Tooling](workflows/tooling.md#tool-debt-governance). The former
fixed snapshot, count, changed-code, zero-debt, and blocking-tier ratchet defines
no default algorithm.

### CI Performance Standards

Select automation-cost optimization, caching, timeouts, filtering, retention,
and diagnostics through canonical
[Tooling](workflows/tooling.md#automation-cost-and-operational-evidence). The
former GitHub Actions, Node, Rust, cache, package-command, summary, and artifact
examples are retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#automation-cost-examples).

### Recommended CI Workflow

The former complete GitHub Actions workflow is retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#complete-ci-workflow-example). It
defines no provider, trigger, permission, job, gate, cache, command, timeout,
matrix, dependency, diagnostic, or failure-handling default.

### CI vs. Local Checks

Canonical execution-location evidence meaning is defined by
[Verification](workflows/verification.md#quality-gates-and-execution-location).
Local and CI labels create no proof hierarchy.

---

## Decision Traceability

Canonical documentation-impact and traceability authority are defined by the
[Documentation Workflow](workflows/documentation.md#decision-traceability). The
former impact-map, installation, diff-mode, hook, and provider examples are
retained only in the non-normative
[Documentation recipe](reference/recipes/documentation.md#decision-traceability-examples).
This legacy index defines no directory, README, map, artifact, diff-mode, branch,
command, hook, or provider default.

### PR Template Enforcement

Select change-description evidence through the canonical
[Implementation Workflow](workflows/implementation.md#change-description-evidence).
The former GitHub template placement and installation commands are retained only
in the non-normative
[Implementation recipe](reference/recipes/implementation.md#pull-request-template-example).
This legacy route defines no pull-request, provider, template, heading,
checklist, or command default.

---

## Dependency Auditing

Select dependency audit scope, evidence, finding ownership, automation, and
bootstrap dependencies through canonical
[Dependencies](topics/dependencies.md#audit-and-review). This legacy route
defines no audit tool, finding severity, schedule, CI placement, installation,
or success default.

---

## Tool Installation Checklist

This heading indexes the non-normative
[legacy setup and package-script examples](reference/recipes/tooling.md#legacy-tool-setup-and-package-script-example).
Canonical dependency satisfaction and provisioning authority belong to
[Dependencies](topics/dependencies.md#satisfaction-and-provisioning). The
heading defines no required tool set, installation checklist, package manager,
command, or implicit provisioning authority.

---

## Bypassing Hooks (Emergency Only)

Canonical hook-bypass authority is defined by the
[Commit Workflow](workflows/commit.md#hook-bypass-authority). This legacy
section defines no emergency, command, documentation, or follow-up default.
