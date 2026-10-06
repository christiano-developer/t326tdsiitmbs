import seedrandom from "seedrandom";
import { sampleVariance } from "simple-statistics";
import fs from "fs";
const file = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const gen = (seed) => { const n = seedrandom(seed); const l = n()*50+25;
  return Array.from({length:1000}, () => Math.floor(Math.max(0, l + (n()*40-20)))); };
for (const email of [process.argv[3], "", "undefined"]) {
  const s = gen(`${email}#q-calculate-variance`);
  const same = s.length === file.length && s.every((v,i) => v === file[i]);
  console.log(JSON.stringify(email||"(empty)").padEnd(40), "expected", sampleVariance(s).toFixed(2), "| matches file:", same, "| first5", s.slice(0,5).join(","));
}
console.log("file".padEnd(40), "variance", sampleVariance(file).toFixed(2), "| first5", file.slice(0,5).join(","));
