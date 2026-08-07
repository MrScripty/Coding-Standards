#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
DISPOSITIONS="$S/consolidation-dispositions.tsv"
GAPS="$S/fixtures/migration/undisposed-source-gaps.tsv"
LEGACY="$R/DOCUMENTATION-STANDARDS.md"

[[ "$(awk -F '\t' '$1 == "STD-0349" { print $2 FS $3 FS $4 }' "$DISPOSITIONS")" == $'DOCUMENTATION-STANDARDS.md\tworkflows/documentation.md\tindex' ]]
[[ "$(awk -F '\t' '$1 == "STD-0349" { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]

expected=()
mapfile -t actual < <(awk -F '\t' 'NR > 1 { print $1 }' "$GAPS")
[[ "${actual[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 3 { n++ } END { print n+0 }' "$GAPS")" -eq 0 ]]

for text in '# Documentation Standards' 'non-normative navigation' \
  "Router's typed" \
  '[Documentation Workflow](workflows/documentation.md)' \
  '[Documentation Recipe](reference/recipes/documentation.md)' \
  '[Release Workflow](workflows/release.md)' \
  'This index has no independent normative authority'; do
  rg -F -q "$text" "$LEGACY"
done

obsolete_source_assertion='This file is a migration ''index'
if rg -F -q "$obsolete_source_assertion" "$0"; then
  printf 'Documentation checker owns obsolete source prose: %s\n' \
    "$obsolete_source_assertion" >&2
  exit 1
fi

"$S/verify-undisposed-source-gaps.sh"
"$S/verify-documentation-decisions.sh"
"$S/verify-documentation-policy-consolidation.sh"
"$S/verify-milestone-7-row-41-decomposition.sh"
printf 'Documentation index closure passed: 1 exact disposition, 0 audit candidates remain, P33 closed\n'
