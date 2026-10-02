#!/usr/bin/env bash
set -euo pipefail
# Start with: uvicorn app.main:app --reload
curl -X POST http://localhost:8000/v1/run -H 'content-type: application/json' -d '{"value":"Hello World"}'
