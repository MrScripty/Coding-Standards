#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
V="$S/milestone-7-row-35-owner-validation.tsv"
A="$S/milestone-7-row-35-readme-dependencies.tsv"
D="$S/milestone-7-row-35-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"

expected=(STD-{0001..0006})
mapfile -t ids < <(
  awk -F '\t' '$1 == 35 { n=split($3,a,","); for(i=1;i<=n;i++) print a[i] }' "$O" | sort
)
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 == 35 { n++ } END { print n+0 }' "$O")" -eq 2 ]]
[[ "$(awk -F '\t' '$1 == 35 && ($6 != "exists" || $7 != "pre-slice-review" || $8 != "focused" || $10 != "none" || NF != 10) { n++ } END { print n+0 }' "$O")" -eq 0 ]]

mapfile -t validated < <(awk -F '\t' 'NR > 1 { print $1 }' "$V")
[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 4 { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 >= "STD-0001" && $1 <= "STD-0005" && $2 != "STANDARDS-ROUTER.md" { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == "STD-0006" { print $2 FS $3 }' "$V")" == $'LICENSE\tindex' ]]

[[ "$(awk -F '\t' 'NR > 1 { n++ } END { print n+0 }' "$A")" -eq 31 ]]
[[ "$(awk -F '\t' 'NR > 1 && ($2 != "root-readme-route-or-catalog-assertion" || $3 != "canonical-router-or-owner-evidence" || NF != 3) { n++ } END { print n+0 }' "$A")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 }' "$A" | sort | uniq -d | wc -l)" -eq 0 ]]
while IFS=$'\t' read -r file current replacement; do
  [[ "$file" == file ]] && continue
  [[ -f "$R/$file" ]]
done < "$A"

for text in '## Owner Contract' 'sole authority' '## Exact Ownership' \
  '`35.1`' '`35.2`' '## Bounded Write Sets' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done
[[ "$(awk -F '\t' '$1 == 35 { print $6 FS $7 FS $8 }' "$S/milestone-7-execution-train.tsv")" == $'STANDARDS-ROUTER.md\texists\tfinal-closure' ]]
[[ "$(awk -F '\t' '$1 == 35 { print $8 }' "$S/milestone-7-accelerated-packages.tsv")" == full-suite ]]
rg -F -q '`7.4b25a` (`Accepted`)' "$P"
rg -F -q '`7.4b25b` (`Planned`)' "$P"
rg -F -q '`7.4b25c` (`Planned`)' "$P"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-35 decomposition passed: 6 IDs across 2 serial closure children and 31 frozen checker dependencies\n'
