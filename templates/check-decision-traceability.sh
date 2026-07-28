#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  check-decision-traceability.sh --mode staged --map <path>
  check-decision-traceability.sh --mode range --map <path> \
    --base-ref <ref> --head-ref <ref>
EOF
}

mode=""
map_file=""
base_ref=""
head_ref=""

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --mode)
      if [[ "$#" -lt 2 ]]; then
        printf '%s requires a value.\n' "$1" >&2
        exit 2
      fi
      mode="${2:-}"
      shift 2
      ;;
    --map)
      if [[ "$#" -lt 2 ]]; then
        printf '%s requires a value.\n' "$1" >&2
        exit 2
      fi
      map_file="${2:-}"
      shift 2
      ;;
    --base-ref)
      if [[ "$#" -lt 2 ]]; then
        printf '%s requires a value.\n' "$1" >&2
        exit 2
      fi
      base_ref="${2:-}"
      shift 2
      ;;
    --head-ref)
      if [[ "$#" -lt 2 ]]; then
        printf '%s requires a value.\n' "$1" >&2
        exit 2
      fi
      head_ref="${2:-}"
      shift 2
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ "$mode" != "staged" && "$mode" != "range" ]]; then
  printf 'Traceability mode must be explicitly staged or range.\n' >&2
  usage
  exit 2
fi
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'Not inside a Git repository.\n' >&2
  exit 2
fi

normalize_path() {
  local path="$1"

  path="${path#./}"
  if [[ -z "$path" || "$path" == /* || "$path" == *:* ||
        "$path" == ".." || "$path" == ../* || "$path" == */../* ||
        "$path" == */.. ]]; then
    return 1
  fi
  printf '%s\n' "$path"
}

if ! map_file="$(normalize_path "$map_file")"; then
  printf 'Traceability map must be a repository-relative path.\n' >&2
  exit 2
fi

if [[ "$mode" == "staged" ]]; then
  if [[ -n "$base_ref" || -n "$head_ref" ]]; then
    printf 'Staged mode does not accept base or head refs.\n' >&2
    exit 2
  fi
  mapfile -t changed_files < <(
    git diff --cached --name-only --diff-filter=ACMRD --
  )
  if ! map_content="$(git show ":$map_file" 2>/dev/null)"; then
    printf 'Traceability map is absent from the Git index: %s\n' \
      "$map_file" >&2
    exit 2
  fi
  prior_map_content=""
  if git rev-parse --verify "HEAD^{commit}" >/dev/null 2>&1; then
    prior_map_content="$(git show "HEAD:$map_file" 2>/dev/null || true)"
  fi
else
  if [[ -z "$base_ref" || -z "$head_ref" ]]; then
    printf 'Range mode requires explicit base and head refs.\n' >&2
    exit 2
  fi
  if ! git rev-parse --verify "${base_ref}^{commit}" >/dev/null 2>&1; then
    printf 'Traceability base ref is not a commit: %s\n' "$base_ref" >&2
    exit 2
  fi
  if ! git rev-parse --verify "${head_ref}^{commit}" >/dev/null 2>&1; then
    printf 'Traceability head ref is not a commit: %s\n' "$head_ref" >&2
    exit 2
  fi
  mapfile -t changed_files < <(
    git diff --name-only --diff-filter=ACMRD \
      "${base_ref}...${head_ref}" --
  )
  if ! map_content="$(git show "${head_ref}:$map_file" 2>/dev/null)"; then
    printf 'Traceability map is absent from head commit %s: %s\n' \
      "$head_ref" "$map_file" >&2
    exit 2
  fi
  prior_map_content="$(
    git show "${base_ref}:$map_file" 2>/dev/null || true
  )"
fi

if [[ -n "$prior_map_content" ]]; then
  IFS=$'\t' read -r prior_trigger prior_boundary prior_profile \
    prior_artifact prior_extra <<< "$prior_map_content"
  if [[ "$prior_trigger" != "trigger_path" ||
        "$prior_boundary" != "boundary_id" ||
        "$prior_profile" != "profile" ||
        "$prior_artifact" != "artifact_path" ||
        -n "${prior_extra:-}" ]]; then
    printf 'Prior traceability map has an invalid header: %s\n' \
      "$map_file" >&2
    exit 2
  fi
  map_content="$(
    {
      printf '%s\n' "$map_content"
      tail -n +2 <<< "$prior_map_content"
    } | awk '!seen[$0]++'
  )"
fi

declare -A changed_lookup=()
for file in "${changed_files[@]}"; do
  changed_lookup["$file"]=1
done

matches_trigger() {
  local changed_file="$1"
  local trigger="$2"

  if [[ "$trigger" == */ ]]; then
    [[ "$changed_file" == "$trigger"* ]]
  else
    [[ "$changed_file" == "$trigger" ]]
  fi
}

require_heading() {
  local content="$1"
  local artifact="$2"
  local heading="$3"

  if ! rg -F -x -q -- "$heading" <<< "$content"; then
    printf '%s is missing required heading: %s\n' \
      "$artifact" "$heading" >&2
    return 1
  fi
}

