# Prompt log — q-move-rename-files

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** scaffold; user adds the unzipped files

```text
Move and rename files
<Bash background + task: see README.md>
scaffold then ill add the unzipped contents
```

- **Result:** scaffolded `data/extracted/`. Read the grader (hash of sorted unique `renamed:x` lines; first-token
  match). Flagged the chained-sed and locale traps.
- **Next:** user drops files.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** compute the hash

```text
done added to data
```

- **Result:** found 3×10 files + a Finder `.DS_Store`. `src/move_rename.sh` (scratch copy) → `37cb5289…95c6`;
  the Python grader formula matches; the chained-sed control differs.
- **Next:** user submits.

---

## P3

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
this one correct
```

- **Result:** ✅ passed on the first submission. Status → `solved`, committed and tagged.
- **Next:** none.
