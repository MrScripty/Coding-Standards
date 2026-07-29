# Rust Security Profile

**Standards metadata**

- ID: `profile.language.rust.security`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust converts untrusted dimensions, counts, offsets, strides, or lengths before arithmetic, allocation, indexing, or bounded resource use.
- Does not apply when: Values are already represented by a validated type whose invariant proves the complete arithmetic and resource contract.
- Requires: `core`, `workflow.verification`, `topic.security`, `profile.language.rust`
- Specializes: `topic.security`, `profile.language.rust`
- Verification: Rust checked-boundary-arithmetic decisions plus affected parser, allocation, indexing, and boundary tests.
- Canonical owner: `profiles/languages/rust/security.md`

## Checked Boundary Sizing

Treat dimensions, counts, offsets, strides, and lengths from FFI, IPC, network,
file, command-line, or other untrusted input as source-domain values until
conversion succeeds.

Convert each value into the target integer domain with `TryFrom` or an
equivalent checked conversion before multiplication, addition, indexing,
allocation, or slice construction. A later checked multiplication does not
repair an earlier lossy cast.

Use checked arithmetic for every operation in the size expression. Return typed
`invalid` for negative values, values that do not fit the target domain, and
arithmetic overflow.

## Resource Limits

Check the operation's supported resource limit after representability and
arithmetic succeed. Integer fit does not prove that an allocation, collection,
message, image, or other resource size is permitted.

Return typed `invalid` when the computed value exceeds the declared operation
limit. A zero value is accepted only when the operation contract explicitly
permits it; otherwise return typed `invalid`.

## Interop Relationship

This profile owns checked Rust sizing for untrusted inputs. When the computed
size authorizes access to raw foreign memory, also apply the
[Rust Interop profile](interop.md); numeric validity does not prove pointer,
allocation, provenance, initialization, alignment, aliasing, or lifetime
authority.

## No Fallback

Failed conversion, arithmetic, or limit proof cannot fall back to:

- `as` or another lossy or unchecked conversion;
- zero, an empty value, or a sentinel size;
- clamping, saturation, wrapping, or truncation;
- a smaller default allocation or operation; or
- continuing with a partially checked expression.

Return the typed diagnostic before allocation, indexing, slice construction, or
resource use.

## Verification

Affected tests cover:

- negative and target-domain-too-wide values;
- multiplication and addition overflow;
- values that fit the integer domain but exceed the resource limit;
- permitted and forbidden zero values;
- valid bounded values; and
- rejection of cast, zero, clamp, saturation, wrap, truncation, and
  smaller-default recovery.
