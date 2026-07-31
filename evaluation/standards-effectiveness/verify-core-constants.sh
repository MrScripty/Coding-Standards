#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
while IFS=$'\t' read -r case meaning unit owner reuse variation fallback expected extra; do
  [[ "$case" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$meaning" == missing || "$unit" == missing || "$owner" == missing ]]; then actual=typed-unavailable
  elif [[ "$variation" == authorized ]]; then actual=configure
  elif [[ "$owner" == shared ]]; then actual=share
  elif [[ "$meaning" == obvious ]]; then actual=keep-local
  else actual=name
  fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/core/constants-decisions.tsv"
for text in '### Semantic Constants And Configuration' 'coordinated change must be explicit' \
  'narrowest concern that owns' 'imports do not transfer ownership' \
  'Do not turn invariants into settings'; do rg -F -q "$text" "$R/CORE-STANDARDS.md"; done
! rg -F -q '### No Magic Numbers or Strings' "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0148"&&$1<="STD-0150"{print $1}' "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0148 STD-0149 STD-0150' ]]
rg -F -q '`7.4b8bf` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bg` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Core constants passed: 12 decisions, 3 exact dispositions, active child 15.4\n'
