# Library Application Profile

**Standards metadata**

- ID: `profile.application.library`
- Role: `profile`
- Level: `PROFILE`
- Applies when: The changed artifact is a reusable library, package, crate, SDK, or library module.
- Does not apply when: The changed code is only an application entrypoint or user interface.
- Requires: `core`
- Specializes: `none`
- Verification: Library-focused tests and any real consumer contract selected by routing.
- Canonical owner: `profiles/applications/library.md`

## Ownership

- Keep reusable behavior independent of application startup, UI, transport, and
  process-global lifecycle unless the library's contract explicitly owns them.
- Expose the smallest coherent API that preserves domain types and failure
  meaning.
- Keep internal modules internal. Do not create a public compatibility burden
  solely to ease tests or wiring.

## Consumer And Compatibility Conditions

- Internal library modules released with all callers may change in a
  coordinated slice.
- Public packages, independently deployed consumers, generated bindings, and
  persisted formats require their routed contract/versioning guidance.
- A repository containing a library does not imply every internal symbol is a
  public contract.

## Verification

- Local deterministic behavior requires focused regression tests.
- Public API behavior requires tests through the public API.
- Real downstream consumers require contract or integration evidence when their
  boundary changes.
- Do not select launcher, frontend, release, or packaging guidance unless the
  task actually affects those concerns.

## Dependencies

- Keep runtime/framework dependencies out of the reusable core unless its
  contract requires them.
- Add optional features only for real consumer configurations.
- Test supported feature combinations; do not require an impossible
  all-features build when features are intentionally exclusive.
