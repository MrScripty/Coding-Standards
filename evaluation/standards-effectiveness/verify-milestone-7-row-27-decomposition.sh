#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-27-owner-validation.tsv";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
mapfile -t ids < <(awk -F '\t' '$1==27{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);expected=(STD-{0888..0898});[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==27{print $2}' "$O")" == 1 ]];[[ "$(awk -F '\t' '$1==27&&NF!=9{n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' 'NR>1&&($2!="workflows/implementation.md"||$3!="index"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]
for t in '## Owner Contract' 'sole normative owner' 'optional derived projection' '## Exact Dispositions' '`STD-0888` through `STD-0898`' '`27.1`' '## Projection Requirements' 'checked boxes' '## Re-plan Triggers';do rg -F -q "$t" "$S/milestone-7-row-27-decomposition.md";done
[[ "$(awk -F '\t' '$1==27{print $6}' "$S/milestone-7-execution-train.tsv")" == 'workflows/implementation.md' ]]
rg -F -q '`7.4b17a` (`Accepted`)' "$P";rg -F -q '`7.4b17b` (`Planned`)' "$P"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-27 decomposition passed: 11 IDs assigned to one Implementation-owned child\n'
