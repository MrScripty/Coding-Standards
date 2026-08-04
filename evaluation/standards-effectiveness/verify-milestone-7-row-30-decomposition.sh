#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-30-owner-validation.tsv";D="$S/milestone-7-row-30-decomposition.md";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
expected=(STD-{0055..0062})
mapfile -t ids < <(awk -F '\t' '$1==30{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==30{n++}END{print n+0}' "$O")" -eq 2 ]];[[ "$(awk -F '\t' '$1==30&&NF!=10{n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR>1&&($2!="topics/contracts.md"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR>1&&$3=="refine"{n++}END{print n+0}' "$V")" -eq 5 ]];[[ "$(awk -F '\t' 'NR>1&&$3=="index"{n++}END{print n+0}' "$V")" -eq 3 ]]
for text in '## Owner Contract' 'sole normative owner' '## Exact Ownership' '`STD-0055` and `STD-0056`' '`30.1`' '`30.2`' '## Typed Outcomes And No Fallback' '## Re-plan Triggers';do rg -F -q "$text" "$D";done
[[ "$(awk -F '\t' '$1==30{print $6}' "$S/milestone-7-execution-train.tsv")" == topics/contracts.md ]]
rg -F -q '`7.4b20a` (`Accepted`)' "$P";rg -F -q '`7.4b20b` (`Accepted`)' "$P";rg -F -q '`7.4b20c` (`Planned`)' "$P"
mapfile -t disposed < <(awk -F '\t' '$1>="STD-0055"&&$1<="STD-0057"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "STD-0055 STD-0056 STD-0057" ]]
"$S/verify-contract-artifact-selection.sh"
printf 'Milestone 7 row-30 decomposition passed: 8 IDs across 2 Contracts-owned children\n'
