#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly OWNER_RULES="$SCRIPT_DIR/owner-map.tsv"
readonly OWNER_OVERRIDES="$SCRIPT_DIR/owner-overrides.tsv"
readonly OUTPUT="$SCRIPT_DIR/generated/rule-owner-map.tsv"

declare -A owners
declare -A dispositions
declare -A override_owners
declare -A override_dispositions

while IFS=$'\t' read -r current_path future_owner disposition; do
  if [[ "$current_path" == "current_path" ]]; then
    continue
  fi
  if [[ -n "${owners[$current_path]:-}" ]]; then
    printf 'Duplicate owner mapping for %s\n' "$current_path" >&2
    exit 1
  fi
  owners["$current_path"]="$future_owner"
  dispositions["$current_path"]="$disposition"
done < "$OWNER_RULES"

while IFS=$'\t' read -r id_start id_end future_owner disposition; do
  if [[ "$id_start" == "id_start" ]]; then
    continue
  fi
  start="${id_start#STD-}"
  end="${id_end#STD-}"
  for ((number = 10#$start; number <= 10#$end; number += 1)); do
    id="$(printf 'STD-%04d' "$number")"
    if [[ -n "${override_owners[$id]:-}" ]]; then
      printf 'Duplicate owner override for %s\n' "$id" >&2
      exit 1
    fi
    override_owners["$id"]="$future_owner"
    override_dispositions["$id"]="$disposition"
  done
done < "$OWNER_OVERRIDES"

printf 'id\tcurrent_path\tline\tfuture_owner\tdisposition\theading\n' > "$OUTPUT"

while IFS=$'\t' read -r id current_path line _level _role _old_disposition heading; do
  if [[ "$id" == "id" ]]; then
    continue
  fi
  if [[ -z "${owners[$current_path]:-}" ]]; then
    printf 'Missing future owner for %s (%s)\n' "$id" "$current_path" >&2
    exit 1
  fi
  future_owner="${override_owners[$id]:-${owners[$current_path]}}"
  disposition="${override_dispositions[$id]:-${dispositions[$current_path]}}"
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$id" "$current_path" "$line" "$future_owner" "$disposition" "$heading" \
    >> "$OUTPUT"
done < "$INVENTORY"

printf 'Generated canonical-owner proposals for %s sections\n' \
  "$(( $(wc -l < "$OUTPUT") - 1 ))"
