# q-image-grayscale-rebuild

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no (file upload) |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed in Google Chrome) |

## Question

**Reconstruct and desaturate an image**: background: *Images: Compression* (dimensions, lossless vs lossy, SVG,
WebP, Pillow, cwebp/pngquant/jpegoptim/ImageMagick, squoosh, sharp).

> Forensic desaturation task for PixelGuard. Steps:
> 1. Download the scrambled puzzle (`jigsaw.webp`).
> 2. Reassemble the 5×5 grid using the mapping provided (scrambled row/col → original row/col).
> 3. Convert the reconstructed image to grayscale using luminance coefficients (0.2126 R, 0.7152 G, 0.0722 B).
> 4. Export the grayscale image without resizing or recompression artefacts (lossless formats such as PNG or WEBP).
>
> Upload the reconstructed grayscale image. It must exactly match the luminance-based grayscale conversion.

## Inputs / given data

- [data/jigsaw.webp](data/jigsaw.webp): scrambled 500×500 **lossy** WebP (VP8); same file for every student.
- [data/mapping.json](data/mapping.json): 25-entry mapping, extracted from the quiz JS and identical to the page table
  ([data/mapping-screenshot.png](data/mapping-screenshot.png)).

## Final answer

✅ Upload [data/reconstructed-grayscale.png](data/reconstructed-grayscale.png) **from Google Chrome** (500×500 RGBA PNG,
R=G=B=luminance; RGBA sha256 `876038f7…c0c4`). The accepted upload was the browser-made copy
`grayscale-chrome-20261006T180133.png`, which is byte-identical to this file.

## Status notes

- Passed once checked in **real Google Chrome**. All earlier rejections happened in **Brave**, whose fingerprinting
  protection adds noise to canvas reads and corrupts the grader's own expected data (proven with `src/diagnose.js`).
- `data/attempt-1-rejected.png` is the same correct file, rejected only because of Brave.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md)
- [src/console_snippet.js](src/console_snippet.js) — **run on the exam page**: grader logic in your browser → downloads the PNG
- [src/diagnose.js](src/diagnose.js) — run in the exam tab: Brave/noise detection, expected hash, grader's exact check on the attached file
- [src/rebuild.html](src/rebuild.html) — grader logic in the browser → PNG data URL (serve the folder over http)
- [src/verify.py](src/verify.py) — independent Pillow rebuild, compares every pixel with the PNG
