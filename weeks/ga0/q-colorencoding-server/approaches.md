# Approaches — q-colorencoding-server

## Problem in one line

Replace a sequential colour ramp on unordered categories with a categorical palette that passes the
grader's CIEDE2000 test, and explain the false hierarchy the ramp implied.

## Grader (from quiz JS)

- Variant seeded from `email#q-colorencoding-server` → 1 of ~18 charts. **Mine: "Website Traffic by Source",
  correct type `categorical`.** Expected palette in the JS: Tableau `#4e79a7 #f28e2b #e15759 #76b7b2 #59a14f`.
- Checks, all collected and then reported together:
  1. Submission ≥ 50 chars.
  2. **Hex extraction:** every `#rgb` / `#rrggbb` in the **whole submission** (CSS, comments, text, JS),
     deduped in order of appearance. At least 2 needed.
  3. Rainbow: only if ≥ 6 colours; HSV hue span must be ≤ 270°.
  4. Categorical: **pairwise CIEDE2000 ≥ 30 across the first 8 extracted colours.**
  5. The word `categorical` appears anywhere (case-insensitive).
  6. One of these phrases appears: *"falsely implies traffic sources have a natural progression"*,
     *"hierarchy among sources"*, *"implies ordering among unordered sources"*,
     *"traffic sources have a natural progression"*, *"false hierarchy"*.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| Code comment in the broken chart: `// WRONG: categorical palette applied to sequential data` | **Distractor** | Backwards. It's a **sequential** palette on **categorical** data. Copying the comment's framing gives the wrong scheme word and explanation |
| Primer: "Categorical: Tableau 10, `#4e79a7 #f28e2b #e15759 #76b7b2 #59a14f`" (also the grader's own `pal`) | **Distractor / trap** | The first 5 Tableau colours **fail the grader's own ΔE ≥ 30 check**: blue/teal 27.6, orange/red 27.5, teal/green 22.9. The best 5 from all of Tableau 10 only reach 26.5 |
| Page CSS colours (`#ffffff #212529 #6c757d #f8f9fa #adb5bd`) | **Hidden trap** | Not mentioned anywhere, but the extractor reads them first. `#ffffff` vs `#f8f9fa` = ΔE 1.4 → fail. Swapping only the bar colours fails (confirmed) |
| Quoting the old palette in the explanation comment | Trap | Those hexes would be extracted too. The explanation must not contain any hex |
| Hint "categories have no inherent order" | Genuine | Correct |
| Hidden markup in this question | None found | Scanned the question template for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, zero opacity or font size |

## Options considered

| # | Approach | Result (src/check.py) | Verdict |
|---|----------|----------------------|---------|
| A | Swap bar colours to the primer's Tableau 5, keep the page as-is | FAIL: CSS greys + Tableau pairs < 30 (8 violations) | rejected |
| B | Tableau 5 and strip the CSS hexes | FAIL: 3 Tableau pairs < 30 | rejected |
| C | Best 5-colour subset of Set1 | PASS at min 31.2 (thin margin; includes a pure yellow) | backup |
| D | **Okabe-Ito (colour-blind safe) without black + no other hex in the file** | **PASS, min 37.0** | **chosen** |

Palette search: brute-forced every 5-colour subset of Tableau 10, Set1, Dark2 and Okabe-Ito with the
grader's exact CIEDE2000. Okabe-Ito's best set includes black (38.4), which disappears on the dark-mode
background, so I used the best non-black set: `#0072b2 #d55e00 #009e73 #cc79a7 #f0e442` (37.0).

## Chosen: D

**Why:** largest safe margin that still renders well in light and dark mode, and colour-blind safe.
CSS colours were rewritten as `white` / `rgb(…)` (identical values), so the bars are the only hexes. The
explanation sits in a top HTML comment and repeats in visible text, using two accepted phrases
("falsely implies traffic sources have a natural progression", "false hierarchy") and the word "categorical".

## Gotchas

- **The extractor sees everything.** Any hex anywhere counts: CSS, comments, prose. Keep only palette hexes.
- **Don't trust the primer's palette.** Verify against the grader's ΔE implementation.
- The grader's CIEDE2000 has a non-standard hue quirk (adds 360° when b < 0 *or* a′ < 0). `check.py` copies it,
  so its numbers match the grader, not textbook ΔE00.

## Verification

- `python3 src/check.py src/corrected.html` → PASS (5 hexes, 10 pairs, min 37.0).
- Negative controls (scratch, not kept): option A → 8 pair failures; option B → 3 pair failures.
- Rendered → [data/corrected-chart.png](data/corrected-chart.png): five distinct hues; dark mode intact.
- Exam "Check" button: ✅ passed on attempt 1 (2026-10-06).
