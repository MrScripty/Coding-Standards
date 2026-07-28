#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"

mapfile -t expected_ids < <(
  awk -F '\t' '$2 == "COMMIT-STANDARDS.md" { print $1 }' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' 'NR > 1 && $2 == "COMMIT-STANDARDS.md" { print $1 }' \
    "$DISPOSITIONS"
)

if [[ "${#expected_ids[@]}" -ne "${#actual_ids[@]}" ]]; then
  printf 'Commit disposition count mismatch: expected %s, found %s\n' \
    "${#expected_ids[@]}" "${#actual_ids[@]}" >&2
  exit 1
fi

expected_sorted="$(printf '%s\n' "${expected_ids[@]}" | sort)"
actual_sorted="$(printf '%s\n' "${actual_ids[@]}" | sort)"
if [[ "$expected_sorted" != "$actual_sorted" ]]; then
  printf 'Commit dispositions do not cover the frozen identifiers exactly\n' >&2
  exit 1
fi

duplicates="$(
  printf '%s\n' "${actual_ids[@]}" | sort | uniq -d
)"
if [[ -n "$duplicates" ]]; then
  printf 'Duplicate consolidation dispositions:\n%s\n' "$duplicates" >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ "$id" == "id" || "$source" != "COMMIT-STANDARDS.md" ]]; then
    continue
  fi
  [[ "$disposition" =~ ^(move|reference|remove|index)$ ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]

  if [[ "$disposition" == "remove" ]]; then
    [[ "$target" == "none" ]]
  elif [[ ! -f "$REPO_ROOT/$target" ]]; then
    printf '%s target does not exist: %s\n' "$id" "$target" >&2
    exit 1
  fi
done < "$DISPOSITIONS"

if [[ "$(wc -l < "$REPO_ROOT/COMMIT-STANDARDS.md")" -gt 20 ]]; then
  printf 'Legacy commit index exceeds 20 lines\n' >&2
  exit 1
fi
if ! rg -F -q "workflows/commit.md" "$REPO_ROOT/COMMIT-STANDARDS.md" ||
    ! rg -F -q "reference/recipes/commits.md" \
      "$REPO_ROOT/COMMIT-STANDARDS.md"; then
  printf 'Legacy commit index does not route to both canonical owners\n' >&2
  exit 1
fi
if ! rg -F -q -- "- Role: \`reference\`" \
    "$REPO_ROOT/reference/recipes/commits.md" ||
    ! rg -F -q -- "- Level: \`REFERENCE\`" \
      "$REPO_ROOT/reference/recipes/commits.md"; then
  printf 'Commit recipe is not non-normative reference material\n' >&2
  exit 1
fi

printf 'Commit consolidation dispositions passed\n'
