#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/dependencies/audit-lineage-decisions.tsv"
readonly OWNER="$R/topics/dependencies.md"
readonly LEGACY="$R/TOOLING-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id scope evidence finding_owner automation \
  bootstrap fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none ]]; then
    actual=typed-invalid
  elif [[ "$scope" == missing || "$evidence" == missing ||
          "$finding_owner" == unknown || "$bootstrap" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

for text in '## Audit And Review' '## Automation And Bootstrap' \
  'Derive audit scope and cadence' \
  'prove only their declared detection contracts' \
  'Tools required to execute dependency checks are dependencies themselves' \
  'Do not install audit tools implicitly'; do
  rg -F -q "$text" "$OWNER"
done

rg -F -q '[Dependencies](topics/dependencies.md#audit-and-review)' "$LEGACY"
rg -F -q 'This heading indexes the non-normative' "$LEGACY"
rg -F -q 'legacy setup and package-script examples' "$LEGACY"
rg -F -q 'heading defines no required tool set' "$LEGACY"
! rg -F -q '[DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md)' "$LEGACY"

expected=(
  $'STD-0699\tTOOLING-STANDARDS.md\ttopics/dependencies.md\trefine'
  $'STD-0700\tTOOLING-STANDARDS.md\ttopics/dependencies.md\tindex'
)
mapfile -t actual < <(
  awk -F '\t' '$1 >= "STD-0699" && $1 <= "STD-0700" {
    print $1 "\t" $2 "\t" $3 "\t" $4
  }' "$DISPOSITIONS"
)
[[ "${actual[*]}" == "${expected[*]}" ]]

rg -F -q '`7.4b9r` (`Accepted`)' "$PLAN"
next_slice_block="$(awk '
  /^\*\*Next slice:\*\*/ { capture = 1 }
  capture && /^$/ { exit }
  capture { print }
' "$PLAN")"
[[ "$next_slice_block" == *'row 23'* ]]
for id in STD-0832; do
  [[ "$next_slice_block" == *"$id"* ]]
done
[[ "$next_slice_block" == *'row 23'* ]]

printf 'Dependency audit lineage passed: 12 decisions, 2 exact dispositions\n'
