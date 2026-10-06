// Regenerates the hidden eShopCo product list exactly as the GA0 grader does (exam-tds-2026-09-ga0.js)
// and sums data-discount over items whose classes include both "featured" and "sale" (= .featured.sale).
// Usage: node src/regenerate.mjs <exam-email>     (needs: npm i seedrandom@3)
import seedrandom from "seedrandom";

const email = process.argv[2];
if (!email) { console.error("usage: node src/regenerate.mjs <exam-email>"); process.exit(1); }

const n = seedrandom(`${email}#q-css-selectors-sum`);
const CLASS_SETS = ["featured sale", "sale featured", "sale", "featured", "on-sale", "featured new",
                    "sale vip", "featured sale vip", "vip sale", "new"];
const classes = Array.from({ length: 20 }, () => CLASS_SETS[Math.floor(n() * CLASS_SETS.length)]);
const discounts = Array.from({ length: 20 }, () => Math.floor(n() * 46) + 5);

let sum = 0;
classes.forEach((c, i) => {
  const parts = c.split(/\s+/);
  const hit = parts.includes("featured") && parts.includes("sale");  // same rule as .featured.sale
  if (hit) sum += discounts[i];
  console.log(`${String(i + 1).padStart(2)}  ${hit ? "✓" : " "}  <li class="${c}" data-discount="${discounts[i]}">`);
});
console.log(`\nANSWER sum of data-discount on .featured.sale: ${sum}`);
