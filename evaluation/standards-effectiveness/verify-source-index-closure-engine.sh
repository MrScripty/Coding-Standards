#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly ENGINE="$SCRIPT_DIR/check-source-index-closure.sh"
readonly FIXTURES="$SCRIPT_DIR/fixtures/source-index-engine"
readonly VALID_REPO="$FIXTURES/valid/repo"
readonly VALID_SOURCE="$FIXTURES/valid/source"

"$ENGINE" "$VALID_REPO" "$VALID_SOURCE"

assert_rejected() {
  local expected="$1"
  local mutation="$2"
  local case_root
  local output
  case_root="$(mktemp -d)"
  cp -R "$VALID_REPO" "$case_root/repo"
  cp -R "$VALID_SOURCE" "$case_root/source"
  local case_source="$case_root/repo/languages/rust/LEGACY.md"

  case "$mutation" in
    malformed-contract)
      sed -i '1s/value/invalid/' "$case_root/source/contract.tsv"
      ;;
    malformed-routes)
      sed -i '1s/\thref//' "$case_root/source/routes.tsv"
      ;;
    duplicate-heading)
      printf '# Legacy Index\n' >> "$case_root/source/headings.tsv"
      ;;
    duplicate-route)
      printf 'owner_copy\tOWNER.md\t../../OWNER.md\n' >> \
        "$case_root/source/routes.tsv"
      ;;
    duplicate-href)
      printf 'router\tSTANDARDS-ROUTER.md\t../../OWNER.md\n' >> \
        "$case_root/source/routes.tsv"
      ;;
    unresolved-route)
      sed -i 's/\tOWNER.md\t/\tABSENT.md\t/' "$case_root/source/routes.tsv"
      ;;
    mismatched-href)
      sed -i 's#../../OWNER.md#../../STANDARDS-ROUTER.md#' \
        "$case_root/source/routes.tsv"
      ;;
    escaping-href)
      sed -i 's#../../OWNER.md#../../../OWNER.md#' \
        "$case_root/source/routes.tsv"
      ;;
    absent-href)
      sed -i 's#../../OWNER.md#../../STANDARDS-ROUTER.md#' "$case_source"
      ;;
    absent-manifest)
      sed -i '/languages\/rust\/LEGACY.md/d' \
        "$case_root/repo/evaluation/standards-effectiveness/milestone-7-final-source-closure.tsv"
      ;;
    normative-corpus)
      sed -i 's/\tderived\t/\tyes\t/' \
        "$case_root/repo/evaluation/standards-effectiveness/corpus.tsv"
      ;;
    legacy-authority)
      printf '\nThis file remains canonical.\n' >> "$case_source"
      ;;
    heading-drift)
      sed -i 's/## Routes/## Changed Routes/' "$case_source"
      ;;
    line-bound)
      sed -i 's/max_lines\t24/max_lines\t3/' "$case_root/source/contract.tsv"
      ;;
    count-disagreement)
      sed -i '$d' \
        "$case_root/repo/evaluation/standards-effectiveness/consolidation-dispositions.tsv"
      ;;
    *)
      printf 'unknown source-index mutation: %s\n' "$mutation" >&2
      exit 2
      ;;
  esac

  if output="$("$ENGINE" "$case_root/repo" "$case_root/source" 2>&1)"; then
    printf 'invalid source-index fixture passed: %s\n' "$mutation" >&2
    exit 1
  fi
  [[ "$output" == *"$expected"* ]] || {
    printf 'source-index diagnostic mismatch for %s: expected %s, got %s\n' \
      "$mutation" "$expected" "$output" >&2
    exit 1
  }
}

assert_rejected 'contract header must be: field<TAB>value' malformed-contract
assert_rejected 'routes header must be: route<TAB>target<TAB>href' malformed-routes
assert_rejected 'duplicate heading: # Legacy Index' duplicate-heading
assert_rejected 'duplicate route target: OWNER.md' duplicate-route
assert_rejected 'duplicate route href: ../../OWNER.md' duplicate-href
assert_rejected 'route target is unresolved: ABSENT.md' unresolved-route
assert_rejected 'route href does not resolve to target' mismatched-href
assert_rejected 'route href escapes the repository: ../../../OWNER.md' escaping-href
assert_rejected 'required route href is absent from languages/rust/LEGACY.md' absent-href
assert_rejected 'source is absent from the closure manifest: languages/rust/LEGACY.md' absent-manifest
assert_rejected 'corpus row remains normative for languages/rust/LEGACY.md: yes' normative-corpus
assert_rejected 'source retains prohibited authority text: This file remains canonical' legacy-authority
assert_rejected 'heading drift for languages/rust/LEGACY.md at position 2' heading-drift
assert_rejected 'line bound exceeded for languages/rust/LEGACY.md: maximum 3' line-bound
assert_rejected 'identifier counts disagree for languages/rust/LEGACY.md' count-disagreement

printf 'Source-index closure engine fixtures passed: 1 nested positive, 15 negative\n'
