# Git Commit Message History Repair

## Scope And Authority

On 2026-08-29 the repository owner explicitly requested systematic repair of
missing commit-message bodies. A fresh fetch confirmed `origin/main` at
`933c9ab93d18ede987d449a6fe7b9ebd313922fc`; all 136 descendant commits were
local and unpushed. Only `main` and one worktree existed, with no tags, merges,
dependent branches, or dirty state.

The audit found 83 commits with an existing subject and an empty body. The
first was `e742b0f4876915d3f9330333d23e03b8016e6229`, whose parent is
`879475365ea43c8962dbb319347e80cff665a87d`. Rewording that commit necessarily
replaced its 91-commit descendant chain. The earlier 45 local commits were left
untouched.

## Repair Method

Each missing body was written from the corresponding contemporaneous plan,
ledger, issue, report, diff, and acceptance evidence. Existing subjects were
not rewritten. The eight descendants that already had bodies retained their
complete messages unchanged.

The exact original-to-replacement mapping is recorded in
[the lineage map](git-message-history-repair.tsv). Every mapped row retains the
same tree and subject. The original tip
`befab13354778444cd76fd686e229c6bc1178862` remains protected at
`refs/recovery/pre-message-body-rewrite-20260829`, so citations to the former
lineage remain resolvable. Existing historical records are intentionally not
rewritten to conceal the superseded identities; this map provides their
translation to the selected lineage.

## Verified Result

- 83 missing bodies were repaired and eight existing bodies were preserved.
- All 91 replacement commits retain their original tree, subject, author,
  author date, committer, and committer date.
- The old and replacement tips have no content diff.
- The linear order and zero-merge topology are unchanged.
- The live result exactly matches the independently exercised temporary-clone
  prototype at `f526e69bdc6f40ac61f86eefd3d496fc4543984d`.
- No published commit or `origin/main` reference was rewritten.
- The complete standards checkpoint passed all 226 declarative suites and all
  53 retained Bash checkers after the rewrite.
- The 91-row lineage map, repository object graph, generated inventories, and
  whitespace checks passed their integrity checks.

The recovery ref is retained until the repository owner separately authorizes
its retirement. This report and map are the only new repository files added by
the history-maintenance operation.
