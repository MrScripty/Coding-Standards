# Milestone 7 Declared Navigation Route Admission

The nine-index correction is published by the Engine in `67d3e205`, following
capability commit `c99773d8`. Its exact candidate passed 73 suites and 121 checks.
All nine accepted reads match their reviewed previews; the other eighteen
entrypoints and all 70 canonical modules are unchanged.

Full-population path/heading inspection found one additional stale route in a
retained entrypoint: `CODING-STANDARDS.md` links to
`CORE-STANDARDS.md#code-and-terminology-discipline`. Core no longer owns that
heading. The current owner is `topic.code-design`, which contains Code And
Terminology Discipline.

The stale link is not a required inventory member. Coding's current coverage
inventory protects seventeen other routes, including section destinations.
A plain whole-standard rewrite would omit those required sections. A passing
structural checkpoint therefore neither discovers this stale fragment nor
permits dropping the other declared routes.

## Bounded Correction And Capability

Extend the existing `rewrite-navigation-index` renderer to preserve captured
required section routes when their canonical owners are explicitly selected.
Continue to accept only the snapshot-bound entrypoint handle, canonical owner
IDs, and existing rationale/evidence. No new edit type, tool, caller-supplied
Markdown, path, URL, slug, or inventory mutation is needed.

The Engine captures the current source-closure route inventory, resolves its
canonical owners, preserves their exact declared destinations in the rendered
index, and binds the declarations and owner content into index review evidence.
Reject omitted required owners and required artifact routes outside the
supported canonical-standard selection. Do not infer a missing owner selection
or change a coverage claim to make a candidate pass. Preserve the route
inventory and all coverage checks unchanged.

Older captured authority without this inventory retains its prior capability;
never read the current worktree to augment it. Preserve fingerprints for indexes
without declared inventory routes, including the nine just published.

Rewrite only the additional Coding index, explicitly selecting its existing
canonical owners plus Code Design. Its seventeen declared routes remain
protected. The unlisted obsolete anchor disappears with the old index content.
Retain the other seventeen entrypoints. Do not add general section authoring,
artifact authoring, or route-level mutation for this correction.

## Composed Design And Write Set

The existing navigation-authoring admission's architecture probes still apply:
canonical owners retain meaning; navigation owns selected routes and rendering;
Analysis owns review; repository Git owns publication. The added authority is
the current declared route inventory and the owners those routes name. Callers
continue to supply canonical IDs without learning table or Markdown mechanics.
Missing selections produce typed failure rather than inferred applicability.

Implementation is confined to the Engine navigation module, focused navigation
fixtures, the authoring reference and contract documentation, and this plan
bundle. No Analysis decision algebra or public contract shape changes. The
current route inventory remains unchanged; generated verification inputs are
refreshed through the Engine.

Require a complete protected-route rewrite test, preserved declared section
links, mandatory review, real verification/application, omitted-owner and
unsupported-artifact rejection, and unchanged-inventory assertions. Keep the
navigation fixture independent of obsolete text in the live repository.

Commit the capability before using it to rewrite the live Coding index. Then
repeat the 27-entrypoint link audit and current checkpoint. Milestone 7 and A2
remain open until the additional correction; downstream pilots and A5 concision
remain separate work.

## Implementation Evidence

The renderer now captures and preserves declared section routes for explicitly
selected owners, with no contract-shape or operation-count change. Required
artifact routes remain explicitly unsupported. The fixtures create their own
obsolete input instead of depending on errors remaining in the live library.

All fourteen navigation tests pass, including complete verified application,
unchanged inventory, omission rejection, unsupported artifacts, frozen capture,
and owner/declaration fingerprint binding. All fourteen focused MCP and cold
snapshot/replay tests pass. Ruff, skill validation, and the current Engine
checkpoint pass; the checkpoint covers 73 suites and 121 structural checks.

The additional live Coding correction remains the next slice. Its bounded
read-only inline-consumer scan found no tracked Markdown link targeting the
Coding entrypoint. This does not certify external bookmarks or undeclared
consumers, and the retained entrypoint path remains available.
