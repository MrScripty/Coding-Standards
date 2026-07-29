#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/checked-boundary-arithmetic-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/security.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-SECURITY-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id conversion arithmetic limit zero fallback \
  expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$conversion" =~ ^(valid|negative|too-wide|unchecked)$ ]]
  [[ "$arithmetic" =~ ^(checked|overflow|unchecked|not-checked)$ ]]
  [[ "$limit" =~ ^(within|exceeded|not-checked)$ ]]
  [[ "$zero" =~ ^(not-zero|permitted|forbidden)$ ]]
  [[ "$fallback" =~ ^(none|zero|clamp|saturate|wrap|truncate|smaller-default)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$conversion" != 'valid' ||
        "$arithmetic" != 'checked' ||
        "$limit" != 'within' ||
        "$zero" == 'forbidden' ||
        "$fallback" != 'none' ]]; then
    actual='typed-invalid'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

mapfile -t inventory_ids < <(
  awk -F '\t' '
    $2 == "languages/rust/RUST-SECURITY-STANDARDS.md" &&
    $1 == "STD-0823" { print $1 }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && $2 == "languages/rust/RUST-SECURITY-STANDARDS.md" &&
    $1 == "STD-0823" { print $1 }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == 'STD-0823' ]]
[[ "${disposition_ids[*]}" == 'STD-0823' ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  [[ "$id" == 'STD-0823' ]] || continue
  [[ "$source:$target:$disposition" == \
    'languages/rust/RUST-SECURITY-STANDARDS.md:profiles/languages/rust/security.md:refine' ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/security.md" \
  "$RUST_INDEX" \
  "$PROFILE"

required_profile=(
  '## Checked Boundary Sizing'
  'checked conversion before'
  'checked arithmetic for every operation'
  '## Resource Limits'
  'resource limit after representability'
  'typed `invalid`'
  '## Interop Relationship'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

rg -F -q '(security.md)' "$RUST_INDEX"
rg -F -q 'profiles/languages/rust/security.md' "$LEGACY"

legacy_moved="$(
  awk '
    {
      line = $0
      sub(/\r$/, "", line)
    }
    line == "## Checked Arithmetic At Boundaries" { capture = 1 }
    line == "## Bounded Queues" { capture = 0 }
    capture { print }
  ' "$LEGACY"
)"
if rg -q '```|as usize|checked_mul|expect|unwrap|BufferSizeOverflow' \
  <<< "$legacy_moved"; then
  printf 'legacy Rust boundary arithmetic guidance remains active\n' >&2
  exit 1
fi

rg -F -q '`7.4b3e` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-f022-f023-decomposition.sh"

printf 'Rust boundary arithmetic policy passed\n'
