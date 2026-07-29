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

expected_ids=()
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
[[ "$global_remaining" -eq 589 ]]
[[ "${#remaining_sources[@]}" -eq 28 ]]
[[ "${#remaining_owners[@]}" -eq 27 ]]

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
  $'1\ttopics/security.md\t7\texists\ttopics/contracts.md\ttwo-accepted-five-decomposition-required\tnone\tSTD-0583,STD-0601'
  $'2\ttopics/cross-platform.md\t6\texists\tnone\tdecomposition-and-missing-owner\tworkflows/tooling.md\tnone'
  $'3\tprofiles/boundaries/interop.md\t10\texists\ttopics/contracts.md\tone-accepted-nine-decomposition-required\tnone\tSTD-0473'
  $'4\tprofiles/languages/rust/interop.md\t1\texists\tprofiles/languages/rust/language-bindings.md,topics/contracts.md\tone-accepted-no-current-remainder\tnone\tSTD-0757'
  $'5\tprofiles/languages/rust/security.md\t3\texists\ttopics/security.md\tone-accepted-two-blocked\tnone\tSTD-0824'
  $'6\tprofiles/languages/rust/language-bindings.md\t34\texists\tprofiles/boundaries/language-bindings.md,profiles/languages/rust/async.md\tdecomposition-and-missing-owner\tworkflows/tooling.md\tnone'
)
mapfile -t actual_groups < <(tail -n +2 "$GROUP_FILE")
[[ "${actual_groups[*]}" == "${expected_groups[*]}" ]]

baseline_trust_total=0
current_trust_total=0
owner_groups=0
while IFS=$'\t' read -r order owner count owner_state prerequisite status \
  known_missing_owner accepted_ids extra; do
  [[ "$order" == 'order' ]] && continue
  [[ "$order" =~ ^[1-6]$ && "$count" =~ ^[0-9]+$ ]]
  accepted_count=0
  if [[ "$accepted_ids" != 'none' ]]; then
    IFS=',' read -r -a group_accepted_ids <<< "$accepted_ids"
    for accepted_id in "${group_accepted_ids[@]}"; do
      [[ " ${f048_baseline_ids[*]} " == *" $accepted_id "* ]]
      [[ -n "${disposed[$accepted_id]:-}" ]]
      ((accepted_count += 1))
    done
  fi
  expected_count=$((count - accepted_count))
  [[ "${remaining_by_owner[$owner]:-0}" -eq "$expected_count" ]]
  [[ -e "$REPO_ROOT/$owner" && "$owner_state" == 'exists' ]]
  [[ -n "$prerequisite" && -n "$status" && -n "$known_missing_owner" &&
      -n "$accepted_ids" &&
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
[[ "$current_trust_total" -eq 56 ]]
[[ "$owner_groups" -eq 6 ]]

mapfile -t actual_ids < <(tail -n +2 "$NEXT_SLICE" | cut -f3)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]

expected_rows=()
mapfile -t actual_rows < <(tail -n +2 "$NEXT_SLICE")
[[ "${actual_rows[*]}" == "${expected_rows[*]}" ]]

row_count=0
while IFS=$'\t' read -r slice order id source target disposition rationale extra; do
  [[ "$slice" == 'slice' ]] && continue
  [[ "$slice" == '7.4b7m' && "$order" =~ ^[12]$ ]]
  [[ "${source_by_id[$id]}" == "$source" ]]
  [[ "${owner_by_id[$id]}" == 'topics/security.md' ]]
  [[ "$source" == 'SECURITY-STANDARDS.md' ]]
  [[ "$target" == 'topics/contracts.md' ]]
  [[ "$disposition" == 'refine' ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  [[ -z "${disposed[$id]:-}" ]]
  ((row_count += 1))
done < "$NEXT_SLICE"
[[ "$row_count" -eq 0 ]]

required_report=(
  '589 residual identifiers across 28 legacy'
  '61 frozen baseline identifiers and 56 current identifiers'
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
  '## Accepted Slice 7.4b7i: Rust Serialized Binding Representation'
  '## Planned Slice 7.4b7j: Independent Trust Remainder Re-plan'
  '## Accepted Slice 7.4b7j: Independent Trust Remainder Re-plan'
  '## Planned Slice 7.4b7k: Rust External-Input Queue Contract'
  '## Accepted Slice 7.4b7k: Rust External-Input Queue Contract'
  '## Planned Slice 7.4b7l: Independent Trust Remainder Re-plan'
  '## Accepted Slice 7.4b7l: Independent Trust Remainder Re-plan'
  '## Planned Slice 7.4b7m: Validation Proof-Lifetime Contract'
  '## Accepted Slice 7.4b7m: Validation Proof-Lifetime Contract'
  '## Planned Slice 7.4b7n: Independent Trust Remainder Re-plan'
  'rolling remainder is 593 identifiers'
  'independent trust subset is 60 identifiers'
  'Their 61 frozen identifiers include accepted `STD-0473`'
  '`STD-0757` is a serialized Rust/host representation'
  'first isolated draft selected six generic Security'
  'schema-free JSON'
  '`F051`'
  'pre-existing checker defect'
  'rolling remainder is 592 identifiers across 28 legacy sources and 27'
  '27 focused wire-representation decisions'
  '`STD-0824` is a bounded external-input queue rule'
  '`F052`'
  '`STD-0583` and `STD-0601` are one validation'
  '`F053`'
  'rolling remainder is 589 identifiers'
  'rolling remainder is 591 identifiers'
  'independent trust remainder'
  '**No fallback:**'
  '**Pre-slice review:** accepted.'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done
rg -U -q 'independent trust\nremainder is 59 identifiers' "$REPORT"

rg -F -q '(milestone-7-independent-trust-replan.md)' "$PARENT"
rg -F -q '56 remaining identifiers across six proposed-owner groups' "$PARENT"
rg -F -q '| F048 | Partially corrected through Milestone 7.4b7m |' "$FINDINGS"
rg -F -q 'Correct the remaining 56 cross-role destinations' "$FINDINGS"
rg -F -q '| F049 | Resolved in Milestone 7.4b7g |' "$FINDINGS"
rg -F -q '| F050 | Resolved in Milestone 7.4b7f2 |' "$FINDINGS"
rg -F -q '| F051 | Resolved in Milestone 7.4b7i |' "$FINDINGS"
rg -F -q '| F052 | Resolved in Milestone 7.4b7k |' "$FINDINGS"
rg -F -q '| F053 | Resolved in Milestone 7.4b7m |' "$FINDINGS"
rg -F -q '## Accepted Slice 7.4b7g: Event Registration Lifecycle Contract' \
  "$REPORT"
rg -F -q '`7.4b7f` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7f2` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7g` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7h` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7i` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7j` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7k` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7l` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7m` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b7n` (`Planned`)' "$PLAN"
rg -F -q '**Next slice:** Milestone 7.4b7n' "$PLAN"

"$SCRIPT_DIR/verify-contract-ownership.sh"
"$SCRIPT_DIR/verify-concurrency-policy.sh"
"$SCRIPT_DIR/verify-interop-boundary-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-decomposition.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 independent trust re-plan passed: %s baseline IDs, %s current across %s owners; next-slice dispositions %s/0\n' \
  "$baseline_trust_total" "$current_trust_total" "$owner_groups" \
  "$next_dispositions"
