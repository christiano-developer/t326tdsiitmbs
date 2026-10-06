"""Independent check of the upload: rebuild the expected grayscale with Pillow (same mapping, same formula and
rounding as the grader: Math.round(.2126*R + .7152*G + .0722*B), alpha kept) and compare every pixel and the size
with data/reconstructed-grayscale.png (built in Chrome by src/rebuild.html).

Usage: python3 src/verify.py
"""
import json
import math
import sys
from PIL import Image

wo = json.load(open("data/mapping.json"))                   # "scrRow,scrCol" -> "origRow,origCol"
src = Image.open("data/jigsaw.webp").convert("RGBA")
W, H = src.size
s, a = W // 5, H // 5

out = Image.new("RGBA", (W, H))
for k, v in wo.items():
    f, y = map(int, k.split(","))
    w, b = map(int, v.split(","))
    out.paste(src.crop((y * s, f * a, y * s + s, f * a + a)), (b * s, w * a))

# JS Math.round(x) == floor(x + 0.5) (Python's round() is banker's rounding); same operand order as the grader
expected = [(g, g, g, A) for R, G, B, A in out.getdata() for g in [math.floor(.2126 * R + .7152 * G + .0722 * B + 0.5)]]

up = Image.open(sys.argv[1] if len(sys.argv) > 1 else "data/reconstructed-grayscale.png").convert("RGBA")
size_ok = up.size == (W, H)
diff = sum(1 for p, q in zip(expected, up.getdata()) if p != q)
print(f"size {up.size} vs {(W, H)} | differing pixels: {diff} of {W * H} | {'PASS' if size_ok and diff == 0 else 'FAIL'}")
sys.exit(0 if size_ok and diff == 0 else 1)
