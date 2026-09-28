# Offline recipient observation — 2026-09-28

Built the published routing example request with the local builder and wrote the
handoff ZIP outside the repository at
`/tmp/review-evidence-routing-recipient-v4.zip`. The request names the
baseline `ff2e13ed31a42dbe6cc70ee76f7e7a7e58eabe76`, candidate
`09d7829df79d2e0c25b8fb9add4b7c47d6368684`, CI subject
`39d44f007c36684e1ebc546f31a19e20e2e660e5`, and later records
`32e78530096f2884d4c77e0a5a02a0de2ff869fe`. The ZIP is a developer
handoff artifact, not a tracked repository file.

A separate Python standard-library process opened only the finished ZIP. It did
not import the builder or read the source repository. It found 98 ZIP members,
54 selected primary/context paths, 49 changed primary paths, a 1,083,975-byte
complete patch, 5,704,505 included payload bytes (excluding index and manifest),
and 96 index links; all 96 links resolve to ZIP members. The generated index
correctly reports 98 total file members and separates changed files from context. The
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
`sha256:48060851b6a3373fe2071431a0a35bbb3e07442533a3d288c3fef87233f35574`.
The manifest also records distinct commit/tree pairs for all four roles. Its
recorded trees are baseline `6d1f1f8a33d4391c9ab8e315b18bfc25603e1b97`,
candidate `dffce50ba13e17bc6e55155ca2679a3742f3f658`, CI
`ca0e6c212003fff0d8be2c3d73f2a07b3897bfdd`, and records
`08759cc18fd2973c105743e050746996fbb67308`.
The builder source digest recorded in that manifest is
`sha256:c76843abc8b52bf46065d8382a7e4c5a01088508c398ee4ee899a2185ef70029`.
The `tools/` comparison equals the candidate for both CI and record revisions,
while the full metadata inventories retain three and ten paths outside that
selected scope. No CI success, broader applicability, review finding, or acceptance
is inferred from those byte observations.

This observation checks offline navigation and explicit gaps. It does not replace
independent source review, exact-source CI, or the acceptance owner's disposition.
