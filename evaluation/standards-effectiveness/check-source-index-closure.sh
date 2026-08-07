#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 2 ]]; then
  printf 'usage: %s REPO_ROOT FIXTURE_DIR\n' "$0" >&2
  exit 2
fi

readonly REPO_ROOT="$1"
readonly FIXTURE_DIR="$2"
readonly EVALUATION="$REPO_ROOT/evaluation/standards-effectiveness"
readonly CONTRACT="$FIXTURE_DIR/contract.tsv"
readonly HEADINGS="$FIXTURE_DIR/headings.tsv"
readonly ROUTES="$FIXTURE_DIR/routes.tsv"
readonly PROHIBITED="$FIXTURE_DIR/prohibited.tsv"
readonly MANIFEST="$EVALUATION/milestone-7-final-source-closure.tsv"
readonly CORPUS="$EVALUATION/corpus.tsv"
readonly OWNER_MAP="$EVALUATION/generated/rule-owner-map.tsv"
readonly DISPOSITIONS="$EVALUATION/consolidation-dispositions.tsv"
readonly ROUTER="$REPO_ROOT/STANDARDS-ROUTER.md"

fail() {
  printf 'invalid source-index closure: %s\n' "$1" >&2
  exit 1
}

for file in "$CONTRACT" "$HEADINGS" "$ROUTES" "$PROHIBITED" \
  "$MANIFEST" "$CORPUS" "$OWNER_MAP" "$DISPOSITIONS" "$ROUTER"; do
  [[ -f "$file" ]] || fail "required input is unavailable: $file"
done

declare -A contract_fields
contract_count=0
contract_line=0
while IFS=$'\t' read -r field value extra; do
  contract_line=$((contract_line + 1))
  if [[ "$contract_line" -eq 1 ]]; then
    [[ "$field" == field ]] || fail 'contract header must be: field<TAB>value'
    [[ "$value" == value && -z "${extra:-}" ]] || \
      fail 'contract header must be: field<TAB>value'
    continue
  fi
  [[ -n "$field" && -n "$value" && -z "${extra:-}" ]] || \
    fail 'contract rows require exactly field and value'
  [[ -z "${contract_fields[$field]:-}" ]] || \
    fail "duplicate contract field: $field"
  case "$field" in
    source|title|max_lines) ;;
    *) fail "unknown contract field: $field" ;;
  esac
  contract_fields["$field"]="$value"
  contract_count=$((contract_count + 1))
done < "$CONTRACT"

[[ "$contract_count" -eq 3 ]] || fail 'contract requires source, title, and max_lines'
for field in source title max_lines; do
  [[ -n "${contract_fields[$field]:-}" ]] || fail "missing contract field: $field"
done
[[ "${contract_fields[max_lines]}" =~ ^[1-9][0-9]*$ ]] || \
  fail 'max_lines must be a positive integer'

readonly SOURCE="${contract_fields[source]}"
readonly TITLE="${contract_fields[title]}"
readonly MAX_LINES="${contract_fields[max_lines]}"
readonly SOURCE_FILE="$REPO_ROOT/$SOURCE"

