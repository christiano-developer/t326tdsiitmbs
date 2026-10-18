# Final — q-cosine-similarity-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-cosine-similarity-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-cosine-similarity-server)

## How to solve (for a teammate)

> Seeded per email: your documents, queries and answer differ from mine.

1. On the exam page click **Download q-cosine-similarity-server.json** (≈525 KB: 250 documents and 10 queries,
   each with a 64-number `embedding`).
2. Save the script below as `cosine.mjs` in the same folder (Node 18+, no packages).
3. Run `node cosine.mjs q-cosine-similarity-server.json > answer.json`.
4. Paste the contents of `answer.json` into the answer box, then Check (it should say 10/10) and Save.

<details><summary>cosine.mjs (click to expand)</summary>

```js
import { readFileSync } from "node:fs";

export function topK(task, k = 5) {
  const norm = (v) => Math.sqrt(v.reduce((s, x) => s + x * x, 0));
  const docs = task.documents.map((d) => ({ id: d.doc_id, e: d.embedding, n: norm(d.embedding) }));
  const out = {};
  for (const q of task.queries) {
    const qn = norm(q.embedding);
    const scored = docs.map((d) => ({
      id: d.id,
      s: Math.round((d.e.reduce((a, x, i) => a + x * q.embedding[i], 0) / (qn * d.n)) * 1e12) / 1e12,
    }));
    scored.sort((a, b) => b.s - a.s || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
    out[q.query_id] = scored.slice(0, k).map((x) => x.id);
  }
  return out;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const task = JSON.parse(readFileSync(process.argv[2] ?? "q-cosine-similarity-server.json", "utf8"));
  process.stdout.write(JSON.stringify(topK(task), null, 2) + "\n");
}
```

</details>

## Final prompt

```text
q-cosine-similarity-server.json has documents[{doc_id, embedding}] and queries[{query_id, embedding}] (64-dim).
Write a Node script that, for each query, computes cosine similarity to every document, sorts descending with
ties broken by the smaller doc_id, and prints JSON {"Q001": [5 doc_ids], ...} for all queries.
```

- **Tool / model used:** Claude (Claude Opus 5.5) via Claude in Chrome.

## Reproduction steps (needs a clone of this repo)

1. Download `q-cosine-similarity-server.json` from the exam page into `weeks/ga1/q-cosine-similarity-server/data/`.
2. Run:

```bash
cd weeks/ga1/q-cosine-similarity-server/src
node cosine.mjs ../data/q-cosine-similarity-server.json | node -e '
  const a=JSON.parse(require("fs").readFileSync(0,"utf8"));
  const b=JSON.parse(require("fs").readFileSync("../data/answer.json","utf8"));
  console.log(JSON.stringify(a)===JSON.stringify(b) ? "same" : "DIFFERENT")'
```

## Expected output

```
same
```

## Answer submitted (✅ Check passed, 10/10)

```json
{
  "Q001": ["D000036", "D000131", "D000236", "D000196", "D000186"],
  "Q002": ["D000112", "D000232", "D000077", "D000052", "D000007"],
  "Q003": ["D000203", "D000068", "D000043", "D000183", "D000063"],
  "Q004": ["D000034", "D000059", "D000149", "D000194", "D000044"],
  "Q005": ["D000005", "D000165", "D000150", "D000125", "D000015"],
  "Q006": ["D000006", "D000231", "D000061", "D000076", "D000241"],
  "Q007": ["D000102", "D000132", "D000197", "D000007", "D000157"],
  "Q008": ["D000038", "D000058", "D000138", "D000228", "D000128"],
  "Q009": ["D000084", "D000229", "D000119", "D000244", "D000154"],
  "Q010": ["D000055", "D000220", "D000235", "D000200", "D000195"]
}
```
