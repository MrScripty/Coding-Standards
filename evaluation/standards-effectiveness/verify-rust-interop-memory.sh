#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/foreign-memory-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/interop.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-INTEROP-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id conversion arithmetic pointer alignment \
  allocation initialized extent lifetime copy expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$conversion" =~ ^(valid|negative|too-wide)$ ]]
  [[ "$arithmetic" =~ ^(valid|overflow|not-checked)$ ]]
  [[ "$pointer" =~ ^(valid|null|unknown)$ ]]
  [[ "$alignment" =~ ^(valid|invalid|unknown)$ ]]
  [[ "$allocation" =~ ^(single|split|unknown)$ ]]
  [[ "$initialized" =~ ^(full|partial|not-required|unknown)$ ]]
  [[ "$extent" =~ ^(valid|too-large|zero|unknown)$ ]]
  [[ "$lifetime" =~ ^(valid|expired|unknown)$ ]]
  [[ "$copy" =~ ^(after-proof|before-proof|none)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$conversion" != 'valid' ||
          "$arithmetic" != 'valid' ||
          "$pointer" == 'null' ||
          "$alignment" == 'invalid' ||
          "$allocation" == 'split' ||
          "$initialized" == 'partial' ||
          "$extent" == 'too-large' ||
          "$lifetime" == 'expired' ||
          "$copy" == 'before-proof' ]]; then
    actual='typed-invalid'
  elif [[ "$pointer" == 'unknown' ||
          "$alignment" == 'unknown' ||
          "$allocation" == 'unknown' ||
          "$initialized" == 'unknown' ||
          "$extent" == 'unknown' ||
          "$lifetime" == 'unknown' ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

expected_ids=(STD-0752 STD-0753 STD-0754 STD-0755 STD-0756)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $2 == "languages/rust/RUST-INTEROP-STANDARDS.md" &&
    $1 >= "STD-0752" && $1 <= "STD-0756" { print $1 }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && $2 == "languages/rust/RUST-INTEROP-STANDARDS.md" &&
    $1 >= "STD-0752" && $1 <= "STD-0756" { print $1 }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0752)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-INTEROP-STANDARDS.md:profiles/languages/rust/interop.md:move' ]]
      ;;
    STD-0753|STD-0754|STD-0755|STD-0756)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-INTEROP-STANDARDS.md:profiles/languages/rust/interop.md:refine' ]]
      ;;
    *)
      continue
      ;;
  esac
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$REPO_ROOT/topics/security.md" \
  "$REPO_ROOT/profiles/boundaries/interop.md" \
  "$RUST_INDEX" \
  "$PROFILE"

required_profile=(
  '## Checked Dimensions'
  'checked conversion before'
  '## Raw Slice Preconditions'
  'one allocation with compatible provenance'
  'initialized and valid to read'
  'does not exceed `isize::MAX`'
  '## Zero-Length Views'
  '## Copy After Proof'
  'typed `unavailable`'
  'typed `invalid`'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

for file in "$LEGACY"; do
  rg -F -q 'profiles/languages/rust/interop.md' "$file"
done
rg -F -q '(interop.md)' "$RUST_INDEX"

legacy_moved="$(
  awk '
    {
      line = $0
      sub(/\r$/, "", line)
    }
    line == "# Rust Interop Standards" { capture = 1 }
    line == "## Serde Wire-Format Alignment" { capture = 0 }
    capture { print }
  ' "$LEGACY"
)"
if rg -q '```|width as usize|unwrap_or\\(0\\)|from_raw_parts|raw_data\\.to_vec|raw pointer manipulation' \
  <<< "$legacy_moved"; then
  printf 'legacy Rust foreign-memory guidance remains active\n' >&2
  exit 1
fi

rg -F -q '`7.4b3d` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-f022-f023-decomposition.sh"

printf 'Rust interop memory policy passed\n'
