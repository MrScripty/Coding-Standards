#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/dependencies/standards-consolidation-decisions.tsv"
while IFS=$'\t' read -r case requirement ownership candidate compatibility footprint audit automation fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none || "$requirement" == contradictory ||
        "$ownership" == contradictory ]]; then actual=typed-invalid
  elif [[ "$candidate" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$requirement" == missing || "$ownership" == unknown ||
          "$compatibility" == missing || "$audit" == missing ]]; then
    actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"
for text in '## Compatibility And Lifecycle' '## Features And Footprint' \
  '## Audit And Review' '## Automation And Bootstrap' \
  'version labels and changelogs' \
  'mechanisms, not defaults' 'prove only their declared detection contracts' \
  'dependencies themselves'; do
  rg -F -q "$text" "$R/topics/dependencies.md"
done
rg -F -q '# Dependency Standards Migration Index' "$R/DEPENDENCY-STANDARDS.md"
rg -F -q '[Dependencies](topics/dependencies.md)' "$R/DEPENDENCY-STANDARDS.md"
! rg -F -q 'Build-or-Depend Decision Matrix' "$R/DEPENDENCY-STANDARDS.md"
! rg -F -q 'Transitive Dependency Thresholds' "$R/DEPENDENCY-STANDARDS.md"
! rg -F -q 'Example CI Workflow' "$R/DEPENDENCY-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0300"&&$1<="STD-0348"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
expected=(STD-{0300..0348})
[[ "${ids[*]}" == "${expected[*]}" ]]
rg -F -q '`7.4b8bs` (`Accepted`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b9m` (`Planned`)' \
  "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-dependencies-owner-contract.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Dependency standards consolidation passed: 20 decisions, 49 dispositions\n'
