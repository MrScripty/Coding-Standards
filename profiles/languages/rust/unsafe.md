# Rust Unsafe Profile

**Standards metadata**

- ID: `profile.language.rust.unsafe`
- Role: `profile`
- Level: `PROFILE`
- Applies when: Rust source contains or exposes an unsafe operation, unsafe function, unsafe trait contract, unsafe implementation, raw resource, or module that owns unsafe invariants.
- Does not apply when: The affected Rust path contains no unsafe contract and does not own facts relied on by unsafe code.
- Requires: `core`, `workflow.verification`, `profile.language.rust`
- Specializes: `profile.language.rust`
- Verification: Rust unsafe-contract decisions plus mechanism-selected dynamic, integration, target, and feature-path evidence.
- Canonical owner: `profiles/languages/rust/unsafe.md`

## Deny By Default

Deny unsafe code by default. Relax that policy only in the smallest crate or
module that explicitly owns a required unsafe mechanism, its invariants, and
its verification.

Safe Rust being inconvenient or slower is not proof that an unsafe mechanism
is required. Record why the selected mechanism cannot meet its contract through
the available safe operations.

## Adjacent Operation Proof

Every unsafe operation has an adjacent `SAFETY:` rationale. The rationale names
the operation's actual preconditions and explains which established facts prove
each one at that point.

A comment that only restates the operation, says a wrapper is safe, or refers
generically to prior validation is incomplete. Link to a shared invariant when
appropriate, but keep operation-specific proof adjacent to the operation.

## Caller Contracts

Every public `unsafe fn` and unsafe trait contract has a `# Safety` section that
states the obligations its caller must establish. Caller obligations and local
operation proof are separate: documentation cannot replace the implementation's
adjacent proof, and local proof cannot omit obligations delegated to callers.

Safe wrappers validate every precondition they own before entering unsafe code.
They cannot claim to prove allocation, provenance, initialization, lifetime,
thread, aliasing, or other facts that remain caller- or provider-owned.

## Module Invariants

An unsafe-owning module documents:

- the shared invariants that make its unsafe operations valid;
- which type, module, crate, provider, or caller establishes each invariant;
- ownership, lifetime, aliasing, mutability, and thread constraints;
- valid state transitions and release behavior; and
- which safe APIs preserve the invariants.

Keep unsafe mechanics out of domain logic. A safe API narrows authority; it
does not erase the proof obligations of the unsafe implementation beneath it.

## Mechanism-Selected Verification

Select evidence from the actual unsafe mechanism and supported environment:

- pure Rust memory and aliasing paths use Miri when the mechanism and target are
  supported;
- concurrent or lock-free paths use the applicable model checker, race
  detector, sanitizer, and stress evidence;
- FFI paths use real provider/consumer contract tests and applicable
  cross-language sanitizers;
- memory-mapped and raw operating-system resources use target integration plus
  applicable memory diagnostics; and
- embedded or `no_std` paths use supported target builds plus emulator or
  hardware evidence required by the contract.

If required evidence cannot run for the selected mechanism or target, record it
as unavailable and keep the acceptance claim partial or blocked. Do not replace
it with evidence for a mock, safe alternative, different target, or disabled
feature.

## Feature-Gated Unsafe Paths

A feature gate may control availability; it does not prove correctness. Test
the unsafe path with the feature enabled and through the real selected
mechanism. A passing default build or safe implementation proves only that
different path.

## No Fallback

Incomplete unsafe proof cannot fall back to:

- a safe-wrapper name or type signature as proof;
- caller documentation without adjacent operation proof;
- adjacent comments without complete caller obligations;
- a feature gate, disabled feature, mock, or safe alternate path;
- verification selected for a different unsafe mechanism or target; or
- an unsupported verifier treated as a passing result.

Keep acceptance partial or blocked until every required proof and evidence
claim is satisfied.

## Verification

Affected checks cover complete and incomplete:

- adjacent unsafe-operation rationales;
- public caller `# Safety` contracts;
- module invariants and ownership;
- safe-wrapper validation without caller-fact overclaim;
- mechanism and environment selection; and
- direct execution of every supported feature-gated unsafe path.
