#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/release/decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/release.md"
readonly LEGACY="$REPO_ROOT/RELEASE-STANDARDS.md"

while IFS=$'\t' read -r case_id ships promise visible expected_release expected_log; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi
  for value in "$ships" "$promise" "$visible" "$expected_release" "$expected_log"; do
    [[ "$value" =~ ^(yes|no)$ ]]
  done

  actual_release="no"
  if [[ "$ships" == "yes" || "$promise" == "yes" ]]; then
    actual_release="yes"
  fi
  actual_log="no"
  if [[ "$actual_release" == "yes" && "$visible" == "yes" ]]; then
    actual_log="yes"
  fi

  if [[ "$actual_release" != "$expected_release" ||
        "$actual_log" != "$expected_log" ]]; then
    printf '%s: expected %s/%s, derived %s/%s\n' \
      "$case_id" "$expected_release" "$expected_log" \
      "$actual_release" "$actual_log" >&2
    exit 1
  fi
done < "$FIXTURE"

mapfile -t expected_ids < <(
  awk -F '\t' '
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 531 &&
    substr($1, 5) + 0 <= 540 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 531 &&
    substr($1, 5) + 0 <= 540 { print $1 }
  ' "$DISPOSITIONS"
)

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "${#expected_ids[@]}" -ne 10 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ||
      "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Release foundation dispositions are not exact and ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ ! "$id" =~ ^STD-0(53[1-9]|540)$ ]]; then
    continue
  fi
  [[ "$source" == "RELEASE-STANDARDS.md" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  if [[ "$id" == "STD-0540" ]]; then
    [[ "$target" == "none" && "$disposition" == "remove" ]]
  else
    [[ "$target" == "workflows/release.md" && "$disposition" == "move" ]]
  fi
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$WORKFLOW"

for file in "$REPO_ROOT/STANDARDS-ROUTER.md" "$LEGACY"; do
  if ! rg -F -q "workflows/release.md" "$file"; then
    printf '%s does not link the canonical release workflow\n' \
      "${file#"$REPO_ROOT"/}" >&2
    exit 1
  fi
done

required_sections=(
  "## Release Boundary"
  "## Contract And Version Decision"
  "## Deprecation And Migration"
  "## Changelog"
  "## Acceptance Boundary"
  "## Optional Reference"
)
for section in "${required_sections[@]}"; do
  rg -F -q "$section" "$WORKFLOW"
done

removed_headings='^## (Semantic Versioning|Changelog Management|Release Acceptance Boundary)$'
if rg -q "$removed_headings" "$LEGACY"; then
  printf 'Legacy release foundation section remains authoritative\n' >&2
  exit 1
fi

if rg -q '^## (Release Artifacts|Reproducible Builds)$' "$LEGACY"; then
  printf 'Migrated artifact foundation remains in the legacy file\n' >&2
  exit 1
fi

removed_rules=(
  'All versioned software must follow'
  '`0.x` signals instability'
  'all member packages share a version'
  'Every PR that adds user-visible changes updates'
  'map commit types to changelog categories'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$WORKFLOW" "$LEGACY"; then
    printf 'Removed release rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

printf 'Release workflow foundation passed\n'
