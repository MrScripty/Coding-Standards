# Milestone 7 F022/F023 Decomposition

## Purpose

This report decomposes critical findings `F022` and `F023` before normative
guidance moves. It is planning evidence, not a standards owner. The sequence
establishes generic foreign-boundary and language-binding contracts before
their Rust specializations, then removes unsafe conversion, memory, and
contract examples without fallback.

## Trigger And Evidence

The legacy corpus currently presents four correctness defects:

- Rust binding tables call `String`, `Vec<T>`, and `Option<T>` universally
  FFI-safe even though a binding framework may lift or serialize those values
  without making their Rust representation C-ABI-safe;
- wrapper examples use unchecked `as` conversions, including `u128` duration
  values narrowed to `u64`, and prescribe infallible `From` conversions where
  a target representation can reject a source value;
- the foreign-buffer example constructs a slice without stating every
  allocation, initialization, alignment, provenance, lifetime, and total-size
  precondition; copying afterward cannot repair invalid slice construction;
  and
- the unsafe policy requires one `SAFETY:` form for both unsafe blocks and
  `unsafe fn`, conflating a local proof of an unsafe operation with the public
  `# Safety` contract callers must uphold.

Inspection also found the unchecked signed-to-`usize` size pattern in
`STD-0823`, outside the original `F023` evidence. It must be replaced before
the finding can be resolved. The consistent `# Safety` reminder in
`STD-0716` is not moved by these slices; the Rust unsafe owner will become
canonical for its semantics, and the later Rust API migration must retain only
a link.

## Binding Ownership

| Owner | Authority |
| --- | --- |
| `profiles/boundaries/interop.md` | Generic foreign resource, memory authority, initialization/shutdown, thread, lifetime, and adapter-isolation contracts. |
| `profiles/boundaries/language-bindings.md` | Generic binding-layer separation and the distinction between framework transport support and a concrete ABI representation. |
| `profiles/languages/rust/interop.md` | Rust pointer, slice, checked length, provenance, alignment, initialization, and borrowed-lifetime mechanisms at foreign boundaries. |
| `profiles/languages/rust/security.md` | Rust checked arithmetic and typed rejection for externally supplied sizes before allocation or memory-view construction. |
| `profiles/languages/rust/unsafe.md` | Rust unsafe ownership, local `SAFETY:` rationale, caller-facing `# Safety` contracts, and mechanism-appropriate verification. |
| `profiles/languages/rust/language-bindings.md` | Rust binding DTO classification, checked conversion, framework-specific lifting, concrete C-ABI representation, and conversion tests. |

The generic profiles are accepted before Rust specializations. Rust Interop
owns whether raw foreign memory can be represented safely; Rust Security owns
checked hostile-size conversion; Rust Unsafe owns proof documentation; Rust
Language Bindings owns value representation and conversion. None may redefine
another owner's contract.

## Slice Map

[milestone-7-f022-f023-slices.tsv](milestone-7-f022-f023-slices.tsv) records
the exact frozen identifiers, target owners, proposed final dispositions, and
execution order.

| Slice | Frozen IDs | Outcome |
| --- | --- | --- |
| `7.4b3b` | `STD-0465`-`STD-0472` | Canonical generic foreign-boundary profile. |
| `7.4b3c` | `STD-0483`-`STD-0486` | Canonical generic language-binding profile. |
| `7.4b3d` | `STD-0752`-`STD-0756` | Rust foreign-memory specialization. |
| `7.4b3e` | `STD-0823` | Rust checked boundary-size conversion. |
| `7.4b3f` | `STD-0843`-`STD-0848` | Rust unsafe proof and caller-contract specialization. |
| `7.4b3g` | `STD-0772`-`STD-0775`, `STD-0794`-`STD-0796`, `STD-0801`-`STD-0803` | Rust binding representation and checked-conversion specialization. |

The slices are serial. No unrelated trust-boundary or consolidation slice may
run between them while unsafe foreign-memory and conversion guidance remains
active.

## Slice 7.4b3b: Generic Foreign-Boundary Contract

**Allowed write set:**

- `profiles/boundaries/interop.md` (new canonical profile);
- `INTEROP-STANDARDS.md`;
- `STANDARDS-ROUTER.md`;
- `README.md`;
- `evaluation/standards-effectiveness/fixtures/interop/foreign-memory-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-interop-boundary-policy.sh`;
- this decomposition checker for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, active plan, and execution
  ledger.

No language profile, binding profile, generated inventory, template, lockfile,
or downstream repository belongs to this slice.

**Required semantics:**

