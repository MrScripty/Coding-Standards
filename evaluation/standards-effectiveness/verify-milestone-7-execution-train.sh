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

expected_order=0
cluster_count=0
checkpoint_count=0
baseline_count=0
completed_cluster_count=0
completed_id_count=0
pending_cluster_count=0
active_order=
active_start=
active_end=
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
  cluster_size=$((end_number - start_number + 1))
  cluster_disposed=0
  for ((number = start_number; number <= end_number; number += 1)); do
    printf -v id 'STD-%04d' "$number"
    [[ -z "${seen[$id]:-}" ]]
    [[ "${source_by_id[$id]}" == "$source" ]]
    [[ "${owner_by_id[$id]}" == "$owner" ]]
    seen["$id"]=1
    [[ -n "${disposed[$id]:-}" ]] && ((cluster_disposed += 1))
  done

  if [[ "$cluster_disposed" -eq "$cluster_size" ]]; then
    [[ -z "$active_order" ]]
    ((completed_cluster_count += 1))
    ((completed_id_count += cluster_size))
  elif [[ "$cluster_disposed" -eq 0 ]]; then
    if [[ -z "$active_order" ]]; then
      active_order="$order"
      active_start="$start_id"
      active_end="$end_id"
    fi
    ((pending_cluster_count += 1))
  else
    printf 'execution-train cluster %s is partially disposed\n' "$order" >&2
    exit 1
  fi

  [[ "$checkpoint" == full-suite ]] && ((checkpoint_count += 1))
  ((baseline_count += cluster_size))
  ((cluster_count += 1))
done < "$MANIFEST"

[[ "$cluster_count" -eq 47 ]]
[[ "$checkpoint_count" -eq 5 ]]
[[ "$baseline_count" -eq 589 ]]
[[ "${#seen[@]}" -eq "$baseline_count" ]]
[[ "$remaining_count" -eq $((baseline_count - completed_id_count)) ]]
for id in "${!remaining[@]}"; do
  [[ -n "${seen[$id]:-}" ]]
done

rg -F -q '`7.4b7n` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7o` (`Accepted`)' "$PLAN"
next_slice_line="$(rg '^\*\*Next slice:\*\*' "$PLAN" | head -n 1)"
if [[ -n "$active_order" ]]; then
  [[ "$next_slice_line" == *"$active_start"* ]]
  [[ "$next_slice_line" == *"$active_end"* ]]
  next_milestone="$(
    sed -E 's/.*Milestone ([^ ]+).*/\1/' <<< "$next_slice_line"
  )"
  [[ "$next_milestone" != "$next_slice_line" ]]
  rg -F -q "\`$next_milestone\` (\`Planned\`)" "$PLAN"
else
  [[ "$next_slice_line" == *'Milestone 7.4c'* ]]
  rg -F -q '`7.4c` (`Planned`)' "$PLAN"
fi
"$SCRIPT_DIR/verify-milestone-7-decomposition.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 execution train passed: %s baseline IDs; %s completed and %s remaining across %s completed and %s pending clusters; active row %s\n' \
  "$baseline_count" "$completed_id_count" "$remaining_count" \
  "$completed_cluster_count" "$pending_cluster_count" "${active_order:-complete}"
