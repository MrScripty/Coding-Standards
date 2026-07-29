#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/binding-enum-representation-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

count=0
while IFS=$'\t' read -r case_id mechanism contract variants discriminant \
  payload unknown conversion capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$mechanism" =~ ^(framework|wire|c-abi|opaque|generated)$ ]]
  [[ "$contract" =~ ^(selected|missing|contradictory)$ ]]
  [[ "$variants" =~ ^(complete|unsupported|mismatch)$ ]]
  [[ "$discriminant" =~ ^(defined|not-applicable|implicit|wrong)$ ]]
  [[ "$payload" =~ ^(defined|not-applicable|mismatch)$ ]]
  [[ "$unknown" =~ ^(reject|contract-selected|sentinel|omit)$ ]]
  [[ "$conversion" =~ ^(checked|unchecked)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$evidence" =~ ^(native-host|native-only|missing)$ ]]
  [[ "$fallback" =~ ^(none|native-layout|assumed-name|assumed-number|unknown-sentinel|omit-variant|alternate-mechanism|default-success)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$contract" == contradictory ||
        "$variants" == mismatch ||
        "$discriminant" =~ ^(implicit|wrong)$ ||
        "$payload" == mismatch ||
        "$unknown" =~ ^(sentinel|omit)$ ||
        "$conversion" == unchecked ]]; then
    actual=typed-invalid
  elif [[ "$variants" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$contract" == missing ||
          "$capability" == unavailable ||
          "$evidence" != native-host ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
  ((count += 1))
done < "$FIXTURE"
[[ "$count" -eq 25 ]]

[[ "$(awk -F '\t' '$1 == "STD-0797" { count++ } END { print count + 0 }' \
  "$INVENTORY")" -eq 1 ]]
awk -F '\t' '
  NR > 1 && $1 == "STD-0797" {
    count += 1
    if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
        $3 != "profiles/languages/rust/language-bindings.md" ||
        $4 != "refine" || $5 == "" || NF != 5) {
      exit 1
    }
  }
  END { exit count != 1 }
' "$DISPOSITIONS"

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" \
  "$REPO_ROOT/topics/security.md" \
  "$REPO_ROOT/profiles/boundaries/interop.md" \
  "$REPO_ROOT/profiles/boundaries/language-bindings.md" \
  "$REPO_ROOT/profiles/languages/rust/README.md" \
  "$PROFILE"

required_profile=(
  '## Enum Representation'
  'After selecting the boundary mechanism'
  'binding framework contract defines supported variants'
  'Serialized Wire Representation'
  'stable C ABI defines discriminant width'
  'opaque handle exposes only its declared operations'
  'generated wrapper remains derived'
  'implicit discriminants'
  'fieldless Rust enum is not automatically an ABI'
  'integer, and a data-carrying enum'
  'data-carrying enum is not automatically a stable tagged union'
  'Use checked conversion in both directions'
  'Return `invalid`'
  '`unsupported`'
  '`unavailable`'
  'Do not substitute an unknown sentinel'
  'report default success'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_enum="$(
  sed -n '/^### Enum Representation$/,/^---$/p' "$LEGACY"
)"
rg -F -q \
  'profiles/languages/rust/language-bindings.md#enum-representation' \
  <<< "$legacy_enum"
for pattern in \
  'Enum conversion rejects variants' \
  'Serialization is permitted only' \
  '```'; do
  ! rg -F -q "$pattern" <<< "$legacy_enum"
done

rg -F -q '## Memory Ownership Model' "$LEGACY"
rg -F -q '`7.4b8k` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-rust-wire-representation.sh"
"$SCRIPT_DIR/verify-rust-binding-conversions.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
printf 'Rust binding enum representation passed: %s decisions, 1 exact disposition\n' \
  "$count"
