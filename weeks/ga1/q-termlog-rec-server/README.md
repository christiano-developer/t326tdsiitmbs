# q-termlog-rec-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

termlog records your terminal and signs it with your Google login.
1. Install termlog, `termlog login` with your exam email. 2. `termlog rec demo.cast`.
3. Inside the recording: `curl -s "<questionData URL>"` for your challenge.
4. Decode it **using shell commands, in the same recording** (3 reversible transforms).
5. `exit` → `demo.cast` + `demo.cast.jwt`. 6. `tar -czf submission.tar.gz demo.cast demo.cast.jwt`.
7. Upload it somewhere public and submit the URL.
Hint: ROT13, hex, string reversal in some order. Code changes every 3 hours.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

Challenge from `questionData` (needs `quizSign`). termlog binary: https://github.com/mynkpdr/termlog (Rust fork of asciinema).

## Final answer

```
https://github.com/<you>/<repo>/releases/download/ga1-termlog/submission.tar.gz
```

## Status notes

Checked ✅ on 2026-10-18. The archive lives only in the `ga1-termlog` GitHub release (not committed); keep the release until grading is done.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
