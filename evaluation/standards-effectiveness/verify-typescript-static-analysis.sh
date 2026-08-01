#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r c facts authority capability boundary fallback expected extra; do
 [[ "$c" == case ]]&&continue; [[ -z "${extra:-}" ]]
 if [[ "$fallback" != none || "$facts" == contradictory ]];then actual=typed-invalid
 elif [[ "$authority" == missing || "$boundary" == missing ]];then actual=typed-unavailable
 elif [[ "$capability" == unsupported ]];then actual=typed-unsupported;else actual=allow;fi
 [[ "$actual" == "$expected" ]]
done < "$S/fixtures/typescript/static-analysis-decisions.tsv"
for t in '## Static Analysis And Compiler Configuration' 'actual TypeScript project boundaries' 'Architecture analysis must derive' 'parser, preset, formatter integration' 'are `invalid`' 'is `unavailable`' 'is `unsupported`';do rg -F -q "$t" "$R/profiles/languages/typescript.md";done
for id in STD-0677 STD-0678 STD-0679 STD-0680;do awk -F '\t' -v id="$id" '$1==id&&$3=="profiles/languages/typescript.md"&&$4=="split"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv";done
rg -F -q '## TypeScript Tooling Examples' "$R/reference/recipes/tooling.md"
! rg -F -q 'Enable all strict checks for type safety' "$R/TOOLING-STANDARDS.md"
printf 'TypeScript static analysis passed: 10 decisions, 4 split dispositions\n'
