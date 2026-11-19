# Final — q-ollama-faiss-rank-correlation-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga5/q-ollama-faiss-rank-correlation-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga5/q-ollama-faiss-rank-correlation-server)

## How to solve (for a teammate)

The dataset is **seeded per email**: download `dataset.json` from your exam page.

1. `ollama pull nomic-embed-text && ollama pull mxbai-embed-large` (Ollama running locally).
2. `python3 -m pip install faiss-cpu scipy requests numpy`
3. `python3 src/rank_corr.py path/to/dataset.json` → prints the 10×7 matrix (also `answer.json`).
4. Paste the matrix, Check, Save.

Gotchas: do **not** add nomic `search_query:`/`search_document:` prefixes; use the legacy `/api/embeddings`
endpoint like the starter; ρ is over all 50 documents.

## Final prompt

```text
Dual Embedding Alignment (2 marks)
<paste the full question + starter script>
Give me a script that reproduces the starter exactly and prints the 10x7 matrix.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

`python3 weeks/ga5/q-ollama-faiss-rank-correlation-server/src/rank_corr.py weeks/ga5/q-ollama-faiss-rank-correlation-server/data/dataset.json`

## Expected output

The matrix in [README.md](README.md); exam Check passes.

## Answer submitted

See [README.md](README.md).
