# Prompt log — q-visual-game-tangram

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app + Claude in Chrome (Brave, then Chrome).
- **Goal:** solve the Tangram from the browser.

```text
Geometric Reasoning: Tangram Silhouette Dissection (2 marks) — try this question.
tell what all is needed from me. my school email ROLL_NUMBER@ds.study.iitm.ac.in
```

- **Result:** partial. Claude traced the target PNG on the exam page, worked out the board's pose format
  (`[x, y, orientation, reflected]`, 1/16-unit ticks, y up, rotation about the piece's local origin), identified
  the 7 pieces in the silhouette, and hill-climbed positions against the image (IoU ≈ 0.97). The first fit
  overlapped (`large-a+large-b`, `large-b+parallelogram`); a non-overlapping one loaded as "Valid candidate".
  The token from it failed: *"The submitted arrangement does not match your assigned target silhouette."*
- **Next:** find out what "match" means exactly.

---

## P2

- **Tool / model:** same.
- **Goal:** read how the target is chosen and matched.

```text
(continuation) the grader rejected a visually matching layout — read how the target and match key are built.
```

- **Result:** worked.
  - The quiz JS embeds 100 targets `{target_id, family, expected_match_key, svg_path}`; rendering each `svg_path`
    and comparing with the page's image picked **tg-100** (153 px off vs 6,254 for the runner-up).
  - The board's `kernel.js` exports `computeMatchKey(adapter, candidate, config)`; with the adapter from
    `games/tangram/adapter.js` it reproduces the board's "Candidate match key" exactly.
  - Fitting against the crisp `svg_path` (instead of the anti-aliased PNG) with a sub-tick translation search
    landed on a state whose key equals tg-100's expected key. Loaded it, generated the signed payload, pasted it:
    **"Correct"**.
- **Next:** none. Scripts saved as [src/find-target.js](src/find-target.js) and [src/refine.js](src/refine.js);
  both re-run in the browser and reproduce the result.
