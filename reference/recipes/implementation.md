# Implementation Recipe

**Standards metadata**

- ID: `reference.recipes.implementation`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A contributor needs an example that transports already selected implementation or review evidence.
- Does not apply when: Change context, review evidence, acceptance, provider, or template requirements are being decided.
- Requires: `workflow.implementation`
- Specializes: `none`
- Verification: Implementation-reference dispositions, metadata, links, and authority checks.
- Canonical owner: `reference/recipes/implementation.md`

This material is non-normative. The
[Implementation Workflow](../../workflows/implementation.md#change-description-evidence)
must select required evidence and its owner before an example is adapted.

## Pull-Request Template Example

A project that has selected GitHub and a pull-request template might place a
project-owned template with commands such as:

```bash
mkdir -p .github
cp templates/PULL_REQUEST_TEMPLATE.md .github/PULL_REQUEST_TEMPLATE.md
```

Illustrative headings could include Problem, Constraints, Rationale,
Alternatives, Behavioral Effects, and Verification. Include only selected facts;
do not create empty sections or checkboxes as proof.

The provider, `.github` location, source template, destination name, commands,
headings, and checklist structure are examples only. They define no fallback
review process or evidence contract.
