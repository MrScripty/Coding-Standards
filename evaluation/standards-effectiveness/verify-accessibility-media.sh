#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd "$S/../.."&&pwd)"
while IFS=$'\t' read -r case meaning classification equivalent context state capability fallback expected;do
 [[ "$case" == case ]]&&continue
 if [[ "$fallback" != none ]];then actual=typed-invalid
 elif [[ "$classification" == contradictory ]];then actual=typed-invalid
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$meaning" == missing || "$classification" == missing || "$equivalent" == missing || "$context" == missing || "$state" == missing || "$capability" == missing ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s, got %s\n' "$case" "$expected" "$actual" >&2;exit 1;}
done < "$S/fixtures/accessibility/media-decisions.tsv"
for t in '## Media Meaning And Classification' '## Equivalent Media Outcomes' 'filename' 'library convention';do rg -F -q "$t" "$R/topics/accessibility.md";done
for t in '## Web Image And Icon Mechanisms' 'alt=""' 'alt="Error"' 'aria-hidden="true"';do rg -F -q "$t" "$R/reference/recipes/accessibility.md";done
block="$(sed -n '/^## Media Semantics/,/^## Linting Enforcement/p' "$R/ACCESSIBILITY-STANDARDS.md")";[[ "$block" == *Migrated* && "$block" != *'<img'* ]]
mapfile -t ids < <(awk -F '\t' '$1>="STD-0020"&&$1<="STD-0022"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${ids[*]}" == 'STD-0020 STD-0021 STD-0022' ]]
rg -F -q '`7.4b18f` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-accessibility-name-input.sh"
printf 'Accessibility media semantics passed: 13 decisions, 3 exact dispositions\n'