- a foreign pointer, handle, buffer, callback, or resource is authority governed
  by an explicit provider/consumer contract;
- allocation identity, initialized extent, access permission, lifetime,
  mutability, thread, and release authority are established before access;
- copying is permitted only after the source memory is valid to read for the
  copied extent;
- initialization and shutdown have explicit owners and idempotency/concurrency
  rules;
- inability to establish required authority returns a typed diagnostic; and
- missing proof cannot fall back to a guessed length, sentinel, copy attempt,
  alternate ownership assumption, or unchecked access.

**Focused evidence:** decisions cover valid and invalid foreign buffers,
partially initialized allocations, expired lifetimes, wrong-thread callbacks,
double release, copy-after-validation, copy-before-validation, and unavailable
authority proof.

**Acceptance gate:** the generic profile routes deterministically, all eight
identifiers have exact dispositions, legacy generic sections are links without
competing rules, and focused plus affected regressions pass.

## Slice 7.4b3c: Generic Language-Binding Contract

**Allowed write set:**

- `profiles/boundaries/language-bindings.md` (new canonical profile);
- `LANGUAGE-BINDINGS-STANDARDS.md`;
- `STANDARDS-ROUTER.md`;
- `README.md`;
- `evaluation/standards-effectiveness/fixtures/language-bindings/representation-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-language-binding-boundary.sh`;
- this decomposition checker for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, active plan, and execution
  ledger.

No language specialization, generated binding, schema, lockfile, or downstream
repository belongs to this slice.

**Required semantics:**

- framework-supported transport or lifting and stable ABI representation are
  separate facts;
- every binding declares its concrete boundary mechanism and representation;
- domain logic remains outside adapters and generated host code;
- conversion rejection is preserved as a typed boundary outcome; and
- unsupported representation cannot fall back to reinterpretation, lossy
  serialization, or a different binding mechanism.

**Focused evidence:** decisions distinguish generated wrappers, serialized
transport, stable C ABI DTOs, opaque handles, unsupported types, and unavailable
conversion capability.

**Acceptance gate:** the generic binding profile is useful without selecting a
language or framework, all four identifiers have exact dispositions, legacy
sections are link-only, and focused plus affected regressions pass.

## Slice 7.4b3d: Rust Foreign-Memory Proof

**Allowed write set:**

- `profiles/languages/rust/interop.md` (new canonical specialization);
- `profiles/languages/rust/README.md`;
- `languages/rust/RUST-INTEROP-STANDARDS.md`;
- `README.md`;
- `evaluation/standards-effectiveness/fixtures/rust/foreign-memory-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-interop-memory.sh`;
- this decomposition checker for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, active plan, and execution
  ledger.

No Rust Security, Unsafe, API, binding, generated, Cargo, or downstream file
belongs to this slice.

**Required semantics:**

- signed and wider dimensions use checked conversion before checked arithmetic;
- raw slice construction proves non-nullness when required, alignment, one
  allocation and provenance, initialized readable extent, non-wrapping total
  size, and a lifetime no longer than the provider guarantee;
- zero-length pointer rules are explicit rather than inferred;
- copying occurs only after safe temporary access is established;
- borrowed foreign memory cannot escape its provider lifetime; and
- failure returns a typed diagnostic without zero-length substitution,
  truncation, saturation, wrapping, or unchecked construction.

**Focused evidence:** Rust decisions cover negative and oversized dimensions,
overflow, null/zero-length combinations, misalignment, split allocations,
uninitialized bytes, stale callbacks, valid copying, and failed proof.

**Acceptance gate:** the Rust profile specializes generic Interop without
duplicating generic ownership, all five identifiers have exact dispositions,
unsafe `as usize`/`unwrap_or(0)` construction guidance is removed, and focused
plus affected regressions pass.

## Slice 7.4b3e: Rust Checked Boundary Arithmetic

**Allowed write set:**

- `profiles/languages/rust/security.md` (new canonical specialization);
- `profiles/languages/rust/README.md`;
- `languages/rust/RUST-SECURITY-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/rust/checked-boundary-arithmetic-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-boundary-arithmetic.sh`;
- this decomposition checker for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, active plan, and execution
  ledger.

No generic Security change, Rust Interop/Unsafe/API/binding file, generated
inventory, Cargo file, or downstream repository belongs to this slice.

**Required semantics:** externally supplied dimensions are checked into the
target integer domain before arithmetic; multiplication/addition and
allocation limits are checked separately; each failure is typed; and no cast,
zero, clamp, saturation, wrapping operation, or smaller default substitutes for
rejection.

