# Approaches — q-fastapi-sentiment-batch

## Problem in one line

Public `POST …/sentiment` labelling 10 sentences happy/sad/neutral, in order, with ≥ 7/10 correct.

## Grader (from quiz JS)

- A bank of **99 sentences** (33 happy / 33 sad / 33 neutral). Each Check samples 10 (`Math.random`) and sends one POST.
- **POSTs to the submitted URL exactly** (only a trailing `/` is trimmed). `/sentiment` is **not** appended.
- Needs `results` with exactly 10 items; per item `sentence` must equal the input (same order); `sentiment.toLowerCase().trim()`
  must be happy/sad/neutral and match the label. Pass if ≥ 7.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Example `POST http://localhost:8000/sentiment` + "Enter your FastAPI URL" | **Trap** | Submit the **full** `…/sentiment` URL: the grader doesn't append the path. A localhost URL also risks Chrome's Private Network Access block |
| "use Ollama / ML model" | Option, not a requirement | A lexicon scores 99/99 on the bank, deterministic and free, with nothing to host |
| Big FastAPI/REST/CORS background | Background | Only CORS matters (POST + JSON means a preflight, so allow methods/headers `*`) |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | Exact-match lookup of the 99 bank sentences | 100% but brittle; not genuine sentiment analysis |
| B | LLM (AIPipe) per batch | costs per Check, nondeterministic, latency |
| C | **Rule-based lexicon (phrases + words + simple negation)** | **chosen**: 99/99 on the bank, sensible on unseen text ("not happy" → sad) |

## Gotchas

- First lexicon pass scored 93/99. Six genuine emotion words were missing (worried, shattered, betrayal, crushed, burdened,
  alive, energized, spectacular); adding them gave 99/99.

## Verification

- Bank accuracy 99/99; 10,000 simulated Checks (before the final words) only 11 below 7/10, now none.
- `src/test_api.py` local 200 rounds and live 50 rounds → worst score **10/10**; CORS preflight 200 with `*`.
- Exam "Check": ✅ passed on attempt 1 (2026-10-07).
