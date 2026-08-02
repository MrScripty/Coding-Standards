#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case_id facts authority capability scope fallback expected extra; do
  [[ "$case_id" == case ]] && continue; [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$facts" == contradictory ]]; then actual=typed-invalid
  elif [[ "$authority" == missing || "$scope" == missing ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/tooling/debt-cost-decisions.tsv"
for text in '## Tool-Debt Governance' '## Automation Cost And Operational Evidence' \
  'Do not default to a committed snapshot' 'Do not default to caching' \
  'is `invalid`' 'is `unavailable`' 'is `unsupported`'; do rg -F -q "$text" "$R/workflows/tooling.md"; done
awk -F '\t' '$1=="STD-0691"&&$3=="workflows/tooling.md"&&$4=="refine"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"
awk -F '\t' '$1=="STD-0692"&&$3=="workflows/tooling.md"&&$4=="split"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"
rg -F -q '## Automation Cost Examples' "$R/reference/recipes/tooling.md"
for legacy in 'Keep a committed baseline snapshot' 'actions/setup-node@v4' 'actions/upload-artifact@v4' 'inside a live matrix run'; do ! rg -F -q "$legacy" "$R/TOOLING-STANDARDS.md"; done
printf 'Tooling debt and cost passed: 16 decisions, 1 direct and 1 split disposition\n'
