# Prompt log — q-unicode-data

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** scaffold; user adds the unzipped files

```text
Process files with different encodings
<Unicode background + task: see README.md>
scaffold, then ill add the unzipped content
```

- **Result:** scaffolded `data/extracted/`. Read the grader (targets = data1's first 3 symbols; value = row index).
  Flagged the lookalike-symbol and encoding traps.
- **Next:** user adds files.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** compute the sum

```text
added
```

- **Result:** `file` confirmed the encodings (data3 UTF-16 LE with BOM). `src/sum_symbols.py` → 40909; the grader
  formula from the seed → 40909.
- **Next:** user submits.

---

## P3

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
correct
```

- **Result:** ✅ passed on the first submission. Status → `solved`, committed and tagged.
- **Next:** none.
