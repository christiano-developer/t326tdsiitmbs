# q-fastapi-sentiment-batch

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes (Vercel) |
| Started   | 2026-10-07 |
| Closed    | 2026-10-07 (passed on attempt 1) |

## Question

**FastAPI Batch Sentiment Analysis**: background: *FastAPI*, *REST APIs*, *CORS*.

> Build a `POST` endpoint at `/sentiment` that accepts multiple sentences and returns their sentiments (any method:
> Ollama, rule-based, ML model…). Request `{"sentences": [...]}`, response `{"results": [{"sentence": ..., "sentiment":
> "happy"|"sad"|"neutral"}, ...]}` in input order. Pass at least 7 of 10 test cases. The evaluation sends 10 random
> sentences in a single POST. Enter your FastAPI URL.

## Inputs / given data

- [data/grader_sentences.json](data/grader_sentences.json): the grader's bank of 99 labelled sentences (33 each), from the quiz JS.

## Final answer

```
https://tds-ga0-sentiment.vercel.app/sentiment
```

(The grader POSTs to the URL exactly as given, so it includes `/sentiment`.)

## Status notes

- Classifier 99/99 on the bank; local 200 rounds and live 50 rounds, worst 10/10; CORS `*`. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md) · [deploy.md](deploy.md)
- [src/sentiment.py](src/sentiment.py) — rule-based classifier · [src/main.py](src/main.py) — FastAPI app · [src/test_api.py](src/test_api.py) — grader replay
