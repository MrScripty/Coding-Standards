#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/release/artifact-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/release.md"
readonly LEGACY="$REPO_ROOT/RELEASE-STANDARDS.md"

while IFS=$'\t' read -r case_id ships bundles sbom_required checksum_consumed \
  closure_source consumer_resolves expected_sbom expected_checksum \
  expected_lockfile; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi
  for value in "$ships" "$bundles" "$sbom_required" "$checksum_consumed" \
    "$closure_source" "$consumer_resolves" "$expected_sbom" \
    "$expected_checksum" "$expected_lockfile"; do
    [[ "$value" =~ ^(yes|no)$ ]]
  done

  actual_sbom="no"
  if [[ "$ships" == "yes" &&
        ( "$bundles" == "yes" || "$sbom_required" == "yes" ) ]]; then
    actual_sbom="yes"
  fi

  actual_checksum="no"
  if [[ "$ships" == "yes" && "$checksum_consumed" == "yes" ]]; then
    actual_checksum="yes"
  fi

  actual_lockfile="no"
  if [[ "$ships" == "yes" && "$closure_source" == "yes" ]]; then
    actual_lockfile="yes"
  elif [[ "$ships" == "yes" && "$consumer_resolves" != "yes" ]]; then
    printf '%s: dependency resolution ownership is unresolved\n' \
      "$case_id" >&2
    exit 1
  fi

  actual="$actual_sbom/$actual_checksum/$actual_lockfile"
  expected="$expected_sbom/$expected_checksum/$expected_lockfile"
  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

mapfile -t expected_ids < <(
  awk -F '\t' '
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 543 &&
    substr($1, 5) + 0 <= 551 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 543 &&
    substr($1, 5) + 0 <= 551 { print $1 }
  ' "$DISPOSITIONS"
)

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "${#expected_ids[@]}" -ne 9 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ||
      "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Release artifact dispositions are not exact and ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ ! "$id" =~ ^STD-0(54[3-9]|55[0-1])$ ]]; then
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

for section in '## Artifact Plan' '## Reproducibility'; do
  rg -F -q "$section" "$WORKFLOW"
done

if rg -q '^## (Release Artifacts|Reproducible Builds)$' "$LEGACY"; then
  printf 'Legacy artifact or reproducibility policy remains authoritative\n' >&2
  exit 1
fi

for retained in '## Rollback Procedure' '## Release Tool Recipes'; do
  rg -F -q "$retained" "$LEGACY"
done

removed_rules=(
  'SHA256 checksums | Always'
  'Recommended for all releases'
  'Commit lockfiles for applications; omit them for libraries.'
  'not required for initial or pre-1.0 releases'
  'Use GitHub'\''s pre-release flag for `0.x.y`'
  'Generate `checksums-sha256.txt`'
  'Generate SBOM'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$WORKFLOW" "$LEGACY"; then
    printf 'Removed artifact rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

rg -F -q 'workflows/release.md' "$LEGACY"
rg -F -q 'Major version zero does not by itself' "$WORKFLOW"

printf 'Release artifact policy passed\n'
