#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-32-owner-validation.tsv";D="$S/milestone-7-row-32-decomposition.md";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
expected=(STD-{0106..0118});mapfile -t ids < <(awk -F '\t' '$1==32{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);[[ "${ids[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' '$1==32{n++}END{print n+0}' "$O")" -eq 3 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' 'NR>1&&($2!="profiles/boundaries/persistence.md"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]
for t in '## Owner Contract' 'does not own every in-memory mutation' '## Exact Ownership' '`32.1`' '`32.2`' '`32.3`' '## Typed Outcomes And No Fallback' '## Re-plan Triggers';do rg -F -q "$t" "$D";done
rg -F -q '`7.4b22a` (`Accepted`)' "$P";rg -F -q '`7.4b22b` (`Accepted`)' "$P";rg -F -q '`7.4b22c` (`Accepted`)' "$P";rg -F -q '`7.4b22d` (`Accepted`)' "$P";rg -F -q '`7.4b22dr` (`Accepted`)' "$P"
"$S/verify-persistence-owner-contract.sh"
rg -F -q $'STD-0106\tARCHITECTURE-PATTERNS.md\tprofiles/boundaries/persistence.md\tindex' "$S/consolidation-dispositions.tsv"
"$S/verify-persistence-durable-mutation.sh"
"$S/verify-persistence-migration-execution.sh"
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-32 decomposition passed: 13 IDs across 3 Persistence children\n'
