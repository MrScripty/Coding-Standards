#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly INVENTORY="$S/milestone-7-source-package-preparation.tsv"
readonly MANIFEST="$S/milestone-7-final-source-closure.tsv"
readonly REPLAN="$S/milestone-7-source-index-verifier-replan.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"
readonly checker_subject_pattern='^checker:(evaluation/standards-effectiveness/verify-[A-Za-z0-9._-]+\.sh)$'
readonly suite_subject_pattern='^suite:(evaluation/standards-effectiveness/suites/[A-Za-z0-9._-]+\.toml)$'

readonly expected_header=$'package\tsource\tmanifest_order\tpreparation_wave\tchecker_class\twritable_verifiers\tpreserved_evidence\tintegration_rule'
[[ "$(head -n 1 "$INVENTORY")" == "$expected_header" ]]

declare -A seen_packages=()
declare -A seen_sources=()
declare -A seen_verifier_subjects=()
declare -A seen_verifier_paths=()
row_count=0
orders=()

while IFS=$'\t' read -r package source order wave checker_class verifiers \
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

  IFS=',' read -r -a verifier_list <<< "$verifiers"
  [[ "${#verifier_list[@]}" -gt 0 ]]
  for verifier_subject in "${verifier_list[@]}"; do
    if [[ "$verifier_subject" =~ $checker_subject_pattern ]]; then
      verifier_path="${BASH_REMATCH[1]}"
    elif [[ "$verifier_subject" =~ $suite_subject_pattern ]]; then
      verifier_path="${BASH_REMATCH[1]}"
    else
      printf 'invalid: unknown or untyped verifier subject: %s\n' \
        "$verifier_subject" >&2
      exit 1
    fi

    if [[ -L "$R/$verifier_path" ]]; then
      printf 'invalid: verifier subject path cannot be a symlink: %s\n' \
        "$verifier_subject" >&2
      exit 1
    fi
    if [[ ! -f "$R/$verifier_path" ]]; then
      printf 'unavailable: verifier subject path does not exist: %s\n' \
        "$verifier_subject" >&2
      exit 1
    fi
    if [[ -n "${seen_verifier_subjects[$verifier_subject]:-}" ]]; then
      printf 'invalid: duplicate verifier subject: %s\n' \
        "$verifier_subject" >&2
      exit 1
    fi
    if [[ -n "${seen_verifier_paths[$verifier_path]:-}" ]]; then
      printf 'invalid: duplicate verifier path: %s\n' "$verifier_path" >&2
      exit 1
    fi
    seen_verifier_subjects["$verifier_subject"]="$package"
    seen_verifier_paths["$verifier_path"]="$package"
  done

  orders+=("$order")
  ((row_count += 1))
done < "$INVENTORY"

[[ "$row_count" -eq 8 ]]
[[ "${orders[*]}" == '5 8 17 18 20 21 24 26' ]]
[[ "${#seen_verifier_subjects[@]}" -eq 9 ]]
[[ "${#seen_verifier_paths[@]}" -eq 9 ]]

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

printf 'Source-package preparation protocol passed: %s packages, %s exclusive verifier subjects\n' \
  "$row_count" "${#seen_verifier_subjects[@]}"
