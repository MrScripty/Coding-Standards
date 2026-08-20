#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv"
mapfile -t ids < <(awk -F '\t' '$1==28{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);expected=(STD-{0007..0026});[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==28{print $2}' "$O"|paste -sd ' ' -)" == '1 2 3 4 5 6' ]];[[ "$(awk -F '\t' '$1==28&&NF!=10{n++}END{print n+0}' "$O")" -eq 0 ]]
[[ "$(awk -F '\t' '$1==28&&$10=="missing-to-exists"{print $2}' "$O")" == 1 ]]
for t in '## Owner Contract' 'modality' '## Exact Ownership' '## Ordered Children' '`28.1`' '`28.6`' '## No-Fallback Rule' '## Re-plan Triggers';do rg -F -q "$t" "$S/milestone-7-row-28-decomposition.md";done
[[ "$(awk -F '\t' '$1==28&&$6!="exists"{n++}END{print n+0}' "$O")" -eq 0 ]]
[[ "$(awk -F '\t' '$1==28&&$2==1{print $7}' "$O")" == owner-review ]]
[[ "$(awk -F '\t' '$1==28&&$2>1&&$7!="pre-slice-review"{n++}END{print n+0}' "$O")" -eq 0 ]]
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-28 decomposition passed: 20 IDs across 6 ordered children\n'
