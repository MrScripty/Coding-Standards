#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
V="$S/milestone-7-row-35-owner-validation.tsv"
A="$S/milestone-7-row-35-readme-dependencies.tsv"
C="$S/milestone-7-row-35-transitive-contract-callers.tsv"
M="$S/milestone-7-row-35-readme-consumers.tsv"
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

[[ "$(awk -F '\t' 'NR > 1 { n++ } END { print n+0 }' "$A")" -eq 21 ]]
[[ "$(awk -F '\t' 'NR > 1 && ($2 != "root-readme-route-or-catalog-assertion" && $2 != "transitive-root-readme-route-assertion" && $2 != "computed-root-readme-route-assertion") { n++ } END { print n+0 }' "$A")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && ($3 != "canonical-router-or-owner-evidence" || NF != 3) { n++ } END { print n+0 }' "$A")" -eq 0 ]]
[[ "$(awk -F '\t' '$2 == "root-readme-route-or-catalog-assertion" { n++ } END { print n+0 }' "$A")" -eq 19 ]]
[[ "$(awk -F '\t' '$2 == "transitive-root-readme-route-assertion" { n++ } END { print n+0 }' "$A")" -eq 1 ]]
[[ "$(awk -F '\t' '$2 == "computed-root-readme-route-assertion" { n++ } END { print n+0 }' "$A")" -eq 1 ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 }' "$A" | sort | uniq -d | wc -l)" -eq 0 ]]
while IFS=$'\t' read -r file current replacement; do
  [[ "$file" == file ]] && continue
  [[ -f "$R/$file" ]]
done < "$A"

[[ "$(awk -F '\t' 'NR > 1 { n++ } END { print n+0 }' "$M")" -eq 32 ]]
"$S/verify-root-readme-consumer-audit.sh"

mapfile -t callers < <(awk -F '\t' 'NR > 1 { print $1 }' "$C" | sort)
[[ "${#callers[@]}" -gt 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && ($2 != "evaluation/standards-effectiveness/verify-contract-ownership.sh" || NF != 2) { n++ } END { print n+0 }' "$C")" -eq 0 ]]
mapfile -t observed_callers < <(
  rg -l '^"\$(SCRIPT_DIR|S)/verify-contract-ownership\.sh"$' "$S"/verify-*.sh |
    sed "s#^$R/##" |
    sort
)
[[ "${observed_callers[*]}" == "${callers[*]}" ]]
for caller in "${callers[@]}"; do
  [[ -f "$R/$caller" ]]
  "$R/$caller"
done

for text in '## Owner Contract' 'sole authority' '## Exact Ownership' \
  '`35.1`' '`35.2`' '## Bounded Write Sets' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done
[[ "$(awk -F '\t' '$1 == 35 { print $6 FS $7 FS $8 }' "$S/milestone-7-execution-train.tsv")" == $'STANDARDS-ROUTER.md\texists\tfinal-closure' ]]
[[ "$(awk -F '\t' '$1 == 35 { print $8 }' "$S/milestone-7-accelerated-packages.tsv")" == full-suite ]]
rg -F -q '`7.4b25a` (`Accepted`)' "$P"
rg -F -q '`7.4b25b` (`Accepted`)' "$P"
rg -F -q '`7.4b25c` (`Accepted`)' "$P"
"$S/verify-root-index-closure.sh"
"$S/verify-root-router-evidence.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-35 decomposition passed: 6 IDs across 2 serial closure children, 21 frozen checker dependencies, 32 classified README consumers, and %d shared-checker callers\n' \
  "${#callers[@]}"
