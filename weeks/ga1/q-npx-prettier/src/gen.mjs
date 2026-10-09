// Rebuild the seeded README.md exactly as the quiz JS does (q-npx-prettier).
// Usage: EXAM_EMAIL=you@ds.study.iitm.ac.in node gen.mjs > ../data/README.md
import seedrandom from "seedrandom";

const email = process.env.EXAM_EMAIL;
if (!email) throw new Error("set EXAM_EMAIL");

const header = [
  "#  Badly  Formatted  Markdown    ",
  "",
  "*  This is an uneven list",
  "* With inconsistent spacing",
  "   *    And weird indentation",
  "",
  ">This quote has no space",
  ">   This one has too many",
  "",
].join("\n");

// Same char distribution as the quiz: 80% alnum, 19% space, 1% newline
const ALNUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const rng = seedrandom(`${email}#q-npx-prettier`);
const tail = Array.from({ length: 300 }, () => {
  const a = rng();
  return a < 0.8 ? ALNUM[Math.floor((a / 0.8) * ALNUM.length)] : a < 0.99 ? " " : "\n";
}).join("");

process.stdout.write(header + "\n" + tail);
