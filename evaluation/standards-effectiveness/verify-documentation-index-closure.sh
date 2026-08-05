#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
DISPOSITIONS="$S/consolidation-dispositions.tsv"
GAPS="$S/fixtures/migration/undisposed-source-gaps.tsv"
LEGACY="$R/DOCUMENTATION-STANDARDS.md"

[[ "$(awk -F '\t' '$1 == "STD-0349" { print $2 FS $3 FS $4 }' "$DISPOSITIONS")" == $'DOCUMENTATION-STANDARDS.md\tworkflows/documentation.md\tindex' ]]
[[ "$(awk -F '\t' '$1 == "STD-0349" { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]

expected=(STD-0899 STD-0900 STD-0901 STD-0902 STD-0903 STD-0904 STD-0905 \
  STD-0907 STD-0908 STD-0909 STD-0910 STD-0911 STD-0912 STD-0913 \
  STD-0914 STD-0915 STD-0916)
mapfile -t actual < <(awk -F '\t' 'NR > 1 { print $1 }' "$GAPS")
[[ "${actual[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 3 { n++ } END { print n+0 }' "$GAPS")" -eq 0 ]]

for text in '# Documentation Standards' 'This file is a migration index' \
  '[Documentation Workflow](workflows/documentation.md)' \
  '[Documentation Recipe](reference/recipes/documentation.md)' \
  '[Release Workflow](workflows/release.md)' \
  'This index has no independent normative authority'; do
  rg -F -q "$text" "$LEGACY"
done

"$S/verify-undisposed-source-gaps.sh"
"$S/verify-documentation-decisions.sh"
"$S/verify-documentation-policy-consolidation.sh"
"$S/verify-milestone-7-row-41-decomposition.sh"
printf 'Documentation index closure passed: 1 exact disposition, 17 audit candidates remain, P33 closed\n'
