# Getting started

## Requirements

| Tool | Used for | Check |
|------|----------|-------|
| git + [GitHub CLI](https://cli.github.com/) | branches, tags, repo | `git --version; gh --version` |
| [uv](https://docs.astral.sh/uv/) | Python scripts and tools | `uv --version` |
| Node.js | `npx` tools (prettier, vercel) | `node --version` |
| A Vercel account | deploy questions | `npx vercel login` |

## Install

```bash
git clone https://github.com/christiano-developer/t326tdsiitmbs.git
cd t326tdsiitmbs
git switch init          # the workflow only: README, CMDS, templates, scripts
```

## Start a section

Every section (GA, project, ROE) is its own branch, started from `init`:

```bash
git switch -c ga1 init
```

## Scaffold a question

```bash
scripts/new-question.sh weeks/ga1 q-github-pages --marks 1
scripts/new-question.sh weeks/ga1 q-mcp-server-live-server --deploy --marks 3
```

This creates:

```text
weeks/ga1/q-github-pages/
├── README.md        question, marks, status, final answer
├── prompts.md       every prompt tried, with its result
├── approaches.md    grader notes, distractors, options, verification
├── final.md         teammate how-to + final prompt + reproduction steps
├── src/  data/
└── deploy.md        (--deploy only) run, test, deploy, teardown
```

…and adds a row to `weeks/ga1/README.md`.

!!! note "Next"
    Follow the [per-question workflow](workflow.md).
