# Approaches — q-image-grayscale-rebuild

## Problem in one line

Unscramble a 5×5 tiled WebP with a given mapping, convert to grayscale with Rec.709 luma weights, upload a pixel-exact image.

## Grader (from quiz JS)

- Loads `jigsaw.webp` (static, same for everyone) with `createImageBitmap`, and draws scrambled tile `"r,c"` at original
  position `"R,C"` on a 500×500 canvas.
- `getImageData`; per pixel `v = Math.round(.2126*R + .7152*G + .0722*B)`; R=G=B=v, alpha kept.
- The upload is decoded via `<img>` → canvas → `getImageData`. **Dimensions and all 1,000,000 bytes must be equal.**
- Everything runs **in the submitting browser**, so the expected array depends on that browser's decoder and canvas.
  Clean Chrome expected RGBA sha256: `876038f7c47be4deab3507be7b85618fa547480309fda139529af66f1729c0c4`.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| **Brave browser** | **Trap (environment)** | Brave's fingerprinting protection ("farbling") adds noise to canvas reads. The grader's *expected* data is corrupted, so **no upload can pass in Brave**. Brave's UA string says "Chrome"; only `navigator.brave` reveals it |
| Pillow `img.convert("L")` | Trap | BT.601 weights (0.299/0.587/0.114): 206,674 / 250,000 pixels wrong (measured) |
| Python `round()` | Trap | Banker's rounding ≠ JS `Math.round` on .5. Use `floor(x + 0.5)` |
| `jigsaw.webp` is **lossy** (VP8) | Risk | Decoders could differ. Here clean Chrome, headless Chrome and Pillow all decode identically |
| "lossless formats such as PNG or WEBP" | Genuine | JPEG or lossy WebP output would break exactness |
| Mapping direction | Note | Rows are *scrambled → original*. Taken from the quiz JS; identical to the page table |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | Pillow crop/paste + `convert("L")` | rejected: wrong weights |
| B | Pillow crop/paste + manual luma with JS rounding | correct (`src/verify.py`) |
| C | The grader's own code in headless Chrome (`src/rebuild.html`) | correct: **byte-identical to the accepted file** |
| D | The grader's own code in the user's browser (`src/console_snippet.js`) | correct in Chrome; noisy in Brave |

## Attempts

| # | File / where it was checked | Result |
|---|-----------------------------|--------|
| 1 | offline `data/reconstructed-grayscale.png`, checked in **Brave** | ❌ (the file was correct; Brave's canvas noise corrupted the expected data) |
| 2–3 | snippet in Brave (PNG, then WebP) | self-check 534 noisy bytes; ❌ |
| 4 | offline lossless WebP | not useful in Brave (same pixels as #1) |
| 5 | snippet PNG auto-attached, still in Brave | ❌ |
| diag | `src/diagnose.js`: Brave → 256 noisy pixels in a solid-colour test; expected sha `edb3c398…` ≠ Chrome `876038f7…` | root cause proven |
| ✅ | **`grayscale-chrome-20261006T180133.png` uploaded and checked in real Google Chrome** (byte-identical to #1) | **passed** |

## Gotchas

- **Use plain Google Chrome for canvas/pixel-exact questions.** Brave (fingerprinting protection), Safari private/advanced
  protection, Firefox `resistFingerprinting` and some extensions add canvas noise. `src/diagnose.js` detects this in 10 seconds.
- `toBlob("image/webp", q)` is lossless in Chrome only at `q = 1.0`.
- `canvas.getImageData` on `file://` images is tainted: serve over `http://127.0.0.1`.
- Headless Chrome's `--dump-dom` can snapshot before async work finishes (use `--virtual-time-budget`, or verify in Python).

## Verification

- `python3 src/verify.py [file]` → 0 differing pixels of 250,000 (PNG and WebP).
- `src/diagnose.js` in clean Chrome: not Brave · noise clean · expected sha = `876038f7…` (Chrome reference).
- Exam "Check" button: ✅ passed in Google Chrome (2026-10-06).
