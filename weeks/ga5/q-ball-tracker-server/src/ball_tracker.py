"""GA5 Q3: track the red ball.

1. Download the frames binary from /questionData (questionId=q-ball-tracker-server, needs email + quizSign):
   header = 5 big-endian uint32 (fps, frameCount, f1, f2, f3), then frameCount x (uint32 length + PNG bytes).
2. Detect balls: frames use a 4-5 colour palette (bg 250, ball outline 90, container 40, fill 150, red 220/30/30 fading,
   digits 255). Ball interiors = pixels that are not bg / outline / container -> 8-connected components -> centroids.
   This gives exactly 100 balls in every frame (outlines keep touching balls apart).
3. Track: Hungarian assignment (scipy linear_sum_assignment) between consecutive frames on distance to the previous
   position. Cross-checked with half-constant-velocity and 4-substep elastic-physics predictors: all agree on the
   red ball through the three answer frames. Pure constant-velocity prediction is the weakest (diverges late).
4. Read the number on the tracked ball in the last frame (crop and look).
Usage: python3 ball_tracker.py frames.bin
"""
import struct, sys, io
import numpy as np, cv2
from PIL import Image
from scipy.optimize import linear_sum_assignment

b = open(sys.argv[1] if len(sys.argv) > 1 else "frames.bin", "rb").read()
fps, n, *targets = struct.unpack(">5I", b[:20]); o = 20
frames = []
for _ in range(n):
    L, = struct.unpack(">I", b[o:o+4]); frames.append(np.array(Image.open(io.BytesIO(b[o+4:o+4+L])).convert("RGB"))); o += 4 + L

def detect(a):
    s = a.astype(int).sum(2)
    m = ((s != 750) & (s != 270) & (s != 120)).astype(np.uint8)
    _, _, _, cen = cv2.connectedComponentsWithStats(m, 8)
    return cen[1:]

dets = [detect(f) for f in frames]
a0 = frames[0].astype(int)
red = [i for i, (x, y) in enumerate(dets[0]) if a0[int(round(y)), int(round(x)), 1] == 30][0]
pos = dets[0]; track = [pos[red]]
for t in range(1, n):
    C = np.linalg.norm(pos[:, None] - dets[t][None], axis=2)
    _, c = linear_sum_assignment(C)
    pos = dets[t][c]; track.append(pos[red])
for f in targets:
    print(f, np.round(track[f]).astype(int).tolist())
x, y = np.round(track[-1]).astype(int)
Image.fromarray(frames[-1][y-30:y+30, x-30:x+30]).resize((240, 240), Image.NEAREST).save("final_ball.png")
print("final ball crop -> final_ball.png at", (x, y))
