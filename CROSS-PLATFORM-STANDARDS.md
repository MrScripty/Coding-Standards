# Cross-Platform Standards

Requirements for multi-platform support with minimal OS-specific code.

## Platform Targets

Define your supported platforms explicitly:

| Platform | Status | .NET RID | Rust Target |
|----------|--------|----------|-------------|
| Linux x86_64 | Required | `linux-x64` | `x86_64-unknown-linux-gnu` |
| Windows x86_64 | Required | `win-x64` | `x86_64-pc-windows-msvc` |
| macOS ARM | Best-effort | `osx-arm64` | `aarch64-apple-darwin` |
| macOS Intel | Best-effort | `osx-x64` | `x86_64-apple-darwin` |

**Required** means CI must build and test on this platform.
**Best-effort** means the code must compile and the architecture must support
it, but CI and testing are optional if impractical.

## Core Rules

### 1. No Inline Platform Checks in Business Logic

Platform-specific behavior must live behind an abstraction. Never scatter
`if (IsWindows)` through handlers, services, or UI code.

```csharp
// BAD: Platform check mixed into business logic
public async Task ExtractAsync(string path)
{
    if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
        await ExtractLinux(path);
    else
        await ExtractWindows(path);
}

// GOOD: Platform logic behind an interface, selected by factory
var extractor = ExtractorFactory.Create();  // Returns platform-specific impl
await extractor.ExtractAsync(path);
```

### 2. Strategy + Factory Pattern

Each platform gets its own class implementing a shared interface. A factory
selects the correct implementation at runtime.

```csharp
// Interface — platform-agnostic contract
public interface IPlatformService
{
    string PlatformName { get; }
    bool TryInitialize(ILogger? logger = null);
}

// Factory — single place where platform detection happens
public static class PlatformServiceFactory
{
    public static IPlatformService Create()
    {
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
            return new LinuxPlatformService();
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            return new WindowsPlatformService();
        if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            return new MacOSPlatformService();

        throw new PlatformNotSupportedException(
            $"Not supported on {RuntimeInformation.OSDescription}");
    }
}
```

### 3. One Platform Per File

Platform implementations live in separate files named by platform:

```
Feature/
├── IFeatureService.cs              ← Interface
├── FeatureServiceBase.cs           ← Shared logic (Template Method)
├── LinuxFeatureService.cs          ← Linux implementation
├── WindowsFeatureService.cs        ← Windows implementation
├── MacOSFeatureService.cs          ← macOS implementation
└── FeatureServiceFactory.cs        ← Factory
```

Never put multiple platform implementations in one file. This keeps diffs
clean and makes it obvious which platforms are supported.

### 4. Graceful Degradation for Best-Effort Platforms

Best-effort platform implementations should exist even if minimal. Use
`PlatformNotSupportedException` for genuinely unsupported features, not
missing files.

```csharp
// Acceptable: best-effort stub that degrades gracefully
public sealed class MacOSFeatureService : FeatureServiceBase
{
    public override string PlatformName => "macOS";

    public override bool TryInitialize(ILogger? logger = null)
    {
        logger?.Warning("Feature X is not yet fully supported on macOS");
        return false;  // Graceful degradation, not a crash
    }
}
```

### 5. No `#if` Preprocessor Directives for Platform

Use runtime detection only. `#if` directives prevent cross-compilation in
a single build and make code harder to read and test.

```csharp
// BAD: Compile-time exclusion
#if LINUX
    LoadLinuxLibrary();
#elif WINDOWS
    LoadWindowsLibrary();
#endif

// GOOD: Runtime detection via factory
var loader = LibraryLoaderFactory.Create();
loader.Load();
```

### 6. Rust: `cfg()` Only in Thin Platform Modules

Rust's `cfg()` is compile-time, which is acceptable because Rust targets
a single platform per build. But keep `cfg()` isolated to dedicated modules:

```rust
// BAD: cfg scattered through business logic
fn process_data(path: &str) {
    #[cfg(target_os = "linux")]
    let lib = load_linux_lib();
    #[cfg(target_os = "windows")]
    let lib = load_windows_lib();
    // ...
}

// GOOD: Platform module with cfg at module level
// platform_linux.rs
#[cfg(target_os = "linux")]
pub fn load_native_lib() -> Library { /* ... */ }

// platform_windows.rs
#[cfg(target_os = "windows")]
pub fn load_native_lib() -> Library { /* ... */ }

// mod.rs — re-exports the correct module
#[cfg(target_os = "linux")]
mod platform_linux;
#[cfg(target_os = "windows")]
mod platform_windows;

#[cfg(target_os = "linux")]
pub use platform_linux::load_native_lib;
#[cfg(target_os = "windows")]
pub use platform_windows::load_native_lib;
```

#### Acceptable Inline Exception

A `cfg()` block may remain inline when **all** of the following are true:

1. The platform-specific code is 5 lines or fewer
2. Extracting it would require passing 3+ parameters or restructuring the
   surrounding function (e.g., setting a flag on a builder mid-construction)
3. Both platform behaviors are documented with comments
4. The file contains no more than 2 inline `cfg()` blocks total

```rust
// ACCEPTABLE: Single-expression cfg on a builder, documented
fn spawn_detached(cmd: &mut Command) {
    // Windows: CREATE_NO_WINDOW prevents console flash
    #[cfg(windows)]
    cmd.creation_flags(0x08000000);
    // Unix: setsid detaches from parent terminal
    #[cfg(unix)]
    cmd.process_group(0);

    cmd.spawn().expect("failed to spawn");
}
```

If the file accumulates more than 2 inline `cfg()` blocks, refactor the
platform-specific logic into the platform module.

---

## File System Conventions

### Path Construction

Always use platform-agnostic path APIs. Never hardcode separators.

```csharp
// BAD: Hardcoded separator
var path = baseDir + "/" + fileName;
var path = baseDir + "\\" + fileName;

// GOOD: Platform-agnostic
var path = Path.Combine(baseDir, fileName);
```

```typescript
// BAD: Hardcoded separator
const fullPath = `${dir}/${file}`;

// GOOD: Use path.join (Node) or let the backend handle paths
import path from 'node:path';
const fullPath = path.join(dir, file);
```

### Path Comparison

Normalize before comparing. Windows paths are case-insensitive;
Linux paths are case-sensitive.

```csharp
// GOOD: Normalize and use platform-appropriate comparison
var resolved = Path.GetFullPath(inputPath);
var root = Path.GetFullPath(allowedRoot);
if (resolved.StartsWith(root, StringComparison.OrdinalIgnoreCase))
    // Valid path
```

### Spaces in Paths

All path handling must support spaces in directory and file names:

- Always quote paths in shell scripts: `"$PATH_VAR"`
- Always use proper path APIs, never string splitting on `/`
- Test with spaces in paths before merging

---

## Native Library Rules

### Loading Strategy

Platform-specific native libraries (`.so`, `.dll`, `.dylib`) should be loaded
through the Strategy pattern, not embedded in managed assemblies.

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
- Best-effort platform CI is optional but code must compile
- CI should invoke the same build commands as local development

### When to Build

| Trigger | What Runs | Platform |
|---------|-----------|----------|
| Pre-commit | Type check / lint | Current platform only |
| Pre-push | Full test suite | Current platform only |
| CI (push/PR) | Full build + test | All required platforms |
