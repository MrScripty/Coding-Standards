# Cross-Platform Standards

Canonical target support, platform-behavior isolation, mechanism selection,
semantic fidelity, and typed unresolved outcomes moved to the
[Cross-Platform topic](topics/cross-platform.md#platform-support-contract).
Language-specific mechanisms are selected through the
[Standards Router](STANDARDS-ROUTER.md).

---

## File System Conventions

Canonical path construction, display/lexical/canonical identity, comparison,
alias, space, and filesystem-family verification policy moved to
[Cross-Platform](topics/cross-platform.md#filesystem-paths). Untrusted
filesystem authorization additionally follows
[Security containment](topics/security.md#filesystem-containment).

---

## Native Library Rules

Native artifact loading is governed by the canonical
[Cross-Platform loading contract](topics/cross-platform.md#native-artifact-loading).

### Loading Strategy

See the
[Cross-Platform loading contract](topics/cross-platform.md#native-artifact-loading).

### Library Naming

| Platform | Prefix | Extension | Example |
|----------|--------|-----------|---------|
| Linux | `lib` | `.so` | `libmylib.so` |
| Windows | (none) | `.dll` | `mylib.dll` |
| macOS | `lib` | `.dylib` | `libmylib.dylib` |

### Installation Documentation

Each platform-specific class should include installation instructions for its
native dependencies. Users should not have to guess where to get libraries.

---

## CI Matrix

CI must build on all required platforms:

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - os: ubuntu-latest
        rid: linux-x64
      - os: windows-latest
        rid: win-x64
```

Rules:
- CI must build on at least Linux and Windows (or your required platforms)
- Platform-specific tests run on their respective OS
- Matrix builds should set `fail-fast: false` so one platform failure does not
  hide others
- Best-effort platform CI is optional but code must compile
- CI should invoke the same build commands as local development

### When to Build

| Trigger | What Runs | Platform |
|---------|-----------|----------|
| Pre-commit | Type check / lint | Current platform only |
| Pre-push | Full test suite | Current platform only |
| CI (push/PR) | Full build + test | All required platforms |
