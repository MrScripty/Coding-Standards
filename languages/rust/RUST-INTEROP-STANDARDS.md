# Rust Interop Standards

Canonical Rust foreign-memory, checked-dimension, raw-slice, callback-lifetime,
and copy-after-proof guidance moved to the
[Rust Interop Profile](../../profiles/languages/rust/interop.md).

## Validate Before Unsafe Access

Checked conversion and complete raw-access proof moved to the
[Rust Interop Profile](../../profiles/languages/rust/interop.md#checked-dimensions).

## Copy Foreign Buffers Immediately

Copy-after-proof and ownership transfer moved to the
[Rust Interop Profile](../../profiles/languages/rust/interop.md#copy-after-proof).

## Unsafe Isolation

Validated adapter isolation moved to the
[Rust Interop Profile](../../profiles/languages/rust/interop.md#callback-and-adapter-boundary).

## Callback Thread Contracts

Thread, re-entry, and borrowed-input lifetime guidance moved to the
[Rust Interop Profile](../../profiles/languages/rust/interop.md#callback-and-adapter-boundary).

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