section_body() {
  local content="$1"
  local heading="$2"

  awk -v heading="$heading" '
    $0 == heading { in_section = 1; next }
    in_section && /^## / { exit }
    in_section { print }
  ' <<< "$content"
}

validate_artifact() {
  local boundary="$1"
  local profile="$2"
  local artifact="$3"
  local invalid=0
  local content=""

  if [[ "$mode" == "staged" ]]; then
    if ! content="$(git show ":$artifact" 2>/dev/null)"; then
      printf 'Traceability artifact is absent from the Git index: %s\n' \
        "$artifact" >&2
      return 1
    fi
  else
    if ! content="$(git show "${head_ref}:$artifact" 2>/dev/null)"; then
      printf 'Traceability artifact is absent from head commit %s: %s\n' \
        "$head_ref" "$artifact" >&2
      return 1
    fi
  fi

  case "$profile" in
    boundary-readme|contract-readme)
      for heading in \
        "## Purpose" \
        "## Responsibility" \
        "## Invariants" \
        "## Entry Points"; do
        require_heading "$content" "$artifact" "$heading" || invalid=1
      done
      if [[ "$profile" == "contract-readme" ]] &&
          ! rg -F -x -q -- "## Consumer Contract" <<< "$content" &&
          ! rg -F -x -q -- "## Produced Contract" <<< "$content"; then
        printf '%s requires Consumer Contract or Produced Contract\n' \
          "$artifact" >&2
        invalid=1
      fi
      ;;
    adr)
      for heading in \
        "## Status" \
        "## Context" \
        "## Decision" \
        "## Alternatives" \
        "## Consequences" \
        "## Affected Boundaries"; do
        require_heading "$content" "$artifact" "$heading" || invalid=1
      done
      affected="$(section_body "$content" "## Affected Boundaries")"
      if ! rg -F -x -q -- "- \`boundary:${boundary}\`" \
          <<< "$affected"; then
        printf '%s does not identify boundary:%s\n' \
          "$artifact" "$boundary" >&2
        invalid=1
      fi
      ;;
    runbook)
      for heading in \
        "## Preconditions" \
        "## Procedure" \
        "## Validation" \
        "## Failure Handling" \
        "## Owner"; do
        require_heading "$content" "$artifact" "$heading" || invalid=1
      done
      ;;
    *)
      printf 'Unknown traceability profile: %s\n' "$profile" >&2
      return 1
      ;;
  esac

  [[ "$invalid" -eq 0 ]]
}

failures=0
matched=0
line_number=0

while IFS=$'\t' read -r trigger boundary profile artifact extra; do
  line_number=$((line_number + 1))
  if [[ "$line_number" -eq 1 ]]; then
    if [[ "$trigger" == "trigger_path" &&
          "$boundary" == "boundary_id" &&
          "$profile" == "profile" &&
          "$artifact" == "artifact_path" ]]; then
      continue
    fi
    printf '%s:1 has an invalid header\n' "$map_file" >&2
    exit 2
  fi
  if [[ -z "$trigger" || "$trigger" == \#* ]]; then
    continue
  fi
  if [[ -n "${extra:-}" ]]; then
    printf '%s:%s has unexpected columns\n' "$map_file" "$line_number" >&2
    exit 2
  fi
  if ! trigger="$(normalize_path "$trigger")" ||
      ! artifact="$(normalize_path "$artifact")"; then
    printf '%s:%s contains an invalid repository path\n' \
      "$map_file" "$line_number" >&2
    exit 2
  fi
  if [[ ! "$boundary" =~ ^[a-z][a-z0-9.-]*$ ]]; then
    printf '%s:%s contains invalid boundary ID: %s\n' \
      "$map_file" "$line_number" "$boundary" >&2
    exit 2
  fi
  if [[ ! "$profile" =~ ^(boundary-readme|contract-readme|adr|runbook)$ ]]; then
    printf '%s:%s contains invalid profile: %s\n' \
      "$map_file" "$line_number" "$profile" >&2
    exit 2
  fi

  row_matched=false
  for file in "${changed_files[@]}"; do
    if matches_trigger "$file" "$trigger"; then
      row_matched=true
      matched=$((matched + 1))
      break
    fi
  done
  if [[ "$row_matched" == "false" ]]; then
    continue
  fi

  if [[ "${changed_lookup["$artifact"]+set}" != "set" ]]; then
    printf '%s changed without required %s artifact %s for boundary:%s\n' \
      "$trigger" "$profile" "$artifact" "$boundary" >&2
    failures=$((failures + 1))
    continue
  fi
  if ! validate_artifact "$boundary" "$profile" "$artifact"; then
    failures=$((failures + 1))
  fi
done <<< "$map_content"

if [[ "$failures" -gt 0 ]]; then
  printf 'Decision traceability check failed (%s issue(s)).\n' \
    "$failures" >&2
  exit 1
fi
if [[ "$matched" -eq 0 ]]; then
  printf 'No configured decision-bearing paths changed.\n'
else
  printf 'Decision traceability check passed.\n'
fi
