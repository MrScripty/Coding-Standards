#!/usr/bin/env bash
set -euo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly EVALUATION="$ROOT/evaluation/standards-effectiveness"
readonly CHECK_METADATA="$EVALUATION/check-metadata.sh"
readonly EXPECTED="$EVALUATION/fixtures/routing/s1-rust-library.expected"
readonly SUMMARY="$EVALUATION/generated/summary.tsv"
readonly -a MODULES=(
  "$ROOT/CORE-STANDARDS.md"
  "$ROOT/STANDARDS-ROUTER.md"
  "$ROOT/workflows/implementation.md"
  "$ROOT/workflows/verification.md"
  "$ROOT/profiles/applications/library.md"
  "$ROOT/profiles/languages/rust/README.md"
)

"$CHECK_METADATA" "$ROOT" "${MODULES[@]}"

actual="$(mktemp)"
trap 'rm -f "$actual"' EXIT

for module in "${MODULES[@]}"; do
  sed -n 's/^- ID: `\([^`]*\)`.*/\1/p' "$module"
done | sort > "$actual"

diff -u "$EXPECTED" "$actual"

for module in "${MODULES[@]}"; do
  while IFS= read -r target; do
    case "$target" in
      http://*|https://*|mailto:*|"")
        continue
        ;;
    esac
    target="${target%%#*}"
    if [[ ! -e "$(dirname "$module")/$target" ]]; then
      printf '%s: missing link target %s\n' "$module" "$target" >&2
      exit 1
    fi
  done < <(
    rg -o '\]\([^)]+\)' "$module" |
      sed -e 's/^](//' -e 's/)$//'
  )
done

baseline_lines="$(
  awk -F '\t' '$1 == "normative_and_derived_lines" { print $2 }' "$SUMMARY"
)"
selected_lines="$(wc -l "${MODULES[@]}" | awk 'END { print $1 }')"

if (( selected_lines * 4 >= baseline_lines )); then
  printf 'S1 routed context is not below 25%%: %s/%s lines\n' \
    "$selected_lines" "$baseline_lines" >&2
  exit 1
fi

if rg -q 'Read each document' "$ROOT/README.md"; then
  printf 'Root README still requires a full-library read\n' >&2
  exit 1
fi

printf 'S1 route passed: %s modules, %s/%s baseline lines\n' \
  "${#MODULES[@]}" "$selected_lines" "$baseline_lines"
