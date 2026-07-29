#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly GROUP_FILE="$SCRIPT_DIR/milestone-7-trust-lifecycle-groups.tsv"
readonly NEXT_SLICE="$SCRIPT_DIR/milestone-7-trust-lifecycle-next-slice.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-trust-lifecycle-replan.md"
readonly PARENT="$SCRIPT_DIR/milestone-7-decomposition.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A disposed
declare -A disposed_source
declare -A disposed_target
declare -A disposed_disposition
declare -A remaining_by_owner
declare -A source_by_id
declare -A owner_by_id

while IFS=$'\t' read -r id source target disposition _rationale; do
  [[ "$id" == 'id' ]] && continue
  disposed["$id"]=1
  disposed_source["$id"]="$source"
  disposed_target["$id"]="$target"
  disposed_disposition["$id"]="$disposition"
done < "$DISPOSITIONS"

while IFS=$'\t' read -r id source _line owner _disposition _heading; do
  [[ "$id" == 'id' ]] && continue
  source_by_id["$id"]="$source"
  owner_by_id["$id"]="$owner"
  [[ -n "${disposed[$id]:-}" ]] && continue
  remaining_by_owner["$owner"]=$(( ${remaining_by_owner[$owner]:-0} + 1 ))
done < "$OWNER_MAP"

expected_ids=(
  STD-0263 STD-0264 STD-0265 STD-0266 STD-0267
  STD-0268 STD-0270 STD-0271 STD-0272
)
next_dispositions=0
for id in "${expected_ids[@]}"; do
  [[ -n "${disposed[$id]:-}" ]] && ((next_dispositions += 1))
done
[[ "$next_dispositions" -eq 0 || "$next_dispositions" -eq 9 ]]

rust_async_ids=(
  STD-0717 STD-0718 STD-0719 STD-0720 STD-0721
  STD-0722 STD-0723 STD-0724 STD-0725
)
rust_async_dispositions=0
for id in "${rust_async_ids[@]}"; do
  [[ -n "${disposed[$id]:-}" ]] && ((rust_async_dispositions += 1))
done
[[ "$rust_async_dispositions" =~ ^(0|2|5|7|9)$ ]]

expected_groups=(
  $'lifecycle-bridge\t1\ttopics/concurrency.md\t17\tmissing\tnone\tnext'
  $'lifecycle-bridge\t2\tprofiles/languages/rust/async.md\t9\tmissing\ttopics/concurrency.md\tbridge-prerequisite'
  $'trust-boundaries\t1\ttopics/security.md\t12\texists\tnone\tindependent-audit'
  $'trust-boundaries\t2\ttopics/cross-platform.md\t15\texists\tnone\tindependent-audit'
  $'trust-boundaries\t3\tprofiles/boundaries/interop.md\t10\texists\ttopics/contracts.md\tindependent-audit'
  $'trust-boundaries\t4\tprofiles/languages/rust/cross-platform.md\t5\tmissing\ttopics/cross-platform.md\tdependent-audit'
  $'trust-boundaries\t5\tprofiles/languages/rust/interop.md\t1\texists\tprofiles/boundaries/interop.md\tdependent-audit'
  $'trust-boundaries\t6\tprofiles/languages/rust/security.md\t5\texists\ttopics/security.md,profiles/languages/rust/async.md\tdependent-audit'
  $'trust-boundaries\t7\tprofiles/languages/rust/language-bindings.md\t42\texists\tprofiles/languages/rust/async.md\tdependent-audit'
)
mapfile -t actual_groups < <(tail -n +2 "$GROUP_FILE")
[[ "${actual_groups[*]}" == "${expected_groups[*]}" ]]

