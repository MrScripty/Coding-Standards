#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
V="$S/milestone-7-row-36-owner-validation.tsv"
D="$S/milestone-7-row-36-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"

expected=(STD-{0027..0045})
mapfile -t ids < <(
  awk -F '\t' '$1 == 36 { n=split($3,a,","); for(i=1;i<=n;i++) print a[i] }' "$O" | sort
)
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 == 36 { n++ } END { print n+0 }' "$O")" -eq 4 ]]
[[ "$(awk -F '\t' '$1 == 36 && NF != 10 { n++ } END { print n+0 }' "$O")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == 36 && $2 == 1 { print $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'reference/patterns/architecture.md\texists\towner-review\tfocused\tmissing-to-exists' ]]
[[ "$(awk -F '\t' '$1 == 36 && $2 > 1 && ($5 != "topics/architecture.md" || $6 != "exists" || $7 != "pre-slice-review" || $8 != "focused" || $10 != "none") { n++ } END { print n+0 }' "$O")" -eq 0 ]]

mapfile -t validated < <(awk -F '\t' 'NR > 1 { print $1 }' "$V")
[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && $2 != "topics/architecture.md" && $2 != "reference/patterns/architecture.md" { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && $3 != "index" && $3 != "split" && $3 != "move" && $3 != "merge-duplicate" { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == "STD-0033" { print $2 FS $3 FS $4 }' "$V")" == $'topics/architecture.md\tmerge-duplicate\tnone' ]]
for id in STD-0031 STD-0037 STD-0041 STD-0042 STD-0043 STD-0044; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { print $2 FS $3 }' "$V")" == $'topics/architecture.md\tsplit' ]]
done

for text in '## Owner Contract' 'sole normative owner' \
  'rows 37, 39, and 40' '## Exact Ownership' '`36.1`' '`36.2`' \
  '`36.3`' '`36.4`' 'P30 remains open' '## Bounded Write Sets' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done
[[ "$(awk -F '\t' '$1 == 36 { print $6 FS $7 FS $8 }' "$S/milestone-7-execution-train.tsv")" == $'reference/patterns/architecture.md\tmissing\towner-review' ]]
[[ "$(awk -F '\t' '$1 == 36 { print $2 FS $4 FS $8 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P30\treference/patterns/architecture.md\tfull-suite' ]]
rg -F -q '`7.4b26a` (`Accepted`)' "$P"
rg -F -q '`7.4b26b` (`Accepted`)' "$P"
rg -F -q '`7.4b26c` (`Accepted`)' "$P"
rg -F -q '`7.4b26d` (`Accepted`)' "$P"
for milestone in 7.4b26e; do
  printf -v pattern '`%s` (`Planned`)' "$milestone"
  rg -F -q "$pattern" "$P"
done
"$S/verify-architecture-pattern-reference-owner.sh"
"$S/verify-architecture-layered-pattern.sh"
"$S/verify-architecture-monorepo-pattern.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-36 decomposition passed: 19 IDs across 4 serial children with P30 deferred through row 37\n'
