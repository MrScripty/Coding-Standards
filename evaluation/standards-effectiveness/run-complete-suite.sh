#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";count=0
while IFS= read -r checker;do
  printf 'RUN %s\n' "${checker##*/}"
  "$checker"
  ((count+=1))
done < <(find "$S" -maxdepth 1 -type f -name 'verify-*.sh' -print | LC_ALL=C sort)
printf 'Complete standards suite passed: %s checkers\n' "$count"
