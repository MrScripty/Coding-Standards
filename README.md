# Standards Library

Reusable engineering standards with routed workflows, profiles, topics, and
reference material.

## Quick Start

1. Read [Core Standards](CORE-STANDARDS.md).
2. Use the [Standards Router](STANDARDS-ROUTER.md) to select only applicable
   workflows, profiles, and topics.
3. Record project-specific contracts and exceptions in the adopting
   repository.
4. Copy a template or tool only when routed guidance requires it.
5. Reference the adopted standards version in the project's main README.

## Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [CORE-STANDARDS.md](CORE-STANDARDS.md) | Universal ownership, boundary, failure, lifecycle, quality, and verification invariants | Every adopted project |
| [STANDARDS-ROUTER.md](STANDARDS-ROUTER.md) | Applicability, exclusions, dependency routing, and migration authority | Start of every task |
| [workflows/implementation.md](workflows/implementation.md) | Bounded implementation slices and commit boundary | Any repository change |
| [workflows/commit.md](workflows/commit.md) | Atomic commits, branch review, and explicit history-rewrite authority | Commit creation or history maintenance |
| [workflows/planning.md](workflows/planning.md) | Active plans, lifecycle, re-planning, and delegated ownership | Multi-step or high-risk work |
| [workflows/verification.md](workflows/verification.md) | Objective-aligned evidence selection | Any acceptance claim |
| [workflows/documentation.md](workflows/documentation.md) | Proportional durable documentation and traceability profiles | Responsibility, decision, contract, or operational-boundary changes |
| [workflows/release.md](workflows/release.md) | Release applicability, versioning, changelog, contract, and acceptance boundaries | Shipping artifacts or changing published promises |
| [reference/recipes/commits.md](reference/recipes/commits.md) | Non-normative staging and conventional commit examples | Formatting a commit after the workflow has selected process rules |
| [reference/recipes/documentation.md](reference/recipes/documentation.md) | Non-normative comment, Markdown, public-interface, and algorithm examples | Applying a selected documentation requirement |
| [topics/contracts.md](topics/contracts.md) | Contract classes, migration, compatibility, degraded outcomes, and typed unavailability | Contract or persisted-state evolution and fallback decisions |
| [profiles/applications/library.md](profiles/applications/library.md) | Reusable library ownership and consumer conditions | Library/package changes |
| [profiles/languages/rust/README.md](profiles/languages/rust/README.md) | Rust mechanisms and focused verification | Rust-owned changes |
| [CODING-STANDARDS.md](CODING-STANDARDS.md) | Code organization, simplicity/complection guidance, layering, service independence, runtime wiring guidance | Setting up any new codebase |
| [TESTING-STANDARDS.md](TESTING-STANDARDS.md) | Test placement strategy, naming, coverage, vertical slices, and cross-layer verification guidance | Writing maintainable tests |
| [COMMIT-STANDARDS.md](COMMIT-STANDARDS.md) | Migration index, conventional commit syntax, and message examples | Existing links and commit-message reference |
| [ARCHITECTURE-PATTERNS.md](ARCHITECTURE-PATTERNS.md) | System design patterns, monorepo package roles, executable contracts, composition roots, and resilient workflow coordination | Multi-layer, client-server, monorepo, or service-oriented apps |
| [TOOLING-STANDARDS.md](TOOLING-STANDARDS.md) | Linting, hooks, automation | Enforcing code quality |
| [FRONTEND-STANDARDS.md](FRONTEND-STANDARDS.md) | Declarative rendering, UI synchronization, frontend testing/tooling conventions | Web, desktop UI, and component-heavy frontend codebases |
| [DOCUMENTATION-STANDARDS.md](DOCUMENTATION-STANDARDS.md) | Migration index for canonical documentation, release, and recipe owners | Existing links only |
| [SECURITY-STANDARDS.md](SECURITY-STANDARDS.md) | Boundary validation, path safety, input sanitization, network transport safety | Apps handling user input, file paths, or local IPC |
| [CONCURRENCY-STANDARDS.md](CONCURRENCY-STANDARDS.md) | Async/threading patterns, async task lifecycle, mutex selection | Multi-threaded or async applications |
| [CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md) | Platform abstraction, file system conventions, CI matrix | Apps targeting multiple OS platforms |
| [INTEROP-STANDARDS.md](INTEROP-STANDARDS.md) | FFI safety, cross-language boundaries, contract maintenance | Multi-language or native interop projects |
| [DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md) | Dependency evaluation, versioning, auditing, and minimization | Adding or reviewing third-party packages |
| [PLAN-STANDARDS.md](PLAN-STANDARDS.md) | Migration index for planning guidance | Existing links only |
| [LAUNCHER-STANDARDS.md](LAUNCHER-STANDARDS.md) | `launcher.sh` contract, lifecycle flags, dependency checks, and app startup | Standardizing app entry points and setup workflows |
| [LANGUAGE-BINDINGS-STANDARDS.md](LANGUAGE-BINDINGS-STANDARDS.md) | Binding architecture, FFI wrapper design, code generation, type mapping | Exposing a core library to multiple target languages |
| [RELEASE-STANDARDS.md](RELEASE-STANDARDS.md) | Migration index with rollback and tool guidance pending consolidation | Unmigrated release concerns only |
| [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) | Semantic HTML, keyboard interaction, ARIA, a11y linting | UI components in web or desktop apps |
| [languages/README.md](languages/README.md) | Language-specific extensions to the generic standards | Rust and future language-specific rules |

## Templates

Ready-to-use configuration files in `/templates/`:

| Template | Purpose |
|----------|---------|
| [README-TEMPLATE.md](templates/README-TEMPLATE.md) | Concise boundary and contract README profiles |
| [PLAN-TEMPLATE.md](templates/PLAN-TEMPLATE.md) | Implementation plan template |
| [PULL_REQUEST_TEMPLATE.md](templates/PULL_REQUEST_TEMPLATE.md) | PR checklist for decision traceability |
| [check-decision-traceability.sh](templates/check-decision-traceability.sh) | CI/hook script to enforce README/ADR decision updates |
| [decision-traceability-map.tsv](templates/decision-traceability-map.tsv) | Project-owned decision-bearing path and artifact map |
| [lefthook.yml](templates/lefthook.yml) | Pre-commit hook configuration |
| [.editorconfig](templates/.editorconfig) | Editor formatting settings |

## Customization

These standards are intentionally generic. When adopting them:

1. **Replace placeholders** - Look for `[YOUR-...]` markers
2. **Add tech-specific rules** - Extend with language-specific conventions
3. **Define your scopes** - Map commit scopes to your project structure
4. **Configure tooling** - Adapt hook commands to your build tools

## License

These standards are provided as-is for free use in any project.
