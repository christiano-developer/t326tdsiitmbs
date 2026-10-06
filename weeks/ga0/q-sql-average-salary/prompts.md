# Prompt log — q-sql-average-salary

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** write the SQL

```text
SQL: Average salary by department
<SQLite background + GlobalTech task + table preview screenshot: see README.md>
```

- **Result:** read the grader (col0 = dept, col1 = avg, ±5, order unchecked). Regenerated the seeded table
  (matches the preview) and ran the query in SQLite → exact match, PASS.
- **Next:** user submits.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
correct
```

- **Result:** ✅ passed on the first submission. Status → `solved`, committed and tagged.
- **Next:** none.
