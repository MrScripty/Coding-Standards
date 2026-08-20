# Concurrent Plan Integration Mechanism Recipes

This document is non-normative. The
[Concurrent Plan Integration profile](../../profiles/workflows/concurrent-plan-integration.md)
owns required behavior. Select a mechanism from the adopting system's supported
authority; do not copy one of these examples as a default.

## Revision Mechanism Examples

A revision token may be:

- a database row or aggregate version checked by conditional update;
- an immutable object identifier;
- a repository revision combined with path-specific content identity; or
- a cryptographic digest over explicitly selected authoritative content.

The mechanism is suitable only when every participating writer can obtain the
admitted token, compare it with current authority at the required gates, and
distinguish stale state without selecting latest, retrying, or merging
automatically.

## Framed Content Digest Example

When an adopting tool specifically selects a content digest, it can avoid
ambiguous concatenation by encoding a versioned scheme, algorithm, canonical
repository-relative paths, explicit presence markers, and length-delimited raw
path and content bytes in canonical order. The selected authoritative files
must be explicit. Timestamps, filesystem metadata, inferred paths, and ledger
narration should not become digest input.

A proposal identity may additionally cover the plan path, operation, actor,
prior revision, scope, write set, prerequisites, intended outcome and state,
resulting revision, and verification contract. This is useful only when a
supported constructor and validator consume the same representation.

These framing details are an illustration, not `workflow.planning` compliance
requirements. An adopter that does not provide the corresponding tool should
select another supported revision mechanism or report the profile mechanism as
`unsupported`.
