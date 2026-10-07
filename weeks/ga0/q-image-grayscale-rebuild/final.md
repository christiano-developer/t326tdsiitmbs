# Final — q-image-grayscale-rebuild

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-image-grayscale-rebuild](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-image-grayscale-rebuild)

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

Use **Google Chrome**. Brave adds noise to canvas pixels and every upload fails.

1. Open the exam page in Chrome. Open DevTools (Ctrl+Shift+I; Mac: Cmd+Opt+I) and click **Console**.
2. Copy the code below into a text editor. Replace the `wo = {...}` mapping with the mapping from your question (format `"row,col": "row,col"`).
   <details><summary>console_snippet.js (click to expand)</summary>

   ```js
   // Paste into DevTools Console ON THE EXAM PAGE, in plain Chrome (not Brave:
   // its fingerprinting protection adds noise to canvas reads).
   // Runs the grader's exact logic with this browser's own WebP decoder, then:
   //  1. self-checks the PNG round-trip (<img> -> canvas, like the grader),
   //  2. attaches the PNG directly to the question's file input,
   //  3. downloads a copy with a unique, timestamped name.
   (async () => {
     const wo = {
       "0,0": "2,1", "0,1": "1,1", "0,2": "4,1", "0,3": "0,3", "0,4": "0,1",
       "1,0": "1,4", "1,1": "2,0", "1,2": "2,4", "1,3": "4,2", "1,4": "2,2",
       "2,0": "0,0", "2,1": "3,2", "2,2": "4,3", "2,3": "3,0", "2,4": "3,4",
       "3,0": "1,0", "3,1": "2,3", "3,2": "3,3", "3,3": "4,4", "3,4": "0,2",
       "4,0": "3,1", "4,1": "1,2", "4,2": "1,3", "4,3": "0,4", "4,4": "4,0",
     };
     const blob = await fetch("jigsaw.webp").then((r) => r.blob());
     const n = await createImageBitmap(blob);
     const s = n.width / 5, a = n.height / 5;
     const cv = document.createElement("canvas");
     cv.width = n.width;
     cv.height = n.height;
     const u = cv.getContext("2d");
     for (const [k, v] of Object.entries(wo)) {
       const [f, y] = k.split(",").map(Number);
       const [w, b] = v.split(",").map(Number);
       u.drawImage(n, y * s, f * a, s, a, b * s, w * a, s, a);
     }
     const img = u.getImageData(0, 0, cv.width, cv.height);
     const d = img.data;
     for (let h = 0; h < d.length; h += 4) {
       const g = Math.round(0.2126 * d[h] + 0.7152 * d[h + 1] + 0.0722 * d[h + 2]);
       d[h] = d[h + 1] = d[h + 2] = g;
     }
     u.putImageData(img, 0, 0);
     const png = await new Promise((r) => cv.toBlob(r, "image/png"));
     // Self-check: decode back through <img> + canvas, like the grader
     const im = new Image();
     im.src = URL.createObjectURL(png);
     await im.decode();
     const c2 = document.createElement("canvas");
     c2.width = im.width;
     c2.height = im.height;
     const x2 = c2.getContext("2d");
     x2.drawImage(im, 0, 0);
     const back = x2.getImageData(0, 0, c2.width, c2.height).data;
     let bad = 0;
     for (let k = 0; k < d.length; k++) if (d[k] !== back[k]) bad++;
     console.log("round-trip mismatched bytes:", bad, bad === 0 ? "OK" : "PROBLEM");
     const ts = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15);
     const name = "grayscale-chrome-" + ts + ".png";
     const file = new File([png], name, { type: "image/png" });
     // Attach to the question's upload field (id = question id)
     const input = document.getElementById("q-image-grayscale-rebuild");
     if (input) {
       const dt = new DataTransfer();
       dt.items.add(file);
       input.files = dt.files;
       input.dispatchEvent(new Event("change", { bubbles: true }));
       console.log("attached to upload field:", name, "- now click Check");
     } else {
       console.warn("upload field not found; upload the downloaded file");
     }
     const link = document.createElement("a");
     link.href = im.src;
     link.download = name;
     link.click();
   })();
   ```

   </details>

3. Paste the edited snippet into the Console and press Enter.
4. It should print `round-trip mismatched bytes: 0 OK` and `attached to upload field`. It also downloads a copy of the PNG.
5. Click Check, then Save. If the attach didn't work, upload the downloaded PNG manually.

## Final prompt

```text
Reassemble a 5x5 scrambled image: for each mapping entry "r,c" -> "R,C", the tile at scrambled (row r, col c) goes to
original (row R, col C). Then grayscale every pixel as Math.round(0.2126*R + 0.7152*G + 0.0722*B) (JS rounding, i.e.
floor(x+0.5); do NOT use Pillow convert("L")), set R=G=B, keep alpha, and save as lossless PNG at the same size.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
cd weeks/ga0/q-image-grayscale-rebuild
python3 -m http.server 8765 --bind 127.0.0.1 &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --virtual-time-budget=10000 --dump-dom "http://127.0.0.1:8765/src/rebuild.html" \
  | python3 -c "import sys,re,base64; m=re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', sys.stdin.read()); open('data/reconstructed-grayscale.png','wb').write(base64.b64decode(m.group(1)))"
kill %1
python3 src/verify.py      # independent check
```

Upload [`data/reconstructed-grayscale.png`](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-image-grayscale-rebuild/data/reconstructed-grayscale.png) **from Google Chrome** (Brave's canvas noise makes any upload fail).

## Expected output

```
size (500, 500) vs (500, 500) | differing pixels: 0 of 250000 | PASS
```

## Answer submitted (✅ passed, in Google Chrome)

[data/reconstructed-grayscale.png](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-image-grayscale-rebuild/data/reconstructed-grayscale.png) (byte-identical to the accepted
`grayscale-chrome-20261006T180133.png`). **Submit from Google Chrome, not Brave.**
