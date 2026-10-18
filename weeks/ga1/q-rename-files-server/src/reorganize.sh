#!/usr/bin/env bash
# Reorganize the extracted files_to_reorganize/ tree in place:
#   <dirs>/<file>.txt  ->  <category>/<dirs-joined-by-dashes>-<file>.txt
# category = first line of the file that starts with "category:" (lowercase), value trimmed.
# Safe for spaces and Unicode (NUL-delimited). Run from the extraction root, then print the hash.
set -euo pipefail
shopt -s nullglob

# 1. plan every move first (so new category folders are never walked)
plan=()
while IFS= read -r -d '' f; do
  rel="${f#./}"
  cat="$(grep -m1 '^category:' -- "$f" | sed -e 's/^category:[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [[ -n "$cat" ]] || { echo "no category: $rel" >&2; exit 1; }
  plan+=("$rel" "$cat/${rel//\//-}")
done < <(find . -type f -name '*.txt' -print0)

# 2. move
for ((i = 0; i < ${#plan[@]}; i += 2)); do
  mkdir -p -- "$(dirname -- "${plan[i+1]}")"
  mv -- "${plan[i]}" "${plan[i+1]}"
done

# 3. remove what isn't part of the answer: the ZIP's README.md and the now-empty source folders
rm -f -- README.md
find . -mindepth 1 -type d -empty -delete

find . -type f | LC_ALL=C sort | sha256sum
