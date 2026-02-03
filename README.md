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
| [CODING-STANDARDS.md](CODING-STANDARDS.md) | Code organization, file limits, layering | Setting up any new codebase |
| [COMMIT-STANDARDS.md](COMMIT-STANDARDS.md) | Git workflow, conventional commits | Any project using version control |
| [ARCHITECTURE-PATTERNS.md](ARCHITECTURE-PATTERNS.md) | System design patterns | Multi-layer or client-server apps |
| [TOOLING-STANDARDS.md](TOOLING-STANDARDS.md) | Linting, hooks, automation | Enforcing code quality |
| [DOCUMENTATION-STANDARDS.md](DOCUMENTATION-STANDARDS.md) | README requirements, comments | Maintaining readable codebases |

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
