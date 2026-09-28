# Review-evidence packaging issues and decisions

| ID | Severity / evidence | Owner and boundary | Disposition / verification / revisit trigger |
| --- | --- | --- | --- |
| RP-01 | Required records historically absent from review packets; baseline read from removed diff lines | Packet material selection, not review judgment | Address in P1 with complete primary source/diff and explicit availability. Verify offline recipient access in P2. Do not reopen old acceptances. |
| RP-02 | CI and closure revisions differ from the routing production commit; tools subtree equal, manifests/docs/archive topology differ | Git observation and acceptance owner | Address in P1 with separate revisions, exact limited comparisons and outside-scope differences. Never infer CI applicability. |
| RP-03 | Existing exact Git reader is suitable but generic metadata commands are not a proved local-only packet path | Repository Git public read-only boundary | Resolve during P1 via existing safe primitives or narrow adapter methods; test hostile helper/promisor settings. Unsupported configurations fail before network/object fallback. Replan if global Engine behavior must change. |
| RP-04 | Source/evidence can contain private material, active content or unsafe paths | Operator disclosure and packet I/O | Local explicit selection only; no links, uploads, executable payloads, arbitrary archive extraction or secret-scanner claim. Add path/bounds/side-effect tests. External disclosure is a later authorization. |
| RP-05 | Checksums can be mistaken for authenticated origin or successful evidence | Manifest/checker semantics | Match bytes and expose provenance limits. Imported reports/URLs remain reports/references. Test self-consistent untrusted manifest limits and expected-digest mismatch. No signature service admitted. |
| RP-06 | A package can grow into a provider/plan/acceptance framework | Composition owner | Keep one coherent local assembly scope. Claims are caller associations pointing to the existing plan. Replan for parsing claim semantics, automatic consumer completeness or external execution. |
| RP-07 | Current operator's unrelated uncommitted output-contract work is unavailable | Integration owner | Preserve it. Build against explicit commits; do not infer or copy worktree content. Reconcile actual current files before implementing this plan. |
| RP-08 | Packet code, local-only transport and actual recipient path do not yet exist | Implementation/verification owners | All P-A claims stay pending. Planning schema/probes are not tests of an implementation. Run current locked CI and independent review on the coherent candidate. |
| RP-09 | Partial evidence is legitimate, but partial primary source could mislead | Packet completeness owner | Primary source/diff/plan failures block publication; missing or intentionally linked external evidence yields built-with-gaps. Recipient sees both material scope and limits. |
| RP-10 | Copied evidence could be mutable during collection | External-file reader | Require explicit regular files, bounded stable reads and optional expected hashes; mismatch/unstable acquisition fails rather than blessing mixed bytes. Revisit only for a real streaming-evidence consumer. |

No source-design blocker is demonstrated. These are the concrete implementation
and acceptance responsibilities of the new slice, not unresolved obligations in
the accepted routing-fact or earlier refactoring plans. Broader deferred test
advisories remain priority 3 and are not silently promoted into this write set.

Implementation note (2026-09-28): the owner removed the standalone checker.
RP-05 now concerns the builder's staged integrity validation and honest manifest
semantics. Any references here to checker-specific tests are superseded by the
plan's scope amendment.

## Candidate review findings — 2026-09-28

Two read-only review axes inspected the committed `32e78530...HEAD` change.
The Standards axis found that a well-formed future request version was reported
as `invalid` rather than `unsupported`; request decoding now distinguishes it,
with a focused test. The Spec axis found three gaps: valid revision roles sharing
one commit were rejected, tree IDs were absent, and `INDEX.md` understated ZIP
members while combining changed/context scope without byte totals. The builder
now permits shared exact IDs and empty diffs, records each commit/tree pair, and
prints separate changed/context sections with honest member and payload-byte
counts. Focused tests and the refreshed offline recipient observation exercise
those corrections. These are implementation finding dispositions; the acceptance
owner has not accepted P1 or P2.

## Follow-up code review F1–F4

| ID | Demonstrated boundary | Repair and evidence |
| --- | --- | --- |
| F1 | Output parent could be replaced after pathname admission; analogous evidence-root acquisition used a reopened root path. | Open and hold directory chains; descriptor-relative evidence reads, staging, validation, linking and cleanup. Revalidate requested identities and roll back only the attempt's final link on detected post-link replacement. Deterministic interleavings cover before-create, after-validation, inside-link and evidence-root/ancestor replacement. |
| F2 | A linked worktree's common Git directory was not excluded from output. | Repository Git exposes private/common directories; packet output excludes both. Real linked and separate-Git-dir fixtures exercise positive external output and non-mutating rejection. |
| F3 | Full-name folding missed file/directory and prefix-spelling collisions. | One component-wise namespace check serves collection and staged validation; tests cover both orders, shared directories, case differences and Unicode-equivalent prefixes. |
| F4 | Untracked attributes and local diff settings altered the primary patch. | Opt-in Repository Git exact patch policy fixes formatting, neutralizes configured/global/system attributes and rejects info attributes/custom driver semantics. Tests preserve configuration bytes and prove either identical packet bytes or explicit unsupported rejection. |

All four were reproduced on 6be1d7a0 before repair (five test methods; nine failed
assertions including subcases). Their candidate regression and package outcomes
are in `reports/repair-verification.md`; the original failure log is retained.
No change to the standalone-checker amendment, provider permissions, Engine schema
or the accepted previous work is part of these repairs. The lower-priority
single-module implementation-hash observation is clarified in README; no new
fingerprinting system or performance cache is admitted.

Source implementation now exists; RP-08's planning-era absence is historical, not
the current state. Required exact-candidate locked CI, independent review of the
repairs and owner acceptance remain pending. Original plan/source-review records
are retained rather than relabeled as completed candidate evidence.

F4 direct-consumer completion: `cli.py` now exposes only the new Git owner's fixed
`PATCH_CONFIGURATION` message, retaining its existing result shape and keeping
arbitrary Git stderr private. The actual CLI test verifies the useful rejection,
unchanged source configuration and no output creation. This narrow consumer repair
and its added regression are included in the final 48-test builder pass.
