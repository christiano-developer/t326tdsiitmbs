# Final — q-llm-yes-no-split

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-llm-yes-no-split](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-llm-yes-no-split)

## How to solve (for a teammate)

> Not seeded: the same prompt should work for anyone, but model behaviour drifts. Re-test before submitting.

**Approach:** don't look for a fact the two models "know" differently; look for a **capability gap**. Ask about a
claim that is *true* but can only be confirmed by actually working it out, and add a certainty gate: *"Say Yes only
if you are certain, else No."* The larger model verifies it and says Yes; the small model can't, so the gate makes it
say No. Plain trap questions don't work: the small model says Yes to most numeric claims.

1. Open the exam page, DevTools → Console, paste `probe.js` (below). It asks for your AI Pipe token (kept in the
   browser only) and runs each candidate 6× on both models.
2. Try a few candidates of the form `Is <a>*<b> = <true product>? Say Yes only if you are certain, else No. One word.`
   (4-digit numbers; compute the product yourself). Keep one that scores 6/6 on both.
3. Paste it into the answer box, Check (it asks for the token once), Save.

<details><summary>probe.js (click to expand)</summary>

```js
// Run in the DevTools console on the exam page (aipipe.org allows browser calls).
// Tests candidate prompts N times on both models and reports how often each gives the required word.
// Each call costs AI Pipe credit: keep N small.
const TOKEN = prompt("AI Pipe token");            // never hard-code it
const ask = async (model, content) => {
  const r = await fetch("https://aipipe.org/openai/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${TOKEN}` },
    body: JSON.stringify({ model, messages: [{ role: "user", content }] }),
  });
  const j = await r.json();
  return j.choices?.[0]?.message?.content ?? JSON.stringify(j);
};
const yes = (s) => /\bYes\b/.test(s) && !/\bNo\b/.test(s);
const no = (s) => /\bNo\b/.test(s) && !/\bYes\b/.test(s);
async function probe(candidates, n = 6) {
  for (const p of candidates) {
    const runs = await Promise.all([...Array(n)].flatMap(() => [ask("gpt-5.6-luna", p), ask("gpt-5.4-mini", p)]));
    const L = runs.filter((_, i) => i % 2 === 0), M = runs.filter((_, i) => i % 2 === 1);
    console.log(`${p.length} chars | luna Yes ${L.filter(yes).length}/${n} | mini No ${M.filter(no).length}/${n} | ${p}`);
  }
}
probe([
  "Is 7919*7927 = 62773913? Say Yes only if you are certain, else No. One word.",
]);
```

</details>

## Final prompt

```text
Find a prompt of at most 100 characters that makes gpt-5.6-luna reply Yes and gpt-5.4-mini reply No
(case-sensitive, no system prompt). Use a true claim that needs real computation to confirm, plus
"Say Yes only if you are certain, else No. One word." Probe each candidate several times on both models.
```

- **Tool / model used:** Claude (Claude Opus 5.5) via Claude in Chrome.

## Reproduction steps (needs a clone of this repo)

Run [src/probe.js](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-llm-yes-no-split/src/probe.js)
in the exam page console with your AI Pipe token.

## Expected output

```
76 chars | luna Yes 6/6 | mini No 6/6 | Is 7919*7927 = 62773913? Say Yes only if you are certain, else No. One word.
```

## Answer submitted (✅ Check passed)

```
Is 7919*7927 = 62773913? Say Yes only if you are certain, else No. One word.
```
