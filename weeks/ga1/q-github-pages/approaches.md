# Approaches — q-github-pages

## Problem in one line

A public github.io page whose HTML contains the exam email.

## Grader (from quiz JS)

- Client-side: hostname must include `github.io`; fetches `/proxy/<url>` (exam server proxy);
  passes if the HTML matches the email.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "GitHub Pages are served via CloudFlare" | Background | Wrapping in `email_off` is harmless either way; keeps the raw email in HTML |
| Email in public HTML | Privacy | Email becomes public on the page (already public in GA0 `email.json`) |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Single `index.html` in a public repo, Pages "Deploy from a branch" | GitHub web UI | No build, no CLI, ~3 min | Plain page | **chosen for the teammate how-to** |
| B | Static-site generator (MkDocs/Jekyll) deployed by GitHub Actions | Actions | Nicer site | Workflow + build to get right; more ways to fail | works, not needed |

## Chosen: A

**Why:** the grader only checks for the email in the HTML on a `github.io` host. Fewest moving parts = one try.

## Gotchas hit

- Use the **exam** email (IITM login shown on the question), not a personal one.
- Pages needs a **public** repo on a free account.
- Renaming the repo later breaks the Pages URL (no redirect).

## Verification

- `curl -s "https://exam.sanand.workers.dev/proxy/<url>" | grep -c <exam email>` → 1 (the grader's own fetch path).
- Exam Check: ✅ passed on attempt 1.
