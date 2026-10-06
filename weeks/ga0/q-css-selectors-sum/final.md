# Final — q-css-selectors-sum

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
On the exam page there is a hidden list <ul class="products d-none"> of <li> elements with classes and a
data-discount attribute. Give me a one-line DevTools console snippet that sums data-discount over
elements matching ul.products li.featured.sale, and also prints how many matched.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

Either:

1. **DevTools** (on the exam page, Console):

```js
[...document.querySelectorAll('ul.products li.featured.sale')].reduce((t, e) => t + Number(e.dataset.discount), 0)
```

2. **Seed regeneration** (offline):

```bash
npm i seedrandom@3            # once, in a scratch folder
node src/regenerate.mjs <exam-email>
```

Enter the integer as a bare number.

## Expected output

```
 7  ✓  <li class="featured sale" data-discount="23">
 8  ✓  <li class="sale featured" data-discount="47">
 9  ✓  <li class="featured sale vip" data-discount="33">
10  ✓  <li class="featured sale vip" data-discount="36">
13  ✓  <li class="featured sale" data-discount="45">
14  ✓  <li class="featured sale" data-discount="40">
18  ✓  <li class="sale featured" data-discount="21">
19  ✓  <li class="featured sale" data-discount="48">

ANSWER sum of data-discount on .featured.sale: 293
```

## Answer submitted (✅ passed, attempt 1)

```
293
```
