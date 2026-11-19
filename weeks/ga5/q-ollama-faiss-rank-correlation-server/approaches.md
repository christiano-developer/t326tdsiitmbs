# Approaches — q-ollama-faiss-rank-correlation-server

## Problem in one line

Run the exam's own starter script unchanged against local Ollama (plain `/api/embeddings`, no task prefixes).

## ⚠️ Distractors, gotchas and hidden text

| Item | Type | Reality |
|------|------|---------|
| nomic task prefixes (`search_query:` / `search_document:`) | Trap | The reference uses plain prompts; adding prefixes moves ρ. Match the starter script exactly. |
| ρ over what | Genuine | Spearman over the 50 per-document similarity scores (aligned by doc index), not over the top-3. |
| Same model twice | Guard | ρ ≥ 0.95 fails; the script asserts it. |
| Where to run | Gotcha | The chat's sandbox / device VM cannot reach the Mac's `localhost:11434`; run the script in the Mac terminal. |

## Verification

- Exam Check passed (2/2) on 2026-11-19; the dataset in `data/` was regenerated from the exam JS and matched the page's download.
