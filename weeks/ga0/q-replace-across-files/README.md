# q-replace-across-files

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga0 |
| Marks     | ? |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | no |
| Started   | 2026-10-06 |
| Closed    | 2026-10-06 (passed on attempt 1) |

## Question

**Replace across files**: background: *Terminal: Bash*.

> Download `q-replace-across-files.zip` and unzip it into a new folder, then replace all "IITM" (in upper, lower, or
> mixed case) with "IIT Madras" in all files. Leave everything as-is - don't change the line endings.
>
> What does running `cat * | sha256sum` in that folder show in bash?

(The instruction line was missing from the pasted text; recovered from the quiz page source.)

Per-user variant: 10 random-text files seeded from the student email.

## Inputs / given data

- [data/extracted/q-replace-across-files/](data/extracted/q-replace-across-files/): `file0.txt`…`file9.txt` (ASCII, LF),
  300 case-insensitive `iitm` matches. Kept untouched; the script works on a copy.

## Final answer

```
16bd7ac66647ebf24e115c4319f062770812af8a002b01f1e4a51183c1e726ef
```

## Status notes

- Shell (`perl -pi`) and Python agree; byte check confirms only the replacements changed. Exam Check ✅ **passed**.

## Files

- [prompts.md](prompts.md) · [approaches.md](approaches.md) · [final.md](final.md)
- [src/replace.sh](src/replace.sh) — copy → `perl -pi -e 's/iitm/IIT Madras/gi'` → `cat * | sha256sum`
