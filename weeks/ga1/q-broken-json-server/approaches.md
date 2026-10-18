# Approaches — q-broken-json-server

## Problem in one line

Repair 6 kinds of injected JSON syntax errors without changing any data.

## Grader (from quiz JS)

- Client-side: rebuilds the valid JSON from the seed; passes if
  `JSON.stringify(JSON.parse(answer)) === JSON.stringify(valid)` (whitespace/formatting free).
- Corruptions, by `index % 6`: removed trailing comma · `,}`/`,]` · unquoted key · `'key':` ·
  `{` line deleted · `}` → `}}`.
- Error messages: record count mismatch, first-3-record mismatch, "content doesn't match".

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "All N records must remain" | **Distractor** | N counts every `{` (incl. nested `metadata`), not records. There are 300 records |
| "fix one error at a time" strategy | Background | Grader only compares final parsed data |
| Missing-brace lines | Gotcha | A deleted `{` line must be restored, not just tolerated |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Regex repair passes, re-parse until `JSON.parse` succeeds | Node / browser JS | Fast, general, shows each error | Needs a new pass for corruption kinds not seen yet | chosen |
| B | Fix by hand in VS Code using the parser's error line | VS Code | No code | Slow on 180 KB, easy to miss one | rejected |
| C | Rebuild the valid JSON from the seed (`src/valid.mjs`) | Node + seedrandom | Exact by construction | Depends on reading the quiz JS; breaks if it changes | used to verify |

## Chosen: A

**Why:** quickest route that also explains every fix; C confirms the result byte-for-byte.

## Gotchas hit

- This seed had 8 errors of 4 kinds: single-quoted key ×2, unquoted key ×3, trailing comma ×1, missing comma ×2.
  No deleted `{` line or `}}` this time. Other emails can get those, and `fix.mjs` doesn't handle them:
  if `JSON.parse` still fails, open the reported line and restore the brace by hand.
- Order matters: quote keys before adding commas, or the missing-comma pass can't see that the next line starts with `"`.
- The ZIP is built in the page as a `blob:` URL, so it can be fetched and unzipped in the tab (`DecompressionStream('deflate-raw')`).

## Verification

- `node src/fix.mjs data/broken.json` → `fixed 8 …`, `records: 300`; output `JSON.stringify` equals `data/fixed.json` (151206 chars).
- Exam **Check** → "Correct" (Brave and Chrome, 2026-10-18).
