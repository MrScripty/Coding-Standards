#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/performance/testing-evidence-decisions.tsv"

while IFS=$'\t' read -r case authority workload environment baseline measurement budget substitute expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$substitute" != none || "$authority" == contradictory ||
        "$workload" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$environment" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$environment" == missing || "$baseline" == missing ||
          "$measurement" == missing || "$budget" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"

for text in '## Performance Test Evidence' \
  'An ecosystem harness may improve' \
  'A performance budget names its authority' \
  'not copy a duration, percentage, sample count' \
  'successful harness execution as the required result'; do
  rg -F -q "$text" "$R/topics/performance.md"
done
rg -F -q 'topics/performance.md' \
  "$R/TESTING-STANDARDS.md"
! rg -F -q 'expect(duration).toBeLessThan(100)' "$R/TESTING-STANDARDS.md"
! rg -F -q "Use the ecosystem's benchmark harness" "$R/TESTING-STANDARDS.md"

mapfile -t ids < <(awk -F '\t' '$1>="STD-0642"&&$1<="STD-0644"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0642 STD-0643 STD-0644' ]]
rg -F -q '`7.4b8ca` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8cb` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9s` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing performance evidence passed: 15 decisions, 3 dispositions\n'
