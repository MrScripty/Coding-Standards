# Milestone 7 Row 28 Accessibility Decomposition

## Owner Contract

Create `topics/accessibility.md` as the generic owner for perceivable,
operable, understandable interaction semantics across supported modalities.
Frontend specializes web mechanisms; Tooling owns lint selection and
orchestration; Verification owns evidence claims. HTML, JSX, CSS, icon-library,
ESLint, command, rule-name, and CI examples are not generic defaults.

## Exact Ownership

- `STD-0007` is an `index` route to the new owner.
- `STD-0008` through `STD-0022` split durable Accessibility policy from web
  examples moved to `reference/recipes/accessibility.md`; empty parent headings
  may use `index` when they add no independent policy.
- `STD-0023` through `STD-0026` split Accessibility evidence requirements from
  Tooling/Verification decisions and move ESLint commands, products, rules, and
  CI syntax to reference without defaults.

Each identifier receives exactly one disposition. The detailed owner-validation
table is frozen before each implementation child, not inferred from proximity.

## Ordered Children

1. `28.1`: create the useful generic owner, reference boundary, router and
   parent-index routes, metadata, and focused owner decisions with `STD-0007`.
2. `28.2`: migrate semantic-role and action/navigation contracts for
   `STD-0008` through `STD-0012`, extracting web syntax.
3. `28.3`: migrate keyboard, focus visibility, and focus-lifecycle contracts for
   `STD-0013` through `STD-0016`, extracting CSS and mechanism examples.
4. `28.4`: migrate accessible-name and form-label contracts for `STD-0017`
   through `STD-0019`, extracting JSX examples.
5. `28.5`: migrate informative/decorative media contracts for `STD-0020`
   through `STD-0022`, extracting HTML and icon-library examples.
6. `28.6`: migrate evidence obligations for `STD-0023` through `STD-0026`,
   extract lint/CI mechanisms, close the legacy source, and run the full suite.

Shared router, README, metadata, dispositions, plan, and ledger remain serial.
Each child may additionally touch only its owner section, reference section,
focused fixture/checker, legacy source section, and frozen validation rows.

## No-Fallback Rule

Do not make HTML, ARIA, React, JSX, CSS, ESLint, a plugin, named rules, CI, WCAG
version, pointer modality, or visible-interface assumptions universal. Missing
required user/modality/interaction/evidence facts are `unavailable`;
contradictory semantics are `invalid`; unsupported assistive or test capability
is `unsupported`, never a reason to omit the obligation silently.

## Re-plan Triggers

Stop if a child needs a product default, external-standard version default,
multiple dispositions for one identifier, frontend ownership of generic
semantics, duplicated normative owners, or files outside its approved write set.
