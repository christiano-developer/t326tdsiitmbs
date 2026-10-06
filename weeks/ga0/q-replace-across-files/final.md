# Final — q-replace-across-files

> Goal: the answer can be reproduced from this file alone.

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
