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
