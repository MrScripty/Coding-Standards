# Issues and Pending Facts

These are bounded implementation or rollout facts, not claims of newly reproduced production defects.

| ID | Status | Owner | Fact or risk | Disposition and deciding evidence |
| --- | --- | --- | --- | --- |
| PSE-01 | resolved | Integration owner | The actual implementation checkout may differ from inspected `366c1d9`. | Reused branch 41598c4c; only its existing CI workflow differed from inspected main. |
| PSE-02 | partially resolved | Verification owner | Installed local-client qualification remains incomplete. | Hash-locked Python 3.12, official MCP SDK 1.30.0, and a temporary Codex authoring registration passed the candidate workflows. The installed registration now declares authoring purpose and loads tools, but accepted `main` returns `SUPPORT.UNSUPPORTED_CAPTURE`; integration and store disposition remain pending. |
| PSE-03 | resolved | Installation owner | The old store contains ten proposal roots and ten revisions. Five revisions have applied outcomes; five have no readiness, application selection, or application admission. No admitted publication is unresolved. | A verified SQLite backup and per-revision inventory are retained offline at `/home/jeremy/.local/share/standards-engine/archive/old-store-2026-09-23/`. The five deferred drafts are excluded from active cutover; useful intent requires new proposals against accepted standards. No stored records were edited. |
| PSE-04 | known boundary | Content owner | Existing standards contain unreviewed mixed prose. Code alone cannot establish positive application content. | Start the real application-exposure manifest empty; migrate content through the separate guide after code acceptance. |
| PSE-05 | pending | Host owner | An application agent may have independent checkout/store/log access. | Confirm the deployment boundary; Engine-mediated guarantees do not imply OS isolation or context erasure. |
| PSE-06 | implemented | Authoring owner | Prompts/templates and whole-module rewrites must be editable through the final Engine contract. | Runtime and tested operation map include scope_updates and registered prompt/template editing; independent C10 review remains pending. |
| PSE-07 | resolved for selected source checks | Verification owner | Existing failures could mask a changed claim. | Final selected runs pass after recorded fixture and implementation repairs. Full supported-environment qualification remains PSE-02. |

No item authorizes unrelated repository cleanup or a normative-content change during code implementation. Block only the dependent action when its required fact is unavailable.

## Delivery and review

Remote Git transport is unavailable; the user explicitly selected a ZIP fallback.
Local Git CLI commits and the exact base remain the delivery authority.
Independent material review and actual installation/store cutover are pending;
source tests and synthetic reviews do not claim them.
