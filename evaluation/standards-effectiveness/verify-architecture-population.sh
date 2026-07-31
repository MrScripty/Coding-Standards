#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
rg -F -q '[Architecture](topics/architecture.md)' "$R/CODING-STANDARDS.md"
for text in '## File Organization' '## Layered Architecture' 'Backend-Owned Data Principle' \
  'No Optimistic Updates' 'Composition Root for Runtime Wiring' 'usePollingController'; do
  ! rg -F -q "$text" "$R/CODING-STANDARDS.md"
done
mapfile -t ids < <(awk -F '\t' '$1>="STD-0137"&&$1<="STD-0147"{print $1}' "$S/consolidation-dispositions.tsv" | sort)
expected=(STD-{0137..0147})
[[ "${ids[*]}" == "${expected[*]}" ]]
rg -F -q '`7.4b8be` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bf` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-architecture-owner-contract.sh"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Architecture population passed: 11 exact dispositions, active child 15.3\n'
