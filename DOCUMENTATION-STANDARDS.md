# Documentation Standards

Requirements for maintaining readable, navigable codebases.

## Documentation Selection

The [Documentation Workflow](workflows/documentation.md) is the canonical owner
for deciding when durable documentation is required and which profile applies.
This file retains artifact-layout, ADR, changelog, and project-README guidance
until their owner-bounded consolidation slices complete.

Do not infer a README requirement from directory count, file count, or a `src/`
path. Require documentation only for an affected durable responsibility,
decision, contract, or operational procedure.

## Documentation Artifact Layout

Project-level Markdown artifacts must live under a root-level `docs/`
directory unless the project has a documented legacy convention that is being
migrated.

Use these standard subdirectories:

```text
docs/
  adr/                    Architecture decision records
  plans/                  Implementation plans and staged work plans
  refactors/              Large refactor planning and execution records
  reports/                Audits, investigations, and analysis reports
```

When a plan, refactor, or report produces multiple Markdown files, create a
slugged subdirectory under the relevant category:

```text
docs/refactors/<refactor-slug>/
  pass-instructions/      Prompts or instruction files for analysis passes
  findings/               Findings produced by each analysis pass
  implementation-waves/   Planned parallel implementation waves and slice specs
  reports/                Future implementation sub-agent reports
  coordination-ledger.md  Host-owned status, dependencies, and handoffs
  final-plan.md           Final consolidated plan
```

Use lowercase, hyphen-separated slugs for artifact directories and file names.
Include dates in names only when they clarify ordering or distinguish repeated
work, for example `2026-04-22-runtime-boundary-refactor`.

Do not scatter planning artifacts across the repository root. Keep generated
planning, findings, and report Markdown grouped by the work item they support.

### README Template

Use [templates/README-TEMPLATE.md](templates/README-TEMPLATE.md) after the
Documentation Workflow selects `boundary-readme` or `contract-readme`.

The template contains a concise boundary profile and optional contract
extensions. Omit sections that do not apply. Do not create placeholder
sections, restate an ADR, or list every implementation file.

### Keeping Durable Documentation Current

Update the artifact that owns the changed knowledge:

- boundary README for responsibility or invariant changes;
- contract documentation for consumer-visible semantics;
- ADR for durable cross-boundary rationale; or
- runbook for operational procedure changes.

Routine source changes that preserve those facts do not require documentation
churn. Link canonical rationale instead of duplicating it.

---

## Code And Markdown Examples

Comment, Markdown, public-interface, and algorithm examples moved to the
non-normative
[Documentation Recipe](reference/recipes/documentation.md).

The [Documentation Workflow](workflows/documentation.md) remains the canonical
owner for deciding when durable documentation is required. Language profiles,
project formatters, and consumer contracts own their specific syntax and
behavior; this migration index does not impose a universal TODO format, table
alignment, public-symbol documentation rule, or algorithm template.

---

## Architecture Decision Records (ADRs)

### When to Write an ADR

Document significant architectural decisions:
- Technology choices
- Pattern selections
- Trade-offs made

### ADR Format

```markdown
# ADR-001: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
What situation are we facing? What problem needs solving?

## Decision
What did we decide to do?

## Consequences
What are the results of this decision?

### Positive
- Benefit 1
- Benefit 2

### Negative
- Drawback 1
- Drawback 2

### Neutral
- Side effect 1
```

### ADR Example

```markdown
# ADR-003: Use Event Sourcing for Order History

## Status
Accepted

## Context
We need to maintain a complete audit trail of all order changes.
Traditional CRUD updates lose historical state.

## Decision
Implement event sourcing for the Order aggregate.
All changes stored as immutable events.
Current state derived by replaying events.

## Consequences

### Positive
- Complete audit trail automatically maintained
- Can reconstruct state at any point in time
- Events enable easy integration with other systems

### Negative
- More complex than simple CRUD
- Requires event store infrastructure
- Querying current state requires projection

### Neutral
- Team needs to learn event sourcing patterns
```

### Where to Store ADRs

```
docs/
└── adr/
    ├── README.md          # Index of all ADRs
    ├── ADR-001-title.md
    ├── ADR-002-title.md
    └── ADR-003-title.md
```

---

## Changelog

For comprehensive release workflow guidance including changelog automation and
CI/CD integration, see [RELEASE-STANDARDS.md](RELEASE-STANDARDS.md).

### When to Maintain

For libraries, APIs, or any versioned software used by others.

### Format (Keep a Changelog)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature X

### Changed
- Updated behavior of Y

### Deprecated
- Feature Z will be removed in v3.0

### Removed
- Deleted deprecated function

### Fixed
- Bug in component A

### Security
- Fixed vulnerability in auth

## [1.2.0] - 2024-01-15

### Added
- Feature description

## [1.1.0] - 2024-01-01

### Fixed
- Bug description
```

### Categories

| Category | Use For |
|----------|---------|
| Added | New features |
| Changed | Changes in existing functionality |
| Deprecated | Soon-to-be removed features |
| Removed | Removed features |
| Fixed | Bug fixes |
| Security | Vulnerability fixes |

---

## README.md (Project Root)

### Required Sections

```markdown
# Project Name

Brief description of what the project does.

## Quick Start

Minimal steps to get running:
1. Clone
2. Install
3. Run

## Installation

Detailed installation instructions.

## Usage

How to use the project with examples.

## Development

How to set up for development:
- Prerequisites
- Build commands
- Test commands

## Project Structure

Overview of directory layout.

## Contributing

How to contribute (or link to CONTRIBUTING.md).

## License

License information.
```

### Keep It Current

The root README is often the first thing people see. Keep it:
- Accurate
- Up to date
- Focused on getting started

---

## Documentation Review Checklist

When reviewing PRs, check:

- [ ] New `src/` directories have README.md
- [ ] New non-`src/` directories with 3+ files or non-obvious purpose have README.md
- [ ] Public APIs are documented
- [ ] Complex logic has explanatory comments
- [ ] README updated if structure changed
- [ ] No orphaned TODOs
- [ ] Examples work and are accurate
