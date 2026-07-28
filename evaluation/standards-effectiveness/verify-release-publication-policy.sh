#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/release/publication-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly WORKFLOW="$REPO_ROOT/workflows/release.md"
readonly LEGACY="$REPO_ROOT/RELEASE-STANDARDS.md"

while IFS=$'\t' read -r case_id handoff destination channel notes artifacts \
  expected; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi
  for value in "$handoff" "$destination" "$channel" "$notes" "$artifacts" \
    "$expected"; do
    [[ "$value" =~ ^(yes|no)$ ]]
  done

  actual="no"
  if [[ "$handoff" == "yes" && "$destination" == "yes" &&
        "$channel" == "yes" && "$notes" == "yes" &&
        "$artifacts" == "yes" ]]; then
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
    substr($1, 5) + 0 >= 566 &&
    substr($1, 5) + 0 <= 574 { print $1 }
  ' "$INVENTORY"
)
mapfile -t actual_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "RELEASE-STANDARDS.md" &&
    substr($1, 5) + 0 >= 566 &&
    substr($1, 5) + 0 <= 574 { print $1 }
  ' "$DISPOSITIONS"
)

expected_ordered="$(printf '%s\n' "${expected_ids[@]}")"
actual_ordered="$(printf '%s\n' "${actual_ids[@]}")"
if [[ "${#expected_ids[@]}" -ne 9 ||
      "${#actual_ids[@]}" -ne "${#expected_ids[@]}" ||
      "$expected_ordered" != "$actual_ordered" ]]; then
  printf 'Release publication dispositions are not exact and ordered\n' >&2
  exit 1
fi

while IFS=$'\t' read -r id source target disposition rationale extra; do
  if [[ ! "$id" =~ ^STD-0(56[6-9]|57[0-4])$ ]]; then
    continue
  fi
  [[ "$source" == "RELEASE-STANDARDS.md" ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
  case "$id" in
    STD-0572|STD-0573)
      [[ "$target" == "none" && "$disposition" == "remove" ]]
      ;;
    STD-0566|STD-0569|STD-0570)
      [[ "$target" == "workflows/release.md" &&
         "$disposition" == "move" ]]
      ;;
    *)
      [[ "$target" == "workflows/release.md" &&
         "$disposition" == "merge" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$WORKFLOW"

rg -F -q '## Publication Presentation' "$WORKFLOW"
required_rules=(
  'A publication surface presents an accepted release to consumers'
  'own versioning, channels, artifact identity'
  'A provider feature or manual'
  'Major version zero does not by itself'
  'summaries may supplement'
  'Present the exact artifact identities and relationships'
  'release-publication diagnostic'
)
for rule in "${required_rules[@]}"; do
  rg -F -q "$rule" "$WORKFLOW"
done

if rg -q '^## (GitHub Releases|Downloads)$' "$LEGACY"; then
  printf 'Legacy hosted publication policy remains authoritative\n' >&2
  exit 1
fi

for retained in '## Language-Specific Guidance' '## Release Checklist' \
  '## Rollback Procedure' '## Release Tool Recipes'; do
  rg -F -q "$retained" "$LEGACY"
done

removed_rules=(
  "GitHub's auto-generated release notes"
  'CI creates draft GitHub Release'
  'my-tool-1.0.0-x86_64'
  'libmy_lib-1.0.0'
  'checksums-sha256.txt'
)
for rule in "${removed_rules[@]}"; do
  if rg -F -q "$rule" "$WORKFLOW" "$LEGACY"; then
    printf 'Removed publication rule remains: %s\n' "$rule" >&2
    exit 1
  fi
done

printf 'Release publication policy passed\n'
