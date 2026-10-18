# Approaches — q-npx-prettier

## Problem in one line

SHA-256 of prettier 3.4.2's formatted output of the downloaded file.

## Grader (from quiz JS)

- Client-side: formats the same text with prettier 3.4.2 (markdown parser) in the browser, SHA-256s it.
- Check: `answer.trim().split(/\s+/)[0] === hash` (trailing `  -` is fine).

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "make sure it is called README.md" | Genuine | Browsers rename duplicates to `README (1).md`; prettier picks the parser from the extension |
| `sha256sum` | Note | On macOS `shasum -a 256` is equivalent if `sha256sum` is missing |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Rebuild the seeded file from the quiz JS, run the real `npx prettier` + `shasum` | Node, seedrandom, npx | Exactly the asked command; reproducible | Needs the generator | chosen |
| B | Download via the button, run the command | Browser, npx | Simplest for a teammate | Browser rename risk (`README (1).md`) | teammate path in final.md |

## Chosen: A

**Why:** same bytes as the download, and the CLI hash was cross-checked against prettier's Node API (what the browser grader uses).

## Gotchas hit

- macOS has no `sha256sum`, so use `shasum -a 256`.

## Verification

CLI hash == API hash (`b84b9f…f304`). Check passed on attempt 1.
