#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
M="$S/milestone-7-row-35-readme-consumers.tsv"
D="$S/milestone-7-row-35-readme-dependencies.tsv"

mapfile -t expected < <(awk -F '\t' 'NR > 1 { print $1 }' "$M" | sort)
mapfile -t observed < <(
  rg -l 'README\.md' "$S"/verify-*.sh |
    sed "s#^$R/##" |
    sort
)
[[ "${observed[*]}" == "${expected[*]}" ]] || {
  printf 'README consumer inventory is incomplete\n' >&2
  diff -u <(printf '%s\n' "${expected[@]}") <(printf '%s\n' "${observed[@]}") >&2
  exit 1
}

[[ "$(awk -F '\t' 'NR > 1 { n++ } END { print n+0 }' "$M")" -eq 31 ]]
[[ "$(awk -F '\t' 'NR > 1 && NF != 3 { n++ } END { print n+0 }' "$M")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && $2 !~ /^(none|negative-purity|root-authority-verifier|root-closure-verifier|consumer-audit-infrastructure)$/ { n++ } END { print n+0 }' "$M")" -eq 0 ]]
[[ "$(awk -F '\t' 'NR > 1 && $3 !~ /^(none|fixture-data|language-index-closure|legacy-heading-pattern|rust-profile-index)$/ { n++ } END { print n+0 }' "$M")" -eq 0 ]]
[[ "$(awk -F '\t' '$2 == "root-authority-verifier" { print $1 }' "$M")" == \
  evaluation/standards-effectiveness/verify-root-router-evidence.sh ]]
[[ "$(awk -F '\t' '$2 == "root-closure-verifier" { print $1 }' "$M")" == \
  evaluation/standards-effectiveness/verify-root-index-closure.sh ]]
[[ "$(awk -F '\t' '$2 == "consumer-audit-infrastructure" { print $1 }' "$M")" == \
  evaluation/standards-effectiveness/verify-root-readme-consumer-audit.sh ]]
[[ "$(awk -F '\t' '$3 == "language-index-closure" { print $1 }' "$M")" == \
  evaluation/standards-effectiveness/verify-language-index-closure.sh ]]
[[ "$(awk -F '\t' '$2 == "negative-purity" { print $1 }' "$M" | sort | paste -sd ' ' -)" == \
  'evaluation/standards-effectiveness/verify-s1-routing.sh' ]]

! rg -F -q '"README.md"' "$S/verify-commit-authority.sh"
awk -F '\t' '$1 == "evaluation/standards-effectiveness/verify-commit-authority.sh" && $2 == "computed-root-readme-route-assertion" { found = 1 } END { exit !found }' "$D"
rg -F -q 'workflows/commit.md' "$R/STANDARDS-ROUTER.md"
rg -F -q 'topics/contracts.md' "$R/STANDARDS-ROUTER.md"
! rg -F -q '(workflows/commit.md)' "$R/README.md"
! rg -F -q '(topics/contracts.md)' "$R/README.md"

printf 'Root README consumer audit passed: 31 classified verifier consumers, no positive route consumers\n'
