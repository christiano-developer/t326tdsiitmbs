# q-rag-colosseum-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga5 |
| Marks     | 2 |
| Status    | solved |
| Deploy?   | yes |
| Started   | 2026-11-19 |
| Closed    | 2026-11-19 |

## Question

> **RAG Colosseum: 20-Probe Deployment Gauntlet (50-Passage Knowledge Base)** (2 marks)
>
> Deploy a RAG system that the exam server probes with 20 questions across 5 rounds. It must retrieve from a
> personalized knowledge base of 50 technical passages (5 domains: Distributed Systems, ML, Databases, Networking,
> Security), navigate confounder passages (Raft vs Multi-Paxos, SGD vs AdamW, Postgres MVCC vs MySQL undo logs…),
> extract factual answers, abstain on near-domain unanswerable queries, synthesize cross-boundary chunks, resist
> stealth prompt injections, and handle concurrent load.
>
> `POST /query` `{"question": "...", "top_k": 3}` → `{"answer": str|null, "sources": [int], "scores": [float], "confidence": float}`
> - `answer` null/"" when abstaining; `sources` 0-based KB indices by descending score, `[]` when abstaining;
>   `scores` same length, descending, in [0,1]; `confidence` < 0.4 when abstaining, > 0.6 when answering.
> - ≤ 8 s per request; `Access-Control-Allow-Origin: *` must be present.
> - Submit the public base URL (without `/query`).

## Inputs / given data

- KB: 50 passages generated client-side from the email (`generateKB(email)` in the exam JS, seeded
  `<email>#rag-colosseum-server`). Values are deliberately *wrong vs the real world* (e.g. Redis on port 27017).
  Copy in [src/tds-ga5-rag/api/kb.json](src/tds-ga5-rag/api/kb.json) (passages + per-passage token values).

## Final answer

```
https://<your-project>.vercel.app
```

Gauntlet: **2/2 — R1 4/4, R2 4/4, R3 4/4, R4 4/4, R5 4/4**. Q1 is all-or-nothing in the header: anything below
2/2 shows "Incorrect. Try again." and counts 0.
