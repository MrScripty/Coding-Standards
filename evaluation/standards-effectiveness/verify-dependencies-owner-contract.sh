#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/dependencies/owner-contract-decisions.tsv"
readonly OWNER="$R/topics/dependencies.md"
readonly ROUTER="$R/STANDARDS-ROUTER.md"
readonly README="$R/README.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly OVERLAY="$S/milestone-7-execution-decomposition.tsv"
readonly TRAIN="$S/milestone-7-execution-train.tsv"
readonly PACKAGES="$S/milestone-7-accelerated-packages.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id requirement owner candidate constraints \
  resolution authority evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$requirement" == contradictory ||
        "$authority" == missing ]]; then
    actual=typed-invalid
  elif [[ "$candidate" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$requirement" == missing || "$owner" == unknown ||
          "$constraints" == missing || "$resolution" == missing ||
          "$evidence" != complete ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

required_owner=(
  'ID: `topic.dependencies`'
  'Dependency Authority'
  'Requirement And Ownership'
  'Candidate Selection'
  'Resolution And Reproducibility'
  'Satisfaction And Provisioning'
  'Declare each dependency at the narrowest boundary'
  'Popularity, recency, download count'
  'automation authority'
  'typed `invalid`'
  'Do not continue with an incumbent'
)
for text in "${required_owner[@]}"; do
  rg -F -q "$text" "$OWNER"
done

rg -F -q 'Dependency requirement, ownership, selection, resolution, provisioning, update, or removal policy is required' "$ROUTER"
rg -F -q '[topics/dependencies.md](topics/dependencies.md)' "$README"

mapfile -t dispositions < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0496" && $1 <= "STD-0498" {
    print $1
  }' "$DISPOSITIONS"
)
[[ "${dispositions[*]}" == 'STD-0496 STD-0497 STD-0498' ]]

overlay_row="$(
  awk -F '\t' '$1 == 14 && $2 == 3 {
    print $3 "\t" $5 "\t" $6 "\t" $7 "\t" $8
  }' "$OVERLAY"
)"
[[ "$overlay_row" == $'STD-0496,STD-0497,STD-0498\ttopics/dependencies.md\texists\tpre-slice-review\tfocused' ]]

train_row="$(
  awk -F '\t' '$1 == 16 {
    print $3 "\t" $4 "\t" $6 "\t" $7 "\t" $8 "\t" $9
  }' "$TRAIN"
)"
[[ "$train_row" == $'STD-0300\tSTD-0348\ttopics/dependencies.md\texists\tpre-slice-review\tfocused' ]]

package_row="$(
  awk -F '\t' '$1 == 16 {
    print $3 "\t" $4 "\t" $5 "\t" $6 "\t" $8
  }' "$PACKAGES"
)"
[[ "$package_row" == $'consolidation\ttopics/dependencies.md\texisting-review\tdecision-table\tfull-suite' ]]

rg -F -q '`7.4b8ax` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8ay` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8az` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
[[ "$next_slice_line" == *'row 23'* ]]
[[ "$next_slice_line" == *'STD-0837'* ]]

"$S/verify-milestone-7-accelerated-execution-replan.sh"
"$S/verify-milestone-7-execution-train.sh"
"$S/check-plan-structure.sh" "$PLAN"
"$S/verify-plan-fixtures.sh"

printf 'Dependencies owner contract passed: 19 decisions, owner established\n'
