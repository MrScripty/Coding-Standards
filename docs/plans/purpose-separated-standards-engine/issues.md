# Issues and Pending Facts

These are bounded implementation or rollout facts, not claims of newly reproduced production defects.

| ID | Status | Owner | Fact or risk | Disposition and deciding evidence |
| --- | --- | --- | --- | --- |
| PSE-01 | resolved | Integration owner | The actual implementation checkout may differ from inspected `366c1d9`. | Reused branch 41598c4c; only its existing CI workflow differed from inspected main. |
| PSE-02 | resolved | Verification owner | Installed local-client qualification was required. | Hash-locked Python 3.12 and official MCP SDK 1.30.0 passed candidate publication/recovery; the installed Codex authoring registration passed catalog/schema/route/read after accepted-main integration and fresh-store activation. The application CLI returns the expected content-unavailable result. |
| PSE-03 | resolved | Installation owner | The old store contains ten proposal roots and ten revisions. Five revisions have applied outcomes; five have no readiness, application selection, or application admission. No admitted publication is unresolved. | A verified SQLite backup and per-revision inventory are retained offline at `/home/jeremy/.local/share/standards-engine/archive/old-store-2026-09-23/`. The five deferred drafts are excluded from active cutover; useful intent requires new proposals against accepted standards. No stored records were edited. |
| PSE-04 | known boundary | Content owner | Existing standards contain unreviewed mixed prose. Code alone cannot establish positive application content. | Start the real application-exposure manifest empty; migrate content through the separate guide after code acceptance. |
| PSE-05 | known host boundary | Host owner | An application agent may have independent checkout/store/log access. | Engine-mediated guarantees apply to its interface; deployers must keep private files and diagnostics outside an application agent's independent reach. Application exception diagnostics now omit exception text and tracebacks. |
| PSE-06 | accepted | Authoring owner | Prompts/templates and whole-module rewrites must be editable through the final Engine contract. | Runtime and tested operation map include scope_updates and registered prompt/template editing; independent C10 review found no substantive spec mismatch. |
| PSE-07 | resolved | Verification owner | Existing failures could mask a changed claim. | Complete pre-repair run passed 477 tests; focused post-fix tests passed, and 73 structural checks passed after refreshing generated inputs. The interrupted post-fix full repeat is recorded in implementation evidence. |

No item authorizes unrelated repository cleanup or a normative-content change during code implementation. Block only the dependent action when its required fact is unavailable.

## Delivery and review

Remote Git transport is unavailable; the user explicitly selected a ZIP fallback.
Local Git CLI commits and the exact base remain the delivery authority.
Independent Standards and Spec reviews and the local installation/store cutover
are complete. Remote publication remains separate from this local acceptance.
