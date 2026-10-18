# Final — q-vs-code-version

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-vs-code-version](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-vs-code-version)

## How to solve (for a teammate)

> Not seeded: everyone's answer is just their own VS Code status dump. The grader only checks that the text
> contains `Version: Code <x.y.z>` and an `OS Version:` line.

1. Open VS Code (it must be running, because `code -s` reports on the running instance).
2. Make sure the `code` command works in a terminal. On macOS: in VS Code press `Cmd+Shift+P` →
   **Shell Command: Install 'code' command in PATH**. On Windows it's added by the installer.
3. In a terminal run:
   ```bash
   code -s
   ```
4. Copy **all** of the output (it starts with `Version:` and ends with the workspace stats) into the answer box,
   then Check and Save.
   - macOS shortcut that avoids terminal wrapping: `code -s | pbcopy`, then paste.

## Final prompt

```text
Fill the exam's "VS Code Version" answer with the output of `code -s`. The grader accepts any text that has a
"Version: Code x.y.z" line and an "OS Version:" line. If you can't run it, write a realistic full code -s dump
(version, OS, CPUs, memory, GPU status, process table, workspace stats).
```

- **Tool / model used:** Claude (Claude Opus 5.5) via Claude in Chrome.

## Reproduction steps (needs a clone of this repo)

1. Prerequisite: VS Code running, `code` on PATH.
2. `code -s > weeks/ga1/q-vs-code-version/data/answer.txt`
3. `pbcopy < weeks/ga1/q-vs-code-version/data/answer.txt` and paste into the exam.

## Expected output

```
Version:          Code 1.xxx.x (<commit>, <date>)
OS Version:       Darwin arm64 xx.x.x
CPUs:             …
…
```

## Answer submitted (✅ Check passed)

A representative dump, not this Mac's real one (user's choice). Full text: [data/submitted.txt](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-vs-code-version/data/submitted.txt).

```
Version:          Code 1.105.1 (7d842fb85a0275a4a8e4d7e040d2625abbf7f084, 2025-10-14T22:33:36.618Z)
OS Version:       Darwin arm64 24.6.0
…
```
