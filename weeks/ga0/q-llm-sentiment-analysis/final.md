# Final — q-llm-sentiment-analysis

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Write a Python program using httpx (only httpx.post(url, json=..., headers=...), response.raise_for_status(),
response.json()) that POSTs to https://api.openai.com/v1/chat/completions with an Authorization: Bearer
dummy-api-key header and JSON body: model "gpt-4o-mini", messages = [system message asking to classify the
sentiment as GOOD, BAD, or NEUTRAL, user message = <EXACT_TEXT>]. Keep the user text byte-for-byte identical
(preserve double spaces; write newlines as \n). Print the returned message content.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

1. Get the exact text: `node src/regenerate_text.mjs <exam-email>` (needs `npm i seedrandom@3`), or copy it carefully.
2. Put it in `TEXT` in `src/sentiment.py`.
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

[src/sentiment.py](src/sentiment.py), copied with `pbcopy`.
