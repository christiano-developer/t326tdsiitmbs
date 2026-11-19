# Final — q-ball-tracker-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga5/q-ball-tracker-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga5/q-ball-tracker-server)

## How to solve (for a teammate)

Your video is **unique per email**.

1. In the exam tab's console: `JSON.parse(localStorage.user).quizSign` → your quizSign (treat as a secret).
2. Download `https://exam.sanand.workers.dev/questionData?email=<email>&quizSign=<urlencoded sign>&questionId=q-ball-tracker-server` → `frames.bin`.
3. `pip install numpy opencv-python pillow scipy` then `python3 src/ball_tracker.py frames.bin`
   → prints the centre at each target frame and writes `final_ball.png` (crop of your ball in the last frame).
4. Read the number in `final_ball.png`; answer `N; x1,y1; x2,y2; x3,y3` (rounded ints). Check, Save.

Gotchas: work on the PNG frames, not the WebM; segment by palette colour so touching balls stay separate; don't
use constant-velocity prediction (collisions every frame) — nearest-position Hungarian is the robust choice.

## Final prompt

```text
Track the red ball (2 marks)
<paste the question + the frame format from the exam JS>
Write a Python script that decodes the frames, detects all 100 balls per frame, tracks the red one from
frame 0 with Hungarian matching, prints its centre at the 3 target frames, and crops it in the last frame.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

`python3 weeks/ga5/q-ball-tracker-server/src/ball_tracker.py frames.bin`

## Expected output

Three centres + the final crop; exam Check passes.

## Answer submitted

See [README.md](README.md).
