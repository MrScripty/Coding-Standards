#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/wire-representation-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly GENERIC="$REPO_ROOT/profiles/boundaries/language-bindings.md"
readonly CONTRACTS="$REPO_ROOT/topics/contracts.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-INTEROP-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"

decision_count=0
while IFS=$'\t' read -r case_id schema serializer attributes consumer variant \
  capability evidence fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$schema" =~ ^(selected|missing|contradictory)$ ]]
  [[ "$serializer" =~ ^(selected|missing|contradictory)$ ]]
  [[ "$attributes" =~ ^(complete|none-applicable|incomplete|contradictory)$ ]]
  [[ "$consumer" =~ ^(aligned|mismatch|missing)$ ]]
  [[ "$variant" =~ ^(supported|unsupported|malformed)$ ]]
  [[ "$capability" =~ ^(available|unavailable)$ ]]
  [[ "$evidence" =~ ^(native-host-round-trip|producer-only|missing)$ ]]
  [[ "$fallback" =~ ^(none|default-shape|schema-free-json|native-layout|unknown-sentinel|omit-variant|alternate-serializer|generated-assumption|weaker-evidence)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        "$schema" == 'contradictory' ||
        "$serializer" == 'contradictory' ||
        "$attributes" =~ ^(incomplete|contradictory)$ ||
        "$consumer" == 'mismatch' ||
        "$variant" == 'malformed' ]]; then
    actual='typed-invalid'
  elif [[ "$variant" == 'unsupported' ]]; then
    actual='typed-unsupported'
  elif [[ "$schema" == 'missing' ||
          "$serializer" == 'missing' ||
          "$consumer" == 'missing' ||
          "$capability" == 'unavailable' ||
          "$evidence" != 'native-host-round-trip' ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
  ((decision_count += 1))
done < "$FIXTURE"
[[ "$decision_count" -eq 27 ]]

mapfile -t inventory_ids < <(
  awk -F '\t' '$1 == "STD-0757" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 == "STD-0757" { print $1 }' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == 'STD-0757' ]]
[[ "${disposition_ids[*]}" == 'STD-0757' ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  [[ "$id" == 'STD-0757' ]] || continue
  [[ "$source:$target:$disposition" == \
    'languages/rust/RUST-INTEROP-STANDARDS.md:profiles/languages/rust/language-bindings.md:refine' ]]
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$CONTRACTS" \
  "$REPO_ROOT/topics/security.md" \
  "$REPO_ROOT/profiles/boundaries/interop.md" \
  "$GENERIC" \
  "$REPO_ROOT/profiles/languages/rust/README.md" \
  "$PROFILE"

required_profile=(
  '## Serialized Wire Representation'
  'Select the wire schema, serializer contract'
  'effective wire representation is derived'
  'Account for every applicable attribute.'
  'Receiving consumers must agree'
  'Generated types do not replace runtime decoding.'
  'typed `invalid`'
  '`unsupported`'
  '`unavailable`'
  'Rust-to-host and host-to-Rust'
  'Producer-only snapshots'
  'schema-free JSON'
  'another serializer or binding mechanism'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done
rg -U -q 'supported schema or protocol\nversion' "$PROFILE"

legacy_wire="$(
  sed -n '/^## Serde Wire-Format Alignment$/,$p' "$LEGACY"
)"
rg -F -q \
  'profiles/languages/rust/language-bindings.md#serialized-wire-representation' \
  <<< "$legacy_wire"
for text in '#[derive(Serialize, Deserialize)]' 'type ServerMessage' \
  'Use explicit `rename_all`' 'Prefer shared schema generation'; do
  if rg -F -q "$text" <<< "$legacy_wire"; then
    printf 'legacy Serde default remains: %s\n' "$text" >&2
    exit 1
  fi
done

rg -F -q '(language-bindings.md)' "$RUST_INDEX"
if rg -F -q 'RUST-INTEROP-STANDARDS.md#serde-wire-format-alignment' \
  "$RUST_INDEX"; then
  printf 'Rust index still routes wire representation to legacy Interop\n' >&2
  exit 1
fi

rg -F -q '| F051 | Resolved in Milestone 7.4b7i |' "$FINDINGS"
"$SCRIPT_DIR/verify-language-binding-boundary.sh"
"$SCRIPT_DIR/verify-rust-binding-conversions.sh"
"$SCRIPT_DIR/verify-milestone-7-independent-trust-replan.sh"

printf 'Rust wire representation passed: %s decisions, 1 exact disposition\n' \
  "$decision_count"
