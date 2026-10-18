# Final — q-npx-prettier

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-npx-prettier](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-npx-prettier)

## How to solve (for a teammate)

> The file is seeded from your exam email, so every student's hash is different.
> Needs Node.js (for `npx`).

1. On the exam page click the **README.md** button. Make a new empty folder (e.g. `ga1-prettier`) and move the download into it.
2. Make sure the file is named exactly `README.md`. Browsers rename repeat downloads to `README (1).md`,
   and prettier picks its parser from the file extension and name.
3. Open a terminal in that folder and run:
   - Linux / Git Bash: `npx -y prettier@3.4.2 README.md | sha256sum`
   - macOS (no `sha256sum`): `npx -y prettier@3.4.2 README.md | shasum -a 256`
   - Windows PowerShell: use Git Bash instead. PowerShell's pipe re-encodes the text, which changes the hash.
4. It prints one line like `b84b9f…f304  -`. Paste that line (or just the 64-char hash, since the grader ignores the trailing `-`).
5. Click Check. If it fails, re-download the file. Editing or re-saving it in an editor changes the hash.

## Final prompt

```text
I downloaded README.md from a quiz. Give me the exact command to format it with prettier 3.4.2 via npx and
print the SHA-256 of prettier's stdout, on macOS (no sha256sum) and on Linux. The file must keep the name
README.md and must not be edited.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

1. Prerequisites: Node.js and the `EXAM_EMAIL` env var.
2. Rebuild the seeded file (same generator as the quiz JS) and hash it:

```bash
cd weeks/ga1/q-npx-prettier/src
npm i seedrandom@3.0.5
EXAM_EMAIL=you@ds.study.iitm.ac.in node gen.mjs > ../data/README.md
cd ../data && npx -y prettier@3.4.2 README.md | shasum -a 256
```

3. Generator: [`src/gen.mjs`](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-npx-prettier/src/gen.mjs).

## Expected output

```
<64 hex chars>  -
```

## Answer submitted (✅ passed, attempt 1)

```
b84b9fbf1be2872bf8188bc860205f58ce7d3bba4a88f141e23bd6168184f304
```
