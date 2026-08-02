#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case_id facts authority capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue; [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$facts" == contradictory ]]; then actual=typed-invalid
  elif [[ "$authority" == missing || "$evidence" == missing ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/implementation/change-evidence-decisions.tsv"
for text in '## Change-Description Evidence' 'affected risk' \
  'Do not default to a pull request' 'are `invalid`' 'is `unavailable`' \
  '`unsupported`; do not substitute'; do rg -F -q "$text" "$R/workflows/implementation.md"; done
awk -F '\t' '$1=="STD-0698"&&$3=="workflows/implementation.md"&&$4=="split"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"
for text in 'ID: `reference.recipes.implementation`' '## Pull-Request Template Example' \
  'mkdir -p .github' 'define no fallback'; do rg -F -q "$text" "$R/reference/recipes/implementation.md"; done
for legacy in 'mkdir -p .github' 'PULL_REQUEST_TEMPLATE.md'; do ! rg -F -q "$legacy" "$R/TOOLING-STANDARDS.md"; done
printf 'Implementation change evidence passed: 13 decisions, 1 split disposition\n'
