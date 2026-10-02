# Semantic LLM Cache

A runnable FastAPI reference implementation for canonicalizing prompts and serving repeat requests from a TTL cache.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

POST `{"value":"Hello World"}` to `/v1/run`. Repeated equivalent whitespace/case variants demonstrate a cache hit.

## Production extensions
Use embeddings or model-specific canonicalization, Redis for distributed storage, namespace-aware invalidation, token/cost accounting, and cache safety policies for user-specific data.
