# Prompt log — q-git-forensics-token-server

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5), Claude desktop app + Claude in Chrome (Chrome).
- **Goal:** solve from the exam tab.

```text
sure do Q 9,7,10
```

- **Result:** worked. The question's iframe offers `history.fastimport` as a `data:` link (4,086 bytes). Claude parsed
  the fast-import stream in the page (blobs, marks, `from`, `M` ops), replayed the 14 commits on `main`, and tracked
  `stg_…` strings in the tree: exactly one token, present from `:13` "Add staging deploy token to app config" until
  `:21` "Rotate and revoke leaked staging token" (value replaced by `__rotated__`). No branches, resets or decoys.
  Typed the JSON answer; Check: "Correct! You found the introducing commit and the token."
- **Next:** none.

---

## P2

- **Tool / model:** same.
- **Goal:** log it in the repo and verify with real git.

```text
log and work these into the repo
```

- **Result:** history saved byte-exact as [data/history.fastimport](data/history.fastimport)
  (sha256 `a33c4a7a…ae36`). `git fast-import` + `git log -S stg_ --reverse` gives the same two commits;
  [src/find-token.sh](src/find-token.sh) prints the answer JSON.
- **Next:** none.
