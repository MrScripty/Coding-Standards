#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/release/procedure-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/release.md"
readonly LEGACY="$REPO_ROOT/RELEASE-STANDARDS.md"
readonly ROUTER="$REPO_ROOT/STANDARDS-ROUTER.md"
readonly RUST_PROFILE="$REPO_ROOT/profiles/languages/rust/README.md"

while IFS=$'\t' read -r case_id boundary profiles decisions claims dispatch \
  artifacts publication expected; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi
  for value in "$boundary" "$profiles" "$decisions" "$claims" "$dispatch" \
    "$artifacts" "$publication" "$expected"; do
    [[ "$value" =~ ^(yes|no)$ ]]
  done

  actual="no"
  if [[ "$boundary" == "yes" && "$profiles" == "yes" &&
        "$decisions" == "yes" && "$claims" == "yes" &&
        "$dispatch" == "yes" && "$artifacts" == "yes" &&
        "$publication" == "yes" ]]; then
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
    substr($1, 5) + 0 >= 575 &&
    substr($1, 5) + 0 <= 576 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 575 &&
    substr($1, 5) + 0 <= 576 { print $1 }
  ' "$DISPOSITIONS"
)

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "${#expected_ids[@]}" -ne 2 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ||
      "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Release procedure dispositions are not exact and ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ ! "$id" =~ ^STD-0(575|576)$ ]]; then
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
  "$WORKFLOW" \
  "$RUST_PROFILE"

rg -F -q '## Profile Routing And Release Procedure' "$WORKFLOW"
required_rules=(
  'Use [Standards Router](../STANDARDS-ROUTER.md)'
  'Profiles add ecosystem mechanisms and verification'
  'Derive the release procedure from the accepted release decisions'
  'Select applicable profiles and topics through the router'
  'Satisfy every required behavior, environment, and release-artifact claim'
  'typed release-procedure'
)
for rule in "${required_rules[@]}"; do
  rg -F -q "$rule" "$WORKFLOW"
done

rg -F -q '| Rust source, Cargo metadata, or Rust-generated artifacts change |' \
  "$ROUTER"
rg -F -q '[Release](../../../languages/rust/RUST-RELEASE-STANDARDS.md)' \
  "$RUST_PROFILE"

if rg -q '^## (Language-Specific Guidance|Release Checklist)$' "$LEGACY"; then
  printf 'Legacy release routing or checklist remains authoritative\n' >&2
  exit 1
fi

rg -F -q 'workflows/release.md' "$LEGACY"

removed_rules=(
  'cargo audit'
  'npm audit'
  'pip-audit'
  'chore(release): prepare vX.Y.Z'
  'git tag vX.Y.Z'
  'Push commit and intended release tag'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$WORKFLOW" "$LEGACY"; then
    printf 'Removed release-procedure rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

printf 'Release procedure policy passed\n'
