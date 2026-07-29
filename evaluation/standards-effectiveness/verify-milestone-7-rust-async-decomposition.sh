#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly MAP="$SCRIPT_DIR/milestone-7-rust-async-slices.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-rust-async-decomposition.md"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly PARENT="$SCRIPT_DIR/milestone-7-decomposition.md"

readonly -a slices=(7.4b4d 7.4b4e 7.4b4f 7.4b4g)
declare -A expected_counts=(
  [7.4b4d]=2
  [7.4b4e]=3
  [7.4b4f]=2
  [7.4b4g]=2
)
declare -A disposed_counts=(
  [7.4b4d]=0
  [7.4b4e]=0
  [7.4b4f]=0
  [7.4b4g]=0
)

expected_ids=(
  STD-0717 STD-0718 STD-0719 STD-0720 STD-0721
  STD-0722 STD-0723 STD-0724 STD-0725
)
mapfile -t actual_ids < <(tail -n +2 "$MAP" | cut -f3)
[[ "${actual_ids[*]}" == "${expected_ids[*]}" ]]
[[ "$(printf '%s\n' "${actual_ids[@]}" | sort | uniq -d | wc -l)" -eq 0 ]]

row_count=0
expected_order=1
while IFS=$'\t' read -r slice order id source target disposition rationale extra; do
  if [[ "$slice" == 'slice' ]]; then
    [[ "$order" == 'order' && "$id" == 'id' && "$source" == 'source' ]]
    continue
  fi

  [[ "$slice" =~ ^7\.4b4[d-g]$ ]]
  [[ "$order" -eq "$expected_order" ]]
  [[ "$source" == 'languages/rust/RUST-ASYNC-STANDARDS.md' ]]
  [[ "$target" == 'profiles/languages/rust/async.md' ]]
  [[ "$disposition" =~ ^(move|refine)$ ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]

  inventory_source="$(
    awk -F '\t' -v expected="$id" '$1 == expected { print $2 }' "$INVENTORY"
  )"
  owner_target="$(
    awk -F '\t' -v expected="$id" '$1 == expected { print $4 }' "$OWNER_MAP"
  )"
  [[ "$inventory_source" == "$source" ]]
  [[ "$owner_target" == "$target" ]]

  current_disposition="$(
    awk -F '\t' -v expected="$id" '
      NR > 1 && $1 == expected {
        count += 1
        value = $2 "\t" $3 "\t" $4
      }
      END {
        if (count > 1) {
          exit 2
        }
        if (count == 1) {
          print value
        }
      }
    ' "$DISPOSITIONS"
  )"
  if [[ -n "$current_disposition" ]]; then
    [[ "$current_disposition" == \
      "$source"$'\t'"$target"$'\t'"$disposition" ]]
    ((disposed_counts["$slice"] += 1))
  fi

  case "$id" in
    STD-0717)
      [[ "$slice:$disposition" == '7.4b4d:move' ]]
      ;;
    STD-0718)
      [[ "$slice:$disposition" == '7.4b4d:refine' ]]
      ;;
    STD-0719|STD-0720|STD-0721)
      [[ "$slice:$disposition" == '7.4b4e:refine' ]]
      ;;
    STD-0722|STD-0723)
      [[ "$slice:$disposition" == '7.4b4f:refine' ]]
      ;;
    STD-0724|STD-0725)
      [[ "$slice:$disposition" == '7.4b4g:refine' ]]
      ;;
    *)
      exit 1
      ;;
  esac

  ((row_count += 1))
  ((expected_order += 1))
done < "$MAP"
[[ "$row_count" -eq 9 ]]

required_report=(
  '[milestone-7-rust-async-slices.tsv](milestone-7-rust-async-slices.tsv)'
  'Only the first implementation slice is fully specified.'
  'dropping a Rust future stops polling that future'
  'does not by itself authorize force-aborting work'
  'The Rust Async profile does not own domain policy'
  '## Next Slice 7.4b4d: Rust Async Foundation'
  '**No fallback:**'
  'After `7.4b4g`, dependent Rust Security and Rust'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q 'milestone-7-rust-async-decomposition.md' "$PLAN"
rg -F -q '(milestone-7-rust-async-decomposition.md)' "$PARENT"
rg -F -q '`7.4b4c` (`Accepted`)' "$PLAN"

first_planned=''
seen_planned=0
for slice in "${slices[@]}"; do
  planned="$(grep -cF "\`$slice\` (\`Planned\`)" "$PLAN" || true)"
  accepted="$(grep -cF "\`$slice\` (\`Accepted\`)" "$PLAN" || true)"
  [[ "$((planned + accepted))" -eq 1 ]]

  if [[ "$accepted" -eq 1 ]]; then
    [[ "$seen_planned" -eq 0 ]]
    [[ "${disposed_counts[$slice]}" -eq "${expected_counts[$slice]}" ]]
  else
    seen_planned=1
    [[ "${disposed_counts[$slice]}" -eq 0 ]]
    if [[ -z "$first_planned" ]]; then
      first_planned="$slice"
    fi
  fi
done

if [[ -n "$first_planned" ]]; then
  rg -F -q "**Next slice:** Milestone $first_planned" "$PLAN"
else
  if rg -q '^\*\*Next slice:\*\* .*7\.4b4[d-g]' "$PLAN"; then
    printf 'Accepted Rust Async slice remains next\n' >&2
    exit 1
  fi
fi

"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 Rust Async decomposition passed: 9 IDs across 4 serial slices; dispositions %s/2 %s/3 %s/2 %s/2\n' \
  "${disposed_counts[7.4b4d]}" \
  "${disposed_counts[7.4b4e]}" \
  "${disposed_counts[7.4b4f]}" \
  "${disposed_counts[7.4b4g]}"
