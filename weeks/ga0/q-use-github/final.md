# Final — q-use-github

> Goal: the answer can be reproduced from this file alone.

## Final prompt

```text
Give me the commands to add email.json containing {"email": "<EXAM_EMAIL>"} to my public GitHub repo, push it,
and build the raw.githubusercontent.com URL pinned to the commit SHA. Then a curl command to verify the JSON.
```

- **Tool / model used:** Claude Code (Claude Opus 5.5).

## Reproduction steps

```bash
printf '{"email": "<exam-email>"}\n' > weeks/ga0/q-use-github/email.json
git add weeks/ga0/q-use-github && git commit -m "solved(ga0/q-use-github): ..." && git push origin ga0
SHA=$(git rev-parse HEAD)
URL="https://raw.githubusercontent.com/christiano-developer/t326tdsiitmbs/$SHA/weeks/ga0/q-use-github/email.json"
weeks/ga0/q-use-github/src/check_raw_url.sh "$URL" "<exam-email>"
echo "$URL"   # submit this
```

## Expected output

```
PASS host is raw.githubusercontent.com
PASS email matches exactly
```

## Answer submitted

The commit-pinned raw URL (see README → Final answer).
