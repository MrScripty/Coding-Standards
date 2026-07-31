#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly PACKAGES="$S/milestone-7-accelerated-packages.tsv"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly REPORT="$S/milestone-7-row-14-decomposition.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

expected_rows=(
  $'14\t1\tSTD-0487,STD-0488,STD-0489,STD-0490,STD-0491,STD-0492,STD-0493,STD-0494,STD-0499,STD-0501,STD-0502,STD-0503,STD-0504,STD-0505,STD-0506,STD-0507,STD-0511,STD-0512\tLAUNCHER-STANDARDS.md\tprofiles/applications/launcher.md\texists\tpre-slice-review\tfocused'
  $'14\t2\tSTD-0495\tLAUNCHER-STANDARDS.md\tworkflows/verification.md\texists\tpre-slice-review\tfocused'
  $'14\t3\tSTD-0496,STD-0497,STD-0498\tLAUNCHER-STANDARDS.md\ttopics/dependencies.md\texists\tpre-slice-review\tfocused'
  $'14\t4\tSTD-0500\tLAUNCHER-STANDARDS.md\tworkflows/release.md\texists\tpre-slice-review\tfocused'
  $'14\t5\tSTD-0508,STD-0509,STD-0510\tLAUNCHER-STANDARDS.md\ttopics/security.md\texists\tpre-slice-review\tfocused'
)
mapfile -t actual_rows < <(
  awk -F '\t' '$1 == 14 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8
  }' "$OVERLAY"
)
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

expected_ids=(STD-{0487..0512})
mapfile -t actual_ids < <(
  awk -F '\t' '$1 == 14 {
    count = split($3, ids, ",")
    for (i = 1; i <= count; i += 1) print ids[i]
  }' "$OVERLAY" | sort
)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

expected_dispositions=(
  STD-0487 STD-0488 STD-0489 STD-0490 STD-0491 STD-0492 STD-0493
  STD-0494 STD-0495 STD-0496 STD-0497 STD-0498 STD-0499 STD-0500
  STD-0501 STD-0502 STD-0503 STD-0504 STD-0505
  STD-0506 STD-0507 STD-0508 STD-0509 STD-0510 STD-0511 STD-0512
)
mapfile -t dispositions < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0487" && $1 <= "STD-0512" {
    print $1
  }' "$DISPOSITIONS" | sort
)
[[ "${dispositions[*]}" == "${expected_dispositions[*]}" ]]

package_row="$(
  awk -F '\t' '$1 == 14 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $8 \
      "\t" $9 "\t" $10
  }' "$PACKAGES"
)"
[[ "$package_row" == $'14\tP09\trefinement\tprofiles/applications/launcher.md\texisting-review\tdecision-table\tfull-suite\tlauncher-row-decomposition\tcore,workflow.verification,workflow.release,topic.resilience,topic.security' ]]

[[ -e "$R/profiles/applications/launcher.md" ]]
[[ -e "$R/workflows/verification.md" ]]
[[ -e "$R/topics/dependencies.md" ]]
[[ -e "$R/workflows/release.md" ]]
[[ -e "$R/topics/security.md" ]]

required_report=(
  'do not share one canonical owner'
  '### Child 14.1: Launcher Population And Structural Closure'
  '### Child 14.2: GUI Smoke Acceptance'
  '### Child 14.3: Dependencies Owner And Population'
  '### Child 14.4: Build Procedure'
  '### Child 14.5: Generated Command Security'
  'successful build no-ops'
  'typed outcomes'
  'no normative or legacy standard'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '`7.4b8au` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8av` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aw` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ax` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ay` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8az` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b8bd'* ]]
[[ "$next_slice_line" == *'STD-0137'* ]]
[[ "$next_slice_line" == *'STD-0147'* ]]

"$S/verify-milestone-7-accelerated-execution-replan.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Milestone 7 row-14 decomposition passed: all 26 IDs assigned across 5 ordered children\n'
