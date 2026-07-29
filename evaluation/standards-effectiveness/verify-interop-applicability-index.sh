#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly LEGACY="$REPO_ROOT/INTEROP-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

[[ "$(awk -F '\t' '$1 == "STD-0482" { count++ } END { print count + 0 }' \
  "$INVENTORY")" -eq 1 ]]
awk -F '\t' '
  NR > 1 && $1 == "STD-0482" {
    count += 1
    if ($2 != "INTEROP-STANDARDS.md" ||
        $3 != "INTEROP-STANDARDS.md" ||
        $4 != "index" || $5 == "" || NF != 5) {
      exit 1
    }
  }
  END { exit count != 1 }
' "$DISPOSITIONS"

index_section="$(sed -n '/^## When These Rules Apply/,$p' "$LEGACY")"
required_text=(
  'non-normative routing index'
  'one boundary can require multiple canonical owners'
  'profiles/boundaries/interop.md'
  'profiles/boundaries/ipc.md'
  'profiles/boundaries/language-bindings.md'
  'topics/contracts.md'
  'topics/security.md'
  'This index defines none of them.'
)
for text in "${required_text[@]}"; do
  rg -F -q "$text" <<< "$index_section"
done

for pattern in \
  '```' \
  'Key Concerns' \
  'Rust ↔ C' \
  'WebSocket, stdin/stdout' \
  'HTTP REST, gRPC' \
  'must ' \
  'always ' \
  'fallback' \
  'default'; do
  ! rg -i -F -q "$pattern" <<< "$index_section"
done

rg -F -q '`7.4b8f` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-interop-boundary-policy.sh"
"$SCRIPT_DIR/verify-ipc-payload-validation.sh"
"$SCRIPT_DIR/verify-language-binding-wire-representation.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"
printf 'Interop applicability index passed: 1 exact index disposition\n'
