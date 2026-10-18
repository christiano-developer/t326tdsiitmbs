# q-git-forensics-token-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 1.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

A staging token was committed to a repository and later rotated out. Download the history, rebuild it with
`git fast-import`, and use `git log -p`, `git log -S`, `git show` to find the commit that **introduced** the token.

Answer (JSON): `{"token": "stg_...", "commit_subject": "..."}`

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

History is served in an iframe from `questionData` (needs logged-in `quizSign`).

## Final answer

```json
{"token": "stg_2cd3a4befba1509329fa3f7a", "commit_subject": "Add staging deploy token to app config"}
```

## Status notes

Checked ✅ in Chrome on 2026-10-18. Marked solved at the user\'s request before the GA1 page was saved.
The token is a per-student exam fixture (already "rotated" in the history), not a real secret.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer

- `src/` — code · `data/` — inputs/outputs
