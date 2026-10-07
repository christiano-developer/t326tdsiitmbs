# Final — q-use-devtools

> Goal: the answer can be reproduced from this file alone.

## How to solve (for a teammate)

> Values are seeded from your email, so your answer will differ from ours (see "Answer submitted").

1. On the exam page, open DevTools (Ctrl+Shift+I; Mac: Cmd+Opt+I) and click the **Console** tab.
2. Paste this and press Enter:
   ```js
   $$('input[type=hidden]').map(e => e.value)
   ```
3. It prints a list containing a 10-character code like `6dprrqe39p`. Enter that code, then Check and Save.

## Final prompt

None needed. Open DevTools on the exam page and run in the Console:

```js
$$('input[type=hidden]').map(e => e.value)
```

## Reproduction steps

1. Cmd+Opt+I → Elements: find the hidden `<input>` above the question paragraph, or use the Console snippet above.
2. Copy its `value` and submit it.
3. Optional cross-check: `node -e 'console.log(require("seedrandom")(process.argv[1]+"#q-use-devtools")().toString(36).slice(-10))' "<exam-email>"`

## Expected output

```
6dprrqe39p
```

## Answer submitted

`6dprrqe39p`
