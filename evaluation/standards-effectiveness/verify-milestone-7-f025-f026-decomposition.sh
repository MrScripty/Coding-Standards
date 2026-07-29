#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly MAP="$SCRIPT_DIR/milestone-7-f025-f026-slices.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-f025-f026-decomposition.md"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly OWNER_MAP="$SCRIPT_DIR/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"
readonly PARENT="$SCRIPT_DIR/milestone-7-decomposition.md"
readonly TRUST_REPLAN="$SCRIPT_DIR/milestone-7-trust-lifecycle-replan.md"

readonly -a slices=(7.4b5b 7.4b5c 7.4b5d 7.4b5e 7.4b5f)
declare -A expected_counts=(
  [7.4b5b]=4
  [7.4b5c]=3
  [7.4b5d]=1
  [7.4b5e]=1
  [7.4b5f]=1
)
declare -A disposed_counts=(
  [7.4b5b]=0
  [7.4b5c]=0
  [7.4b5d]=0
  [7.4b5e]=0
  [7.4b5f]=0
)

expected_ids=(
  STD-0759 STD-0760 STD-0790 STD-0791
  STD-0798 STD-0799 STD-0800 STD-0781 STD-0822 STD-0825
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

  [[ "$slice" =~ ^7\.4b5[b-f]$ ]]
  [[ "$order" -eq "$expected_order" ]]
  [[ "$source" =~ ^languages/rust/RUST-(LANGUAGE-BINDINGS|SECURITY)-STANDARDS\.md$ ]]
  [[ "$target" =~ ^profiles/languages/rust/(language-bindings|security)\.md$ ]]
  [[ "$disposition" == 'refine' ]]
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
    STD-0759|STD-0760|STD-0790|STD-0791)
      [[ "$slice:$target" == \
        '7.4b5b:profiles/languages/rust/language-bindings.md' ]]
      ;;
    STD-0798|STD-0799|STD-0800)
      [[ "$slice:$target" == \
        '7.4b5c:profiles/languages/rust/language-bindings.md' ]]
      ;;
    STD-0781)
      [[ "$slice:$target" == \
        '7.4b5d:profiles/languages/rust/language-bindings.md' ]]
      ;;
    STD-0822)
      [[ "$slice:$target" == \
        '7.4b5e:profiles/languages/rust/security.md' ]]
      ;;
    STD-0825)
      [[ "$slice:$target" == \
        '7.4b5f:profiles/languages/rust/security.md' ]]
      ;;
    *)
      exit 1
      ;;
  esac

  ((row_count += 1))
  ((expected_order += 1))
done < "$MAP"
[[ "$row_count" -eq 10 ]]

required_report=(
  '[milestone-7-f025-f026-slices.tsv](milestone-7-f025-f026-slices.tsv)'
  'Only the first implementation slice is fully specified.'
  'The accepted `STD-0802` disposition'
  'Bindings adapt a host call to an injected runtime/lifecycle capability'
  'A canonicalized `PathBuf` is'
  'Per-call inputs, cancellation, and results remain'
  '## Accepted Slice 7.4b5b: Binding Core And Adapter Boundary'
  '**No fallback:**'
  'Independent trust-boundary groups remain'
)
for text in "${required_report[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q 'milestone-7-f025-f026-decomposition.md' "$PLAN"
rg -F -q '(milestone-7-f025-f026-decomposition.md)' "$PARENT"
rg -F -q '(milestone-7-f025-f026-decomposition.md)' "$TRUST_REPLAN"
rg -F -q '`7.4b5a` (`Accepted`)' "$PLAN"

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
  if rg -q '^\*\*Next slice:\*\* .*7\.4b5[b-f]' "$PLAN"; then
    printf 'Accepted F025/F026 slice remains next\n' >&2
    exit 1
  fi
fi

"$SCRIPT_DIR/verify-milestone-7-trust-lifecycle-replan.sh"
"$SCRIPT_DIR/check-plan-structure.sh" "$PLAN"
"$SCRIPT_DIR/verify-plan-fixtures.sh"

printf 'Milestone 7 F025/F026 decomposition passed: 10 IDs across 5 serial slices; dispositions %s/4 %s/3 %s/1 %s/1 %s/1\n' \
  "${disposed_counts[7.4b5b]}" \
  "${disposed_counts[7.4b5c]}" \
  "${disposed_counts[7.4b5d]}" \
  "${disposed_counts[7.4b5e]}" \
  "${disposed_counts[7.4b5f]}"
