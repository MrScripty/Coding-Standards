#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";O="$S/milestone-7-execution-decomposition.tsv";V="$S/milestone-7-row-25-owner-validation.tsv";P="$R/plans/standards-library-effectiveness-restructure-plan.md"
mapfile -t ids < <(awk -F '\t' '$1==25{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O"|sort);expected=(STD-{0852..0858});[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==25{print $2}' "$O"|paste -sd ' ' -)" == 1 ]];[[ "$(awk -F '\t' '$1==25&&NF!=9{n++}END{print n+0}' "$O")" -eq 0 ]]
mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V");[[ "${validated[*]}" == "${expected[*]}" ]];[[ "$(awk -F '\t' 'NR>1&&($2!="workflows/implementation.md"||$3!="index"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]
for t in '## Owner Contract' 'identifier lineage' '## Exact Dispositions' '`STD-0852` through `STD-0858`' '## Ordered Children' '`25.1a`' '`25.1b`' '## Child 25.1 Plan Identity Replan' 'Security owns path' 'Cross-Platform applies conditionally' '## Child 25.1 Lifecycle Admission Replan' '`start` accepts only `Planned`' '`continue` accepts only `Active`' '`verify` accepts `Implemented` or `Verifying`' '## Child 25.1 Concurrent Admission Replan' 'explicit expected revision' 'Concurrency owns stale-read' 'serial integration owner alone' 'Do not retry the old operation automatically' 'lock files, leases, scheduler infrastructure' '## Re-plan Triggers';do rg -F -q "$t" "$S/milestone-7-row-25-decomposition.md";done
rg -F -q '`7.4b15a` (`Accepted`)' "$P";rg -F -q '`7.4b15b` (`Accepted`)' "$P";rg -F -q '`7.4b15c` (`Planned`)' "$P"
next="$(awk '/^\*\*Next slice:\*\*/{c=1}c&&/^$/{exit}c{print}' "$P")";[[ "$next" == *'row 25 child 25.1a'* && "$next" == *'plan identity'* ]]
"$S/verify-milestone-7-execution-train.sh"
printf 'Milestone 7 row-25 decomposition passed: 7 snapshot IDs assigned to one Implementation-owned child\n'
