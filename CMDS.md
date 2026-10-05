# CMDS — command reference

> Living file. Append new commands under the right section as they are used.
> Format: one-line comment saying what it does, then the command.

---

## 1. Environment setup

```bash
# Check tool versions
uv --version; gh --version; git --version; node --version; docker --version; ollama --version

# Install uv (Python package/runtime manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# GitHub CLI login
gh auth login

# Vercel CLI (via npx, no global install)
npx vercel login
```

---

## 2. Git workflow

```bash
# Start a section branch from main (first time)
git switch main && git pull && git switch -c ga0

# Resume an existing section branch
git switch ga0

# Revisit a section that is already merged
git switch main && git switch -c ga0-revisit
```

### Author check (once per machine)

```bash
# Author must be the GitHub user
git config user.name    # → christiano-developer
git config user.email   # → email linked to the GitHub account
```

### Commit + tag a question (one commit, at completion)

Each `-m` adds a paragraph. The last one holds the trailers, one `Co-Authored-By` per LLM/agent used.

```bash
# solved
git add weeks/ga0/q-fastapi weeks/ga0/README.md CMDS.md
git commit -m "solved(ga0/q-fastapi): <summary>" \
  -m "Approach: <one line>; see final.md" \
  -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Co-Authored-By: ChatGPT <model> <noreply@openai.com>"
git tag -a ga0/q-fastapi/solved -m "solved(ga0/q-fastapi): <summary>"

# set aside
git add weeks/ga0/<q-id> weeks/ga0/README.md
git commit -m "set-aside(ga0/<q-id>): <where it stopped>" \
  -m "Co-Authored-By: <LLM> <model> <noreply@...>"
git tag -a ga0/<q-id>/set-aside -m "set-aside(ga0/<q-id>): <where it stopped>"

# can't approach
git add weeks/ga0/<q-id> weeks/ga0/README.md
git commit -m "cant-approach(ga0/<q-id>): <blocker>" \
  -m "Co-Authored-By: <LLM> <model> <noreply@...>"
git tag -a ga0/<q-id>/cant-approach -m "cant-approach(ga0/<q-id>): <blocker>"

# No AI used
git commit -m "solved(ga0/<q-id>): <summary>" -m "AI: none"

# Verify author + co-authors of the last commit
git log -1 --format='Author: %an <%ae>%n%(trailers:key=Co-Authored-By)'

# Forgot a trailer? Fix BEFORE tagging/pushing
git commit --amend

# Push branch + its annotated tags
git push -u origin ga0 --follow-tags
```

### Merge + tag a completed section

```bash
# Check every question in the section has a final status (should print nothing)
grep -E '\| (todo|in-progress) \|' weeks/ga0/README.md

# Merge, keeping per-question commits
git switch main && git merge --no-ff ga0 -m "merge(ga0): section complete"

# Tag the merge commit
git tag -a ga0/complete -m "merge(ga0): section complete"
git push origin main --follow-tags

# Revisit merge (n = 1, 2, ...)
git merge --no-ff ga0-revisit -m "merge(ga0-revisit): <summary>"
git tag -a ga0/revisit-1 -m "merge(ga0-revisit): <summary>"
```

### Sync main into a section branch (after a `setup:` commit)

```bash
# Merge (never rebase) so pushed commits and their tags stay intact; n = 1, 2, ...
git switch ga0
git merge --no-ff main -m "sync(ga0): merge main (setup/<name>)" \
  -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git tag -a ga0/sync-1 -m "sync(ga0): merge main (setup/<name>)"
git push origin ga0 --follow-tags
```

### Tags

```bash
# All tags for a section
git tag -l 'ga0/*'

# All set-aside / can't-approach questions across the repo
git tag -l '*/set-aside'; git tag -l '*/cant-approach'

# Show a tag's message and commit
git show ga0/q-fastapi/solved --stat

# Find question commits that have no tag yet (prints untagged commits)
for c in $(git rev-list main..HEAD); do git describe --exact-match --tags $c >/dev/null 2>&1 || git log -1 --oneline $c; done
```

### Inspect

```bash
# Per-question commits on the current branch
git log --oneline main..HEAD

# Commits by type
git log --oneline --grep '^set-aside'
```

---

## 3. Scaffolding

```bash
# Plain question
scripts/new-question.sh weeks/ga0 q-sort-filter-json --marks 0.5

# Question needing deploy / server / external config
scripts/new-question.sh weeks/ga0 q-vercel-latency --deploy --marks 3

# ROE / project
scripts/new-question.sh roe q01
scripts/new-question.sh projects/p1 r01-api --deploy

# Create local secrets file for a deploy question
cp weeks/ga0/<q-id>/.env.example weeks/ga0/<q-id>/.env
```

---

## 4. Run, deploy and servers

### Python / FastAPI (uv)

```bash
# Run a FastAPI app locally with auto-reload
uv run --with fastapi --with uvicorn uvicorn main:app --reload --port 8000

# Test a local endpoint
curl -s "http://localhost:8000/api?x=1" | jq
```

### Vercel

```bash
# Deploy to production from the current folder
npx vercel --prod
```

### Ollama

```bash
# Pull and run a local model; API listens on :11434
ollama pull <model> && ollama serve
```

---

### Headless Chrome (render / screenshot a local HTML page)

```bash
# Screenshot a local HTML file (waits up to 5s for JS like Chart.js to draw)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --window-size=1000,450 --virtual-time-budget=5000 \
  --screenshot="$PWD/out.png" "file://$PWD/page.html"
```

---

## 5. One-liners

```bash
# Pretty-print / query JSON
jq '.' file.json

# Fetch a URL and show only headers
curl -sI <url>
```

### Exam submissions

```bash
# Copy a submission file to the clipboard (never copy from terminal output — wrapping mangles it)
pbcopy < weeks/ga0/<q-id>/src/<file>

# Download the GA quiz JS to read grader logic (hacking is allowed in TDS)
curl -sL https://exam.sanand.workers.dev/exam-tds-2026-09-ga0.js -o /tmp/ga0.js
grep -o 'outside tolerance' /tmp/ga0.js   # then read the surrounding check function
```
