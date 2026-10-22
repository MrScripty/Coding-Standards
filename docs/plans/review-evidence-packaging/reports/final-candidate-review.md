# Independent packaging candidate review — 2026-09-29

**Candidate:** `91ceb0fedcd6bb23513cf414a60b1e506d7de893`.
**Review range:** `6be1d7a0..91ceb0fe` for F1–F4, with the final F4-C1
correction checked against `143c8de1..91ceb0fe`.
**Reviewer:** separate read-only agent `packaging_review`; recommendation only.

The reviewer found no concrete implementation or standards blocker. F1 retains
directory descriptors and identity checks through evidence reads and output
publication; F2 excludes private and common Git administrative directories; F3
checks the portable component namespace; F4 fixes the local exact-patch
environment and rejects unsupported overrides. F4-C1 sets
`core.ignoreCase=false` for the owned patch command only. Direct Git and actual
CLI tests distinguish lowercase textual content from an exact-case binary
attribute match and check unchanged source, index, refs, request, and repository
configuration. The packet and manifest remain byte-identical across the tested
configuration values.

**Recommendation:** the bounded source candidate is suitable for acceptance
review. This review does not qualify the supported locked runtime or grant
acceptance. The accepted plan status remains the acceptance owner's decision.
The Linux/configuration tests do not claim coverage of a case-insensitive
filesystem or every Git setting. The first offline packet's unavailable raw CI
log and referenced CI URL remain visible as material gaps, not invented evidence.

Existing local evidence is in [repair verification](repair-verification.md) and
[case-policy verification](attribute-case-verification.md). The separately
recorded exact-source workflow `36509340996` has a completed/successful Engine
job; source identity and claim applicability remain as bounded in the plan.
