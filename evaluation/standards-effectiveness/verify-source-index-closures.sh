#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly ENGINE="$SCRIPT_DIR/check-source-index-closure.sh"
readonly FIXTURE_ROOT="$SCRIPT_DIR/fixtures/source-closure"
readonly MANIFEST="$SCRIPT_DIR/milestone-7-final-source-closure.tsv"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

fail() {
  printf 'invalid source-index registry: %s\n' "$1" >&2
  exit 1
}

[[ -x "$ENGINE" ]] || fail "engine is unavailable: $ENGINE"
[[ -d "$FIXTURE_ROOT" ]] || fail "fixture root is unavailable: $FIXTURE_ROOT"
[[ -f "$MANIFEST" ]] || fail "closure manifest is unavailable: $MANIFEST"

mapfile -t loose_files < <(find "$FIXTURE_ROOT" -mindepth 1 -maxdepth 1 -type f -print | sort)
[[ "${#loose_files[@]}" -eq 0 ]] || \
  fail "fixture root contains unregistered file: ${loose_files[0]}"
mapfile -t fixture_dirs < <(find "$FIXTURE_ROOT" -mindepth 1 -maxdepth 1 -type d -print | sort)
[[ "${#fixture_dirs[@]}" -gt 0 ]] || fail 'no source fixture directories are registered'

declare -A fixtures_by_source
for fixture_dir in "${fixture_dirs[@]}"; do
  mapfile -t fixture_entries < <(
    find "$fixture_dir" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort
  )
  expected_entries=(contract.tsv headings.tsv prohibited.tsv routes.tsv)
  [[ "${fixture_entries[*]}" == "${expected_entries[*]}" ]] || \
    fail "fixture directory has an unknown or missing entry: $fixture_dir"
  for name in contract.tsv headings.tsv routes.tsv prohibited.tsv; do
    [[ -f "$fixture_dir/$name" ]] || \
      fail "fixture directory is partial: $fixture_dir lacks $name"
  done
  source="$(awk -F '\t' '$1 == "source" { print $2 }' "$fixture_dir/contract.tsv")"
  [[ -n "$source" && "$source" != *$'\n'* ]] || \
    fail "fixture contract has no unique source: $fixture_dir"
  [[ -z "${fixtures_by_source[$source]:-}" ]] || \
    fail "source has duplicate fixture directories: $source"
  fixtures_by_source["$source"]="$fixture_dir"
done

registered_count=0
while IFS=$'\t' read -r _order source _owner _shape _treatment _evidence \
  _risk _concurrency _gate extra; do
  [[ "$source" == source ]] && continue
  [[ -z "${extra:-}" ]] || fail "closure manifest row has extra fields: $source"
  fixture_dir="${fixtures_by_source[$source]:-}"
  [[ -z "$fixture_dir" ]] && continue
  "$ENGINE" "$REPO_ROOT" "$fixture_dir"
  registered_count=$((registered_count + 1))
done < "$MANIFEST"

[[ "$registered_count" -eq "${#fixture_dirs[@]}" ]] || \
  fail "registered source count disagrees with manifest order: fixtures ${#fixture_dirs[@]}, verified $registered_count"
rg -F -q '`7.4c3v1` (`Accepted`)' "$PLAN" || \
  fail 'implementation acceptance is absent for milestone 7.4c3v1'

printf 'Source-index aggregate passed: %s registered source(s)\n' "$registered_count"
