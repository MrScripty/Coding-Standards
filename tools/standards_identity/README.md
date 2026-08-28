# Standards Identity

`standards_identity` encodes immutable JSON-compatible identity values without
Unicode normalization and produces domain-separated SHA-256 identifiers.

Domain modules own field selection, semantic normalization, ordering, and
deduplication. This module accepts only `None`, exact Booleans, exact integers,
Unicode-scalar strings, `IdentityArray`, and `IdentityObject` values. Mutable
containers and floating-point values are invalid.

```python
material = IdentityObject(
    (
        ("policy", "workflow.planning.plan-admission"),
        ("revision", 2),
        ("selectors", IdentityArray(("prompt", "template"))),
    )
)
identifier = hash_identity(
    "coding-standards:policy-unit:v2",
    "policy-unit",
    material,
)
```

`encode_identity_value` exposes the exact identity-v2 value encoding for owner
codecs. Raw-content digests remain SHA-256 over raw bytes and do not use this
module.
