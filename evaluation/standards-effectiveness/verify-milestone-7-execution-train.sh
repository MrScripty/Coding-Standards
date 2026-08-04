#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly MANIFEST="$SCRIPT_DIR/milestone-7-execution-train.tsv"
readonly DECOMPOSITION="$SCRIPT_DIR/milestone-7-execution-decomposition.tsv"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A disposed source_by_id owner_by_id remaining seen
declare -A overlay_lines overlay_orders_seen
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

overlay_row_count=0
while IFS=$'\t' read -r baseline_order child_order ids source owner owner_state \
  activation checkpoint rationale owner_transition extra; do
  if [[ "$baseline_order" == baseline_order ]]; then
    [[ "$child_order" == child_order && "$ids" == ids &&
       "$owner_transition" == owner_transition ]]
    continue
  fi
  [[ "$baseline_order" =~ ^[0-9]+$ ]]
  [[ "$child_order" =~ ^[0-9]+$ ]]
  [[ -n "$ids" && -n "$source" && -n "$owner" && -n "$rationale" ]]
  [[ "$owner_state" =~ ^(exists|missing)$ ]]
  [[ "$activation" =~ ^(pre-slice-review|owner-review|final-closure)$ ]]
  [[ "$checkpoint" =~ ^(focused|full-suite)$ ]]
  [[ "$owner_transition" =~ ^(none|missing-to-exists)$ ]]
  [[ -z "${extra:-}" ]]
  overlay_lines["$baseline_order"]+="$baseline_order"$'\t'"$child_order"$'\t'
  overlay_lines["$baseline_order"]+="$ids"$'\t'"$source"$'\t'"$owner"$'\t'
  overlay_lines["$baseline_order"]+="$owner_state"$'\t'"$activation"$'\t'
  overlay_lines["$baseline_order"]+="$checkpoint"$'\t'"$rationale"$'\t'
  overlay_lines["$baseline_order"]+="$owner_transition"$'\n'
  ((overlay_row_count += 1))
done < "$DECOMPOSITION"
[[ "$overlay_row_count" -gt 0 ]]

completed_cluster_count=0
completed_id_count=0
pending_cluster_count=0
logical_cluster_count=0
active_label=
active_required_ids=

