#!/usr/bin/env bash
# Replica of the GA0 q-github-action grader: unauthenticated GitHub API, MOST RECENT run only,
# PASS if any step name in its jobs contains the email.
# Usage: src/check_latest_run.sh <owner/repo> <exam-email>
set -euo pipefail
REPO="${1:?owner/repo}"; EMAIL="${2:?exam email}"

runs=$(curl -s "https://api.github.com/repos/$REPO/actions/runs")
jobs_url=$(echo "$runs" | python3 -c "import json,sys; r=json.load(sys.stdin)['workflow_runs']; print(r[0]['jobs_url'] if r else '')")
[ -z "$jobs_url" ] && { echo "FAIL: No runs found"; exit 1; }
echo "$runs" | python3 -c "import json,sys; r=json.load(sys.stdin)['workflow_runs'][0]; print('latest run:', r['id'], r['name'], r['head_branch'], r['status'], r['conclusion'], r['created_at'])"

curl -s "$jobs_url" | EMAIL="$EMAIL" python3 -c "
import json, os, sys
email = os.environ['EMAIL']
names = [s['name'] for j in json.load(sys.stdin)['jobs'] for s in j.get('steps', [])]
print('step names:', ['<email>' if n == email else n for n in names])
ok = any(email in n for n in names)
print('PASS: a step name contains the email' if ok else 'FAIL: No step matches the email')
sys.exit(0 if ok else 1)
"
