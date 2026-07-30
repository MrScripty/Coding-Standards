#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE_DIR="$SCRIPT_DIR/fixtures/contracts"
readonly SCHEMA="$FIXTURE_DIR/binding-evolution-schema.tsv"
readonly DECISIONS="$FIXTURE_DIR/binding-evolution-decisions.tsv"
readonly OBSERVED="$FIXTURE_DIR/binding-evolution-observed.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly CONTRACTS="$REPO_ROOT/topics/contracts.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

"$SCRIPT_DIR/check-decision-table.sh" "$SCHEMA" "$DECISIONS" "$OBSERVED"

while IFS=$'\t' read -r case_id class deployment change generator_input \
  version_relation evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$version_relation" =~ ^forced- ||
        ( "$class" == internal-coordinated && "$deployment" != atomic ) ||
        ( "$class" == generated && "$generator_input" == not-applicable ) ]]; then
    actual=typed-invalid
  elif [[ "$change" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$version_relation" == missing || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    case "$class:$generator_input" in
      internal-coordinated:*) actual=replace ;;
      persisted:*) actual=migrate ;;
      public-versioned:*) actual=version ;;
      distributed-independent:*) actual=negotiate ;;
      generated:changed) actual=regenerate ;;
      generated:unchanged) actual=no-regeneration ;;
    esac
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$DECISIONS"

expected_ids=(STD-0767 STD-0807 STD-0808)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $1 == "STD-0767" || $1 == "STD-0807" || $1 == "STD-0808" { print $1 }
  ' "$INVENTORY" | sort
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && ($1 == "STD-0767" || $1 == "STD-0807" || $1 == "STD-0808") {
      print $1
    }
  ' "$DISPOSITIONS" | sort
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0767|STD-0807|STD-0808)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:topics/contracts.md:refine' ]]
      [[ -n "$rationale" && -z "${extra:-}" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

required_contracts=(
  'classify each affected artifact independently'
  'canonical generator input'
  'shared release input'
  'Common build or release provenance'
  'does not select a compatibility class'
  'Regenerate only affected outputs'
  'private implementation change does not require'
  'derive every affected output deterministically'
  'Select shared or independent artifact versions'
  'force native libraries and host packages into'
  'syntactically additive change is compatible only'
  'exhaustive variants'
)
for text in "${required_contracts[@]}"; do
  rg -F -q "$text" "$CONTRACTS"
done

compatibility_section="$(
  sed -n '/^### Compatibility Notes$/,/^---$/p' "$LEGACY"
)"
rg -F -q 'topics/contracts.md#cross-language-contract-selection' \
  <<< "$compatibility_section"
rg -F -q 'does not impose one compatibility promise' \
  <<< "$compatibility_section"
for removed in \
  'Product-facing naming may differ' \
  'If a native library name or generated package name changes' \
  'Binding packages should state whether'; do
  ! rg -F -q "$removed" <<< "$compatibility_section"
done

legacy_section="$(
  sed -n '/^## Versioning and Compatibility$/,/^### Version Export$/p' "$LEGACY"
)"
rg -F -q 'topics/contracts.md#cross-language-contract-selection' \
  <<< "$legacy_section"
for removed in \
  'Re-generate bindings after every API change' \
  'Classify each boundary independently' \
  'Use coordinated replacement only' \
  '### Rules'; do
  ! rg -F -q "$removed" <<< "$legacy_section"
done

rg -F -q '`7.4b8q` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-contract-decisions.sh"
"$SCRIPT_DIR/verify-contract-ownership.sh"
"$SCRIPT_DIR/verify-milestone-7-row-5-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Binding contract evolution passed: %s decisions, 3 exact dispositions\n' \
  "$(( $(wc -l < "$DECISIONS") - 1 ))"