process_cluster() {
  local label="$1"
  local ids_csv="$2"
  local required_ids="$3"
  local cluster_disposed=0
  local -a cluster_ids
  IFS=',' read -r -a cluster_ids <<< "$ids_csv"
  [[ "${#cluster_ids[@]}" -gt 0 ]]

  for id in "${cluster_ids[@]}"; do
    [[ "$id" =~ ^STD-[0-9]{4}$ ]]
    [[ -n "${source_by_id[$id]:-}" ]]
    [[ -n "${disposed[$id]:-}" ]] && ((cluster_disposed += 1))
  done

  if [[ "$cluster_disposed" -eq "${#cluster_ids[@]}" ]]; then
    [[ -z "$active_label" ]] || {
      printf 'execution-train cluster %s completed out of order\n' "$label" >&2
      exit 1
    }
    ((completed_cluster_count += 1))
    ((completed_id_count += ${#cluster_ids[@]}))
  elif [[ "$cluster_disposed" -eq 0 ]]; then
    if [[ -z "$active_label" ]]; then
      active_label="$label"
      active_required_ids="$required_ids"
    fi
    ((pending_cluster_count += 1))
  else
    printf 'execution-train cluster %s is partially disposed\n' "$label" >&2
    exit 1
  fi
  ((logical_cluster_count += 1))
}

expected_order=0
baseline_cluster_count=0
checkpoint_count=0
baseline_count=0
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

  [[ "$owner_state" != missing || "$activation" == owner-review ]]
  [[ "$activation" != final-closure || "$wave" == reference-index-closure ]]

  start_number=$((10#${start_id#STD-}))
  end_number=$((10#${end_id#STD-}))
  [[ "$start_number" -le "$end_number" ]]
  cluster_size=$((end_number - start_number + 1))
  baseline_ids_csv=
  declare -A baseline_ids=()
  for ((number = start_number; number <= end_number; number += 1)); do
    printf -v id 'STD-%04d' "$number"
    [[ -z "${seen[$id]:-}" ]]
    [[ "${source_by_id[$id]}" == "$source" ]]
    [[ "${owner_by_id[$id]}" == "$owner" ]]
    seen["$id"]=1
    baseline_ids["$id"]=1
    baseline_ids_csv+="${baseline_ids_csv:+,}$id"
  done

  if [[ -n "${overlay_lines[$order]:-}" ]]; then
    overlay_orders_seen["$order"]=1
    expected_child=0
    overlay_id_count=0
    owner_transition_count=0
    owner_transition_complete=0
    declare -A overlay_seen=()
    while IFS=$'\t' read -r overlay_order child_order ids overlay_source \
      overlay_owner overlay_owner_state overlay_activation overlay_checkpoint \
      rationale overlay_owner_transition overlay_extra; do
      [[ -z "$overlay_order" ]] && continue
      ((expected_child += 1))
      [[ "$overlay_order" -eq "$order" ]]
      [[ "$child_order" -eq "$expected_child" ]]
      [[ "$overlay_source" == "$source" ]]
      [[ "$overlay_activation" =~ ^(pre-slice-review|owner-review|final-closure)$ ]]
      [[ "$overlay_checkpoint" == focused ]]
      [[ "$overlay_owner_transition" =~ ^(none|missing-to-exists)$ ]]
      [[ -n "$rationale" && -z "${overlay_extra:-}" ]]
      [[ "$overlay_activation" != final-closure ||
          "$wave" == reference-index-closure ]]
      if [[ "$overlay_owner_transition" == missing-to-exists ]]; then
        ((owner_transition_count += 1))
        [[ "$owner_transition_count" -eq 1 ]]
        [[ "$owner_state" == missing && "$overlay_owner" == "$owner" ]]
        [[ "$overlay_owner_state" == exists ]]
        [[ "$overlay_activation" == pre-slice-review ]]
        transition_disposed=0
        IFS=',' read -r -a transition_ids <<< "$ids"
        for transition_id in "${transition_ids[@]}"; do
          [[ -n "${disposed[$transition_id]:-}" ]] && ((transition_disposed += 1))
        done
        [[ "$transition_disposed" -eq 0 ||
           "$transition_disposed" -eq "${#transition_ids[@]}" ]]
        [[ "$transition_disposed" -eq 0 ]] || owner_transition_complete=1
      elif [[ "$overlay_owner" != "$owner" ]]; then
        if [[ -e "$REPO_ROOT/$overlay_owner" ]]; then
          [[ "$overlay_owner_state" == exists ]]
        else
          [[ "$overlay_owner_state" == missing &&
             "$overlay_activation" == owner-review ]]
        fi
      fi

      IFS=',' read -r -a child_ids <<< "$ids"
      for child_id in "${child_ids[@]}"; do
        [[ -n "${baseline_ids[$child_id]:-}" ]]
        [[ -z "${overlay_seen[$child_id]:-}" ]]
        [[ "${source_by_id[$child_id]}" == "$source" ]]
        overlay_seen["$child_id"]=1
        ((overlay_id_count += 1))
      done
      process_cluster "$order.$child_order" "$ids" "$ids"
    done <<< "${overlay_lines[$order]}"
    [[ "$overlay_id_count" -eq "$cluster_size" ]]
    [[ "$owner_transition_count" -le 1 ]]
    effective_owner_state="$owner_state"
    [[ "$owner_transition_complete" -eq 0 ]] || effective_owner_state=exists
    if [[ -e "$REPO_ROOT/$owner" ]]; then
      [[ "$effective_owner_state" == exists ]]
    else
      [[ "$effective_owner_state" == missing ]]
    fi
  else
    if [[ -e "$REPO_ROOT/$owner" ]]; then
      [[ "$owner_state" == exists ]]
    else
      [[ "$owner_state" == missing ]]
    fi
    process_cluster "$order" "$baseline_ids_csv" "$start_id,$end_id"
  fi

  [[ "$checkpoint" == full-suite ]] && ((checkpoint_count += 1))
  ((baseline_count += cluster_size))
  ((baseline_cluster_count += 1))
done < "$MANIFEST"

for overlay_order in "${!overlay_lines[@]}"; do
  [[ -n "${overlay_orders_seen[$overlay_order]:-}" ]]
done
[[ "$baseline_cluster_count" -eq 47 ]]
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
next_slice_block="$(
  awk '
    /^\*\*Next slice:\*\*/ { capture = 1 }
    capture && /^$/ { exit }
    capture { print }
  ' "$PLAN"
)"
if [[ -n "$active_label" ]]; then
  IFS=',' read -r -a required_ids <<< "$active_required_ids"
  for required_id in "${required_ids[@]}"; do
    [[ "$next_slice_block" == *"$required_id"* ]]
  done
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
"$SCRIPT_DIR/verify-owner-state-transitions.sh"

printf 'Milestone 7 execution train passed: %s baseline IDs; %s completed and %s remaining across %s completed and %s pending logical clusters; active row %s\n' \
  "$baseline_count" "$completed_id_count" "$remaining_count" \
  "$completed_cluster_count" "$pending_cluster_count" \
  "${active_label:-complete}"