**Focused evidence:** decisions cover negative, too-wide, overflow,
resource-limit, valid zero, valid bounded, and typed-error outcomes.

**Acceptance gate:** `STD-0823` has its exact disposition, the legacy example
cannot perform unchecked narrowing before checked arithmetic, and focused plus
affected regressions pass.

## Slice 7.4b3f: Rust Unsafe Contracts

**Allowed write set:**

- `profiles/languages/rust/unsafe.md` (new canonical specialization);
- `profiles/languages/rust/README.md`;
- `languages/rust/RUST-UNSAFE-STANDARDS.md`;
- `evaluation/standards-effectiveness/fixtures/rust/unsafe-contract-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-unsafe-contracts.sh`;
- this decomposition checker for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No Rust API, Interop, Security, binding, Cargo, generated, or downstream file
belongs to this slice.

**Required semantics:**

- each unsafe operation has an adjacent `SAFETY:` rationale proving its
  required preconditions from established facts;
- every public `unsafe fn` has a `# Safety` section stating caller obligations;
- unsafe modules document shared invariants and ownership;
- safe wrappers validate what they can and do not claim to prove caller-owned
  facts;
- verification follows the actual unsafe mechanism and supported environment;
  and
- a safe alternative or feature flag cannot serve as proof for an unsafe path.

**Focused evidence:** decisions distinguish local unsafe-block proof, caller
contracts, module invariants, incomplete comments, safe wrappers, unsupported
verification, and feature-gated unsafe execution.

**Acceptance gate:** all six identifiers have exact dispositions; local proof
and caller contract are distinct and complete; legacy guidance is link-only;
and focused plus affected regressions pass. `F023` is resolved only after this
slice and all preceding F023 slices are accepted.

## Slice 7.4b3g: Rust Binding Representation And Conversion

**Allowed write set:**

- `profiles/languages/rust/language-bindings.md` (new canonical specialization);
- `profiles/languages/rust/README.md`;
- `profiles/boundaries/language-bindings.md`;
- `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md`;
- `README.md`;
- `evaluation/standards-effectiveness/fixtures/rust/binding-conversion-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-rust-binding-conversions.sh`;
- this decomposition checker for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No generated binding, package manifest, lockfile, runtime integration, or
downstream repository belongs to this slice.

**Required semantics:**

- native Rust representation, framework-liftable value, serialized wire value,
  opaque handle, and stable C-ABI representation are distinct categories;
- `String`, `Vec<T>`, `Option<T>`, Rust enums, and framework objects are never
  labeled universally C-ABI-safe;
- narrowing, sign-changing, duration, size, path, enum, and serialization
  conversions use checked/fallible operations whenever the target can reject;
- `From` is reserved for truly infallible conversions; `TryFrom`/`TryInto` or an
  explicit fallible constructor preserves typed failure;
- conversion tests cover success, every rejection class, and the concrete
  native/host boundary; and
- conversion failure cannot fall back to truncation, lossy path conversion,
  default values, JSON-as-universal-ABI, or another binding framework.

**Focused evidence:** decisions cover UniFFI/Rustler lifting versus `extern
"C"`, fixed-width and platform-width integers, `u128` duration narrowing,
non-UTF-8 paths, enums, serialized DTOs, opaque handles, and checked failures.

**Acceptance gate:** `F022` is resolved; all ten identifiers have exact
dispositions; no active or legacy table calls framework-liftable Rust
containers universally FFI-safe; unchecked conversion examples are removed;
and focused plus affected regressions pass.

## No-Fallback And Legacy Rule

Implementation replaces unsafe guidance in place. Legacy documents may retain
concise migration links for moved sections, but not unchecked casts, guessed
lengths, zero-on-overflow behavior, incomplete raw-slice proof, universal
FFI-safe labels, conflated `SAFETY:`/`# Safety` requirements, lossy conversion
defaults, or alternate boundary mechanisms. Missing proof returns a typed
diagnostic.

## Re-Plan Triggers

- Generic memory authority cannot be expressed independently of Rust pointer
  mechanics.
- Framework lifting and concrete ABI representation require a new role or
  precedence level.
- A frozen section must split across owners in a way one disposition cannot
  represent unambiguously.
- Resolving either finding requires generated bindings, package manifests,
  lockfiles, or downstream implementation.
- A required precondition cannot be verified or represented as a typed
  diagnostic.
- Verification cannot distinguish valid copying from copy-after-invalid-access,
  checked arithmetic from checked-multiply-after-cast, or framework support
  from C-ABI safety.
- Existing canonical Contracts, Security, IPC, or Rust profile guidance
  conflicts with the planned ownership.
