# t326tdsiitmbs

Coursework and assignments for **Tools in Data Science (TDS)**, Sep 2026 term, IITM BS.

- Course: https://tds.s-anand.net/
- Exams: `https://exam.sanand.workers.dev/tds-2026-09-<ga0..ga8|p1|p2>`

| Component | Weight | Date |
|-----------|--------|------|
| GA0–GA8 (best 7 of 9) | 20% | weekly |
| Project 1 | 20% | 2026-11-09 |
| ROE (45 min) | 20% | 2026-11-29 |
| Project 2 | 20% | 2026-12-13 |
| End-term (in person) | 20% | 2027-01-10 |

---

## 1. Approach

The goal is **reproducibility**. For every question the repo records:

1. what was asked,
2. every prompt tried (including failures),
3. the approaches considered and why one was chosen,
4. **one final prompt + steps that reproduce the answer from scratch**,
5. for deploy/server/external-config questions, the exact commands and a guide to get it running.

Each question is a self-contained folder. Each section (GA, project, ROE) is a branch.
Each question ends in exactly one commit, and each commit gets its own tag.

---

## 2. Layout

```
README.md                  this file: approach, rules, workflow
CMDS.md                    running list of commands (updated constantly)
templates/
  question/                README.md, prompts.md, approaches.md, final.md
  deploy/                  deploy.md, .env.example
scripts/new-question.sh    scaffolds a question folder from templates/
weeks/ga0 … ga8/           one folder per GA (ga0 = GA0)
projects/p1, p2/           one folder per requirement
roe/                       one folder per ROE question
```

Every section folder has a `README.md` tracking table:
`| Question | Marks | Deploy | Status | Answer |`

### Question folder

| File | Purpose |
|------|---------|
| `README.md` | question text, marks, status, final answer, status notes |
| `prompts.md` | append-only log of every prompt, with its result |
| `approaches.md` | options considered, choice + reason, gotchas, verification |
| `final.md` | **single consolidated prompt + reproduction steps + expected output** |
| `deploy.md` | *deploy/server/external-config questions only*: local run → test → deploy → dashboard config → verify → keep-alive → teardown |
| `.env.example` | *deploy only*: env var **names**; values live in git-ignored `.env` |
| `src/`, `data/` | code; inputs and outputs |

---

## 3. Rules for agents (and me)

### 3.1 Edit scope

While working on question `<section>/<q-id>`, only these may be changed:

- `<section>/<q-id>/**`
- that question's row in `<section>/README.md`
- `CMDS.md`, **append only**, when a new command is used

Anything else (other questions, `templates/`, `scripts/`, this README) needs **explicit permission** first.

### 3.2 No action without a go-ahead

Propose first, execute only after approval. This covers scaffolding, deploying, committing, branching and merging.

### 3.3 Secrets

Never commit `.env`, tokens or keys. Only `.env.example` with names.

---

## 4. Branches

| Section | Branch |
|---------|--------|
| GA0 … GA8 | `ga0` … `ga8` |
| Project 1 / 2 | `project-p1`, `project-p2` |
| ROE | `roe` |
| Revisit a closed section | `<branch>-revisit`, e.g. `ga0-revisit` |

- Branch from `main`.
- Merge into `main` **only when the section is complete**, using `git merge --no-ff` so per-question commits stay visible.
- A section is **complete** when every question has status `solved`, `set-aside` or `cant-approach`.
- **No direct commits to `main`**, except repo-level files (`README.md`, `CMDS.md`, `templates/`, `scripts/`, `.gitignore`).

---

## 5. Commits

**One commit per question, made only when the question reaches a final status.**
No work-in-progress commits. The commit type must match the `Status` field in the question's `README.md`.

| Type | When | Required before committing |
|------|------|----------------------------|
| `solved` | answer verified and saved on the exam page | `final.md` reproduces the answer; `Final answer` filled |
| `set-aside` | parked on purpose, to come back later | `Status notes`: where it stopped and the next step |
| `cant-approach` | attempted but blocked | `Status notes`: the blocker and what was tried |

Message format:

