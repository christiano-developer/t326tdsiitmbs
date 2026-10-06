// Paste into DevTools Console ON THE EXAM PAGE, in plain Chrome (not Brave:
// its fingerprinting protection adds noise to canvas reads).
// Runs the grader's exact logic with this browser's own WebP decoder, then:
//  1. self-checks the PNG round-trip (<img> -> canvas, like the grader),
//  2. attaches the PNG directly to the question's file input,
//  3. downloads a copy with a unique, timestamped name.
(async () => {
  const wo = {
    "0,0": "2,1", "0,1": "1,1", "0,2": "4,1", "0,3": "0,3", "0,4": "0,1",
    "1,0": "1,4", "1,1": "2,0", "1,2": "2,4", "1,3": "4,2", "1,4": "2,2",
    "2,0": "0,0", "2,1": "3,2", "2,2": "4,3", "2,3": "3,0", "2,4": "3,4",
    "3,0": "1,0", "3,1": "2,3", "3,2": "3,3", "3,3": "4,4", "3,4": "0,2",
    "4,0": "3,1", "4,1": "1,2", "4,2": "1,3", "4,3": "0,4", "4,4": "4,0",
  };
  const blob = await fetch("jigsaw.webp").then((r) => r.blob());
  const n = await createImageBitmap(blob);
  const s = n.width / 5, a = n.height / 5;
  const cv = document.createElement("canvas");
  cv.width = n.width;
  cv.height = n.height;
  const u = cv.getContext("2d");
  for (const [k, v] of Object.entries(wo)) {
    const [f, y] = k.split(",").map(Number);
    const [w, b] = v.split(",").map(Number);
    u.drawImage(n, y * s, f * a, s, a, b * s, w * a, s, a);
  }
  const img = u.getImageData(0, 0, cv.width, cv.height);
  const d = img.data;
  for (let h = 0; h < d.length; h += 4) {
    const g = Math.round(0.2126 * d[h] + 0.7152 * d[h + 1] + 0.0722 * d[h + 2]);
    d[h] = d[h + 1] = d[h + 2] = g;
  }
  u.putImageData(img, 0, 0);
  const png = await new Promise((r) => cv.toBlob(r, "image/png"));
  // Self-check: decode back through <img> + canvas, like the grader
  const im = new Image();
  im.src = URL.createObjectURL(png);
  await im.decode();
  const c2 = document.createElement("canvas");
  c2.width = im.width;
  c2.height = im.height;
  const x2 = c2.getContext("2d");
  x2.drawImage(im, 0, 0);
  const back = x2.getImageData(0, 0, c2.width, c2.height).data;
  let bad = 0;
  for (let k = 0; k < d.length; k++) if (d[k] !== back[k]) bad++;
  console.log("round-trip mismatched bytes:", bad, bad === 0 ? "OK" : "PROBLEM");
  const ts = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15);
  const name = "grayscale-chrome-" + ts + ".png";
  const file = new File([png], name, { type: "image/png" });
  // Attach to the question's upload field (id = question id)
  const input = document.getElementById("q-image-grayscale-rebuild");
  if (input) {
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    input.dispatchEvent(new Event("change", { bubbles: true }));
    console.log("attached to upload field:", name, "- now click Check");
  } else {
    console.warn("upload field not found; upload the downloaded file");
  }
  const link = document.createElement("a");
  link.href = im.src;
  link.download = name;
  link.click();
})();
