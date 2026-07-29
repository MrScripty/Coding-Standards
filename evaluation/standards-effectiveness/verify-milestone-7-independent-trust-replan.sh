#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly GROUP_FILE="$SCRIPT_DIR/milestone-7-independent-trust-groups.tsv"
readonly NEXT_SLICE="$SCRIPT_DIR/milestone-7-independent-trust-next-slice.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-independent-trust-replan.md"
readonly PARENT="$SCRIPT_DIR/milestone-7-decomposition.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

declare -A disposed
declare -A disposed_source
declare -A disposed_target
declare -A disposed_disposition
declare -A remaining_by_owner
declare -A remaining_sources
declare -A remaining_owners
declare -A source_by_id
declare -A owner_by_id
declare -a f048_actual_ids

while IFS=$'\t' read -r id source target disposition _rationale; do
  [[ "$id" == 'id' ]] && continue
  disposed["$id"]=1
  disposed_source["$id"]="$source"
  disposed_target["$id"]="$target"
  disposed_disposition["$id"]="$disposition"
done < "$DISPOSITIONS"

expected_ids=(STD-0473)
next_dispositions=0
for id in "${expected_ids[@]}"; do
  [[ -n "${disposed[$id]:-}" ]] && ((next_dispositions += 1))
done
[[ "$next_dispositions" -eq 0 || "$next_dispositions" -eq 1 ]]

global_remaining=0
while IFS=$'\t' read -r id source _line owner _disposition _heading; do
  [[ "$id" == 'id' ]] && continue
  source_by_id["$id"]="$source"
  owner_by_id["$id"]="$owner"
  [[ -n "${disposed[$id]:-}" ]] && continue
  ((global_remaining += 1))
  remaining_sources["$source"]=1
  remaining_owners["$owner"]=1
  remaining_by_owner["$owner"]=$(( ${remaining_by_owner[$owner]:-0} + 1 ))
  case "$owner" in
    topics/security.md|topics/cross-platform.md|profiles/boundaries/interop.md|\
profiles/languages/rust/interop.md|profiles/languages/rust/security.md|\
profiles/languages/rust/language-bindings.md)
      f048_actual_ids+=("$id")
      ;;
  esac
done < "$OWNER_MAP"
[[ "$global_remaining" -eq $((594 - next_dispositions)) ]]
[[ "${#remaining_sources[@]}" -eq 29 ]]
[[ "${#remaining_owners[@]}" -eq 28 ]]

missing_owners=0
for owner in "${!remaining_owners[@]}"; do
  [[ -e "$REPO_ROOT/$owner" ]] || ((missing_owners += 1))
done
[[ "$missing_owners" -eq 13 ]]

f048_baseline_ids=(
  STD-{0294..0299}
  STD-{0473..0482}
  STD-0582 STD-0583 STD-{0588..0591} STD-0601
  STD-0757 STD-0758 STD-{0761..0771} STD-{0776..0780}
  STD-{0782..0789} STD-0792 STD-0793 STD-0797 STD-{0804..0809}
  STD-0821 STD-0824 STD-0826
)
[[ "${#f048_baseline_ids[@]}" -eq 61 ]]
f048_expected_ids=()
for id in "${f048_baseline_ids[@]}"; do
  [[ -n "${disposed[$id]:-}" ]] || f048_expected_ids+=("$id")
done
[[ "${f048_actual_ids[*]}" == "${f048_expected_ids[*]}" ]]

for dependency in \
  topics/security.md \
  topics/cross-platform.md \
  topics/contracts.md \
  profiles/boundaries/interop.md \
  profiles/boundaries/language-bindings.md \
  profiles/languages/rust/async.md; do
  [[ -e "$REPO_ROOT/$dependency" ]]
done

expected_groups=(
  $'1\ttopics/security.md\t7\texists\tnone\towner-correction-required'
  $'2\ttopics/cross-platform.md\t6\texists\tnone\towner-correction-required'
  $'3\tprofiles/boundaries/interop.md\t10\texists\ttopics/contracts.md\tone-activated-nine-blocked'
  $'4\tprofiles/languages/rust/interop.md\t1\texists\tprofiles/boundaries/interop.md\towner-correction-required'
  $'5\tprofiles/languages/rust/security.md\t3\texists\ttopics/security.md,profiles/languages/rust/async.md\towner-correction-required'
  $'6\tprofiles/languages/rust/language-bindings.md\t34\texists\tprofiles/boundaries/language-bindings.md,profiles/languages/rust/async.md\tdecomposition-required'
)
mapfile -t actual_groups < <(tail -n +2 "$GROUP_FILE")
[[ "${actual_groups[*]}" == "${expected_groups[*]}" ]]

