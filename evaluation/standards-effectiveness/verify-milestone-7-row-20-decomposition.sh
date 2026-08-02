#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly VALIDATION="$S/milestone-7-row-20-owner-validation.tsv"
readonly REPORT="$S/milestone-7-row-20-decomposition.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

mapfile -t ids < <(
  awk -F '\t' '$1 == 20 {
    count = split($3, values, ",")
    for (i = 1; i <= count; i += 1) print values[i]
  }' "$OVERLAY" | sort
)
expected=(STD-{0706..0716})
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1 == 20 {print $2}' "$OVERLAY" | paste -sd ' ' -)" == '1 2 3 4 5 6' ]]
[[ "$(awk -F '\t' '$1 == 20 && NF != 9 {n++} END {print n+0}' "$OVERLAY")" -eq 0 ]]

mapfile -t validated < <(awk -F '\t' 'NR > 1 {print $1}' "$VALIDATION")
[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 4 {n++} END {print n+0}' "$VALIDATION")" -eq 0 ]]
[[ "$(awk -F '\t' '$3 == "index" {n++} END {print n+0}' "$VALIDATION")" -eq 1 ]]
[[ "$(awk -F '\t' '$3 == "refine" {n++} END {print n+0}' "$VALIDATION")" -eq 2 ]]
[[ "$(awk -F '\t' '$3 == "split" {n++} END {print n+0}' "$VALIDATION")" -eq 8 ]]

for text in '## Owner Contract' 'narrow language specialization' \
  'does not own domain invariants' 'Generic owners' \
  'selects a supported Rust expression' \
  '## Exact Dispositions' '## Ordered Children' '## Re-plan Triggers'; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '`7.4b10a` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b10b` (`Planned`)' "$PLAN"
next_slice_block="$(awk '
  /^\*\*Next slice:\*\*/ { capture = 1 }
  capture && /^$/ { exit }
  capture { print }
' "$PLAN")"
for id in STD-0706 STD-0713 STD-0714; do
  [[ "$next_slice_block" == *"$id"* ]]
done

"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-20 decomposition passed: 11 IDs across 6 children\n'
