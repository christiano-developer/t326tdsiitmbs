# Approaches — q-use-github

## Problem in one line

Serve `{"email": "<exam email>"}` from a public GitHub repo and submit its raw.githubusercontent.com URL.

## Grader (from quiz JS)

1. `new URL(answer).hostname` must include `raw.githubusercontent.com`.
2. `fetch(answer).json()`: `.email` must equal the exam email exactly. Otherwise it errors with
   `<json> does not match {"email": "…"}`.

Nothing else is checked: repo name, path, file count and newness are all ignored.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "Create a new public repository" | **Distractor** | Not checked. Any public repo works, including this one |
| "Commit a single JSON file" | Distractor | Only the fetched JSON is checked; other files in the repo don't matter |
| Raw URL with a branch name | Trap (durability) | A branch URL breaks if the branch is deleted after merging. A commit-SHA URL is permanent |
| Hidden markup in this question | None found | Scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Pros | Cons | Verdict |
|---|----------|------|------|---------|
| A | New public repo with just `email.json` | Literal reading | Extra repo; same email exposure | rejected |
| B | **`weeks/ga0/q-use-github/email.json` in this repo, raw URL pinned to the commit SHA** | Stays in scope; permanent URL | Email committed to this public repo's history (unavoidable: the grader reads the file) | **chosen** |

## Chosen: B

**Why:** the grader only verifies the fetched content, and keeping it in this repo follows the repo-scope rule.

## Gotchas

- The JSON must be strictly valid and the email exact (case and whitespace).
- raw.githubusercontent.com can cache for a few minutes. A commit-SHA URL avoids stale-branch caching.

## Verification

- `src/check_raw_url.sh <raw-url> <exam-email>` after the push → PASS on host + email.
- Exam "Check" button: see prompts.md.
