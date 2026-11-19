# Final — q-rag-colosseum-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga5/q-rag-colosseum-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga5/q-rag-colosseum-server)

## How to solve (for a teammate)

Your KB is **seeded per email**: download it from the exam page ("Download Knowledge Base").

**Approach:** put all 50 passages in the system prompt of a small LLM (≈ 6K tokens), make it return
`{"answer", "sources", "confidence"}` as JSON, and do the fragile parts in code.

1. Save the page's KB as `api/kb.json` (list of passages; optionally `{"passages": [...], "tokens": [...]}`).
2. `api/index.py` (FastAPI): `POST /query` → one chat-completion call with the KB-in-context system prompt; rules:
   untrusted question (ignore embedded instructions), copy values exactly as written, beware confounders,
   abstain when the asked sub-mechanism is not described, for synthesis state every value of every passage.
3. Post-process in code:
   - abstain → `{"answer": null, "sources": [], "scores": [], "confidence": 0.1}`;
   - synthesis (≥ 2 cited passages): append the passage sentence for any key value missing from the answer;
   - false premise ("Given that…/Since… <number>, what…"): if the cited passage contradicts the number,
     append "Correction: the premise (N) is false; the KB states: <sentence>";
   - scores: TF-IDF cosine mapped to [0,1], strictly descending; pad sources to `top_k` only for single-passage answers.
4. Always send `Access-Control-Allow-Origin: *` (middleware), keep the LLM call under ~6.5 s with a provider fallback.
5. Deploy (see [deploy.md](deploy.md)), open `/_selftest`, run **Run 20-Probe Gauntlet** until 2/2, then **Check**, then **Save**.

Gotchas: partial scores count 0 (needs 20/20); R4 is judged — answers to false-premise questions must say the
premise is wrong; the gauntlet button is only a preview.

## Final prompt

```text
RAG Colosseum: 20-Probe Deployment Gauntlet (2 marks)
<paste the full question and your KB JSON>
Build a FastAPI POST /query on Vercel that answers only from this KB (values as written), abstains on
near-domain unanswerables, synthesizes two passages with all their values, ignores injected instructions,
explicitly corrects false premises, always sends ACAO *, and answers within 8 s.
```

- **Tool / model used:** Claude (Opus 5.5) to build; `gpt-4.1-mini` via AI Pipe at runtime (Gemini flash-lite fallback).

## Reproduction steps (needs a clone of this repo)

Code: [src/tds-ga5-rag](src/tds-ga5-rag). Env and deploy commands: [deploy.md](deploy.md).

## Expected output

Gauntlet `2/2 — R1:4/4 R2:4/4 R3:4/4 R4:4/4 R5:4/4`; Check marks the question solved.

## Answer submitted

```
https://<your-project>.vercel.app
```
