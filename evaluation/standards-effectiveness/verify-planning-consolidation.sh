#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/planning/consolidation-decisions.tsv"
while IFS=$'\t' read -r case objective scope facts ownership acceptance next_slice fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none || "$objective" == contradictory ||
        "$ownership" == overlap || "$next_slice" == multiple ]]; then
    actual=typed-invalid
  elif [[ "$facts" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$facts" == missing || "$acceptance" == missing ]]; then
    actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"
for text in '## When A Written Plan Is Required' '## Artifact Model' \
  '## Required Active-Plan Fields' '## Milestones And Slices' \
  '## Current State, Not History' '## Re-Planning' '## Concurrent Work' \
  'Do not substitute a headless path' '`Implemented` is not complete'; do
  rg -F -q "$text" "$R/workflows/planning.md"
done
rg -F -q '# Plan Standards' "$R/PLAN-STANDARDS.md"
rg -F -q '[workflows/planning.md](workflows/planning.md)' \
  "$R/PLAN-STANDARDS.md"
rg -F -q 'contains no independent normative planning' "$R/PLAN-STANDARDS.md"
! rg -F -q '## When a Plan Is Required' "$R/PLAN-STANDARDS.md"
! rg -F -q '## Concurrent Worker Execution' "$R/PLAN-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0513"&&$1<="STD-0530"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
expected=(STD-{0513..0530})
[[ "${ids[*]}" == "${expected[*]}" ]]
rg -F -q '`7.4b8bt` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bu` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9d` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-execution-train.sh"
printf 'Planning consolidation passed: 17 decisions, 18 dispositions\n'
