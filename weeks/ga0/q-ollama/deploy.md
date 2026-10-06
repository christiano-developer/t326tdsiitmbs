# Deploy guide — q-ollama

> Local processes + tunnel. **Both must keep running until grading closes.** No secrets in the repo.

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Local Ollama + ngrok (free tier) |
| Public URL    | `https://<random>.ngrok-free.dev` (changes on every ngrok restart; graded: `https://unluckily-barber-cultivate.ngrok-free.dev`) |
| Runtime       | Ollama 0.17.5, ngrok 3.39.11 |
| Required      | ngrok authtoken (`ngrok config add-authtoken …`, stored in `~/Library/Application Support/ngrok/ngrok.yml`) |

## Prerequisites

- [x] `ollama` installed; the Ollama **desktop app quit** (it ignores terminal env vars)
- [x] `brew install ngrok`; free account at ngrok.com; `ngrok config add-authtoken <token>` (run it yourself; it's secret)
- [x] `cp src/traffic-policy.example.yml traffic-policy.local.yml` and put the exam email in `X-Email` (git-ignored)

## 1. Run Ollama with CORS (Terminal A)

```bash
OLLAMA_ORIGINS="*" ollama serve
```

## 2. Test locally

```bash
curl -s http://localhost:11434/api/version            # {"version":"…"}
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:11434/api/version -H "Host: x.ngrok-free.dev"   # 403 = Host check active
```

## 3. Tunnel (Terminal B)

```bash
cd weeks/ga0/q-ollama
ngrok http 11434 --host-header=rewrite --traffic-policy-file traffic-policy.local.yml
```

`traffic-policy.local.yml` adds `X-Email`, `Access-Control-Expose-Headers: *` and
`Access-Control-Allow-Headers: …,Ngrok-skip-browser-warning` to every response.

## 4. Test the public URL (grader replica)

```bash
weeks/ga0/q-ollama/src/check_ngrok.sh https://<random>.ngrok-free.dev "<my-exam-email>"    # expect ALL CHECKS PASS
```

## 5. Keep alive until graded

Leave Terminals A and B running (and the laptop awake). If ngrok restarts, the URL changes: re-run step 4 and resubmit.

## Teardown (after grading)

```bash
# Ctrl+C in Terminal B (ngrok) and Terminal A (ollama serve)
ngrok config add-authtoken <NEW-token>     # after resetting the token on the ngrok dashboard (it was pasted in chat)
```

## Troubleshooting log

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ERROR: Malformed header: Content-Type` | ngrok 3.39 deprecated `--response-header-add`; it splits values on commas | traffic policy file (`add-headers`) |
| ngrok log: `OPTIONS 204`, then `GET 403`; exam: "Unexpected end of JSON input" | Ollama rejects non-localhost `Host` (DNS-rebinding protection) | `--host-header=rewrite` (or bind Ollama to 0.0.0.0) |
