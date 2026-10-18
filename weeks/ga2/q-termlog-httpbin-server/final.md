# Final — q-termlog-httpbin-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-termlog-httpbin-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-termlog-httpbin-server)

## How to solve (for a teammate)

Assigned values (tags, IDs, parameters) are **seeded per email**: use the ones on your exam page.

**Approach:** Define the capture helper inside a termlog recording, run seven precise curl invocations, exit, tar the cast + signed receipt **without macOS metadata**, host as a GitHub release asset.

1. Install termlog, `termlog login` with your exam email. Work in an empty folder.
2. `termlog rec httpbin.cast`, then inside the recording (replace `<TAG>`/`<QTY>`/`<STATUS>` with your values):

```bash
capture() { task="$1"; shift; printf '\nHTTPBIN_BEGIN <TAG> %s\n' "$task"; "$@"; printf '\nHTTPBIN_END <TAG> %s\n' "$task"; }
capture GET curl -sS -G https://httpbin.org/get --data-urlencode course=TDS --data-urlencode tag=<TAG> -H 'X-Exam-Tag: <TAG>'
capture POST curl -sS -X POST https://httpbin.org/post -H 'Content-Type: application/json' -d '{"tag":"<TAG>","quantity":<QTY>,"active":true}'
capture FORM curl -sS -X PUT https://httpbin.org/put --data-urlencode tag=<TAG> --data-urlencode quantity=<QTY>
capture AUTH curl -sS https://httpbin.org/bearer -H 'Authorization: Bearer <TAG>'
capture REDIRECT curl -sS -L -G https://httpbin.org/redirect-to --data-urlencode 'url=https://httpbin.org/get?tag=<TAG>'
curl -sS -c /tmp/httpbin-jar.txt -o /dev/null 'https://httpbin.org/cookies/set?exam=<TAG>'
capture COOKIES curl -sS -b /tmp/httpbin-jar.txt https://httpbin.org/cookies
capture STATUS curl -sS -o /dev/null -w '%{http_code}' https://httpbin.org/status/<STATUS>
exit
```
3. Check outputs before `exit`: JSON for each, POST shows `"quantity": <QTY>` (number) and `"active": true`, COOKIES shows your tag, STATUS prints only the code. Re-run any capture where HTTPBin returned an error page (the last complete capture per label counts).
4. Package **without macOS metadata** (otherwise the grader fails with an `atob()` error):
   `COPYFILE_DISABLE=1 tar --no-mac-metadata --no-xattrs -czf submission.tar.gz httpbin.cast httpbin.cast.jwt` and confirm `tar -tzf submission.tar.gz` lists only those two files.
5. Host it: `gh release create <tag-name> submission.tar.gz` and submit `https://github.com/<you>/<repo>/releases/download/<tag-name>/submission.tar.gz`. To replace later: `gh release upload <tag-name> submission.tar.gz --clobber`.

Gotchas: bsdtar on macOS stores xattrs as `._httpbin.cast.jwt`; the grader picks that binary file as the receipt → `atob() called with invalid base64`. Build with `COPYFILE_DISABLE=1 tar --no-mac-metadata --no-xattrs`. Must be *outside* the COOKIES capture; use a jar file (`-c` then `-b`). Send raw JSON with `-d '{…"quantity":8,"active":true}'` so they stay number/boolean. `-X PUT --data-urlencode` sends `application/x-www-form-urlencoded`. `-o /dev/null -w '%{http_code}'` prints only `400`. `http-…` is a dummy bearer token; never put a real key in a recording.

## Final prompt

```text
HTTPBin terminal lab (termlog) (2 marks)
<paste the full question with your assigned values>
Give me the exact files and terminal commands for macOS (zsh) to satisfy every grader check, including
how to expose it publicly / package it, plus a quick local test for each check.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

See the steps above; code lives in [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-termlog-httpbin-server/src](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-termlog-httpbin-server/src).

## Expected output

Exam **Check** marks the question solved.

## Answer submitted

```
https://github.com/<you>/<repo>/releases/download/ga2-termlog-httpbin/submission.tar.gz
```
