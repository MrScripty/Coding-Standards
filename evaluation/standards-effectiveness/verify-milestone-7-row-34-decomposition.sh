#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-34-owner-validation.tsv";D="$S/milestone-7-row-34-decomposition.md";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
expected=(STD-{0449..0464});mapfile -t ids < <(awk -F '\t' '$1==34{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);[[ "${ids[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' '$1==34{n++}END{print n+0}' "$O")" -eq 6 ]]
[[ "$(awk -F '\t' '$1==34&&($6!="exists"||$7!="pre-slice-review"||$8!="focused"||$10!="none"||NF!=10){n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' 'NR>1&&NF!=4{n++}END{print n+0}' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR>1&&$1>="STD-0449"&&$1<="STD-0454"&&$2!="profiles/applications/frontend.md"{n++}END{print n+0}' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR>1&&$1>="STD-0455"&&$1<="STD-0456"&&$2!="profiles/languages/typescript.md"{n++}END{print n+0}' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR>1&&$1>="STD-0457"&&$1<="STD-0463"&&$2!="profiles/applications/frontend.md"{n++}END{print n+0}' "$V")" -eq 0 ]]
[[ "$(awk -F '\t' '$1=="STD-0464"{print $2}' "$V")" == topics/accessibility.md ]]
for t in '## Owner Contract' 'does not own domain state' '## Exact Ownership' '`34.1`' '`34.2`' '`34.3`' '`34.4`' '`34.5`' '`34.6`' 'Deleted selector, event, DOM-shim' '## Typed Outcomes And No Fallback' '## Re-plan Triggers';do rg -F -q "$t" "$D";done
[[ "$(awk -F '\t' '$1==34{print $6}' "$S/milestone-7-execution-train.tsv")" == profiles/applications/frontend.md ]]
for m in a b c;do needle="$(printf '`7.4b24%s` (`Accepted`)' "$m")";rg -F -q "$needle" "$P";done;for m in d e f g;do needle="$(printf '`7.4b24%s` (`Planned`)' "$m")";rg -F -q "$needle" "$P";done
"$S/verify-frontend-applicability.sh"
"$S/verify-frontend-rendering-synchronization.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-34 decomposition passed: 16 IDs across 6 owner-aligned children\n'
