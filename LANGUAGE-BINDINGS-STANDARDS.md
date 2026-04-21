# Language Bindings Standards

Architecture patterns for exposing a core library to one or more host
languages. Language-specific implementation rules must live under
`languages/<language>/`.

Rust-specific binding architecture, wrapper crates, UniFFI, Rustler, generated
host bindings, async bridging, FFI type shaping, and release artifact layout live
in
[languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md](languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md).

For low-level boundary safety, see [INTEROP-STANDARDS.md](INTEROP-STANDARDS.md).
For platform-specific build concerns, see
[CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md).

## Core Principles

1. Keep domain logic independent from binding frameworks.
2. Treat generated host-language bindings as artifacts, not hand-maintained
   source.
3. Keep the binding layer thin: type conversion, error mapping, lifecycle
   bridging, and host-runtime adaptation only.
4. Version binding packages and native artifacts from the same release input.
5. Document host-language ownership, threading, async, and shutdown semantics.
6. Test the core library without binding frameworks, then test each binding at
   the host-language boundary.

## Layer Model

```text
+-----------------------------------------------------------+
|  Layer 3: Generated / Host Bindings                       |
|  Host-language packages, generated source, wrappers       |
+-----------------------------------------------------------+
|  Layer 2: Binding / FFI Adapter                           |
|  FFI-safe DTOs, conversions, errors, callbacks, lifecycle |
+-----------------------------------------------------------+
|  Layer 1: Core Library                                    |
|  Domain logic, validated types, no binding concerns       |
+-----------------------------------------------------------+
```

Rules:

1. Core logic must compile and test without binding-specific frameworks.
2. Binding adapters depend on core; core must not depend on binding adapters.
3. Generated host-language code is regenerated after API changes and should not
   contain business logic.
4. Multiple binding frameworks may coexist only if they wrap the same core
   contract through separate adapters.
5. Release artifacts must make native library, generated binding package, and
   version compatibility explicit.

## Language-Specific Extensions

Add binding standards under the language that owns the native implementation or
binding toolchain:

```text
languages/
`-- rust/
    `-- RUST-LANGUAGE-BINDINGS-STANDARDS.md
```

Root binding standards should describe cross-language architecture. Framework
details, commands, annotations, generated-file layouts, and host-runtime bridges
belong in the language-specific standard.
