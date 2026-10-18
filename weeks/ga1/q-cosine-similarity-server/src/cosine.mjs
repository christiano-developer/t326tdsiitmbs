// Top-5 documents per query by cosine similarity, ties broken by smaller doc_id.
// Usage: node cosine.mjs ../data/q-cosine-similarity-server.json > ../data/answer.json
// Input = the per-email file from the exam page's "Download q-cosine-similarity-server.json" button.
import { readFileSync } from "node:fs";

export function topK(task, k = 5) {
  const norm = (v) => Math.sqrt(v.reduce((s, x) => s + x * x, 0));
  const docs = task.documents.map((d) => ({ id: d.doc_id, e: d.embedding, n: norm(d.embedding) }));
  const out = {};
  for (const q of task.queries) {
    const qn = norm(q.embedding);
    const scored = docs.map((d) => ({
      id: d.id,
      // round to 1e-12 so float noise can't break an exact tie
      s: Math.round((d.e.reduce((a, x, i) => a + x * q.embedding[i], 0) / (qn * d.n)) * 1e12) / 1e12,
    }));
    scored.sort((a, b) => b.s - a.s || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
    out[q.query_id] = scored.slice(0, k).map((x) => x.id);
  }
  return out;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const task = JSON.parse(readFileSync(process.argv[2] ?? "../data/q-cosine-similarity-server.json", "utf8"));
  process.stdout.write(JSON.stringify(topK(task), null, 2) + "\n");
}
