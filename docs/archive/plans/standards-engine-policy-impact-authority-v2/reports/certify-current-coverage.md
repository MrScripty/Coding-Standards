# Policy-Impact V2 Current Coverage Certification Evidence

**Status:** `Reviewed`

**Frozen base:** commit
`e6d075b5fbc1558e69ff7aa3c6779d31b07142e8`, tree
`650493a43a34de541ccc4906604219f3b0065e17`

**Auditor authority:** `standards.review.audit` supplied by the user-authorized
policy-impact authority v2 continuation.

## Bound Authority

| Authority | Exact identity |
| --- | --- |
| Coverage horizon | `sha256:538c9ef051b79129beb5d471394d9c399c7e3c2882567c6aad4c16c1b4d62f43` |
| Compiled declarations | `sha256:77d2e5d6c53f8cbdef44dd37c51534a1e0ec690222486f3f255adfa99f030b8c` |
| Policy-impact provider contract | `sha256:2a75ced97772f942b14574aca2c2f4aefca289372269d342c5ab38b25d10df98` |
| Authoring contract | `tools/standards_policy_impact/contracts/policy-impact-authoring-v2.toml` |
| Horizon provider | `standards-analysis:policy-impact-consumer-horizon`, version 3 |
| Coverage and attestation contracts | version 2 |

The frozen input closure includes the canonical module and policy-unit corpus,
the complete registered suite catalog and suite inputs, the edge-source
registry, supplemental artifact catalog, compiled relationship declarations,
registered prompts, templates, documentation, references, fixtures, and
implementation/evidence artifacts. Horizon membership and each member's
relevant content fingerprint are bound by the horizon digest. Attestation
instances, reports, timestamps, and display-only governance text do not enter
coverage identity.

## Review Method

1. Resolve every active policy unit from the canonical metadata corpus and
   verify its locator, owner, semantic revision, content digest, and structural
   digest.
2. Compile every source-owned relationship through the version 2 authoring
   contract and inspect its source, target, typed relationship kind,
   applicability program, evidence owner, and declaration provenance.
3. Compare the compiled relationship identity set with the admitted migration
   inventory by exact source/consumer keys. No edge total is used as an oracle.
4. Review the independently derived horizon and its registered consumer
   classes for omitted consumers. Existing declarations and the supplemental
   node catalog are not treated as proof of completeness.
5. Inspect the final selected consumers for every active subject, including
   subjects with no declared outgoing relationship. No missing consumer,
   unresolved identity, unsupported relationship, or unaudited exclusion was
   found.
6. Derive each coverage requirement from the frozen view. Requirement handles
   are recorded in the M0 candidate and re-derived before attestation authoring;
   the sets are identical.

## Subject Disposition

Every active policy unit in the frozen corpus has disposition `complete`. The
owner-local attestation files contain exactly one record for each mechanically
derived requirement:

- `topic.architecture`;
- `workflow.commit`;
- `topic.contracts`;
- `topic.dependencies`;
- `profile.boundary.generated-contract`;
- `workflow.planning`;
- `router`; and
- `workflow.verification`.

There are no explicit exclusions. If any source, policy unit, relationship,
suite registration, horizon member, content fingerprint, contract version, or
provider identity changes, these attestations must fail exact requirement
matching and be reviewed again. Generated certificates remain derived proof;
they are not authored authority and are not stored as a second declaration.

## Mechanical Certification Result

Coverage compilation over the frozen authority proved exact equality of the
active policy-unit, requirement, attestation, and generated-certificate subject
sets. Each subject has one record in each derived set, and every attestation
names the exact requirement handle produced for that subject. No stale,
duplicate, extra, missing, excluded, or blocked subject remains.

The transition-provenance projection was regenerated independently from the
bound predecessor commit and current frozen corpus. Its bytes match the
admitted artifact with SHA-256
`b36112c64cb480e9c226bb832ada05577fb2345811bc731c201375b9afaf6b1e`.
That projection is not an input to requirement, attestation, certificate, or
analysis identity.
