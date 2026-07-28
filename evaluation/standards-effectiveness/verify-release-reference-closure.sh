#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/release.md"
readonly RECIPE="$REPO_ROOT/reference/recipes/releases.md"
readonly LEGACY="$REPO_ROOT/RELEASE-STANDARDS.md"

mapfile -t expected_ids < <(
  awk -F '\t' '
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 541 &&
    substr($1, 5) + 0 <= 542 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 541 &&
    substr($1, 5) + 0 <= 542 { print $1 }
  ' "$DISPOSITIONS"
)

if [[ "${expected_ids[*]}" != 'STD-0541 STD-0542' ]]; then
  printf 'unexpected frozen release-reference identifiers: %s\n' \
    "${expected_ids[*]:-none}" >&2
  exit 1
fi
if [[ "${actual_ids[*]}" != "${expected_ids[*]}" ]]; then
  printf 'release-reference dispositions do not exactly cover frozen IDs\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0541|STD-0542)
      [[ "$source" == 'RELEASE-STANDARDS.md' ]]
      [[ "$target" == 'reference/recipes/releases.md' ]]
      [[ "$disposition" == 'move' ]]
      [[ -n "$rationale" && -z "${extra:-}" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$WORKFLOW" \
  "$RECIPE"

rg -F -q -- '- Level: `REFERENCE`' "$RECIPE"
rg -F -q 'does not require git-cliff' "$RECIPE"
rg -F -q '../reference/recipes/releases.md' "$WORKFLOW"
rg -F -q 'workflows/release.md' "$LEGACY"
rg -F -q 'reference/recipes/releases.md' "$LEGACY"

if [[ "$(rg -c '^# ' "$LEGACY")" -ne 1 ]] ||
   rg -q '^## |```|git-cliff|cliff\.toml|\b(MUST|SHOULD|REQUIRED)\b' "$LEGACY"; then
  printf 'legacy release index retains policy or executable recipe content\n' >&2
  exit 1
fi

printf 'Release reference closure checks passed.\n'
