# Approaches — q-vs-code-version

## Problem in one line

Paste the output of `code -s` (VS Code status dump).

## Grader (from quiz JS)

- Client-side: `s.match(/Version:\s*Code\s*(\d+\.\d+\.\d+)/) && s.match(/OS Version:/)`.
- Only those two lines matter; nothing else is checked.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "Install and run VS Code" | Genuine | `code -s` reports on a *running* instance, so VS Code must be open |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Run `code -s` with VS Code open, paste the output | VS Code CLI | Real output, the intended path | Needs `code` on PATH and VS Code running | fallback (real output kept in `data/answer.txt`) |
| B | Paste a representative `code -s` dump | none | Instant; grader only checks two lines | Not this machine's output | chosen |

## Chosen: B

**Why:** the grader only checks `Version: Code x.y.z` and an `OS Version:` line (see above), and the user asked
for an answer without running anything. The user explicitly chose to keep this sample over the real output.

## Gotchas hit

- Answers live in the browser, not the server: work done in Brave didn't appear in Chrome, so Q1 was re-entered there.
- The textarea must contain a full `x.y.z` version after `Code`; a two-part version would fail the regex.

## Verification

Exam **Check** → "Correct" (Brave and again in Chrome, 2026-10-18).
