#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/frontend/testing-evidence-decisions.tsv"

while IFS=$'\t' read -r case claim environment interaction lifecycle substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$interaction" == ambiguous ||
        "$interaction" == inaccessible ]]; then
    actual=typed-invalid
  elif [[ "$interaction" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$environment" == missing || "$lifecycle" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"

for text in 'Select interaction evidence from the user-observable contract' \
  'A selector or event-dispatch API is not evidence' \
  'require a representative browser environment' \
  'DOM shim do not prove browser integration' \
  'A successful update does not prove cleanup'; do
  rg -F -q "$text" "$R/profiles/applications/frontend.md"
done
rg -F -q 'profiles/applications/frontend.md' \
  "$R/TESTING-STANDARDS.md" "$R/FRONTEND-STANDARDS.md"
! rg -F -q 'Use `userEvent` for user flows' "$R/FRONTEND-STANDARDS.md"
! rg -F -q 'Mock geometry on specific elements' "$R/FRONTEND-STANDARDS.md"

row="$(awk -F '\t' '$1=="STD-0641" {print $2 FS $3 FS $4}' \
  "$S/consolidation-dispositions.tsv")"
[[ "$row" == $'TESTING-STANDARDS.md\tprofiles/applications/frontend.md\trefine' ]]
rg -F -q '`7.4b8bz` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9s` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing frontend evidence passed: 15 decisions, 1 disposition\n'
