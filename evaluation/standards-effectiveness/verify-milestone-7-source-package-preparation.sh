#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly INVENTORY="$S/milestone-7-source-package-preparation.tsv"
readonly MANIFEST="$S/milestone-7-final-source-closure.tsv"
readonly REPLAN="$S/milestone-7-source-index-verifier-replan.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

readonly expected_header=$'package\tsource\tmanifest_order\tpreparation_wave\tchecker_class\twritable_checkers\tpreserved_evidence\tintegration_rule'
[[ "$(head -n 1 "$INVENTORY")" == "$expected_header" ]]

declare -A seen_packages=()
declare -A seen_sources=()
declare -A seen_checkers=()
row_count=0
orders=()

while IFS=$'\t' read -r package source order wave checker_class checkers \
  preserved integration extra; do
  [[ "$package" == package ]] && continue
  [[ -z "${extra:-}" ]]
  [[ "$package" == "7.4c3.$order" ]]
  [[ "$wave" == p1 ]]
  [[ "$checker_class" == mixed-policy ]]
  [[ "$preserved" == owner+routes+dispositions+typed-outcomes+negative-policy ]]
  [[ "$integration" == serial-manifest-order ]]
  [[ -z "${seen_packages[$package]:-}" ]]
  [[ -z "${seen_sources[$source]:-}" ]]
  seen_packages["$package"]=1
  seen_sources["$source"]=1

  manifest_source="$(awk -F '\t' -v order="$order" \
    'NR > 1 && $1 == order { print $2 }' "$MANIFEST")"
  [[ "$manifest_source" == "$source" ]]

  IFS=',' read -r -a checker_list <<< "$checkers"
  [[ "${#checker_list[@]}" -gt 0 ]]
  for checker in "${checker_list[@]}"; do
    [[ "$checker" == evaluation/standards-effectiveness/verify-*.sh ]]
    [[ -f "$R/$checker" ]]
    [[ -z "${seen_checkers[$checker]:-}" ]]
    seen_checkers["$checker"]="$package"
  done

  orders+=("$order")
  ((row_count += 1))
done < "$INVENTORY"

[[ "$row_count" -eq 8 ]]
[[ "${orders[*]}" == '5 8 17 18 20 21 24 26' ]]
[[ "${#seen_checkers[@]}" -eq 9 ]]

required_replan=(
  '## Concurrent Preparation And Serial Acceptance'
  'Preparation order and acceptance order are separate contracts.'
  'Workers cannot edit shared acceptance state.'
  'A prepared package is not accepted evidence.'
  'one complete-suite run may accept'
  'non-overlapping former'
  'Architecture remains excluded from preparation wave `p1`'
)
for text in "${required_replan[@]}"; do
  rg -F -q "$text" "$REPLAN"
done

rg -F -q '`7.4c3p` (`Accepted`)' "$PLAN"
rg -F -q 'milestone-7-source-package-preparation.tsv' "$PLAN"

printf 'Source-package preparation protocol passed: %s packages, %s exclusive checkers\n' \
  "$row_count" "${#seen_checkers[@]}"
