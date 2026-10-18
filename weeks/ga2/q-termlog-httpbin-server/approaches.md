# Approaches — q-termlog-httpbin-server

## Problem in one line

Define the capture helper inside a termlog recording, run seven precise curl invocations, exit, tar the cast + signed receipt **without macOS metadata**, host as a GitHub release asset.

## ⚠️ Distractors, gotchas and hidden text

| Item | Type | Reality |
|------|------|---------|
| macOS tar adds `._*` AppleDouble files | Gotcha (cost a Check) | bsdtar on macOS stores xattrs as `._httpbin.cast.jwt`; the grader picks that binary file as the receipt → `atob() called with invalid base64`. Build with `COPYFILE_DISABLE=1 tar --no-mac-metadata --no-xattrs`. |
| Cookie-set call | Genuine | Must be *outside* the COOKIES capture; use a jar file (`-c` then `-b`). |
| Types in POST | Genuine | Send raw JSON with `-d '{…"quantity":8,"active":true}'` so they stay number/boolean. |
| FORM | Genuine | `-X PUT --data-urlencode` sends `application/x-www-form-urlencoded`. |
| STATUS | Genuine | `-o /dev/null -w '%{http_code}'` prints only `400`. |
| Dummy token | Note | `http-…` is a dummy bearer token; never put a real key in a recording. |

Scanned the question HTML for hidden elements/comments: none found.

## Verification

- Exam **Check** passed on 2026-10-18 (run by the user on their Mac; tunnels/recordings are local).
