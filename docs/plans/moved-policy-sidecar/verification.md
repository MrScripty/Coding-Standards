# Moved-Policy Sidecar Repair: Execution And Verification

**Source implementation:** Complete for the bounded selector correction.
**Plan status:** `Verifying`; canonical-compiler and installed-workflow evidence remain outstanding.
**Baseline:** `b14e807e9e129c1226669973cbb425cd0476dde5`, implementation branch.

## Source And Preserved State

The two existing changed files were recovered from the prior delivery ZIP and verified against their current published Git blob identities:

| Path | Baseline Git blob |
| --- | --- |
| `tools/standards_engine/standards_engine/logical_authoring.py` | `a4127709eb3d07c64983ca075bba0f5d3b3f6363` |
| `tools/standards_engine/tests/test_policy_registration.py` | `41ab191ca3a7b385fa0018c82cbcf0958b39f3a9` |

The observed `core.toml` declaration was also retained as verification evidence and matches blob `8f3cb702ed8579237ec962c7277b288292905ae2`. It is not included as a replacement repository file. Its policy `core.simplicity-and-complection` declares module `topic.code-design` and semantic revision 2.

Direct Git transport failed DNS resolution. Prior archives supplied the affected files, but not a complete repository. The local packaging Git baseline is synthetic and is not presented as the user's actual Git history. The package manifest identifies the real source baseline and exact changed-file inputs.

The user's store, proposal `503f233b-5c9f-442f-a04f-99f330142bae`, draft revision prefix `7d21edc9`, approvals and independent review were not accessed or modified. Real normative prose, policy declarations, registries, Router text and exposure records remain unchanged.

## Correction

`_ensure_policy_sidecar` now reuses the registered derived sidecar when no registered sidecar already contains a declaration for the requested module. Active declarations for other modules no longer make that registered file unavailable.

The existing scan still parses the registered file. Existing matching-owner preference, unregistered-path collision rejection and new-file registration remain unchanged. Selection writes no existing file. Registration keeps its existing append/serialization path, which carries all active declarations and tombstones into the candidate.

An AST comparison establishes that the only changed production function is `_ensure_policy_sidecar`. There is no Core-specific branch, new filename scheme, file relocation, policy renaming, identity migration or schema change. Interface 33 and persisted representations are unchanged.

## Executed Evidence

| Observation | Result | Boundary |
| --- | --- | --- |
| Ten new focused selector/serialization regressions against original source | Four cases fail with `AUTHORING.PROJECTION_DISAGREEMENT`; six pass | Exact selected production function bodies; package imports excluded |
| The same ten regressions after correction | Ten pass | Same source-level boundary and unchanged test assertions |
| Previously supplied isolated registration-mechanism probe | Nine pass | Supporting only: the probe substitutes metadata resolution/validation |
| Syntax compilation of the three changed/new Python files | Pass on available Python 3.13.5 | Syntax, not runtime integration |
| Python 3.11 grammar parsing of the same files | Pass | Grammar only; not execution on Python 3.11 |
| Production AST scope comparison | Pass | Only the admitted selector changes |
| Full compiler integration test invocation | Collection fails: `tools.standards_engine.standards_engine.authoring` is absent | No canonical compiler tests are claimed as executed |
| Patch reproduction, hashes and archive integrity | Recorded in package verification artifacts | Changed-file packaging, not installation |

The focused source runner executes the actual AST bodies of the selector and its TOML/registry helpers with the same checked-in test assertions. Error definitions are a retained excerpt from the same published revision. It does not load the full authoring module, metadata validator, graph, store or MCP. These limits are explicit; passing those ten tests is not presented as a full Engine run.

No network calls, fabricated module implementations or fallbacks were added to production. The supplementary source runner is a package-local diagnostic, not a new permanent repository verification framework.

## Integration Regressions Added, Not Executed Here

`test_policy_registration.py` gains a synthetic legacy-storage fixture. It creates two modules through the actual logical compiler, retains the second module's policy declaration in the first module's sidecar, refreshes fixture inputs using the owning projector, and recompiles that frozen fixture with the real Engine. No fixture creation touches real accepted source or the user's store.

Four tests then cover:

- Registration while preserving the moved policy, its alias, registry membership and both module bodies.
- Grouped registrations for two logical owners that share a physical sidecar, independent of request order.
- A same-candidate module rewrite, registration, consumer relationship and provenance record without losing the moved declaration.
- Full/incremental replay agreement, plus failed-suffix preservation of original and predecessor material.

The pure selector suite additionally covers tombstones, mixed logical owners, existing matching-owner preference, empty storage, repeated selection, malformed files and unregistered occupied paths.

## Remaining Acceptance And Resume

S1 and S2 have focused source-level evidence; S3 requires the full canonical compiler and replay checks; S4 is established by the package reproduction record; S5 requires the actual installed workflow. The plan remains `Verifying` until the latter claims are established at their named boundaries.

Apply and verify the patch in the complete checkout, refresh generated verification inputs through the existing owner, and restart the MCP server process before reconnecting. A catalog reporting interface 33 identifies the wire contract, not the implementation revision; qualify the corrected behavior itself.

Inspect and resume the exact preserved proposal through supported operations. Follow any current stale-base or review obligations. Retained material review remains useful evidence, while readiness and publication remain the existing Engine's responsibility. This package does not authorize or attempt real standards publication.
