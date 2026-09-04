# Policy-Impact V2 Recovered Coverage Certification Evidence

**Status:** `Reviewed`

**Admitted recovery start:** commit
`879c29899a764a7c000542a4f256ce70718656d6`, tree
`bae195b37e07c39e28af7773365b20c65dfa9870`

**Rejected predecessor candidate:** commit
`101001bd2373631b0474d214871ba11ad1b6e4ab`, tree
`955e77e06c2477569da6a6f3f8263c602ca7533d`

**Auditor authority:** `standards.review.audit` supplied by the user-authorized
policy-impact authority v2 continuation.

## Bound Authority

| Authority | Rejected identity | Corrected identity |
| --- | --- | --- |
| Coverage horizon | `sha256:538c9ef051b79129beb5d471394d9c399c7e3c2882567c6aad4c16c1b4d62f43` | unchanged |
| Compiled declarations | `sha256:77d2e5d6c53f8cbdef44dd37c51534a1e0ec690222486f3f255adfa99f030b8c` | `sha256:dde852daaa6bb60d1987f44f46140e9de80cc3bd0c9d6277ec2f7fa037c8a0dd` |
| Policy-impact provider contract | `sha256:2a75ced97772f942b14574aca2c2f4aefca289372269d342c5ab38b25d10df98` | `sha256:e4124f6088b1c21c5e8a7d707cee7f57bb649fb0e6f129b9acaee5f2695899ed` |
| Authoring contract | predecessor candidate content | `sha256:79e3da8c9b146588bff81a1da695a852680425edd68439d57dcea402e9948a4b` |
| Supplemental artifact catalog | `sha256:aff67842c9b61404bc32b0755539b20ada91931912e597354d2b9d426815f620` | unchanged |
| Policy-impact fact schema | `sha256:694b87b31797467a94d0aaacb5a30c40c3ed259fc66e3811172d1c5e4e243884` | unchanged |
| Coverage horizon provider | `standards-analysis:policy-impact-consumer-horizon`, version 3 | unchanged |
| Coverage and attestation contracts | version 2 | unchanged |

The corrected authoring contract replaces nine identical, ineffective
per-relationship-kind evidence booleans with one effective
`required-registered-suite` evidence-owner rule. That rule is validated by the
compiler, participates in relationship dependency identity through the
authoring contract, and requires every declaration to name one registered
suite owner. No optional-evidence mode exists.

## Semantic Preservation

The rejected and corrected compilers were run over their exact repository
trees. A canonical projection included every compiled graph node, group, and
edge; artifact identity and metadata; relationship source, consumer, kind,
applicability program, scopes, propagation, evidence owner, rationale, and
declaration provenance. It deliberately excluded the dependency fingerprints
whose correction is the purpose of this recovery.

Both projections have SHA-256
`410a4d6fcaa3ef2fac61f1c09abafdc9f2e0089dd2147e204067c439375598f6`
and compare byte-for-byte equal. The corrected contract therefore changes the
honesty of compiled dependency identity without changing topology, relation,
target, scope, applicability, evidence ownership, rationale, or public shape.

The admitted transition-provenance projection remains byte-identical with
SHA-256
`b36112c64cb480e9c226bb832ada05577fb2345811bc731c201375b9afaf6b1e`.
It remains generated migration evidence and is not an input to coverage
requirements, attestations, certificates, or analysis identity.

## Coverage Review

1. Resolve every active policy unit from the canonical metadata corpus and
   verify its locator, owner, semantic revision, representation digest, and
   structural digest.
2. Compile every source-owned relationship through the corrected authoring
   contract and inspect its complete typed semantic projection.
3. Execute the complete contract-derived relation/representative-target
   compatibility matrix. Each pairing reaches its exact accepted result or
   typed incompatibility diagnostic without relying on catalog totals.
4. Review the independently derived provider-v3 horizon and its registered
   consumer classes for omitted consumers. Existing declarations and graph
   nodes are not treated as proof of completeness.
5. Derive each coverage authority view and requirement after the corrected
   contract freeze. Replace each stale attestation requirement with the exact
   new handle for the same canonical policy-unit subject.
6. Preserve every prior complete disposition, rationale, explicit-exclusion
   set, and auditor provenance. Only the requirement and evidence-document
   bindings change.
7. Compile generated certificates and compare canonical active-policy-unit,
   requirement, attestation, and certificate subject sets for exact equality.

## Certification Result

Every active policy unit has one current requirement, one complete owner-local
attestation, and one generated certificate. The subject sets are exactly equal.
No stale, duplicate, extra, missing, excluded, unresolved, or blocked subject
remains. Generated certificates are derived proof and are not stored as a
second authority.

The exact clean implementation commit and tree are intentionally not asserted
here because this document participates in attestation evidence and therefore
in the resulting certificate identities. The recovery candidate report binds
the final commit and tree after this evidence, all attestations, and lifecycle
records are complete.
