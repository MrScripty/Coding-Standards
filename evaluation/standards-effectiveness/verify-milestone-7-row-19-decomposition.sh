#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"
RPT="$S/milestone-7-row-19-decomposition.md"

mapfile -t ids < <(awk -F '\t' '$1==19{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O" | sort)
expected=(STD-{0654..0703})
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==19{print $2}' "$O" | sort -n | paste -sd ' ' -)" == "$(seq 1 18 | paste -sd ' ' -)" ]]
[[ "$(awk -F '\t' '$1==19&&NF!=9{n++}END{print n+0}' "$O")" -eq 0 ]]

for owner in workflows/tooling.md workflows/verification.md workflows/commit.md \
  workflows/documentation.md workflows/implementation.md topics/dependencies.md \
  profiles/languages/typescript.md reference/recipes/tooling.md; do
  rg -F -q "$owner" "$O"
done
for text in '## Proposed Owner Contract' 'does not own what evidence proves' \
  'must not fall back' '## Ordered Children' '18 overlay rows' \
  'canonical-owner-homogeneous' 'Child `19.8` is a reviewed split package' \
  'exactly one `split` disposition' 'Child `19.9` applies the same boundary' \
  'Child `19.12` applies the split boundary' \
  'Child `19.13` applies the same boundary' \
  'Child `19.15` reconciles replacement lineage' \
  'Child `19.16` keeps Implementation' \
  '## Implementation Sequence' '## Re-plan Triggers'; do
  rg -F -q "$text" "$RPT"
done
rg -F -q '`7.4b9a` (`Accepted`)' "$P"
rg -F -q '`7.4b9b` (`Accepted`)' "$P"
rg -F -q '`7.4b9c` (`Accepted`)' "$P"
rg -F -q '`7.4b9d` (`Accepted`)' "$P"
rg -F -q '`7.4b9e` (`Accepted`)' "$P"
rg -F -q '`7.4b9f` (`Accepted`)' "$P"
rg -F -q '`7.4b9g` (`Accepted`)' "$P"
rg -F -q '`7.4b9h` (`Accepted`)' "$P"
rg -F -q '`7.4b9i` (`Accepted`)' "$P"
rg -F -q '`7.4b9j` (`Accepted`)' "$P"
rg -F -q '`7.4b9k` (`Accepted`)' "$P"
rg -F -q '`7.4b9l` (`Accepted`)' "$P"
rg -F -q '`7.4b9s` (`Planned`)' "$P"
rg -F -q 'Row 19 TypeScript split replan (`Accepted`)' "$P"
rg -F -q 'Row 19 formatting split replan (`Accepted`)' "$P"
rg -F -q 'Row 19 CI orchestration split replan (`Accepted`)' "$P"
rg -F -q 'Row 19 debt and automation-cost split replan (`Accepted`)' "$P"
rg -F -q 'Row 19 traceability-lineage replan (`Accepted`)' "$P"
rg -F -q 'Row 19 change-evidence split replan (`Accepted`)' "$P"
awk -F '\t' '$1==19&&$2==8&&$5=="profiles/languages/typescript.md"&&$7=="pre-slice-review"&&$9~/non-normative Tooling reference/{f=1}END{exit !f}' "$O"
awk -F '\t' '$1==19&&$2==9&&$5=="workflows/tooling.md"&&$9~/VS Code format-on-save Prettier ESLint pairing/{f=1}END{exit !f}' "$O"
awk -F '\t' '$1==19&&$2==12&&$5=="workflows/tooling.md"&&$9~/GitHub fail-fast summary continue-on-error/{f=1}END{exit !f}' "$O"
awk -F '\t' '$1==19&&$2==13&&$5=="workflows/tooling.md"&&$9~/GitHub permissions concurrency setup cache/{f=1}END{exit !f}' "$O"
awk -F '\t' '$1==19&&$2==15&&$3=="STD-0696,STD-0697"&&$5=="workflows/documentation.md"&&$9~/pre-migration Decision Traceability lineage/{f=1}END{exit !f}' "$O"
awk -F '\t' '$1==19&&$2==16&&$3=="STD-0698"&&$5=="workflows/implementation.md"&&$9~/GitHub template placement installation/{f=1}END{exit !f}' "$O"
[[ -e "$R/workflows/tooling.md" ]]
[[ -e "$R/reference/recipes/tooling.md" ]]
printf 'Milestone 7 row-19 decomposition passed: 50 IDs across 18 children\n'
