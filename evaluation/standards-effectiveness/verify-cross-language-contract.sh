#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/contracts/cross-language-contract-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly CONTRACTS="$REPO_ROOT/topics/contracts.md"
readonly LEGACY="$REPO_ROOT/INTEROP-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

count=0
while IFS=$'\t' read -r case_id contract_class authority deployment \
  producer_update consumer_update version evidence fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ "$contract_class" =~ ^(internal-coordinated|persisted|public-versioned|distributed-independent|generated)$ ]]
  [[ "$authority" =~ ^(selected|missing|ambiguous)$ ]]
  [[ "$deployment" =~ ^(atomic|independent)$ ]]
  [[ "$producer_update" =~ ^(complete|incomplete)$ ]]
  [[ "$consumer_update" =~ ^(complete|incomplete)$ ]]
  [[ "$version" =~ ^(supported|unsupported|not-applicable)$ ]]
  [[ "$evidence" =~ ^(matched|missing)$ ]]
  [[ "$fallback" =~ ^(none|guess-schema|old-shape|dual-shape|default)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ]]; then
    actual=typed-invalid
  elif [[ "$authority" != selected ]]; then
    actual=typed-unavailable
  elif [[ "$version" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$producer_update" != complete ||
          "$consumer_update" != complete ||
          "$evidence" != matched ]]; then
    actual=typed-invalid
  elif [[ "$contract_class" =~ ^(internal-coordinated|generated)$ &&
          "$deployment" != atomic ]]; then
    actual=typed-invalid
  elif [[ "$contract_class" =~ ^(persisted|public-versioned|distributed-independent)$ &&
          "$version" != supported ]]; then
    actual=typed-invalid
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
[[ "$count" -eq 16 ]]

for id in STD-0474 STD-0475 STD-0477 STD-0481; do
  [[ "$(awk -F '\t' -v id="$id" '$1 == id { count++ } END { print count + 0 }' \
    "$INVENTORY")" -eq 1 ]]
  awk -F '\t' -v id="$id" '
    NR > 1 && $1 == id {
      count += 1
      if ($2 != "INTEROP-STANDARDS.md" ||
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
  '## Cross-Language Contract Selection'
  'one canonical authority'
  'serializer defaults'
  '`internal-coordinated`'
  '`distributed-independent`'
  'consumer evidence'
  'Return `unavailable`'
  '`unsupported`'
  'try a second shape'
)
for text in "${required_contract_text[@]}"; do
  rg -F -q "$text" "$CONTRACTS"
done

validate_head="$(git -C "$REPO_ROOT" show HEAD:INTEROP-STANDARDS.md |
  sed -n '/^### Validate Received Messages/,/^---/p')"
validate_current="$(sed -n '/^### Validate Received Messages/,/^---/p' "$LEGACY")"
applicability_head="$(git -C "$REPO_ROOT" show HEAD:INTEROP-STANDARDS.md |
  sed -n '/^## When These Rules Apply/,$p')"
applicability_current="$(sed -n '/^## When These Rules Apply/,$p' "$LEGACY")"
[[ "$validate_current" == "$validate_head" ]]
[[ "$applicability_current" == "$applicability_head" ]]

[[ "$(rg -c 'topics/contracts.md#cross-language-contract-selection' \
  "$LEGACY")" -eq 2 ]]
[[ "$(rg -c \
  'profiles/boundaries/language-bindings.md#serialized-wire-representation' \
  "$LEGACY")" -eq 3 ]]
for pattern in \
  'Use shared schema files when possible' \
  'Update coordinated sides in the same commit' \
  'indefinite backward compatibility'; do
  ! rg -F -q "$pattern" "$LEGACY"
done

rg -F -q '`7.4b8c` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-contract-ownership.sh"
"$SCRIPT_DIR/verify-runtime-decoding-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
printf 'Cross-language contract policy passed: %s decisions, 4 exact dispositions\n' \
  "$count"
