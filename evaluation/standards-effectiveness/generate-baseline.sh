#!/usr/bin/env bash
set -euo pipefail

readonly BASELINE_COMMIT="6b4df85f042898374e9d23d265f4ecd25b0a7ba7"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly MANIFEST="$SCRIPT_DIR/corpus.tsv"
readonly OUTPUT_DIR="$SCRIPT_DIR/generated"
readonly REPO="${1:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)}"

git -C "$REPO" cat-file -e "$BASELINE_COMMIT^{commit}"
mkdir -p "$OUTPUT_DIR"

readonly FILE_METRICS="$OUTPUT_DIR/file-metrics.tsv"
readonly SECTION_INVENTORY="$OUTPUT_DIR/section-inventory.tsv"
readonly SUMMARY="$OUTPUT_DIR/summary.tsv"

printf 'path\tkind\tnormative\ttarget_role\tdisposition\tbaseline_source\tsha256\tlines\theadings\timperatives\n' \
  > "$FILE_METRICS"
printf 'id\tpath\tline\tlevel\ttarget_role\tdisposition\theading\n' \
  > "$SECTION_INVENTORY"

sequence=0
total_files=0
total_lines=0
total_headings=0
total_imperatives=0
normative_files=0
normative_lines=0
normative_headings=0
normative_imperatives=0

while IFS=$'\t' read -r path kind normative target_role disposition baseline_source; do
  if [[ "$path" == "path" ]]; then
    continue
  fi

  artifact="$(mktemp)"
  case "$baseline_source" in
    git)
      git -C "$REPO" show "$BASELINE_COMMIT:$path" > "$artifact"
      ;;
    snapshot)
      cp "$SCRIPT_DIR/snapshots/$path" "$artifact"
      ;;
    *)
      printf 'Unknown baseline source for %s: %s\n' "$path" "$baseline_source" >&2
      exit 1
      ;;
  esac

  sha256="$(sha256sum "$artifact" | awk '{ print $1 }')"
  lines="$(wc -l < "$artifact")"
  headings="$(awk '/^#{1,6} / { count += 1 } END { print count + 0 }' "$artifact")"
  imperatives="$(
    awk '
      BEGIN { IGNORECASE = 1 }
      /(^|[^[:alpha:]])(must|required|shall|never|always|mandatory|do not)([^[:alpha:]]|$)/ {
        count += 1
      }
      END { print count + 0 }
    ' "$artifact"
  )"

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$path" "$kind" "$normative" "$target_role" "$disposition" \
    "$baseline_source" "$sha256" "$lines" "$headings" "$imperatives" \
    >> "$FILE_METRICS"

  total_files=$((total_files + 1))
  total_lines=$((total_lines + lines))
  total_headings=$((total_headings + headings))
  total_imperatives=$((total_imperatives + imperatives))

  if [[ "$normative" != "no" ]]; then
    normative_files=$((normative_files + 1))
    normative_lines=$((normative_lines + lines))
    normative_headings=$((normative_headings + headings))
    normative_imperatives=$((normative_imperatives + imperatives))

    while IFS=$'\t' read -r line level heading; do
      sequence=$((sequence + 1))
      printf 'STD-%04d\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$sequence" "$path" "$line" "$level" "$target_role" \
        "$disposition" "$heading" >> "$SECTION_INVENTORY"
    done < <(
      awk '
        /^#{1,6} / {
          match($0, /^#+/)
          level = RLENGTH
          heading = substr($0, level + 2)
          sub(/\r$/, "", heading)
          printf "%d\t%d\t%s\n", NR, level, heading
        }
      ' "$artifact"
    )
  fi

  rm -f "$artifact"
done < "$MANIFEST"

{
  printf 'metric\tvalue\n'
  printf 'baseline_commit\t%s\n' "$BASELINE_COMMIT"
  printf 'files\t%s\n' "$total_files"
  printf 'lines\t%s\n' "$total_lines"
  printf 'headings\t%s\n' "$total_headings"
  printf 'imperatives\t%s\n' "$total_imperatives"
  printf 'normative_and_derived_files\t%s\n' "$normative_files"
  printf 'normative_and_derived_lines\t%s\n' "$normative_lines"
  printf 'normative_and_derived_headings\t%s\n' "$normative_headings"
  printf 'normative_and_derived_imperatives\t%s\n' "$normative_imperatives"
  printf 'inventoried_sections\t%s\n' "$sequence"
} > "$SUMMARY"

printf 'Generated baseline from %s\n' "$BASELINE_COMMIT"
