#!/usr/bin/env bash
set -euo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly ARCHITECTURE="$ROOT/ARCHITECTURE-PATTERNS.md"
readonly RUST_BINDINGS="$ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly CONTRACTS="$ROOT/topics/contracts.md"

for file in \
  "$ROOT/README.md" \
  "$ROOT/CODING-STANDARDS.md" \
  "$ROOT/INTEROP-STANDARDS.md" \
  "$ROOT/LANGUAGE-BINDINGS-STANDARDS.md" \
  "$ROOT/workflows/release.md" \
  "$ARCHITECTURE" \
  "$RUST_BINDINGS"; do
  if [[ "$(grep -c 'topics/contracts.md' "$file")" -lt 1 ]]; then
    printf '%s: missing canonical contract link\n' "${file#"$ROOT"/}" >&2
    exit 1
  fi
done

grep -q 'workflows/release.md' "$ROOT/RELEASE-STANDARDS.md"

if rg -q \
  'Append-only changes|Additive changes are safe|Delete and rebuild from scratch|continue with defaults or degraded mode|Use cached fallback or return partial results|returns safe defaults' \
  "$ARCHITECTURE"; then
  printf 'ARCHITECTURE-PATTERNS.md retains conflicting contract/fallback policy\n' >&2
  exit 1
fi

if rg -q 'Additive changes are backward-compatible|Err\\(_\\) => self\\.host' \
  "$RUST_BINDINGS"; then
  printf 'Rust bindings retain blanket compatibility or catch-all fallback\n' >&2
  exit 1
fi

grep -q 'destructive replacement does not require a speculative' "$ARCHITECTURE"
grep -q 'return the selected typed unavailable, invalid, unsupported, or deferred' \
  "$ARCHITECTURE"
grep -q 'syntactically additive change is compatible only' "$CONTRACTS"
grep -q 'topics/contracts.md#cross-language-contract-selection' "$RUST_BINDINGS"

printf 'Contract ownership checks passed\n'
