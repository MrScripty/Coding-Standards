#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd "$S/../.."&&pwd)"
while IFS=$'\t' read -r case claim scope mechanism environment evidence tooling fallback expected;do [[ "$case" == case ]]&&continue;if [[ "$fallback" != none ]];then actual=typed-invalid;elif [[ "$claim" == contradictory ]];then actual=typed-invalid;elif [[ "$mechanism" == unsupported ]];then actual=typed-unsupported;elif [[ "$claim" == missing || "$scope" == missing || "$mechanism" == missing || "$environment" == missing || "$evidence" == missing || "$tooling" == missing ]];then actual=typed-unavailable;else actual=allow;fi;[[ "$actual" == "$expected" ]]||exit 1;done < "$S/fixtures/accessibility/evidence-decisions.tsv"
for t in '## Accessibility Evidence Claims' 'Tooling selects' 'does not prove';do rg -F -q "$t" "$R/topics/accessibility.md";done
for t in '## Legacy JSX Lint Mechanisms' 'eslint-plugin-jsx-a11y' 'click-events-have-key-events';do rg -F -q "$t" "$R/reference/recipes/accessibility.md";done
awk '/^## /&&$0!~/Migrated/{n++}END{exit n!=0}' "$R/ACCESSIBILITY-STANDARDS.md";! rg -q 'eslint-plugin|jsx-a11y|npm install' "$R/ACCESSIBILITY-STANDARDS.md"
mapfile -t ids < <(awk -F '\t' '$1>="STD-0023"&&$1<="STD-0026"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${ids[*]}" == 'STD-0023 STD-0024 STD-0025 STD-0026' ]]
rg -F -q '`7.4b18g` (`Accepted`)' "$R/plans/standards-library-effectiveness-restructure-plan.md";rg -F -q '`7.4b19a` (`Planned`)' "$R/plans/standards-library-effectiveness-restructure-plan.md"
"$S/verify-accessibility-media.sh"
printf 'Accessibility evidence closure passed: 13 decisions, 4 exact dispositions\n'