```
<type>(<section>/<q-id>): <one-line summary>

e.g.
solved(ga0/q-fastapi): GET /api endpoint deployed on Vercel
set-aside(ga0/q-dbt-operations-dashboard): mart layer pending
cant-approach(roe/q07): needs paid API, no access
```

A set-aside question solved later gets its own `solved(...)` commit, on the `-revisit` branch if the section is already merged.

### Authorship

Every commit records **who** made it and **which LLMs/agents** helped:

- **Author**: the GitHub user `christiano-developer`, taken from `git config user.name` / `user.email`.
  Never override the author with an agent identity.
- **Co-authors**: add one `Co-Authored-By:` trailer for **each** LLM or agent used on that question,
  matching the tools listed in its `prompts.md`. Agents must add their own trailer when they commit.

| LLM / agent | Trailer |
|-------------|---------|
| Claude Code / Claude (Opus 5.5) | `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` |
| Claude (other model) | `Co-Authored-By: Claude <model> <noreply@anthropic.com>` |
| ChatGPT | `Co-Authored-By: ChatGPT <model> <noreply@openai.com>` |
| Gemini / Google AI mode | `Co-Authored-By: Gemini <model> <noreply@google.com>` |
| Grok | `Co-Authored-By: Grok <model> <noreply@x.ai>` |
| Perplexity | `Co-Authored-By: Perplexity <model> <noreply@perplexity.ai>` |
| Ollama (local) | `Co-Authored-By: Ollama <model> <noreply@ollama.com>` |
| No AI used | no trailer; add the line `AI: none` to the body instead |

Full commit message:

```
solved(ga0/q-fastapi): GET /api endpoint deployed on Vercel

Approach: FastAPI on Vercel serverless; see final.md

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Co-Authored-By: ChatGPT <model> <noreply@openai.com>
```

Trailers go at the very end, after one blank line, one per line. GitHub then shows every co-author on the commit.

---

## 6. Tags

**Every question commit gets an annotated tag**, created right after the commit.
Every section merge also gets a tag.

| Event | Tag | Example |
|-------|-----|---------|
| Question commit | `<section>/<q-id>/<type>` | `ga0/q-fastapi/solved` |
| | | `ga0/q-dbt-operations-dashboard/set-aside` |
| | | `roe/q07/cant-approach` |
| Section merged into `main` | `<section>/complete` | `ga0/complete`, `project-p1/complete` |
| Revisit merged into `main` | `<section>/revisit-<n>` | `ga0/revisit-1` |

- `<section>` uses the branch name: `ga0` … `ga8`, `project-p1`, `project-p2`, `roe`.
- Always annotated (`git tag -a`). The message repeats the commit's one-line summary.
- Tags are never moved or deleted. A set-aside question that's solved later gets a **new** `…/solved` tag, and the old `…/set-aside` tag stays as history.
- Push tags along with the branch (`git push --follow-tags`).

---

## 7. Workflow per question

1. **Branch**: `git switch <section-branch>`, creating it from `main` if new.
2. **Scaffold**: `scripts/new-question.sh <section> <q-id> [--deploy] [--marks N]`
3. **Capture**: paste the question into `README.md` and set Status to `in-progress`.
4. **Plan**: list options in `approaches.md` and choose one.
5. **Iterate**: log every prompt and its result in `prompts.md`.
6. **Deploy** *(if needed)*: fill `deploy.md` as you go, including dashboard-only settings.
7. **Verify**: exam "Check" button, curl, or a hand-worked sample. Record it in `approaches.md`.
8. **Consolidate**: write `final.md` so the answer can be reproduced in one pass.
9. **Close**: set the final Status, fill the answer or status notes, and update the section table.
10. **Commit**: one commit using the matching type, authored by the GitHub user, with a `Co-Authored-By` trailer for every LLM/agent used (§5).
11. **Tag**: annotated tag `<section>/<q-id>/<type>` on that commit (§6).
12. **Section done?** Merge into `main` with `--no-ff` (§4) and tag `<section>/complete` (§6).

Commands for every step: see [CMDS.md](CMDS.md).
