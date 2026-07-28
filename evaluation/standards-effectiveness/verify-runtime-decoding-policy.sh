#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/contracts/runtime-decoding-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly CONTRACTS="$REPO_ROOT/topics/contracts.md"
readonly LEGACY="$REPO_ROOT/ARCHITECTURE-PATTERNS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id applicability input_trust decoder_status \
  invariant_coverage normalization version construction expected; do
  [[ "$case_id" == 'case' ]] && continue

  [[ "$applicability" =~ ^(boundary|internal)$ ]]
  [[ "$input_trust" =~ ^(unknown|validated)$ ]]
  [[ "$decoder_status" =~ ^(success|failure|unavailable|not-required)$ ]]
  [[ "$invariant_coverage" =~ ^(complete|partial|not-required)$ ]]
  [[ "$normalization" =~ ^(valid|invalid|not-required)$ ]]
  [[ "$version" =~ ^(supported|unsupported|not-versioned)$ ]]
  [[ "$construction" =~ ^(decoder|assertion|original|none)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]

  if [[ "$applicability" == 'internal' ]]; then
    if [[ "$input_trust" == 'validated' &&
          "$decoder_status" == 'not-required' &&
          "$invariant_coverage" == 'not-required' &&
          "$normalization" == 'not-required' &&
          "$version" == 'not-versioned' &&
          "$construction" == 'none' ]]; then
      actual='allow'
    else
      actual='typed-invalid'
    fi
  elif [[ "$decoder_status" == 'unavailable' ]]; then
    actual='typed-unavailable'
  elif [[ "$version" == 'unsupported' ]]; then
    actual='typed-unsupported'
  elif [[ "$decoder_status" != 'success' ||
          "$invariant_coverage" != 'complete' ||
          "$normalization" == 'invalid' ||
          "$construction" != 'decoder' ]]; then
    actual='typed-invalid'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

expected_ids=(STD-0051 STD-0052 STD-0053 STD-0054)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $2 == "ARCHITECTURE-PATTERNS.md" &&
    $1 >= "STD-0051" && $1 <= "STD-0054" {
      print $1
    }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 &&
    $2 == "ARCHITECTURE-PATTERNS.md" &&
    $1 >= "STD-0051" && $1 <= "STD-0054" {
      print $1
    }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0051)
      [[ "$source:$target:$disposition" == \
        'ARCHITECTURE-PATTERNS.md:topics/contracts.md:merge' ]]
      ;;
    STD-0052|STD-0053|STD-0054)
      [[ "$source:$target:$disposition" == \
        'ARCHITECTURE-PATTERNS.md:topics/contracts.md:refine' ]]
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
  "$CONTRACTS"

required_contracts=(
  '## Runtime Decoding At Boundaries'
  'A validated value is a construction result, not a type annotation.'
  'Before constructing a validated value, check every invariant required by that'
  'type assertion, generic object check'
  '`invalid` for malformed data'
  '`unsupported` for a well-formed version'
  '`unavailable` when required decoding capability'
  'Do not fall back to a cast'
  'kept inside one trusted in-process boundary'
)
for text in "${required_contracts[@]}"; do
  rg -F -q "$text" "$CONTRACTS"
done

rg -F -q \
  'topics/contracts.md#runtime-decoding-at-boundaries' "$LEGACY"
legacy_runtime="$(
  awk '
    /^## Executable Boundary Contracts$/ { capture = 1 }
    /^### Packaging Guidance$/ { capture = 0 }
    capture { print }
  ' "$LEGACY"
)"
if rg -q '^### |```|input as CreateJobRequest|throws/returns error if invalid' \
  <<< "$legacy_runtime"; then
  printf 'legacy executable-contract policy remains active\n' >&2
  exit 1
fi

removed_patterns=(
  'input as CreateJobRequest'
  'runtime input is trusted blindly'
  'Validate once at the boundary, then pass validated values inward.'
)
for pattern in "${removed_patterns[@]}"; do
  if rg -F -q "$pattern" "$CONTRACTS" "$LEGACY"; then
    printf 'unsafe runtime-decoding guidance remains: %s\n' "$pattern" >&2
    exit 1
  fi
done

rg -F -q '`7.4b2b` (`Accepted`)' "$PLAN"

printf 'Runtime decoding policy passed\n'
