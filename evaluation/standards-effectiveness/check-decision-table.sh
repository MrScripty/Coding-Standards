#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 3 ]]; then
  printf 'usage: %s SCHEMA DECISIONS OBSERVED\n' "$0" >&2
  exit 2
fi

readonly SCHEMA="$1"
readonly DECISIONS="$2"
readonly OBSERVED="$3"

for file in "$SCHEMA" "$DECISIONS" "$OBSERVED"; do
  [[ -f "$file" ]] || {
    printf 'decision table input is unavailable: %s\n' "$file" >&2
    exit 2
  }
done

awk -F '\t' -v schema="$SCHEMA" -v decisions="$DECISIONS" '
  function fail(message) {
    print message > "/dev/stderr"
    exit 1
  }

  function value_allowed(column, value, values, count, allowed_index) {
    if (domains[column] == "*") {
      return value != ""
    }
    count = split(domains[column], values, ",")
    for (allowed_index = 1; allowed_index <= count; allowed_index += 1) {
      if (values[allowed_index] == value) {
        return 1
      }
    }
    return 0
  }

  {
    sub(/\r$/, "", $NF)
  }

  FILENAME == schema {
    if (FNR == 1) {
      if ($0 != "column\tallowed") {
        fail("decision schema header must be: column<TAB>allowed")
      }
      next
    }
    if (NF != 2 || $1 == "" || $2 == "") {
      fail("decision schema rows require column and allowed values")
    }
    if ($1 in domains) {
      fail("duplicate decision schema column: " $1)
    }
    if ($2 ~ /(^,|,$|,,)/) {
      fail("decision schema has an empty allowed value: " $1)
    }
    if ($2 == "*" && $1 != "case") {
      fail("decision schema wildcard is allowed only for case")
    }
    if ($2 != "*") {
      value_count = split($2, domain_values, ",")
      for (left = 1; left <= value_count; left += 1) {
        for (right = left + 1; right <= value_count; right += 1) {
          if (domain_values[left] == domain_values[right]) {
            fail("duplicate allowed decision value for " $1 ": " domain_values[left])
          }
        }
      }
    }
    columns[++column_count] = $1
    domains[$1] = $2
    next
  }

  FILENAME == decisions {
    if (FNR == 1) {
      if (column_count < 3 || columns[1] != "case" ||
          domains["case"] != "*" ||
          columns[column_count] != "expected" ||
          domains["expected"] == "*") {
        fail("decision schema must start with case and end with expected")
      }
      if (NF != column_count) {
        fail("decision table header does not match schema width")
      }
      for (field_index = 1; field_index <= column_count; field_index += 1) {
        if ($field_index != columns[field_index]) {
          fail("decision table header mismatch at column " field_index)
        }
      }
      next
    }
    if (NF != column_count) {
      fail("decision row has wrong width at line " FNR)
    }
    case_id = $1
    if (case_id in expected_by_case) {
      fail("duplicate decision case: " case_id)
    }
    for (field_index = 1; field_index <= column_count; field_index += 1) {
      if (!value_allowed(columns[field_index], $field_index)) {
        fail("decision value outside schema for " case_id ": " columns[field_index] "=" $field_index)
      }
    }
    expected_by_case[case_id] = $column_count
    decision_count += 1
    next
  }

  {
    if (FNR == 1) {
      if ($0 != "case\tactual") {
        fail("observed decision header must be: case<TAB>actual")
      }
      next
    }
    if (NF != 2 || $1 == "" || $2 == "") {
      fail("observed decision rows require case and actual")
    }
    case_id = $1
    if (!(case_id in expected_by_case)) {
      fail("observed decision has unknown case: " case_id)
    }
    if (case_id in observed_by_case) {
      fail("duplicate observed decision case: " case_id)
    }
    if (!value_allowed("expected", $2)) {
      fail("observed outcome outside expected domain for " case_id ": " $2)
    }
    if ($2 != expected_by_case[case_id]) {
      fail(case_id ": expected " expected_by_case[case_id] ", observed " $2)
    }
    observed_by_case[case_id] = $2
    observed_count += 1
  }

  END {
    if (column_count == 0) {
      fail("decision schema has no columns")
    }
    if (decision_count == 0) {
      fail("decision table has no cases")
    }
    for (case_id in expected_by_case) {
      if (!(case_id in observed_by_case)) {
        fail("missing observed decision case: " case_id)
      }
    }
    if (observed_count != decision_count) {
      fail("observed decision count does not match decision cases")
    }
  }
' "$SCHEMA" "$DECISIONS" "$OBSERVED"

printf 'Decision table passed: %s\n' "$DECISIONS"
