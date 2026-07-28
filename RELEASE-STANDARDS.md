# Release Standards

Release applicability, versioning, changelog, contract-evolution, deprecation,
migration, and acceptance policy moved to the canonical
[Release Workflow](workflows/release.md).

This file temporarily retains only unmigrated maintenance/channel,
hosted-publication, checklist, rollback, and tool-recipe guidance. These
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

---

## Hotfix and LTS Workflow

### Standard Releases

Standard releases use the project's adopted maintenance policy and dispatch the
canonical release pipeline from an accepted immutable source reference.

### Hotfix Workflow

When a critical bug or security vulnerability is found in an already-released
version, create a hotfix branch from the release tag:

1. Branch from the tag: `git checkout -b hotfix/vX.Y.Z vX.Y.0` (where `vX.Y.0`
   is the affected release tag)
2. Apply the fix on the hotfix branch
3. Update the changelog and bump the patch version
4. Tag the fix: `git tag vX.Y.1`
5. Push the branch and release reference; dispatch the canonical pipeline
6. Cherry-pick or merge the fix back into `main` to ensure it is not lost

### LTS Releases

Only releases explicitly labeled as **LTS** (Long-Term Support) receive a
long-lived release branch. Non-LTS releases are tagged only.

- Create a release branch at the LTS tag: `release/X.Y`
- LTS branches receive backported bug fixes and security patches
- LTS branches follow the same canonical pipeline dispatch contract
- Document the LTS support window in the project README (e.g., "12 months of
  security patches from the LTS release date")

---

## Feature Flags and Release Channels

For applications (desktop apps, servers, CLI tools), consider staged rollouts to
reduce release risk:

- **Release channels** (`stable`, `beta`, `nightly`) allow early adopters to
  test upcoming changes before they reach the general user base
- **Feature flags** decouple deployment from release — ship code behind a flag,
  enable it separately from the binary release
- Flags should be short-lived; treat unremoved flags as technical debt with a
  cleanup deadline

These mechanisms are primarily applicable to applications. Library releases
typically do not need feature flags or release channels.

---

## GitHub Releases

### Draft-Then-Publish

CI creates draft releases. A human reviews artifacts and release notes before
publishing. This prevents broken releases from being visible to users.

Protect whichever references or approvals authorize release dispatch;
convention alone is insufficient. When team size allows, the reviewer who
publishes the draft should not be the same actor who authorized the candidate.

### Pre-Release Flag

Set the hosting service's prerelease flag only when the accepted version has a
prerelease identifier or the release channel contract explicitly classifies
the artifact as prerelease. Major version zero alone is not that decision.

### Release Notes

Use the changelog entry for the released version as the release body. GitHub's
auto-generated release notes (from PR titles) are acceptable as a supplement
but should not replace a curated changelog.

For major version bumps, include or link the migration guide in the release
notes.

### Asset Organization

Present assets using the identities and relationships selected by the
canonical artifact plan. Group related assets in the release description when
that helps consumers select the correct download; do not invent a second naming
scheme in publication automation.

---

## Language-Specific Guidance

Rust release rules for Cargo metadata, `publish = false`, workspace versioning,
toolchain pinning, and `cargo-release` live in
[languages/rust/RUST-RELEASE-STANDARDS.md](languages/rust/RUST-RELEASE-STANDARDS.md).

---

## Release Checklist

Before every release:

1. Complete the canonical
   [Release Workflow](workflows/release.md) version, changelog, contract, and
   acceptance decisions.
2. Dependency audit shows no unaccepted high/critical vulnerabilities (e.g., `cargo audit`,
   `npm audit`, `pip-audit`)
3. Commit: `chore(release): prepare vX.Y.Z`
4. Tag: `git tag vX.Y.Z`
5. Push commit and intended release tag.
6. CI creates draft GitHub Release; verify all expected artifacts are present.
7. Download the representative published artifacts required by the acceptance
    plan and run each named `release-artifact` smoke criterion
8. Review release notes, then publish the release

For dependency security auditing in CI, see
[DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md#ci-integration).

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
