# Final — q-llm-sentiment-analysis

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-llm-sentiment-analysis](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-llm-sentiment-analysis)

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

1. Copy the code below into a text editor.
   <details><summary>sentiment.py (click to expand)</summary>

   ```python
   import httpx

   # Exact test text (note the DOUBLE space between "qZMGqx7" and "XJHhTji3")
   TEXT = "U8jxE atNpVd TsBW qZMGqx7  XJHhTji3 D9cZtLdOsqCgM"

   response = httpx.post(
       "https://api.openai.com/v1/chat/completions",
       headers={
           "Authorization": "Bearer dummy-api-key",
           "Content-Type": "application/json",
       },
       json={
           "model": "gpt-4o-mini",
           "messages": [
               {
                   "role": "system",
                   "content": (
                       "Analyze the sentiment of the user's text. "
                       "Classify it as exactly one of: GOOD, BAD, or NEUTRAL. "
                       "Reply with only that one word."
                   ),
               },
               {"role": "user", "content": TEXT},
           ],
       },
   )
   response.raise_for_status()
   print(response.json()["choices"][0]["message"]["content"])
   ```

   </details>

2. Replace the `TEXT = "..."` value with the exact text from your question. Keep every space, including double spaces.
3. Paste the code into the answer box, then Check and Save. Nothing needs to be run.

## Final prompt

```text
Write a Python program using httpx (only httpx.post(url, json=..., headers=...), response.raise_for_status(),
response.json()) that POSTs to https://api.openai.com/v1/chat/completions with an Authorization: Bearer
dummy-api-key header and JSON body: model "gpt-4o-mini", messages = [system message asking to classify the
sentiment as GOOD, BAD, or NEUTRAL, user message = <EXACT_TEXT>]. Keep the user text byte-for-byte identical
(preserve double spaces; write newlines as \n). Print the returned message content.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

1. Get the exact text: `node src/regenerate_text.mjs <exam-email>` (needs `npm i seedrandom@3`), or copy it carefully.
2. Put it in `TEXT` in [`src/sentiment.py`](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-llm-sentiment-analysis/src/sentiment.py).
3. Validate offline (no cost): `python3 src/check.py`.
4. `pbcopy < src/sentiment.py`, then paste, Check and Save.

## Expected output

```
GOOD
PASS httpx.post() request made
... (10 checks)
PASS user message == exact text (after trim)
```

## Answer submitted (✅ passed, attempt 1)

[src/sentiment.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga0/q-llm-sentiment-analysis/src/sentiment.py), copied with `pbcopy`.
