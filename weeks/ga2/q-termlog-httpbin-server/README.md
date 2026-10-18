# q-termlog-httpbin-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**HTTPBin terminal lab (termlog) (2 marks)**

Complete seven HTTPBin exercises with curl in one signed `termlog rec httpbin.cast` recording (logged in as your exam email). Tag/dummy bearer token `http-48c9d2a0`, quantity `8` (seeded per email). Define `capture() { task="$1"; shift; printf '\nHTTPBIN_BEGIN <tag> %s\n' "$task"; "$@"; printf '\nHTTPBIN_END <tag> %s\n' "$task"; }` and run each request as `capture TASK curl -sS …` (no `-i`, no extra text):
GET (query course=TDS, tag; header X-Exam-Tag), POST (JSON body with number + boolean types), FORM (PUT url-encoded tag, quantity), AUTH (Bearer to /bearer), REDIRECT (/redirect-to → /get?tag=…, follow), COOKIES (set via /cookies/set into a jar outside the capture, then capture GET /cookies with the jar), STATUS (/status/400, discard body, print only the code via --write-out). `exit`, then `tar -czf submission.tar.gz httpbin.cast httpbin.cast.jwt` and submit a public URL (≤ 1 MB / 5 MB).

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
https://github.com/<you>/<repo>/releases/download/ga2-termlog-httpbin/submission.tar.gz
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
