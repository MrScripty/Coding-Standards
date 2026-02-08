# Dependency Standards

Guidelines for evaluating, adding, versioning, and auditing third-party dependencies.

## Core Principles

### 1. Every Dependency Must Justify Its Cost

Dependencies add maintenance burden, supply-chain attack surface, and compilation
or bundle size. Every dependency must provide value that exceeds these costs. If you
can implement the functionality in a small, well-tested module, prefer that over
adding a third-party package.

### 2. Dependencies Flow Downward

Library and utility layers should be lean. Orchestration and application layers can
afford heavier dependency trees because they are leaf nodes — nothing else depends
on them. Every unnecessary dependency in a library multiplies across all its
consumers.

```
┌──────────────────────────────────────┐
│   Application / Binary (heavier OK)  │  Leaf node — only built once
├──────────────────────────────────────┤
│   Library / Core (keep lean)         │  Consumed by multiple targets
└──────────────────────────────────────┘
```

### 3. Prefer the Standard Library

Before reaching for a third-party package, check whether the language's standard
library already provides the functionality. Standard library code is maintained by
the language team, has no additional supply-chain risk, and adds zero transitive
dependencies.

### 4. One Purpose per Dependency

Do not add a large framework to use one small function. If you need string padding,
do not import a utility grab-bag. If you need HTTP client functionality, do not
import a full web framework.

---

## Before Adding a Dependency

### Evaluation Questions

Before adding any dependency, answer these questions:

1. **Can this be implemented in-house?** If the functionality is small and
   well-understood, write it yourself.
2. **Is it actively maintained?** Check last commit date, open issue count, and
   maintainer response time.
3. **What is the license?** Verify compatibility with your project's license.
4. **How heavy is it?** Count transitive dependencies before adding.
5. **Is there already a similar dependency in the project?** Avoid multiple
   packages solving the same problem.
6. **What is the security track record?** Check for past CVEs and how quickly
   they were addressed.

### Build-or-Depend Decision Matrix

| In-House Effort | Dependency Quality | Decision |
|---|---|---|
| < 50 lines, straightforward | Any | Implement in-house |
| 50–200 lines, well-understood | Well-maintained, small dep tree | Either; prefer in-house |
| 50–200 lines, well-understood | Poorly maintained or heavy | Implement in-house |
| > 200 lines or specialized domain | Well-maintained, small dep tree | Use the dependency |
| > 200 lines or specialized domain | Poorly maintained | Search for alternatives |

### Transitive Dependency Thresholds

When evaluating how heavy a dependency is, use these thresholds:

| Transitive Deps | Action |
|---|---|
| < 20 | Add freely |
| 20–100 | Note in PR why this dependency is needed |
| 100+ | Must be feature-gated or justified in writing |

**Rust — Check transitive count before adding:**

```bash
# How many transitive deps does this crate bring?
cargo tree -p <crate> --depth=0 -e normal

# Is it already in the tree as a transitive dep?
cargo tree -i <crate>
```

**TypeScript/Node — Check package size:**

```bash
# View dependency tree of a package before installing
npm view <package> dependencies

# Check bundle size impact
npx package-size <package>
```

**C# — Check transitive count:**

```bash
# List all transitive dependencies
dotnet list package --include-transitive
```

---

## Searching and Comparing Dependencies

### Where to Search

| Ecosystem | Primary Registry | Search and Comparison Tools |
|---|---|---|
| Rust | crates.io | lib.rs (rankings, categories), `cargo search` |
| TypeScript / Node | npmjs.com | npms.io (quality/maintenance scores), `npm search` |
| C# / .NET | nuget.org | fuget.org (API browser), NuGet Package Explorer |

### Comparison Criteria

When evaluating multiple candidates for the same functionality, compare:

- **Download and usage trends** — Is adoption growing or declining?
- **Issue response time** — Does the maintainer engage with bug reports?
- **Release frequency** — Are there regular releases with changelogs?
- **Transitive dependency count** — Fewer is better.
- **Bundle or binary size impact** — Measure, don't guess.
- **API quality and documentation** — Can you understand the API without reading source?
- **Test coverage** — Does the project have a CI pipeline and tests?

### Red Flags

Avoid dependencies that exhibit these warning signs:

| Red Flag | Risk |
|---|---|
| Single maintainer with no succession plan (for critical functionality) | Bus factor of one; abandonment risk |
| No releases in 12+ months with open bug reports | Effectively unmaintained |
| Excessive transitive dependencies for stated purpose | Disproportionate cost |
| No tests or CI in the repository | Quality unknown |
| Unclear or incompatible license | Legal risk |
| History of slow CVE response | Security risk |

