#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd "$S/../.."&&pwd)"
while IFS=$'\t' read -r c facts authority capability scope fallback expected extra;do
 [[ "$c" == case ]]&&continue;[[ -z "${extra:-}" ]]
 if [[ "$fallback" != none || "$facts" == contradictory ]];then actual=typed-invalid
 elif [[ "$authority" == missing || "$scope" == missing ]];then actual=typed-unavailable
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi
 [[ "$actual" == "$expected" ]]
done < "$S/fixtures/tooling/formatting-policy-decisions.tsv"
for t in '## Formatting Policy And Orchestration' 'formatter and linter' 'Do not default to format-on-save' 'mutation authority' '`invalid`' '`unavailable`' '`unsupported`';do rg -F -q "$t" "$R/workflows/tooling.md";done
for id in STD-0681 STD-0683;do awk -F '\t' -v id="$id" '$1==id&&$3=="workflows/tooling.md"&&$4=="refine"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv";done
for id in STD-0682 STD-0686;do awk -F '\t' -v id="$id" '$1==id&&$3=="workflows/tooling.md"&&$4=="split"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv";done
rg -F -q '## Formatting Automation Examples' "$R/reference/recipes/tooling.md"
! rg -F -q '"editor.formatOnSave": true' "$R/TOOLING-STANDARDS.md"
! rg -F -q 'npm install eslint-config-prettier' "$R/TOOLING-STANDARDS.md"
printf 'Tooling formatting policy passed: 10 decisions, 2 direct and 2 split dispositions\n'
