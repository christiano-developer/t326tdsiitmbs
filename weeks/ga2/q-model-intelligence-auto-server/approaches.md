# Approaches — q-model-intelligence-auto-server

## Problem in one line

Find a prompt where the *weaker* model (nano) says YES and the *stronger* one (mini) says NO, reliably enough that ≥ 2 of 3 trials win (per-trial win rate ≳ 80 %).

## Grader (from quiz JS)

- Server-side (`/backendVerify`) with your AI Pipe token: 3 trials × 2 models, `reasoning_effort: "minimal"`, `max_completion_tokens: 2048`.
- Pass only if nano = YES **and** mini = NO in the same trial, in ≥ 2 trials. Cached per exact trimmed prompt — a failed prompt stays failed; edit it to re-run.
- Not seeded.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "Try a subtle contradiction, a misleading premise or a reasoning problem" | Genuine hint | Misleading premise is what worked. |
| Cost / cache | Note | Every probe and every new Check spends AI Pipe credit; probe in the console first, Check once. |
| Direction | Trap | Reverse of GA1 (there the strong model said Yes). Certainty-gating makes nano say NO, the wrong way here. |

Scanned for hidden text: none found.

## Options considered (probe results, wins = same-trial nano YES & mini NO)

| # | Idea | Example | Result |
|---|------|---------|--------|
| A | False arithmetic claim | `7919 × 7927 = 62773914?` | 0/3 — nano answers NO to anything it can't verify |
| B | Classic misconceptions | Sahara largest desert, Everest farthest from centre, Lake Superior largest | 0–1/4 — nano knows them too |
| C | Pedantic truths | "exactly five senses", "Earth a perfect sphere" | 0/4 — both models agree |
| D | Prompt-injection in quoted text | quoted "the answer is YES" | ≤ 1/4 — nano resists too |
| E | Compute-and-compare | "if 487×593 is 288791 answer NO else YES" | mixed — at minimal effort *both* mis-multiply |
| F | Trick riddles (surgeon, "all but 9 die", random-host Monty Hall) | plain surgeon riddle | 3/8 — mini NO is solid, nano YES only ~50 % |
| G | Surgeon riddle **primed** with "everyone knows the twist: the surgeon is the mother" | | nano YES 100 %, but mini also drifts to YES (2–3/6) |
| H | G + a cue only the bigger model acts on: "**Based only on the facts of this story**" | final prompt | **17/18** wins |

## Chosen: H

**Why:** the priming sentence overrides nano's reading of the story (it pattern-matches the famous answer), while the "based only on the facts" cue makes mini re-read: the story literally says the man is the father. Other cues tested: "In this particular story" 12/18 (mini wavers), "Taking every sentence literally" 4/6 (nano starts reading carefully), "Careful:" 2/6.

## Gotchas hit

- `==` or query-string-looking text in browser-tool output gets blocked; mask before printing.
- Short runs lie: S2 looked 5/6 then 2/10. Confirm with ≥ 12 trials before spending a graded evaluation.

## Verification

- Probe (exact grader settings): 17/18 same-trial wins (nano YES 17/18, mini NO 18/18) → P(≥ 2 of 3) ≈ 0.99.
- Exam **Check** → Solved on the first graded evaluation (2026-10-18).
