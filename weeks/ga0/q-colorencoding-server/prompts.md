# Prompt log — q-colorencoding-server

## P1

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** explain, set up and solve, with a short explanation

```text
Fix the Color Encoding Mismatch
<full question text, broken chart HTML, task, hint, colour-scheme primer, verification criteria:
see README.md / data/original.html>
i need a corrected html
Must include: corrected hex colors, the scheme type word, and your explanation of what the original
chart implied incorrectly.
explain layout the base and solve, keep the explanation short
```

- **Result:** worked.
  - Read the grader: it extracts every hex in the submission, checks pairwise CIEDE2000 ≥ 30 on the first 8,
    and needs the word "categorical" plus one of 5 phrases.
  - Found 3 traps: the reversed code comment, the primer's Tableau palette failing its own check, and the
    page's CSS hexes being extracted.
  - Ported the grader to `src/check.py`, brute-forced palettes, and picked Okabe-Ito (min 37.0). Wrote
    `src/corrected.html` with no other hexes → PASS; rendered OK.
- **Next:** user submits; record Check result.

---

## P2

- **Tool / model:** Claude Code (Claude Opus 5.5)
- **Goal:** record the result

```text
its correct,
```

- **Result:** ✅ passed on the first submission. Status → `solved`.
- **Next:** commit + tag.
