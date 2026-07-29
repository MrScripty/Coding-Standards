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

Canonical selected-schema, Serde-attribute, consumer-agreement, typed-outcome,
and native/host evidence guidance moved to
[Serialized Wire Representation](../../profiles/languages/rust/language-bindings.md#serialized-wire-representation).
