# Approaches — q-ball-tracker-server

## Problem in one line

Decode the frame binary, segment ball interiors by palette colour (outlines keep touching balls apart), track by
frame-to-frame Hungarian assignment, read the final number from a crop.

## ⚠️ Distractors, gotchas and hidden text

| Item | Type | Reality |
|------|------|---------|
| Make my video | Distractor | The page only re-encodes the PNG frames to WebM; use the raw frames instead (exact pixels, no codec blur). |
| Red fades | Gotcha | Red → grey over frames 34–56 through intermediate colours; motion starts at frame 60. Identify the ball in frame 0. |
| Detection | Gotcha | Distance-transform / disk-correlation peaks gave 99–108 "balls". Palette is only 4–5 colours (bg 250, outline 90, container 40, fill 150, red, digits 255): interior = not bg/outline/container → exactly 100 components every frame. |
| Motion | Trap | Dense elastic gas (≈ 7–9 px/frame, collisions almost every frame); constant-velocity prediction is *worse* than none and diverged after frame 603. |
| Robustness | Check | Zero-motion, half-velocity and 4-substep physics predictors all agreed on the red ball through all three target frames; the final number was read visually (28). |

## Verification

- Exam Check passed (2/2) on 2026-11-19.
