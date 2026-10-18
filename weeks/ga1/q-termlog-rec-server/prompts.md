# Prompt log — q-termlog-rec-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5) via Claude in Chrome (preview of the challenge) + the user's terminal.
- **Goal:** know the decode pipeline before recording, then record it.

```text
then guide me to 13, and 15
```

- **Result:** worked. Claude fetched the challenge in the exam tab beforehand: a comment block plus one hex string.
  Hex → ASCII gave `QK4SGQH5-YG` (letters + digits, looks rotated/reversed), reversed `GY-5HQGS4KQ`, ROT13 → a clean
  `TL-5UDTF4XD` style code. So: `xxd -r -p | rev | tr 'A-Za-z' 'N-ZA-Mn-za-m'`.
  In the recording: `curl -s "<URL>"`, then the pipeline (a first attempt read a `cipher.txt` that hadn't been saved;
  harmless), `exit`. termlog wrote `demo.cast` + `demo.cast.jwt`; packed with tar, uploaded as a GitHub release
  asset. Exam Check: "Verified recording."
- **Next:** none.
