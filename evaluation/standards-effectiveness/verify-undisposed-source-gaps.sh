#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
INVENTORY="$S/generated/section-inventory.tsv"
DISPOSITIONS="$S/consolidation-dispositions.tsv"
EXPECTED="$S/fixtures/migration/undisposed-source-gaps.tsv"
BASELINE="$(awk -F '\t' '$1 == "baseline_commit" { print $2 }' "$S/generated/summary.tsv")"

[[ "$BASELINE" =~ ^[0-9a-f]{40}$ ]]
git -C "$R" cat-file -e "$BASELINE^{commit}"

declare -A id_by_location path_by_id level_by_id heading_by_id
declare -A disposed expected_class expected_reason observed

while IFS=$'\t' read -r id path line level _role _disposition heading extra; do
  [[ "$id" == id ]] && continue
  [[ -z "${extra:-}" ]]
  id_by_location["$path"$'\t'"$line"]="$id"
  path_by_id["$id"]="$path"
  level_by_id["$id"]="$level"
  heading_by_id["$id"]="$heading"
done < "$INVENTORY"

while IFS=$'\t' read -r id _rest; do
  [[ "$id" == id ]] && continue
  disposed["$id"]=1
done < "$DISPOSITIONS"

while IFS=$'\t' read -r id classification reason extra; do
  [[ "$id" == id ]] && continue
  [[ "$id" =~ ^STD-[0-9]{4}$ ]]
  [[ "$classification" =~ ^(retained-diff|deferred-row38|deferred-row47)$ ]]
  [[ -n "$reason" && -z "${extra:-}" ]]
  [[ -z "${expected_class[$id]:-}" ]]
  [[ -n "${path_by_id[$id]:-}" ]]
  expected_class["$id"]="$classification"
  expected_reason["$id"]="$reason"
done < "$EXPECTED"

while IFS=$'\t' read -r path line; do
  id="${id_by_location["$path"$'\t'"$line"]:-}"
  [[ -n "$id" && -z "${disposed[$id]:-}" ]] || continue
  observed["$id"]=1
done < <(
  git -C "$R" diff --no-ext-diff --unified=0 "$BASELINE" -- '*.md' |
    awk '
      BEGIN { OFS="\t" }
      /^--- a\// { path=substr($0, 7); next }
      /^--- \/dev\/null/ { path=""; next }
      /^\+\+\+ / { next }
      /^@@ / {
        h=$0
        sub(/^@@ -/, "", h)
        sub(/[, +].*$/, "", h)
        old=h+0
        next
      }
      /^-/ {
        content=substr($0, 2)
        if (path != "" && content ~ /^#{1,6} /) print path, old
        old++
        next
      }
      /^\+/ { next }
      /^ / { old++; next }
    '
)

for id in "${!observed[@]}"; do
  if [[ -z "${expected_class[$id]:-}" ]]; then
    printf 'invalid: unrecorded undisposed source gap %s\n' "$id" >&2
    exit 1
  fi
done
for id in "${!expected_class[@]}"; do
  if [[ -z "${observed[$id]:-}" ]]; then
    printf 'invalid: expected source-gap candidate is no longer observed: %s\n' "$id" >&2
    exit 1
  fi

  path="${path_by_id[$id]}"
  level="${level_by_id[$id]}"
  heading="${heading_by_id[$id]}"
  current_count="$(
    awk -v expected_level="$level" -v expected_heading="$heading" '
      /^#{1,6} / {
        match($0, /^#+/)
        actual_level=RLENGTH
        actual_heading=substr($0, actual_level + 2)
        sub(/\r$/, "", actual_heading)
        if (actual_level == expected_level && actual_heading == expected_heading) count++
      }
      END { print count+0 }
    ' "$R/$path"
  )"

  if [[ "${expected_class[$id]}" == retained-diff ]]; then
    [[ "$current_count" -gt 0 ]] || {
      printf 'invalid: retained source heading is absent: %s\n' "$id" >&2
      exit 1
    }
  elif [[ "$current_count" -ne 0 ]]; then
    printf 'invalid: deferred source heading remains active: %s\n' "$id" >&2
    exit 1
  fi
done

printf 'Undisposed source-gap audit passed: %d exact candidates\n' "${#observed[@]}"
