#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case surface authority runtime_input projection evidence fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$authority" == contradictory ]]; then actual=typed-invalid
  elif [[ "$runtime_input" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$authority" == missing || "$projection" == missing ||
          "$evidence" == missing ]]; then actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2
    exit 1
  }
done < "$S/fixtures/typescript/owner-contract-decisions.tsv"
for text in 'ID: `profile.language.typescript`' '## Public Type Surfaces' \
  '## Runtime Boundaries' '## Contract Type Projection' \
  'Do not require explicit return types for every exported function' \
  'TypeScript types do not validate runtime values' \
  'wrapping every string or'; do
  rg -F -q "$text" "$R/profiles/languages/typescript.md"
done
rg -F -q '`profile.language.typescript`' \
  "$R/profiles/languages/typescript/async.md"
rg -F -q '[profiles/languages/typescript.md](profiles/languages/typescript.md)' \
  "$R/README.md"
rg -F -q '[TypeScript profile](profiles/languages/typescript.md)' \
  "$R/STANDARDS-ROUTER.md"
rg -F -q '[TypeScript profile](profiles/languages/typescript.md)' \
  "$R/CODING-STANDARDS.md"
! rg -F -q '// GOOD: Explicit return type' "$R/CODING-STANDARDS.md"
! rg -F -q 'Don'\''t pass raw `string` or `any`' "$R/CODING-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0184"&&$1<="STD-0186"{print $1}' \
  "$S/consolidation-dispositions.tsv" | sort)
[[ "${ids[*]}" == 'STD-0184 STD-0185 STD-0186' ]]
rg -F -q '`7.4b8bp` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8ca` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-milestone-7-row-15-decomposition.sh"
printf 'TypeScript owner contract passed: 17 decisions, 3 dispositions\n'
