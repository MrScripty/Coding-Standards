# Release Recipe

**Standards metadata**

- ID: `reference.recipes.releases`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A selected changelog automation tool needs an illustrative configuration.
- Does not apply when: Release policy, changelog categories, commit conventions, or tool selection are being decided.
- Requires: `workflow.release`
- Specializes: `none`
- Verification: Release-reference dispositions, metadata, and link checks.
- Canonical owner: `reference/recipes/releases.md`

This recipe illustrates the [Release Workflow](../../workflows/release.md). It
does not require git-cliff, Conventional Commits, these changelog categories,
or this template. Projects select tooling and configuration from their release
contract and should verify current tool syntax before adopting an example.

## Git-Cliff Example

```toml
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
