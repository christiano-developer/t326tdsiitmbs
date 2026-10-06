# Approaches — q-llm-sentiment-analysis

## Problem in one line

Write an `httpx.post` call to the chat-completions endpoint with the right header, model and messages, where the user
message is the exact seeded text.

## Grader (from quiz JS)

- Text: `se(50, seedrandom(email#q-llm-sentiment-analysis)).join("").trim()`. Each char is a letter/digit (80%),
  a space (19%) or a **newline (1%)**.
- Runs the submission in Pyodide with a **mock `httpx`**. `post(url, json=None, headers=None, **kwargs)` records
  `{method, url, json, headers}` and returns `{"choices":[{"message":{"content":"GOOD"}}]}`. **No network, no cost.**
- Checks, in order: POST was made → URL ends with `/v1/chat/completions` → `headers.Authorization` present → `json=`
  body → `model == "gpt-4o-mini"` → exactly 2 messages → roles `system`, `user` → system content contains `GOOD`,
  `BAD`, `NEUTRAL` → `user_content.trim() === text`.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| The displayed test text | **Trap** | Exact-match check, and the text can contain **double spaces or newlines**. HTML rendering and copy-paste can collapse them. Mine has a double space (`qZMGqx7  XJHhTji3`); a single space fails (confirmed) |
| "send a POST request to OpenAI's API" | Clarification | It's a mock. Any URL ending in `/v1/chat/completions` passes; nothing is sent |
| AIPipe base URLs / `openai/gpt-4.1-nano` model names in the background | **Distractor** | The model must be exactly `gpt-4o-mini` (no `openai/` prefix). The AIPipe URL would also pass, but isn't needed |
| "dummy httpx" API list | Genuine | Use keyword `headers=` and `json=`. The mock reads them by name |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | Copy the text from the page into the code | Risky: whitespace may be collapsed |
| B | **Regenerate the exact text from the seed, hard-code it with the double space, validate with the offline mock** | **chosen** |

## Chosen: B

**Why:** removes the only real risk (exact whitespace). The program uses only the four allowed mock APIs.

## Gotchas

- Copy the submission from the file (`pbcopy`). The double space must survive.
- If a variant's text contains a newline, write it as `\n` inside the Python string.

## Verification

- `python3 src/check.py` → 10/10 PASS (prints the mock reply `GOOD`).
- Negative control: same code with a single space → FAIL on the exact-text check.
- Cost: none (mock; no AIPipe calls).
- Exam "Check" button: ✅ passed on attempt 1 (2026-10-06).
