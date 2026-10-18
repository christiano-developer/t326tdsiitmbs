# q-visual-game-tangram

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

Rebuild your assigned silhouette with the seven Tangram pieces on the board at
https://tds-network-games.sanand.workers.dev/tangram/ (enter your email; drag, Q/E rotate 45°, F flip).
Click **Generate signed payload** and paste the token. The board exposes WebMCP tools
(`tangram_get_state`, `tangram_set_piece_pose`, `tangram_apply_actions`, `tangram_attest`).

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

Target = one of 100 silhouettes, index seeded from `email#q-visual-game-tangram` (shown as an SVG).

## Final answer

Signed board token (≈2,100 chars, not stored) for target **tg-100**, from this board state
([data/solution-state.json](data/solution-state.json)):

```
[[134,79,2,0],[91,33,1,0],[106,16,0,0],[39,80,3,0],[136,78,5,0],[39,80,1,0],[38,79,0,0]]
```

## Status notes

Checked ✅ in Chrome on 2026-10-18. Marked solved at the user\'s request before the GA1 page was saved.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
