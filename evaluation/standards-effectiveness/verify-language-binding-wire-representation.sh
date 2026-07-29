#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/language-bindings/serialized-wire-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/boundaries/language-bindings.md"
readonly LEGACY="$REPO_ROOT/INTEROP-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

count=0
while IFS=$'\t' read -r case_id schema serializer shape consumer variant \
  capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$schema" =~ ^(selected|missing)$ ]]
  [[ "$serializer" =~ ^(selected|missing)$ ]]
  [[ "$shape" =~ ^(complete|incomplete|contradictory)$ ]]
  [[ "$consumer" =~ ^(aligned|mismatch|missing)$ ]]
  [[ "$variant" =~ ^(supported|unsupported|malformed)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$evidence" =~ ^(round-trip|one-way-consumer|producer-only|missing)$ ]]
  [[ "$fallback" =~ ^(none|default-shape|schema-free|omit-variant|alternate-serializer|weaker-evidence)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$shape" =~ ^(incomplete|contradictory)$ ||
        "$consumer" == mismatch ||
        "$variant" == malformed ]]; then
    actual=typed-invalid
  elif [[ "$variant" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$schema" == missing ||
          "$serializer" == missing ||
          "$consumer" == missing ||
          "$capability" == unavailable ||
          "$evidence" =~ ^(producer-only|missing)$ ]]; then
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

for id in STD-0478 STD-0479 STD-0480; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { count++ } END { print count + 0 }' \
    "$INVENTORY")" -eq 1 ]]
  awk -F '\t' -v id="$id" '
    NR > 1 && $1 == id {
      count += 1
      if ($2 != "INTEROP-STANDARDS.md" ||
          $3 != "profiles/boundaries/language-bindings.md" ||
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
  "$PROFILE"

required_profile=(
  '## Serialized Wire Representation'
  'tagged-enum form'
  'variant spelling'
  'flattening, omission, and default rule'
  'Consumers must agree'
  'producer-to-consumer and consumer-to-producer'
  'Return `invalid`'
  '`unsupported`'
  '`unavailable`'
  'retry with another serializer'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

for heading in \
  '### Tagged Enum Alignment' \
  '### Enum Variant Alignment' \
  '### Struct Field Alignment'; do
  section="$(
    sed -n "/^${heading}$/,/^### /p" "$LEGACY" | sed '$d'
  )"
  rg -F -q \
    'profiles/boundaries/language-bindings.md#serialized-wire-representation' \
    <<< "$section"
done

for pattern in \
  'Tagged enum serializers produce specific wire shapes' \
  'Check the serializer configuration in the source language' \
  'determine field name casing' \
  'RUST-INTEROP-STANDARDS.md#serde-wire-format-alignment'; do
  ! rg -F -q "$pattern" "$LEGACY"
done

rg -F -q '`7.4b8e` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-language-binding-boundary.sh"
"$SCRIPT_DIR/verify-cross-language-contract.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
printf 'Language Binding wire representation passed: %s decisions, 3 exact dispositions\n' \
  "$count"
