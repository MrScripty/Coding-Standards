#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-33-owner-validation.tsv";D="$S/milestone-7-row-33-decomposition.md";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
expected=(STD-{0126..0133});mapfile -t ids < <(awk -F '\t' '$1==33{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);[[ "${ids[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' '$1==33{n++}END{print n+0}' "$O")" -eq 2 ]]
[[ "$(awk -F '\t' '$1==33&&($5!="topics/contracts.md"||$6!="exists"||$7!="pre-slice-review"||$8!="focused"||$10!="none"||NF!=10){n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' 'NR>1&&($2!="topics/contracts.md"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]
for t in '## Owner Contract' 'sole normative owner for outcome meaning' 'IPC remains transport-independent' '## Exact Ownership' '`33.1`' '`33.2`' 'reference/recipes/http.md' '## Typed Outcomes And No Fallback' 'default an unknown failure to `500`' '## Re-plan Triggers';do rg -F -q "$t" "$D";done
[[ "$(awk -F '\t' '$1==33{print $6}' "$S/milestone-7-execution-train.tsv")" == topics/contracts.md ]]
rg -F -q '`7.4b23a` (`Accepted`)' "$P";rg -F -q '`7.4b23b` (`Planned`)' "$P";rg -F -q '`7.4b23c` (`Planned`)' "$P"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-33 decomposition passed: 8 IDs across 2 Contracts children\n'
