# Approaches — q-llm-yes-no-split

## Problem in one line

A ≤100-char prompt where luna answers Yes and 5.4-mini answers No.

## Grader (from quiz JS)

- Client-side, **in your browser with your AIPipe token**: 2 calls per Check (`aipipe.org/openai/v1/chat/completions`),
  no temperature set. Same prompt is cached and not re-sent.
- Pass: luna reply matches `/\bYes\b/` and not `/\bNo\b/`; mini reply the reverse.
- Not seeded.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Cost | Note | Every Check and every local test costs AIPipe credit → get approval first |
| Weight | Note | Function default 2, registry 1 → 1 mark |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | Self-identity question | AI Pipe | Cheap | Neither model answers Yes about itself | rejected |
| B | Knowledge-cutoff question | AI Pipe | Natural split | Both report the same cutoff | rejected |
| C | A **true** claim the strong model can verify but the small one can't, plus "Yes only if certain, else No" | AI Pipe | Exploits capability, not luck; small model defaults to No | Needs probing | chosen |

## Chosen: C

**Why:** the certainty gate turns the small model's uncertainty into a stable No, while the larger model actually
verifies the claim and answers Yes. Choose a claim that is true but not checkable by recall
(here a 4-digit × 4-digit product).

## Gotchas hit

- Bare numeric yes/no claims: the small model answers Yes most of the time (Yes-bias), so "trap" facts alone don't work.
- The grader is case-sensitive and needs exactly one of the words; "One word." keeps replies clean.
- Each Check and each probe costs AI Pipe credit; probe in batches with a handful of runs.
- The token stays in the browser (`globalThis.aiPipeToken` / a `prompt()`), never in files.

## Verification

- 16 runs per model: luna Yes 16/16, mini No 16/16.
- Exam **Check** → "Correct" (2026-10-18).
