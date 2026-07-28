#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/release/recovery-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/release.md"
readonly LEGACY="$REPO_ROOT/RELEASE-STANDARDS.md"

while IFS=$'\t' read -r case_id scope capability authority action evidence \
  expected; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi
  for value in "$scope" "$capability" "$authority" "$action" "$evidence" \
    "$expected"; do
    [[ "$value" =~ ^(yes|no)$ ]]
  done

  actual="no"
  if [[ "$scope" == "yes" && "$capability" == "yes" &&
        "$authority" == "yes" && "$action" == "yes" &&
        "$evidence" == "yes" ]]; then
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
    substr($1, 5) + 0 >= 577 &&
    substr($1, 5) + 0 <= 581 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 577 &&
    substr($1, 5) + 0 <= 581 { print $1 }
  ' "$DISPOSITIONS"
)

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "${#expected_ids[@]}" -ne 5 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ||
      "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Release recovery dispositions are not exact and ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ ! "$id" =~ ^STD-0(57[7-9]|58[0-1])$ ]]; then
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

rg -F -q '## Recovery And Withdrawal' "$WORKFLOW"
required_rules=(
  'Published artifacts may be immutable, cached'
  'Classify affected release units, versions, channels'
  'withdrawal as erasure'
  'Urgency does not grant implicit authority'
  'recovery status cannot waive normal acceptance'
  'it is not a universal post-incident record'
  'typed release-recovery'
)
for rule in "${required_rules[@]}"; do
  rg -F -q "$rule" "$WORKFLOW"
done

if rg -q '^## Rollback Procedure$' "$LEGACY"; then
  printf 'Legacy rollback policy remains authoritative\n' >&2
  exit 1
fi
rg -F -q 'workflows/release.md' "$LEGACY"

removed_rules=(
  'Revert the GitHub Release to draft'
  'crates.io, npm, PyPI'
  'Address the issue on `main`'
  '[Hotfix Workflow](#hotfix-workflow)'
  'Publish a new patch version'
  'do not wait for consensus'
  'Add a brief post-mortem note to the changelog'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$WORKFLOW" "$LEGACY"; then
    printf 'Removed release-recovery rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

printf 'Release recovery policy passed\n'
