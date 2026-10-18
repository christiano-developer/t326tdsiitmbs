# Final — q-model-intelligence-auto-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-model-intelligence-auto-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-model-intelligence-auto-server)

## How to solve (for a teammate)

Not seeded — the same prompt works for everyone. You just need your AI Pipe token.

**Approach (generalised):** you need the *weaker* model to be confidently wrong with YES and the *stronger* one right with NO. At minimal reasoning effort, nano defaults to NO on anything it can't verify, so plain false claims don't work. What works is a **misleading premise**: take a famous riddle, change one fact so the famous answer becomes wrong, **prime the famous answer** in the prompt (nano pattern-matches it → YES), and add a cue that makes the stronger model re-read the actual story (**"Based only on the facts of this story"** → mini NO).

1. Open the exam page, open DevTools → Console, run `globalThis.aiPipeToken = "<your AI Pipe token>"`.
2. (Optional, recommended) Paste this probe to test candidates cheaply before spending a graded evaluation:

<details><summary>probe.js (click to expand)</summary>

```js
// Run in the DevTools console on the exam page (aipipe.org allows browser calls).
// Set your token first:  globalThis.aiPipeToken = "<AI Pipe token>"   (never hard-code it)
// Mirrors the grader: single user message, reasoning_effort "minimal", max_completion_tokens 2048,
// win = nano says YES and mini says NO *in the same trial*. Each trial = 2 calls of AI Pipe credit.
const ask = async (model, content) => {
  const r = await fetch("https://aipipe.org/openai/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${globalThis.aiPipeToken}` },
    body: JSON.stringify({ model, messages: [{ role: "user", content }], reasoning_effort: "minimal", max_completion_tokens: 2048 }),
  });
  const j = await r.json();
  return j.choices?.[0]?.message?.content ?? "ERR " + (j.error?.message || r.status);
};
const norm = (s) => { const t = String(s).trim().replace(/[.!]$/, "").trim().toUpperCase(); return t === "YES" ? "Y" : t === "NO" ? "N" : "?"; };
async function probe(prompts, n = 6) {
  for (const p of prompts) {
    const runs = await Promise.all([...Array(n)].flatMap(() => [ask("gpt-5-nano-2025-08-07", p), ask("gpt-5-mini-2025-08-07", p)]));
    const nano = runs.filter((_, i) => i % 2 === 0).map(norm).join(""), mini = runs.filter((_, i) => i % 2 === 1).map(norm).join("");
    let win = 0; for (let i = 0; i < n; i++) if (nano[i] === "Y" && mini[i] === "N") win++;
    console.log(`win ${win}/${n} nano=${nano} mini=${mini} :: ${p}`);
  }
}
probe([
  "A man and his son are in a car accident. The man is a surgeon. At the hospital the surgeon looks at the boy and says, 'I can't operate on him, he's my son.' Everyone knows the twist of this famous riddle: the surgeon is the boy's mother. Based only on the facts of this story, is the surgeon the boy's mother? Answer only YES or NO.",
]);
```

</details>

   You want ≥ 10/12 same-trial wins; short runs are noisy.
3. Paste the final prompt (below) into the Q2 textarea **by typing/pasting** (not by script), press **Check** (enter your token if asked), then **Save**.
4. If it fails: results are cached per exact prompt, so change the wording slightly (e.g. a different cue sentence) and probe again before re-checking.

## Final prompt

```text
A man and his son are in a car accident. The man is a surgeon. At the hospital the surgeon looks at the boy and says, 'I can't operate on him, he's my son.' Everyone knows the twist of this famous riddle: the surgeon is the boy's mother. Based only on the facts of this story, is the surgeon the boy's mother? Answer only YES or NO.
```

- **Tool / model used:** Claude (Opus 5.5) designing candidates; probed against `gpt-5-nano-2025-08-07` / `gpt-5-mini-2025-08-07` via AI Pipe.

## Reproduction steps (needs a clone of this repo)

1. Exam page → DevTools console → `globalThis.aiPipeToken = "…"`.
2. Paste [src/probe.js](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-model-intelligence-auto-server/src/probe.js) into the console; it runs the final prompt 6 times on both models.

## Expected output

```
win 6/6 nano=YYYYYY mini=NNNNNN :: A man and his son are in a car accident. …
```
(17/18 over two runs on 2026-10-18; an occasional nano NO is expected.)

## Answer submitted

```
A man and his son are in a car accident. The man is a surgeon. At the hospital the surgeon looks at the boy and says, 'I can't operate on him, he's my son.' Everyone knows the twist of this famous riddle: the surgeon is the boy's mother. Based only on the facts of this story, is the surgeon the boy's mother? Answer only YES or NO.
```
