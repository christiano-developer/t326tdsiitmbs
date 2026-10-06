# Approaches — q-move-rename-files

## Problem in one line

Flatten 3 folders of files into one, shift every digit in the names by +1 (mod 10), then hash `grep . *` output sorted in C locale.

## Grader (from quiz JS)

- Zip: 3 folders (random lowercase names) × 10 unique `<random>.txt` files, each containing `x` (seeded).
- Expected: `sha256( sorted unique lines "<renamed>:x\n" )`, where renamed = each digit `d → (d+1) % 10`, all at once.
- Check: the **first whitespace-separated token** of the answer equals the hash (a trailing `  -` is fine).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "replace each digit with the next" | **Trap** | Must be **simultaneous**. Chained `sed 's/0/1/g;s/1/2/g;…'` cascades (`yud3vxvx → yud0vxvx`) and gives a different hash (`449dfb71…`, confirmed) |
| `LC_ALL=C` | Genuine | Byte-order sort = the grader's JS `.sort()`; other locales may reorder lines |
| `.DS_Store` added by macOS Finder | **Trap (local)** | A hidden file in the extracted folder; `*/*` doesn't match hidden files, so it isn't moved |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | **Bash: `mv src/*/* flat/`, rename with `tr '0-9' '1-90'`, run the exact command** | **chosen** |
| B | Python re-implementation of the grader formula | used as the cross-check |

## Verification

- `src/move_rename.sh data/extracted/q-move-rename-files <workdir>` → 30 files → `37cb5289…95c6  -`.
- Python (grader formula) → same hash.
- Negative control (chained replacement) → `449dfb71…` (different).
- Exam "Check" button: ✅ passed on attempt 1 (2026-10-06).
