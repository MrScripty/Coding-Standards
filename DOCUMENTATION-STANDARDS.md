# Documentation Standards

Requirements for maintaining readable, navigable codebases.

## Directory Documentation

### Requirement

**Every directory under `src/` (or equivalent source folders) must contain a `README.md` file.**

Outside source folders, directories with 3+ files or non-obvious purpose should contain a `README.md` file.

If rules overlap, enforce the stricter requirement. For `src/`, the universal requirement takes precedence.

### Why

- **Discoverability:** New developers understand structure without reading code
- **Onboarding:** Reduces time to first contribution
- **Maintenance:** Prevents architectural drift

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

See [templates/README-TEMPLATE.md](templates/README-TEMPLATE.md) for a copy-paste template.

Required sections:

```markdown
# [Directory Name]

## Purpose
One paragraph explaining what this directory contains and why it exists.

## Contents
| File/Folder | Description |
|-------------|-------------|
| `file.ts` | Brief description |
| `subfolder/` | Brief description |

## Problem
What problem this directory solves at the system level.

## Constraints
Technical and product constraints that shaped the design.

## Decision
Chosen approach and why it was selected.

## Alternatives Rejected
- Option A: Why rejected
- Option B: Why rejected

## Invariants
- Invariant 1 that must remain true
- Invariant 2 that must remain true

## Revisit Triggers
- Concrete conditions that should trigger reconsideration

## Dependencies
**Internal:** What other parts of the codebase this depends on
**External:** Third-party libraries used

## Related ADRs
- `ADR-00X` brief description
- Or, if there are no related ADRs:
- `None identified as of YYYY-MM-DD.`
- `Reason: <why no ADR currently applies>`
- `Revisit trigger: <event that should force ADR creation or linkage>`

## Usage Examples
Code snippets showing how to use components in this directory.

## API Consumer Contract
- Supported inputs and outputs
- Lifecycle and ordering expectations
- Error behavior and retry guidance
- Compatibility/versioning notes for clients

## Structured Producer Contract
- Stable fields and shape expectations
- Default semantics when fields are omitted
- Enum semantics and label/value meanings
- Compatibility expectations for persisted consumers or saved artifacts
- Regeneration or migration rules when the contract changes
```

### Required Section Completion Rule

Every required section must contain one of:

- Concrete project-specific content, or
- An explicit `None` statement with:
  - `Reason:` why content is currently absent
  - `Revisit trigger:` what event should prompt re-evaluation

This rule prevents fabricated rationale while still preserving future
traceability.

Example:

```markdown
## Alternatives Rejected
- None identified as of 2026-03-05.
- Reason: This module is a thin adapter over a fixed upstream contract.
- Revisit trigger: A second viable adapter strategy appears.
```

### Banned Placeholder Language

Do not use generic filler that can be inferred from file names or directory
structure.

Examples that are not acceptable:

- `Source file used by modules in this directory.`
- `Subdirectory containing related implementation details.`
- `Keep files in this directory scoped to a single responsibility boundary.`
- `import { value } from './module';`

If a sentence could be reused unchanged in unrelated directories, rewrite it
with module-specific rationale.

### Host-Facing Module Contract Requirement

When a directory exposes functionality consumed by external callers (API
clients, plugins, bindings, SDK consumers, or other process boundaries), its
README must include `## API Consumer Contract` with:

- Expected request/input shape and validation expectations
- Response/output shape, including stable fields
- Lifecycle and ordering constraints (init, shutdown, retry, idempotency)
- Error semantics, retry/backoff expectations, and timeout behavior
- Compatibility policy (versioning, deprecations, and migration notes)

### Structured Producer Contract Requirement

When a directory publishes machine-consumed metadata, configuration, schemas,
templates, manifests, or other structured artifacts, its README must include
`## Structured Producer Contract` with:

- Stable fields and which fields are intentionally volatile
- Default semantics when fields are absent
- Enum meanings and label/value mappings where relevant
- Ordering guarantees where consumers rely on order
- Compatibility expectations for persisted consumers and saved artifacts
- Regeneration or migration rules when the contract changes

### Minimum Meaningful Content by Section

| Section | Minimum Content |
| ------- | --------------- |
| `Purpose` | Responsibility and why the directory boundary exists. |
| `Contents` | Key artifacts only (typically 3-7). Explain why each matters; do not list every file by default. |
| `Problem` | System-level problem being solved and affected actors. |
| `Constraints` | Real constraints (technical, product, compatibility, operational). |
| `Decision` | Chosen approach and rationale tied to constraints. |
| `Alternatives Rejected` | At least one rejected option with reason, or explicit `None` with reason and revisit trigger. |
| `Invariants` | Conditions that must remain true for correctness (testable where possible). |
| `Revisit Triggers` | Concrete events/thresholds that should force re-evaluation. |
| `Dependencies` | Significant internal/external dependencies and why they are needed. |
| `Usage Examples` | One realistic usage example that reflects actual entry points. |
| `API Consumer Contract` | Required for host-facing modules; include lifecycle, failures, and compatibility behavior. |
| `Structured Producer Contract` | Required for machine-consumed metadata/config/schema producers; include semantics, persistence compatibility, and regeneration rules. |

