#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly REFERENCE="$REPO_ROOT/reference/recipes/documentation.md"
readonly LEGACY="$REPO_ROOT/DOCUMENTATION-STANDARDS.md"

mapfile -t expected_ids < <(
  awk -F '\t' '
    $2 == "DOCUMENTATION-STANDARDS.md" &&
    substr($1, 5) + 0 >= 376 &&
    substr($1, 5) + 0 <= 399 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "DOCUMENTATION-STANDARDS.md" &&
    substr($1, 5) + 0 >= 376 &&
    substr($1, 5) + 0 <= 399 { print $1 }
  ' "$DISPOSITIONS"
)

if [[ "${#expected_ids[@]}" -ne 24 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ]]; then
  printf 'Documentation reference disposition count mismatch\n' >&2
  exit 1
fi

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Documentation reference dispositions are not exact or ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ "$id" == "id" || ! "$id" =~ ^STD-0(37[6-9]|38[0-9]|39[0-9])$ ]]; then
    continue
  fi
  [[ "$source" == "DOCUMENTATION-STANDARDS.md" ]]
  [[ "$target" == "reference/recipes/documentation.md" ]]
  [[ "$disposition" == "reference" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < "$DISPOSITIONS"

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/documentation.md" \
  "$REFERENCE"

required_links=(
  "$LEGACY"
)
for file in "${required_links[@]}"; do
  if ! rg -F -q "reference/recipes/documentation.md" "$file"; then
    printf '%s does not link the documentation recipe\n' \
      "${file#"$REPO_ROOT"/}" >&2
    exit 1
  fi
done

legacy_headings='^## (Code Comments|Markdown Formatting|API Documentation|Algorithm Documentation)$'
if rg -q "$legacy_headings" "$LEGACY"; then
  printf 'Legacy documentation example sections remain authoritative\n' >&2
  exit 1
fi

removed_rules=(
  'All public functions, classes, and types should be documented'
  'All rows in a table must use the same column widths'
  'Always include:'
  'For non-trivial algorithms, provide comprehensive documentation'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$LEGACY" "$REFERENCE"; then
    printf 'Removed blanket documentation rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

printf 'Documentation reference consolidation passed\n'
