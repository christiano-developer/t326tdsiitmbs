# Approaches — q-replace-across-files

## Problem in one line

Case-insensitive replace `iitm` → `IIT Madras` in 10 files without touching anything else, then hash the concatenation.

## Grader (from quiz JS)

- 10 files of 10,000 random chars each (letters/digits/spaces/newlines), with ` IITM `, ` iitm `, ` IITm ` inserted
  10× each; lines trimmed; a trailing `\n` added.
- Expected: `sha256( concat(files).replace(/iitm/gi, "IIT Madras") )`. This is a **plain substring**, case-insensitive.
- Check: the first token of the answer equals the hash.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| The pasted question lacked the instruction | Note | Recovered from the page source: replace IITM (any case) → "IIT Madras", keep line endings |
| `sed -i 's/iitm/IIT Madras/gI'` (common answer) | **Trap (macOS)** | BSD sed has no `I` flag, and `-i` needs an argument. Use `perl -pi -e 's/…/…/gi'` |
| "don't change the line endings" | Genuine | Editors/tools may convert to CRLF or add a final newline. `perl -pi` keeps bytes |
| Whole-word matching `\biitm\b` | Trap | The grader replaces plain substrings. Here all 300 matches were the planted ones, but substring is the safe rule |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | GNU `sed -i 's/iitm/IIT Madras/gI' *` | Linux only; fails on macOS sed |
| B | **`perl -pi -e 's/iitm/IIT Madras/gi' *`** | **chosen**: portable, byte-preserving |
| C | Python `re.sub(rb'(?i)iitm', b'IIT Madras', …)` | cross-check |

## Verification

- `src/replace.sh data/extracted/q-replace-across-files <workdir>` → 0 `iitm` left, 300 `IIT Madras`, hash `16bd7ac6…26ef`.
- Python: each new file == original with only `/iitm/gi` replaced; concatenated hash identical.
- Exam "Check" button: ✅ passed on attempt 1 (2026-10-06).
