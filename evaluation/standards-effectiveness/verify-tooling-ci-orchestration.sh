#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd "$S/../.." && pwd)"
while IFS=$'\t' read -r case_id facts dependencies capability reporting fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$facts" == contradictory ]]; then actual=typed-invalid
  elif [[ "$dependencies" == missing || "$reporting" == missing ]]; then actual=typed-unavailable
  elif [[ "$capability" == unsupported ]]; then actual=typed-unsupported
  else actual=allow; fi
  [[ "$actual" == "$expected" ]]
done < "$S/fixtures/tooling/ci-orchestration-decisions.tsv"
for text in '## CI Orchestration And Scheduling' 'required Verification claims' \
  'Do not default to GitHub Actions' 'typed `invalid`' 'typed `unavailable`' \
  'is `unsupported`'; do rg -F -q "$text" "$R/workflows/tooling.md"; done
awk -F '\t' '$1=="STD-0687"&&$3=="workflows/tooling.md"&&$4=="refine"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"
for id in STD-0689 STD-0690; do awk -F '\t' -v id="$id" '$1==id&&$3=="workflows/tooling.md"&&$4=="split"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"; done
rg -F -q '## CI Orchestration Examples' "$R/reference/recipes/tooling.md"
for legacy in 'strategy.fail-fast: false' 'Use three tiers:' './launcher.sh --ci-preflight'; do ! rg -F -q "$legacy" "$R/TOOLING-STANDARDS.md"; done
printf 'Tooling CI orchestration passed: 12 decisions, 1 direct and 2 split dispositions\n'
