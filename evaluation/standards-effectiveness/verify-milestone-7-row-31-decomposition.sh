#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-31-owner-validation.tsv";D="$S/milestone-7-row-31-decomposition.md";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
expected=(STD-{0089..0092});mapfile -t ids < <(awk -F '\t' '$1==31{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==31{n++}END{print n+0}' "$O")" -eq 2 ]];[[ "$(awk -F '\t' '$1==31&&NF!=10{n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' 'NR>1&&($2!="topics/diagnostics.md"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]
for text in '## Owner Contract' 'Contracts owns typed outcome meaning' 'does not mandate logging' '## Exact Ownership' '`31.1`' '`31.2`' '## Typed Outcomes And No Fallback' '## Re-plan Triggers';do rg -F -q "$text" "$D";done
[[ "$(awk -F '\t' '$1==31{print $6}' "$S/milestone-7-execution-train.tsv")" == topics/diagnostics.md ]]
rg -F -q '`7.4b21a` (`Accepted`)' "$P";rg -F -q '`7.4b21b` (`Accepted`)' "$P";rg -F -q '`7.4b21c` (`Planned`)' "$P"
"$S/verify-diagnostics-owner-contract.sh"
printf 'Milestone 7 row-31 decomposition passed: 4 IDs across 2 Diagnostics children\n'
