# Final — q-move-rename-files

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Bash: I have a folder with sub-folders of files. Move all files from the sub-folders into a new empty folder with mv,
then rename each file replacing every digit with the next one (9 -> 0) in a single pass (use tr '0-9' '1-90', not
chained sed). Then run: grep . * | LC_ALL=C sort | sha256sum
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

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
