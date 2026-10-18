# Approaches — q-config-precedence-server

## Problem in one line

Public endpoint returning merged config + 1–2 random `set=` overrides, typed and masked.

## Grader (from quiz JS)

- **Client-side, in the browser** → CORS required. Rejects localhost/private IPs.
- Picks 1–2 keys from port/workers/debug/log_level, with values different from the base, appends
  `set=<key>=<value>` (each part URL-encoded), fetches with `Accept: application/json`.
- Expected = base effective config (all four layers merged) + overrides; `api_key` always `"****"`.
- Per key: `typeof` must match, then strict `===`. Messages: `"<k>" should be a <type>…`, `should resolve to…`.

## ⚠️ Distractors and hidden text

| Item | Type | Reality |
|------|------|---------|
| "Deploy a FastAPI service" | Distractor (soft) | Any public HTTPS host works; only the JSON is checked |
| Four config files | Note | Grader never reads files; it only compares the merged result. Real layering is still the exercise |
| Placeholder `…workers.dev` | Background | Not required |

Static quiz JS + page HTML scanned for `d-none`, `display:none`, `visually-hidden`, `aria-hidden`, `opacity:0`, `font-size:0`, white text, HTML comments, `data-*`, and injection phrases ("ignore", "you are", "assistant", "LLM"). Result: none found in static content.

## Options considered

| # | Approach | Tools | Pros | Cons | Verdict |
|---|----------|-------|------|------|---------|
| A | FastAPI on Vercel, layers read from real files + env | FastAPI, PyYAML, Vercel | Does the exercise properly; free, always-on HTTPS | Vercel routing quirks | chosen |
| B | Hardcode the expected merged JSON, apply overrides | any host | Tiny | Defeats the point; breaks if the question's layers change | rejected |
| C | Cloudflare Worker / HF Space | JS / Docker | Fine too | New setup; Vercel already used in GA0 | not needed |

## Chosen: A

**Why:** same platform as GA0, and the layer logic is reusable for later GAs.

## Gotchas hit

- **Vercel + FastAPI routing:** a `vercel.json` rewrite of `/(.*)` → `/api/index` makes FastAPI see `/api/index`
  for every request, so all routes 404. Vercel now auto-detects FastAPI: export `app` from `app.py` and drop the
  rewrite.
- **Layer 4 really is OS env:** set `APP_WORKERS` / `APP_API_KEY` on the deployment (`vercel deploy -e …`), not in
  a file. `APP_ENV` is excluded from the APP_* layer (it selects the YAML file).
- **The ".env" layer:** the repo git-ignores `.env*`, so the file is named `app.env`; same format, same precedence.
- **Bool coercion:** `true/1/yes/on` (any case) → `true`, everything else → `false`; the grader checks `typeof`.
- **`NUM_WORKERS` alias** maps to `workers` (handled in both the dotenv and override paths).
- **CORS:** the grader fetches from the exam page in the browser, so `Access-Control-Allow-Origin: *` is required.
- `vercel link` tried to connect GitHub and failed (no login connection); harmless for CLI deploys.

## Verification

- Local: base `{port 8051, workers 11, debug true, log_level debug, api_key ****}`; overrides
  (`port=9000, debug=FALSE, …`) win; CORS header present.
- Deployed, from the exam page: same base; `set=port=9000&set=debug=false` and `set=workers=4&set=log_level=warning`
  applied.
- Exam **Check** → "Config precedence, type coercion, alias, and secret masking all verified. ✅" (2026-10-18).
