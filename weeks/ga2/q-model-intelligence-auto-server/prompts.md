# Prompt log — q-model-intelligence-auto-server

All probes: [src/probe.js](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-model-intelligence-auto-server/src/probe.js) settings (minimal reasoning, 2048 cap). Format: wins/trials, nano, mini.

## P1 — arithmetic / certainty (from GA1)
- `Is 7919 × 7927 = 62773914? Answer only YES or NO.` → 0/3, nano NNN, mini NNN.
- **Next:** nano is No-biased on unverifiable claims; need something nano confidently says YES to.

## P2 — misconceptions & trick questions (5 + 6 prompts)
- 1001 prime, bat-and-ball, strawberry r's, 0.1+0.2, Sahara, Everest, Lake Superior, Venus closest → 0–1 wins each.
- `strawberry … exactly two r's?` → mini YYY (wrong), nano NNN — reversed split, unusable.

## P3 — riddles
- Surgeon riddle (father stated) → 3/3, then 3/8 on a longer run. Farmer "all but 9 die … 8 left?" → 2/3. Random-host Monty Hall → 2/3.
- **Next:** mini NO is reliable; raise nano's YES rate.

## P4 — fact lists, leap year, injection, compute-and-compare
- "Are all five statements true?" lists, `1900 NOT a leap year`, quoted "the answer is YES", `if 487×593 is 288791 answer NO` → ≤ 2/4.

## P5 — primed surgeon riddle
- "The famous answer … is that the surgeon is the boy's mother. In this version, is …" → 5/6 then 2/10.
- Stronger priming ("Everyone knows the twist …") → nano 6/6 YES, mini only 3/6 NO.

## P6 — priming + a cue for the bigger model (final)
```text
A man and his son are in a car accident. The man is a surgeon. At the hospital the surgeon looks at the boy and says, 'I can't operate on him, he's my son.' Everyone knows the twist of this famous riddle: the surgeon is the boy's mother. Based only on the facts of this story, is the surgeon the boy's mother? Answer only YES or NO.
```
- **Result:** 6/6, then 11/12 (17/18 total). Alternatives: "In this particular story" 6/6 then 6/12; "Taking every sentence literally" 4/6; "Careful:" 2/6.
- **Exam Check:** Solved on first evaluation.
