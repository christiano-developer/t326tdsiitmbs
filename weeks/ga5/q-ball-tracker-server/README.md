# q-ball-tracker-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga5 |
| Marks     | 2 |
| Status    | solved |
| Deploy?   | no |
| Started   | 2026-11-19 |
| Closed    | 2026-11-19 |

## Question

> **Track the red ball** (2 marks)
>
> 100 balls bounce around inside a circle. At the start, your ball is red. It then turns grey like all the others,
> and the balls start colliding. When the balls stop, a number appears on each one. Tell us the number on your ball
> at the end, and your ball's centre x,y in three given video frames (frames from 0; pixels from the top-left).
> Format: `42; 118,203; 260,97; 301,288`. Your video is unique to you.

## Inputs / given data

- Frames: `GET /questionData?email=<email>&quizSign=<sign>&questionId=q-ball-tracker-server` (needs the signed-in
  exam session's `quizSign`, from `localStorage.user`). Binary: 5 big-endian uint32 (fps, frameCount, f1, f2, f3)
  then `frameCount` × (uint32 length + PNG). Here: 30 fps, 726 frames, targets 211 / 348 / 592. Not committed (6.8 MB, per-user).

## Final answer

```
28; 90,265; 66,209; 308,343
```
(Valid only for this email's video.)
