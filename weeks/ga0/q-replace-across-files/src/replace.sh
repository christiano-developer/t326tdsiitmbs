#!/usr/bin/env bash
# GA0 q-replace-across-files: replace every case-insensitive "iitm" with "IIT Madras" in all files, keep line endings,
# then print `cat * | sha256sum`. Works on a COPY so the extracted originals stay untouched.
# Usage: src/replace.sh <extracted-folder> [workdir]
set -euo pipefail
SRC="${1:?folder with file0.txt..file9.txt}"
WORK="${2:-$(mktemp -d)}"

mkdir -p "$WORK/new" && cp "$SRC"/* "$WORK/new/"
cd "$WORK/new"

# perl -pi: in-place, case-insensitive, plain substring (like the grader's /iitm/gi), bytes otherwise untouched.
# (macOS/BSD sed has no `I` flag, so `sed -i 's/iitm/IIT Madras/gI'` doesn't work there.)
perl -pi -e 's/iitm/IIT Madras/gi' *

echo "remaining iitm: $(grep -oi 'iitm' * | wc -l | tr -d ' ')  |  'IIT Madras' count: $(grep -o 'IIT Madras' * | wc -l | tr -d ' ')" >&2
cat * | sha256sum 2>/dev/null || cat * | shasum -a 256
