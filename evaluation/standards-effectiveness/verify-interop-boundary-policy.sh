#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/interop/foreign-memory-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/boundaries/interop.md"
readonly LEGACY="$REPO_ROOT/INTEROP-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id representation allocation initialized access \
  lifetime thread release copy proof expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$representation" =~ ^(valid|unsupported)$ ]]
  [[ "$allocation" =~ ^(valid|invalid|unavailable)$ ]]
  [[ "$initialized" =~ ^(valid|partial|not-required)$ ]]
  [[ "$access" =~ ^(allowed|denied)$ ]]
  [[ "$lifetime" =~ ^(valid|expired)$ ]]
  [[ "$thread" =~ ^(valid|wrong|not-required)$ ]]
  [[ "$release" =~ ^(valid|double|not-required)$ ]]
  [[ "$copy" =~ ^(after-proof|before-proof|none)$ ]]
  [[ "$proof" =~ ^(complete|guessed|sentinel|alternate|none)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$representation" == 'unsupported' ]]; then
    actual='typed-unsupported'
  elif [[ "$allocation" == 'unavailable' ]]; then
    actual='typed-unavailable'
  elif [[ "$allocation" == 'invalid' ||
          "$initialized" == 'partial' ||
          "$access" == 'denied' ||
          "$lifetime" == 'expired' ||
          "$thread" == 'wrong' ||
          "$release" == 'double' ||
          "$copy" == 'before-proof' ||
          "$proof" != 'complete' ]]; then
    actual='typed-invalid'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

expected_ids=(
  STD-0465 STD-0466 STD-0467 STD-0468
  STD-0469 STD-0470 STD-0471 STD-0472
)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $2 == "INTEROP-STANDARDS.md" &&
    $1 >= "STD-0465" && $1 <= "STD-0472" { print $1 }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && $2 == "INTEROP-STANDARDS.md" &&
    $1 >= "STD-0465" && $1 <= "STD-0472" { print $1 }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0465|STD-0466)
      [[ "$source:$target:$disposition" == \
        'INTEROP-STANDARDS.md:profiles/boundaries/interop.md:move' ]]
      ;;
    STD-0467)
      [[ "$source:$target:$disposition" == \
        'INTEROP-STANDARDS.md:profiles/boundaries/interop.md:merge' ]]
      ;;
    STD-0468|STD-0469|STD-0470|STD-0471|STD-0472)
      [[ "$source:$target:$disposition" == \
        'INTEROP-STANDARDS.md:profiles/boundaries/interop.md:refine' ]]
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
  "$PROFILE"

required_profile=(
  '## Foreign Authority'
  'allocation identity'
  'initialized readable or writable extent'
  'provider-guaranteed lifetime'
  '## Copying Is Not Proof'
  '## Initialization And Release'
  '## Thread And Callback Contract'
  'Return `invalid`'
  '`unsupported`'
  '`unavailable`'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

for file in "$REPO_ROOT/STANDARDS-ROUTER.md" "$LEGACY"; do
  rg -F -q 'profiles/boundaries/interop.md' "$file"
done

legacy_moved="$(
  awk '
    {
      line = $0
      sub(/\r$/, "", line)
    }
    line == "# Interop Standards" { capture = 1 }
    line == "### 6. Event Subscription Lifecycle" { capture = 0 }
    capture { print }
  ' "$LEGACY"
)"
if rg -q '```|JsonSerializer|IDisposable|CallDeferred|Always copy|Validate before use' \
  <<< "$legacy_moved"; then
  printf 'legacy foreign-authority guidance remains active\n' >&2
  exit 1
fi

rg -F -q '`7.4b3b` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-f022-f023-decomposition.sh"

printf 'Interop boundary policy passed\n'
