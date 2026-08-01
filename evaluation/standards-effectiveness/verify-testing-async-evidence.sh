#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/verification/async-completion-decisions.tsv"

while IFS=$'\t' read -r case completion states boundary timing diagnostics mechanism substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$completion" == contradictory ||
        "$states" == contradictory || "$boundary" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$mechanism" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$completion" == missing || "$states" == missing ||
          "$timing" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || exit 1
done < "$F"

for text in '## Async Completion And Failure Evidence' \
  'terminal state and externally meaningful' 'not a universal pair' \
  'cannot substitute for the selected boundary' 'weaker-boundary evidence'; do
  rg -F -q "$text" "$R/workflows/verification.md"
done
rg -F -q 'workflows/verification.md' \
  "$R/TESTING-STANDARDS.md"
rg -F -q '[Concurrency](topics/concurrency.md)' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q '// GOOD: Properly awaited' "$R/TESTING-STANDARDS.md"
! rg -F -q 'Upstream non-success responses' "$R/TESTING-STANDARDS.md"

mapfile -t ids < <(awk -F '\t' '$1=="STD-0636"||$1=="STD-0637"||$1=="STD-0638"||$1=="STD-0640"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0636 STD-0637 STD-0638 STD-0640' ]]
rg -F -q '`7.4b8ch` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9m` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing async evidence passed: 16 decisions, 4 dispositions\n'
