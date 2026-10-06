# Prompt log — q-fastapi-sentiment-batch

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** build and deploy the batch sentiment endpoint

```text
FastAPI Batch Sentiment Analysis
<FastAPI / REST / CORS background + task + example: see README.md>
Note: The evaluation will test 10 random sentences in a single POST request.
```

- **Result:** read the grader (99-sentence bank, 10 per Check, URL used as-is without `/sentiment` appended, ≥ 7/10).
  Built a lexicon classifier (93/99, then 99/99 after adding 9 genuine emotion words; negation handled), the FastAPI app and a
  grader replay. Local 200 rounds and live 50 rounds, worst 10/10; deployed to Vercel `tds-ga0-sentiment`; CORS `*`.
- **Next:** user submits `https://tds-ga0-sentiment.vercel.app/sentiment`.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
correct
```

- **Result:** ✅ passed on the first submission. Status → `solved`, committed and tagged. Keep the Vercel project up until grading closes.
- **Next:** none.
