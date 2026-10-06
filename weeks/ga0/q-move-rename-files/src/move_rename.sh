#!/usr/bin/env bash
# GA0 q-move-rename-files: move every file from the sub-folders into one empty folder, then replace each digit in
# the file names with the next one (0→1 … 8→9, 9→0), and print the grader's hash.
# Works on a COPY so the extracted originals stay untouched.
# Usage: src/move_rename.sh <extracted-root> [workdir]
set -euo pipefail
SRC="${1:?extracted root (contains the 3 folders)}"
WORK="${2:-$(mktemp -d)}"

cp -R "$SRC/." "$WORK/src"          # scratch copy
mkdir -p "$WORK/flat"               # the empty target folder

# 1. mv all files under the folders (not hidden ones like .DS_Store) into the empty folder
mv "$WORK"/src/*/* "$WORK/flat/"

# 2. rename: shift every digit in ONE pass (tr), never chained sed (s/1/2/; s/2/3/ would turn 1 into 3)
cd "$WORK/flat"
for f in *; do
  new=$(echo "$f" | tr '0-9' '1-90')
  [ "$f" != "$new" ] && mv -- "$f" "$new"
done

ls -1 | sed 's/^/  /' >&2
echo "files: $(ls -1 | wc -l | tr -d ' ')" >&2

# 3. the question's command
grep . * | LC_ALL=C sort | sha256sum 2>/dev/null || grep . * | LC_ALL=C sort | shasum -a 256
