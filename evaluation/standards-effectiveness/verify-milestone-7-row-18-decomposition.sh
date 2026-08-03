#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly REPORT="$S/milestone-7-row-18-decomposition.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

expected_rows=(
  $'18\t1\tSTD-0611,STD-0639\tTESTING-STANDARDS.md\ttopics/concurrency.md\texists\tpre-slice-review\tfocused'
  $'18\t2\tSTD-0616\tTESTING-STANDARDS.md\tprofiles/boundaries/language-bindings.md\texists\tpre-slice-review\tfocused'
  $'18\t3\tSTD-0617\tTESTING-STANDARDS.md\ttopics/resilience.md\texists\tpre-slice-review\tfocused'
  $'18\t4\tSTD-0635\tTESTING-STANDARDS.md\ttopics/contracts.md\texists\tpre-slice-review\tfocused'
  $'18\t5\tSTD-0641\tTESTING-STANDARDS.md\tprofiles/applications/frontend.md\texists\tpre-slice-review\tfocused'
  $'18\t6\tSTD-0642,STD-0643,STD-0644\tTESTING-STANDARDS.md\ttopics/performance.md\texists\tpre-slice-review\tfocused'
  $'18\t7\tSTD-0608,STD-0609,STD-0610,STD-0612,STD-0613,STD-0614,STD-0615\tTESTING-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
  $'18\t8\tSTD-0618,STD-0619,STD-0620,STD-0621,STD-0622,STD-0623,STD-0624\tTESTING-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
  $'18\t9\tSTD-0603,STD-0604,STD-0605,STD-0606,STD-0607\tTESTING-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
  $'18\t10\tSTD-0625,STD-0626,STD-0627,STD-0628,STD-0629,STD-0630,STD-0631\tTESTING-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
  $'18\t11\tSTD-0632,STD-0633,STD-0634\tTESTING-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
  $'18\t12\tSTD-0636,STD-0637,STD-0638,STD-0640\tTESTING-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
  $'18\t13\tSTD-0645,STD-0646,STD-0647,STD-0648,STD-0649,STD-0650,STD-0651,STD-0652\tTESTING-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
  $'18\t14\tSTD-0602,STD-0653\tTESTING-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
)
mapfile -t actual_rows < <(
  awk -F '\t' '$1 == 18 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8
  }' "$OVERLAY"
)
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

expected_ids=(STD-{0602..0653})
mapfile -t actual_ids < <(
  awk -F '\t' '$1 == 18 {
    count = split($3, ids, ",")
    for (i = 1; i <= count; i += 1) print ids[i]
  }' "$OVERLAY" | sort
)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

for owner in topics/concurrency.md profiles/boundaries/language-bindings.md \
  topics/resilience.md topics/contracts.md profiles/applications/frontend.md \
  topics/performance.md workflows/verification.md; do
  [[ -e "$R/$owner" ]]
done

for text in 'Those concerns do not share one canonical' \
  '## Ordered Implementation' 'suite labels as evidence' 'typed diagnostics' \
  'no normative or legacy standard' '## Refined Verification Boundary' \
  'eight Verification children' 'final legacy-closure child' \
  'Row 21 child `21.1` creates the narrow Rust dependency'; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '`7.4b8bu` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8bv` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8bw` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8bx` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8by` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8cb` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8cc` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8cd` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ce` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8cf` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8cg` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ch` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ci` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8cj` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b9s` (`Accepted`)' "$PLAN"
next_slice_block="$(awk '
  /^\*\*Next slice:\*\*/ { capture = 1 }
  capture && /^$/ { exit }
  capture { print }
' "$PLAN")"
[[ "$next_slice_block" == *'row 23'* ]]
for id in STD-0834; do
  [[ "$next_slice_block" == *"$id"* ]]
done
[[ "$next_slice_block" == *'row 23'* ]]

"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-18 decomposition passed: all 52 IDs assigned across 14 ordered children\n'
