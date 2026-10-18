# Prompt log — q-cosine-similarity-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app + Claude in Chrome (Brave).
- **Goal:** solve the "download, process, submit" questions directly in the exam tab.

```text
okay do those questions (Q2, Q5, Q8, Q11, Q16 — the ones you can do from the browser)
```

- **Result:** worked. The download button builds the JSON in the page, so Claude intercepted the blob
  (`URL.createObjectURL`) instead of saving a file, computed cosine similarity for 10 queries × 250 docs,
  sorted descending with doc_id tie-break, and submitted the top 5 per query.
  Check: "Cosine similarity search verified: 10/10 queries matched exactly. ✅"
- **Next:** session moved to Chrome; redo there.

---

## P2

- **Tool / model:** Claude (Claude Opus 5.5) via Claude in Chrome (Chrome).
- **Goal:** redo in Chrome.

```text
https://exam.sanand.workers.dev/tds-2026-09-ga1   (redo the solved questions here)
```

- **Result:** same answer, 10/10. Logic saved as [src/cosine.mjs](src/cosine.mjs); its `topK()` was re-run in the
  exam tab on the live task file and reproduces the submitted answer exactly. Answer in [data/answer.json](data/answer.json).
- **Next:** none.
