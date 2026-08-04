#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd "$S/../.."&&pwd)"
while IFS=$'\t' read -r case purpose name relationship instructions state capability fallback expected;do
 [[ "$case" == case ]]&&continue
 if [[ "$fallback" != none ]];then actual=typed-invalid
 elif [[ "$name" == contradictory || "$relationship" == contradictory ]];then actual=typed-invalid
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$purpose" == missing || "$name" == missing || "$relationship" == missing || "$instructions" == missing || "$state" == missing || "$capability" == missing ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2;exit 1;}
done < "$S/fixtures/accessibility/name-input-decisions.tsv"
for t in '## Names And Descriptions' '## Input Relationships And Instructions' 'placeholder' 'Visual proximity';do rg -F -q "$t" "$R/topics/accessibility.md";done
for t in '## Web Naming And Form Mechanisms' 'aria-label="Delete item"' 'htmlFor="username"' 'type="search"';do rg -F -q "$t" "$R/reference/recipes/accessibility.md";done
block="$(sed -n '/^## Names And Forms/,/^## Media Semantics/p' "$R/ACCESSIBILITY-STANDARDS.md")";[[ "$block" == *Migrated* && "$block" != *'aria-label='* ]]
mapfile -t ids < <(awk -F '\t' '$1>="STD-0017"&&$1<="STD-0019"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${ids[*]}" == 'STD-0017 STD-0018 STD-0019' ]]
rg -F -q '`7.4b18e` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-accessibility-focus-lifecycle.sh"
printf 'Accessibility names and inputs passed: 14 decisions, 3 exact dispositions\n'
