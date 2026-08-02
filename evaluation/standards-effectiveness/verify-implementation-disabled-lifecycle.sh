#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case state owner surfaces tracking exit_criteria review production_stub expected; do
  [[ "$case" == case ]] && continue
  if [[ "$production_stub" != none && "$production_stub" != test-only ]]; then actual=typed-invalid
  elif [[ "$state" == invalid ]]; then actual=typed-invalid
  elif [[ "$state" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$owner" == missing || "$surfaces" == missing ||
          "$tracking" == missing || "$exit_criteria" == missing ||
          "$review" == missing ]]; then actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/implementation/disabled-lifecycle-decisions.tsv"
for text in '## Disabled And Incomplete Behavior' \
  'remove deliberately unsupported capability' \
  'keep incomplete implementation unreachable' \
  'must agree with the selected lifecycle state' \
  'silent no-op' 'typed `unavailable`, `unsupported`, or `invalid`'; do
  rg -F -q "$text" "$R/workflows/implementation.md"
done
! rg -F -q 'Status: DISABLED' "$R/CODING-STANDARDS.md"
! rg -F -q 'GOOD: Do not register the route' "$R/CODING-STANDARDS.md"
rg -F -q 'workflows/implementation.md#disabled-and-incomplete-behavior' \
  "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0174"&&$1<="STD-0177"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0174 STD-0175 STD-0176 STD-0177' ]]
rg -F -q '`7.4b8bl` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9s` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Implementation disabled lifecycle passed: 15 decisions, 4 dispositions\n'
