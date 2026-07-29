#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE_DIR="$SCRIPT_DIR/fixtures/rust"
readonly SCHEMA="$FIXTURE_DIR/binding-core-adapter-testability-schema.tsv"
readonly DECISIONS="$FIXTURE_DIR/binding-core-adapter-testability-decisions.tsv"
readonly OBSERVED="$FIXTURE_DIR/binding-core-adapter-testability-observed.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

"$SCRIPT_DIR/check-decision-table.sh" "$SCHEMA" "$DECISIONS" "$OBSERVED"

while IFS=$'\t' read -r case_id boundary core_evidence adapter_required \
  adapter_evidence capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$boundary" == contradictory ||
        "$core_evidence" == failed ||
        "$adapter_evidence" =~ ^(failed|native-only)$ ||
        ( "$adapter_required" == no &&
          "$adapter_evidence" != not-required ) ]]; then
    actual=typed-invalid
  elif [[ "$boundary" == missing ||
          "$core_evidence" == missing ||
          "$capability" == unavailable ||
          ( "$adapter_required" == yes &&
            "$adapter_evidence" == missing ) ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$DECISIONS"

[[ "$(awk -F '\t' '$1 == "STD-0804" { count++ } END { print count + 0 }' \
  "$INVENTORY")" -eq 1 ]]
awk -F '\t' '
  NR > 1 && $1 == "STD-0804" {
    count += 1
    if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
        $3 != "profiles/languages/rust/language-bindings.md" ||
        $4 != "refine" || $5 == "" || NF != 5) {
      exit 1
    }
  }
  END { exit count != 1 }
' "$DISPOSITIONS"

required_profile=(
  'Core and adapter evidence are independent obligations'
  'domain behavior and validated native types'
  'selected real native/host boundary'
  'native-only adapter test does not prove host behavior'
  'core remains framework-independent'
  'separately provisioned verification environment'
  'does not permit excluding the adapter evidence'
  'typed `invalid`'
  'typed `unavailable`'
  'skip framework-free core verification'
  'select another binding framework'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_section="$(
  sed -n '/^### NIF Pure-Logic Separation$/,/^---$/p' \
    "$LEGACY"
)"
rg -F -q \
  'language-bindings.md#verification' <<< "$legacy_section"
rg -F -q \
  'Rustler/NIF is one possible selected adapter' <<< "$legacy_section"
for removed in \
  'fn parse_model_type_impl' \
  '#[rustler::nif]' \
  'ElixirModelType::Unknown' \
  'test_parse_model_type'; do
  ! rg -F -q "$removed" <<< "$legacy_section"
done

rg -F -q '`7.4b8o` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8p` (`Planned`)' "$PLAN"
"$SCRIPT_DIR/verify-rust-binding-architecture.sh"
"$SCRIPT_DIR/verify-rust-binding-conversions.sh"
"$SCRIPT_DIR/verify-milestone-7-row-5-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Rust binding core/adapter testability passed: %s decisions, 1 exact disposition\n' \
  "$(( $(wc -l < "$DECISIONS") - 1 ))"
