#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/verification/test-data-lifecycle-decisions.tsv"

while IFS=$'\t' read -r case authority identity construction mutation isolation lifecycle substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$authority" == contradictory ||
        "$identity" == contradictory || "$lifecycle" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$isolation" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$authority" == missing || "$identity" == missing ||
          "$lifecycle" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || exit 1
done < "$F"

for text in '## Test Data Authority And Lifecycle' \
  'none is a default hierarchy' 'lifetime independently' \
  'carries no originating check input' 'passing retries'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done
rg -F -q 'workflows/verification.md' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q '// GOOD: Factory with defaults' "$R/TESTING-STANDARDS.md"
! rg -F -q '// GOOD: Fresh state per test' "$R/TESTING-STANDARDS.md"

mapfile -t ids < <(awk -F '\t' '$1>="STD-0632"&&$1<="STD-0634"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0632 STD-0633 STD-0634' ]]
rg -F -q '`7.4b8cg` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9s` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing data lifecycle passed: 16 decisions, 3 dispositions\n'