---

## Version Management

### Always Use Lockfiles

Every ecosystem provides a lockfile mechanism. Commit it to version control. Use
the CI-specific install command that enforces lockfile consistency.

| Ecosystem | Manifest | Lockfile | CI Install Command |
|---|---|---|---|
| Rust | Cargo.toml | Cargo.lock | `cargo build` (lockfile enforced automatically) |
| Node (npm) | package.json | package-lock.json | `npm ci` |
| Node (pnpm) | package.json | pnpm-lock.yaml | `pnpm install --frozen-lockfile` |
| C# / .NET | *.csproj | packages.lock.json | `dotnet restore --locked-mode` |

### Version Pinning Strategy

| Dependency Type | Version Strategy | Rationale |
|---|---|---|
| Application (deployed binary) | Pin exact in lockfile | Reproducible builds |
| Library (published for others) | Semver ranges in manifest | Allow consumers flexibility |
| CI tools and dev dependencies | Pin exact or narrow range | Prevent surprise CI breakage |
| Security-critical dependencies | Pin exact, update deliberately | Control attack surface |

### Centralized Version Management

When a project has multiple packages or crates, centralize shared dependency
versions to ensure consistency and simplify auditing.

**Rust — Workspace dependency inheritance:**

```toml
# Cargo.toml (workspace root)
[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }

# member/Cargo.toml — inherits version and features from workspace
[dependencies]
serde = { workspace = true }
tokio = { workspace = true }
```

All dependencies used by two or more workspace members should be declared in the
root `Cargo.toml` under `[workspace.dependencies]` and referenced with
`{ workspace = true }` in member crates.

**TypeScript/Node — pnpm workspace catalog or npm overrides:**

```jsonc
// pnpm-workspace.yaml — pnpm catalog for shared versions
catalog:
  react: "^18.2.0"
  typescript: "^5.3.0"

// Or package.json (monorepo root) — npm/yarn overrides
{
  "overrides": {
    "lodash": "4.17.21"
  }
}
```

**C# — Directory.Packages.props (Central Package Management):**

```xml
<!-- Directory.Packages.props at solution root -->
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageVersion Include="xunit" Version="2.7.0" />
  </ItemGroup>
</Project>

<!-- Individual .csproj files omit the Version attribute -->
<!-- <PackageReference Include="Newtonsoft.Json" /> -->
```

### Checking Compatibility Before Upgrading

Before upgrading a dependency to a new version:

1. **Read the changelog** — Look for breaking changes, deprecations, and migration
   guides.
2. **Diff the transitive tree** — Check whether the upgrade introduces new
   transitive dependencies or version conflicts.
3. **Run the full test suite** — Do not rely on type-checking alone; behavioral
   changes may not surface until runtime.
4. **Check for duplicate versions** — The upgrade may cause two versions of the
   same package to coexist in the tree.

---

## Minimizing Dependency Footprint

### Enable Only Required Features

Most package managers support feature flags or modular imports. Disable defaults
you do not use. Import only the functions you need.

**Rust — Select specific features:**

```toml
# BAD: Pulling in everything
[dependencies]
tokio = { version = "1", features = ["full"] }
hyper = { version = "1", features = ["full"] }

# GOOD: Only what you actually use
[dependencies]
tokio = { version = "1", features = ["rt-multi-thread", "net", "macros"] }
hyper = { version = "1", features = ["client", "http1"] }
```

**TypeScript/Node — Import specific modules:**

```typescript
// BAD: Import the entire library
import _ from 'lodash';
const result = _.pick(obj, ['a', 'b']);

// GOOD: Import only the function you need
import pick from 'lodash/pick';
const result = pick(obj, ['a', 'b']);

// BETTER: Implement trivially small utilities yourself
const { a, b } = obj;
```

**C# — Avoid meta-packages when you need one sub-package:**

```xml
<!-- BAD: Meta-package pulls in dozens of assemblies -->
<PackageReference Include="Microsoft.AspNetCore.App" />

<!-- GOOD: Only the specific package you need -->
<PackageReference Include="Microsoft.AspNetCore.Mvc.Core" Version="2.2.5" />
```

### Feature-Gate Heavy Optional Functionality

When your own library has optional heavyweight dependencies, put them behind
feature flags so consumers do not pay the cost unless they opt in.

