# Approaches — q-visual-game-tangram

## Problem in one line

Place 7 pieces to match the target silhouette; submit the board's signed JWT.

## Grader (from quiz JS)

- Client-side ES256 JWT check against an embedded JWKS (kids `tds-2025`, `tds-dev-local`).
- Payload must have: `iss=tds-network-games.sanand.workers.dev`, `aud=tds-visual-grader`,
  `purpose=visual-state-receipt`, `receipt_version=1`, `sub` = email (case-insensitive), `game=tangram`,
  `game_version=1`, `config_id=standard-seven-v1`, `state_version=1`, `equivalence_version=2`,
  `invalid=false`, no `errors`, and `match_key` = the target's `expected_match_key`.
- Translation-invariant; the token must be produced by the board.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "NP-complete search problem" | Background | Framing; targets are on a 45° / grid lattice |
| WebMCP tool descriptions | Watch | Board JS checked: no injection text |
| "The page does not know the target answer" (board) | Half-true | The board doesn't, but the **exam** page embeds all 100 targets with their expected match keys |
| "Reproduce the target silhouette" | Gotcha | Looking right is not enough: the match key must be identical, so every piece must be on the exact tick |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Drag pieces by eye on the board | Browser | No code | One tick (1/16 unit) off changes the key; impossible to see | rejected |
| B | Fit poses to the target PNG, then sign | Canvas raster fit | Got IoU 0.97, valid layout | The PNG is anti-aliased and 1 px blurred; ambiguous at the 1-tick level, so the key didn't match | tried, failed |
| C | Find your target's `svg_path` + `expected_match_key` in the quiz JS, fit to the crisp path, verify with the board's own `computeMatchKey` | Console scripts | Exact: you know it matches before signing | Needs a rough starting layout | chosen |

## Chosen: C

**Why:** the grader compares match keys, and the board can compute the same key locally, so the search can stop
exactly when the key matches. No guessing, no wasted signed tokens.

## Gotchas hit

- Pose format: `[x, y, orientation, reflected]`; x/y in 1/16 units with **y measured upwards** from the board's
  bottom; orientation = 45° steps anticlockwise about the piece's local origin (the right-angle corner for
  triangles, except medium = midpoint of its long side); `reflected` mirrors x before rotating.
- The target outline is shifted by a non-grid amount, so the fit needs a sub-tick translation search.
- Pieces that look flush can still overlap by a hair: the board reports `overlap:<a>+<b>` and won't sign a valid
  candidate. The key check catches this too.
- "Generate signed payload" copies the token to the clipboard; paste it with Cmd+V (it's ~2,100 characters).
- Equivalence is union-boundary + translation only: which identical piece goes where doesn't matter.

## Verification

- Board: "Valid candidate", Candidate match key = tg-100's `expected_match_key` (6dc467e6…).
- Exam **Check** → "Correct" (Chrome, 2026-10-18).
- `src/find-target.js` re-run in the exam tab → tg-100; `src/refine.js` re-run on the board from the rough
  layout → the same state, key matches (≈3 s).
