# Offline recipient observation — 2026-09-28

Built the published routing example request with the local builder and wrote the
handoff ZIP outside the repository at
`/tmp/review-evidence-routing-recipient-v2.zip`. The request names the
baseline `ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76`, candidate
`09d7829df79d2e0c25b8fb9add4b7c47d6368684`, CI subject
`39d44f007c36684e1ebc546f31a19e20e2e660e5`, and later records
`32e78530096f2884d4c77e0a5a02a0de2ff869fe`. The ZIP is a developer
handoff artifact, not a tracked repository file.

A separate Python standard-library process opened only the finished ZIP. It did
not import the builder or read the source repository. It found 98 ZIP members,
54 selected primary/context paths, 49 changed primary paths, a 1,083,975-byte
complete patch, and 96 index links; all 96 links resolve to ZIP members. The
exact governing plan is at `records/governing-plan/plan.md`. Both versions of
`tools/standards_engine/standards_engine/_generated_contract.py` are present:
598,325 baseline bytes and 599,254 candidate bytes, each with a readable tail.
Their packet SHA-256 values are respectively
`f22a3791b1e3ee80f9846273f7dea3c2b169a556f029a10c2ba0c6b2afa7c6d8`
and `af70a74f6f00ffccffcb378dfe9aad4c30626edecc27c1ad408f7d1afc135797`.

The manifest identifies five included later records: accepted plan, verification,
external review, live observation, and issue dispositions. The requested raw CI
log is `missing`; the CI URL is `referenced`, with no included bytes. The builder
reported `built-with-gaps`, exit 1, and manifest digest
`sha256:c653dfc5938eb61dd6655265bfb18dcaa6a4066898ea2c2d3c2430b17a564df3`.
The builder source digest recorded in that manifest is
`sha256:18be0b691579c366209e05ea5604c608f362ee00234cb327ddc858c5a2085043`.
The `tools/` comparison equals the candidate for both CI and record revisions,
while the full metadata inventories retain three and ten paths outside that
selected scope. No CI success, broader applicability, review finding, or acceptance
is inferred from those byte observations.

This observation checks offline navigation and explicit gaps. It does not replace
independent source review, exact-source CI, or the acceptance owner's disposition.
