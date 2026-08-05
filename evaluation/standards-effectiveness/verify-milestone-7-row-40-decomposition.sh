#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
V="$S/milestone-7-row-40-owner-validation.tsv"
D="$S/milestone-7-row-40-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"

[[ "$(awk -F '\t' '$1 == 40 { print $2 FS $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'1\tSTD-0134\tARCHITECTURE-PATTERNS.md\treference/patterns/architecture.md\texists\tfinal-closure\tfocused\tnone' ]]
[[ "$(awk -F '\t' '$1 == 40 { n++ } END { print n+0 }' "$O")" -eq 1 ]]
[[ "$(awk -F '\t' '$1 == 40 && NF != 10 { n++ } END { print n+0 }' "$O")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 FS $2 FS $3 FS $4 }' "$V")" == $'STD-0134\treference/patterns/architecture.md\tmerge-duplicate\tnone' ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 5 { n++ } END { print n+0 }' "$V")" -eq 0 ]]

for text in '## Owner Review' '`STD-0134`' \
  'pattern presence' '## Exact Outcome' \
  '`merge-duplicate`' '## Ordered Child' '`40.1`' \
  '## Bounded Write Set' '## Verification Gates' 'focused P32 gate' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

[[ -e "$R/reference/patterns/architecture.md" ]]
[[ "$(awk -F '\t' '$1 == 40 { print $6 FS $7 FS $8 }' "$S/milestone-7-execution-train.tsv")" == $'reference/patterns/architecture.md\tmissing\towner-review' ]]
[[ "$(awk -F '\t' '$1 == 40 { print $2 FS $4 FS $8 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P32\treference/patterns/architecture.md\tfocused' ]]
rg -F -q '`7.4b30a` (`Accepted`)' "$P"
rg -F -q '`7.4b30br` (`Accepted`)' "$P"
rg -F -q '`7.4b30b` (`Accepted`)' "$P"
"$S/verify-architecture-pattern-reference-owner.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-40 decomposition passed: STD-0134 has one reference merge-duplicate child closing P32\n'
