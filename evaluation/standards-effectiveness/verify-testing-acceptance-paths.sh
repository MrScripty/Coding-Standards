#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/verification/acceptance-path-decisions.tsv"

while IFS=$'\t' read -r case authority path boundaries environment result substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$authority" == contradictory ||
        "$boundaries" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$path" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$boundaries" == missing || "$environment" == missing ||
          "$result" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"

for text in '## Acceptance Paths And Boundaries' \
  'name the observable start' \
  'Repository suite labels such as unit' \
  'one path claim plus separate contract' \
  'This sequencing is a planning mechanism' \
  'partial traversal, checklist completion'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done
rg -F -q 'workflows/verification.md#acceptance-paths-and-boundaries' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q 'Test complete user workflows' "$R/TESTING-STANDARDS.md"
! rg -F -q 'Write the vertical slice acceptance test before' \
  "$R/TESTING-STANDARDS.md"
for route in 'topics/concurrency.md#isolate-verification-resources' \
  'profiles/boundaries/language-bindings.md#binding-evidence-cohorts' \
  'topics/resilience.md#replay-and-resumption-evidence'; do
  rg -F -q "$route" "$R/TESTING-STANDARDS.md"
done

mapfile -t ids < <(awk -F '\t' \
  '$1=="STD-0608"||$1=="STD-0609"||$1=="STD-0610"||
   $1=="STD-0612"||$1=="STD-0613"||$1=="STD-0614"||$1=="STD-0615" {print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0608 STD-0609 STD-0610 STD-0612 STD-0613 STD-0614 STD-0615' ]]
rg -F -q '`7.4b8cc` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8cj` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing acceptance paths passed: 16 decisions, 7 dispositions\n'