**Rust:**

```toml
[features]
default = []
rag = ["dep:lancedb", "dep:arrow-array", "dep:arrow-schema"]
visualization = ["dep:plotters"]
export-pdf = ["dep:printpdf"]

[dependencies]
lancedb = { version = "0.22", optional = true }
arrow-array = { version = "53", optional = true }
arrow-schema = { version = "53", optional = true }
plotters = { version = "0.3", optional = true }
printpdf = { version = "0.7", optional = true }
```

```rust
#[cfg(feature = "visualization")]
pub mod visualization {
    // Only compiled when the consumer opts in
}
```

**TypeScript/Node — Use optional peer dependencies:**

```json
{
  "peerDependencies": {
    "canvas": "^2.0.0"
  },
  "peerDependenciesMeta": {
    "canvas": { "optional": true }
  }
}
```

### Keep Library Packages Lean

Library packages are depended on by multiple consumers. Every unnecessary
dependency in a library multiplies across all its consumers.

- If only the application binary needs a dependency, declare it there — not in
  the library that the binary imports.
- If a dependency is only needed for a specific feature, make it optional.
- Periodically review library dependencies and remove any that are no longer used.

### Transitive Dependency Inspection

Understand what your direct dependencies pull in before they become a problem.

| Ecosystem | Inspect Full Tree | Direct Deps Only |
|---|---|---|
| Rust | `cargo tree` | `cargo tree --depth 1` |
| Node | `npm ls --all` | `npm ls --depth=0` |
| C# | `dotnet list package --include-transitive` | `dotnet list package` |

**Rust — Additional tree queries:**

```bash
# Who depends on a specific crate?
cargo tree -i lancedb

# Total unique deps for one workspace member
cargo tree -p my-crate --prefix none --no-dedupe | sort -u | wc -l

# Find duplicate versions of the same crate
cargo tree --duplicates
```

---

## Auditing Dependencies

### Security Auditing

Run security audit tooling on every PR and before every release.

| Ecosystem | Audit Command | Advisory Database |
|---|---|---|
| Rust | `cargo audit` | RustSec |
| Node | `npm audit --audit-level=high` | npm Advisory DB |
| C# | `dotnet list package --vulnerable` | GitHub Advisory DB / NuGet |

### Detecting Unused Dependencies

Dependencies declared in the manifest but never imported in source code waste
compile time, increase bundle size, and expand the attack surface.

| Ecosystem | Tool | Usage |
|---|---|---|
| Rust | cargo-machete | `cargo machete` (fast, heuristic-based) |
| Rust | cargo-udeps | `cargo +nightly udeps` (precise, requires nightly) |
| Node | depcheck | `npx depcheck` |
| C# | (manual or IDE analysis) | Remove the reference, build, check for errors |

```toml
# BAD: Declared but never imported in any source file
[dependencies]
regex = "1"       # grep shows zero imports of regex::
chrono = "0.4"    # was used in a test that was deleted

# GOOD: Every dependency has corresponding usage in source code
[dependencies]
serde = { version = "1.0", features = ["derive"] }  # use serde::{Serialize, Deserialize}
tokio = { version = "1", features = ["rt-multi-thread"] }  # use tokio::runtime
```

### Manual Usage Verification

For any dependency in the manifest, confirm actual usage in source code:

```bash
# Replace <crate> and <path> with the dependency and source directory
grep -r "use <crate>" <path>/src/
grep -r "<crate>::" <path>/src/
```

If both return nothing, the dependency is likely unused.

**Watch for masking:** A local `mod foo` can shadow an external crate `foo`. If
you see `use foo::` but there is a `mod foo;` in the same scope, the external
crate may not actually be in use.

### Detecting Duplicate Versions

When the dependency tree contains multiple versions of the same package, binary
size increases and subtle bugs can occur at type boundaries.

**Rust:**

```bash
cargo tree --duplicates
```

**Node:**

```bash
npm ls 2>/dev/null | grep "deduped\|invalid\|UNMET"
```

Resolution strategy: Update dependents to converge on a single version, or use
workspace resolution / overrides to force consistency.

### Identifying Heavy Dependencies

Periodically check which dependencies contribute the most to compile time or
bundle size.

**Rust:**

```bash
# Build timing per crate
cargo build --timings

# Count transitive deps per workspace member
cargo tree -p <crate> --prefix none --no-dedupe | sort -u | wc -l
```

**TypeScript/Node:**

