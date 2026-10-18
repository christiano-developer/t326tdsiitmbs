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
