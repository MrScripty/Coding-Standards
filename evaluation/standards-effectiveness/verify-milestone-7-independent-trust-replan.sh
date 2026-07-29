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

expected_ids=(STD-0757)
next_dispositions=0
for id in "${expected_ids[@]}"; do
  [[ -n "${disposed[$id]:-}" ]] && ((next_dispositions += 1))
done
[[ "$next_dispositions" -eq 0 ]]

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
[[ "$global_remaining" -eq 593 ]]
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
  profiles/languages/rust/async.md \
  profiles/languages/rust/language-bindings.md; do
  [[ -e "$REPO_ROOT/$dependency" ]]
done

expected_groups=(
  $'1\ttopics/security.md\t7\texists\ttopics/contracts.md\tdecomposition-required\tnone'
  $'2\ttopics/cross-platform.md\t6\texists\tnone\tdecomposition-and-missing-owner\tworkflows/tooling.md'
  $'3\tprofiles/boundaries/interop.md\t10\texists\ttopics/contracts.md\tone-accepted-nine-decomposition-required\tnone'
  $'4\tprofiles/languages/rust/interop.md\t1\texists\tprofiles/languages/rust/language-bindings.md,topics/contracts.md\tcorrected-owner-ready\tnone'
  $'5\tprofiles/languages/rust/security.md\t3\texists\ttopics/security.md,profiles/languages/rust/async.md\tdecomposition-and-missing-owner\tprofiles/languages/rust/api.md'
  $'6\tprofiles/languages/rust/language-bindings.md\t34\texists\tprofiles/boundaries/language-bindings.md,profiles/languages/rust/async.md\tdecomposition-and-missing-owner\tworkflows/tooling.md'
)
mapfile -t actual_groups < <(tail -n +2 "$GROUP_FILE")
[[ "${actual_groups[*]}" == "${expected_groups[*]}" ]]

baseline_trust_total=0
current_trust_total=0
owner_groups=0
while IFS=$'\t' read -r order owner count owner_state prerequisite status \
  known_missing_owner extra; do
  [[ "$order" == 'order' ]] && continue
  [[ "$order" =~ ^[1-6]$ && "$count" =~ ^[0-9]+$ ]]
  expected_count="$count"
  case "$owner" in
    profiles/boundaries/interop.md)
      expected_count=$((count - 1))
      ;;
    profiles/languages/rust/interop.md)
      expected_count=$((count - next_dispositions))
      ;;
  esac
  [[ "${remaining_by_owner[$owner]:-0}" -eq "$expected_count" ]]
  [[ -e "$REPO_ROOT/$owner" && "$owner_state" == 'exists' ]]
  [[ -n "$prerequisite" && -n "$status" && -n "$known_missing_owner" &&
      -z "${extra:-}" ]]
  if [[ "$known_missing_owner" == 'none' ]]; then
    [[ "$status" != *missing-owner* ]]
  else
    [[ "$status" == *missing-owner* ]]
    [[ ! -e "$REPO_ROOT/$known_missing_owner" ]]
  fi
  ((baseline_trust_total += count))
  ((current_trust_total += expected_count))
  ((owner_groups += 1))
done < "$GROUP_FILE"
[[ "$baseline_trust_total" -eq 61 ]]
[[ "$current_trust_total" -eq 60 ]]
[[ "$owner_groups" -eq 6 ]]

mapfile -t actual_ids < <(tail -n +2 "$NEXT_SLICE" | cut -f3)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

expected_rows=(
  $'7.4b7i\t1\tSTD-0757\tlanguages/rust/RUST-INTEROP-STANDARDS.md\tprofiles/languages/rust/language-bindings.md\trefine\tbind the effective Serde wire shape to the selected schema attributes consumer contract and native-host evidence'
)
mapfile -t actual_rows < <(tail -n +2 "$NEXT_SLICE")
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

row_count=0
while IFS=$'\t' read -r slice order id source target disposition rationale extra; do
  [[ "$slice" == 'slice' ]] && continue
  [[ "$slice" == '7.4b7i' && "$order" -eq 1 ]]
  [[ "${source_by_id[$id]}" == "$source" ]]
  [[ "${owner_by_id[$id]}" == 'profiles/languages/rust/interop.md' ]]
  [[ "$source" == 'languages/rust/RUST-INTEROP-STANDARDS.md' ]]
  [[ "$target" == 'profiles/languages/rust/language-bindings.md' ]]
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
  '593 residual identifiers across 29 legacy'
  '61 frozen baseline identifiers and 60 current identifiers'
  '`F048`'
  '`F049`'
  '## Accepted Slice 7.4b7f: Planning-Only Remainder Re-plan'
  'No normative or legacy standard, final disposition'
  'in-flight delivery'
  'fixtures/interop/event-registration-decisions.tsv'
  'verify-interop-event-registration.sh'
  'conditional Concurrency selection'
  'provider contract select'
  'lifecycle phase'
  '## Accepted Slice 7.4b7f2: Executor Delegation Verification Repair'
  '## Accepted Slice 7.4b7g: Event Registration Lifecycle Contract'
  '## Accepted Slice 7.4b7h: Independent Trust Remainder Re-plan'
  '## Planned Slice 7.4b7i: Rust Serialized Binding Representation'
  'rolling remainder is 593 identifiers'
  'independent trust subset is 60 identifiers'
  'Their 61 frozen identifiers include accepted `STD-0473`'
  '`STD-0757` is a serialized Rust/host representation'
  'first isolated draft selected six generic Security'
  'schema-free JSON'
  '`F051`'
  'pre-existing checker defect'
  '**No fallback:**'
  '**Pre-slice review:** accepted.'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q '(milestone-7-independent-trust-replan.md)' "$PARENT"
rg -F -q '60 remaining identifiers across six proposed-owner groups' "$PARENT"
rg -F -q '| F048 | Partially corrected through Milestone 7.4b7g |' "$FINDINGS"
rg -F -q 'Correct the remaining 60 cross-role destinations' "$FINDINGS"
rg -F -q '| F049 | Resolved in Milestone 7.4b7g |' "$FINDINGS"
rg -F -q '| F050 | Resolved in Milestone 7.4b7f2 |' "$FINDINGS"
rg -F -q '| F051 | Planned for Milestone 7.4b7i |' "$FINDINGS"
rg -F -q '## Accepted Slice 7.4b7g: Event Registration Lifecycle Contract' \
  "$REPORT"
rg -F -q '`7.4b7f` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7f2` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7g` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7h` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7i` (`Planned`)' "$PLAN"
rg -F -q '**Next slice:** Milestone 7.4b7i' "$PLAN"

"$SCRIPT_DIR/verify-contract-ownership.sh"
"$SCRIPT_DIR/verify-concurrency-policy.sh"
"$SCRIPT_DIR/verify-interop-boundary-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-decomposition.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 independent trust re-plan passed: %s baseline IDs, %s current across %s owners; next-slice dispositions %s/1\n' \
  "$baseline_trust_total" "$current_trust_total" "$owner_groups" \
  "$next_dispositions"
