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
