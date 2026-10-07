# Question folder

| File | Purpose |
|------|---------|
| `README.md` | question text, marks, status, final answer, status notes |
| `prompts.md` | append-only log of every prompt, with its result |
| `approaches.md` | grader notes, distractors and hidden text, options, choice, verification |
| `final.md` | teammate how-to, final prompt, reproduction steps, expected output |
| `deploy.md` | *deploy questions*: local run → test → deploy → configure → verify → teardown |
| `.env.example` | *deploy questions*: variable **names** only; values stay in git-ignored `.env` |
| `src/`, `data/` | code; inputs and outputs |

## Status values

| Status | Meaning |
|--------|---------|
| `todo` | scaffolded |
| `in-progress` | being worked on |
| `solved` | verified on the exam page |
| `set-aside` | parked, with next step noted |
| `cant-approach` | blocked, with the blocker noted |

## Secrets

- Never commit `.env`, tokens or keys.
- Personal values needed by a CI job (like the exam email) live in **repository variables**, not files.
