# Prompt log — q-vs-code-version

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app driving the exam page through Claude in Chrome (Brave).
- **Goal:** fill Q1 without running `code -s` locally.

```text
now answer question 1 without the need to actually run the code. i handle the submit for now
```

- **Result:** worked. Claude wrote a representative macOS `code -s` dump (VS Code 1.105.1, Darwin arm64) into the
  textarea and pressed Check: "Correct". Not captured from this Mac.
- **Next:** session moved to Chrome (answers are stored per browser), so redo there.

---

## P2

- **Tool / model:** Claude (Claude Opus 5.5) via Claude in Chrome (Chrome).
- **Goal:** re-enter Q1 in Chrome.

```text
https://exam.sanand.workers.dev/tds-2026-09-ga1   (redo the solved questions here)
```

- **Result:** worked. Slightly trimmed version of the same sample (fewer GPU lines); Check: "Correct".
  Saved as [data/submitted.txt](data/submitted.txt). User chose to keep this sample rather than the real
  output in [data/answer.txt](data/answer.txt).
- **Next:** none.
