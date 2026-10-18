# Approaches — q-rename-files-server

## Problem in one line

Flatten 30 files into category folders, then hash the sorted file list.

## Grader (from quiz JS)

- Client-side: builds the expected list `./{category}/{dirs joined by -}-{filename}`, sorted by
  UTF-16 code unit (same as `LC_ALL=C` byte order for these chars), joined with `\n` + trailing `\n`, SHA-256.
- Check: first whitespace token === hash. A `-` in the answer triggers "submit only the hash".

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| `README.md` inside the ZIP | **Gotcha** | Not in the expected list. If it remains in the tree, `find` includes it and the hash fails |
| Example script `for file in $(find …)` | **Distractor** | Word-splits on spaces (`part 2`, `spaces here`); breaks the moves |
| "or 32 for the hash function used by this system" | **Distractor** | It's SHA-256: 64 hex chars |
| `fіle07.txt` with Cyrillic `і` | Gotcha | ~10% of filenames use a homoglyph; keep bytes as-is |
| `Category:` line in the body | Gotcha | Match `^category:` (lowercase) on the first line only |
| macOS | Gotcha | Extract with CLI `unzip` (not Finder); watch for `.DS_Store` and Unicode normalisation |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Bash: `find -print0` → plan moves → `mv` → delete README → hash | bash, grep, find | The intended path; NUL-safe for spaces and Unicode | macOS has `shasum -a 256` instead of `sha256sum` | written as `src/reorganize.sh`, verified |
| B | Compute the expected sorted path list and hash it without moving anything | Browser JS / Python | No files touched; can't half-fail | Must reproduce `LC_ALL=C` byte order and the trailing newline exactly | chosen for the submission |
| C | `for file in $(find …)` (the page's example) | bash | Short | Word-splits `part 2`; breaks on spaces | rejected (distractor) |

## Chosen: B (submitted), A (verified)

**Why:** the hash only depends on the final paths, so computing them directly is fastest and safest; A confirms
it the way the question intends.

## Gotchas hit

- Keep filenames byte-for-byte: three files use a Cyrillic `і` (`fіle07.txt`, `fіle13.txt`, `fіle27.txt`) and look
  identical to their Latin twins.
- 13 categories, several non-ASCII (`日本語`, `résumé`, `münchen`, `naïve-bayes`); `LC_ALL=C` sorts them by UTF-8 bytes.
- Delete the ZIP's `README.md` (and any `.DS_Store`) before hashing, or `find` counts it.
- Plan all moves before moving, so the script never walks into the new category folders.

## Verification

- Expected list: 30 paths, sorted by bytes → `621877e7d4c18e9c500c752d8c7c7e2c05c1ad3cc1cecd9e8f962a3de10b1451`.
- `src/reorganize.sh` on a tree rebuilt from `data/manifest.json` → same hash.
- Exam **Check** → "Correct" (Chrome, 2026-10-18).
