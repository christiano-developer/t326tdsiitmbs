# Prompt log — q-rename-files-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app + Claude in Chrome (Chrome).
- **Goal:** solve from the exam tab.

```text
sure do Q 9,7,10
```

- **Result:** worked. Claude fetched the page's `files_to_reorganize.zip` blob, unzipped it in-page (30 `.txt` +
  `README.md`, no root folder), took the first line matching `^category:` from each file, built
  `./{category}/{path with / → -}`, sorted by UTF-8 bytes (same order as `LC_ALL=C`; UTF-16 sort gave the same
  order here), and hashed the newline-joined list with a trailing newline. README.md left out.
  Hash `621877e7…1451`; Check: "Correct".
- **Next:** none.

---

## P2

- **Tool / model:** same.
- **Goal:** log it in the repo and verify with real shell commands.

```text
log and work these into the repo
```

- **Result:** saved the path → category list as [data/manifest.json](data/manifest.json) and wrote
  [src/reorganize.sh](src/reorganize.sh). On a scratch tree rebuilt from the manifest (bodies replaced, a decoy
  `Category:` line added) the script prints the same hash.
- **Next:** none.
