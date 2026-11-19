# Prompts — q-ollama-faiss-rank-correlation-server

1. Read the grader: starter script calls `POST /api/embeddings` with `{"model", "prompt"}` → no prefixes.
2. Generated `dataset.json` from the exam module in Node (stubbed CDN imports) and compared with the page's blob (identical).
3. Wrote `src/rank_corr.py` (starter logic + assert ρ < 0.95); user ran it on the Mac after `ollama pull` of both models.
4. Typed the matrix into the textarea with real keystrokes → Check passed.
