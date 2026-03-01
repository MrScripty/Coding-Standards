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
- `ADR-00X` brief description (or "None")

## Usage Examples
Code snippets showing how to use components in this directory.
```

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
```rust
fn main() {}
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

```rust
/// # Topological Sort Algorithm
///
/// Produces a linear ordering of nodes such that for every directed
/// edge (u, v), u comes before v in the ordering.
///
/// ## Reference
/// Based on Kahn's algorithm (1962)
/// See: Kahn, A.B., "Topological sorting of large networks"
///
/// ## Algorithm
/// ```text
///     Input graph:          Output order:
///       A → B → D           [A, C, B, E, D, F]
///       A → C → E
///       B → E → F
/// ```
///
/// ## Preconditions
/// - Graph is a DAG (no cycles)
/// - All node IDs are valid
///
/// ## Postconditions
/// - Output contains every node exactly once
/// - For every edge (u, v): index(u) < index(v)
///
/// ## Complexity
/// - Time: O(V + E) where V = vertices, E = edges
/// - Space: O(V) for in-degree tracking
///
/// ## Error Cases
/// Returns `Err(CycleDetected)` if:
/// - Graph contains a cycle
/// - Graph has self-referencing edges
pub fn topological_sort(graph: &Graph) -> Result<Vec<NodeId>, CycleError>
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

```rust
/// Sort records by priority score, highest first.
///
/// ## Complexity
/// O(n log n) where n = record count
pub fn sort_by_priority(records: &mut [Record])
```

### ASCII Diagrams

Use ASCII art to illustrate transformations:

```rust
/// Rebalance a binary search tree after insertion.
///
/// ```text
///     Before (unbalanced):     After (balanced):
///         A                        B
///          \                      / \
///           B                    A   C
///            \
///             C
/// ```
pub fn rebalance(tree: &mut BinaryTree) -> &mut Node
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
