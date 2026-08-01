#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/verification/focused-test-design-decisions.tsv"

while IFS=$'\t' read -r case claim structure boundary domain oracle substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$claim" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$claim" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$boundary" == missing || "$domain" == missing || "$oracle" == missing ]]; then
    actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || exit 1
done < "$F"

for text in 'one coherent observable claim or invariant' \
  'Do not split or combine checks' 'preference hierarchy' \
  'not universal requirements' 'generation, shrinking, reproducibility' \
  'Never weaken an assertion'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done
rg -F -q 'workflows/verification.md' "$R/TESTING-STANDARDS.md"
! rg -F -q 'Prefer (in order)' "$R/TESTING-STANDARDS.md"
! rg -F -q 'Always test:' "$R/TESTING-STANDARDS.md"

mapfile -t ids < <(awk -F '\t' '$1>="STD-0618"&&$1<="STD-0624"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0618 STD-0619 STD-0620 STD-0621 STD-0622 STD-0623 STD-0624' ]]
rg -F -q '`7.4b8cd` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9d` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing focused design passed: 16 decisions, 7 dispositions\n'
