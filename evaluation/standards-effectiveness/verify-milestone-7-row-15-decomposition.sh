#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
O="$S/milestone-7-execution-decomposition.tsv"
mapfile -t ids < <(awk -F '\t' '$1==15{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O" | sort)
expected=(STD-{0135..0194})
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==15{n++}END{print n+0}' "$O")" -eq 15 ]]
mapfile -t dispositions < <(
  awk -F '\t' '$1>="STD-0135"&&$1<="STD-0194"{print $1}' \
    "$S/consolidation-dispositions.tsv" | sort
)
expected_dispositions=(STD-{0135..0194})
[[ "${dispositions[*]}" == "${expected_dispositions[*]}" ]]
[[ -e "$R/topics/architecture.md" ]]
[[ -e "$R/topics/licensing.md" ]]
[[ -e "$R/profiles/languages/typescript.md" ]]
[[ -e "$R/profiles/applications/frontend.md" ]]
[[ -e "$R/topics/performance.md" ]]
for text in 'not one Core consolidation' '## Owner Closure' 'fixed layer diagrams' 'no normative or legacy standard'; do
  rg -F -q "$text" "$S/milestone-7-row-15-decomposition.md"
done
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-15 decomposition passed: 60 IDs across 15 children, no missing owners\n'
