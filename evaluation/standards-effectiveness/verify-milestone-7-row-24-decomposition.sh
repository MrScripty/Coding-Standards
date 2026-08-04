#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)";R="$(cd -- "$S/../.." && pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-24-owner-validation.tsv";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
mapfile -t ids < <(awk -F '\t' '$1==24{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);expected=(STD-{0849..0851});[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==24{print $2}' "$O"|paste -sd ' ' -)" == '1' ]]
[[ "$(awk -F '\t' '$1==24&&NF!=9{n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR>1&&($2!="workflows/planning.md"||$3!="index"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]
for t in '## Owner Contract' 'sole normative owner' '## Exact Dispositions' '`STD-0849`, `STD-0850`, and `STD-0851`' '## Ordered Children' '`24.1`' '## Re-plan Triggers';do rg -F -q "$t" "$S/milestone-7-row-24-decomposition.md";done
[[ "$(awk -F '\t' '$1=="prompts/full-codebase-standards-refactor.md"{print $2"\t"$3}' "$S/owner-map.tsv")" == $'workflows/planning.md\treplace-with-derived-entrypoint' ]]
[[ "$(awk -F '\t' '$1==24{print $6}' "$S/milestone-7-execution-train.tsv")" == 'workflows/planning.md' ]]
rg -F -q '`7.4b14a` (`Accepted`)' "$P";rg -F -q '`7.4b14b` (`Accepted`)' "$P"
mapfile -t disposed < <(awk -F '\t' '$1>="STD-0849"&&$1<="STD-0851"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == 'STD-0849 STD-0850 STD-0851' ]]
"$S/verify-full-review-prompt-entrypoint.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-24 decomposition passed: 3 IDs assigned to one Planning-owned child\n'
