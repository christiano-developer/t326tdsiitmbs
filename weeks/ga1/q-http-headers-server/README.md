# q-http-headers-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 0.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-09 |
| Closed    | 2026-10-09 |

## Question

Fetch this URL, but ask for the headers too:

```
curl -i "<exam-origin>/questionData?email=<email>&quizSign=<sign>&questionId=q-http-headers-server"
```

The page body says nothing useful. Look for a header named `X-Exam-Code` — that's your answer.
The code changes every hour, so fetch it again if yours has expired.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

The exact URL (with your `quizSign`) is shown on the logged-in exam page. Copy it from there.

## Final answer

```
NNUEPJHP   (hourly code, 2026-10-09 15:57 UTC)
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
