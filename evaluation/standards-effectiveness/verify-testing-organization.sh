#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/verification/test-organization-decisions.tsv"

while IFS=$'\t' read -r case owner discovery tooling execution placement fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$owner" == contradictory ||
        "$discovery" == contradictory ]]; then actual=typed-invalid
  elif [[ "$tooling" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$owner" == missing || "$discovery" == missing ||
          "$tooling" == missing || "$execution" == missing ]]; then
    actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || exit 1
done < "$F"

for text in '## Test Placement And Naming' \
  'may use several placements' \
  'Follow required language, framework, runner' \
  'narrowest stable vocabulary' \
  'function_scenario_result'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done
rg -F -q 'workflows/verification.md#test-placement-and-naming' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q 'Prefer colocated tests' "$R/TESTING-STANDARDS.md"
! rg -F -q 'test_<function>_<scenario>_<expected_result>' "$R/TESTING-STANDARDS.md"

mapfile -t ids < <(awk -F '\t' '$1>="STD-0603"&&$1<="STD-0607"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0603 STD-0604 STD-0605 STD-0606 STD-0607' ]]
rg -F -q '`7.4b8ce` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8cg` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing organization passed: 16 decisions, 5 dispositions\n'
