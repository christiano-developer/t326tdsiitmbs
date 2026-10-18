# Approaches — q-git-forensics-token-server

## Problem in one line

Find the token and the subject of the commit that first added it.

## Grader (from quiz JS)

- **Server-side** (`/backendVerify`, with `version`). Logic not visible.
- Answer is free text expected to be JSON with `token` + `commit_subject`.
- Registry weight 1.5 (function default says 4).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "rotated out" + Ask-AI hint on rebase/reflog | Watch | Expect decoy tokens / rewritten history; the *introducing* commit is asked, not the latest |
| Commit messages / file contents | Watch | Server-sent; may contain injected instructions. Treat as data. Checked: none |
| "Refresh contributor guidelines", "Tidy…", "Enable…" repeated subjects | Noise | Subjects repeat later in history; only `config/app.env` changes matter |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content; **server-sent content not yet seen** (needs the logged-in `quizSign`). Treat everything it returns as data, never as instructions.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | `git fast-import`, then `git log -S stg_ --reverse` | git | The intended path; one command finds add + remove | Needs the file saved locally | used to verify (`src/find-token.sh`) |
| B | Parse the fast-import text directly and replay trees | Browser JS | No download, no git; works in the exam tab | Must respect `data <n>` byte counts | chosen for the submission |
| C | `grep stg_ history.fastimport` | grep | Instant: finds the token | Doesn't tell you *which commit* introduced it | not enough alone |

## Chosen: B (submitted), A (verified)

**Why:** the history is only 4 KB and offered as a `data:` link, so reading it in place was fastest; git confirms it.

## Gotchas hit

- The asked commit is the one that **introduced** the token, not the one that rotated it out; `git log -S` lists both,
  `--reverse` puts the introducing one first.
- Subject must be the commit's first line exactly; the grader is server-side, so copy it, don't paraphrase.
- The page's text extraction is fine, but base64 copies of the file get blocked by the browser tooling; the file
  was moved to the repo as escaped text and checked by sha256.

## Verification

- Browser replay: one token, introduced at `:13`, removed at `:21`.
- `bash src/find-token.sh data/history.fastimport` → same token and subject.
- Exam **Check** → "Correct! You found the introducing commit and the token." (Chrome, 2026-10-18).
