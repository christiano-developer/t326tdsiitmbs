// Regenerates the exact seeded test text as the GA0 grader does. Usage: node src/regenerate_text.mjs <exam-email> (npm i seedrandom@3)
import seedrandom from "seedrandom";
const ne = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const n = seedrandom(`${process.argv[2]}#q-llm-sentiment-analysis`);
const se = (t, o) => Array.from({ length: t }, () => { const e = o(); return e < .8 ? ne[Math.floor(e / .8 * ne.length)] : e < .99 ? " " : "\n"; });
const l = se(50, n).join("").trim();
console.log(JSON.stringify(l));
