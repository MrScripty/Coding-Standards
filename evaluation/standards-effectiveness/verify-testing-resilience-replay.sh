#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/resilience/replay-resumption-decisions.tsv"

while IFS=$'\t' read -r case contract history duplicate convergence partial boundary substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$history" == inferred ||
        "$duplicate" == contradictory || "$convergence" == missing ||
        "$partial" == unknown ]]; then
    actual=typed-invalid
  elif [[ "$contract" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$history" == missing || "$boundary" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"

for text in '## Replay And Resumption Evidence' \
  'authoritative history or checkpoint' \
  'projection convergence after recovery' \
  'repair or rejection of partial work' \
  'A pure helper, successful restart, empty-state' \
  'Do not restart from an inferred position'; do
  rg -F -q "$text" "$R/topics/resilience.md"
done
rg -F -q 'topics/resilience.md' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q 'These checks may be integration or end-to-end tests' \
  "$R/TESTING-STANDARDS.md"

row="$(awk -F '\t' '$1=="STD-0617" {print $2 FS $3 FS $4}' \
  "$S/consolidation-dispositions.tsv")"
[[ "$row" == $'TESTING-STANDARDS.md\ttopics/resilience.md\trefine' ]]
rg -F -q '`7.4b8bx` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8by` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9r` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing resilience replay passed: 14 decisions, 1 disposition\n'
