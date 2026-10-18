// Rebuild the seeded *valid* JSON exactly as the quiz JS does (q-broken-json-server),
// before it injects the ~20 syntax errors. The grader compares JSON.stringify(answer)
// with JSON.stringify(this), so minified output is fine.
// Usage: EXAM_EMAIL=you@ds.study.iitm.ac.in node valid.mjs > ../data/fixed.json
import seedrandom from "seedrandom";

const email = process.env.EXAM_EMAIL;
if (!email) throw new Error("set EXAM_EMAIL");

const SCENARIOS = ["configuration settings", "API records", "database records", "log entries"];
const rng = seedrandom(`${email}#q-broken-json-server`); // version "" for this GA
const dataType = SCENARIOS[Math.floor(rng() * SCENARIOS.length)];
const pad = (n) => String(n).padStart(2, "0");

// Field order and rng call order must match the quiz exactly
const records = [];
for (let d = 0; d < 300; d++) {
  records.push({
    id: `record_${String(d).padStart(5, "0")}`,
    name: `Entry ${d}`,
    value: Math.floor(rng() * 1e4),
    status: rng() < 0.5 ? "active" : "inactive",
    category: ["alpha", "beta", "gamma", "delta"][Math.floor(rng() * 4)],
    timestamp: `2024-${pad(Math.floor(rng() * 12) + 1)}-${pad(Math.floor(rng() * 28) + 1)}T${pad(Math.floor(rng() * 24))}:${pad(Math.floor(rng() * 60))}:00Z`,
    metadata: {
      source: ["system_a", "system_b", "system_c"][Math.floor(rng() * 3)],
      priority: Math.floor(rng() * 5) + 1,
      tags: ["tag1", "tag2", "tag3"].slice(0, Math.floor(rng() * 3) + 1),
    },
    description:
      `This is a sample ${dataType} entry with sufficient text to ensure the JSON file is large enough. `.repeat(3),
  });
}
process.stdout.write(JSON.stringify(records));
