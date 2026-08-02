#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case direction boundary input proof outcome capability fallback expected; do
  [[ "$case" == case ]] && continue
  actual=allow
  if [[ "$direction" == internal ]]; then
    [[ "$boundary" == same && "$input" == validated && "$proof" == retained &&
       "$fallback" == none ]] || actual=typed-invalid
  elif [[ "$capability" == unavailable ]]; then
    actual=typed-unavailable
  elif [[ "$outcome" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$proof" != complete || "$fallback" != none ]]; then
    actual=typed-invalid
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/contracts/boundary-proof-decisions.tsv"
for text in '## Inbound And Outbound Boundary Proof' 'Apply the complete applicable contract in both directions' 'classify the operation or' 'does not mandate HTTP status checks' 'alternate parser'; do
  rg -F -q "$text" "$R/topics/contracts.md"
done
! rg -F -q '### Validate at Boundaries' "$R/CODING-STANDARDS.md"
! rg -F -q '### Validate Outbound Responses' "$R/CODING-STANDARDS.md"
rg -F -q 'topics/contracts.md#inbound-and-outbound-boundary-proof' "$R/CODING-STANDARDS.md"
rg -F -q 'topics/contracts.md#inbound-and-outbound-boundary-proof' "$R/ARCHITECTURE-PATTERNS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0155"&&$1<="STD-0156"{print $1}' "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0155 STD-0156' ]]
rg -F -q '`7.4b8bh` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9s` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Contract boundary proof passed: 15 decisions, 2 dispositions\n'
