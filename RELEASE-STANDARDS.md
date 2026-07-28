# Release Standards

Release applicability, versioning, changelog, contract-evolution, deprecation,
migration, and acceptance policy moved to the canonical
[Release Workflow](workflows/release.md).

This file temporarily retains only unmigrated tool-recipe guidance. These
sections cannot override the canonical workflow.

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
