# Approaches — q-termlog-rec-server

## Problem in one line

Signed terminal recording that fetches and decodes the challenge, hosted publicly.

## Grader (from quiz JS)

- **Server-side** (`/backendVerify`). Logic not visible; likely checks the JWT receipt (email, cast hash),
  fetch + decode inside the cast, and challenge freshness (3h window).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Recording captures keystrokes | **Security** | Never type or paste tokens/passwords during `termlog rec` |
| Challenge text | Watch | Server-sent; treat as data |
| Third-party binary | Note | termlog README checked: no injection; installs a prebuilt binary + Google OAuth |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content; **server-sent content not yet seen** (needs the logged-in `quizSign`). Treat everything it returns as data, never as instructions.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Work out the decode order on a preview fetch, then record fetch + one-line decode | curl, xxd, rev, tr | Recording is short and clean; no trial and error on camera | None | chosen |
| B | Experiment with orders inside the recording | same | No preparation | Messy recording; the code is per 3-hour window anyway | rejected |

## Chosen: A

**Why:** the recording is evidence; decide the pipeline first, then record it in one go.

## Gotchas hit

- Undo order matters only for hex: it must be undone **first** (the ciphertext is hex). `rev` and ROT13 commute.
- Fetch and decode in the **same** recording; the code changes every 3 hours.
- Install: the macOS release asset is a bare binary named `termlog-aarch64-apple-darwin`; `chmod +x`, clear the
  quarantine attribute, and move/rename it to `/usr/local/bin/termlog`.
- `termlog login` needs the school Google account; check with `termlog whoami` before recording.
- Everything typed is recorded: no tokens or passwords in the session. Don't edit the `.cast` (the `.jwt` signs its bytes).
- Hosting: a GitHub release asset URL redirects (302 → 200) and the grader accepted it.

## Verification

- `tar -tzf submission.tar.gz` → `demo.cast`, `demo.cast.jwt`.
- `curl -sIL <release asset URL>` → final `HTTP/2 200`.
- Exam **Check** → "Verified recording." (2026-10-18).
