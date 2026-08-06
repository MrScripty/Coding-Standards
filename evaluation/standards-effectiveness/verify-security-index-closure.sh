#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
DISPOSITIONS="$S/consolidation-dispositions.tsv"
LEGACY="$R/SECURITY-STANDARDS.md"

[[ "$(awk -F '\t' '$1 == "STD-0582" { print $2 FS $3 FS $4 }' "$DISPOSITIONS")" == $'SECURITY-STANDARDS.md\ttopics/security.md\tindex' ]]
[[ "$(awk -F '\t' '$1 == "STD-0582" { n++ } END { print n+0 }' "$DISPOSITIONS")" -eq 1 ]]

for text in '# Security Standards' \
  'topics/contracts.md#validation-proof-lifetime' \
  'topics/security.md#filesystem-containment' \
  'topics/security.md#input-validation-authority' \
  'topics/security.md#untrusted-structured-input' \
  'profiles/boundaries/ipc.md' \
  'topics/security.md#network-transport-boundary' \
  'topics/concurrency.md#own-work-failure-and-cancellation'; do
  rg -F -q "$text" "$LEGACY"
done

for prohibited in 'PathValidator' 'InputValidator' 'SafeNamePattern' \
  '127.0.0.1' '0.0.0.0' 'Runtime type check before cast' \
  'single implementation'; do
  if rg -F -q "$prohibited" "$LEGACY"; then
    printf 'invalid: legacy Security mechanism remains: %s\n' "$prohibited" >&2
    exit 1
  fi
done

"$S/verify-validation-proof-lifetime.sh"
"$S/verify-filesystem-containment-policy.sh"
"$S/verify-input-validation-authority.sh"
"$S/verify-ipc-payload-validation.sh"
"$S/verify-network-transport-policy.sh"
"$S/verify-milestone-7-row-42-decomposition.sh"
printf 'Security index closure passed: 1 exact disposition, canonical routes preserved, P34 closed\n'
