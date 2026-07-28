#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly MAP="$SCRIPT_DIR/milestone-7-f022-f023-slices.tsv"
readonly REPORT="$SCRIPT_DIR/milestone-7-f022-f023-decomposition.md"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

readonly -a slices=(7.4b3b 7.4b3c 7.4b3d 7.4b3e 7.4b3f 7.4b3g)
declare -A expected_counts=(
  [7.4b3b]=8
  [7.4b3c]=4
  [7.4b3d]=5
  [7.4b3e]=1
  [7.4b3f]=6
  [7.4b3g]=10
)
declare -A disposed_counts=(
  [7.4b3b]=0
  [7.4b3c]=0
  [7.4b3d]=0
  [7.4b3e]=0
  [7.4b3f]=0
  [7.4b3g]=0
)

expected_ids=(
  STD-0465 STD-0466 STD-0467 STD-0468 STD-0469 STD-0470 STD-0471 STD-0472
  STD-0483 STD-0484 STD-0485 STD-0486
  STD-0752 STD-0753 STD-0754 STD-0755 STD-0756
  STD-0823
  STD-0843 STD-0844 STD-0845 STD-0846 STD-0847 STD-0848
  STD-0772 STD-0773 STD-0774 STD-0775
  STD-0794 STD-0795 STD-0796
  STD-0801 STD-0802 STD-0803
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

  [[ "$slice" =~ ^7\.4b3[b-g]$ ]]
  [[ "$order" -eq "$expected_order" ]]
  [[ "$source" =~ ^(INTEROP-STANDARDS.md|LANGUAGE-BINDINGS-STANDARDS.md|languages/rust/RUST-(INTEROP|SECURITY|UNSAFE|LANGUAGE-BINDINGS)-STANDARDS.md)$ ]]
  [[ "$target" =~ ^profiles/(boundaries/(interop|language-bindings)|languages/rust/(interop|security|unsafe|language-bindings)).md$ ]]
  [[ "$disposition" =~ ^(move|merge|refine)$ ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]

  inventory_source="$(
    awk -F '\t' -v expected="$id" '$1 == expected { print $2 }' "$INVENTORY"
  )"
  [[ "$inventory_source" == "$source" ]]

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
    STD-0465|STD-0466)
      [[ "$slice:$target:$disposition" == \
        '7.4b3b:profiles/boundaries/interop.md:move' ]]
      ;;
    STD-0467)
      [[ "$slice:$target:$disposition" == \
        '7.4b3b:profiles/boundaries/interop.md:merge' ]]
      ;;
    STD-0468|STD-0469|STD-0470|STD-0471|STD-0472)
      [[ "$slice:$target:$disposition" == \
        '7.4b3b:profiles/boundaries/interop.md:refine' ]]
      ;;
    STD-0483|STD-0485)
      [[ "$slice:$target:$disposition" == \
        '7.4b3c:profiles/boundaries/language-bindings.md:move' ]]
      ;;
    STD-0484)
      [[ "$slice:$target:$disposition" == \
        '7.4b3c:profiles/boundaries/language-bindings.md:refine' ]]
      ;;
    STD-0486)
      [[ "$slice:$target:$disposition" == \
        '7.4b3c:profiles/boundaries/language-bindings.md:merge' ]]
      ;;
    STD-0752)
      [[ "$slice:$target:$disposition" == \
        '7.4b3d:profiles/languages/rust/interop.md:move' ]]
      ;;
    STD-0753|STD-0754|STD-0755|STD-0756)
      [[ "$slice:$target:$disposition" == \
        '7.4b3d:profiles/languages/rust/interop.md:refine' ]]
      ;;
    STD-0823)
      [[ "$slice:$target:$disposition" == \
        '7.4b3e:profiles/languages/rust/security.md:refine' ]]
      ;;
    STD-0843)
      [[ "$slice:$target:$disposition" == \
        '7.4b3f:profiles/languages/rust/unsafe.md:move' ]]
      ;;
    STD-0844|STD-0845|STD-0846|STD-0847|STD-0848)
      [[ "$slice:$target:$disposition" == \
        '7.4b3f:profiles/languages/rust/unsafe.md:refine' ]]
      ;;
    STD-0772|STD-0794)
      [[ "$slice:$target:$disposition" == \
        '7.4b3g:profiles/languages/rust/language-bindings.md:move' ]]
      ;;
    STD-0773|STD-0774|STD-0775|STD-0795|STD-0796|STD-0802|STD-0803)
      [[ "$slice:$target:$disposition" == \
        '7.4b3g:profiles/languages/rust/language-bindings.md:refine' ]]
      ;;
    STD-0801)
      [[ "$slice:$target:$disposition" == \
        '7.4b3g:profiles/languages/rust/language-bindings.md:merge' ]]
      ;;
    *)
      exit 1
      ;;
  esac

  ((row_count += 1))
  ((expected_order += 1))
done < "$MAP"
[[ "$row_count" -eq 34 ]]

required_report_text=(
  '[milestone-7-f022-f023-slices.tsv](milestone-7-f022-f023-slices.tsv)'
  'framework may lift or serialize'
  'allocation, initialization, alignment, provenance, lifetime'
  'copying afterward cannot repair invalid slice construction'
  'typed diagnostic'
  'no cast'
  '`F023` is resolved only after'
  '`F022` is resolved'
)
for text in "${required_report_text[@]}"; do
  rg -F -q "$text" "$REPORT"
done

rg -F -q 'milestone-7-f022-f023-decomposition.md' "$PLAN"
rg -F -q '`7.4b3a` (`Accepted`)' "$PLAN"

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
  if rg -q '^\*\*Next slice:\*\* .*7\.4b3[b-g]' "$PLAN"; then
    printf 'Accepted F022/F023 slice remains next\n' >&2
    exit 1
  fi
fi

printf 'Milestone 7 F022/F023 decomposition passed: 34 IDs across 6 serial slices; dispositions %s/8 %s/4 %s/5 %s/1 %s/6 %s/10\n' \
  "${disposed_counts[7.4b3b]}" \
  "${disposed_counts[7.4b3c]}" \
  "${disposed_counts[7.4b3d]}" \
  "${disposed_counts[7.4b3e]}" \
  "${disposed_counts[7.4b3f]}" \
  "${disposed_counts[7.4b3g]}"
