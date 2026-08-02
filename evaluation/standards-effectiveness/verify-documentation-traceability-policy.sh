#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case_id facts mapping input capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue; [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$facts" == contradictory ]]; then actual=typed-invalid
  elif [[ "$mapping" == missing || "$input" == missing ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/documentation/traceability-policy-decisions.tsv"
for text in '## Decision Traceability' 'project-owned trigger paths' \
  'evaluates only index state' 'Do not default to a `src/` directory' \
  'is `invalid`' 'are `unavailable`' '`unsupported`; do not infer'; do rg -F -q "$text" "$R/workflows/documentation.md"; done
awk -F '\t' '$1=="STD-0696"&&$3=="workflows/documentation.md"&&$4=="index"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"
awk -F '\t' '$1=="STD-0697"&&$3=="workflows/documentation.md"&&$4=="split"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"
for text in '## Decision Traceability Examples' 'trigger_path' \
  'check-decision-traceability.sh --mode staged' '--base-ref'; do rg -F -q -- "$text" "$R/reference/recipes/documentation.md"; done
for legacy in 'trigger_path' 'check-decision-traceability.sh --mode staged' '--base-ref'; do ! rg -F -q -- "$legacy" "$R/TOOLING-STANDARDS.md"; done
printf 'Documentation traceability policy passed: 14 decisions, 1 index and 1 split disposition\n'
