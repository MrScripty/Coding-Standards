#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly MANIFEST="$SCRIPT_DIR/milestone-7-execution-train.tsv"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A disposed source_by_id owner_by_id remaining seen
while IFS=$'\t' read -r id _rest; do
  [[ "$id" == id ]] && continue
  disposed["$id"]=1
done < "$DISPOSITIONS"

remaining_count=0
while IFS=$'\t' read -r id source _line owner _disposition _heading; do
  [[ "$id" == id ]] && continue
  source_by_id["$id"]="$source"
  owner_by_id["$id"]="$owner"
  if [[ -z "${disposed[$id]:-}" ]]; then
    remaining["$id"]=1
    ((remaining_count += 1))
  fi
done < "$OWNER_MAP"
[[ "$remaining_count" -eq 589 ]]

expected_order=0
cluster_count=0
checkpoint_count=0
while IFS=$'\t' read -r order wave start_id end_id source owner owner_state \
  activation checkpoint extra; do
  [[ "$order" == order ]] && continue
  ((expected_order += 1))
  [[ "$order" -eq "$expected_order" ]]
  [[ "$wave" =~ ^(trust-boundaries|lifecycle-runtime|process-dependencies|application-boundaries|reference-index-closure)$ ]]
  [[ "$start_id" =~ ^STD-[0-9]{4}$ && "$end_id" =~ ^STD-[0-9]{4}$ ]]
  [[ "$activation" =~ ^(pre-slice-review|owner-review|final-closure)$ ]]
  [[ "$checkpoint" =~ ^(focused|full-suite)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ -e "$REPO_ROOT/$owner" ]]; then
    [[ "$owner_state" == exists ]]
  else
    [[ "$owner_state" == missing && "$activation" == owner-review ]]
  fi
  [[ "$activation" != final-closure || "$wave" == reference-index-closure ]]

  start_number=$((10#${start_id#STD-}))
  end_number=$((10#${end_id#STD-}))
  [[ "$start_number" -le "$end_number" ]]
  for ((number = start_number; number <= end_number; number += 1)); do
    printf -v id 'STD-%04d' "$number"
    [[ -n "${remaining[$id]:-}" ]]
    [[ -z "${seen[$id]:-}" ]]
    [[ "${source_by_id[$id]}" == "$source" ]]
    [[ "${owner_by_id[$id]}" == "$owner" ]]
    seen["$id"]=1
  done

  [[ "$checkpoint" == full-suite ]] && ((checkpoint_count += 1))
  ((cluster_count += 1))
done < "$MANIFEST"

[[ "$cluster_count" -eq 47 ]]
[[ "$checkpoint_count" -eq 5 ]]
[[ "${#seen[@]}" -eq "$remaining_count" ]]
for id in "${!remaining[@]}"; do
  [[ -n "${seen[$id]:-}" ]]
done

rg -F -q '`7.4b7n` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8a` (`Planned`)' "$PLAN"
rg -F -q '**Next slice:** Milestone 7.4b8a' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-decomposition.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 execution train passed: %s IDs across %s clusters and %s full-suite checkpoints\n' \
  "$remaining_count" "$cluster_count" "$checkpoint_count"
