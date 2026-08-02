#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="$(cd "$S/../.." && pwd)"
for id in STD-0693 STD-0694; do
  awk -F '\t' -v id="$id" '$1==id&&$3=="reference/recipes/tooling.md"&&$4=="move"{f=1}END{exit !f}' "$S/consolidation-dispositions.tsv"
done
for text in '## Complete CI Workflow Example' 'This is the complete legacy GitHub Actions example' \
  '# .github/workflows/ci.yml' 'actions/checkout@v4' 'ci_summary:' \
  'define no fallback'; do rg -F -q "$text" "$R/reference/recipes/tooling.md"; done
for text in '# .github/workflows/ci.yml' 'actions/checkout@v4' 'ci_summary:'; do
  ! rg -F -q "$text" "$R/TOOLING-STANDARDS.md"
done
rg -F -q 'defines no provider, trigger, permission, job, gate, cache, command' "$R/TOOLING-STANDARDS.md"
printf 'Tooling CI workflow reference passed: 2 exact move dispositions\n'
