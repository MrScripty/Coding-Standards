# Rust Cross-Platform Standards

Rust target and platform rules. These specialize the generic
[Cross-Platform Standards](../../CROSS-PLATFORM-STANDARDS.md).

## Target Policy

Define supported Rust targets explicitly:

| Platform | Target |
| --- | --- |
| Linux x86_64 | `x86_64-unknown-linux-gnu` |
| Windows x86_64 | `x86_64-pc-windows-msvc` |
| macOS ARM | `aarch64-apple-darwin` |
| macOS Intel | `x86_64-apple-darwin` |

Required targets must compile in CI. Best-effort targets should keep platform
modules and APIs compatible even when full runtime tests are impractical.

## Keep `cfg()` In Thin Platform Modules

Rust `cfg()` is compile-time, which is acceptable because Rust builds target one
platform at a time. Keep `cfg()` isolated to platform modules instead of
scattering it through business logic.

```rust
// BAD: cfg scattered through business logic.
fn process_data(path: &str) {
    #[cfg(target_os = "linux")]
    let lib = load_linux_lib();
    #[cfg(target_os = "windows")]
    let lib = load_windows_lib();
    // ...
}
```

```rust
// platform/linux.rs
#[cfg(target_os = "linux")]
pub fn load_native_lib() -> Library {
    // ...
}

// platform/windows.rs
#[cfg(target_os = "windows")]
pub fn load_native_lib() -> Library {
    // ...
}

// platform/mod.rs
#[cfg(target_os = "linux")]
mod linux;
#[cfg(target_os = "windows")]
mod windows;

#[cfg(target_os = "linux")]
pub use linux::load_native_lib;
#[cfg(target_os = "windows")]
pub use windows::load_native_lib;
```

Rules:

- Platform-specific behavior belongs behind a shared trait or platform module
  API.
- The rest of the crate should call platform-neutral functions.
- Do not mix target-specific subprocess, filesystem, dynamic library, or path
  behavior into domain services.
- Name platform modules clearly: `linux`, `windows`, `macos`, `unix`, or by the
  target-specific concern.

## Acceptable Inline `cfg()` Exception

An inline `cfg()` block may remain when all of the following are true:

1. The platform-specific code is five lines or fewer.
2. Extracting it would require passing three or more parameters or restructuring
   the surrounding function.
3. Both platform behaviors are documented with comments.
4. The file contains no more than two inline `cfg()` blocks total.

```rust
fn spawn_detached(cmd: &mut Command) {
    // Windows: CREATE_NO_WINDOW prevents console flash.
    #[cfg(windows)]
    cmd.creation_flags(0x08000000);

    // Unix: setsid detaches from parent terminal.
    #[cfg(unix)]
    cmd.process_group(0);

    cmd.spawn().expect("failed to spawn");
}
```

If a file accumulates more than two inline `cfg()` blocks, refactor the
platform-specific logic into the platform module.

## Verification

Cross-platform Rust workspaces should define target checks for supported
platforms:

```bash
cargo check --workspace --target x86_64-unknown-linux-gnu
cargo check --workspace --target x86_64-pc-windows-msvc
cargo check --workspace --target aarch64-apple-darwin
```

Use `cross`, containerized builds, or hosted CI runners when native toolchains
are impractical locally.
