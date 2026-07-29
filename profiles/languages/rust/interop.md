# Rust Interop Profile

**Standards metadata**

- ID: `profile.language.rust.interop`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust code converts foreign dimensions, constructs references or slices from raw foreign memory, receives borrowed callback data, or copies foreign buffers.
- Does not apply when: Rust code uses only ordinary safe owned values and no foreign memory or resource authority.
- Requires: `core`, `workflow.verification`, `profile.language.rust`, `profile.boundary.interop`
- Specializes: `profile.language.rust`, `profile.boundary.interop`
- Verification: Rust foreign-memory decisions plus affected Miri, sanitizer, and provider/consumer boundary tests selected by the unsafe mechanism.
- Canonical owner: `profiles/languages/rust/interop.md`

## Checked Dimensions

Convert signed, platform-width, and wider foreign dimensions into the target
integer domain with `TryFrom` or equivalent checked conversion before
arithmetic. Then use checked multiplication and addition for element counts,
strides, offsets, and byte sizes.

Check the operation's resource limit separately from representability. A value
can fit `usize` and still be too large for the supported allocation or
provider contract.

Return a typed error for negative, too-wide, overflowed, or over-limit values.
Do not use `as`, wrapping, saturation, truncation, clamping, or zero as a
substitute for failed conversion.

## Raw Slice Preconditions

Before calling `slice::from_raw_parts` or an equivalent constructor, prove:

- the pointer follows Rust's non-null and alignment rules, including the
  explicitly selected zero-length representation;
- the complete range belongs to one allocation with compatible provenance;
- every byte or element in the range is initialized and valid to read;
- the total size does not exceed `isize::MAX` and address calculation does not
  wrap;
- aliasing and mutability rules permit the requested view; and
- the resulting lifetime does not outlive the provider guarantee.

Non-nullness and a numeric length are not complete proof. A safe wrapper may
encode established facts, but it cannot manufacture allocation, provenance,
initialization, or lifetime authority.

## Zero-Length Views

Define whether zero-length input is supported. If supported, use a pointer form
that satisfies Rust's requirements even though no element is accessed. Do not
infer that null is valid from a zero length or replace an invalid nonzero input
with an empty slice.

## Copy After Proof

Create a temporary borrowed view only after all applicable preconditions hold,
then copy before the provider lifetime ends when owned data is required.
Copying does not repair invalid construction and cannot precede proof.

The owned copy may escape the callback only after the copy succeeds. The raw
pointer, temporary slice, and any derived borrow remain bounded by the foreign
provider lifetime.

## Callback And Adapter Boundary

Document callback thread, re-entry, and borrowed-input lifetime. Keep raw
pointer construction in the boundary adapter and pass validated or owned Rust
values to domain logic.

If required pointer, alignment, allocation, provenance, initialization, extent,
or lifetime evidence cannot be obtained, return typed `unavailable`.
Contradictory or malformed evidence returns typed `invalid`.

## No Fallback

Failed foreign-memory proof cannot fall back to:

- `as usize` or another unchecked conversion;
- `unwrap_or(0)`, an empty slice, or a sentinel length;
- wrapping, saturating, truncating, or clamping arithmetic;
- assuming alignment, one allocation, initialization, or provenance;
- copying after constructing an invalid view; or
- extending a borrow beyond the provider lifetime.

Return the typed diagnostic before any unsafe access.

## Verification

Affected tests cover:

- negative, too-wide, overflowed, and over-limit dimensions;
- supported and unsupported zero-length pointer forms;
- null and misaligned pointers;
- split or unknown allocation/provenance;
- missing pointer, alignment, initialization, extent, or lifetime evidence;
- partial initialization and excessive extent;
- expired callbacks and escaped borrows;
- successful copy after proof and rejected copy before proof; and
- mechanism-appropriate dynamic checks for the supported targets.
