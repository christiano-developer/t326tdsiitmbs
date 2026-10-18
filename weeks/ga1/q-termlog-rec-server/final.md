# Final — q-termlog-rec-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-termlog-rec-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-termlog-rec-server)

## How to solve (for a teammate)

> Per student and per 3-hour window: your cipher differs and changes. The recording is signed with your Google
> login, so only you can make it.

**Approach:** the challenge is your code after three reversible transforms (ROT13, hex, reversal). Look at the
ciphertext: it's hex, so hex was applied last and must be undone first; reversal and ROT13 commute. Decide the
pipeline before recording, then record just the fetch and the decode.

1. Install termlog from https://github.com/mynkpdr/termlog/releases (macOS arm64: `termlog-aarch64-apple-darwin`):
   `chmod +x termlog-aarch64-apple-darwin && xattr -d com.apple.quarantine termlog-aarch64-apple-darwin; sudo mv termlog-aarch64-apple-darwin /usr/local/bin/termlog`
2. `termlog login` (school Google account), `termlog whoami`.
3. `termlog rec demo.cast`, then inside the recording:
   ```bash
   curl -s "<the Q13 curl URL from the exam page>" | grep -v '^#' | xxd -r -p | rev | tr 'A-Za-z' 'N-ZA-Mn-za-m'; echo
   exit
   ```
4. `tar -czf submission.tar.gz demo.cast demo.cast.jwt`
5. Host it publicly, e.g. `gh release create <tag> submission.tar.gz -R <you>/<repo>`; the asset URL is
   `https://github.com/<you>/<repo>/releases/download/<tag>/submission.tar.gz`. Check with `curl -sIL <url>` (ends in 200).
6. Paste the URL, Check ("Verified recording."), Save.

<details><summary>decode.sh (click to expand)</summary>

```bash
#!/usr/bin/env bash
# Decode the q-termlog-rec-server cipher: undo hex, then reversal, then ROT13 (reversal and ROT13 commute).
# Usage (inside the termlog recording):  curl -s "<Q13 URL from the exam page>" | bash decode.sh
#   or:                                  echo <hex string> | bash decode.sh
grep -v '^#' | tr -d ' \n' | xxd -r -p | rev | tr 'A-Za-z' 'N-ZA-Mn-za-m'; echo
```

</details>

## Final prompt

```text
A string is my code after ROT13, hex encoding and string reversal in some order. Here it is: <cipher>.
Work out the undo order from what the ciphertext looks like and give me one shell pipeline (xxd, rev, tr)
that prints the code. I'll run it inside a termlog recording.
```

- **Tool / model used:** Claude (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
printf '514b3453475148352d5947\n' | bash weeks/ga1/q-termlog-rec-server/src/decode.sh
```

## Expected output

```
TL-5UDTF4XD
```

## Answer submitted (✅ Check passed)

The public release-asset URL of `submission.tar.gz` (see README).
