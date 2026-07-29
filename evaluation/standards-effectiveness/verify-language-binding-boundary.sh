#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/language-bindings/representation-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/boundaries/language-bindings.md"
readonly LEGACY="$REPO_ROOT/LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id mechanism representation schema conversion \
  generated_logic expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$mechanism" =~ ^(framework|serialized|c-abi|opaque|generated|unknown|unavailable)$ ]]
  [[ "$representation" =~ ^(declared|undeclared|incompatible)$ ]]
  [[ "$schema" =~ ^(valid|invalid|unavailable|not-required)$ ]]
  [[ "$conversion" =~ ^(valid|rejected|not-checked)$ ]]
  [[ "$generated_logic" =~ ^(absent|present)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$mechanism" == 'unknown' || "$representation" == 'incompatible' ]]; then
    actual='typed-unsupported'
  elif [[ "$mechanism" == 'unavailable' || "$schema" == 'unavailable' ]]; then
    actual='typed-unavailable'
  elif [[ "$representation" != 'declared' ||
          "$schema" == 'invalid' ||
          "$conversion" != 'valid' ||
          "$generated_logic" == 'present' ]]; then
    actual='typed-invalid'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

expected_ids=(STD-0483 STD-0484 STD-0485 STD-0486)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $2 == "LANGUAGE-BINDINGS-STANDARDS.md" &&
    $1 >= "STD-0483" && $1 <= "STD-0486" { print $1 }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && $2 == "LANGUAGE-BINDINGS-STANDARDS.md" &&
    $1 >= "STD-0483" && $1 <= "STD-0486" { print $1 }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0483|STD-0485)
      [[ "$source:$target:$disposition" == \
        'LANGUAGE-BINDINGS-STANDARDS.md:profiles/boundaries/language-bindings.md:move' ]]
      ;;
    STD-0484)
      [[ "$source:$target:$disposition" == \
        'LANGUAGE-BINDINGS-STANDARDS.md:profiles/boundaries/language-bindings.md:refine' ]]
      ;;
    STD-0486)
      [[ "$source:$target:$disposition" == \
        'LANGUAGE-BINDINGS-STANDARDS.md:profiles/boundaries/language-bindings.md:merge' ]]
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
  "$PROFILE"

required_profile=(
  '## Declare The Boundary Mechanism'
  'binding-framework lifting'
  'Stable ABI value'
  'Opaque handle'
  'Generated host wrapper'
  'Framework support does not imply stable memory layout'
  'Return:'
  '`invalid`'
  '`unsupported`'
  '`unavailable`'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

for file in "$REPO_ROOT/README.md" "$REPO_ROOT/STANDARDS-ROUTER.md" "$LEGACY"; do
  rg -F -q 'profiles/boundaries/language-bindings.md' "$file"
done

if rg -q '^## |```|FFI-safe DTOs|Multiple binding frameworks|Language-Specific Extensions' \
  "$LEGACY"; then
  printf 'legacy language-binding policy remains active\n' >&2
  exit 1
fi

removed_patterns=(
  'Framework support does not imply'
  'reinterpret'
  'lossy or schema-free'
)
for pattern in "${removed_patterns[@]}"; do
  rg -F -q "$pattern" "$PROFILE"
done

rg -F -q '`7.4b3c` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-f022-f023-decomposition.sh"

printf 'Language binding boundary policy passed\n'