### Keeping READMEs Current

- Update README when adding/removing files
- Update when architecture changes
- Every PR that changes `src/<module>/` code must do one of:
  - update that module's `README.md`, or
  - add/update an ADR under `docs/adr/`
- README updates must capture design reasoning (`Problem`, `Constraints`,
  `Decision`, `Alternatives Rejected`) not only file listings

---

## Code Comments

### When to Comment

**Comment the "why", not the "what".**

```typescript
// BAD: Describes what code does (obvious from reading it)
// Loop through users and filter active ones
const active = users.filter(u => u.isActive);

// GOOD: Explains why this approach
// Filter before mapping to avoid expensive transformations on inactive users
const active = users.filter(u => u.isActive);
```

### When NOT to Comment

- Self-explanatory code
- Code that could be made self-explanatory by renaming
- Temporary notes (use TODO with ticket number)

```typescript
// BAD: Comment that could be code
// Check if user is admin
if (user.role === 'admin') { ... }

// GOOD: Self-documenting
if (user.isAdmin()) { ... }
```

### TODO Format

```typescript
// TODO(#123): Refactor when new API is available
// TODO(@username): Discuss approach in next sync
```

Always include:
- Ticket number, OR
- Owner/author, OR
- Date when it should be addressed

**Never:** Orphaned TODOs without context

### Comment Style

Use your language's standard doc comment format:

```typescript
// TypeScript/JavaScript - JSDoc
/**
 * Calculates the total price including tax.
 * @param items - Cart items to total
 * @param taxRate - Tax rate as decimal (0.08 for 8%)
 * @returns Total price with tax applied
 */
function calculateTotal(items: Item[], taxRate: number): number
```

```python
# Python - Docstring
def calculate_total(items: list[Item], tax_rate: float) -> float:
    """
    Calculate the total price including tax.

    Args:
        items: Cart items to total
        tax_rate: Tax rate as decimal (0.08 for 8%)

    Returns:
        Total price with tax applied
    """
```

---

## Markdown Formatting

### Fenced Code Blocks

Always specify a language identifier on fenced code blocks so renderers apply
syntax highlighting:

````markdown
```text
example code or command output
```
````

Use `text` as the language for plain-text blocks that have no specific syntax.

### Tables

Use standard markdown table syntax so tables render correctly in all viewers.
The separator row must use dashes with single-space padding that match the
header cell widths:

```markdown
| Name | Description |
| ---- | ----------- |
| foo  | Does X      |
| bar  | Does Y      |
```

Rules:

- Separator dashes must match the header column width (one space of padding on
  each side of the dashes)
- All rows in a table must use the same column widths — pad shorter cells with
  trailing spaces
- Do not omit leading or trailing pipes

---

## API Documentation

### Public Interfaces

All public functions, classes, and types should be documented:

```typescript
/**
 * User authentication service.
 *
 * Handles login, logout, and session management.
 *
 * @example
 * const auth = new AuthService(config);
 * const session = await auth.login(credentials);
 */
export class AuthService {
    /**
     * Authenticate user with credentials.
     *
     * @param credentials - Username and password
     * @returns Session token if successful
     * @throws AuthError if credentials invalid
     */
    async login(credentials: Credentials): Promise<Session>
}
```

### What to Document

| Element | Document? | Include |
|---------|-----------|---------|
| Public function | Yes | Purpose, params, return, throws, example |
| Public class | Yes | Purpose, usage example |
| Public type/interface | Yes | Purpose, when to use |
| Private/internal | Optional | Only if complex |
| Obvious getters/setters | No | |

---

## Algorithm Documentation

For non-trivial algorithms, provide comprehensive documentation:

### Required Elements

```markdown
# Topological Sort Algorithm

Produces a linear ordering of nodes such that for every directed edge `(u, v)`,
`u` comes before `v` in the ordering.

## Reference
Based on Kahn's algorithm (1962).

## Preconditions
- Graph is a DAG with no cycles.
- All node IDs are valid.

## Postconditions
- Output contains every node exactly once.
- For every edge `(u, v)`, `index(u) < index(v)`.

## Complexity
- Time: `O(V + E)` where `V` = vertices and `E` = edges.
- Space: `O(V)` for in-degree tracking.

## Error Cases
Returns a cycle error when the graph contains a cycle or self-referencing edge.
```

### When to Document Algorithms

Document comprehensively when:

- **Complexity is non-obvious** - O(n²) or worse, or subtle constant factors
- **Based on academic papers** - Include citation and any modifications
- **Adapted from reference implementations** - Include attribution
- **Maintains critical invariants** - Document what must remain true
- **Has non-trivial preconditions** - Caller needs to know requirements

### Minimal Documentation

For simpler algorithms, at minimum include:

```markdown
Sort records by priority score, highest first.

## Complexity
`O(n log n)` where `n` = record count.
```

### ASCII Diagrams

Use ASCII art to illustrate transformations:

```text
Rebalance a binary search tree after insertion.

Before (unbalanced):     After (balanced):
    A                        B
     \                      / \
      B                    A   C
       \
        C
```

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
