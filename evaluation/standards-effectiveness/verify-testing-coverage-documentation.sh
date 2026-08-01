#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/verification/coverage-documentation-decisions.tsv"

while IFS=$'\t' read -r case claim metric scope authority baseline context substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$metric" == contradictory ||
        "$authority" == contradictory ]]; then actual=typed-invalid
  elif [[ "$metric" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$authority" == missing || "$baseline" == missing ||
          "$context" == missing ]]; then actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || exit 1
done < "$F"

for text in '## Coverage And Durable Evidence Records' \
  'does not prove observable' 'named risk or claim' \
  'cannot be recovered from the check name' \
  'requiring an inline comment' 'successful instrumentation'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done
rg -F -q 'workflows/verification.md' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q 'Simple getters/setters with no logic' "$R/TESTING-STANDARDS.md"
! rg -F -q 'directly above the test' "$R/TESTING-STANDARDS.md"

mapfile -t ids < <(awk -F '\t' '$1>="STD-0625"&&$1<="STD-0631"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0625 STD-0626 STD-0627 STD-0628 STD-0629 STD-0630 STD-0631' ]]
rg -F -q '`7.4b8cf` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9h` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing coverage documentation passed: 16 decisions, 7 dispositions\n'
