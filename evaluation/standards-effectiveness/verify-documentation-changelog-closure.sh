#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly LEGACY="$REPO_ROOT/DOCUMENTATION-STANDARDS.md"
readonly RELEASE="$REPO_ROOT/workflows/release.md"

mapfile -t expected_ids < <(
  awk -F '\t' '
    $2 == "DOCUMENTATION-STANDARDS.md" &&
    substr($1, 5) + 0 >= 421 &&
    substr($1, 5) + 0 <= 436 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "DOCUMENTATION-STANDARDS.md" &&
    substr($1, 5) + 0 >= 421 &&
    substr($1, 5) + 0 <= 436 { print $1 }
  ' "$DISPOSITIONS"
)

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "${#expected_ids[@]}" -ne 16 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ||
      "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Documentation changelog dispositions are not exact and ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ ! "$id" =~ ^STD-0(42[1-9]|43[0-6])$ ]]; then
    continue
  fi
  [[ "$source" == "DOCUMENTATION-STANDARDS.md" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  case "$id" in
    STD-0423|STD-0424|STD-0432|STD-0433|STD-0434|STD-0435)
      [[ "$target" == "none" && "$disposition" == "remove" ]]
      ;;
    *)
      [[ "$target" == "workflows/release.md" &&
         "$disposition" == "move" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$RELEASE"

for link in \
  'workflows/documentation.md' \
  'reference/recipes/documentation.md' \
  'workflows/release.md'; do
  if ! rg -F -q "$link" "$LEGACY"; then
    printf 'Documentation migration index is missing %s\n' "$link" >&2
    exit 1
  fi
done

if rg -q '^## ' "$LEGACY"; then
  printf 'Documentation migration index retains a policy section\n' >&2
  exit 1
fi

if [[ "$(wc -l < "$LEGACY")" -gt 20 ]]; then
  printf 'Documentation migration index exceeds its bounded role\n' >&2
  exit 1
fi

for section in '## Release Boundary' '## Changelog'; do
  rg -F -q "$section" "$RELEASE"
done

required_release_rules=(
  'consumer-visible changes'
  'unreleased section'
  'Typical categories include added'
  'but project-owned formats'
)
for rule in "${required_release_rules[@]}"; do
  rg -F -q "$rule" "$RELEASE"
done

removed_legacy_content=(
  'Keep a Changelog'
  'All notable changes to this project'
  '2024-01-15'
  '2024-01-01'
)
for content in "${removed_legacy_content[@]}"; do
  if rg -F -q "$content" "$LEGACY"; then
    printf 'Removed changelog content remains: %s\n' "$content" >&2
    exit 1
  fi
done

rg -F -q \
  'Migration index for canonical documentation, release, and recipe owners' \
  "$REPO_ROOT/README.md"

printf 'Documentation changelog closure passed\n'
