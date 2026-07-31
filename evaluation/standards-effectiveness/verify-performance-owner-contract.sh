#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case authority workload environment baseline evidence mechanism fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$authority" == contradictory || "$workload" == contradictory ]]; then
    actual=typed-invalid
  elif [[ "$environment" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$authority" == missing || "$environment" == missing ||
          "$baseline" == missing || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/performance/owner-contract-decisions.tsv"
for text in 'ID: `topic.performance`' '## Performance Claim Authority' \
  '## Measurement Contract' '## Optimization Decision' \
  '## Benchmarks And Regression Evidence' \
  'does not independently' 'mechanisms, not defaults' \
  'Documentation records durable claim'; do
  rg -F -q "$text" "$R/topics/performance.md"
done
rg -F -q '[topics/performance.md](topics/performance.md)' "$R/README.md"
rg -F -q '[Performance](topics/performance.md)' "$R/STANDARDS-ROUTER.md"
rg -F -q '[Performance](topics/performance.md)' "$R/CODING-STANDARDS.md"
! rg -F -q 'Avoid allocations in hot paths' "$R/CODING-STANDARDS.md"
! rg -F -q 'Code runs once at startup' "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0188"&&$1<="STD-0194"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0188 STD-0189 STD-0190 STD-0191 STD-0192 STD-0193 STD-0194' ]]
rg -F -q '`7.4b8br` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bx` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Performance owner contract passed: 18 decisions, 7 dispositions\n'
