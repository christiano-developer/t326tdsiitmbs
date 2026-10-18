# Final — q-rename-files-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-rename-files-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-rename-files-server)

## How to solve (for a teammate)

> Seeded per email: your file paths and categories differ, so your hash differs.

1. On the exam page click **Download Files (ZIP)**. Extract it from the terminal (not Finder, which can add
   `.DS_Store` files): `mkdir q7 && cd q7 && unzip ../files_to_reorganize.zip`.
2. Save the script below as `reorganize.sh` **outside** that folder (e.g. one level up), then from inside the
   extracted folder run `bash ../reorganize.sh`.
3. It moves every file to `<category>/<path-with-dashes>-<filename>`, deletes the ZIP's `README.md` and the empty
   folders, and prints `<64 hex chars>  -`. Submit only the 64 hex characters, then Check and Save.
   - macOS without `sha256sum`: change the last line to `find . -type f | LC_ALL=C sort | shasum -a 256`.

<details><summary>reorganize.sh (click to expand)</summary>

```bash
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
```

</details>

## Final prompt

```text
I extracted files_to_reorganize.zip: 30 .txt files in nested folders (paths contain spaces, accents and a
Cyrillic "і" homoglyph) plus a README.md. For each .txt, the category is the first line starting with
"category:" (lowercase). Write a NUL-safe bash script that plans all moves first, then moves each file to
<category>/<original path with every / replaced by ->, deletes README.md and empty folders, and prints
find . -type f | LC_ALL=C sort | sha256sum.
```

- **Tool / model used:** Claude (Claude Opus 5.5) via Claude in Chrome.

## Reproduction steps (needs a clone of this repo)

The repo keeps only path → category ([data/manifest.json](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-rename-files-server/data/manifest.json));
the hash depends only on the final paths, so a stand-in tree reproduces it:

```bash
mkdir /tmp/q7 && cd /tmp/q7
python3 - "$OLDPWD/weeks/ga1/q-rename-files-server/data/manifest.json" <<'PY2'
import json, sys, pathlib
for r in json.load(open(sys.argv[1], encoding="utf-8")):
    p = pathlib.Path(r["path"]); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"category: {r['category']}\n", encoding="utf-8")
pathlib.Path("README.md").write_text("readme\n")
PY2
bash "$OLDPWD/weeks/ga1/q-rename-files-server/src/reorganize.sh"
```

## Expected output

```
621877e7d4c18e9c500c752d8c7c7e2c05c1ad3cc1cecd9e8f962a3de10b1451  -
```

## Answer submitted (✅ Check passed)

```
621877e7d4c18e9c500c752d8c7c7e2c05c1ad3cc1cecd9e8f962a3de10b1451
```
