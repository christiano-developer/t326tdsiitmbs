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
