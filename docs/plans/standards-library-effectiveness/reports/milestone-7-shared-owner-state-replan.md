# Milestone 7 Shared Owner State Replan

## Problem

The immutable execution train can record one proposed owner as historically
missing in multiple rows. Once an earlier row creates that owner through an
authorized decomposition transition, later pending rows must observe current
filesystem truth without being treated as semantically complete.

Row-local reconciliation rejected this valid state for
`reference/patterns/architecture.md`: row 36 completed the one creation
transition, while rows 37, 39, and 40 retained historical `missing` values.

## Selected Contract

Owner creation is owner-scoped and semantic completion remains row-scoped.

- Preserve immutable baseline owner state as historical evidence.
- Permit exactly one declared `missing-to-exists` transition per owner.
- Mark current owner state as existing only after every identifier in the
  creation child has a disposition and the owner exists on disk.
- Let later rows naming that owner inherit current existence only.
- Retain each later row's activation, ordering, semantic decomposition,
  dispositions, and package gate independently.
- Reject premature presence, missing completed owners, repeated transitions,
  transition from an existing baseline owner, and filesystem disagreement.

No registry or second mutable source of truth is introduced. The verifier
derives declared and completed owner transitions from the existing
decomposition overlay while traversing the immutable train in order.

## Bounded Write Set

This repair may touch the execution-train verifier, owner-transition fixture
and verifier, row 36 decomposition evidence and checker, active plan, and
ledger. It must not touch normative standards, reference content, legacy
sources, dispositions, generated inventories, the immutable train, package
manifests, templates, configuration, lockfiles, or downstream repositories.

## Verification

Focused evidence covers first creation, pending creation, inherited completed
creation, inherited pending creation, undeclared presence, premature presence,
missing completed owners, duplicate transitions before and after completion,
and transition attempts for historically existing owners.

Because the execution-train verifier is shared migration infrastructure, its
self-tests, row 36 checker, plan structure, shell syntax, diff integrity, and
the complete fail-fast standards suite are required before acceptance.

## Re-plan Triggers

Stop if the repair requires changing immutable train rows, introducing a
mutable owner-state registry, repeating a creation transition, inferring
semantic completion, changing package membership, or weakening filesystem
consistency.
