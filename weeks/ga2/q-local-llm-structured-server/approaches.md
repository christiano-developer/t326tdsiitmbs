# Approaches — q-local-llm-structured-server

## Problem in one line

Ollama `/api/chat` with a JSON-schema `format` and temperature 0 picks the fields; the model copies the amount *as written* and code parses it locale-aware and reconciles it with the numbers in the text; Pydantic validates; bad input → 422, LLM down → 503.

## ⚠️ Distractors, gotchas and hidden text

| Item | Type | Reality |
|------|------|---------|
| European decimal comma | Gotcha (cost a Check) | An invoice wrote `129,25`; asking the model for a "plain number" produced `12925`. Fixed by having it copy the amount as written and parsing `,`/`.` in code (last separator + 1–2 digits = decimal). |
| Due date vs invoice date | Genuine | Prompt asks explicitly for the *payment due* date and the *total due* amount. |
| Garbage input | Genuine | Custom `RequestValidationError` handler + empty/symbol-only check → 422, never 500. |

Scanned the question HTML for hidden elements/comments: none found.

## Verification

- Exam **Check** passed on 2026-10-18 (run by the user on their Mac; tunnels/recordings are local).
