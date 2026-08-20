#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE_DIR="$SCRIPT_DIR/fixtures/language-bindings"
readonly SCHEMA="$FIXTURE_DIR/mechanism-selection-schema.tsv"
readonly DECISIONS="$FIXTURE_DIR/mechanism-selection-decisions.tsv"
readonly OBSERVED="$FIXTURE_DIR/mechanism-selection-observed.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/boundaries/language-bindings.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"

"$SCRIPT_DIR/check-decision-table.sh" "$SCHEMA" "$DECISIONS" "$OBSERVED"

while IFS=$'\t' read -r case_id topology representation selection lifecycle \
  requirement capability evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]

  selection_mismatch=0
  if [[ "$topology" == process ]]; then
    [[ "$selection" == ipc ]] || selection_mismatch=1
  elif [[ "$selection" == ipc || "$selection" != "$representation" ]]; then
    selection_mismatch=1
  fi

  if [[ "$fallback" != none ||
        "$selection_mismatch" -eq 1 ||
        "$lifecycle" == mismatch ]]; then
    actual=typed-invalid
  elif [[ "$requirement" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$capability" == unavailable || "$evidence" == missing ]]; then
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

expected_ids=(STD-0805 STD-0806)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 == "STD-0805" || $1 == "STD-0806" { print $1 }' \
    "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && ($1 == "STD-0805" || $1 == "STD-0806") { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0805|STD-0806)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:profiles/boundaries/language-bindings.md:refine' ]]
      [[ -n "$rationale" && -z "${extra:-}" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

required_profile=(
  '## Select The Boundary Mechanism'
  'complete boundary contract'
  'host consumers, supported runtimes, and process topology'
  'failure-containment'
  'Use binding-framework lifting only'
  'Select a stable ABI only'
  'identity and exported operations'
  'Select serialization'
  'IPC boundary profile'
  'process transport is not a substitute'
  'Target-language count'
  'UI technology'
  'same domain contract only'
  'Return `invalid`'
  '`unsupported`'
  '`unavailable`'
  'Do not retry through another'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_section="$(
  sed -n '/^## Choosing a Binding Approach$/,/^---$/p' "$LEGACY"
)"
rg -F -q \
  'language-bindings.md#select-the-boundary-mechanism' <<< "$legacy_section"
for removed in \
  'Default to UniFFI' \
  'Use Rustler only' \
  'Use Tauri IPC' \
  'Use RPC when' \
  'Targeting 3+ languages' \
  '| Approach |'; do
  ! rg -F -q "$removed" <<< "$legacy_section"
done

"$SCRIPT_DIR/verify-language-binding-boundary.sh"
"$SCRIPT_DIR/verify-milestone-7-row-5-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Language binding mechanism selection passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$DECISIONS") - 1 ))"