trust_total=0
bridge_total=0
while IFS=$'\t' read -r wave order owner count owner_state prerequisite status extra; do
  [[ "$wave" == 'wave' ]] && continue
  [[ "$order" =~ ^[0-9]+$ && "$count" =~ ^[0-9]+$ ]]
  expected_count="$count"
  expected_state="$owner_state"
  if [[ "$owner" == 'topics/concurrency.md' &&
        "$next_dispositions" -eq 9 ]]; then
    expected_count=8
    expected_state='exists'
  fi
  if [[ "$owner" == 'profiles/languages/rust/async.md' ]]; then
    expected_count=$((9 - rust_async_dispositions))
    if [[ "$rust_async_dispositions" -eq 0 ]]; then
      expected_state='missing'
    else
      expected_state='exists'
    fi
  fi
  [[ "${remaining_by_owner[$owner]:-0}" -eq "$expected_count" ]]
  if [[ -e "$REPO_ROOT/$owner" ]]; then
    actual_state='exists'
  else
    actual_state='missing'
  fi
  [[ "$actual_state" == "$expected_state" ]]
  [[ -n "$prerequisite" && -n "$status" && -z "${extra:-}" ]]
  if [[ "$wave" == 'trust-boundaries' ]]; then
    ((trust_total += count))
  else
    [[ "$wave" == 'lifecycle-bridge' ]]
    ((bridge_total += count))
  fi
done < "$GROUP_FILE"
[[ "$trust_total" -eq 90 && "$bridge_total" -eq 26 ]]

mapfile -t actual_ids < <(tail -n +2 "$NEXT_SLICE" | cut -f3)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r slice order id source target disposition rationale extra; do
  [[ "$slice" == 'slice' ]] && continue
  [[ "$slice" == '7.4b4b' && "$order" =~ ^[0-9]+$ ]]
  [[ "${source_by_id[$id]}" == "$source" ]]
  [[ "${owner_by_id[$id]}" == "$target" ]]
  [[ "$source" == 'CONCURRENCY-STANDARDS.md' ]]
  [[ "$target" == 'topics/concurrency.md' ]]
  [[ "$disposition" =~ ^(move|refine)$ ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  if [[ -n "${disposed[$id]:-}" ]]; then
    [[ "${disposed_source[$id]}" == "$source" ]]
    [[ "${disposed_target[$id]}" == "$target" ]]
    [[ "${disposed_disposition[$id]}" == "$disposition" ]]
  fi
done < "$NEXT_SLICE"

required_report=(
  '641 undisposed frozen identifiers'
  '90 trust-boundary identifiers'
  'F025'
  'F026'
  'Establish generic concurrency ownership before the Rust async'
  'shutdown canonical in the Rust language-binding profile'
  'Only'
  '`7.4b4d` is now implementation-ready'
  'No normative standard, final disposition'
  '## Accepted Slice 7.4b4b: Generic Concurrency Contract'
  '## Accepted Slice 7.4b4c: Rust Async Decomposition'
  'callbacks and other externally controlled code do not execute while the'
  '**No fallback:**'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '(milestone-7-trust-lifecycle-replan.md)' "$PARENT"
rg -F -q '| F044 | Resolved in Milestone 7.4b4a |' "$FINDINGS"
rg -F -q '`7.4b4a` (`Accepted`)' "$PLAN"
rg -F -q '`7.4c` (`Planned`)' "$PLAN"
if [[ "$next_dispositions" -eq 0 ]]; then
  rg -F -q '**Next slice:** Milestone 7.4b4b' "$PLAN"
  rg -F -q '`7.4b4b` (`Planned`)' "$PLAN"
else
  rg -F -q '`7.4b4b` (`Accepted`)' "$PLAN"
  rg -F -q '`7.4b4c` (`Accepted`)' "$PLAN"
  rg -F -q 'milestone-7-rust-async-decomposition.md' "$PLAN"
fi

"$SCRIPT_DIR/verify-milestone-7-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-rust-async-decomposition.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 trust/lifecycle re-plan passed: %s trust IDs, %s bridge IDs, generic dispositions %s/9, Rust Async dispositions %s/9\n' \
  "$trust_total" "$bridge_total" "$next_dispositions" "$rust_async_dispositions"