[[ "$SOURCE" != /* && "$SOURCE" != *'../'* && "$SOURCE" != '../'* ]] || \
  fail "source path escapes the repository: $SOURCE"
[[ -f "$SOURCE_FILE" ]] || fail "source is unavailable: $SOURCE"

manifest_result="$({
  awk -F '\t' -v source="$SOURCE" '
    NR == 1 {
      if ($0 != "order\tsource\tcanonical_owner\tcurrent_shape\ttreatment\tretention_evidence\trisk\tconcurrency\tgate") {
        invalid_header = 1
      }
      next
    }
    NF != 9 { invalid_row = 1 }
    $2 == source {
      count += 1
      owner = $3
      shape = $4
      treatment = $5
    }
    END {
      if (invalid_header) {
        print "invalid-header"
      } else if (invalid_row) {
        print "invalid-row"
      } else if (count == 1) {
        print "valid\t" owner "\t" shape "\t" treatment
      } else if (count == 0) {
        print "absent"
      } else {
        print "duplicate"
      }
    }
  ' "$MANIFEST"
})"
case "$manifest_result" in
  invalid-header) fail 'closure manifest header is invalid' ;;
  invalid-row) fail 'closure manifest contains a malformed row' ;;
  absent) fail "source is absent from the closure manifest: $SOURCE" ;;
  duplicate) fail "source has duplicate closure manifest rows: $SOURCE" ;;
  valid$'\t'*) ;;
  *) fail "closure manifest result is malformed for: $SOURCE" ;;
esac
IFS=$'\t' read -r _valid owner shape treatment <<< "$manifest_result"
[[ -n "$owner" && -f "$REPO_ROOT/$owner" ]] || \
  fail "canonical owner is unavailable for $SOURCE: $owner"
[[ "$shape" == concise || "$shape" == expanded ]] || \
  fail "closure manifest shape is invalid for $SOURCE: $shape"
[[ "$treatment" == retain-index || "$treatment" == rewrite-index ]] || \
  fail "closure manifest treatment is invalid for $SOURCE: $treatment"

corpus_result="$({
  awk -F '\t' -v source="$SOURCE" '
    NR == 1 {
      if ($0 != "path\tkind\tnormative\ttarget_role\tpreliminary_disposition\tbaseline_source") {
        invalid_header = 1
      }
      next
    }
    NF != 6 { invalid_row = 1 }
    $1 == source {
      count += 1
      kind = $2
      normative = $3
      role = $4
      disposition = $5
      baseline = $6
      width = NF
    }
    END {
      if (invalid_header) {
        print "invalid-header"
      } else if (invalid_row) {
        print "invalid-row"
      } else if (count == 1) {
        print "valid\t" kind "\t" normative "\t" role "\t" disposition "\t" baseline "\t" width
      } else if (count == 0) {
        print "absent"
      } else {
        print "duplicate"
      }
    }
  ' "$CORPUS"
})"
case "$corpus_result" in
  invalid-header) fail 'corpus header is invalid' ;;
  invalid-row) fail 'corpus contains a malformed row' ;;
  absent) fail "source is absent from the corpus: $SOURCE" ;;
  duplicate) fail "source has duplicate corpus rows: $SOURCE" ;;
  valid$'\t'*) ;;
  *) fail "corpus result is malformed for: $SOURCE" ;;
esac
IFS=$'\t' read -r _valid kind normative target_role disposition baseline width \
  <<< "$corpus_result"
[[ "$width" -eq 6 && -n "$kind" && -n "$target_role" && \
  -n "$disposition" && -n "$baseline" ]] || \
  fail "corpus row is incomplete for: $SOURCE"
[[ "$normative" == derived ]] || \
  fail "corpus row remains normative for $SOURCE: $normative"

declare -a expected_headings=()
declare -A seen_headings
heading_line=0
while IFS=$'\t' read -r heading extra; do
  heading_line=$((heading_line + 1))
  if [[ "$heading_line" -eq 1 ]]; then
    [[ "$heading" == heading ]] || fail 'headings header must be: heading'
    [[ -z "${extra:-}" ]] || fail 'headings header must be: heading'
    continue
  fi
  [[ -n "$heading" && -z "${extra:-}" ]] || \
    fail 'heading rows require exactly one value'
  [[ -z "${seen_headings[$heading]:-}" ]] || fail "duplicate heading: $heading"
  seen_headings["$heading"]=1
  expected_headings+=("$heading")
done < "$HEADINGS"
[[ "${#expected_headings[@]}" -gt 0 ]] || fail 'headings table has no rows'
[[ "${expected_headings[0]}" == "$TITLE" ]] || \
  fail 'contract title does not match the first expected heading'

mapfile -t observed_headings < <(rg '^#{1,6} ' "$SOURCE_FILE" || true)
[[ "${#observed_headings[@]}" -eq "${#expected_headings[@]}" ]] || \
  fail "heading count drift for $SOURCE: expected ${#expected_headings[@]}, observed ${#observed_headings[@]}"
for index in "${!expected_headings[@]}"; do
  [[ "${observed_headings[$index]}" == "${expected_headings[$index]}" ]] || \
    fail "heading drift for $SOURCE at position $((index + 1))"
done

line_count="$(wc -l < "$SOURCE_FILE")"
[[ "$line_count" -le "$MAX_LINES" ]] || \
  fail "line bound exceeded for $SOURCE: maximum $MAX_LINES, observed $line_count"

declare -A seen_route_names seen_route_targets
route_count=0
route_line=0
while IFS=$'\t' read -r route target extra; do
  route_line=$((route_line + 1))
  if [[ "$route_line" -eq 1 ]]; then
    [[ "$route" == route ]] || fail 'routes header must be: route<TAB>target'
    [[ "$target" == target && -z "${extra:-}" ]] || \
      fail 'routes header must be: route<TAB>target'
    continue
  fi
  [[ -n "$route" && -n "$target" && -z "${extra:-}" ]] || \
    fail 'route rows require exactly route and target'
  [[ -z "${seen_route_names[$route]:-}" ]] || fail "duplicate route: $route"
  [[ -z "${seen_route_targets[$target]:-}" ]] || \
    fail "duplicate route target: $target"
  target_path="${target%%#*}"
  [[ -n "$target_path" && "$target_path" != /* && \
    "$target_path" != *'../'* && "$target_path" != '../'* ]] || \
    fail "route target escapes the repository: $target"
  [[ -f "$REPO_ROOT/$target_path" ]] || fail "route target is unresolved: $target"
  rg -F -q "($target)" "$SOURCE_FILE" || \
    fail "required route is absent from $SOURCE: $target"
  seen_route_names["$route"]=1
  seen_route_targets["$target"]=1
  route_count=$((route_count + 1))
done < "$ROUTES"
[[ "$route_count" -gt 0 ]] || fail 'routes table has no rows'

declare -A seen_prohibited
prohibited_count=0
prohibited_line=0
while IFS=$'\t' read -r literal extra; do
  prohibited_line=$((prohibited_line + 1))
  if [[ "$prohibited_line" -eq 1 ]]; then
    [[ "$literal" == literal ]] || fail 'prohibited header must be: literal'
    [[ -z "${extra:-}" ]] || fail 'prohibited header must be: literal'
    continue
  fi
  [[ -n "$literal" && -z "${extra:-}" ]] || \
    fail 'prohibited rows require exactly one literal'
  [[ -z "${seen_prohibited[$literal]:-}" ]] || \
    fail "duplicate prohibited literal: $literal"
  if rg -F -q "$literal" "$SOURCE_FILE"; then
    fail "source retains prohibited authority text: $literal"
  fi
  seen_prohibited["$literal"]=1
  prohibited_count=$((prohibited_count + 1))
done < "$PROHIBITED"
[[ "$prohibited_count" -gt 0 ]] || fail 'prohibited table has no rows'

for required in 'non-normative navigation' 'owns no' 'fallback authority' \
  "Router's typed" 'instead of using prior wording'; do
  rg -F -q "$required" "$SOURCE_FILE" || \
    fail "source lacks required non-authority text: $required"
done
for generic_prohibited in 'Migration authority' 'remains canonical only' \
  'This file remains canonical' 'Conflicts for moved rules' 'not yet moved' \
  'Existing files retain authority'; do
  if rg -F -q "$generic_prohibited" "$SOURCE_FILE"; then
    fail "source retains generic legacy authority: $generic_prohibited"
  fi
done

owner_count="$({
  awk -F '\t' -v source="$SOURCE" '
    NR == 1 && $0 != "id\tcurrent_path\tline\tfuture_owner\tdisposition\theading" {
      print "invalid-header"
      exit
    }
    NR > 1 && $2 == source { count += 1 }
    END { if (NR > 0) print count + 0 }
  ' "$OWNER_MAP"
})"
[[ "$owner_count" != *invalid-header* ]] || fail 'owner-map header is invalid'
disposition_count="$({
  awk -F '\t' -v source="$SOURCE" '
    NR == 1 && $0 != "id\tsource\ttarget\tdisposition\trationale" {
      print "invalid-header"
      exit
    }
    NR > 1 && $2 == source { count += 1 }
    END { if (NR > 0) print count + 0 }
  ' "$DISPOSITIONS"
})"
[[ "$disposition_count" != *invalid-header* ]] || \
  fail 'disposition header is invalid'
[[ "$owner_count" -gt 0 && "$owner_count" -eq "$disposition_count" ]] || \
  fail "identifier counts disagree for $SOURCE: owner-map $owner_count, dispositions $disposition_count"

if rg -F -q "$SOURCE" "$ROUTER"; then
  fail "Router selects former normative source: $SOURCE"
fi

printf 'Source-index closure passed: %s, %s routes, %s frozen IDs, owner %s\n' \
  "$SOURCE" "$route_count" "$owner_count" "$owner"
