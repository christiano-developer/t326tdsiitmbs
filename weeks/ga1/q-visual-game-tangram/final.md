# Final — q-visual-game-tangram

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-visual-game-tangram](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-visual-game-tangram)

## How to solve (for a teammate)

> Seeded per email: you get one of 100 built-in silhouettes. The grader doesn't compare pictures, it compares a
> **match key** computed from your arrangement's outline, so pieces must sit on exactly the right 1/16-unit ticks.
> Dragging until it "looks right" usually fails with *"does not match your assigned target silhouette"*.
> These scripts find your target's exact key and nudge your rough layout until the board's key equals it.

1. **Find your target.** On the logged-in exam page open DevTools → Console, paste `find-target.js` (below), press
   Enter. It prints your `target`, `TKEY = "…"` and `TP = "…"`. Copy those two lines.
2. **Rough layout.** Open the [Tangram board](https://tds-network-games.sanand.workers.dev/tangram/). Drag, rotate
   (Q/E) and flip (F) the pieces until the shape looks like your target. Orientation and flip must be right;
   position only needs to be roughly right (within ~1/8 of a unit), and the status must say "Valid candidate".
   Click **Save state** and copy the array from the "State data" box.
3. **Snap it exactly.** On the board open DevTools → Console, paste `refine.js` (below) with your `TP`, `TKEY` and
   `START` (the array from step 2) filled in at the top, press Enter. After a few seconds it prints
   `key matches: true` and loads the exact layout into the board.
   If it prints `key matches: false`, a piece is rotated/flipped wrongly or more than ~2 ticks off: fix it by eye,
   Save state again and rerun.
4. Enter your exam email in the board's **Email** box, click **Generate signed payload** (it copies the token).
5. In the exam's Tangram answer box press Cmd+V (Ctrl+V), then Check ("Correct") and Save.

<details><summary>find-target.js — run on the exam page (click to expand)</summary>

```js
// Run in the DevTools console on the logged-in exam page (exam.sanand.workers.dev/tds-2026-09-ga1).
// Finds which of the quiz's 100 built-in silhouettes is yours and prints its id, expected match key and SVG path.
// How: the quiz JS embeds the list as [{target_id, family, expected_match_key, svg_path}, ...]; we render every
// svg_path and pick the one that matches the target image shown on the page.
(async () => {
  const js = await (await fetch("/exam-tds-2026-09-ga1.js")).text();
  const start = js.indexOf("[{target_id");
  let depth = 0, i = start;
  for (; i < js.length; i++) {
    const c = js[i];
    if (c === "[" || c === "{") depth++;
    else if (c === "]" || c === "}") { if (--depth === 0) break; }
    else if (c === '"' || c === "'" || c === "`") { const q = c; i++; while (js[i] !== q) { if (js[i] === "\\") i++; i++; } }
  }
  const targets = new Function("return " + js.slice(start, i + 1))();

  const W = 768, H = 576;
  const img = [...document.querySelectorAll("img")].find((im) => im.naturalWidth === W && im.naturalHeight === H);
  const cv = Object.assign(document.createElement("canvas"), { width: W, height: H });
  const g = cv.getContext("2d", { willReadFrequently: true });
  g.drawImage(img, 0, 0);
  const shown = g.getImageData(0, 0, W, H).data;

  const scored = targets.map((t, idx) => {
    g.fillStyle = "#fff"; g.fillRect(0, 0, W, H);
    g.fillStyle = "#000"; g.fill(new Path2D(t.svg_path), "evenodd");
    const d = g.getImageData(0, 0, W, H).data;
    let bad = 0;
    for (let p = 0; p < W * H; p += 3) if ((d[p * 4] < 128) !== (shown[p * 4] < 128)) bad++;
    return { idx, bad };
  }).sort((a, b) => a.bad - b.bad);

  const mine = targets[scored[0].idx];
  console.log("target:", mine.target_id, "| mismatch px:", scored[0].bad, "| runner-up:", scored[1].bad);
  console.log("TKEY =", JSON.stringify(mine.expected_match_key));
  console.log("TP   =", JSON.stringify(mine.svg_path));
  return mine;
})();
```

</details>

<details><summary>refine.js — run on the Tangram board (click to expand)</summary>

```js
// Run in the DevTools console on the board (tds-network-games.sanand.workers.dev/tangram/).
// Fill in TP and TKEY from find-target.js, and START with a rough layout (from "Save state" after placing the
// pieces roughly by eye). The script nudges pieces tick by tick to fit the target outline, checks the board's
// own match key against TKEY, and loads the result into the board when it matches.
// State format per piece: [x, y, orientation 0-7 (x45° anticlockwise), reflected 0/1], x/y in 1/16 units,
// y measured upwards. Order: large-a, large-b, medium, small-a, small-b, square, parallelogram.
const TP = "PASTE svg_path";
const TKEY = "PASTE expected_match_key";
const START = [[134,79,2,0],[90,33,1,0],[105,16,0,0],[39,80,3,0],[135,78,5,0],[39,80,1,0],[38,79,0,0]];

