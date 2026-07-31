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
expected_dispositions=(STD-{0135..0178})
[[ "${dispositions[*]}" == "${expected_dispositions[*]}" ]]
[[ -e "$R/topics/architecture.md" ]]
for owner in topics/licensing.md profiles/languages/typescript.md profiles/applications/frontend.md topics/performance.md; do
  [[ ! -e "$R/$owner" ]]
done
for text in 'not one Core consolidation' '## Missing Owners' 'fixed layer diagrams' 'no normative or legacy standard'; do
  rg -F -q "$text" "$S/milestone-7-row-15-decomposition.md"
done
P="$R/plans/standards-library-effectiveness-restructure-plan.md"
rg -F -q '`7.4b8bb` (`Accepted`)' "$P"
rg -F -q '`7.4b8bc` (`Accepted`)' "$P"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-15 decomposition passed: 60 IDs across 15 children, 4 missing owners\n'
