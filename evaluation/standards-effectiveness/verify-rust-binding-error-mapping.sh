#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/binding-error-mapping-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

count=0
while IFS=$'\t' read -r case_id contract category cancellation context \
  sensitivity mapping capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$contract" =~ ^(selected|missing|contradictory)$ ]]
  [[ "$category" =~ ^(stable|unsupported|wrong|collapsed)$ ]]
  [[ "$cancellation" =~ ^(preserved|lost|not-applicable)$ ]]
  [[ "$context" =~ ^(bounded|unbounded|not-required)$ ]]
  [[ "$sensitivity" =~ ^(safe|sensitive)$ ]]
  [[ "$mapping" =~ ^(checked|rejected|infallible-claim)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$evidence" =~ ^(native-host|native-only|missing)$ ]]
  [[ "$fallback" =~ ^(none|string-flatten|generic-error|named-framework|drop-semantics|default-success)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$contract" == contradictory ||
        "$category" =~ ^(wrong|collapsed)$ ||
        "$cancellation" == lost ||
        "$context" == unbounded ||
        "$sensitivity" == sensitive ||
        "$mapping" != checked ]]; then
    actual=typed-invalid
  elif [[ "$category" == unsupported ]]; then
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
[[ "$count" -eq 18 ]]

for id in STD-0776 STD-0777; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { count++ } END { print count + 0 }' \
    "$INVENTORY")" -eq 1 ]]
  awk -F '\t' -v id="$id" '
    NR > 1 && $1 == id {
      count += 1
      if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
          $3 != "profiles/languages/rust/language-bindings.md" ||
          $4 != "refine" || $5 == "" || NF != 5) {
        exit 1
      }
    }
    END { exit count != 1 }
  ' "$DISPOSITIONS"
done

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
  '## Host Error Representation'
  'stable categories or codes'
  'Preserve distinctions'
  'bounded and non-sensitive'
  'Return `unsupported`'
  '`unavailable`'
  '`invalid`'
  'infallible `From`'
  'report default success'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_error="$(sed -n '/^## Error Handling Across FFI/,/^---/p' "$LEGACY")"
rg -F -q \
  'profiles/languages/rust/language-bindings.md#host-error-representation' \
  <<< "$legacy_error"
for pattern in \
  'intentionally lossy' \
  'Every variant carries a `message: String`' \
  'From<CoreError> for FfiError' \
  'rustler::Error::Term' \
  'Flatten to string messages' \
  '```'; do
  ! rg -F -q "$pattern" <<< "$legacy_error"
done

prefix_head="$(git -C "$REPO_ROOT" show HEAD:languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md |
  sed '/^## Error Handling Across FFI/,$d')"
prefix_current="$(sed '/^## Error Handling Across FFI/,$d' "$LEGACY")"
callback_head="$(git -C "$REPO_ROOT" show HEAD:languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md |
  sed -n '/^## Host-Language Callbacks and Event Delivery/,$p')"
callback_current="$(sed -n '/^## Host-Language Callbacks and Event Delivery/,$p' \
  "$LEGACY")"
[[ "$prefix_current" == "$prefix_head" ]]
[[ "$callback_current" == "$callback_head" ]]

rg -F -q '`7.4b8h` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-rust-binding-conversions.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
printf 'Rust binding error mapping passed: %s decisions, 2 exact dispositions\n' \
  "$count"
