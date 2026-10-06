# Vercel FastAPI entrypoint (the framework preset looks for main.py / app.py / index.py and an `app` object).
# The app itself lives in api/index.py; Vercel routes every path to this app, so no vercel.json rewrite is needed.
from api.index import app  # noqa: F401
