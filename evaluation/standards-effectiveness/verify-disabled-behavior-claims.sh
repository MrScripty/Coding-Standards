#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case state surfaces typed_outcome lifecycle_facts direct_behavior test_isolation fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none || "$surfaces" != complete ||
        "$typed_outcome" != proved || "$direct_behavior" != proved ]]; then
    actual=blocked
  elif [[ "$state" != removed && "$lifecycle_facts" != proved ]]; then
    actual=blocked
  elif [[ "$state" == incomplete && "$test_isolation" != proved ]]; then
    actual=blocked
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/verification/disabled-behavior-decisions.tsv"
for text in '## Disabled Behavior Claims' \
  'every affected advertised, registered' \
  'unreachable from production consumers' \
  'configuration check may prove one local state' \
  'Acceptance remains blocked' \
  'observable disabled behavior.'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done
! rg -F -q '### Review Checklist' "$R/CODING-STANDARDS.md"
! rg -F -q 'Issue created for tracking' "$R/CODING-STANDARDS.md"
rg -F -q 'workflows/verification.md#disabled-behavior-claims' \
  "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1=="STD-0178"{print $1}' \
  "$S/consolidation-dispositions.tsv")
[[ "${ids[*]}" == 'STD-0178' ]]
rg -F -q '`7.4b8bm` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8cf` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Disabled behavior claims passed: 15 decisions, 1 disposition\n'
