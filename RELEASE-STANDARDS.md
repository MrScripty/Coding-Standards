# Release Standards

Release applicability, versioning, changelog, contract-evolution, deprecation,
migration, and acceptance policy moved to the canonical
[Release Workflow](workflows/release.md).

This file temporarily retains only unmigrated pipeline/publication,
channel/download, checklist, rollback, and tool-recipe guidance. These sections
cannot override the canonical workflow.

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

## CI/CD Release Pipeline

### Trigger

Pushing a `v*` tag (e.g., `v0.2.0`) triggers the release pipeline. Regular
pushes and PRs run build + test only.

Release automation must be constrained by tag triggers so ordinary branch pushes
cannot run packaging, signing, publishing, or draft-release creation by accident.
Keep release workflows separate from regular CI when possible:

```yaml
# .github/workflows/release.yml
on:
  push:
    tags: ['v*']
```

Regular CI should stay on branch pushes and pull requests:

```yaml
# .github/workflows/ci.yml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

If a single workflow handles both CI and release jobs, every release job must
still use an explicit tag condition such as:

```yaml
if: startsWith(github.ref, 'refs/tags/v')
```

Path filters may reduce irrelevant validation work, but they must not be the
primary release guard. Protected-branch required checks must still appear
consistently when path filters skip a workflow.

### Build Matrix

The build matrix must include all **required** platforms from
[CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md#platform-targets).
Best-effort platforms are optional.

```yaml
# Target values come from the canonical artifact plan.
strategy:
  fail-fast: false
  matrix:
    include:
      - os: ubuntu-latest
        target: x86_64-unknown-linux-gnu
      - os: windows-latest
        target: x86_64-pc-windows-msvc
      - os: macos-latest
        target: aarch64-apple-darwin
```

**Note:** `macos-latest` on GitHub Actions uses ARM (M-series) runners. For
Intel macOS targets, use `macos-13` (the last Intel runner generation).

### Artifact Upload

Upload the distributable artifacts selected by the canonical
[Release Workflow](workflows/release.md#artifact-plan). Use its artifact
identity in upload names to avoid collisions between matrix entries:

```yaml
- name: Upload artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-${{ matrix.target }}
    path: |
      path/to/binary
      path/to/shared-library
    if-no-files-found: ignore
```

### Release Job

A separate release job runs only on tag pushes, after all build jobs pass:

```yaml
release:
  if: startsWith(github.ref, 'refs/tags/v')
  needs: [build]
  runs-on: ubuntu-latest
  permissions:
    contents: write
```

The release job should consume the accepted artifact plan:

1. Download all build artifacts
2. Apply the planned artifact identities
3. Generate the selected integrity, provenance, and dependency metadata
4. Create a draft release with the complete planned artifact set attached

```yaml
- name: Extract version
  id: version
  run: echo "version=${GITHUB_REF_NAME#v}" >> $GITHUB_OUTPUT

- name: Create release
  uses: softprops/action-gh-release@v2
  with:
    files: release-artifacts/*
    draft: true
    generate_release_notes: true
    prerelease: ${{ startsWith(github.ref_name, 'v0.') }}
```

### Code Signing

When the canonical artifact plan requires signatures, notarization, or
provenance, the release pipeline must produce and verify that metadata for the
final artifacts. Version maturity does not waive consumer, channel,
organizational, or regulatory requirements.

For supply chain maturity goals, see [SLSA](https://slsa.dev/) — Level 2+
requires signed build provenance.

---

## Hotfix and LTS Workflow

### Standard Releases

Standard (non-LTS) releases are tagged on `main`. No release branch is created.
The tag triggers the CI/CD pipeline, which builds and publishes artifacts.

### Hotfix Workflow

When a critical bug or security vulnerability is found in an already-released
version, create a hotfix branch from the release tag:

1. Branch from the tag: `git checkout -b hotfix/vX.Y.Z vX.Y.0` (where `vX.Y.0`
   is the affected release tag)
2. Apply the fix on the hotfix branch
3. Update the changelog and bump the patch version
4. Tag the fix: `git tag vX.Y.1`
5. Push the branch and tag — CI builds from the tag as usual
6. Cherry-pick or merge the fix back into `main` to ensure it is not lost

### LTS Releases

Only releases explicitly labeled as **LTS** (Long-Term Support) receive a
long-lived release branch. Non-LTS releases are tagged only.

- Create a release branch at the LTS tag: `release/X.Y`
- LTS branches receive backported bug fixes and security patches
- LTS branches follow the same CI pipeline, triggered by `v*` tags
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

Restrict `v*` tag push permissions to designated maintainers via tag protection
rules — convention alone is insufficient. When team size allows, the reviewer
who publishes the draft should not be the same person who created the tag.

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
