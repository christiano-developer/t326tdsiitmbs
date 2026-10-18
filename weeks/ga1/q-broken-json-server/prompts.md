# Prompt log — q-broken-json-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P0 (earlier session, 2026-10-09)

- **Tool / model:** Claude Code (Claude Opus 5.5).
- **Goal:** rebuild the valid JSON from the seed, as the quiz JS does.
- **Result:** produced [src/valid.mjs](src/valid.mjs) and [data/fixed.json](data/fixed.json) (300 records); question
  not closed or logged at the time.
- **Next:** used below as the reference to verify the repair.

---

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app + Claude in Chrome (Brave).
- **Goal:** solve the "download, process, submit" questions directly in the exam tab.

```text
okay do those questions (Q2, Q5, Q8, Q11, Q16 — the ones you can do from the browser)
```

- **Result:** worked. Claude fetched the page's `broken_json.zip` blob, unzipped it in-page, and repaired it with
  regex passes guided by `JSON.parse` error positions:
  1. `'metadata':` / `'tags':` single-quoted keys,
  2. `priority:` / `metadata:` / `id:` unquoted keys,
  3. one `,]` trailing comma,
  4. two missing commas between a value and the next line.
  Parsed to 300 records, same keys on every record. Check: "Correct".
- **Next:** session moved to Chrome; redo there.

---

## P2

- **Tool / model:** Claude (Claude Opus 5.5) via Claude in Chrome (Chrome).
- **Goal:** redo in Chrome.

```text
https://exam.sanand.workers.dev/tds-2026-09-ga1   (redo the solved questions here)
```

- **Result:** same passes, Check: "Correct". Passes saved as [src/fix.mjs](src/fix.mjs); on this repo's
  `data/broken.json` it reports 8 fixes and its output equals `data/fixed.json` exactly.
- **Next:** none.
