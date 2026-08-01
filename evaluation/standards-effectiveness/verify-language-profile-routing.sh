#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case condition facts profile capability fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$condition" == none ]]; then actual=no-profile
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$facts" == missing || "$profile" == missing ||
          "$capability" == unavailable ]]; then actual=typed-unavailable
  else actual=route
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/routing/language-profile-decisions.tsv"
rg -F -q '## Language-Specific Guidelines Legacy Route' "$R/CODING-STANDARDS.md"
rg -F -q 'STANDARDS-ROUTER.md#language-profiles' "$R/CODING-STANDARDS.md"
rg -F -q 'policy remains in Core, workflows, and topics.' \
  "$R/CODING-STANDARDS.md"
! rg -F -q 'languages/<language>/' "$R/CODING-STANDARDS.md"
! rg -F -q 'Existing inline ecosystem sections can be migrated incrementally' \
  "$R/CODING-STANDARDS.md"
for text in '## Language Profiles' \
  'No language-specific mechanism changes' \
  'Language profiles specialize mechanisms only'; do
  rg -F -q "$text" "$R/STANDARDS-ROUTER.md"
done
mapfile -t ids < <(awk -F '\t' '$1=="STD-0183"{print $1}' \
  "$S/consolidation-dispositions.tsv")
[[ "${ids[*]}" == 'STD-0183' ]]
rg -F -q '`7.4b8bo` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8ce` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'Language profile routing passed: 13 decisions, 1 disposition\n'
