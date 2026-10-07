# Final — q-replace-across-files

> Goal: the answer can be reproduced from this file alone.

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

Needs a bash shell (Mac/Linux terminal, or Git Bash/WSL on Windows).

1. Open your TDS folder for this GA (create `TDS/GA0` if you don't have one) and open a terminal in it.
2. Download `q-replace-across-files.zip` into it, then run:
   ```bash
   mkdir new && cd new && unzip ../q-replace-across-files.zip
   perl -pi -e 's/iitm/IIT Madras/gi' *
   cat * | sha256sum
   ```
   If the zip contains a sub-folder, `cd` into it before the `perl` line. Use `perl`, not Mac's `sed -i`, which changes line endings.
3. Enter only the 64-character hash, then Check and Save.

## Final prompt

```text
Bash on macOS: in a folder of text files, replace every case-insensitive "iitm" (substring) with "IIT Madras" in place
without changing line endings or anything else (use perl -pi, not BSD sed), then run cat * | sha256sum.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

```bash
mkdir new && cd new && unzip ../q-replace-across-files.zip
perl -pi -e 's/iitm/IIT Madras/gi' *
cat * | sha256sum
# or: src/replace.sh data/extracted/q-replace-across-files /tmp/rpwork
```

## Expected output

```
16bd7ac66647ebf24e115c4319f062770812af8a002b01f1e4a51183c1e726ef  -
```

## Answer submitted (✅ passed, attempt 1)

```
16bd7ac66647ebf24e115c4319f062770812af8a002b01f1e4a51183c1e726ef
```
