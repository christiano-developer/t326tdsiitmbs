# Approaches — q-use-devtools

## Problem in one line

Read the `value` of a hidden `<input>` on the exam page.

## Grader (from quiz JS)

Value = `seedrandom("<email>#q-use-devtools")().toString(36).slice(-10)` (10 base-36 chars). The answer must equal it.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Hidden `<input>` "just above this paragraph" | **Hidden text: required input** | It's the answer itself, visible only in the DOM |
| Hidden markup elsewhere | Not relevant | Only this input matters |

## Options considered

| # | Approach | Verdict |
|---|----------|---------|
| A | **DevTools: Elements panel (or Console: `$$('input[type=hidden]').map(e => e.value)`)** | **chosen (user did this)** |
| B | Regenerate from the seed | used only as a cross-check |

## Verification

- User read `6dprrqe39p` in DevTools; the seed regenerates `6dprrqe39p` (match).
- Exam "Check" button: ✅ passed (2026-10-06).
