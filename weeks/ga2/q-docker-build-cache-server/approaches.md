# Approaches — q-docker-build-cache-server

## Problem in one line

For five independent changes, list which Dockerfile steps (L1–L5) re-execute and their total cost; host the JSON publicly.

## Grader (from quiz JS)

- `Se(email)` seeds costs: install `40 + h%31`, compile `10 + h%11`, test `15 + h%16` (h = FNV-1a of lower-cased email). Here 55 / 10 / 15.
- Checking is server-side (`/backendVerify` GETs the URL).

## Cache rules used

| Instruction | Cache key | Notes |
|-------------|-----------|-------|
| `COPY` | checksum of the copied files' contents (+ mode/ownership) | mtime is **not** part of the checksum; `.dockerignore`d files never enter the context |
| `RUN` | instruction text + parent layer | file changes in the context don't affect a RUN directly |
| any | parent layer | once one step misses, all later steps re-run (stated in the question) |

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| `--no-cache-dir` | Distractor | pip's download cache only, not Docker layers (the question says so). |
| `touch src/app.py` (C) | Trap | mtime-only change → COPY checksum unchanged → all hits. |
| README.md edit (D) | Trap | Excluded by `.dockerignore` → not in context → all hits. |
| `-q` flag (E) | Genuine | New RUN text → L4 misses, L5 follows. L1–L3 hit. |

Scanned for hidden text: none found.

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | Reason from BuildKit cache rules, encode as a tiny script (first miss → tail of steps, sum costs) | chosen |
| B | Actually build a test image 5× and read `CACHED` lines | possible check, not needed |

## Result

| Case | First miss | Steps | Seconds |
|------|-----------|-------|---------|
| A | L3 | L3 L4 L5 | 0+10+15 = 25 |
| B | L1 | L1 L2 L3 L4 L5 | 55+10+15 = 80 |
| C | — | — | 0 |
| D | — | — | 0 |
| E | L4 | L4 L5 | 25 |

## Gotchas hit

- Include zero-cost COPY steps (L1, L3) in `steps` when they re-run.

## Verification

`python3 src/cache_model.py 55 10 15` → [data/answer.json](data/answer.json); costs re-derived from `Se()`.
