#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/contracts/validation-proof-lifetime-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly CONTRACTS="$REPO_ROOT/topics/contracts.md"
readonly LEGACY="$REPO_ROOT/SECURITY-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

count=0
while IFS=$'\t' read -r case_id representation contract mutation boundary \
  proof capability fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$representation" =~ ^(validated|smart|lost|unknown)$ ]]
  [[ "$contract" =~ ^(current|changed|unsupported)$ ]]
  [[ "$mutation" =~ ^(none|unchecked)$ ]]
  [[ "$boundary" =~ ^(same|new)$ ]]
  [[ "$proof" =~ ^(retained|missing|invalidated|not-applicable|history|stale)$ ]]
  [[ "$capability" =~ ^(available|missing)$ ]]
  [[ "$fallback" =~ ^(none|original-input|history-flag|stale-proof|mutable-alias|implicit-trust|permissive-default|weaker-decoder|redundant-decode)$ ]]
  [[ "$expected" =~ ^(allow|require-proof|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ]]; then
    actual=typed-invalid
  elif [[ "$capability" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$contract" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$representation" =~ ^(validated|smart)$ &&
          "$contract" == current && "$mutation" == none &&
          "$boundary" == same && "$proof" == retained ]]; then
    actual=allow
  elif [[ "$representation" == lost || "$mutation" == unchecked ||
          "$contract" == changed || "$boundary" == new ]]; then
    actual=require-proof
  else
    actual=typed-invalid
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
  ((count += 1))
done < "$FIXTURE"
[[ "$count" -eq 16 ]]

for id in STD-0583 STD-0601; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { count++ } END { print count + 0 }' \
    "$INVENTORY")" -eq 1 ]]
  awk -F '\t' -v id="$id" '
    NR > 1 && $1 == id {
      count += 1
      if ($2 != "SECURITY-STANDARDS.md" ||
          $3 != "topics/contracts.md" ||
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
  "$CONTRACTS"

required_contract_text=(
  '## Validation Proof Lifetime'
  'proof-bearing representation'
  'unchecked alias'
  'new trust, process, persistence, plugin, queue'
  'does not carry forward'
  'boolean validation flag'
  'typed `unavailable`'
  'redundant validation'
)
for text in "${required_contract_text[@]}"; do
  rg -F -q "$text" "$CONTRACTS"
done

prefix_head="$(git -C "$REPO_ROOT" show HEAD:SECURITY-STANDARDS.md |
  sed '/^## Core Principle: Validate Once, at the Boundary/,$d')"
prefix_current="$(sed '/^## Core Principle: Validate Once, at the Boundary/,$d' \
  "$LEGACY")"
middle_head="$(git -C "$REPO_ROOT" show HEAD:SECURITY-STANDARDS.md |
  sed -n '/^## Path Validation/,/^## What NOT to Validate/p' |
  sed '$d')"
middle_current="$(sed -n '/^## Path Validation/,/^## What NOT to Validate/p' \
  "$LEGACY" | sed '$d')"
[[ "$prefix_current" == "$prefix_head" && "$middle_current" == "$middle_head" ]]

core_section="$(sed -n \
  '/^## Core Principle: Validate Once, at the Boundary/,/^## Path Validation/p' \
  "$LEGACY")"
final_section="$(sed -n '/^## What NOT to Validate/,$p' "$LEGACY")"
for section in "$core_section" "$final_section"; do
  rg -F -q 'topics/contracts.md#validation-proof-lifetime' <<< "$section"
done
for pattern in 'External Input' 'Trust internally' 'ProcessFile'; do
  ! rg -F -q "$pattern" "$LEGACY"
done

rg -F -q '| F053 | Resolved in Milestone 7.4b7m |' "$FINDINGS"
rg -F -q '`7.4b7m` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-runtime-decoding-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-independent-trust-replan.sh"
printf 'Validation proof-lifetime policy passed: %s decisions, 2 exact dispositions\n' \
  "$count"
