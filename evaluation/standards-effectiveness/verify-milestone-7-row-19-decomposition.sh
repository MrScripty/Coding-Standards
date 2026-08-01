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
[[ "$(awk -F '\t' '$1==19{print $2}' "$O" | sort -n | paste -sd ' ' -)" == "$(seq 1 19 | paste -sd ' ' -)" ]]
[[ "$(awk -F '\t' '$1==19&&NF!=9{n++}END{print n+0}' "$O")" -eq 0 ]]

for owner in workflows/tooling.md workflows/verification.md workflows/commit.md \
  workflows/documentation.md workflows/implementation.md topics/dependencies.md \
  profiles/languages/typescript.md reference/recipes/tooling.md; do
  rg -F -q "$owner" "$O"
done
for text in '## Proposed Owner Contract' 'does not own what evidence proves' \
  'must not fall back' '## Ordered Children' '19 overlay rows' \
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
rg -F -q '`7.4b9h` (`Planned`)' "$P"
[[ -e "$R/workflows/tooling.md" ]]
[[ -e "$R/reference/recipes/tooling.md" ]]
printf 'Milestone 7 row-19 decomposition passed: 50 IDs across 19 children\n'
