# Documentation Standards

Requirements for maintaining readable, navigable codebases.

## Documentation Selection

The [Documentation Workflow](workflows/documentation.md) is the canonical owner
for deciding when durable documentation is required and which profile applies.
This file retains changelog guidance until its release-owned consolidation
slice completes.

Do not infer a README requirement from directory count, file count, or a `src/`
path. Require documentation only for an affected durable responsibility,
decision, contract, or operational procedure.

## Code And Markdown Examples

Comment, Markdown, public-interface, and algorithm examples moved to the
non-normative
[Documentation Recipe](reference/recipes/documentation.md).

The [Documentation Workflow](workflows/documentation.md) remains the canonical
owner for deciding when durable documentation is required. Language profiles,
project formatters, and consumer contracts own their specific syntax and
behavior; this migration index does not impose a universal TODO format, table
alignment, public-symbol documentation rule, or algorithm template.

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
