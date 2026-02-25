# Standards Library

Reusable coding, commit, architecture, tooling, and documentation standards that can be copied to any project.

## Quick Start

1. Copy this entire `/standards/` directory to your project root
2. Read each document and adapt the examples to your tech stack
3. Copy templates from `/standards/templates/` to your project root
4. Reference these standards in your project's main README

## Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [CODING-STANDARDS.md](CODING-STANDARDS.md) | Code organization, file limits, layering, language-specific guidelines | Setting up any new codebase |
| [TESTING-STANDARDS.md](TESTING-STANDARDS.md) | Test organization, naming, coverage, verification layers | Writing maintainable tests |
| [COMMIT-STANDARDS.md](COMMIT-STANDARDS.md) | Git workflow, conventional commits, agent footers | Any project using version control |
| [ARCHITECTURE-PATTERNS.md](ARCHITECTURE-PATTERNS.md) | System design patterns, process coordination, schema migration, infrastructure resilience | Multi-layer, client-server, or service-oriented apps |
| [TOOLING-STANDARDS.md](TOOLING-STANDARDS.md) | Linting, hooks, automation | Enforcing code quality |
| [DOCUMENTATION-STANDARDS.md](DOCUMENTATION-STANDARDS.md) | README requirements, comments, algorithm docs | Maintaining readable codebases |
| [SECURITY-STANDARDS.md](SECURITY-STANDARDS.md) | Boundary validation, path safety, input sanitization, network transport safety | Apps handling user input, file paths, or local IPC |
| [CONCURRENCY-STANDARDS.md](CONCURRENCY-STANDARDS.md) | Async/threading patterns, async task lifecycle, mutex selection | Multi-threaded or async applications |
| [CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md) | Platform abstraction, file system conventions, CI matrix | Apps targeting multiple OS platforms |
| [INTEROP-STANDARDS.md](INTEROP-STANDARDS.md) | FFI safety, cross-language boundaries, contract maintenance | Multi-language or native interop projects |
| [DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md) | Dependency evaluation, versioning, auditing, and minimization | Adding or reviewing third-party packages |
| [LANGUAGE-BINDINGS-STANDARDS.md](LANGUAGE-BINDINGS-STANDARDS.md) | Binding architecture, FFI wrapper design, code generation, type mapping | Exposing a core library to multiple target languages |
| [RELEASE-STANDARDS.md](RELEASE-STANDARDS.md) | Versioning, changelogs, release artifacts, CI/CD release pipelines | Shipping software to users or downstream consumers |
| [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) | Semantic HTML, keyboard interaction, ARIA, a11y linting | UI components in web or desktop apps |

## Templates

Ready-to-use configuration files in `/templates/`:

| Template | Purpose |
|----------|---------|
| [README-TEMPLATE.md](templates/README-TEMPLATE.md) | Directory documentation template |
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
