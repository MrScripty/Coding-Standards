# Rust Interop Standards

Rust-specific FFI, wire-format, and unsafe-boundary rules. These specialize the
generic [Interop Standards](../../INTEROP-STANDARDS.md).

## Validate Before Unsafe Access

FFI input is untrusted. Validate nullability, ranges, and overflow before
constructing references or slices:

```rust
fn on_data_received(&self, buffer: *const u8, width: c_int, height: c_int) {
    if buffer.is_null() {
        return;
    }
    if width <= 0 || height <= 0 {
        return;
    }

    let size = (width as usize)
        .checked_mul(height as usize)
        .and_then(|s| s.checked_mul(4))
        .unwrap_or(0);
    if size == 0 {
        return;
    }

    let data = unsafe { std::slice::from_raw_parts(buffer, size) };
    let owned = data.to_vec();
    self.handle_owned_buffer(owned);
}
```

Prefer returning typed errors over silently dropping input when the boundary
allows error propagation.

## Copy Foreign Buffers Immediately

Foreign code may free or reuse buffers after a callback returns. Copy data into
Rust-owned memory before storing or sharing it:

```rust
// GOOD: Copy immediately, then work with the copy.
let buffer_copy = raw_data.to_vec();
*shared.buffer.lock() = Some(Arc::new(buffer_copy));

// BAD: Store a pointer or slice to foreign memory.
let buffer_ref = raw_data;
```

## Unsafe Isolation

Unsafe operations must live in thin wrapper modules. Business logic should call
safe Rust APIs and should not contain raw pointer manipulation.

```text
my_native_binding/
|-- ffi_wrapper.rs       # unsafe raw pointer access
|-- types.rs             # pure Rust data structures
|-- bridge.rs            # safe API over the FFI wrapper
`-- lib.rs               # public API and safe re-exports
```

Rules:

- Every unsafe block must state the invariant that makes it sound.
- Every `unsafe fn` must document caller obligations in a `# Safety` section.
- FFI wrapper modules should convert raw inputs into validated Rust types before
  handing data to core logic.
- Unsafe-owning crates must follow
  [RUST-UNSAFE-STANDARDS.md](RUST-UNSAFE-STANDARDS.md).

## Callback Thread Contracts

Every callback crossing an FFI boundary must document which thread invokes it,
whether it may re-enter Rust, and how long borrowed data remains valid:

```rust
/// Called on the native library's worker thread.
///
/// `buffer` is only valid for the duration of this callback. The implementation
/// must copy it before returning.
fn on_data_received(&self, buffer: *const u8, width: c_int, height: c_int) {}
```

## Serde Wire-Format Alignment

Serde attributes define the wire contract. Receiving languages must match the
serialized shape exactly.

```rust
#[derive(Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum ServerEvent {
    TimelineChanged,
    BeatUpdated { clip_id: String },
    GenerationProgress { clip_id: String, token: String },
}
```

```typescript
type ServerMessage =
    | { type: 'timeline_changed' }
    | { type: 'beat_updated'; clip_id: string }
    | { type: 'generation_progress'; clip_id: string; token: string };
```

Rules:

- Check `rename_all`, `tag`, `content`, and `rename` before writing client types.
- Use explicit `rename_all` on public wire DTOs instead of relying on Rust enum
  or field casing.
- Test serialization round trips across the boundary.
- Prefer shared schema generation for long-lived public contracts.
