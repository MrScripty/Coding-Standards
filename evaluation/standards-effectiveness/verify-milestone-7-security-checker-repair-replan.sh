#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly INVENTORY="$S/milestone-7-security-checker-repairs.tsv"
readonly REPLAN="$S/milestone-7-security-checker-repair-replan.md"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

readonly expected_header=$'package\tsequence\tscope\twritable_checker\tpreparation\tpreserved_evidence\tintegration_gate'
[[ "$(head -n 1 "$INVENTORY")" == "$expected_header" ]]

declare -A seen_packages=()
declare -A seen_checkers=()
row_count=0
serial_count=0
parallel_count=0

while IFS=$'\t' read -r package sequence scope checker preparation preserved \
  gate extra; do
  [[ "$package" == package ]] && continue
  [[ -z "${extra:-}" ]]
  [[ "$package" =~ ^7\.4c3hs(1|2[abc])$ ]]
  [[ "$sequence" =~ ^[12]$ ]]
  [[ "$scope" =~ ^(cross-source-ipc|security-input-validation|contracts-proof-lifetime|security-network-transport)$ ]]
  [[ "$checker" == evaluation/standards-effectiveness/verify-*.sh ]]
  [[ -f "$R/$checker" ]]
  [[ "$preparation" =~ ^(serial|parallel-local)$ ]]
  [[ "$preserved" == owner+routes+dispositions+typed-outcomes+negative-policy ]]
  [[ "$gate" == focused-then-group-suite ]]
  [[ -z "${seen_packages[$package]:-}" ]]
  [[ -z "${seen_checkers[$checker]:-}" ]]
  seen_packages["$package"]=1
  seen_checkers["$checker"]="$package"
  if [[ "$preparation" == serial ]]; then
    ((serial_count += 1))
  else
    ((parallel_count += 1))
  fi
  ((row_count += 1))
done < "$INVENTORY"

[[ "$row_count" -eq 4 ]]
[[ "$serial_count" -eq 1 ]]
[[ "$parallel_count" -eq 3 ]]
[[ "${seen_checkers[evaluation/standards-effectiveness/verify-ipc-payload-validation.sh]}" == 7.4c3hs1 ]]

required_replan=(
  '## Selected Design'
  'Each mutable checker has exactly one'
  '## Durable Evidence'
  '### Cross-source IPC'
  '### Input Validation'
  '### Validation-Proof Lifetime'
  '### Network Transport'
  'The three `hs2` packages may be prepared concurrently'
  'A prepared patch is not accepted evidence.'
  '## No Fallback'
  'one pure index'
  '## Ordered Execution'
)
for text in "${required_replan[@]}"; do
  rg -F -q "$text" "$REPLAN"
done

for package in 7.4c3hs 7.4c3hs1 7.4c3hs2a 7.4c3hs2b 7.4c3hs2c; do
  rg -F -q "\`$package\`" "$PLAN"
done

printf 'Security checker repair re-plan passed: %s exclusive packages, %s serial and %s parallel-local\n' \
  "$row_count" "$serial_count" "$parallel_count"
