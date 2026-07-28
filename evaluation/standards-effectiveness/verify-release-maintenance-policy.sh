#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/release/maintenance-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/release.md"
readonly LEGACY="$REPO_ROOT/RELEASE-STANDARDS.md"

while IFS=$'\t' read -r case_id maintenance lineage supported reconciliation \
  channel expected; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi
  for value in "$maintenance" "$lineage" "$supported" "$reconciliation" \
    "$channel" "$expected"; do
    [[ "$value" =~ ^(yes|no)$ ]]
  done

  actual="no"
  if [[ "$maintenance" == "yes" && "$lineage" == "yes" &&
        "$supported" == "yes" && "$reconciliation" == "yes" &&
        "$channel" == "yes" ]]; then
    actual="yes"
  fi
  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

mapfile -t expected_ids < <(
  awk -F '\t' '
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 561 &&
    substr($1, 5) + 0 <= 565 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 561 &&
    substr($1, 5) + 0 <= 565 { print $1 }
  ' "$DISPOSITIONS"
)

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "${#expected_ids[@]}" -ne 5 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ||
      "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Release maintenance dispositions are not exact and ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ ! "$id" =~ ^STD-0(56[1-5])$ ]]; then
    continue
  fi
  [[ "$source" == "RELEASE-STANDARDS.md" ]]
  [[ "$target" == "workflows/release.md" ]]
  [[ "$disposition" == "move" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$WORKFLOW"

rg -F -q '## Maintenance And Channels' "$WORKFLOW"
required_rules=(
  'maintenance contract before making that promise'
  'has no intrinsic branch, tag, maintenance duration'
  'Do not mutate published bytes or silently omit an affected supported'
  'release-maintenance diagnostic'
  'A release channel is a consumer contract'
  'Prerelease identifiers and channels are independent decisions'
  'release-channel diagnostic'
  'Feature flags and runtime activation controls do not define release channels'
)
for rule in "${required_rules[@]}"; do
  rg -F -q "$rule" "$WORKFLOW"
done

if rg -q '^## (Hotfix and LTS Workflow|Feature Flags and Release Channels)$' \
  "$LEGACY"; then
  printf 'Legacy maintenance or channel policy remains authoritative\n' >&2
  exit 1
fi

for retained in '## GitHub Releases' '## Language-Specific Guidance' \
  '## Release Checklist' '## Rollback Procedure' '## Release Tool Recipes'; do
  rg -F -q "$retained" "$LEGACY"
done

removed_rules=(
  'git checkout -b hotfix/vX.Y.Z'
  'release/X.Y'
  '12 months of security patches'
  '`stable`, `beta`, `nightly`'
  'Flags should be short-lived'
  'Library releases typically do not need feature flags'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$WORKFLOW" "$LEGACY"; then
    printf 'Removed maintenance/channel rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

printf 'Release maintenance policy passed\n'
