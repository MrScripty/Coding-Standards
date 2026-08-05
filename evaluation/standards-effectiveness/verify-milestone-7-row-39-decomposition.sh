#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
V="$S/milestone-7-row-39-owner-validation.tsv"
D="$S/milestone-7-row-39-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"
F="$S/findings.md"

expected=(STD-{0093..0105})
mapfile -t ids < <(
  awk -F '\t' '$1 == 39 { n=split($3,a,","); for(i=1;i<=n;i++) print a[i] }' "$O"
)
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 == 39 { n++ } END { print n+0 }' "$O")" -eq 3 ]]
[[ "$(awk -F '\t' '$1 == 39 && NF != 10 { n++ } END { print n+0 }' "$O")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == 39 && $2 == 1 { print $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'topics/concurrency.md\texists\towner-review\tfocused\tnone' ]]
[[ "$(awk -F '\t' '$1 == 39 && $2 == 2 { print $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'topics/architecture.md\texists\tpre-slice-review\tfocused\tnone' ]]
[[ "$(awk -F '\t' '$1 == 39 && $2 == 3 { print $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'reference/patterns/architecture.md\texists\tfinal-closure\tfocused\tnone' ]]

mapfile -t validated < <(awk -F '\t' 'NR > 1 { print $1 }' "$V")
[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && $2 != "topics/architecture.md" && $2 != "topics/concurrency.md" && $2 != "topics/contracts.md" && $2 != "topics/cross-platform.md" && $2 != "topics/resilience.md" && $2 != "reference/patterns/architecture.md" { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && $3 != "index" && $3 != "split" && $3 != "refine" && $3 != "move" { n++ } END { print n+0 }' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' '$1 == "STD-0096" { print $2 FS $3 FS $4 }' "$V")" == $'topics/contracts.md\tsplit\tnone' ]]
[[ "$(awk -F '\t' '$1 == "STD-0097" { print $2 FS $3 FS $4 }' "$V")" == $'topics/cross-platform.md\tsplit\tnone' ]]
[[ "$(awk -F '\t' '$1 == "STD-0098" { print $2 FS $3 FS $4 }' "$V")" == $'topics/resilience.md\tsplit\tnone' ]]
[[ "$(awk -F '\t' '$1 == "STD-0103" { print $2 FS $3 FS $4 }' "$V")" == $'topics/architecture.md\tsplit\tconditional-discover-or-create' ]]

for text in '## Re-plan Trigger' 'single-owner review could not confirm' \
  '## Owner Contract' '## Exact Ownership' '`39.1`' '`39.2`' '`39.3`' \
  '## Reference Selection' 'Fixed PID-file' \
  '## Bounded Write Sets' '## Verification Gates' 'P32 remains open' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

[[ "$(awk -F '\t' '$1 == 39 { print $6 FS $7 FS $8 }' "$S/milestone-7-execution-train.tsv")" == $'reference/patterns/architecture.md\tmissing\towner-review' ]]
[[ "$(awk -F '\t' '$1 == 39 { print $2 FS $4 FS $8 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P32\treference/patterns/architecture.md\tfocused' ]]
rg -F -q '| F075 | Resolved in Milestone 7.4b29a |' "$F"
rg -F -q '`7.4b29a` (`Accepted`)' "$P"
rg -F -q '`7.4b29b` (`Accepted`)' "$P"
rg -F -q '`7.4b29c` (`Accepted`)' "$P"
rg -F -q '`7.4b29d` (`Accepted`)' "$P"
"$S/verify-architecture-owner-contract.sh"
"$S/verify-architecture-pattern-reference-owner.sh"
"$S/verify-concurrency-policy.sh"
"$S/verify-contract-ownership.sh"
"$S/verify-resilience-owner-contract.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-39 decomposition passed: 13 IDs across 3 serial children with P32 retained through row 40\n'
