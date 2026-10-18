# Final — q-config-precedence-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga1/q-config-precedence-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga1/q-config-precedence-server)

## How to solve (for a teammate)

> Seeded per email: the values in all four layers come from **your** question. Copy them from the page; the code
> doesn't change.

**Approach:** a tiny FastAPI service that rebuilds the config the 12-factor way — start from defaults, overlay the
environment's YAML file, then the dotenv file, then real `APP_*` environment variables, then `?set=key=value` query
overrides — coerce types at the end, and mask `api_key`. Deploy it on Vercel with layer 4 set as deployment env vars.

1. Make a folder `src/` with the files below. Put your layer-2 values in `config.development.yaml` and your
   layer-3 values in `app.env` (it plays the role of `.env`; any `APP_*` keys, `NUM_WORKERS` allowed).
2. Test locally (needs [uv](https://docs.astral.sh/uv/)):
   `APP_WORKERS=<n> APP_API_KEY=<key> uv run --with fastapi --with pyyaml --with uvicorn uvicorn app:app --port 8000`,
   then open `http://localhost:8000/effective-config` and `…?set=port=9000&set=debug=false`.
3. Deploy (Vercel CLI, logged in): in `src/` run `vercel link --yes --project <any-name>` then
   `vercel deploy --prod -e APP_WORKERS=<n> -e APP_API_KEY=<key>` with your layer-4 values.
4. Submit `https://<the Aliased URL>/effective-config`, Check, Save. Don't use `vercel.json` rewrites (see gotchas).

<details><summary>src/api/index.py (click to expand)</summary>

```python
"""12-factor config precedence service (TDS GA1 q-config-precedence-server).

Layers, low -> high precedence:
  1. defaults (hardcoded)
  2. config.<APP_ENV>.yaml          (APP_ENV defaults to "development")
  3. dotenv file (app.env here)     (APP_* keys; NUM_WORKERS is an alias for workers)
  4. OS environment (APP_* prefix)
  5. ?set=key=value query params    (CLI-style overrides, repeatable)
api_key is always masked as "****".
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parent.parent

DEFAULTS = {"port": 8000, "workers": 1, "debug": False, "log_level": "info", "api_key": "default-secret-000"}
TRUE = {"true", "1", "yes", "on"}
ALIASES = {"num_workers": "workers"}


def coerce(key: str, value):
    if key in ("port", "workers"):
        return int(str(value).strip())
    if key == "debug":
        return value if isinstance(value, bool) else str(value).strip().lower() in TRUE
    return str(value)


def norm_key(key: str) -> str:
    k = key.strip().lower()
    return ALIASES.get(k, k)


def read_dotenv(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k.startswith("APP_"):
            out[norm_key(k[4:])] = v
        elif k.upper() in ("NUM_WORKERS",):
            out["workers"] = v
    return out


def env_layer() -> dict:
    return {norm_key(k[4:]): v for k, v in os.environ.items() if k.startswith("APP_") and k != "APP_ENV"}


def effective(overrides: list[str]) -> dict:
    cfg = dict(DEFAULTS)
    env_name = os.environ.get("APP_ENV", "development")
    yml = ROOT / f"config.{env_name}.yaml"
    layers = [
        yaml.safe_load(yml.read_text(encoding="utf-8")) if yml.exists() else {},
        read_dotenv(ROOT / "app.env"),
        env_layer(),
    ]
    for layer in layers:
        for k, v in (layer or {}).items():
            cfg[norm_key(k)] = v
    for item in overrides:
        if "=" in item:
            k, v = item.split("=", 1)
            cfg[norm_key(k)] = v
    out = {k: coerce(k, v) for k, v in cfg.items()}
    out["api_key"] = "****"
    return out


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/effective-config")
def effective_config(request: Request):
    return effective(request.query_params.getlist("set"))


@app.get("/")
def root():
    return {"ok": True, "endpoint": "/effective-config?set=key=value"}
```

</details>

<details><summary>src/app.py, requirements.txt, config.development.yaml, app.env (click to expand)</summary>

```python
# app.py — Vercel's FastAPI entrypoint
from api.index import app  # noqa: F401
```

```text
# requirements.txt
fastapi
pyyaml
```

```yaml
# config.development.yaml — layer 2 (your values)
port: <from your question>
debug: <true|false>
log_level: <from your question>
```

```bash
# app.env — layer 3, the ".env file" (your values)
APP_PORT=<from your question>
APP_DEBUG=<from your question>
```

Also add an empty `api/__init__.py`.

</details>

## Final prompt

```text
Write a FastAPI app for Vercel exposing GET /effective-config that merges config layers low→high:
hardcoded defaults (port 8000, workers 1, debug false, log_level info, api_key default-secret-000),
config.<APP_ENV or development>.yaml, a dotenv file (APP_* keys, NUM_WORKERS aliases workers), OS env vars
with the APP_ prefix (excluding APP_ENV), then repeatable ?set=key=value overrides. Coerce port/workers to int,
debug to bool (true/1/yes/on, any case), others to str; always return api_key as "****"; allow CORS from *.
Export the app from app.py (Vercel FastAPI preset) and don't use vercel.json rewrites.
```

- **Tool / model used:** Claude (Claude Opus 5.5).

## Reproduction steps (needs a clone of this repo)

See [deploy.md](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga1/q-config-precedence-server/deploy.md):
run locally with your layer-4 env values, then `vercel deploy --prod -e …` from `src/`.

## Expected output

```json
{"port": <int>, "workers": <int>, "debug": <bool>, "log_level": "<str>", "api_key": "****"}
```

## Answer submitted (✅ Check passed)

The deployed `/effective-config` URL (see README).
