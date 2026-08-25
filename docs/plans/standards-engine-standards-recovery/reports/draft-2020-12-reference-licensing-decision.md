# Draft 2020-12 Reference-Only Licensing Decision

## Decision

The standards-recovery work may select the published JSON Schema Draft 2020-12
Core and Validation documents as third-party reference authority for one
bounded historical A1 conformance comparison.

The admitted activity is reference and citation only. No specification file,
schema, test corpus, test vector, executable, code component, excerpt, adapted
text, or dependency is incorporated into or redistributed with this
repository.

## Material And Authority

| Field | Decision |
| --- | --- |
| Material | JSON Schema Core and Validation, Draft 2020-12 |
| Published identity | `draft-bhutton-json-schema-01`, published 16 June 2022 |
| Core source | <https://json-schema.org/draft/2020-12/json-schema-core> |
| Validation source | <https://json-schema.org/draft/2020-12/json-schema-validation> |
| Selected clauses | Core section 4.2.2, Instance Equality; Validation section 6.4.3, `uniqueItems` |
| Copyright authority | The publication's copyright notice identifies the IETF Trust and the document authors. |
| Terms authority | The publication states that it is governed by BCP 78 and the [IETF Trust Legal Provisions](https://trustee.ietf.org/license-info) in effect on its publication date. It separately identifies Revised BSD terms for extracted Code Components. |

The official published URLs and publication identity are used instead of a
moving repository branch. The historical reproduction report must preserve
these identifiers and exact section references.

## Intended Use

The recovery compares existing accepted A1 inputs and outputs with the
behavior specified by the selected clauses. It records the expected behavior,
actual behavior, and known disagreement in project-authored words.

The recovery does not reproduce the specification text, derive a repository
fixture from an upstream example, execute an upstream test suite, or extract a
Code Component. The specification remains externally resolved reference
authority.

## Compatibility And Obligations

For this reference-only activity:

- retain the title, published identity, authoritative URLs, selected sections,
  copyright authority, and terms authority in the reproduction evidence;
- attribute the behavioral expectation to the selected specification rather
  than presenting it as project-authored semantics;
- do not imply endorsement by the IETF Trust, document authors, or JSON Schema
  organization;
- do not add a copied license, notice, specification, schema, or test artifact
  because none is incorporated or redistributed by the admitted activity; and
- reopen Licensing review before any copying, adaptation, extraction,
  generation from, incorporation, or redistribution of third-party material.

This decision does not interpret rights for a future dependency, validator,
test corpus, or A1b implementation. Each such selection would require its own
source, terms, compatibility, obligation, and distribution decision.

## Verification

Milestone 0 evidence must show that repository changes contain only
project-authored reproduction records and citations. Diff inspection must
confirm that no third-party content or dependency entered the tree. The final
coverage and disposition audit must review `topics/licensing.md` and confirm
that the activity did not expand beyond this decision.
