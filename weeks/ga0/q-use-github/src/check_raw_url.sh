#!/usr/bin/env bash
# Replica of the GA0 q-use-github grader: host must be raw.githubusercontent.com and the fetched JSON's
# "email" must equal the exam email exactly.
# Usage: src/check_raw_url.sh <raw-url> <exam-email>
set -euo pipefail
URL="${1:?raw url}"; EMAIL="${2:?exam email}"

case "$URL" in
  https://raw.githubusercontent.com/*) echo "PASS host is raw.githubusercontent.com" ;;
  *) echo "FAIL URL should be https://raw.githubusercontent.com/..."; exit 1 ;;
esac

curl -s "$URL" | EMAIL="$EMAIL" python3 -c "
import json, os, sys
d = json.load(sys.stdin)
ok = d.get('email') == os.environ['EMAIL']
print('PASS email matches exactly' if ok else 'FAIL email does not match: ' + json.dumps(d))
sys.exit(0 if ok else 1)
"
