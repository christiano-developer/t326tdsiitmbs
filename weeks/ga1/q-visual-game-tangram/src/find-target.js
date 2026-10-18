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
