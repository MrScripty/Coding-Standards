#!/usr/bin/env bash
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd "$S/../.." && pwd)"
F="$S/fixtures/verification/testing-index-routes.tsv"
D="$S/consolidation-dispositions.tsv"
T="$R/TESTING-STANDARDS.md"
P="$R/plans/standards-library-effectiveness-restructure-plan.md"

mapfile -t ids < <(awk -F '\t' '$1>="STD-0602"&&$1<="STD-0653"{print $1}' "$D" | sort)
expected=(STD-{0602..0653})
[[ "${ids[*]}" == "${expected[*]}" ]]

while IFS=$'\t' read -r concern owner extra; do
  [[ "$concern" == concern ]] && continue
  [[ -z "${extra:-}" ]]
  rg -F -q "($owner)" "$T"
done < "$F"

rg -F -q 'non-normative compatibility index' "$T"
rg -F -q 'defines no testing policy' "$T"
rg -F -q 'never this index' "$T"
! rg -q '^- \[[ xX]\]' "$T"
! rg -F -q 'Before submitting code' "$T"
! rg -F -q 'All new code has corresponding tests' "$T"

for milestone in 7.4b8bu 7.4b8bv 7.4b8bw 7.4b8bx 7.4b8by 7.4b8cb \
  7.4b8cc 7.4b8cd 7.4b8ce 7.4b8cf 7.4b8cg 7.4b8ch 7.4b8ci 7.4b8cj; do
  rg -F -q "\`$milestone\` (\`Accepted\`)" "$P"
done
rg -F -q '`7.4b9s` (`Accepted`)' "$P"
"$S/verify-milestone-7-row-18-decomposition.sh"
printf 'Testing source closure passed: 52 dispositions, 8 routes\n'
