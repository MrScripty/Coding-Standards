#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/verification/supporting-gate-diagnosis-decisions.tsv"

while IFS=$'\t' read -r case claim gate evidence authority observation substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$claim" == contradictory ||
        "$evidence" == contradictory || "$authority" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$observation" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$claim" == missing || "$authority" == missing ||
          "$observation" == missing ]]; then actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || exit 1
done < "$F"

for text in '## Supporting Gates And Claim-Directed Diagnosis' \
  'supporting gate and cannot replace' 'information gain' \
  'source order is' 'default acceptance'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done
rg -F -q 'workflows/verification.md' "$R/TESTING-STANDARDS.md"
! rg -F -q 'Is it a compiler/type error?' "$R/TESTING-STANDARDS.md"
! rg -F -q 'Always compile after edits' "$R/TESTING-STANDARDS.md"

mapfile -t ids < <(awk -F '\t' '$1>="STD-0645"&&$1<="STD-0652"{print $1}' "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0645 STD-0646 STD-0647 STD-0648 STD-0649 STD-0650 STD-0651 STD-0652' ]]
rg -F -q '`7.4b8ci` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9l` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing gates diagnosis passed: 16 decisions, 8 dispositions\n'
