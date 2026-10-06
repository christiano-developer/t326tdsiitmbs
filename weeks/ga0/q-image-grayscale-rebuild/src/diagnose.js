// Paste into DevTools Console in the EXAM TAB, AFTER choosing your file in the
// question's upload field. Replays the grader's exact check and explains why.
(async () => {
  const CHROME_SHA = "876038f7c47be4deab3507be7b85618fa547480309fda139529af66f1729c0c4";
  const hex = async (buf) => [...new Uint8Array(await crypto.subtle.digest("SHA-256", buf))]
    .map((x) => x.toString(16).padStart(2, "0")).join("");
  // 1. Browser
  const brave = !!(navigator.brave && (await navigator.brave.isBrave()));
  console.log("1. browser:", brave ? "BRAVE (canvas noise!)" : "not Brave", "|", navigator.userAgent);
  // 2. Canvas noise test: a solid colour must read back exactly
  const t = document.createElement("canvas");
  t.width = t.height = 64;
  const tc = t.getContext("2d");
  tc.fillStyle = "rgb(10,20,30)";
  tc.fillRect(0, 0, 64, 64);
  const td = tc.getImageData(0, 0, 64, 64).data;
  let noisy = 0;
  for (let k = 0; k < td.length; k += 4)
    if (td[k] !== 10 || td[k + 1] !== 20 || td[k + 2] !== 30) noisy++;
  console.log("2. canvas noise test:", noisy === 0 ? "clean" : noisy + " noisy pixels");
  // 3. Expected data, computed exactly like the grader
  const wo = {
    "0,0": "2,1", "0,1": "1,1", "0,2": "4,1", "0,3": "0,3", "0,4": "0,1",
    "1,0": "1,4", "1,1": "2,0", "1,2": "2,4", "1,3": "4,2", "1,4": "2,2",
    "2,0": "0,0", "2,1": "3,2", "2,2": "4,3", "2,3": "3,0", "2,4": "3,4",
    "3,0": "1,0", "3,1": "2,3", "3,2": "3,3", "3,3": "4,4", "3,4": "0,2",
    "4,0": "3,1", "4,1": "1,2", "4,2": "1,3", "4,3": "0,4", "4,4": "4,0",
  };
  const n = await createImageBitmap(await fetch("jigsaw.webp").then((r) => r.blob()));
  const s = n.width / 5, a = n.height / 5;
  const i = document.createElement("canvas");
  i.width = n.width;
  i.height = n.height;
  const u = i.getContext("2d");
  for (const [k, v] of Object.entries(wo)) {
    const [f, y] = k.split(",").map(Number), [w, b] = v.split(",").map(Number);
    u.drawImage(n, y * s, f * a, s, a, b * s, w * a, s, a);
  }
  const c = u.getImageData(0, 0, i.width, i.height).data;
  const d = new Uint8ClampedArray(c.length);
  for (let h = 0; h < c.length; h += 4) {
    const g = Math.round(0.2126 * c[h] + 0.7152 * c[h + 1] + 0.0722 * c[h + 2]);
    d[h] = d[h + 1] = d[h + 2] = g;
    d[h + 3] = c[h + 3];
  }
  const sha = await hex(d.buffer);
  console.log("3. expected sha256:", sha, sha === CHROME_SHA ? "(= Chrome reference)" : "(DIFFERS from Chrome reference)");
  // 4. The attached file, decoded exactly like the grader (<img> -> canvas)
  const input = document.getElementById("q-image-grayscale-rebuild");
  if (!input || !input.files.length) return console.warn("4. no file attached to the upload field");
  const file = input.files[0];
  const im = await new Promise((ok, err) => {
    const r = new Image(); r.onload = () => ok(r); r.onerror = err; r.src = URL.createObjectURL(file);
  });
  const o = document.createElement("canvas");
  o.width = im.width;
  o.height = im.height;
  const ox = o.getContext("2d");
  ox.drawImage(im, 0, 0);
  const yv = ox.getImageData(0, 0, o.width, o.height).data;
  let bad = 0, first = -1;
  for (let k = 0; k < d.length; k++) if (d[k] !== yv[k]) { bad++; if (first < 0) first = k; }
  console.log("4. file:", file.name, file.size, "bytes,", im.width + "x" + im.height,
    "| upload sha256:", await hex(yv.buffer));
  console.log("   mismatched bytes vs expected:", bad,
    bad ? "first at byte " + first + " (expected " + d[first] + ", got " + yv[first] + ")" : "-> grader should PASS");
})();
