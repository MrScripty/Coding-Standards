#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
mapfile -t ids < <(awk -F '\t' '$1==28{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);expected=(STD-{0007..0026});[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==28{print $2}' "$O"|paste -sd ' ' -)" == '1 2 3 4 5 6' ]];[[ "$(awk -F '\t' '$1==28&&NF!=9{n++}END{print n+0}' "$O")" -eq 0 ]]
for t in '## Owner Contract' 'modality' '## Exact Ownership' '## Ordered Children' '`28.1`' '`28.6`' '## No-Fallback Rule' '## Re-plan Triggers';do rg -F -q "$t" "$S/milestone-7-row-28-decomposition.md";done
rg -F -q '`7.4b18a` (`Accepted`)' "$P";rg -F -q '`7.4b18b` (`Planned`)' "$P"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-28 decomposition passed: 20 IDs across 6 ordered children\n'
