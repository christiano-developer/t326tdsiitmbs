# Final — q-broken-json-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-broken-json-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-broken-json-server)

## How to solve (for a teammate)

> Seeded per email: your file and its errors differ from mine. The grader compares the **parsed data**, so
> formatting doesn't matter, but you must not change any value.

1. On the exam page click **Download Broken JSON (ZIP)** and unzip it. You get `broken.json` (~180 KB) and a README.
2. Save the script below as `fix.mjs` next to `broken.json` (needs Node 18+, no packages).
3. Run `node fix.mjs broken.json > fixed.json`. It prints how many errors of each kind it fixed and `records: 300`.
4. If it crashes with a JSON error instead, open `broken.json` at the reported line: the remaining error is
   usually a deleted `{` line or a doubled `}}`. Fix that by hand and rerun.
5. Copy `fixed.json` into the answer box (`pbcopy < fixed.json` on macOS, don't copy from the terminal),
   then Check and Save.

<details><summary>fix.mjs (click to expand)</summary>

```js
import { readFileSync } from "node:fs";

let s = readFileSync(process.argv[2] ?? "broken.json", "utf8");
const log = [];
const pass = (name, re, fn) => { s = s.replace(re, (...m) => { log.push(name); return fn(...m); }); };

pass("single-quoted key", /^(\s*)'([^'\n]*)'(\s*):/gm, (_, a, k, b) => `${a}"${k}"${b}:`);
pass("unquoted key", /^(\s*)([A-Za-z_]\w*)(\s*):/gm, (_, a, k, b) => `${a}"${k}"${b}:`);
pass("single-quoted value", /:(\s*)'([^'\n]*)'(\s*[,\n}])/g, (_, a, v, b) => `:${a}"${v}"${b}`);
pass("trailing comma", /,(\s*)([\]}])/g, (_, a, b) => `${a}${b}`);
pass("missing comma", /(["\d\]}el])([ \t]*\n[ \t]*)(?=["{\[])/g, (_, a, b) => `${a},${b}`);

const data = JSON.parse(s);
console.error(`fixed ${log.length}: ${[...new Set(log)].map((n) => `${n} x${log.filter((x) => x === n).length}`).join(", ")}`);
console.error(`records: ${data.length}`);
process.stdout.write(JSON.stringify(data, null, 2));
```

</details>

## Final prompt

```text
Here is broken.json (≈180 KB, ~8 injected syntax errors: single-quoted or unquoted keys, trailing commas,
missing commas, possibly a deleted "{" line or a doubled "}}"). Write a Node script that repairs only the
syntax with targeted regex passes (quote keys first, then remove trailing commas, then add missing commas),
JSON.parses the result, prints a count per fix type and the record count, and writes pretty JSON to stdout.
Do not change any values.
```

- **Tool / model used:** Claude (Claude Opus 5.5) via Claude in Chrome.

## Reproduction steps (needs a clone of this repo)

```bash
cd weeks/ga1/q-broken-json-server/src
node fix.mjs ../data/broken.json > /tmp/repaired.json
# cross-check against the seed rebuild (needs `npm install` here for seedrandom)
EXAM_EMAIL=ROLL_NUMBER@ds.study.iitm.ac.in node valid.mjs | node -e '
  const a=require("fs").readFileSync(0,"utf8");
  const b=JSON.stringify(JSON.parse(require("fs").readFileSync("/tmp/repaired.json","utf8")));
  console.log(a===b ? "identical" : "DIFFERENT")'
pbcopy < /tmp/repaired.json
```

## Expected output

```
fixed 8: single-quoted key x2, unquoted key x3, trailing comma x1, missing comma x2
records: 300
identical
```

## Answer submitted (✅ Check passed)

The 300-record repaired JSON (pretty-printed). Same data as [data/fixed.json](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-broken-json-server/data/fixed.json).
