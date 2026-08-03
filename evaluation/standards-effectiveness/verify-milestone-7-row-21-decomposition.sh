#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly VALIDATION="$S/milestone-7-row-21-owner-validation.tsv"
readonly REPORT="$S/milestone-7-row-21-decomposition.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

mapfile -t ids < <(awk -F '\t' '$1 == 21 {
  n = split($3, values, ","); for (i = 1; i <= n; i++) print values[i]
}' "$OVERLAY" | sort)
expected=(STD-{0731..0751})
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 == 21 {print $2}' "$OVERLAY" | paste -sd ' ' -)" == '1 2 3 4 5 6 7' ]]
[[ "$(awk -F '\t' '$1 == 21 && NF != 9 {n++} END {print n+0}' "$OVERLAY")" -eq 0 ]]

mapfile -t validated < <(awk -F '\t' 'NR > 1 {print $1}' "$VALIDATION")
[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 4 {n++} END {print n+0}' "$VALIDATION")" -eq 0 ]]
[[ "$(awk -F '\t' '$3 == "index" {n++} END {print n+0}' "$VALIDATION")" -eq 1 ]]
[[ "$(awk -F '\t' '$3 == "split" {n++} END {print n+0}' "$VALIDATION")" -eq 6 ]]
[[ "$(awk -F '\t' '$3 == "move" {n++} END {print n+0}' "$VALIDATION")" -eq 14 ]]

for text in '## Owner Contract' 'narrow Rust and Cargo mechanism' \
  'does not own dependency selection' '## Exact Dispositions' \
  'Fourteen command, manifest, and shell examples move' \
  '## Ordered Children' '## Child 21.4 Artifact-Surface Ownership Replan' \
  'Rust Dependency owns Cargo manifest dependency optionality' \
  'Rust API separately owns Rust' 'retain aliases, compatibility wording' \
  '## Re-plan Triggers'; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '`7.4b11a` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b11b` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b11c` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b11d` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b11e` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b11f` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b11g` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b11h` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12a` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12b` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12c` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12d` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b12e` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13a` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13b` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13c` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13d` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13e` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13f` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13g` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13h` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13i` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13j` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13k` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13l` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13m` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b13n` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b14a` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b14b` (`Planned`)' "$PLAN"
next_slice="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice" == *'row 24'* ]]
[[ "$next_slice" == *'STD-0849'* ]]
next_slice_block="$(awk '
  /^\*\*Next slice:\*\*/ { capture = 1 }
  capture && /^$/ { exit }
  capture { print }
' "$PLAN")"
[[ "$next_slice_block" == *'row 24'* ]]
[[ "$next_slice_block" == *'STD-0849'* && "$next_slice_block" == *'STD-0851'* ]]

"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-21 decomposition passed: 21 IDs across 7 children\n'
