# Historical Git Reachability Recovery Issues

| ID | Status | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| HGR001 | Resolved | Critical | Pruning stale worktree registrations removed the only local reachability root for 147 detached heads; at least 11 were already classified as unique. | Exact recovery refs protect all 208 recorded detached heads, including all 147 registration-only heads. |
| HGR002 | Resolved | High | The accepted cleanup plan simultaneously excluded and authorized unique-commit retirement. | Replaced superseded objective, scope, criteria, milestone, and report claims with the actual authorized outcomes. |
| HGR003 | Resolved | High | `git fsck --no-dangling` was recorded as reachability proof even though it suppresses dangling reporting and checks object integrity. | Replaced the claim with explicit protected-OID/ref comparison and documented the distinction. |
| HGR004 | Resolved | High | Commit fixtures authorize any stale-registration prune without head-reachability or commit-disposition evidence. | Added explicit inputs and removed, archived, retained, discard-authorized, and refusal outcomes. |
| HGR005 | Resolved | Medium | Migration checkpoint policy has no cumulative-risk trigger between routine packages. | Added an evidence-based cumulative trigger without restoring per-package mixed checkpoints or a hardcoded package count. |
