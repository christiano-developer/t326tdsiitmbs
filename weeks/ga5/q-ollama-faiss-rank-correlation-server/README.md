# q-ollama-faiss-rank-correlation-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga5 |
| Marks     | 2 |
| Status    | solved |
| Deploy?   | no |
| Started   | 2026-11-19 |
| Closed    | 2026-11-19 |

## Question

> **Dual Embedding Alignment: Ollama, FAISS, and Rank Correlation** (2 marks)
>
> Embed the 50 corpus sentences locally with `nomic-embed-text` and `mxbai-embed-large` via Ollama, L2-normalize,
> build two `faiss.IndexFlatIP` indexes, search with the 10 evaluation queries, and for each query report the top-3
> document indices from each model plus Spearman's ρ between the two models' similarity rankings over all 50
> documents. Submit a 10×7 JSON matrix `[[a1,a2,a3,b1,b2,b3,rho], ...]`.
> Validation: indices 0–49, distinct top-3, ρ within ±0.05 of the reference, ρ < 0.95.

## Inputs / given data

- [data/dataset.json](data/dataset.json): 50 sentences + 10 queries, seeded per email (`buildStudentDataset(email)` in the exam JS).

## Final answer

```
[[48, 33, 36, 48, 36, 33, 0.8155], [8, 12, 46, 46, 12, 8, 0.6817], [25, 10, 7, 25, 7, 10, 0.7531], [38, 42, 32, 38, 42, 22, 0.5216], [37, 1, 4, 37, 4, 35, 0.643], [31, 39, 49, 31, 26, 41, 0.803], [49, 17, 45, 49, 17, 47, 0.7989], [34, 27, 13, 34, 24, 13, 0.6439], [16, 40, 15, 16, 40, 15, 0.7539], [9, 19, 18, 9, 19, 18, 0.7106]]
```
(Valid only for the dataset in `data/`; yours differs.)
