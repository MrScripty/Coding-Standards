#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r case classification owner cause context fallback expected extra; do
 [[ "$case" == case ]] && continue; [[ -z "${extra:-}" ]]
 if [[ "$fallback" != none || "$classification" == contradictory ]]; then actual=typed-invalid
 elif [[ "$owner" == missing || "$cause" == missing || "$context" == missing ]]; then actual=typed-unavailable
 else actual=allow; fi
 [[ "$actual" == "$expected" ]]
done < "$S/fixtures/resilience/failure-boundary-decisions.tsv"
for text in '## Failure Boundaries And Diagnostics' 'narrowest' 'Preserve original' 'Do not mandate logging' 'successful fallback'; do rg -F -q "$text" "$R/topics/resilience.md"; done
mapfile -t ids < <(awk -F '\t' '$1>="STD-0151"&&$1<="STD-0154"{print $1}' "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0151 STD-0152 STD-0153 STD-0154' ]]
rg -F -q '`7.4b8bg` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bh` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Resilience failure boundaries passed: 12 decisions, 4 dispositions\n'
