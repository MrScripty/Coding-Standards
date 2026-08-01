#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/milestone-7-row-19-owner-validation.tsv"
P="$S/milestone-7-row-19-owner-validation.md"

mapfile -t ids < <(awk -F '\t' 'NR>1{print $1}' "$F")
expected=(STD-{0654..0703})
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR>1{print $1}' "$F" | sort | uniq -d | wc -l)" -eq 0 ]]
[[ "$(awk -F '\t' 'NR>1&&NF!=4{count++}END{print count+0}' "$F")" -eq 0 ]]

for owner in workflows/tooling.md workflows/verification.md \
  workflows/implementation.md workflows/commit.md workflows/documentation.md \
  topics/dependencies.md profiles/languages/typescript.md reference; do
  rg -F -q "$owner" "$F"
done
for text in '## Boundary Result' 'validates creating `workflows/tooling.md`' \
  '## Required Option 2 Package' 'before normative implementation' \
  '## Re-plan Triggers'; do
  rg -F -q "$text" "$P"
done
rg -F -q 'Row 19 owner-validation gate (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9a` (`Accepted`): perform the row 19 complete decomposition' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9b` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9c` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
[[ -e "$R/workflows/tooling.md" ]]
printf 'Milestone 7 row-19 owner validation passed: 50 exact proposals\n'
