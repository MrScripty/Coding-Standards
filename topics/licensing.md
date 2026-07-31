# Licensing

**Standards metadata**

- ID: `topic.licensing`
- Role: `topic`
- Level: `MUST`
- Applies when: A change selects, incorporates, adapts, modifies, generates from, redistributes, or publishes third-party code, data, media, documentation, models, or other licensed material.
- Does not apply when: The change uses only material owned by the project and creates no third-party license or notice obligation.
- Requires: `core`, `workflow.verification`
- Specializes: `none`
- Verification: Provenance, license-authority, compatibility, obligation, attribution, and distribution decision fixtures plus affected artifact evidence.
- Canonical owner: `topics/licensing.md`

## Authority And Ownership

Identify the material, source, version or revision, copyright and notice
material, and authoritative license terms before incorporation or
distribution. A repository label, package metadata field, catalog entry,
license name, source comment, or remembered convention is evidence only when
the applicable authority makes it so.

Licensing owns provenance, authoritative terms, intended-use and distribution
compatibility, resulting obligations, and attribution requirements.
Dependencies may use licensing facts when selecting a dependency.
Documentation and Release project accepted notices and obligations into their
owned artifacts; they do not decide compatibility or invent terms.

## Compatibility And Obligations

Evaluate the authoritative terms against the actual activity and artifact:
use, modification, combination, linking, generation, embedding, redistribution,
publication, target recipients, source availability, and other material
conditions. Select only facts applicable to that contract.

Do not infer compatibility from a fixed license-name matrix, labels such as
permissive or viral, a dynamic-versus-static linking slogan, project
popularity, or a prior use in another artifact. When interpretation requires
legal authority beyond the project's accepted policy, record the unresolved
decision and route it to the designated legal or licensing owner.

Record every accepted obligation at the narrowest artifact or distribution
boundary that must satisfy it, including required notices, attribution,
license-text inclusion, source or modification information, offer or
availability duties, and propagation conditions when the authoritative terms
actually require them.

## Attribution And Provenance

Preserve enough provenance to identify the incorporated material and verify
the applicable terms. Place attribution and notices where the authoritative
terms and selected distribution contract require them. Keep adapted scope and
material modifications traceable when needed to distinguish project work from
third-party work or satisfy an obligation.

Do not require one copied file-level or function-level template. Do not omit,
relocate, summarize, or rewrite required legal text merely to fit a preferred
documentation layout. Non-normative examples may illustrate an already
selected obligation but cannot establish one.

## Typed Outcomes

Contradictory source, identity, provenance, or obligation facts are `invalid`.
A well-formed proposed use or distribution that the authoritative terms do not
permit is `unsupported`. Missing source identity, authoritative terms,
required interpretation authority, or obligation evidence is `unavailable`.

Do not continue with guessed terms, a similar license, a package-manager label,
an incumbent attribution, a copied matrix, omitted notices, or default
compatibility.

## Verification

Evidence covers the exact material and revision, authoritative terms, declared
activity and distribution, compatibility decision, applicable obligations,
required notice contents and placement, and the produced artifact or
distribution surface. Negative evidence covers unknown or conflicting
provenance, missing terms, unsupported activity, missing obligations, stale
notices, and attribution attached to the wrong material or artifact.
