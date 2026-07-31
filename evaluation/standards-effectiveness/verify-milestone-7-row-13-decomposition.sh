#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly PACKAGES="$S/milestone-7-accelerated-packages.tsv"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly REPORT="$S/milestone-7-row-13-decomposition.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

expected_rows=(
  $'13\t1\tSTD-0273\tCONCURRENCY-STANDARDS.md\tprofiles/languages/csharp/async.md\texists\tpre-slice-review\tfocused'
  $'13\t2\tSTD-0274\tCONCURRENCY-STANDARDS.md\tCONCURRENCY-STANDARDS.md\texists\tpre-slice-review\tfocused'
  $'13\t3\tSTD-0275,STD-0276\tCONCURRENCY-STANDARDS.md\tprofiles/languages/typescript/async.md\texists\tpre-slice-review\tfocused'
  $'13\t4\tSTD-0277,STD-0278,STD-0279\tCONCURRENCY-STANDARDS.md\tprofiles/frameworks/godot.md\texists\tpre-slice-review\tfocused'
)
mapfile -t actual_rows < <(
  awk -F '\t' '$1 == 13 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8
  }' "$OVERLAY"
)
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

expected_ids=(STD-{0273..0279})
mapfile -t actual_ids < <(
  awk -F '\t' '$1 == 13 {
    count = split($3, ids, ",")
    for (i = 1; i <= count; i += 1) print ids[i]
  }' "$OVERLAY"
)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

mapfile -t dispositions < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0273" && $1 <= "STD-0279" {
    print $1
  }' "$DISPOSITIONS"
)
[[ "${dispositions[*]}" == 'STD-0273 STD-0274 STD-0275 STD-0276 STD-0277 STD-0278 STD-0279' ]]

package_row="$(
  awk -F '\t' '$1 == 13 {
    print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $8 \
      "\t" $9 "\t" $10
  }' "$PACKAGES"
)"
[[ "$package_row" == $'13\tP08\trefinement\ttopics/concurrency.md\texisting-review\tdecision-table\tfocused\tasync-specialization-row-decomposition\tcore,workflow.verification' ]]

[[ -e "$R/profiles/languages/csharp/async.md" ]]
[[ -e "$R/profiles/languages/typescript/async.md" ]]
[[ -e "$R/profiles/frameworks/godot.md" ]]

required_report=(
  'do not share a specialization owner'
  '### Child 13.1: C# Async Owner And Population'
  '### Child 13.2: Rust Routing Index'
  '### Child 13.3: TypeScript Async Owner And Population'
  '### Child 13.4: Godot Framework Owner And Population'
  'silent stale-result discard'
  '`CallDeferred` and `IsInstanceValid` are available mechanisms'
  'typed diagnostics'
  'changes no normative or legacy standard'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '`7.4b8al` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8am` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8an` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ao` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ap` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aq` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ar` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8as` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8at` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8au` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8av` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8aw` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ax` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ay` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8az` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'Milestone 7.4b8bs'* ]]

"$S/verify-milestone-7-accelerated-execution-replan.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Milestone 7 row-13 decomposition passed: all 7 IDs accepted across 4 ordered children\n'
