# Release Standards

Release applicability, versioning, changelog, contract-evolution, deprecation,
migration, and acceptance policy moved to the canonical
[Release Workflow](workflows/release.md).

This file temporarily retains only unmigrated rollback and tool-recipe
guidance. These sections cannot override the canonical workflow.

## Release Tool Recipes (Pending Reference Migration)

### Changelog Automation

[git-cliff](https://git-cliff.org/) is recommended for generating changelogs
from conventional commits. It is config-driven and supports custom templates.

```toml
# cliff.toml (minimal)
[changelog]
header = """# Changelog\n
All notable changes to this project will be documented in this file.\n"""
body = """
{% if version %}\
    ## [{{ version }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}\
    ## [Unreleased]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | upper_first }}
    {% for commit in commits %}
        - {{ commit.message | upper_first }}\
    {% endfor %}
{% endfor %}\n
"""
trim = true

[git]
conventional_commits = true
commit_parsers = [
    { message = "^feat", group = "Added" },
    { message = "^fix", group = "Fixed" },
    { message = "^perf", group = "Changed" },
    { message = "^refactor", group = "Changed" },
    { message = "^deprecated", group = "Deprecated" },
    { message = "^doc", skip = true },
    { message = "^style", skip = true },
    { message = "^test", skip = true },
    { message = "^chore", skip = true },
    { message = "^ci", skip = true },
]
```

---

## Rollback Procedure

### When to Rollback

- Critical regression discovered after publishing
- Broken or corrupt artifacts
- Security vulnerability introduced by the release

### Procedure

1. **Unpublish** — Revert the GitHub Release to draft. On package registries
   (crates.io, npm, PyPI), yank the affected version
2. **Notify** — If the release was public for any duration, inform users through
   the project's standard channels (issue tracker, release notes, etc.)
3. **Fix** — Address the issue on `main` or via a hotfix branch (see
   [Hotfix Workflow](#hotfix-workflow))
4. **Re-release** — Publish a new patch version with the fix. Never reuse a
   yanked version number

### Authority

The release owner or any maintainer with release permissions may initiate a
rollback. Speed matters — do not wait for consensus when artifacts are broken.

### Post-Incident

Add a brief post-mortem note to the changelog or release notes explaining what
went wrong and what was done to prevent recurrence.
