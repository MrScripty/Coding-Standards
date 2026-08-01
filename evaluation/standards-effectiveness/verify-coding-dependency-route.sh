#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
rg -F -q '## Dependency Management Legacy Route' "$R/CODING-STANDARDS.md"
rg -F -q '[Dependencies](topics/dependencies.md)' "$R/CODING-STANDARDS.md"
! sed -n '/## Dependency Management Legacy Route/,/## Code Style/p' \
  "$R/CODING-STANDARDS.md" | rg -F -q 'DEPENDENCY-STANDARDS.md'
mapfile -t rows < <(awk -F '\t' '$1=="STD-0157"{print $2 FS $3 FS $4}' \
  "$S/consolidation-dispositions.tsv")
[[ "${rows[*]}" == $'CODING-STANDARDS.md\tCODING-STANDARDS.md\tindex' ]]
rg -F -q '`7.4b8bi` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9e` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-dependencies-owner-contract.sh"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Coding dependency route passed: 1 exact index disposition\n'
