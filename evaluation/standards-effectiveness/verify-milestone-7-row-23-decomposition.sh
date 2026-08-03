#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)";R="$(cd -- "$S/../.." && pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-23-owner-validation.tsv";P="$R/plans/standards-library-effectiveness-restructure-plan.md";D="$S/consolidation-dispositions.tsv"
mapfile -t ids < <(awk -F '\t' '$1==23{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);expected=(STD-{0831..0842});[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==23{print $2}' "$O"|paste -sd ' ' -)" == '1 2 3 4 5 6 7 8 9 10 11' ]]
[[ "$(awk -F '\t' '$1==23&&NF!=9{n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR>1&&NF!=4{n++}END{print n+0}' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' '$3=="index"{n++}END{print n+0}' "$V")" -eq 1 ]];[[ "$(awk -F '\t' '$3=="split"{n++}END{print n+0}' "$V")" -eq 10 ]];[[ "$(awk -F '\t' '$3=="refine"{n++}END{print n+0}' "$V")" -eq 1 ]]
for t in '## Owner Contract' 'narrow Rust and Cargo tooling' 'does not own claim selection' '## Exact Dispositions' '`STD-0839` refines' '`STD-0842` splits' '## Ordered Children' '## Re-plan Triggers';do rg -F -q "$t" "$S/milestone-7-row-23-decomposition.md";done
rg -F -q '`7.4b13a` (`Accepted`)' "$P";rg -F -q '`7.4b13b` (`Accepted`)' "$P";rg -F -q '`7.4b13c` (`Accepted`)' "$P";rg -F -q '`7.4b13d` (`Planned`)' "$P"
next="$(awk '/^\*\*Next slice:\*\*/{c=1}c&&/^$/{exit}c{print}' "$P")";[[ "$next" == *'row 23 child 23.3'* && "$next" == *'STD-0833'* ]]
[[ -e "$R/profiles/languages/rust/tooling.md" ]];mapfile -t disposed < <(awk -F '\t' '$1>="STD-0831"&&$1<="STD-0842"{print $1}' "$D");[[ "${disposed[*]}" == 'STD-0831 STD-0832' ]]
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-23 decomposition passed: 12 IDs across 11 children, zero premature dispositions\n'
