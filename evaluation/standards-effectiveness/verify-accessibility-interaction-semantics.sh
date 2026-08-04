#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case purpose role capability modalities state feedback fallback expected; do
  [[ "$case" == case ]] && continue
  if [[ "$fallback" != none ]]; then actual=typed-invalid
  elif [[ "$purpose" == contradictory || "$role" == contradictory ]]; then actual=typed-invalid
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  elif [[ "$purpose" == missing || "$role" == missing || "$capability" == missing ||
          "$modalities" == missing || "$state" == missing || "$feedback" == missing ]]; then
    actual=typed-unavailable
  else actual=allow
  fi
  [[ "$actual" == "$expected" ]] || { printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2; exit 1; }
done < "$S/fixtures/accessibility/interaction-semantics-decisions.tsv"
for text in '## Semantic Meaning And Role' '## Action And Navigation Outcomes' \
  '## Custom Interaction Outcomes' 'preferred only on that evidence' \
  'not prove another modality'; do rg -F -q "$text" "$R/topics/accessibility.md"; done
for text in '## Web Interaction Mechanisms' '<button type="button"' \
  '<a href="/settings">' 'role="button"'; do rg -F -q "$text" "$R/reference/recipes/accessibility.md"; done
legacy_block="$(sed -n '/^## Interaction Semantics/,/^## Keyboard And Focus/p' "$R/ACCESSIBILITY-STANDARDS.md")"
[[ "$legacy_block" != *'<button'* && "$legacy_block" != *'role="button"'* &&
   "$legacy_block" == *'Migrated'* ]]
mapfile -t ids < <(awk -F '\t' '$1>="STD-0008"&&$1<="STD-0012"{print $1}' "$S/consolidation-dispositions.tsv")
[[ "${ids[*]}" == 'STD-0008 STD-0009 STD-0010 STD-0011 STD-0012' ]]
rg -F -q '`7.4b18c` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-accessibility-owner-contract.sh"
"$S/verify-milestone-7-row-28-decomposition.sh"
printf 'Accessibility interaction semantics passed: 15 decisions, 5 exact dispositions\n'
