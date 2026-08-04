#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd "$S/../.."&&pwd)"
while IFS=$'\t' read -r case modality sequence focus visibility lifecycle capability fallback expected;do
 [[ "$case" == case ]]&&continue
 if [[ "$fallback" != none ]];then actual=typed-invalid
 elif [[ "$sequence" == contradictory || "$focus" == contradictory ]];then actual=typed-invalid
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$modality" == missing || "$sequence" == missing || "$focus" == missing || "$visibility" == missing || "$lifecycle" == missing || "$capability" == missing ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2;exit 1;}
done < "$S/fixtures/accessibility/focus-lifecycle-decisions.tsv"
for t in '## Input Modality Equivalence' '## Focus Visibility And Authority' '## Focus Lifecycle' 'does not establish another' 'fixed trap';do rg -F -q "$t" "$R/topics/accessibility.md";done
for t in '## Web Focus Mechanisms' ':focus-visible' 'outline-offset: 2px' 'Escape';do rg -F -q "$t" "$R/reference/recipes/accessibility.md";done
block="$(sed -n '/^## Keyboard And Focus/,/^## Names And Forms/p' "$R/ACCESSIBILITY-STANDARDS.md")";[[ "$block" == *Migrated* && "$block" != *':focus-visible'* ]]
mapfile -t ids < <(awk -F '\t' '$1>="STD-0013"&&$1<="STD-0016"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${ids[*]}" == 'STD-0013 STD-0014 STD-0015 STD-0016' ]]
rg -F -q '`7.4b18d` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-accessibility-interaction-semantics.sh"
printf 'Accessibility focus lifecycle passed: 15 decisions, 4 exact dispositions\n'