```bash
# Bundle size analysis
npx webpack-bundle-analyzer stats.json

# Individual package size
npx package-size <package>
```

**The rule:** If a dependency brings 100+ transitive dependencies, it must be
feature-gated or justified in writing. If it accounts for >20% of total compile
time or bundle size, investigate lighter alternatives.

### Periodic Manual Review

Not all dependency risks are detectable by automated tools. Periodically review:

- **Maintenance status** — Is the dependency still actively maintained?
- **Ownership changes** — Has the package changed ownership? (supply chain risk)
- **Version currency** — Are you on the latest major version? Old major versions
  stop receiving security patches.
- **Usage patterns** — Has your code changed such that you no longer need this
  dependency?

---

## CI Integration

### Recommended CI Checks

| Check | Rust | Node | C# | Frequency |
|---|---|---|---|---|
| Security audit | `cargo audit` | `npm audit` | `dotnet list package --vulnerable` | Every PR |
| Unused deps | `cargo machete` | `npx depcheck` | — | Every PR |
| License check | `cargo deny check licenses` | `npx license-checker` | `dotnet-license` | Every PR |
| Lockfile integrity | Automatic | `npm ci` | `dotnet restore --locked-mode` | Every PR |
| Duplicate versions | `cargo tree --duplicates` | `npm ls` | — | On dependency changes |

### Example CI Workflow

```yaml
# .github/workflows/dependency-checks.yml
name: Dependency Checks
on: [pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Security audit
        run: cargo audit

      - name: Check for unused dependencies
        run: |
          cargo install cargo-machete
          cargo machete --with-metadata

      - name: Check for duplicate versions
        run: cargo tree --duplicates

      - name: License compliance
        run: |
          cargo install cargo-deny
          cargo deny check licenses
```

Adapt the workflow to your ecosystem. The structure is the same: security audit,
unused dependency detection, duplicate check, and license verification.

### Blocking vs. Warning

| Check | PR Gate | Rationale |
|---|---|---|
| Security audit (high / critical severity) | Block | Known vulnerabilities must not ship |
| Unused dependencies | Block | Keeps the dependency tree clean |
| License violation | Block | Legal compliance |
| Duplicate versions | Warn | Sometimes unavoidable; track for cleanup |
| Outdated major versions | Warn | Plan upgrades, don't block features |

---

## Common Mistakes

**Declaring deps in library packages that only the application uses.** If the
binary target needs `lancedb` but the library crate does not use it, do not put
it in the library's manifest just because it feels related. This bleeds the
dependency into every consumer of that library.

**Forgetting to remove deps after refactoring.** When moving code between packages
or deleting features, manifest entries often get left behind. The compiler will
not warn you. Run unused dependency detection after refactors.

**Adding transitive deps as direct deps when not calling their APIs.** Packages
like `hyper`, `bytes`, and `http` are transitive deps of `reqwest` and `axum`. If
you are not calling their APIs directly, do not declare them. Add them only when
you actually need their types or functions in your code.

**Using full feature sets when you need one feature.** For example,
`hyper = { features = ["full"] }` when you only need the client. Check what
features your code actually uses and declare only those.

**Not updating lockfiles after manifest changes.** After adding, removing, or
changing a dependency version in the manifest, regenerate the lockfile and commit
it. A stale lockfile causes CI failures and non-reproducible builds.

---

## Dependency Review Checklist

### Adding a Dependency

- [ ] Evaluated against the build-or-depend decision matrix
- [ ] License verified as compatible
- [ ] Maintenance status checked (recent commits, responsive maintainers)
- [ ] Security audit passes with the new dependency
- [ ] Only required features enabled
- [ ] No duplicate versions introduced in the dependency tree
- [ ] Transitive dependency count reviewed and within thresholds
- [ ] Lockfile updated and committed
- [ ] Added to project's approved dependency list with justification
- [ ] Centralized version management used if the dep appears in 2+ packages

### Removing a Dependency

- [ ] All imports and usages removed from source code
- [ ] Dependency removed from manifest file(s)
- [ ] Lockfile regenerated and committed
- [ ] Feature flags referencing this dependency removed or updated
- [ ] Build and tests pass without the dependency

### Periodic Review

- [ ] Security audit run with latest advisory databases
- [ ] Unused dependency scan run and results addressed
- [ ] Duplicate versions reviewed and consolidated where possible
- [ ] Outdated major versions identified and upgrade plan documented
- [ ] Dependency ownership changes reviewed for supply chain risk
