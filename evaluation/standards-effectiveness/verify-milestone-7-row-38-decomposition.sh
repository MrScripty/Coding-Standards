#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
V="$S/milestone-7-row-38-owner-validation.tsv"
D="$S/milestone-7-row-38-decomposition.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"

[[ "$(awk -F '\t' '$1 == 38 { print $3 FS $4 FS $5 FS $6 FS $7 FS $8 FS $10 }' "$O")" == $'STD-0088\tARCHITECTURE-PATTERNS.md\tworkflows/documentation.md\texists\tpre-slice-review\tfocused\tnone' ]]
[[ "$(awk -F '\t' '$1 == 38 { n++ } END { print n+0 }' "$O")" -eq 1 ]]
[[ "$(awk -F '\t' '$1 == 38 && NF != 10 { n++ } END { print n+0 }' "$O")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 { print $1 FS $2 FS $3 FS $4 }' "$V")" == $'STD-0088\tworkflows/documentation.md\tmerge-duplicate\tnone' ]]

for text in '## Owner Contract' '`STD-0088`' 'Activity Tracing is `STD-0089`' \
  '## Source-Gap Recovery' 'exactly sixteen row-47 gaps' \
  '## Bounded Write Set' '## Verification Gates' \
  '## Typed Outcomes And No Fallback' '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

[[ "$(awk -F '\t' '$1 == 38 { print $6 FS $7 FS $8 }' "$S/milestone-7-execution-train.tsv")" == $'workflows/documentation.md\texists\tpre-slice-review' ]]
[[ "$(awk -F '\t' '$1 == 38 { print $2 FS $4 FS $8 }' "$S/milestone-7-accelerated-packages.tsv")" == $'P31\tworkflows/documentation.md\tfocused' ]]
rg -F -q '`7.4b28b2` (`Accepted`)' "$P"
"$S/verify-documentation-directory-readme-closure.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-38 decomposition passed: STD-0088 closed through Documentation with 16 row-47 gaps bounded\n'
