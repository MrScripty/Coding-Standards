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
[[ "$(awk -F '\t' '$1>="STD-0677"&&$1<="STD-0680"&&$2=="profiles/languages/typescript.md"&&$3=="split"{n++}END{print n+0}' "$F")" -eq 4 ]]
[[ "$(awk -F '\t' '($1=="STD-0682"||$1=="STD-0686")&&$2=="workflows/tooling.md"&&$3=="split"{n++}END{print n+0}' "$F")" -eq 2 ]]
[[ "$(awk -F '\t' '($1=="STD-0689"||$1=="STD-0690")&&$2=="workflows/tooling.md"&&$3=="split"{n++}END{print n+0}' "$F")" -eq 2 ]]
[[ "$(awk -F '\t' '$1=="STD-0692"&&$2=="workflows/tooling.md"&&$3=="split"{n++}END{print n+0}' "$F")" -eq 1 ]]
[[ "$(awk -F '\t' '$1=="STD-0696"&&$2=="workflows/documentation.md"&&$3=="index"{n++}END{print n+0}' "$F")" -eq 1 ]]
[[ "$(awk -F '\t' '$1=="STD-0697"&&$2=="workflows/documentation.md"&&$3=="split"{n++}END{print n+0}' "$F")" -eq 1 ]]
[[ "$(awk -F '\t' '$1=="STD-0698"&&$2=="workflows/implementation.md"&&$3=="split"{n++}END{print n+0}' "$F")" -eq 1 ]]
[[ "$(awk -F '\t' '$1=="STD-0699"&&$2=="topics/dependencies.md"&&$3=="route"{n++}END{print n+0}' "$F")" -eq 1 ]]
[[ "$(awk -F '\t' '$1=="STD-0700"&&$2=="topics/dependencies.md"&&$3=="index"{n++}END{print n+0}' "$F")" -eq 1 ]]

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
rg -F -q '`7.4b9c` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9d` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9e` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9f` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9g` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9h` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9i` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9j` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9k` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9l` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9s` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q 'Row 19 TypeScript split replan (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q 'Row 19 formatting split replan (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q 'Row 19 CI orchestration split replan (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q 'Row 19 debt and automation-cost split replan (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q 'Row 19 traceability-lineage replan (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q 'Row 19 change-evidence split replan (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
[[ -e "$R/workflows/tooling.md" ]]
[[ -e "$R/reference/recipes/tooling.md" ]]
printf 'Milestone 7 row-19 owner validation passed: 50 exact proposals\n'
