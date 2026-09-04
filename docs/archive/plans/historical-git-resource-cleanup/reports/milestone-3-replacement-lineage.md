# Milestone 3 Replacement-Lineage Review

## Boundary

This review reconstructs durable source-to-accepted lineage for every
non-ancestral local branch. It does not delete refs, rewrite commits, mutate
remotes, or infer accepted edges from patch similarity alone.

The reviewed evidence combines:

- the current source branch name, tip, and commit identity;
- a stable patch identity with exactly one matching commit on accepted `main`;
- exact semantic commit-subject agreement, or an accepted-subject prefix where
  one historical source subject included its body as literal escaped text; and
- an explicit integration-owner disposition recorded by this review.

`reconstructed-replacement-lineage` describes this evidence reconstruction. It
does not claim that Git can distinguish whether the historical replacement was
created by cherry-pick or by equivalent reconstruction.

## Results

| Classification | Branches | Source commits | Disposition |
| --- | ---: | ---: | --- |
| Unique accepted replacement and semantic subject agreement | 115 | 118 | Candidate for mapped redundant-ref retirement after deletion semantics are authorized |
| Unmapped unique proposal | 12 | 12 | Retain for separate ownership and terminal review |

For the 118 mapped source commits:

- every stable patch identity has exactly one accepted `main` candidate;
- 117 source and accepted subjects are exact matches;
- one source subject contains the accepted subject followed by literal escaped
  body text, so the accepted subject is an exact semantic prefix;
- no source commit is a merge commit; and
- no mapping is missing or ambiguous.

The authoritative review artifacts are:

- [source-to-accepted mappings](../inventories/branch-replacement-mappings.tsv);
- [branch lineage dispositions](../inventories/branch-lineage-dispositions.tsv).

## Re-Plan Trigger

The 115 mapped branches are intentionally non-ancestral because accepted
replacement commits own their changes. Consequently, ordinary
`git branch -d` refuses deletion and `git branch -D` is required to remove the
redundant refs.

The current cleanup plan lists force deletion as a re-plan trigger. This review
does not silently weaken that guard. A re-plan must distinguish narrowly
authorized deletion of a fully mapped redundant ref from prohibited force
deletion that could discard unique, shared, checked-out, unknown, or unmapped
history. Until then, all 115 mapped refs remain present.

## Verification

- branches reviewed: 127;
- source commits reviewed: 130;
- uniquely mapped source commits: 118;
- unmapped unique source commits: 12;
- ambiguous mappings: 0;
- mapped subject mismatches: 0;
- ref mutations during review: 0;
- repository worktree before evidence updates: clean.
