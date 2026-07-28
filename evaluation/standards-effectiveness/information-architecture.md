# Standards Information Architecture Decision

## Status

Accepted for implementation by Milestones 2-8.

## Decision

The library will use progressive disclosure with six document roles:

| Role | Purpose | Normative behavior |
| --- | --- | --- |
| Core | Universal invariants for all adopted projects | Always applies. |
| Router | Selects workflows, profiles, and topics | Procedural authority for applicability only. |
| Workflow | Governs an activity such as planning or release | Applies when that activity occurs. |
| Profile | Specializes guidance for an application, boundary, or language | Applies only when selected conditions hold. |
| Topic | Adds requirements for an affected concern | Applies when the concern is present; does not override. |
| Reference | Examples, recipes, catalogs, and explanations | Never normative. |

Normal task context is:

```text
CORE-STANDARDS.md
  + STANDARDS-ROUTER.md
  + applicable workflow(s)
  + applicable profile(s)
  + affected topic(s)
```

Reference material is loaded only when needed to perform a selected rule.

## Canonical Paths

```text
CORE-STANDARDS.md
STANDARDS-ROUTER.md
workflows/
  commit.md
  documentation.md
  implementation.md
  planning.md
  release.md
  tooling.md
  verification.md
profiles/
  applications/
    cli.md
    desktop.md
    frontend.md
    launcher.md
    library.md
    service-worker.md
  boundaries/
    interop.md
    ipc.md
    language-bindings.md
    persistence.md
  languages/
    rust/
      README.md
      api.md
      async.md
      cross-platform.md
      dependencies.md
      interop.md
      language-bindings.md
      release.md
      security.md
      tooling.md
      unsafe.md
topics/
  accessibility.md
  concurrency.md
  contracts.md
  cross-platform.md
  dependencies.md
  diagnostics.md
  resilience.md
  security.md
reference/
  adoption/
  patterns/
  recipes/
prompts/
templates/
```

Not every listed profile must exist before a real scenario selects it. Empty
placeholder modules are prohibited.

## Module Metadata Contract

Each canonical module begins after its title with:

```markdown
**Standards metadata**

- ID: `workflow.planning`
- Role: `workflow`
- Level: `MUST`
- Applies when: Multi-step implementation work requires an active plan.
- Does not apply when: The task is a bounded local change with no sequencing decision.
- Requires: `core`
- Specializes: `none`
- Verification: Planning scenario fixtures and active-plan structure checks.
- Canonical owner: `workflows/planning.md`
```

Required fields and values are defined in `metadata-schema.md`.

The metadata describes module applicability. Individual requirements still use
plain normative language. Metadata must not become a second prose standards
system.

## Level Semantics

- `MUST`: selected requirements are mandatory for compliance.
- `SHOULD`: defaults may be overridden by a recorded, evidence-based reason.
- `PROFILE`: requirements are mandatory only when routing selects the profile.
- `REFERENCE`: non-binding explanation or implementation help.

A canonical module has one level. If mandatory rules and optional recipes are
mixed, split the recipes into reference material.

## Routing Rules

1. Load Core and Router.
2. Select workflows from the requested activity.
3. Select application profiles from the delivered artifact or process shape.
4. Select boundary profiles from actual trust, process, persistence, FFI, or
   generated-contract crossings.
5. Select language profiles only for languages changed by the task.
6. Select topics from affected concerns.
7. Follow declared `Requires` transitively.
8. Load reference documents only when a selected module links to them.
9. If applicability facts are missing, return an unresolved-routing diagnostic
   rather than guessing.

The router must state both inclusions and common exclusions. A small local fix
must not inherit release, architecture, frontend, launcher, or interop guidance
without an observable condition.

## Precedence

From highest to lowest:

1. Law, platform security constraints, and external protocol/tool contracts.
2. The adopted project's explicit public/persisted contracts and accepted
   architecture decisions.
3. Core invariants.
4. A selected profile, but only for rules named by `Specializes`.
5. Selected workflows and topics, which add requirements without overriding
   higher levels.
6. `SHOULD` defaults.
7. Reference examples and recipes.

Additional rules:

- A project may be stricter than the library.
- A project exception to a `MUST` rule must be explicit, owned, justified, and
  must not be represented as compliance with the overridden rule.
- A profile cannot silently weaken Core.
- A topic cannot override another topic.
- Examples never establish precedence.
- A conflict or dependency cycle is an invalid standards set and must produce
  a diagnostic.

## Existing Entrypoint Migration

Current top-level `*-STANDARDS.md` files remain usable during migration. As
their rules move, they become concise indexes that:

- identify the new canonical owner;
- preserve stable discovery links;
- contain no competing normative text; and
- state the standards version in which the move occurred.

Indexes remain for one published major standards version after migration.
Longer retention requires downstream evidence, not speculative compatibility.

## Prompt And Template Decision

Prompts are distributed operational entrypoints and must be versioned. Milestone
3 will remove `/prompts/` from `.gitignore`, replace machine-specific and
duplicated instructions with thin versioned prompts, and point each prompt to
its canonical workflow.

Templates are derived artifacts. Their canonical semantics belong to the
corresponding workflow; focused checks must prevent template/workflow drift.

## Ownership And Evolution

- Core and Router are serial integration-owner files.
- A workflow owns process state for its activity.
- A profile owns only its specialization mechanism.
- A topic owns one concern across stacks.
- Reference content cannot be cited as a mandatory requirement.
- Rule movement updates its inventory disposition and old index in the same
  slice.
- New roles or precedence levels require a re-plan and metadata fixture change.

## Rejected Alternatives

### Keep The Flat Library

Rejected because applicability and precedence would remain inferential, and
large files would continue mixing policy with recipes.

### One Document Per Task Type

Rejected because it duplicates shared rules across task combinations.

### Fully Machine-Generated Standards

Rejected because architecture quality is not mechanically decidable. Automation
is limited to deterministic metadata, ownership, dependency, and link checks.

### Preserve Ignored Local Prompts

Rejected because unversioned operational guidance cannot be audited, adopted,
or reproduced reliably.
