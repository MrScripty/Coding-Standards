#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-26-owner-validation.tsv";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
mapfile -t ids < <(awk -F '\t' '$1==26{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);expected=(STD-{0859..0887});[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==26{print $2}' "$O")" == 1 ]];[[ "$(awk -F '\t' '$1==26&&NF!=9{n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' 'NR>1&&($2!="workflows/planning.md"||$3!="index"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]
for t in '## Owner Contract' 'sole normative owner' 'derived' '## Exact Dispositions' '`STD-0859` through `STD-0887`' '## Ordered Children' '`26.1`' '## Projection Requirements' 'fixed milestone counts' '## Re-plan Triggers';do rg -F -q "$t" "$S/milestone-7-row-26-decomposition.md";done
[[ "$(awk -F '\t' '$1==26{print $6}' "$S/milestone-7-execution-train.tsv")" == 'workflows/planning.md' ]]
[[ "$(awk -F '\t' '$1==26{print $5}' "$S/milestone-7-execution-train.tsv")" == 'templates/PLAN-TEMPLATE.md' ]]
rg -F -q '`7.4b16a` (`Accepted`)' "$P";rg -F -q '`7.4b16b` (`Planned`)' "$P"
next="$(awk '/^\*\*Next slice:\*\*/{c=1}c&&/^$/{exit}c{print}' "$P")";[[ "$next" == *'Milestone 7.4b16b'* && "$next" == *'STD-0859'* && "$next" == *'STD-0887'* ]]
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-26 decomposition passed: 29 IDs assigned to one Planning-owned child\n'