(async () => {
  const base = new URL("/visual/client/tangram.js", location.origin);
  const ad = await import(new URL("../../games/tangram/adapter.js", base).href);
  const kernel = await import(new URL("../kernel.js", base).href);
  const ids = ["large-a", "large-b", "medium", "small-a", "small-b", "square", "parallelogram"];
  const asCandidate = (st) => ({ game: "tangram", game_version: "1", config_id: "standard-seven-v1", state_version: 1,
    data: { pieces: st.map(([x, y, o, r], i) => ({ id: ids[i], x, y, orientation: o, reflected: !!r })) } });
  const ta = ad.tangramAdapter, cfg = ad.TANGRAM_CONFIG;
  const keyOf = (st) => kernel.computeMatchKey(ta, ta.parseCandidate(asCandidate(st), cfg), cfg);

  // Raster fit against the target outline (2x scale, crop around the shape)
  const S = 2, CW = 768 * S, CH = 576 * S;
  const mk = () => { const c = Object.assign(document.createElement("canvas"), { width: CW, height: CH }); return c.getContext("2d", { willReadFrequently: true }); };
  const tg = mk(); tg.fillStyle = "#fff"; tg.fillRect(0, 0, CW, CH); tg.setTransform(S, 0, 0, S, 0, 0); tg.fillStyle = "#000"; tg.fill(new Path2D(TP), "evenodd");
  const T = tg.getImageData(0, 0, CW, CH).data;
  // only compare inside the target's bounding box (+ margin) to keep it fast
  let x0 = CW, y0 = CH, x1 = 0, y1 = 0;
  for (let y = 0; y < CH; y++) for (let x = 0; x < CW; x++) if (T[(y * CW + x) * 4] < 128) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  const M = 24 * S; x0 = Math.max(0, x0 - M); y0 = Math.max(0, y0 - M); x1 = Math.min(CW - 1, x1 + M); y1 = Math.min(CH - 1, y1 + M);
  const SH = { large: [[0,0],[4,0],[0,4]], medium: [[-2,0],[2,0],[0,2]], small: [[0,0],[2,0],[0,2]], square: [[0,0],[2,0],[2,2],[0,2]], para: [[0,0],[2,0],[4,2],[2,2]] };
  const KIND = ["large", "large", "medium", "small", "small", "square", "para"];
  const polys = (st) => st.map(([x, y, k, f], i) => { const a = k * Math.PI / 4, c = Math.cos(a), s = Math.sin(a);
    return SH[KIND[i]].map(([u, v]) => { if (f) u = -u; return [x / 16 + u * c - v * s, y / 16 + u * s + v * c]; }); });
  const rg = mk();
  const fit = (st, tx, ty) => {
    rg.setTransform(1, 0, 0, 1, 0, 0); rg.fillStyle = "#fff"; rg.fillRect(0, 0, CW, CH); rg.setTransform(S, 0, 0, S, 0, 0); rg.fillStyle = "#000";
    for (const p of polys(st)) { rg.beginPath(); p.forEach(([X, Y], j) => { const px = (X + tx) * 32, py = (18 - (Y + ty)) * 32; j ? rg.lineTo(px, py) : rg.moveTo(px, py); }); rg.closePath(); rg.fill(); }
    const d = rg.getImageData(0, 0, CW, CH).data; let bad = 0;
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) { const i = (y * CW + x) * 4; if ((d[i] < 128) !== (T[i] < 128)) bad++; }
    return bad;
  };

  // 1. best sub-tick translation for the rough layout (the target outline is shifted arbitrarily)
  let st = START.map((r) => r.slice()), tx = 0, ty = 0, best = Infinity;
  for (let ix = -8; ix <= 8; ix++) for (let iy = -8; iy <= 8; iy++) { const b = fit(st, ix / 128, iy / 128); if (b < best) { best = b; tx = ix / 128; ty = iy / 128; } }
  // 2. hill-climb: move single pieces up to ±2 ticks, keep improvements
  for (let round = 0; round < 8; round++) {
    let improved = false;
    for (let i = 0; i < 7; i++) for (let mx = -2; mx <= 2; mx++) for (let my = -2; my <= 2; my++) {
      if (!mx && !my) continue;
      const c = st.map((r) => r.slice()); c[i][0] += mx; c[i][1] += my;
      const b = fit(c, tx, ty); if (b < best) { best = b; st = c; improved = true; }
    }
    for (let ix = -2; ix <= 2; ix++) for (let iy = -2; iy <= 2; iy++) { const b = fit(st, tx + ix / 256, ty + iy / 256); if (b < best) { best = b; tx += ix / 256; ty += iy / 256; improved = true; } }
    if (!improved) break;
  }
  const key = await keyOf(st);
  console.log("state:", JSON.stringify(st), "| mismatch px:", best, "| key matches:", key === TKEY);
  if (key !== TKEY) { console.warn("Key differs: adjust START by eye (orientation/flip) and rerun."); return st; }

  // 3. load into the board
  const ta2 = document.querySelector("textarea");
  Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set.call(ta2, JSON.stringify(st));
  ta2.dispatchEvent(new Event("input", { bubbles: true }));
  [...document.querySelectorAll("button")].find((b) => b.textContent.trim() === "Load state").click();
  console.log("Loaded. Status:", document.getElementById("status")?.textContent);
  return st;
})();
```

</details>

## Final prompt

```text
TDS GA1 Tangram (q-visual-game-tangram). The exam page's quiz JS embeds 100 targets
{target_id, expected_match_key, svg_path}; find mine by rendering each svg_path and matching the target image.
The board (tds-network-games.sanand.workers.dev/tangram/) stores poses as [x, y, orientation, reflected] in 1/16
units (y up, 45° steps); its kernel.js computeMatchKey(adapter, candidate, config) gives the key the grader checks.
Starting from my rough "Save state" layout, fit poses to the svg_path (with a sub-tick translation search),
then confirm the board's key equals expected_match_key before loading the state and generating the signed payload.
```

- **Tool / model used:** Claude (Claude Opus 5.5) via Claude in Chrome.

## Reproduction steps (needs a clone of this repo)

1. Exam page console: run [src/find-target.js](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-visual-game-tangram/src/find-target.js)
   → `tg-100`, key in [data/target.json](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-visual-game-tangram/data/target.json).
2. Board: paste [data/solution-state.json](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-visual-game-tangram/data/solution-state.json)
   into "State data", click **Load state** (or run `src/refine.js` with the default `START`).
3. Email `ROLL_NUMBER@ds.study.iitm.ac.in` → **Generate signed payload** → paste into the exam.

## Expected output

```
target: tg-100 | mismatch px: 153 | runner-up: 6254
state: [[134,79,2,0],[91,33,1,0],[106,16,0,0],[39,80,3,0],[136,78,5,0],[39,80,1,0],[38,79,0,0]] | mismatch px: … | key matches: true
Board: Status "Valid candidate", Candidate match key 6dc467e6322ed5c0…
```

## Answer submitted (✅ Check passed)

The board's signed token for the state above (≈2,100 characters; regenerate it from the state, don't store it).
