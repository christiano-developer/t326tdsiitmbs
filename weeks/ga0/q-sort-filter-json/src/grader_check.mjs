// Regenerates the seeded catalog + threshold and runs the grader's exact check on an answer.
// Usage: node src/grader_check.mjs <exam-email> data/products.json data/answer.min.json   (npm i seedrandom@3)
import seedrandom from "seedrandom"; import fs from "fs";
const n = seedrandom(`${process.argv[2]}#q-sort-filter-json`), l = h => h[Math.floor(n() * h.length)];
const s = ["Electronics","Apparel","Books","Home","Toys"], a = ["Super","Ultra","Eco","Smart","Deluxe","Mini","Pro"], i = ["Widget","Gadget","Device","Kit","Set","Tool","Item"];
const u = Array.from({length:100}, () => ({category:l(s), price:Number((20+n()*180).toFixed(2)), name:`${l(a)} ${l(i)}`}));
const c = Number((50+n()*100).toFixed(2));
const d = u.filter(h => h.price >= c).sort((h,g) => h.category.localeCompare(g.category) || g.price - h.price || h.name.localeCompare(g.name));
const given = JSON.parse(fs.readFileSync(process.argv[3])), mine = JSON.parse(fs.readFileSync(process.argv[4]));
console.log("threshold", c, "| data matches paste:", JSON.stringify(u) === JSON.stringify(given));
const ok = mine.length === d.length && mine.every((f,y) => f.category===d[y].category && f.price===d[y].price && f.name===d[y].name);
console.log("grader check on my answer:", ok, `(${mine.length}/${d.length})`);
