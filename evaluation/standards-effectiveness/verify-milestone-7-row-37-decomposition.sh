#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
V="$S/milestone-7-row-37-owner-validation.tsv"
D="$S/milestone-7-row-37-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"

expected=(STD-{0069..0087})
mapfile -t ids < <(
  awk -F '\t' '$1 == 37 { n=split($3,a,","); for(i=1;i<=n;i++) print a[i] }' "$O" | sort
)
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 == 37 { n++ } END { print n+0 }' "$O")" -eq 4 ]]
[[ "$(awk -F '\t' '$1 == 37 && NF != 10 { n++ } END { print n+0 }' "$O")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == 37 && $2 == 1 { print $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'topics/architecture.md\texists\towner-review\tfocused\tnone' ]]
[[ "$(awk -F '\t' '$1 == 37 && $2 == 2 { print $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'topics/resilience.md\texists\tpre-slice-review\tfocused\tnone' ]]
[[ "$(awk -F '\t' '$1 == 37 && $2 == 3 { print $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'profiles/applications/frontend.md\texists\tpre-slice-review\tfocused\tnone' ]]
[[ "$(awk -F '\t' '$1 == 37 && $2 == 4 { print $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'topics/architecture.md\texists\tfinal-closure\tfocused\tnone' ]]

mapfile -t validated < <(awk -F '\t' 'NR > 1 { print $1 }' "$V")
[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && $2 != "topics/architecture.md" && $2 != "reference/patterns/architecture.md" && $2 != "topics/resilience.md" && $2 != "profiles/applications/frontend.md" && $2 != "reference/recipes/frontend.md" && $2 != "workflows/verification.md" { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && $3 != "index" && $3 != "split" && $3 != "move" && $3 != "merge-duplicate" { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == "STD-0080" { print $2 FS $3 FS $4 }' "$V")" == $'workflows/verification.md\tmerge-duplicate\tnone' ]]
[[ "$(awk -F '\t' '$1 == "STD-0085" { print $2 FS $3 FS $4 }' "$V")" == $'reference/recipes/frontend.md\tmerge-duplicate\texisting-frontend-mechanisms' ]]
[[ "$(awk -F '\t' '$1 == "STD-0087" { print $2 FS $3 FS $4 }' "$V")" == $'topics/architecture.md\tmerge-duplicate\tnone' ]]

for text in '## Owner Contract' 'independent owner review' \
  '## Exact Ownership' '`37.1`' '`37.2`' '`37.3`' '`37.4`' \
  '## Reference Selection' 'view-model class and directory tree are removed' \
  '## Bounded Write Sets' '## Verification Gates' 'P30 closes only' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done
[[ "$(awk -F '\t' '$1 == 37 { print $6 FS $7 FS $8 }' "$S/milestone-7-execution-train.tsv")" == $'reference/patterns/architecture.md\tmissing\towner-review' ]]
[[ "$(awk -F '\t' '$1 == 37 { print $2 FS $4 FS $8 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P30\treference/patterns/architecture.md\tfull-suite' ]]
rg -F -q '`7.4b27a` (`Accepted`)' "$P"
rg -F -q '`7.4b27b` (`Accepted`)' "$P"
rg -F -q '`7.4b27c` (`Accepted`)' "$P"
for milestone in 7.4b27d 7.4b27e; do
  printf -v pattern '`%s` (`Planned`)' "$milestone"
  rg -F -q "$pattern" "$P"
done
"$S/verify-architecture-owner-contract.sh"
"$S/verify-architecture-pattern-reference-owner.sh"
"$S/verify-resilience-owner-contract.sh"
"$S/verify-frontend-owner-contract.sh"
"$S/verify-architecture-composition-root-pattern.sh"
"$S/verify-architecture-durable-workflow-pattern.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-37 decomposition passed: 19 IDs across 4 serial children with P30 closing in child 37.4\n'
