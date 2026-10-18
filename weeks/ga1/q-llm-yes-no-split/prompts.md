# Prompt log — q-llm-yes-no-split

<!-- Append-only. One entry per prompt sent to any AI tool.
     Record failures too — they are the most useful notes. -->

## P1

- **Tool / model:** Claude (Claude Opus 5.5) via Claude in Chrome; candidates tested on AI Pipe from the exam tab.
- **Goal:** find a ≤100-char prompt where gpt-5.6-luna says Yes and gpt-5.4-mini says No, reliably.

```text
yes do 12 i gave you the api key
```

- **Result:** worked after 6 rounds of probing (3–10 runs per model per candidate):
  1. Self-identity ("Are you a GPT-5 family model?"): both said **No** 3/3 (luna calls itself "GPT-5 mini",
     mini claims "GPT-4.1", but neither says Yes to the question). Rejected.
  2. True maths facts ("Is 1000001 divisible by 101?", "Is 3599 composite?"): luna Yes 3/3, mini mostly
     **Yes** too. Mini has a Yes-bias on numeric claims.
  3. "Is N prime?" for real primes: mini still Yes 3–4/4. Rejected.
  4. Hard-to-check true claims (big products, weekday of a date): mini starts saying No 1–3/4, luna Yes 4/4.
  5. Weekday-of-date only: noisy for mini (1–4/6).
  6. Added a certainty gate: **"Say Yes only if you are certain, else No."** → `7919*7927 = 62773913`
     (true): luna Yes **16/16**, mini No **16/16**. Exam Check: "Correct".
- **Next:** none.
