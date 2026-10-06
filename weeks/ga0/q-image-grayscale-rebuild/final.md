# Final — q-image-grayscale-rebuild

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Reassemble a 5x5 scrambled image: for each mapping entry "r,c" -> "R,C", the tile at scrambled (row r, col c) goes to
original (row R, col C). Then grayscale every pixel as Math.round(0.2126*R + 0.7152*G + 0.0722*B) (JS rounding, i.e.
floor(x+0.5); do NOT use Pillow convert("L")), set R=G=B, keep alpha, and save as lossless PNG at the same size.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

```bash
cd weeks/ga0/q-image-grayscale-rebuild
python3 -m http.server 8765 --bind 127.0.0.1 &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --virtual-time-budget=10000 --dump-dom "http://127.0.0.1:8765/src/rebuild.html" \
  | python3 -c "import sys,re,base64; m=re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', sys.stdin.read()); open('data/reconstructed-grayscale.png','wb').write(base64.b64decode(m.group(1)))"
kill %1
python3 src/verify.py      # independent check
```

Upload `data/reconstructed-grayscale.png` **from Google Chrome** (Brave's canvas noise makes any upload fail).

## Expected output

```
size (500, 500) vs (500, 500) | differing pixels: 0 of 250000 | PASS
```

## Answer submitted (✅ passed, in Google Chrome)

[data/reconstructed-grayscale.png](data/reconstructed-grayscale.png) (byte-identical to the accepted
`grayscale-chrome-20261006T180133.png`). **Submit from Google Chrome, not Brave.**
