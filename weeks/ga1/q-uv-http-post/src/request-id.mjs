// Print the seeded request_id shown on the quiz page (q-uv-http-post).
// Usage: EXAM_EMAIL=you@ds.study.iitm.ac.in node request-id.mjs
import seedrandom from "seedrandom";

const email = process.env.EXAM_EMAIL;
if (!email) throw new Error("set EXAM_EMAIL");

const rng = seedrandom(`${email}#q-uv-http-post`);
const HEX = "0123456789abcdef";
let id = "";
for (let i = 0; i < 8; i++) id += HEX[Math.floor(rng() * HEX.length)];
console.log(id);
