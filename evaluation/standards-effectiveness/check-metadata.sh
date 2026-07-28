#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -lt 2 ]]; then
  printf 'Usage: %s <repo-root> <module>...\n' "$0" >&2
  exit 2
fi

readonly ROOT="$(cd "$1" && pwd)"
shift

readonly -a FIELDS=(
  "ID"
  "Role"
  "Level"
  "Applies when"
  "Does not apply when"
  "Requires"
  "Specializes"
  "Verification"
  "Canonical owner"
)

declare -A paths
declare -A roles
declare -A levels
declare -A requirements
declare -A specializations
declare -A states

value_for() {
  local file="$1"
  local field="$2"
  sed -n "s/^- ${field}: //p" "$file" | tr -d '`'
}

for file in "$@"; do
  readonly_path="$(cd "$(dirname "$file")" && pwd)/$(basename "$file")"
  relative_path="${readonly_path#"$ROOT"/}"

  for field in "${FIELDS[@]}"; do
    count="$(grep -c "^- ${field}: " "$file" || true)"
    if [[ "$count" -ne 1 ]]; then
      printf '%s: expected one %s field, found %s\n' \
        "$relative_path" "$field" "$count" >&2
      exit 1
    fi
  done

  id="$(value_for "$file" "ID")"
  role="$(value_for "$file" "Role")"
  level="$(value_for "$file" "Level")"
  owner="$(value_for "$file" "Canonical owner")"
  applies_when="$(value_for "$file" "Applies when")"
  excludes="$(value_for "$file" "Does not apply when")"
  requires="$(value_for "$file" "Requires")"
  specializes="$(value_for "$file" "Specializes")"

  if [[ ! "$id" =~ ^[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)*$ ]]; then
    printf '%s: invalid module ID %s\n' "$relative_path" "$id" >&2
    exit 1
  fi
  if [[ ! "$role" =~ ^(core|router|workflow|profile|topic|reference)$ ]]; then
    printf '%s: invalid role %s\n' "$relative_path" "$role" >&2
    exit 1
  fi
  if [[ ! "$level" =~ ^(MUST|SHOULD|PROFILE|REFERENCE)$ ]]; then
    printf '%s: invalid level %s\n' "$relative_path" "$level" >&2
    exit 1
  fi
  if [[ "$role" == "core" && "$level" != "MUST" ]]; then
    printf '%s: core must use MUST level\n' "$relative_path" >&2
    exit 1
  fi
  if [[ "$role" == "profile" && "$level" != "PROFILE" ]]; then
    printf '%s: profile must use PROFILE level\n' "$relative_path" >&2
    exit 1
  fi
  if [[ "$role" == "reference" && "$level" != "REFERENCE" ]]; then
    printf '%s: reference must use REFERENCE level\n' "$relative_path" >&2
    exit 1
  fi
  if [[ "$owner" != "$relative_path" ]]; then
    printf '%s: canonical owner is %s\n' "$relative_path" "$owner" >&2
    exit 1
  fi
  if [[ ",$requires," == *",$id,"* || ",$specializes," == *",$id,"* ]]; then
    printf '%s: module cannot depend on or specialize itself\n' \
      "$relative_path" >&2
    exit 1
  fi
  if [[ "$role" != "profile" && "$specializes" != "none" ]]; then
    printf '%s: only profiles may specialize rules\n' "$relative_path" >&2
    exit 1
  fi
  if [[ "$applies_when" == "none" && "$excludes" == "none" ]]; then
    printf '%s: applicability and exclusions cannot both be none\n' \
      "$relative_path" >&2
    exit 1
  fi

  if [[ -n "${paths[$id]:-}" ]]; then
    printf '%s: duplicate module ID also used by %s\n' \
      "$relative_path" "${paths[$id]}" >&2
    exit 1
  fi
  paths["$id"]="$relative_path"
  roles["$id"]="$role"
  levels["$id"]="$level"
  requirements["$id"]="$requires"
  specializations["$id"]="$specializes"
done

check_targets() {
  local id="$1"
  local relationship="$2"
  local targets="$3"
  local target

  if [[ "$targets" == "none" ]]; then
    return
  fi

  IFS=',' read -ra target_list <<< "$targets"
  for target in "${target_list[@]}"; do
    target="${target#"${target%%[![:space:]]*}"}"
    target="${target%"${target##*[![:space:]]}"}"
    if [[ -z "${paths[$target]:-}" ]]; then
      printf '%s: unresolved %s target %s\n' \
        "${paths[$id]}" "$relationship" "$target" >&2
      exit 1
    fi
  done
}

visit() {
  local id="$1"
  local target

  if [[ "${states[$id]:-0}" == "1" ]]; then
    printf '%s: dependency cycle includes %s\n' "${paths[$id]}" "$id" >&2
    exit 1
  fi
  if [[ "${states[$id]:-0}" == "2" ]]; then
    return
  fi

  states["$id"]=1
  if [[ "${requirements[$id]}" != "none" ]]; then
    IFS=',' read -ra target_list <<< "${requirements[$id]}"
    for target in "${target_list[@]}"; do
      target="${target#"${target%%[![:space:]]*}"}"
      target="${target%"${target##*[![:space:]]}"}"
      visit "$target"
    done
  fi
  states["$id"]=2
}

for id in "${!paths[@]}"; do
  check_targets "$id" "requirement" "${requirements[$id]}"
  check_targets "$id" "specialization" "${specializations[$id]}"
done

for id in "${!paths[@]}"; do
  visit "$id"
done
