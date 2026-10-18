# Approaches — q-cosine-similarity-server

## Problem in one line

Top-5 cosine neighbours per query over given embeddings.

## Grader (from quiz JS)

- Client checks: valid JSON object. Then **server-side** `/backendVerify` (data seed is client-side, so the
  server can recompute).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| SVG example IDs (`D000151…`) | Background | Illustrative only |
| Ask-AI "how do I compute embeddings" | Distractor | No embedding API needed; embeddings are given |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Plain JS: dot products, sort desc, tie-break on doc_id | Node / browser JS | No deps; runs in the exam tab | None at this size (2,500 dot products) | chosen |
| B | numpy `D @ q` + `argsort` (the page's hint) | Python + numpy | Short | `argsort` alone ignores the doc_id tie-break rule | fallback |

## Chosen: A

**Why:** tiny workload, and it could run in the tab without downloading the 525 KB file.

## Gotchas hit

- Embeddings are already unit-normalised (checked: norms = 1.000000), but the script still divides by norms, so
  it's correct for any input.
- Similarities are rounded to 1e-12 before sorting so floating-point noise can't break an exact tie.
- No near-ties at the top-5 boundary in this seed (smallest gap between 5th and 6th: 0.000055).
- The "Download" button builds the file in the page (`blob:`), so it can be captured with `URL.createObjectURL`.

## Verification

- Exam **Check** → "Cosine similarity search verified: 10/10 queries matched exactly. ✅" (Brave and Chrome, 2026-10-18).
- `topK()` from `src/cosine.mjs`, run in the tab on the live task file, equals the submitted JSON.
