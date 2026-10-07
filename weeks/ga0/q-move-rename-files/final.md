# Final — q-move-rename-files

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga0/q-move-rename-files](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga0/q-move-rename-files)

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

Needs a bash shell (Mac/Linux terminal, or Git Bash/WSL on Windows).

1. Open your TDS folder for this GA (create `TDS/GA0` if you don't have one) and open a terminal in it.
2. Download `q-move-rename-files.zip` into it, then run these lines one by one:
   ```bash
   unzip q-move-rename-files.zip -d extracted
   mkdir flat && mv extracted/q-move-rename-files/*/* flat/ && cd flat
   for f in *; do n=$(echo "$f" | tr '0-9' '1-90'); [ "$f" != "$n" ] && mv -- "$f" "$n"; done
   grep . * | LC_ALL=C sort | sha256sum
   ```
3. The last line prints a 64-character hash followed by ` -`. Enter only the hash, then Check and Save.

If `sha256sum` is missing on a Mac, use `shasum -a 256` instead.

## Final prompt

```text
Bash: I have a folder with sub-folders of files. Move all files from the sub-folders into a new empty folder with mv,
then rename each file replacing every digit with the next one (9 -> 0) in a single pass (use tr '0-9' '1-90', not
chained sed). Then run: grep . * | LC_ALL=C sort | sha256sum
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
unzip q-move-rename-files.zip -d data/extracted
src/move_rename.sh data/extracted/q-move-rename-files /tmp/mvwork
```

Manual equivalent:

```bash
mkdir flat && mv q-move-rename-files/*/* flat/ && cd flat
for f in *; do n=$(echo "$f" | tr '0-9' '1-90'); [ "$f" != "$n" ] && mv -- "$f" "$n"; done
grep . * | LC_ALL=C sort | sha256sum
```

## Expected output

```
37cb52897b47b8e199fa9fa19cb95590955234fd63c9851bb57f5726669195c6  -
```

## Answer submitted (✅ passed, attempt 1)

```
37cb52897b47b8e199fa9fa19cb95590955234fd63c9851bb57f5726669195c6
```
