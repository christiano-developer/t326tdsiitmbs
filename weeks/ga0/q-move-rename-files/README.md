# q-move-rename-files

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**Move and rename files**: background: *Terminal: Bash* (essential commands, text processing, scripting, productivity).

> Download `q-move-rename-files.zip` and extract it. Use `mv` to move all files under folders into an empty folder.
> Then rename all files replacing each digit with the next. 1 becomes 2, 9 becomes 0, `a1b9c.txt` becomes `a2b0c.txt`.
>
> What does running `grep . * | LC_ALL=C sort | sha256sum` in bash on that folder show?

Per-user variant: folder and file names seeded from the student email.

## Inputs / given data

- [data/extracted/q-move-rename-files/](data/extracted/q-move-rename-files/): the unzipped contents (3 folders × 10
  `.txt` files, each containing `x`). Kept untouched; the script works on a copy.

## Final answer

```
37cb52897b47b8e199fa9fa19cb95590955234fd63c9851bb57f5726669195c6
```

## Status notes

- Shell run and the grader formula (Python) agree. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md)
- [src/move_rename.sh](src/move_rename.sh) — mv + one-pass digit rename + the hash, on a scratch copy
