# Release Standards

Versioning, changelog management, artifact packaging, and CI/CD release pipelines.

## Semantic Versioning

All versioned software must follow [Semantic Versioning 2.0.0](https://semver.org/).

### Version Bump Decision Table

| Change Type | Bump | Examples |
| ----------- | ---- | -------- |
| Breaking API change | Major | Remove public function, change return type, rename exported struct |
| New backward-compatible functionality | Minor | Add public function, new optional parameter, new feature |
| Backward-compatible bug fix | Patch | Fix incorrect behavior, fix crash, correct error message |
| Internal refactoring (no public API change) | Patch or none | Rename private module, restructure internals |

### Pre-1.0 Rules

While at `0.x.y`, minor version bumps may include breaking changes. This is
standard SemVer behavior — `0.x` signals instability.

```text
0.1.0 → 0.2.0   May include breaking changes
0.2.0 → 0.2.1   Bug fixes only
1.0.0 → 1.1.0   New features, no breaking changes
1.1.0 → 2.0.0   Breaking changes
```

Document all breaking changes in the changelog regardless of version.

### Deprecation Policy

Deprecated features must follow a structured timeline before removal:

1. **Announce** — Record the deprecation in the changelog under the `Deprecated`
   category. Include what is deprecated, why, and what replaces it
2. **Warn** — Emit warnings at the point of use (compiler warnings, runtime
   warnings, or linter rules) so consumers discover the deprecation without
   reading the changelog
3. **Grace period** — Maintain the deprecated API for at least one full minor
   version cycle after the announcement (or longer if the project documents a
   specific policy)
4. **Remove** — Remove the deprecated API in a major version bump. Record the
   removal in the changelog under the `Removed` category with a reference to the
   version that originally deprecated it

For pre-1.0 software, deprecation may be shortened or skipped since `0.x`
already signals instability, but a changelog entry is still required.

### Migration Guides

Every major version bump that introduces breaking changes must include a
migration guide. The guide should cover:

- What changed and why
- Before/after code examples
- Step-by-step upgrade path
- Any automated migration tooling available (codemods, scripts, etc.)

Link the migration guide from both the changelog entry and the GitHub Release
notes. Migration guides may be a section within the release notes or a separate
document (e.g., `MIGRATION-v2.md`) depending on scope.

For pre-1.0 breaking changes, include migration notes inline in the changelog
entry rather than a separate guide.

### Workspace Version Alignment

When using workspace-level versioning (e.g., a monorepo with a shared version
field), all member packages share a version and are released together.

If a project has multiple manifest files, keep versions synchronized across all
of them.

---

## Changelog Management

For full changelog formatting rules, see
[DOCUMENTATION-STANDARDS.md](DOCUMENTATION-STANDARDS.md#changelog). This section
covers the workflow for maintaining and automating changelogs.

### Maintenance Workflow

1. Every PR that adds user-visible changes updates the `[Unreleased]` section
2. At release time, rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`
3. Add a fresh empty `[Unreleased]` section above it

### Conventional Commits to Changelog Categories

When using [conventional commits](COMMIT-STANDARDS.md), map commit types to
changelog categories:

| Commit Type | Changelog Category |
| ----------- | ------------------ |
| `feat` | Added |
| `fix` | Fixed |
| `perf` | Changed |
| `refactor` (user-visible) | Changed |
| `deprecated` | Deprecated |
| `BREAKING CHANGE` footer (removal) | Removed |
| `BREAKING CHANGE` footer (other) | Changed (with migration note) |
| Security fix (noted in commit body/footer) | Security |
| `docs`, `chore`, `ci`, `style`, `test` | Omit (internal-only) |

These six categories (Added, Changed, Deprecated, Removed, Fixed, Security)
match the [Keep a Changelog](https://keepachangelog.com/) specification.

### Automation

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

## Release Artifacts

### What to Ship

| Artifact Type | When | Example |
| ------------- | ---- | ------- |
| Binary executables | Project produces CLI tools or servers | `my-server`, `my-server.exe` |
| Shared libraries | Project produces native libraries | `libfoo.so`, `foo.dll`, `libfoo.dylib` |
| Desktop applications | Project produces GUI apps | `.AppImage`, `.deb`, `.exe`, `.dmg` |
| SHA256 checksums | Always | `checksums-sha256.txt` |
| SBOM | Recommended for all releases | `my-tool-1.0.0-sbom.cdx.json` |
| Source archives | Not needed — GitHub generates these automatically for tagged releases | |

### Naming Convention

Include version and platform target in every artifact filename. This is required
because GitHub Release assets are flat (no subdirectories), and users need to
identify the correct download.

**Pattern:** `{name}-{version}-{target}[.ext]`

Target naming varies by ecosystem. Use your toolchain's native convention:

| Ecosystem | Example Target |
| --------- | -------------- |
| Rust | `x86_64-unknown-linux-gnu` |
| Go | `linux-amd64` |
| Node | `linux-x64` |
| Python | `manylinux_x86_64` |

| Artifact Type | Naming Pattern | Example |
| ------------- | -------------- | ------- |
| Binary (Linux) | `{name}-{version}-{target}` | `my-tool-0.2.0-x86_64-unknown-linux-gnu` |
| Binary (Windows) | `{name}-{version}-{target}.exe` | `my-tool-0.2.0-x86_64-pc-windows-msvc.exe` |
| Binary (macOS) | `{name}-{version}-{target}` | `my-tool-0.2.0-aarch64-apple-darwin` |
| Shared lib (Linux) | `lib{name}-{version}-{target}.so` | `libmy_lib-0.2.0-x86_64-unknown-linux-gnu.so` |
| Shared lib (Windows) | `{name}-{version}-{target}.dll` | `my_lib-0.2.0-x86_64-pc-windows-msvc.dll` |
| Shared lib (macOS) | `lib{name}-{version}-{target}.dylib` | `libmy_lib-0.2.0-aarch64-apple-darwin.dylib` |
| Desktop app (Linux) | `{AppName}-{version}.AppImage` | `MyApp-0.2.0.AppImage` |
| Desktop app (Windows) | `{AppName}-Setup-{version}.exe` | `MyApp-Setup-0.2.0.exe` |
| Desktop app (macOS) | `{AppName}-{version}.dmg` | `MyApp-0.2.0.dmg` |
| Checksums | `checksums-sha256.txt` | `checksums-sha256.txt` |

For platform naming conventions for shared libraries (prefix, extension), see
[CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md#library-naming).

### Checksum File Format

Generate a single `checksums-sha256.txt` containing SHA256 hashes of all release
artifacts. Use the standard two-space-separated format:

```text
b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c  my-tool-0.2.0-x86_64-unknown-linux-gnu
7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730  my-tool-0.2.0-x86_64-pc-windows-msvc.exe
```

Generate with:

```bash
sha256sum * > checksums-sha256.txt          # Linux
shasum -a 256 * > checksums-sha256.txt      # macOS
```

### Software Bill of Materials

Generate a Software Bill of Materials (SBOM) in
[CycloneDX](https://cyclonedx.org/) or [SPDX](https://spdx.dev/) format
alongside release artifacts. An SBOM lists all dependencies bundled into the
release, enabling downstream consumers to audit supply chain risk.

**Naming convention:** `{name}-{version}-sbom.cdx.json` (CycloneDX) or
`{name}-{version}-sbom.spdx.json` (SPDX).

Ecosystem-agnostic generation tools:

- [syft](https://github.com/anchore/syft) — Multi-ecosystem, generates CycloneDX and SPDX
- [trivy](https://github.com/aquasecurity/trivy) — Also performs vulnerability scanning

Include SBOM generation in the CI release pipeline alongside checksum generation.

---

## Reproducible Builds

The goal of reproducible builds is: same source + same toolchain + same
dependencies = identical artifacts, regardless of when or where the build runs.

### Toolchain Pinning

Pin the toolchain version in a project-level config file so all developers and
CI runners use the same compiler/interpreter version:

| Ecosystem | Config File | Example |
| --------- | ----------- | ------- |
| Rust | `rust-toolchain.toml` | `channel = "1.78.0"` |
| Node | `.node-version` or `.nvmrc` | `20.11.0` |
| Python | `.python-version` | `3.12.1` |
| Multi-tool | `.tool-versions` (asdf/mise) | `rust 1.78.0` |

### Lockfile Policy

Commit lockfiles for applications; omit them for libraries.

| Project Type | Commit lockfile? | Reason |
| ------------ | ---------------- | ------ |
| Application / binary | Yes | Reproducible builds |
| Library only | No | Let consumers resolve dependencies |
| Workspace with any binary | Yes | Binary reproducibility takes priority |

Examples of lockfiles by ecosystem: `Cargo.lock` (Rust), `package-lock.json` /
`yarn.lock` (Node), `poetry.lock` / `uv.lock` (Python), `go.sum` (Go).

### Build Hygiene

- Do not embed timestamps, build-host paths, or other non-deterministic metadata
  in artifacts
- Use a consistent build environment (CI runners with pinned OS images, or
  containerized builds)
- Document the minimum toolchain version required to build the project

---

## CI/CD Release Pipeline

### Trigger

Pushing a `v*` tag (e.g., `v0.2.0`) triggers the release pipeline. Regular
pushes and PRs run build + test only.

```yaml
on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]
```

### Build Matrix

The build matrix must include all **required** platforms from
[CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md#platform-targets).
Best-effort platforms are optional.

```yaml
# Target values are ecosystem-specific (see Naming Convention above)
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

Upload all distributable artifacts from the build step. Use the target
identifier in the artifact name to avoid collisions when multiple platforms build
on the same OS label:

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

The release job should:

1. Download all build artifacts
2. Rename artifacts with version and target (extract version from tag)
3. Generate `checksums-sha256.txt`
4. Generate SBOM
5. Create a draft GitHub Release with all artifacts attached

```yaml
- name: Extract version
  id: version
  run: echo "version=${GITHUB_REF_NAME#v}" >> $GITHUB_OUTPUT

- name: Generate checksums
  working-directory: release-artifacts
  run: sha256sum * > checksums-sha256.txt

- name: Create release
  uses: softprops/action-gh-release@v2
  with:
    files: release-artifacts/*
    draft: true
    generate_release_notes: true
    prerelease: ${{ startsWith(github.ref_name, 'v0.') }}
```

### Code Signing

Code signing (GPG for Linux, Authenticode for Windows, notarization for macOS)
is recommended for production releases but not required for initial or pre-1.0
releases. Add signing as a follow-up once the basic pipeline is stable.

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

Use GitHub's pre-release flag for `0.x.y` releases to signal API instability.
Users browsing releases will see the pre-release label and understand that the
API may change.

### Release Notes

Use the changelog entry for the released version as the release body. GitHub's
auto-generated release notes (from PR titles) are acceptable as a supplement
but should not replace a curated changelog.

For major version bumps, include or link the migration guide in the release
notes.

### Asset Organization

Assets should be self-describing via their filenames (see naming conventions
above). Group related assets in the release description if there are many:

```markdown
## Downloads

### Binaries
- `my-tool-1.0.0-x86_64-unknown-linux-gnu` — Linux x86_64
- `my-tool-1.0.0-x86_64-pc-windows-msvc.exe` — Windows x86_64
- `my-tool-1.0.0-aarch64-apple-darwin` — macOS ARM

### Shared Libraries
- `libmy_lib-1.0.0-x86_64-unknown-linux-gnu.so` — Linux x86_64
- ...

### Checksums
- `checksums-sha256.txt`
```

---

## Rust-Specific Guidance

### Cargo.toml Metadata

Publishable crates should have complete metadata:

```toml
[package]
name = "my-library"
version = "0.1.0"
edition = "2021"
description = "Brief description of what the crate does"
license = "MIT"
repository = "https://github.com/org/repo"
readme = "README.md"
keywords = ["keyword1", "keyword2"]
categories = ["category"]
```

### Publish Control

Crates that should never be published to crates.io (binary-only crates, cdylib
crates for specific runtimes, internal tooling) must set:

```toml
[package]
publish = false
```

### Workspace Version Management

Use `[workspace.package]` to define the version once:

```toml
# Workspace root Cargo.toml
[workspace.package]
version = "0.2.0"

# Member crate Cargo.toml
[package]
version.workspace = true
```

### cargo-release

For automating version bumps, tag creation, and optional crates.io publishing,
[cargo-release](https://github.com/crate-ci/cargo-release) is recommended:

```toml
# release.toml (workspace root)
[workspace]
shared-version = true
consolidate-commits = true
tag-prefix = "v"

[[pre-release-replacements]]
file = "CHANGELOG.md"
search = "## \\[Unreleased\\]"
replace = "## [Unreleased]\n\n## [{{version}}] - {{date}}"
```

This is optional for first releases but recommended once the release cadence
stabilizes.

---

## Release Checklist

Before every release:

1. All CI checks pass on the commit to be released
2. Full test suite passes locally (e.g., `cargo test --workspace`, `npm test`,
   `pytest`)
3. Linter reports no warnings (e.g., `cargo clippy --workspace`, `eslint .`,
   `ruff check`)
4. Dependency audit shows no high/critical vulnerabilities (e.g., `cargo audit`,
   `npm audit`, `pip-audit`)
5. CHANGELOG.md `[Unreleased]` section is populated with all notable changes
6. Version bumped in all manifest files
7. CHANGELOG.md `[Unreleased]` renamed to `[X.Y.Z] - YYYY-MM-DD`
8. Migration guide written and linked (major versions only)
9. Commit: `chore(release): prepare vX.Y.Z`
10. Tag: `git tag vX.Y.Z`
11. Push commit and tag: `git push && git push --tags`
12. CI creates draft GitHub Release — verify all expected artifacts are present
13. Download at least one published artifact and smoke-test it to verify it runs
14. Review release notes, then publish the release

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
