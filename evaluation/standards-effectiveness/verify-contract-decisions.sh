#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/contracts/decisions.tsv"

while IFS=$'\t' read -r case_id class deployment state substitute action; do
  if [[ "$case_id" == "case" ]]; then
    continue
  fi

  [[ "$class" =~ ^(internal-coordinated|persisted|public-versioned|distributed-independent|generated)$ ]]
  [[ "$deployment" =~ ^(atomic|independent)$ ]]
  [[ "$state" =~ ^(ephemeral|authoritative|derived)$ ]]
  [[ "$substitute" =~ ^(none|authoritative-equivalent|unknown)$ ]]
  [[ "$action" =~ ^(replace|migrate|version|negotiate|regenerate|rebuild-derived|degrade-defined|typed-unavailable|typed-invalid|typed-unsupported)$ ]]

  if [[ "$action" == "replace" &&
        ( "$deployment" != "atomic" || "$state" == "authoritative" ) ]]; then
    printf '%s: replacement would bypass consumer or persistence obligations\n' \
      "$case_id" >&2
    exit 1
  fi
  if [[ "$action" == "rebuild-derived" &&
        ( "$state" != "derived" || "$substitute" != "authoritative-equivalent" ) ]]; then
    printf '%s: rebuild lacks disposable state or authoritative source\n' \
      "$case_id" >&2
    exit 1
  fi
  if [[ "$action" == "degrade-defined" &&
        "$substitute" != "authoritative-equivalent" ]]; then
    printf '%s: degraded result lacks semantic authority\n' "$case_id" >&2
    exit 1
  fi
  if [[ "$substitute" == "unknown" &&
        ! "$action" =~ ^typed-(unavailable|invalid|unsupported)$ ]]; then
    printf '%s: unknown substitute must preserve a typed diagnostic\n' \
      "$case_id" >&2
    exit 1
  fi
done < "$FIXTURE"

printf 'Contract decision fixtures passed\n'
