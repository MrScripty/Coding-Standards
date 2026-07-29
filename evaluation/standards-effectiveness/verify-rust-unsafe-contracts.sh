#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/unsafe-contract-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/unsafe.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-UNSAFE-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id operation caller module wrapper verification \
  feature expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$operation" =~ ^(complete|incomplete|absent)$ ]]
  [[ "$caller" =~ ^(complete|incomplete|absent|not-required)$ ]]
  [[ "$module" =~ ^(complete|incomplete|absent|not-required)$ ]]
  [[ "$wrapper" =~ ^(valid|overclaims)$ ]]
  [[ "$verification" =~ ^(selected|unavailable|alternate-only|not-run)$ ]]
  [[ "$feature" =~ ^(direct|disabled-only|safe-default-only|not-applicable)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|evidence-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$operation" != 'complete' ||
        "$caller" == 'incomplete' ||
        "$caller" == 'absent' ||
        "$module" == 'incomplete' ||
        "$module" == 'absent' ||
        "$wrapper" != 'valid' ||
        "$verification" == 'alternate-only' ||
        "$verification" == 'not-run' ||
        "$feature" == 'disabled-only' ||
        "$feature" == 'safe-default-only' ]]; then
    actual='typed-invalid'
  elif [[ "$verification" == 'unavailable' ]]; then
    actual='evidence-unavailable'
  else
    actual='allow'
  fi

  if [[ "$actual" != "$expected" ]]; then
    printf '%s: expected %s, derived %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  fi
done < "$FIXTURE"

expected_ids=(STD-0843 STD-0844 STD-0845 STD-0846 STD-0847 STD-0848)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $2 == "languages/rust/RUST-UNSAFE-STANDARDS.md" &&
    $1 >= "STD-0843" && $1 <= "STD-0848" { print $1 }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && $2 == "languages/rust/RUST-UNSAFE-STANDARDS.md" &&
    $1 >= "STD-0843" && $1 <= "STD-0848" { print $1 }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0843)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-UNSAFE-STANDARDS.md:profiles/languages/rust/unsafe.md:move' ]]
      ;;
    STD-0844|STD-0845|STD-0846|STD-0847|STD-0848)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-UNSAFE-STANDARDS.md:profiles/languages/rust/unsafe.md:refine' ]]
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
  "$RUST_INDEX" \
  "$PROFILE"

required_profile=(
  '## Deny By Default'
  '## Adjacent Operation Proof'
  'adjacent `SAFETY:` rationale'
  '## Caller Contracts'
  'public `unsafe fn`'
  '## Module Invariants'
  '## Mechanism-Selected Verification'
  'keep the acceptance claim partial or blocked'
  '## Feature-Gated Unsafe Paths'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

rg -F -q '(unsafe.md)' "$RUST_INDEX"
rg -F -q 'profiles/languages/rust/unsafe.md' "$LEGACY"

if rg -q '^##|```|unsafe_code|SAFETY:|# Safety|Miri|Valgrind|ASan' "$LEGACY"; then
  printf 'legacy Rust unsafe guidance remains active\n' >&2
  exit 1
fi

rg -F -q '| F023 | Resolved in Milestone 7.4b3f |' "$FINDINGS"
rg -F -q '`7.4b3f` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-f022-f023-decomposition.sh"

printf 'Rust unsafe contract policy passed\n'
