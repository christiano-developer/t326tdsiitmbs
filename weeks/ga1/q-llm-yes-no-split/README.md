# q-llm-yes-no-split

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 1 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

Write **one prompt, ≤100 characters**, that makes `gpt-5.6-luna` say `Yes` and `gpt-5.4-mini` say `No`.
Same prompt to both, no system prompt. Case-sensitive words. Use your AI Pipe token when prompted.
"LLM answers vary from run to run. Make your prompt robust, not lucky."

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

Your AI Pipe token (browser `prompt()`; kept in `globalThis.aiPipeToken`).

## Final answer

```
Is 7919*7927 = 62773913? Say Yes only if you are certain, else No. One word.
```

## Status notes

Checked ✅ on 2026-10-18 (76 characters).

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