baseline_trust_total=0
current_trust_total=0
owner_groups=0
while IFS=$'\t' read -r order owner count owner_state prerequisite status extra; do
  [[ "$order" == 'order' ]] && continue
  [[ "$order" =~ ^[1-6]$ && "$count" =~ ^[0-9]+$ ]]
  expected_count="$count"
  if [[ "$owner" == 'profiles/boundaries/interop.md' ]]; then
    expected_count=$((count - next_dispositions))
  fi
  [[ "${remaining_by_owner[$owner]:-0}" -eq "$expected_count" ]]
  [[ -e "$REPO_ROOT/$owner" && "$owner_state" == 'exists' ]]
  [[ -n "$prerequisite" && -n "$status" && -z "${extra:-}" ]]
  ((baseline_trust_total += count))
  ((current_trust_total += expected_count))
  ((owner_groups += 1))
done < "$GROUP_FILE"
[[ "$baseline_trust_total" -eq 61 ]]
[[ "$current_trust_total" -eq $((61 - next_dispositions)) ]]
[[ "$owner_groups" -eq 6 ]]

mapfile -t actual_ids < <(tail -n +2 "$NEXT_SLICE" | cut -f3)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

row_count=0
while IFS=$'\t' read -r slice order id source target disposition rationale extra; do
  [[ "$slice" == 'slice' ]] && continue
  [[ "$slice" == '7.4b7g' && "$order" -eq 1 ]]
  [[ "${source_by_id[$id]}" == "$source" ]]
  [[ "${owner_by_id[$id]}" == "$target" ]]
  [[ "$source" == 'INTEROP-STANDARDS.md' ]]
  [[ "$target" == 'profiles/boundaries/interop.md' ]]
  [[ "$disposition" == 'refine' ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  if [[ -n "${disposed[$id]:-}" ]]; then
    [[ "${disposed_source[$id]}" == "$source" ]]
    [[ "${disposed_target[$id]}" == "$target" ]]
    [[ "${disposed_disposition[$id]}" == "$disposition" ]]
  fi
  ((row_count += 1))
done < "$NEXT_SLICE"
[[ "$row_count" -eq 1 ]]

required_report=(
  '594 frozen identifiers across 29 legacy'
  'six groups total 61 undisposed identifiers'
  '`F048`'
  '`F049`'
  'Select only `STD-0473`'
  '## Accepted Slice 7.4b7f: Planning-Only Remainder Re-plan'
  'No normative or legacy standard, final disposition'
  'registration owner, callback lifetime and thread'
  'in-flight delivery'
  'garbage collection does not prove'
  'fixtures/interop/event-registration-decisions.tsv'
  'verify-interop-event-registration.sh'
  'conditional Concurrency selection'
  'provider contract select'
  'lifecycle phase'
  '## Accepted Slice 7.4b7f2: Executor Delegation Verification Repair'
  'pre-existing checker defect'
  '**No fallback:**'
  '**Pre-slice review:** accepted.'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '(milestone-7-independent-trust-replan.md)' "$PARENT"
rg -F -q '61 remaining identifiers across six owners' "$PARENT"
rg -F -q '| F048 | Partially corrected in Milestone 7.4b7f |' "$FINDINGS"
rg -F -q 'Correct the remaining 60 cross-role destinations' "$FINDINGS"
rg -F -q '| F049 | Planned for corrected Milestone 7.4b7g |' "$FINDINGS"
rg -F -q '| F050 | Resolved in Milestone 7.4b7f2 |' "$FINDINGS"
rg -F -q '## Planned Slice 7.4b7g: Event Registration Lifecycle Contract' \
  "$REPORT"
rg -F -q '`7.4b7f` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7f2` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7g` (`Planned`)' "$PLAN"
rg -F -q '**Next slice:** Milestone 7.4b7g' "$PLAN"

"$SCRIPT_DIR/verify-contract-ownership.sh"
"$SCRIPT_DIR/verify-concurrency-policy.sh"
"$SCRIPT_DIR/verify-interop-boundary-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-decomposition.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 independent trust re-plan passed: %s baseline IDs, %s current across %s owners; next-slice dispositions %s/1\n' \
  "$baseline_trust_total" "$current_trust_total" "$owner_groups" \
  "$next_dispositions"
