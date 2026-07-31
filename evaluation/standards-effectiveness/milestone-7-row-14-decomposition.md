# Milestone 7 Row 14 Decomposition

## Purpose

This report records the bounded owner review of immutable execution row 14,
`STD-0487` through `STD-0512`. It is planning evidence, not normative policy.

The frozen row combines launcher projection, verification acceptance,
dependency installation, build and release semantics, state isolation, shell
mechanisms, generated-command security, and a copied reference template. Those
concerns do not share one canonical owner, dependency set, semantic decision,
or verification contract.

## Frozen Evidence

| IDs | Frozen concern | Ownership finding |
| --- | --- | --- |
| `STD-0487`-`STD-0494`, `STD-0499`, `STD-0501`-`STD-0507`, `STD-0511`, `STD-0512` | Launcher scope, actions, parsing, workflow projection, output, runtime delegation, managed state, help, outcomes, Bash mechanisms, template, and checklist | The Launcher profile owns command projection, decoding, delegation, process/state lifecycle, and terminal outcomes. It consumes procedure authority from other owners. The copied template and checklist become non-normative structural guidance; Bash, fixed flags, fixed codes, build no-ops, and example commands are not universal authority. |
| `STD-0495` | GUI CI smoke requirements | Verification owns evidence kind, environment, execution mode, and acceptance claims. Launcher only exposes the selected smoke procedure and preserves its result. |
| `STD-0496`-`STD-0498` | Dependency installation, checks, model, and output | The planned Dependencies topic must first own satisfaction evidence, selection, installation authorization, verification, and typed outcomes. Launcher then adapts that accepted procedure without implicit install or package-manager fallback. |
| `STD-0500` | Development and release build behavior | Release owns artifact-plan and build-procedure semantics. Launcher delegates the selected procedure without inventing targets, modes, commands, or successful no-ops. |
| `STD-0508`-`STD-0510` | Generated desktop entries and shell scripts | Security owns untrusted-input authorization, validation, and destination-specific encoding. Example helpers and escaping recipes are mechanisms, not proof or fallback. |

## Ordered Children

### Child 14.1: Launcher Population And Structural Closure

Refine the Launcher-owned identifiers into the existing application profile.
Preserve only command projection, decoding, delegation, process/state
lifecycle, help, and terminal-outcome behavior. Close headings, copied
templates, and checklists as non-normative routing or reference material.

### Child 14.2: GUI Smoke Acceptance

Refine `STD-0495` into Verification. Keep environment and acceptance authority
there while Launcher consumes the selected procedure.

### Child 14.3: Dependencies Owner And Population

Establish a non-empty `topics/dependencies.md` contract before disposing
`STD-0496` through `STD-0498`. Populate only after owner applicability,
selection authority, installation authorization, evidence, and typed outcomes
are accepted.

### Child 14.4: Build Procedure

Refine `STD-0500` into Release as artifact-plan-derived procedure guidance.

### Child 14.5: Generated Command Security

Refine `STD-0508` through `STD-0510` into Security with operation-contract
validation, destination-specific encoding, and negative tests.

## No Fallback

This decomposition does not preserve mandatory Bash, fixed launcher flags,
fixed exit codes, copied commands, implicit installation, monolithic dependency
checks, successful build no-ops, guessed build targets, weakened GUI runtime
modes, raw interpolation, example helper names, or the reference template as
defaults. Missing or contradictory action, procedure, dependency, artifact,
environment, state, validation, encoding, or evidence facts require typed
diagnostics rather than an alternate command, mechanism, target, mode, input,
or default success.

## Scope

This planning slice changes only the row-14 decomposition overlay, package
classification, this report and checker, plan/ledger/evaluation tracking, and
superseded cursor assertions. It changes no normative or legacy standard,
disposition, router, metadata, generated inventory, owner map, configuration,
lockfile, or downstream repository.

## Next Slice

Milestone `7.4b8az` refines `STD-0500` into Release. It does not dispose the
Security group.
