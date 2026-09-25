# Moved-Policy Sidecar Reuse

**Plan status:** `Verifying`
**Acceptance status:** `pending canonical-compiler and installed-workflow evidence`
**Current phase:** Source correction complete; full-checkout and installed qualification remain.
**Next slice:** Run the supplied canonical compiler regressions in the complete supported checkout, then verify the retained draft through the refreshed MCP.
**Canonical plan:** `docs/plans/moved-policy-sidecar/plan.md`; operation: `continue` the existing registration repair.
**Source baseline:** `MrScripty/Coding-Standards@b14e807e9e129c1226669973cbb425cd0476dde5`.
**Composed-design review:** Applicable and bounded below.
**Execution ledger and evidence:** [verification.md](verification.md).
**Issues:** [issues.md](issues.md).

## Objective

Register a policy in an existing module when its derived declaration file is already registered and stores a policy now owned by another module. Preserve every existing policy identity, owner, scope, revision, alias, lineage record and tombstone. Preserve the original proposal and source bytes outside the explicit candidate.

The reported case is `core.toml` containing `core.simplicity-and-complection`, whose declared module is `topic.code-design`. This is valid existing source, not a request to move that policy back to Core. The generic storage correction applies to any such registered sidecar; repository-specific policy names belong only in the issue evidence.

## Authority And Standards

Apply the current Core, Router, Implementation and Verification workflows and the prospective positive-guidance guide's generic design, proportional scope and code/content separation. Relevant concerns are library behavior, persisted declaration integrity and deterministic replay; public schema, IPC dispatch and authorization contracts remain unchanged. This repair follows the established code workstream rather than revising normative content.

Use the exact published affected-file blobs as the source baseline. The available checkout is partial because direct Git download failed. Any isolated-source observations remain distinct from full-module import, canonical corpus compilation and installed MCP evidence. The current reported live proposal is `503f233b-5c9f-442f-a04f-99f330142bae`, revision prefix `7d21edc9`; it is outside this environment and will not be accessed or changed.

## Binding Design

The policy registry authorizes declaration-file membership. Each active declaration's `module` field identifies its current logical owner. A sidecar filename is a storage convention, not an exclusive ownership assertion.

Keep the existing selection order: reuse a registered sidecar already containing a policy for the requested module; otherwise reuse the registered derived path regardless of the current owners of its surviving declarations; otherwise create a new file only when the derived path is unoccupied. Retain the existing typed rejection for an occupied unregistered path and normal parsing failures.

The selected registered file has already been parsed during the existing scan. Reuse it without rewriting its bytes at selection time. The registration owner continues to append to the complete parsed declaration set and serialize active declarations and tombstones together. No alternative filename allocator, relocation, duplicate declarations, migration, special Core branch or new schema is required.

## Write Set

- `tools/standards_engine/standards_engine/logical_authoring.py`: only `_ensure_policy_sidecar`.
- `tools/standards_engine/tests/test_policy_sidecar_selection.py`: focused storage-selection and preservation regressions.
- `tools/standards_engine/tests/test_policy_registration.py`: real-compiler regressions using synthetic moved-policy storage, including grouped edits and replay.
- This plan directory: scope, evidence, limitations and handoff.
- The generated suite-input manifest, only through its owning generator in a complete checkout. It is not manually rewritten in a partial source tree.

No real standards, declaration files, Router text, registry entries, application approvals, proposal data, generated API contracts or interface versions change. Interface 33 remains the current contract for this correction.

## Design Review

**Independent responsibilities:** registry membership selects eligible storage; declaration fields own logical identity; registration owns append/serialization; the existing compiler owns complete-candidate validation. Their owners remain unchanged.

**Identity and representation:** filename and logical module can diverge after relocation. The existing source demonstrates that divergence. Reusing registered storage preserves identity instead of deriving identity from placement.

**Caller knowledge:** callers still provide module and policy identities/scopes. They gain no filesystem arguments or knowledge of where earlier policies were stored.

**Representative change paths:** registration appends one declaration; movement still updates the selected policy through the existing move path; tombstones remain in their existing file; unrelated module bodies remain unchanged.

**Failure and replay:** invalid input remains owned by the canonical validator; unregistered collisions remain errors. Deterministic selection uses the same registry order in complete and incremental replay. No new accepted baseline or cache authority is introduced.

**Deletion review:** remove the `not units` restriction at the registered derived path. Additional ownership maps, file migrations, compatibility paths or permanent verification machinery supply no deciding value for this defect.

## Implementation Slice

1. Add tests that distinguish the currently failing foreign-owned registered path from an unregistered collision. Demonstrate failure with the exact baseline source.
2. Replace the empty-only reuse condition with registered-path reuse. Keep first-match priority, parsing, collision handling and file creation unchanged.
3. Exercise preservation of foreign-owned declarations, mixed owners, tombstones, existing storage preference, repeated selection and untouched source bytes.
4. Extend the real compiler suite with a synthetic historical-storage fixture, registration plus consumer/provenance, grouped registrations sharing one sidecar, failed-candidate immutability, and full/incremental equality.
5. Review the exact diff, record evidence by claim, and package full changed files with a base-bound patch and checksums. Preserve existing draft/review evidence.

## Acceptance

| Claim | Kind | Environment | Mode | Status |
| --- | --- | --- | --- | --- |
| S1: A registered derived path with foreign-owned active declarations is reusable without selection-time mutation. | focused | deterministic | automated | satisfied at isolated source boundary |
| S2: Existing preference, tombstones, mixed ownership, collision rejection and parse failures remain intact. | focused | deterministic | automated | satisfied at isolated source boundary |
| S3: Canonical registration, relationships/provenance and full/incremental replay preserve old declarations and accepted inputs. | integration | complete supported checkout | automated | pending: complete checkout unavailable |
| S4: The package changes only the admitted files and applies exactly to their verified baseline. | release-artifact | deterministic | automated | satisfied by package reproduction record |
| S5: The installed Engine can advance the retained coordinated draft without the reported projection disagreement. | user-workflow | user's actual installation/store | manual | pending: external installation |

Source-only execution can prove the pure selector's behavior but does not satisfy S3 or S5. Keep the plan `Verifying` where those claims await the supported checkout or the user's installed workflow. Compilation, packaging and syntax results establish their named properties only.

## Handoff

Apply the patch after comparing current local changes, regenerate verification inputs through the existing generator, and run the normal focused and affected integration tests. Restart the MCP server process and reconnect the client so calls execute the corrected implementation; the catalog remains interface 33 because the wire contract is unchanged.

Use the existing proposal store. Inspect the exact saved revision through supported status/resume operations, reconcile any accepted-branch drift, and obtain current analysis/readiness before publication. Preserve historical reviews while letting the Engine identify any newly affected obligations. No database reset, raw store modification, premature application, or automatic new proposal is part of this repair.

## Source Evidence

- `logical_authoring.py`, `_ensure_policy_sidecar`, at the baseline commit: registered derived storage is accepted only when active declarations are empty.
- `evaluation/standards-effectiveness/policy-units/core.toml`: the existing moved policy remains in the registered Core-named sidecar.
- `logical_authoring.py`, `_register_policy_units`: selected active declarations and tombstones are retained and final canonical validation is already present.
- Core/Implementation/Verification at the same commit: bounded write set, coherent repair, preserved authority and claim-specific evidence.
