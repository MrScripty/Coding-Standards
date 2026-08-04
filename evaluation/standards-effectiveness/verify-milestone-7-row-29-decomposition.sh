#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly O="$S/milestone-7-execution-decomposition.tsv"
readonly V="$S/milestone-7-row-29-owner-validation.tsv"
readonly D="$S/milestone-7-row-29-decomposition.md"
readonly P="$R/plans/standards-library-effectiveness-restructure-plan.md"

expected=(STD-{0046..0050})
mapfile -t ids < <(awk -F '\t' '$1==29{n=split($3,a,",");for(i=1;i<=n;i++)print a[i]}' "$O" | sort)
[[ "${ids[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' '$1==29{print $2}' "$O")" == 1 ]]
[[ "$(awk -F '\t' '$1==29&&NF!=10{n++}END{print n+0}' "$O")" -eq 0 ]]

mapfile -t validated < <(awk -F '\t' 'NR>1{print $1}' "$V")
[[ "${validated[*]}" == "${expected[*]}" ]]
[[ "$(awk -F '\t' 'NR>1&&($2!="topics/contracts.md"||$3!="index"||NF!=4){n++}END{print n+0}' "$V")" -eq 0 ]]

for text in \
  '## Owner Contract' \
  'sole normative owner' \
  'freeze coordinates concurrent work' \
  '## Exact Dispositions' \
  '`STD-0046` through `STD-0050`' \
  '`29.1`' \
  '## Decision Requirements' \
  'universal append-only evolution' \
  '## Re-plan Triggers'; do
  rg -F -q "$text" "$D"
done

[[ "$(awk -F '\t' '$1==29{print $6}' "$S/milestone-7-execution-train.tsv")" == 'topics/contracts.md' ]]
rg -F -q '`7.4b19a` (`Accepted`)' "$P"
rg -F -q '`7.4b19b` (`Accepted`)' "$P"
rg -F -q '`7.4b20a` (`Accepted`)' "$P"

mapfile -t disposed < <(awk -F '\t' '$1>="STD-0046"&&$1<="STD-0050"{print $1}' "$S/consolidation-dispositions.tsv")
[[ "${disposed[*]}" == "${expected[*]}" ]]
"$S/verify-contract-planning-boundary.sh"
"$S/verify-milestone-7-execution-train.sh"

printf 'Milestone 7 row-29 decomposition passed: 5 IDs assigned to one Contracts-owned index child\n'
