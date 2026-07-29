#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/binding-conversion-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly GENERIC="$REPO_ROOT/profiles/boundaries/language-bindings.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id mechanism representation conversion boundary \
  ownership fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$mechanism" =~ ^(framework|serialized|c-abi|opaque|generated)$ ]]
  [[ "$representation" =~ ^(declared|undeclared|incompatible)$ ]]
  [[ "$conversion" =~ ^(infallible|checked-valid|rejected|schema-valid|schema-invalid|unchecked|infallible-claim|not-required)$ ]]
  [[ "$boundary" =~ ^(native-host|native-only|not-checked)$ ]]
  [[ "$ownership" =~ ^(declared|missing|not-required)$ ]]
  [[ "$fallback" =~ ^(none|lossy-path|default|json-abi|alternate-framework)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$representation" == 'undeclared' ||
          "$conversion" =~ ^(rejected|schema-invalid|unchecked|infallible-claim)$ ||
          ( "$representation" == 'declared' && "$boundary" != 'native-host' ) ||
          "$ownership" == 'missing' ||
          "$fallback" != 'none' ]]; then
    actual='typed-invalid'
  elif [[ "$representation" == 'incompatible' ]]; then
    actual='typed-unsupported'
  else
    actual='allow'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

expected_ids=(STD-0772 STD-0773 STD-0774 STD-0775 STD-0794 STD-0795 STD-0796 STD-0801 STD-0802 STD-0803)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $2 == "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" &&
    ($1 == "STD-0772" || $1 == "STD-0773" || $1 == "STD-0774" ||
     $1 == "STD-0775" || $1 == "STD-0794" || $1 == "STD-0795" ||
     $1 == "STD-0796" || $1 == "STD-0801" || $1 == "STD-0802" ||
     $1 == "STD-0803") { print $1 }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && $2 == "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" &&
    ($1 == "STD-0772" || $1 == "STD-0773" || $1 == "STD-0774" ||
     $1 == "STD-0775" || $1 == "STD-0794" || $1 == "STD-0795" ||
     $1 == "STD-0796" || $1 == "STD-0801" || $1 == "STD-0802" ||
     $1 == "STD-0803") { print $1 }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0772|STD-0794)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:profiles/languages/rust/language-bindings.md:move' ]]
      ;;
    STD-0773|STD-0774|STD-0775|STD-0795|STD-0796|STD-0802|STD-0803)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:profiles/languages/rust/language-bindings.md:refine' ]]
      ;;
    STD-0801)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:profiles/languages/rust/language-bindings.md:merge' ]]
      ;;
    *)
      continue
      ;;
  esac
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" "$REPO_ROOT/topics/security.md" \
  "$REPO_ROOT/profiles/boundaries/interop.md" "$GENERIC" \
  "$RUST_INDEX" "$PROFILE"

required_profile=(
  '## Representation Categories'
  'Framework lifting is not C-ABI safety'
  '## Fallible Conversion'
  'Reserve `From` and `Into`'
  '`TryFrom`, `TryInto`'
  '## Stable C ABI'
  '## Verification'
  'concrete native/host boundary'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do rg -F -q "$text" "$PROFILE"; done

rg -F -q '(language-bindings.md)' "$RUST_INDEX"
rg -F -q 'profiles/languages/rust/language-bindings.md' "$REPO_ROOT/README.md" "$LEGACY"
rg -F -q 'Rust specialization' "$GENERIC"

legacy_forbidden=(
  'Cast with `as`'
  'to_string_lossy'
  'as_millis() as u64'
  'Every FFI wrapper type implements `From'
  '| `String` | Yes'
  '| `Vec<T>` (T is FFI-safe) | Yes'
  '| `Option<T>` (T is FFI-safe) | Yes'
)
for text in "${legacy_forbidden[@]}"; do
  if rg -F -q "$text" "$LEGACY"; then
    printf 'legacy Rust binding conversion guidance remains active: %s\n' \
      "$text" >&2
    exit 1
  fi
done

rg -F -q '| F022 | Resolved in Milestone 7.4b3g |' "$FINDINGS"
rg -F -q '`7.4b3g` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-f022-f023-decomposition.sh"

printf 'Rust binding conversion policy passed\n'
