#!/usr/bin/env bash
# Replica of the GA0 q-ollama grader (browser fetch from the exam page), including the CORS preflight that the custom
# `ngrok-skip-browser-warning` header triggers.
# Usage: src/check_ngrok.sh https://xxxx.ngrok-free.app <exam-email>
set -uo pipefail
URL="${1:?ngrok url}"; EMAIL="${2:?exam email}"; URL="${URL%/}"
ORIGIN="https://exam.sanand.workers.dev"; fail=0
ok()  { echo "PASS $*"; }
bad() { echo "FAIL $*"; fail=1; }

case "$URL" in *ngrok*) ok "hostname contains ngrok" ;; *) bad "hostname must contain ngrok" ;; esac

# 1. Preflight (OPTIONS) - what the browser sends before the real GET
pre=$(curl -s -D - -o /dev/null -X OPTIONS "$URL/api/version" -H "Origin: $ORIGIN" \
  -H "Access-Control-Request-Method: GET" -H "Access-Control-Request-Headers: ngrok-skip-browser-warning")
echo "$pre" | grep -qiE '^HTTP/[0-9.]+ (200|204)' && ok "preflight status 2xx" || bad "preflight status: $(echo "$pre" | head -1)"
echo "$pre" | grep -qi '^access-control-allow-origin: \*' && ok "preflight Allow-Origin *" || bad "preflight lacks Access-Control-Allow-Origin: *"
echo "$pre" | grep -i '^access-control-allow-headers:' | grep -qi 'ngrok-skip-browser-warning' \
  && ok "preflight allows ngrok-skip-browser-warning" || bad "preflight doesn't allow ngrok-skip-browser-warning"

# 2. Real GET
hdr=$(mktemp); body=$(curl -s -D "$hdr" "$URL/api/version" -H "Origin: $ORIGIN" -H "ngrok-skip-browser-warning: true")
echo "body: $body"
echo "$body" | python3 -c "import json,sys; v=json.load(sys.stdin).get('version'); sys.exit(0 if v else 1)" 2>/dev/null \
  && ok "JSON has version (Ollama)" || bad "no .version in body (not Ollama / ngrok warning page?)"
grep -qi '^access-control-allow-origin: \*' "$hdr" && ok "GET Allow-Origin *" || bad "GET lacks Access-Control-Allow-Origin: *"
grep -qi '^access-control-expose-headers: \*' "$hdr" && ok "Expose-Headers * (JS can read X-Email)" || bad "missing Access-Control-Expose-Headers: *"
got=$(grep -i '^x-email:' "$hdr" | head -1 | cut -d: -f2- | tr -d ' \r')
[ "$got" = "$EMAIL" ] && ok "X-Email matches" || bad "X-Email is '$got'"
rm -f "$hdr"
echo; [ $fail -eq 0 ] && echo "ALL CHECKS PASS - submit $URL" || echo "SOME CHECKS FAILED"
exit $fail
