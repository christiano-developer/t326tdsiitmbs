# Prompt log — q-csv-sales-analysis-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app + Claude in Chrome (Brave).
- **Goal:** solve the "download, process, submit" questions directly in the exam tab.

```text
okay do those questions (Q2, Q5, Q8, Q11, Q16 — the ones you can do from the browser)
```

- **Result:** worked. Claude fetched the page's `sales_data.zip` blob, unzipped it in-page, checked the format
  (`2025-May-8`, 112 rows, all 5 columns, 7 cities), and summed quantity × price for Bangalore in May:
  4 rows, 12010.48 → **12010**. Check: "Correct".
- **Next:** session moved to Chrome; redo there.

---

## P2

- **Tool / model:** Claude (Claude Opus 5.5) via Claude in Chrome (Chrome).
- **Goal:** redo in Chrome.

```text
https://exam.sanand.workers.dev/tds-2026-09-ga1   (redo the solved questions here)
```

- **Result:** same 12010, Check: "Correct". CSV saved as [data/sales_data.csv](data/sales_data.csv)
  (sha256 matches the in-page file); logic saved as [src/revenue.mjs](src/revenue.mjs).
- **Next:** none.
