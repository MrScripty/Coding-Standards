# Rust Unsafe Standards

Policy for unsafe Rust, FFI, OS boundaries, embedded/no_std code, memory-mapped
resources, and performance-sensitive escape hatches.

## Default Policy

Safe Rust is the default.

Workspace policy should deny unsafe code by default:

```toml
[workspace.lints.rust]
unsafe_code = "deny"
```

Crates that legitimately own unsafe boundaries may explicitly relax the lint:

```toml
[lints.rust]
unsafe_code = "warn"
```

Use this exception only for crates or modules that intentionally own one of:

- FFI wrappers
- raw OS APIs
- memory-mapped files or devices
- custom allocators
- embedded or `no_std` raw pointer code
- lock-free or performance-critical primitives
- language binding shims that must cross unsafe runtime boundaries

The goal is not to ban unsafe forever. The goal is to make unsafe an explicit
architectural exception instead of an implementation convenience.

## Isolation Rules

Rules:

- Prefer safe Rust and safe wrappers around lower-level mechanisms.
- Business/domain logic must not contain raw pointer or FFI `unsafe` blocks.
- Keep `unsafe` in thin modules with a safe API above them.
- Every `unsafe` block and `unsafe fn` must have a `SAFETY:` comment explaining
  the invariant being upheld.
- If a module exists primarily to contain unsafe behavior, include a module-level
  `# Safety` section.
- Gate optional unsafe implementation paths behind Cargo features when a safe
  default implementation exists.
- Do not introduce `unsafe` without a verification plan.

## Unsafe Exception Checklist

Before relaxing `unsafe_code = "deny"` for a crate:

- [ ] The crate has a documented reason why safe Rust is insufficient.
- [ ] Unsafe code is isolated from domain logic.
- [ ] The safe public wrapper states ownership, lifetime, thread-safety, and
      error behavior.
- [ ] Every unsafe block has a `SAFETY:` comment.
- [ ] The crate has targeted tests for the safe wrapper.
- [ ] The crate has an appropriate verification plan from the matrix below.
- [ ] Optional unsafe paths are feature-gated when a safe fallback exists.

## Unsafe Verification Matrix

| Unsafe kind | Required verification |
| --- | --- |
| Pure Rust unsafe | Miri in CI or scheduled CI |
| FFI or C/C++ calls | Valgrind or ASan where practical |
| Concurrent unsafe or lock-free code | Miri plus TSan or loom, depending on shape |
| Memory-mapped or raw OS resources | ASan or Valgrind plus integration tests |
| Embedded or `no_std` raw pointer code | Miri where possible plus target build checks |

Recommended practice:

- Run Miri on crates with unsafe code.
- Run sanitizers on a scheduled workflow or before release when runtime cost is
  too high for every PR.
- Mock or cfg-gate FFI boundaries that Miri cannot execute.
- Use `cargo geiger` or equivalent review tooling to track unsafe usage in the
  crate and dependency tree.

## Feature-Gated Unsafe Paths

When a safe default implementation exists, optional unsafe implementations must
be behind an explicit feature.

```toml
[features]
default = []
direct-ipmi = []
direct-accelerator-api = []
```

```rust
#[cfg(feature = "direct-ipmi")]
mod direct {
    //! Direct IPMI device access through ioctl.
    //!
    //! # Safety
    //! This module owns raw device access. It is verified with Miri where
    //! possible and Valgrind/ASan for runtime memory checks.
}

#[cfg(not(feature = "direct-ipmi"))]
mod subprocess {
    //! Safe default implementation through a subprocess boundary.
}
```

Unsafe feature paths must be tested directly, not only through default builds.

