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
done < "$S/fixtures/tooling/lint-policy-decisions.tsv"
for text in '## Lint Policy And Orchestration' 'existing debt' 'Do not default to failing every warning' 'unless Verification selected' 'typed `invalid`' 'typed `unavailable`' 'typed `unsupported`'; do rg -F -q "$text" "$R/workflows/tooling.md"; done
for id in STD-0674 STD-0675; do awk -F '\t' -v id="$id" '$1==id&&$3=="workflows/tooling.md"&&$4=="refine"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"; done
! rg -F -q '1. **Fail on warnings**' "$R/TOOLING-STANDARDS.md"
printf 'Tooling lint policy passed: 10 decisions, 2 exact dispositions\n'
