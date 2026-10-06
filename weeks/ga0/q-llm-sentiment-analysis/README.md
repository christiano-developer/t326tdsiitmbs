# q-llm-sentiment-analysis

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no (mock httpx in-browser; no real API call, no cost) |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**LLM Sentiment Analysis**: background: *Large Language Models* module (AIPipe proxy, `$1–2`/month allowance, base
URLs `aipipe.org/openai/v1` / `openrouter/v1`, `llm` CLI, flex processing).

> DataSentinel Inc. tests a sentiment-analysis integration with a Python harness using `httpx` to POST to OpenAI's
> API with the dummy model `gpt-4o-mini` and a dummy API key. Test text (meaningless):
>
> `U8jxE atNpVd TsBW qZMGqx7  XJHhTji3 D9cZtLdOsqCgM`
>
> Write a Python program that uses httpx to send a POST request to OpenAI's API to classify the sentiment as GOOD, BAD
> or NEUTRAL:
> - Pass an Authorization header with a dummy API key.
> - Use `gpt-4o-mini` as the model.
> - The first message must be a system message asking the LLM to analyze the sentiment, mentioning GOOD, BAD, NEUTRAL.
> - The second message must be exactly the text above.
>
> Note: this uses a dummy httpx library, not the real one. Only `httpx.get(url, **kwargs)`,
> `httpx.post(url, json=None, **kwargs)`, `response.raise_for_status()`, `response.json()` are available.

Per-user variant: the 50-char test text is seeded from the student email.

## Inputs / given data

- Exact text, regenerated from the seed: `"U8jxE atNpVd TsBW qZMGqx7  XJHhTji3 D9cZtLdOsqCgM"` (**double space** after `qZMGqx7`).

## Final answer

✅ Passed on the first submission (offline replica 10/10). Copy **from the file**: `pbcopy < src/sentiment.py`.

## Status notes

- Exam Check ✅ **passed**. No API cost (mock httpx).

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [src/sentiment.py](src/sentiment.py) — submission
- [src/check.py](src/check.py) — offline replica of the grader (exam's mock httpx + checks)
- [src/regenerate_text.mjs](src/regenerate_text.mjs) — regenerates the exact seeded text
